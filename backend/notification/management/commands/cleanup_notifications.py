
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from notification.models import Notification
from core.cache.invalidation import invalidate_notification_cache


class Command(BaseCommand):
    help = "Delete notifications older than 24 hours."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many notifications would be deleted without deleting them.",
        )

    def handle(self, *args, **options):
        cutoff_time = timezone.now() - timedelta(days=1)

        old_notifications = Notification.objects.filter(
            created_at__lt=cutoff_time
        )

        total = old_notifications.count()

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(
                    f"DRY RUN: {total} expired notifications found."
                )
            )
            return

        # Identify affected users before deleting notifications.
        recipient_ids = list(
            old_notifications.values_list(
                "recipient_id", flat=True
            ).distinct()
        )

        deleted_count, _ = old_notifications.delete()

        # Invalidate affected users' notification caches.
        for recipient_id in recipient_ids:
            invalidate_notification_cache(recipient_id)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully deleted {deleted_count} expired notification records."
            )
        )
