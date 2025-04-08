from user.models import Users
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_user(sender, **kwargs):
    if not Users.objects.filter(email='admin@admin.com').exists():
        Users.objects.create_superuser(email='admin@admin.com', password='123456789', username='admin', telefone='123456789', nif='123456789')

