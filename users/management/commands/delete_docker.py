import os
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Execute the command lines in order to delete containers and images"""
        os.system('sudo docker compose down')
        os.system('sudo docker rmi $(sudo docker images)')
