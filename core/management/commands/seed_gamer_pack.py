from django.core.management.base import BaseCommand
from core.models import SkillNode, StoreItem, Badge

class Command(BaseCommand):
    help = 'Popula dados iniciais do Pacote Gamer'

    def handle(self, *args, **options):
        # Skills
        python = SkillNode.objects.get_or_create(name='Python', slug='python', defaults={'icon_class': 'fab fa-python', 'description': 'Linguagem de programação versátil'})[0]
        js = SkillNode.objects.get_or_create(name='JavaScript', slug='javascript', defaults={'icon_class': 'fab fa-js', 'description': 'Linguagem web essencial'})[0]
        django = SkillNode.objects.get_or_create(name='Django', slug='django', parent=python, defaults={'icon_class': 'fas fa-server', 'description': 'Framework web Python'})[0]
        react = SkillNode.objects.get_or_create(name='React', slug='react', parent=js, defaults={'icon_class': 'fab fa-react', 'description': 'Biblioteca UI moderna'})[0]
        
        # Store Items
        StoreItem.objects.get_or_create(name='Moldura Bronze', category='FRAME', defaults={'price': 100, 'css_class': 'frame-bronze'})
        StoreItem.objects.get_or_create(name='Moldura Prata', category='FRAME', defaults={'price': 250, 'css_class': 'frame-silver'})
        StoreItem.objects.get_or_create(name='Moldura Ouro', category='FRAME', defaults={'price': 500, 'css_class': 'frame-gold'})
        StoreItem.objects.get_or_create(name='Banner Neon', category='BANNER', defaults={'price': 300, 'css_class': 'banner-neon'})
        
        # Badges
        Badge.objects.get_or_create(slug='first-session', defaults={'name': 'Primeira Sessão', 'description': 'Complete sua primeira sessão de estudo', 'icon_class': 'fas fa-star', 'xp_bonus': 50, 'coin_bonus': 25})
        Badge.objects.get_or_create(slug='streak-7', defaults={'name': 'Semana Completa', 'description': '7 dias de streak', 'icon_class': 'fas fa-fire', 'xp_bonus': 200, 'coin_bonus': 100})
        
        self.stdout.write(self.style.SUCCESS('Pacote Gamer populado com sucesso!'))
