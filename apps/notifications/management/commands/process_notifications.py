"""
Management command para procesar notificaciones pendientes.

Ejecución manual:
    python manage.py process_notifications

Ejecución cada 5 minutos (cron / task scheduler):
    # Linux (crontab):
    */5 * * * * cd /ruta/proyecto && venv/bin/python manage.py process_notifications

    # Windows (Task Scheduler):
    C:\ruta\venv\Scripts\python.exe manage.py process_notifications

Flags:
    --max N        Máximo de notificaciones a procesar (default: 50)
    --retry        También reintenta notificaciones fallidas
    --dry-run      Simula sin enviar realmente
    --verbose      Log detallado
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
import logging


class Command(BaseCommand):
    help = 'Procesa las notificaciones pendientes de envío (recordatorios, etc.)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max',
            type=int,
            default=50,
            help='Máximo de notificaciones a procesar (default: 50)',
        )
        parser.add_argument(
            '--retry',
            action='store_true',
            help='Reintentar notificaciones fallidas',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular sin enviar realmente',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Log detallado',
        )

    def handle(self, *args, **options):
        level = logging.DEBUG if options['verbose'] else logging.INFO
        logging.basicConfig(level=level)

        from apps.notifications.services.notification_service import NotificationService

        service = NotificationService()
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        self.stdout.write(self.style.NOTICE(
            f'[{timestamp}] Procesando notificaciones pendientes...'
        ))

        if options['dry_run']:
            from apps.notifications.models import NotificationLog
            from apps.core.models import NotificationStatus

            pending_count = NotificationLog.objects.filter(
                status=NotificationStatus.PENDING,
                scheduled_at__lte=timezone.now(),
            ).count()

            self.stdout.write(self.style.WARNING(
                f'[DRY-RUN] {pending_count} notificaciones pendientes detectadas.'
            ))
            return

        results = service.process_pending(max_notifications=options['max'])
        self._report(results)

        if options['retry']:
            self.stdout.write(self.style.NOTICE('Reintentando fallidas...'))
            retry_results = service.retry_failed()
            self._report(retry_results, prefix='Reintentos')

    def _report(self, results: dict, prefix: str = 'Resultado'):
        sent = results.get('sent', 0)
        failed = results.get('failed', 0)
        skipped = results.get('skipped', 0)

        if sent:
            self.stdout.write(self.style.SUCCESS(f'{prefix}: {sent} enviadas ✅'))
        if failed:
            self.stdout.write(self.style.ERROR(f'{prefix}: {failed} fallidas ❌'))
        if skipped:
            self.stdout.write(self.style.WARNING(
                f'{prefix}: {skipped} pendientes de reintento ↻'
            ))

        if not sent and not failed and not skipped:
            self.stdout.write(self.style.NOTICE('Sin notificaciones pendientes.'))
