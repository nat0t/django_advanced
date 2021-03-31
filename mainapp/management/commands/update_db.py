from django.core.management.base import BaseCommand
from authapp.models import ShopUser as User
from authapp.models import ShopUserProfile as UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            users_profile = UserProfile.objects.create(user=user)
            users_profile.save()
