from .models import Conquista, Tecnologia, MetodoEstudo

# Badges focadas em horas estudadas por tecnologia
TECH_BADGES = [
    ("Mestre Python", "Python", "#3776ab", "fab fa-python", 20),
    ("Django Unchained", "Django", "#092e20", "fas fa-leaf", 20),
    ("Frontend Ninja", "HTML/CSS", "#e34c26", "fab fa-html5", 20),
    ("JS Jedi", "JavaScript", "#f7df1e", "fab fa-js-square", 20),
    ("Git Master", "Git", "#f05032", "fab fa-git-alt", 10),
    ("SQL Architect", "SQL", "#4479A1", "fas fa-database", 15),
    ("GitHub Contributor", "GitHub", "#181717", "fab fa-github", 10),
    ("Elephant Rider", "PostgreSQL", "#336791", "fas fa-database", 15),
    ("Laravel Artisan", "Laravel", "#ff2d20", "fab fa-laravel", 20),
    ("Android Dev", "Kotlin", "#7f52ff", "fas fa-robot", 20),
    ("Dolphin Keeper", "MySQL", "#4479A1", "fas fa-database", 15),
    ("React Reactor", "React", "#61dafb", "fab fa-react", 20),
    ("Rustacean", "Rust", "#dea584", "fab fa-rust", 20),
    ("Docker Captain", "Docker", "#2496ed", "fab fa-docker", 15),
    ("Ruby Gem", "Ruby", "#cc342d", "fas fa-gem", 20),
    ("Swift Developer", "Swift", "#fa7343", "fab fa-swift", 20),
    ("TypeScript Tycoon", "TypeScript", "#3178c6", "fab fa-js", 20),
    ("C# Sharp", "C#", "#178600", "fas fa-hashtag", 20),
    ("C++ Power", "C++", "#00599c", "fab fa-cuttlefish", 20),
    ("Low Level C", "C", "#3a4049", "fas fa-microchip", 20),
    ("ElePHPant", "PHP", "#777bb4", "fab fa-php", 20),
    ("Logic Master", "Lógica de Programação", "#7f8c8d", "fas fa-brain", 10),
]

# Badges de streak (dias seguidos)
STREAK_BADGES = [
    ("Primeiro Passo", "1 dia de ofensiva", 1, 50, "fas fa-shoe-prints", "#2ecc71"),
    ("Aquecimento", "3 dias seguidos", 3, 150, "fas fa-fire-alt", "#f1c40f"),
    ("Em Chamas", "7 dias seguidos", 7, 500, "fas fa-fire", "#e67e22"),
    ("Lendário", "30 dias seguidos", 30, 3000, "fas fa-meteor", "#8e44ad"),
    ("Inquebrável", "60 dias seguidos", 60, 8000, "fas fa-dragon", "#c0392b"),
    ("Sem Fôlego", "100 dias seguidos", 100, 15000, "fas fa-skull-crossbones", "#16a085"),
]

# Badges de tempo total
TIME_BADGES = [
    ("Hello World", "1 hora total", 1, 50, "fas fa-egg", "#bdc3c7"),
    ("Júnior", "10 horas totais", 10, 200, "fas fa-scroll", "#3498db"),
    ("Pleno", "50 horas totais", 50, 1000, "fas fa-code", "#9b59b6"),
    ("Sênior", "100 horas totais", 100, 2500, "fas fa-laptop-code", "#f1c40f"),
    ("Ultra Marathon", "250 horas totais", 250, 6000, "fas fa-rocket", "#e67e22"),
    ("Legendary Grinder", "500 horas totais", 500, 12000, "fas fa-meteor", "#8e44ad"),
]

METHOD_BADGES = [
    ("Sprint Master", "20h em Projeto Prático", "Projeto Prático", 20, 800, "fas fa-screwdriver-wrench", "#1abc9c"),
    ("Teórico Forte", "15h em Leitura/Teoria", "Leitura/Teoria", 15, 600, "fas fa-book-open", "#9b59b6"),
    ("Maratona de Vídeo", "25h em Videoaula", "Videoaula", 25, 900, "fas fa-video", "#3498db"),
    ("Prática Intensa", "30h em Exercícios", "Exercícios", 30, 1200, "fas fa-dumbbell", "#e67e22"),
]

HIDDEN_BADGES = [
    # tempo
    ("No Days Off", "750 horas totais (oculta)", "tempo", None, None, 750, 15000, "fas fa-bolt", "#2c3e50", True),
    # streak
    ("Imortal", "150 dias seguidos (oculta)", "streak", None, None, 150, 20000, "fas fa-infinity", "#8e44ad", True),
    # tecnologia
    ("Python Sage", "100h em Python (oculta)", "tecnologia", "Python", None, 100, 4000, "fab fa-python", "#1e8bd6", True),
    # método
    ("Videoaluno Elite", "60h em Videoaula (oculta)", "metodo", None, "Videoaula", 60, 5000, "fas fa-film", "#2980b9", True),
]


def seed_badges(reset: bool = True) -> int:
    """Cria/atualiza todas as conquistas padrões. Deleta anteriores quando reset=True."""
    if reset:
        Conquista.objects.all().delete()

    created = 0
    for nome, tech, cor, icone, horas in TECH_BADGES:
        tecnologia, _ = Tecnologia.objects.get_or_create(nome=tech)
        Conquista.objects.update_or_create(
            nome=nome,
            categoria="tecnologia",
            tecnologia_alvo=tecnologia,
            defaults={
                "descricao": f"Complete {horas}h em {tech}.",
                "tipo_visual": "hexagono",
                "quantidade_necessaria": horas,
                "xp_reward": horas * 15,
                "icone_fa": icone,
                "cor_hex": cor,
                "oculta": False,
            },
        )
        created += 1

    for nome, descricao, quantidade, xp, icone, cor in STREAK_BADGES:
        Conquista.objects.update_or_create(
            nome=nome,
            categoria="streak",
            defaults={
                "descricao": descricao,
                "tipo_visual": "hexagono",
                "quantidade_necessaria": quantidade,
                "xp_reward": xp,
                "icone_fa": icone,
                "cor_hex": cor,
                "oculta": False,
            },
        )
        created += 1

    for nome, descricao, quantidade, xp, icone, cor in TIME_BADGES:
        Conquista.objects.update_or_create(
            nome=nome,
            categoria="tempo",
            defaults={
                "descricao": descricao,
                "tipo_visual": "padrao",
                "quantidade_necessaria": quantidade,
                "xp_reward": xp,
                "icone_fa": icone,
                "cor_hex": cor,
                "oculta": False,
            },
        )
        created += 1

    for nome, descricao, metodo, horas, xp, icone, cor in METHOD_BADGES:
        metodo_obj, _ = MetodoEstudo.objects.get_or_create(nome=metodo)
        Conquista.objects.update_or_create(
            nome=nome,
            categoria="metodo",
            metodo_alvo=metodo_obj,
            defaults={
                "descricao": descricao,
                "tipo_visual": "hexagono",
                "quantidade_necessaria": horas,
                "xp_reward": xp,
                "icone_fa": icone,
                "cor_hex": cor,
                "oculta": False,
            },
        )
        created += 1

    for nome, descricao, categoria, tech, metodo, quantidade, xp, icone, cor, oculta in HIDDEN_BADGES:
        tecnologia = None
        metodo_obj = None
        if tech:
            tecnologia, _ = Tecnologia.objects.get_or_create(nome=tech)
        if metodo:
            metodo_obj, _ = MetodoEstudo.objects.get_or_create(nome=metodo)
        Conquista.objects.update_or_create(
            nome=nome,
            categoria=categoria,
            tecnologia_alvo=tecnologia,
            metodo_alvo=metodo_obj,
            defaults={
                "descricao": descricao,
                "tipo_visual": "hexagono" if categoria != "tempo" else "padrao",
                "quantidade_necessaria": quantidade,
                "xp_reward": xp,
                "icone_fa": icone,
                "cor_hex": cor,
                "oculta": oculta,
            },
        )
        created += 1

    return created
