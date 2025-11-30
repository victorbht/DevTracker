from django.core.management.base import BaseCommand
from core.models import SkillNode, ItemLoja, BossBattle

class Command(BaseCommand):
    help = 'Popula dados iniciais do Pacote Gamer'

    def handle(self, *args, **kwargs):
        self.stdout.write('🎮 Iniciando seed do Pacote Gamer...\n')
        
        # === SKILL TREE ===
        self.stdout.write('📚 Criando Árvore de Habilidades...')
        skills_data = [
            {'nome': 'Python', 'icone_fa': 'fab fa-python', 'parent': None},
            {'nome': 'Django', 'icone_fa': 'fas fa-server', 'parent': 'Python'},
            {'nome': 'Flask', 'icone_fa': 'fas fa-flask', 'parent': 'Python'},
            {'nome': 'JavaScript', 'icone_fa': 'fab fa-js', 'parent': None},
            {'nome': 'React', 'icone_fa': 'fab fa-react', 'parent': 'JavaScript'},
            {'nome': 'Node.js', 'icone_fa': 'fab fa-node', 'parent': 'JavaScript'},
            {'nome': 'SQL', 'icone_fa': 'fas fa-database', 'parent': None},
            {'nome': 'Git', 'icone_fa': 'fab fa-git-alt', 'parent': None},
            {'nome': 'Docker', 'icone_fa': 'fab fa-docker', 'parent': None},
            {'nome': 'AWS', 'icone_fa': 'fab fa-aws', 'parent': None},
        ]
        
        skill_objs = {}
        for skill in skills_data:
            parent_obj = skill_objs.get(skill['parent']) if skill['parent'] else None
            obj, created = SkillNode.objects.get_or_create(
                nome=skill['nome'],
                defaults={'icone_fa': skill['icone_fa'], 'parent': parent_obj}
            )
            skill_objs[skill['nome']] = obj
            if created:
                self.stdout.write(f'  ✅ {skill["nome"]}')
        
        # === LOJA ===
        self.stdout.write('\n🛒 Criando Itens da Loja...')
        itens_data = [
            {'nome': 'Moldura Neon Verde', 'categoria': 'FRAME', 'preco': 500, 'raridade': 'RARO', 'css_class': 'frame-neon-green'},
            {'nome': 'Moldura Cyber Azul', 'categoria': 'FRAME', 'preco': 800, 'raridade': 'EPICO', 'css_class': 'frame-cyber-blue'},
            {'nome': 'Moldura Lendária Dourada', 'categoria': 'FRAME', 'preco': 2000, 'raridade': 'LENDARIO', 'css_class': 'frame-legendary-gold'},
            {'nome': 'Banner Matrix', 'categoria': 'BANNER', 'preco': 600, 'raridade': 'RARO', 'css_class': 'banner-matrix'},
            {'nome': 'Banner Cyberpunk', 'categoria': 'BANNER', 'preco': 1000, 'raridade': 'EPICO', 'css_class': 'banner-cyberpunk'},
            {'nome': 'Tema Dark Neon', 'categoria': 'THEME', 'preco': 1500, 'raridade': 'EPICO', 'css_class': 'theme-dark-neon'},
        ]
        
        for item in itens_data:
            obj, created = ItemLoja.objects.get_or_create(
                nome=item['nome'],
                defaults=item
            )
            if created:
                self.stdout.write(f'  ✅ {item["nome"]} ({item["raridade"]})')
        
        # === BOSS BATTLES ===
        self.stdout.write('\n⚔️  Criando Boss Battles...')
        bosses_data = [
            {
                'titulo': 'Clone do Twitter',
                'descricao': 'Crie uma rede social com posts, likes e follows',
                'xp_recompensa': 1000,
                'coins_recompensa': 500,
                'dificuldade': 'MEDIO',
                'boss_icon': 'fab fa-twitter',
                'skill': 'Django'
            },
            {
                'titulo': 'API REST Completa',
                'descricao': 'Desenvolva uma API com autenticação JWT e documentação',
                'xp_recompensa': 800,
                'coins_recompensa': 400,
                'dificuldade': 'MEDIO',
                'boss_icon': 'fas fa-code',
                'skill': 'Python'
            },
            {
                'titulo': 'Dashboard Analytics',
                'descricao': 'Crie um dashboard com gráficos em tempo real',
                'xp_recompensa': 1500,
                'coins_recompensa': 750,
                'dificuldade': 'DIFICIL',
                'boss_icon': 'fas fa-chart-line',
                'skill': 'React'
            },
            {
                'titulo': 'E-commerce Full Stack',
                'descricao': 'Loja completa com carrinho, pagamento e admin',
                'xp_recompensa': 3000,
                'coins_recompensa': 1500,
                'dificuldade': 'LENDARIO',
                'boss_icon': 'fas fa-shopping-cart',
                'skill': 'JavaScript'
            },
        ]
        
        for boss in bosses_data:
            skill_obj = skill_objs.get(boss.pop('skill'))
            obj, created = BossBattle.objects.get_or_create(
                titulo=boss['titulo'],
                defaults={**boss, 'skill_relacionada': skill_obj}
            )
            if created:
                self.stdout.write(f'  ✅ {boss["titulo"]} ({boss["dificuldade"]})')
        
        self.stdout.write(self.style.SUCCESS('\n\n🎉 Pacote Gamer populado com sucesso!'))
