"""
WSGI config for charbot_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/bitnami/canatrace-chatbot')
sys.path.append('/home/bitnami/canatrace-chatbot/charbot_api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'charbot_api.settings')

application = get_wsgi_application()
path = '/home/bitnami/canatrace-chatbot/'
