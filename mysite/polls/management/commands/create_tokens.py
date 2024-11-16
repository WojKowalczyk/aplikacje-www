from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = "Create a token for every user in the database"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f"Token created for user {user.username}: {token.key}")
            else:
                self.stdout.write(f"Token already exists for user {user.username}: {token.key}")
