from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.budget.models import Budget, Upload, UploadLog, TransparencyIndex, Expense, Revenue, BudgetSummary


class Command(BaseCommand):
    help = "Creates groups."

    def handle(self, *args, **options):
        def create_default_perms(group, models):
            for m in models:
                ct = ContentType.objects.get_for_model(m)
                perms = Permission.objects.filter(content_type=ct)
                group.permissions.add(*list(perms))

        group, created = Group.objects.get_or_create(name="CSO Master")
        print(f"Creating permissions for {group.name}")
        group.permissions.add(Permission.objects.get(codename="view_profile"))
        create_default_perms(group, [
            User,
            Budget,
            BudgetSummary,
            Upload,
            UploadLog,
            TransparencyIndex,
            Expense,
            Revenue,
        ])

        group, created = Group.objects.get_or_create(name="CSO Team")
        print(f"Creating permissions for {group.name}")
        create_default_perms(group, [
            Budget,
            BudgetSummary,
            Upload,
            UploadLog,
            TransparencyIndex,
            Expense,
            Revenue,
        ])
