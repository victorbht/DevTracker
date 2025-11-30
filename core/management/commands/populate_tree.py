from django.core.management.base import BaseCommand
from core.models import SkillNode

class Command(BaseCommand):
    help = 'Popula árvore de habilidades Fullstack Python'

    def handle(self, *args, **kwargs):
        self.stdout.write("Criando árvore...")

        root, _ = SkillNode.objects.get_or_create(
            name="Lógica de Programação", slug="logica", 
            defaults={'description': 'Fundamentos: variáveis, loops, condicionais.', 'icon_class': 'fas fa-brain'}
        )

        python, _ = SkillNode.objects.get_or_create(
            name="Python", slug="python", 
            defaults={'parent': root, 'description': 'Linguagem Python.', 'icon_class': 'fab fa-python'}
        )
        git, _ = SkillNode.objects.get_or_create(
            name="Git & GitHub", slug="git", 
            defaults={'parent': root, 'description': 'Versionamento.', 'icon_class': 'fab fa-git-alt'}
        )
        sql, _ = SkillNode.objects.get_or_create(
            name="SQL", slug="sql", 
            defaults={'parent': root, 'description': 'Banco de dados.', 'icon_class': 'fas fa-database'}
        )
        html, _ = SkillNode.objects.get_or_create(
            name="HTML/CSS", slug="html-css", 
            defaults={'parent': root, 'description': 'Frontend básico.', 'icon_class': 'fab fa-html5'}
        )

        django, _ = SkillNode.objects.get_or_create(
            name="Django", slug="django", 
            defaults={'parent': python, 'description': 'Framework web.', 'icon_class': 'fas fa-leaf'}
        )
        api, _ = SkillNode.objects.get_or_create(
            name="APIs REST", slug="apis", 
            defaults={'parent': python, 'description': 'Comunicação entre sistemas.', 'icon_class': 'fas fa-exchange-alt'}
        )
        js, _ = SkillNode.objects.get_or_create(
            name="JavaScript", slug="js", 
            defaults={'parent': html, 'description': 'Interatividade.', 'icon_class': 'fab fa-js'}
        )
        docker, _ = SkillNode.objects.get_or_create(
            name="Docker", slug="docker", 
            defaults={'parent': git, 'description': 'Containers.', 'icon_class': 'fab fa-docker'}
        )

        SkillNode.objects.get_or_create(
            name="Arquitetura", slug="arch", 
            defaults={'parent': django, 'description': 'Clean Arch, DDD.', 'icon_class': 'fas fa-archway'}
        )
        SkillNode.objects.get_or_create(
            name="React", slug="react", 
            defaults={'parent': js, 'description': 'UI reativa.', 'icon_class': 'fab fa-react'}
        )
        SkillNode.objects.get_or_create(
            name="DevOps", slug="devops", 
            defaults={'parent': docker, 'description': 'CI/CD.', 'icon_class': 'fas fa-cogs'}
        )

        self.stdout.write(self.style.SUCCESS('Árvore criada! 🌳'))
