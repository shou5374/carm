from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import UserCreationForm, GroupCreationForm
from django.contrib.auth import login
from .models import User, UserGroup
from common.view_utils import common_process

class SignUpView(TemplateView):
    template_name = "users/sign_up.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": UserCreationForm(),
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'sign_up':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('order:home') # 本当はhomeへ遷移
            else:
                return render(request, self.template_name, {'form': form})


class CreateGroupView(TemplateView):
    template_name = "users/create_group.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return render(request, self.template_name, {
            "form": GroupCreationForm(),
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'create_group':
            form = GroupCreationForm(request.POST)
            if form.is_valid():
                group = form.save(user=request.user)
                request.user.active_group = group
                request.user.save()
                return redirect('order:home')
            else:
                return render(request, self.template_name, {'form': form})


class ChangeGroupView(TemplateView):
    template_name = "users/change_group.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return render(request, self.template_name, {
            "groups": UserGroup.objects.filter(leader=request.user),
        })

    def post(self, request, **kwargs):
        if self.request.POST['action'] == 'change_group':
            pass


class ManageAndSearchGroupView(TemplateView):
    template_name = "users/manage_and_search_group.html"

    session_keys = [("searched_group_name", None)] # (post_key, default_obj)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        session_info = {k: request.session[k] if k in request.session.keys() else default_v for k, default_v in self.session_keys}
        searched_group_name = session_info['searched_group_name']
        member_status = "not_application"
        if searched_group_name is not None:
            try:
                group = UserGroup.objects.get(name=searched_group_name)
                if request.user in group.unapproved_members.all():
                    # print("未承認メンバーに所属")
                    member_status = "unapproved"
                elif request.user in group.members.all():
                    # print("承認済みメンバーに所属")
                    member_status = "approved"
            except:
                pass
        return render(request, self.template_name, {
            "searched_group_name": searched_group_name,
            "member_status": member_status,
            "belong_groups": request.user.members.all(), # related_nameを用いた逆参照 # https://hamaguchictrlz.hatenablog.com/entry/2019/02/10/221143
        })

    def post(self, request, **kwargs):
        if 'action' in self.request.POST.keys():
            if self.request.POST['action'] == 'search_group':
                searched_group_name = self.request.POST['searched_group_name']
                try:
                    group = UserGroup.objects.get(name=searched_group_name)
                    request.session['searched_group_name'] = group.name
                except:
                    request.session['searched_group_name'] = None
            elif self.request.POST['action'] == 'application':
                search_result = self.request.POST['search_result']
                try:
                    # print("承認申請")
                    group = UserGroup.objects.get(name=search_result)
                    group.unapproved_members.add(request.user)
                    group.save()
                except:
                    pass
            elif self.request.POST['action'] == 'activation':
                group_name = self.request.POST['group_name']
                group = UserGroup.objects.get(name=group_name)
                user = User.objects.get(pk=request.user.pk)
                user.active_group = group
                user.save()
                
        return redirect('users:manage_and_search_group')


class ManageGroupView(TemplateView):
    template_name = "users/manage_group.html"

    session_keys = [] # (post_key, default_obj)

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        group_name = self.kwargs.get('group_name')
        group = UserGroup.objects.get(name=group_name)

        if group.leader != request.user: # グループリーダー出ない場合は戻す.
            return redirect('users:login')

        return render(request, self.template_name, {
            "group": group,
            "members": group.members.all(),
            "unapproved_members": group.unapproved_members.all(),
            
        })

    def post(self, request, **kwargs):
        if 'action' in self.request.POST.keys():
            group_name = self.request.POST['group_name']
            member_email = self.request.POST['member_email']
            group = UserGroup.objects.get(name=group_name)
            target_user = User.objects.get(email=member_email)
            if self.request.POST['action'] == 'remove_member':
                group.members.remove(target_user)
            elif self.request.POST['action'] == 'approve':
                group.unapproved_members.remove(target_user)
                group.members.add(target_user)
            elif self.request.POST['action'] == 'remove_application':
                group.unapproved_members.remove(target_user)
            group.save()
        return redirect('users:manage_group', group_name=group_name)