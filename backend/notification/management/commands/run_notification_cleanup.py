
import time
import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run notification cleanup every 60 minutes."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Notification scheduler started.")
        )

        while True:
            try:
                self.stdout.write("Checking expired notifications...")

                call_command("cleanup_notifications")

            except Exception:
                logger.exception(
                    "Notification cleanup failed."
                )

            self.stdout.write(
                "Next notification cleanup in 60 minutes."
            )

            time.sleep(3600)
