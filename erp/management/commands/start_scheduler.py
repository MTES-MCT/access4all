import schedule
import time

from django.core.management.base import BaseCommand

from erp.jobs import check_closed_erps


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        schedule.every().day.at("00:00").do(check_closed_erps.job, verbose=True)
        print("Scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(1)