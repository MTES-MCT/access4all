from django.core.management.base import BaseCommand

from erp.provider import pagesjaunes


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("what", type=str, help="Activité")
        parser.add_argument("where", type=str, help="Lieu")

    def handle(self, *args, **options):
        try:
            pagesjaunes.search(what=options.get("what"), where=options.get("where"))
        except KeyboardInterrupt:
            print("Interrompu.")
