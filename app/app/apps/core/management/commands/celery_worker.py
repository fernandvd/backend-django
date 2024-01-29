import shlex
import subprocess
from typing import Any

from django.core.management.base import BaseCommand
from django.utils import autoreload 

def restart_celery():
    celery_worker_cmd = 'celery -A app worker'
    cmd = f'pkill -f "{celery_worker_cmd}"'
    subprocess.call(shlex.split(cmd))
    subprocess.call(shlex.split(f"{celery_worker_cmd} -l INFO"))

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write(self.style.SUCCESS("Stating celery worker with autoreload ..."))
        autoreload.run_with_reloader(restart_celery)