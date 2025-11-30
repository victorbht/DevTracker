from django.core.management.base import BaseCommand

from core.badges import seed_badges


class Command(BaseCommand):
    help = "Cria/atualiza conquistas padrão (tempo, tecnologia e streak)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep-existing",
            action="store_true",
            help="Não apaga conquistas existentes antes de popular.",
        )

    def handle(self, *args, **options):
        reset = not options["keep_existing"]
        count = seed_badges(reset=reset)
        scope = "resetado" if reset else "atualizado"
        self.stdout.write(self.style.SUCCESS(f"{count} badges {scope}(s)."))
