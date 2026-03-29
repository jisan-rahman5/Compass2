import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "compass.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User

try:
    users = User.objects.all()
    print("Users in DB:", users)
    for user in users:
        print(f"Testing dashboard for user: {user.username}")
        client = Client()
        client.force_login(user)
        response = client.get('/dashboard/')
        print("  STATUS CODE:", response.status_code)
        if response.status_code != 200:
            print("  ERROR CONTENT:")
            content = response.content.decode('utf-8')
            if 'Exception Value:' in content:
                start = content.find('Exception Value:')
                end = content.find('\n', start + 100)
                print("  ", content[start:end])
            else:
                print("  ", content[:1000])
except Exception as e:
    import traceback
    traceback.print_exc()
