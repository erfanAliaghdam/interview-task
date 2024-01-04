from django.core.management.base import BaseCommand
from core.seeds import generate_development_seed
from django.core.management import call_command
import logging
import time

logging.disable(logging.WARNING)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="Answer yes to all prompts",
        )

    def handle(self, *args, **options):
        user_input = ""
        if not options["yes"]:
            user_input = input(
                "Do you want to flush the database ( generating seed without"
                " flushing can cause errors )? (yes-y/no-n): "
            ).lower()

        if options["yes"] or user_input in ["y", "yes"]:
            self.stdout.write(self.style.SUCCESS("Flushing the database... ."))
            call_command("flush", interactive=False)
            self.stdout.write(self.style.SUCCESS("Database flushed successfully"))
        else:
            self.stdout.write(self.style.WARNING("Skipping Flushing the database... ."))
            self.stdout.write(
                self.style.WARNING(
                    "Flushing disabled, this may cause error on generating data..."
                )
            )
        time.sleep(3)
        self.stdout.write(self.style.SUCCESS("------------generating data------------"))
        generate_development_seed()
        self.stdout.write(self.style.SUCCESS("Database generated successfully ."))
