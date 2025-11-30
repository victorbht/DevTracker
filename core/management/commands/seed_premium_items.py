from django.core.management.base import BaseCommand
from core.models import StoreItem

class Command(BaseCommand):
    help = 'Popula itens premium da loja'

    def handle(self, *args, **options):
        items = [
            # Molduras Básicas
            {'name': 'Moldura Bronze', 'category': 'FRAME', 'price': 100, 'css_class': 'frame-bronze'},
            {'name': 'Moldura Prata', 'category': 'FRAME', 'price': 250, 'css_class': 'frame-silver'},
            {'name': 'Moldura Ouro', 'category': 'FRAME', 'price': 500, 'css_class': 'frame-gold'},
            
            # Molduras Premium
            {'name': 'Moldura RGB Gamer', 'category': 'FRAME', 'price': 1000, 'css_class': 'frame-rgb-rainbow'},
            {'name': 'Moldura Error Glitch', 'category': 'FRAME', 'price': 1500, 'css_class': 'frame-error-glitch'},
            {'name': 'Moldura Matrix Rain', 'category': 'FRAME', 'price': 2000, 'css_class': 'frame-matrix-rain'},
            
            # Molduras de Boss (Épicas)
            {'name': 'Escamas da Hidra', 'category': 'FRAME', 'price': 3000, 'css_class': 'frame-hydra-scales'},
            {'name': 'Loop do Ouroboros', 'category': 'FRAME', 'price': 3500, 'css_class': 'frame-ouroboros-loop'},
            {'name': 'Raios da Tempestade', 'category': 'FRAME', 'price': 4000, 'css_class': 'frame-storm-lightning'},
            {'name': 'Vazamento do Espectro', 'category': 'FRAME', 'price': 4500, 'css_class': 'frame-wraith-leak'},
            {'name': 'Ouro do Guardião', 'category': 'FRAME', 'price': 5000, 'css_class': 'frame-gatekeeper-gold'},
            
            # Banners
            {'name': 'Banner Neon', 'category': 'BANNER', 'price': 300, 'css_class': 'banner-neon'},
            {'name': 'Banner Glitch', 'category': 'BANNER', 'price': 800, 'css_class': 'glitch-effect'},
            
            # Pets
            {'name': 'Pet Pato', 'category': 'THEME', 'price': 500, 'css_class': 'pet-duck'},
            {'name': 'Pet Drone', 'category': 'THEME', 'price': 1200, 'css_class': 'pet-drone'},
        ]
        
        created = 0
        for item_data in items:
            obj, created_flag = StoreItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            if created_flag:
                created += 1
        
        self.stdout.write(self.style.SUCCESS(f'{created} itens premium criados!'))
