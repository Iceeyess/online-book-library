import os
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Execute the command lines and upload to docker server and run containers"""
        os.system('sudo docker compose build')
        os.system('sudo docker compose up -d')
