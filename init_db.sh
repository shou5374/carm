rm -rf users/migrations
rm -rf car/migrations
rm -rf book/migrations
rm -rf db.sqlite3

python manage.py makemigrations users
python manage.py makemigrations car
python manage.py makemigrations book
python manage.py migrate

# superuserの作成
echo "from users.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

# Team independentを作成. independentはGuestもデフォルトでアクセス可能なチーム. superuserのactive_groupをindependentに設定
echo "from users.models import User, UserGroup;user=User.objects.get(email='admin@example.com');groupname='independent';new_usergroup=UserGroup.objects.create(name=groupname, leader=user); new_usergroup.members.add(user);new_usergroup.save();user.active_group=new_usergroup;user.save()" | python manage.py shell

# CarType登録
echo "from car.models import CarType; CarType.objects.create(name='passenger');CarType.objects.create(name='van');CarType.objects.create(name='truck');CarType.objects.create(name='special');" | python manage.py shell

# サンプル車両登録
echo "from car.models import Car, CarType; from users.models import UserGroup; group=UserGroup.objects.get(name='independent'); type_name=CarType.objects.get(name='passenger');Car.objects.create(name='1-99999999', group=group, category=type_name, image='images/car/kei1.jpg'); Car.objects.create(name='1-555555', group=group, category=type_name, image='images/car/kei2.jpg');Car.objects.create(name='1-34343', group=group, category=type_name, image='images/car/sport_car1.jpg');Car.objects.create(name='1-6666', group=group, category=type_name, image='images/car/zeep1.jpg');" | python manage.py shell
echo "from car.models import Car, CarType; from users.models import UserGroup; group=UserGroup.objects.get(name='independent'); type_name=CarType.objects.get(name='van');Car.objects.create(name='2-943199', group=group, category=type_name, image='images/car/wagon1.jpg');" | python manage.py shell
echo "from car.models import Car, CarType; from users.models import UserGroup; group=UserGroup.objects.get(name='independent'); type_name=CarType.objects.get(name='truck');Car.objects.create(name='3-943199', group=group, category=type_name, image='images/car/truck1.jpg');" | python manage.py shell
echo "from car.models import Car, CarType; from users.models import UserGroup; group=UserGroup.objects.get(name='independent'); type_name=CarType.objects.get(name='special');Car.objects.create(name='4-943199', group=group, category=type_name, image='images/car/dump1.jpg'); Car.objects.create(name='4-413425', group=group, category=type_name, image='images/car/mixer1.jpg');" | python manage.py shell
