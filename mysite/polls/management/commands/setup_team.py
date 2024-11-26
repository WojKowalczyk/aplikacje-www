from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from polls.models import Osoba  # Replace `polls` with your app name


class Command(BaseCommand):
    help = "Sets up the 'Osoba Managers' group, assigns permissions, and creates a team user."

    def handle(self, *args, **kwargs):
        # Create the group
        group_name = "Osoba Managers"
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(f"Group '{group_name}' created.")
        else:
            self.stdout.write(f"Group '{group_name}' already exists.")

        # Add permission to the group
        osoba_ct = ContentType.objects.get_for_model(Osoba)
        permission = Permission.objects.get(codename='change_osoba', content_type=osoba_ct)
        group.permissions.add(permission)
        self.stdout.write(f"Added permission '{permission.codename}' to group '{group_name}'.")

        # Create a new user
        username = "team_member"
        password = "securepassword123"
        user, user_created = User.objects.get_or_create(username=username)

        if user_created:
            user.set_password(password)
            user.is_staff = True  # Allow access to the admin panel
            user.is_superuser = False  # Not a superuser
            user.save()
            self.stdout.write(f"User '{username}' created with password '{password}'.")
        else:
            self.stdout.write(f"User '{username}' already exists.")

        # Assign the user to the group
        user.groups.add(group)
        self.stdout.write(f"User '{username}' added to group '{group_name}'.")
