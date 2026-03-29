import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "compass.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User

try:
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(username='testuser', password='testpass')
    
    client = Client()
    client.force_login(user)
    
    response = client.get('/dashboard/')
    print("STATUS CODE:", response.status_code)
    if response.status_code != 200:
        print("ERROR CONTENT:")
        # Dump a bit of the error if it's a 500
        content = response.content.decode('utf-8')
        if 'Exception Value:' in content:
            start = content.find('Exception Value:')
            end = content.find('\n', start + 100)
            print(content[start:end])
        else:
            print(content[:1000])
except Exception as e:
    import traceback
    traceback.print_exc()
