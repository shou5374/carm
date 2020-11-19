from django import forms
from .models import User, UserGroup
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.hashers import make_password

class UserCreationForm(forms.Form):
    username = forms.CharField(
        label=_('username'),
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'username',
        }),
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    email = forms.EmailField(
        label=_('email address'),
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'email'
        })
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'password',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ("username", 'email')

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', '既に登録済みのメールアドレスです')
        self.cleaned_data['password1'] = make_password(self.cleaned_data['password1'])
        return self.cleaned_data

    def save(self):
        data = self.cleaned_data
        usergroup = UserGroup.objects.get(name="independent")
        new_user = User.objects.create(username=data['username'], email=data['email'], password=data['password1'], active_group=usergroup)
        new_user.save()
        usergroup.members.add(new_user)
        usergroup.save()
        return new_user
        
        
class GroupCreationForm(forms.Form):
    groupname = forms.CharField(
        label=_('groupname'),
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'group name',
        }),
        help_text=_('Required. 15 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    
    class Meta:
        model = UserGroup
        fields = ['groupname']

    def clean(self):
        groupname = self.cleaned_data.get('groupname')
        if UserGroup.objects.filter(name=groupname).exists():
            self.add_error('groupname', '既に使われているのグループ名です')
        return self.cleaned_data

    def save(self, user=None):
        groupname = self.cleaned_data.get('groupname')
        new_usergroup = UserGroup.objects.create(name=groupname, leader=user)
        new_usergroup.members.add(user)
        new_usergroup.save()
        return new_usergroup
