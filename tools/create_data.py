from django.core.wsgi import get_wsgi_application
from pathlib import Path
import sys
import os

project_path = Path.cwd()
sys.path.extend([str(project_path), f'{project_path}/apps'])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms.settings')
get_wsgi_application()


from apps.goods.models import Category, Goods
from apps.warehouse.models import Warehouse
from apps.purchase.models import Supplier
from apps.user.models import User, Teams
from apps.account.models import Account
from apps.sales.models import Client

teams = Teams.objects.create(phone='18571589816', company_name='test')
user = User(username='test', name='test', phone='18571589816', teams=teams)
user.set_password('test')
user.save()

Warehouse.objects.create(number='1001', name='warehouse1', teams=teams)
Warehouse.objects.create(number='1002', name='warehouse2', teams=teams)
Supplier.objects.create(number='1001', name='supplier1', teams=teams)
Supplier.objects.create(number='1002', name='supplier2', teams=teams)
Client.objects.create(number='1001', name='client1', teams=teams)
Client.objects.create(number='1002', name='client2', teams=teams)
Category.objects.create(number='1001', name='category1', teams=teams)
Category.objects.create(number='1002', name='category2', teams=teams)
Goods.objects.create(number='1001', name='goods1', teams=teams)
Goods.objects.create(number='1002', name='goods2', teams=teams)
Goods.objects.create(number='1003', name='goods3', teams=teams)
Account.objects.create(number='1001', name='account1', teams=teams)
Account.objects.create(number='1002', name='account2', teams=teams)
