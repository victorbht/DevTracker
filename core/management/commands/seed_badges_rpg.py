from django.core.management.base import BaseCommand
from core.models import Badge

class Command(BaseCommand):
    help = 'Popula badges do sistema RPG'

    def handle(self, *args, **kwargs):
        self.stdout.write('🏆 Criando Badges do Sistema RPG...\n')
        
        badges_data = [
            # === BADGES DE GRIND ===
            {
                'slug': 'hello-world',
                'name': 'Hello World',
                'description': 'Registrou sua primeira sessão de estudo!',
                'icon_class': 'fas fa-globe',
                'xp_bonus': 50,
                'coin_bonus': 10,
                'is_secret': False
            },
            {
                'slug': 'maratonista',
                'name': 'Maratonista',
                'description': 'Estudou 4 horas seguidas sem parar!',
                'icon_class': 'fas fa-running',
                'xp_bonus': 200,
                'coin_bonus': 50,
                'is_secret': False
            },
            {
                'slug': 'centuriao',
                'name': 'Centurião',
                'description': 'Alcançou 100 horas totais de estudo!',
                'icon_class': 'fas fa-medal',
                'xp_bonus': 500,
                'coin_bonus': 100,
                'is_secret': False
            },
            {
                'slug': '10k-hours',
                'name': '10.000 Horas',
                'description': 'Alcançou a maestria total! (Lendária)',
                'icon_class': 'fas fa-crown',
                'xp_bonus': 5000,
                'coin_bonus': 1000,
                'is_secret': True
            },
            
            # === BADGES DE COMPORTAMENTO ===
            {
                'slug': 'night-owl',
                'name': 'Coruja Noturna',
                'description': 'Estudou entre 02:00 e 05:00 da manhã',
                'icon_class': 'fas fa-moon',
                'xp_bonus': 100,
                'coin_bonus': 25,
                'is_secret': False
            },
            {
                'slug': 'early-bird',
                'name': 'Madrugador',
                'description': 'Estudou antes das 06:00 da manhã',
                'icon_class': 'fas fa-sun',
                'xp_bonus': 100,
                'coin_bonus': 25,
                'is_secret': False
            },
            {
                'slug': 'on-fire',
                'name': 'On Fire',
                'description': 'Manteve 3 dias de streak consecutivos!',
                'icon_class': 'fas fa-fire',
                'xp_bonus': 150,
                'coin_bonus': 30,
                'is_secret': False
            },
            {
                'slug': 'consistency-king',
                'name': 'Rei da Consistência',
                'description': 'Manteve 30 dias de streak consecutivos!',
                'icon_class': 'fas fa-chess-king',
                'xp_bonus': 500,
                'coin_bonus': 150,
                'is_secret': False
            },
            {
                'slug': 'weekend-warrior',
                'name': 'Guerreiro de Fim de Semana',
                'description': 'Estudou em 4 fins de semana seguidos',
                'icon_class': 'fas fa-calendar-week',
                'xp_bonus': 300,
                'coin_bonus': 75,
                'is_secret': False
            },
            
            # === BADGES DE HABILIDADE ===
            {
                'slug': 'snake-charmer',
                'name': 'Encantador de Serpentes',
                'description': 'Alcançou 50 horas de estudo em Python',
                'icon_class': 'fab fa-python',
                'xp_bonus': 300,
                'coin_bonus': 75,
                'is_secret': False
            },
            {
                'slug': 'fullstack-hero',
                'name': 'Herói Full Stack',
                'description': 'Tem 50h em Back-end e 50h em Front-end',
                'icon_class': 'fas fa-layer-group',
                'xp_bonus': 500,
                'coin_bonus': 150,
                'is_secret': False
            },
            {
                'slug': 'bug-hunter',
                'name': 'Caçador de Bugs',
                'description': 'Completou 10 Boss Battles',
                'icon_class': 'fas fa-bug',
                'xp_bonus': 400,
                'coin_bonus': 100,
                'is_secret': False
            },
            {
                'slug': 'code-master',
                'name': 'Mestre do Código',
                'description': 'Alcançou 500 horas de CODING',
                'icon_class': 'fas fa-code',
                'xp_bonus': 1000,
                'coin_bonus': 250,
                'is_secret': False
            },
            
            # === BADGES SOCIAIS ===
            {
                'slug': 'senpai',
                'name': 'Senpai',
                'description': 'Teve 5 Code Reviews aceitos',
                'icon_class': 'fas fa-user-graduate',
                'xp_bonus': 200,
                'coin_bonus': 50,
                'is_secret': False
            },
            {
                'slug': 'mentor',
                'name': 'Mentor',
                'description': 'Teve 20 Code Reviews aceitos',
                'icon_class': 'fas fa-chalkboard-teacher',
                'xp_bonus': 500,
                'coin_bonus': 150,
                'is_secret': False
            },
            {
                'slug': 'guild-leader',
                'name': 'Líder de Guilda',
                'description': 'Criou um grupo de estudos com 5+ pessoas',
                'icon_class': 'fas fa-users',
                'xp_bonus': 300,
                'coin_bonus': 100,
                'is_secret': False
            },
        ]
        
        created_count = 0
        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                slug=badge_data['slug'],
                defaults=badge_data
            )
            if created:
                self.stdout.write(f'  ✅ {badge.name}')
                created_count += 1
            else:
                self.stdout.write(f'  ⏭️  {badge.name} (já existe)')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 {created_count} badges criadas com sucesso!'))
