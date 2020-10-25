from django.core.wsgi import get_wsgi_application
from pathlib import Path
import sys
import os

project_path = Path.cwd()
sys.path.extend([str(project_path), f'{project_path}/apps'])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms.settings')
get_wsgi_application()

from apps.user.models import User, Teams
teams = Teams.objects.create(phone='18571589816', company_name='test')
user = User(username='test', name='test', phone='18571589816', teams=teams)
user.set_password('test')
user.save()
