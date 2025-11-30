from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Q, Prefetch
from django.utils import timezone
from datetime import timedelta, date
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.cache import cache
import json
import math
from .models import (
    SessaoEstudo, Tecnologia, MetodoEstudo, Conquista, PerfilUsuario,
    UserProfile, StudySession, SkillNode, JobQuest, BossBattle, ProjectSubmission,
    Badge, UserBadge, StoreItem, UserInventory, CodeReview, Notification
)
from .forms import SessaoEstudoForm
from .badges import seed_badges


def duration_human(value):
    """Formata duration/segundos para '2h 30min 2s', ocultando partes zeradas."""
    try:
        seconds = int(value.total_seconds()) if hasattr(value, "total_seconds") else int(value)
    except Exception:
        return "0s"
    hours, rem = divmod(max(seconds, 0), 3600)
    minutes, secs = divmod(rem, 60)
    parts = []
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}min")
    if secs or not parts: parts.append(f"{secs}s")
    return " ".join(parts)

# === ENGINE DE GAMIFICAÇÃO ===
def verificar_conquistas(user):
    # Garante que o perfil existe (fallback de segurança)
    perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
    
    conquistas_desbloqueadas = []
    conquistas_disponiveis = Conquista.objects.exclude(id__in=perfil.conquistas.values_list('id', flat=True))
    
    # Cálculos Totais
    total_horas = 0
    total_obj = SessaoEstudo.objects.aggregate(total=Sum('tempo_liquido'))['total']
    if total_obj: total_horas = total_obj.total_seconds() / 3600

    # Lógica de Streak (Ofensiva)
    datas = SessaoEstudo.objects.dates('data_registro', 'day').order_by('-data_registro')
    streak = 0
    hoje = timezone.now().date()
    if datas and (datas[0] == hoje or datas[0] == hoje - timedelta(days=1)):
        check = datas[0]
        for d in datas:
            if d == check: streak += 1; check -= timedelta(days=1)
            else: break

    # Verificação de cada conquista disponível
    for c in conquistas_disponiveis:
        desbloqueou = False
        if c.categoria == 'tempo' and total_horas >= c.quantidade_necessaria: desbloqueou = True
        elif c.categoria == 'streak' and streak >= c.quantidade_necessaria: desbloqueou = True
        elif c.categoria == 'tecnologia' and c.tecnologia_alvo:
            t_tech = SessaoEstudo.objects.filter(tecnologia=c.tecnologia_alvo).aggregate(t=Sum('tempo_liquido'))['t']
            h_tech = t_tech.total_seconds() / 3600 if t_tech else 0
            if h_tech >= c.quantidade_necessaria: desbloqueou = True
        elif c.categoria == 'metodo' and c.metodo_alvo:
            t_met = SessaoEstudo.objects.filter(metodo=c.metodo_alvo).aggregate(t=Sum('tempo_liquido'))['t']
            h_met = t_met.total_seconds() / 3600 if t_met else 0
            if h_met >= c.quantidade_necessaria: desbloqueou = True
        
        if desbloqueou:
            perfil.conquistas.add(c)
            perfil.xp_total += c.xp_reward
            conquistas_desbloqueadas.append(c)

    # Level Up
    novo_nivel = int(perfil.xp_total / 1000) + 1
    if novo_nivel > perfil.nivel: perfil.nivel = novo_nivel
    perfil.save()
    
    return conquistas_desbloqueadas, streak

# === DASHBOARD PRINCIPAL ===
@login_required
def index(request, periodo='tudo'):
    novas_conquistas = []
    streak_atual = 0
    session_saved = False
    mostrar_todas = request.GET.get('full') == '1'
    page_number = request.GET.get('page', 1)
    cal_ano = request.GET.get('ano')
    cal_mes = request.GET.get('mes')

    # Garante perfil na index também
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SessaoEstudoForm(request.POST)
        if form.is_valid():
            form.save()
            session_saved = True
            novas_conquistas, streak_atual = verificar_conquistas(request.user)
    else:
        form = SessaoEstudoForm()
        # Apenas calcula o streak para exibição
        _, streak_atual = verificar_conquistas(request.user)

    # Filtros de Data com otimização
    data_limite = None
    hoje = timezone.now().date()
    if periodo == 'semana': data_limite = hoje - timedelta(days=7)
    elif periodo == 'mes': data_limite = hoje - timedelta(days=30)
    
    # Query otimizada com select_related e only para reduzir campos
    sessoes = SessaoEstudo.objects.select_related('tecnologia','metodo').only(
        'id', 'tecnologia__nome', 'metodo__nome', 'topico', 'tempo_liquido', 
        'data_registro', 'qtd_exercicios', 'qtd_acertos'
    )
    if data_limite: sessoes = sessoes.filter(data_registro__date__gte=data_limite)

    # Métricas Gerais
    total_sec = sessoes.aggregate(t=Sum('tempo_liquido'))['t']
    total_str = duration_human(total_sec)
    
    # Preparação para Gráficos (JSON)
    def fmt(qs):
        data = []
        for i in qs:
            data.append({'nome': i[list(i.keys())[0]], 'sec': i['t'].total_seconds()})
        return json.dumps(data)

    tech_qs = sessoes.values('tecnologia__nome').annotate(t=Sum('tempo_liquido')).order_by('-t')
    met_qs = sessoes.values('metodo__nome').annotate(t=Sum('tempo_liquido')).order_by('-t')

    # Dados do Perfil
    xp_atual_nivel = perfil.xp_total % 1000
    pct_nivel = int((xp_atual_nivel / 1000) * 100)

    titulo = "Estagiário"
    if perfil.nivel > 5: titulo = "Júnior"
    if perfil.nivel > 10: titulo = "Pleno"
    if perfil.nivel > 20: titulo = "Sênior"

    # Calendário mensal com navegação e streak por dia
    hoje_local = timezone.localdate()
    try:
        ano_ref = int(cal_ano) if cal_ano else hoje_local.year
        mes_ref = int(cal_mes) if cal_mes else hoje_local.month
        if mes_ref < 1 or mes_ref > 12: raise ValueError()
    except Exception:
        ano_ref, mes_ref = hoje_local.year, hoje_local.month

    import calendar
    cal = calendar.Calendar(firstweekday=0)  # 0 = Monday
    sessoes_mes = SessaoEstudo.objects.select_related('tecnologia','metodo').filter(data_registro__year=ano_ref, data_registro__month=mes_ref)
    dias = sessoes_mes.values('data_registro__date').annotate(t=Sum('tempo_liquido'))
    mapa_dias = {d['data_registro__date']: d['t'].total_seconds() for d in dias}
    total_mes_sec = sum(mapa_dias.values()) if mapa_dias else 0
    total_mes = duration_human(total_mes_sec)

    # streak por dia (global)
    dias_sessoes = list(SessaoEstudo.objects.dates('data_registro', 'day').order_by('data_registro'))
    streak_map = {}
    prev = None
    streak_c = 0
    for d in dias_sessoes:
        if prev and d == prev + timedelta(days=1):
            streak_c += 1
        else:
            streak_c = 1
        streak_map[d] = streak_c
        prev = d

    calendario = []
    for week in cal.monthdatescalendar(ano_ref, mes_ref):
        linha = []
        for d in week:
            if d.month != mes_ref:
                linha.append({'dia': None, 'segundos': 0, 'human': '', 'streak': None, 'data': d})
            else:
                sec = mapa_dias.get(d, 0)
                linha.append({
                    'dia': d.day,
                    'segundos': int(sec),
                    'human': duration_human(sec),
                    'streak': streak_map.get(d),
                    'data': d,
                })
        calendario.append(linha)
    sessions_by_day = {}
    for s in sessoes_mes:
        key = s.data_registro.date().isoformat()
        sessions_by_day.setdefault(key, []).append({
            'hora': s.data_registro.strftime('%H:%M'),
            'tech': s.tecnologia.nome,
            'metodo': s.metodo.nome if s.metodo else '',
            'tempo': duration_human(s.tempo_liquido),
            'topico': s.topico,
        })

    mes_display = f"{mes_ref:02d}"
    prev_year, prev_month = (ano_ref, mes_ref - 1) if mes_ref > 1 else (ano_ref - 1, 12)
    next_year, next_month = (ano_ref, mes_ref + 1) if mes_ref < 12 else (ano_ref + 1, 1)

    meses_pt = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    paginator = Paginator(sessoes.order_by('-data_registro'), 50)
    page_obj = paginator.get_page(page_number)

    # Progresso por método (próxima badge)
    metodo_hours = {m['metodo__nome']: m['total'].total_seconds() / 3600 for m in SessaoEstudo.objects.values('metodo__nome').annotate(total=Sum('tempo_liquido')) if m['metodo__nome']}
    metodo_badges = Conquista.objects.filter(categoria='metodo').select_related('metodo_alvo')
    metodo_progresso = []
    for nome, horas in metodo_hours.items():
        prox = metodo_badges.filter(metodo_alvo__nome=nome, quantidade_necessaria__gt=horas).order_by('quantidade_necessaria').first()
        pct = 100
        restante = 0
        alvo = None
        if prox:
            alvo = prox.quantidade_necessaria
            restante = max(0, prox.quantidade_necessaria - horas)
            pct = int(min(100, (horas / prox.quantidade_necessaria) * 100))
        metodo_progresso.append({'nome': nome, 'horas': horas, 'alvo': alvo, 'restante': restante, 'pct': pct})

    # Estatísticas do Dashboard
    total_sessoes = sessoes.count()
    dias_estudados = sessoes.dates('data_registro', 'day').count()
    media_dia = (total_sec.total_seconds() / 3600 / dias_estudados) if dias_estudados and total_sec else 0
    
    # Top 3 tecnologias
    top_techs = list(tech_qs[:3])
    
    # Progresso de metas
    semana_inicio = hoje - timedelta(days=hoje.weekday())
    horas_semana = SessaoEstudo.objects.filter(data_registro__date__gte=semana_inicio).aggregate(t=Sum('tempo_liquido'))['t']
    horas_semana_val = horas_semana.total_seconds() / 3600 if horas_semana else 0
    
    mes_inicio = hoje.replace(day=1)
    horas_mes = SessaoEstudo.objects.filter(data_registro__date__gte=mes_inicio).aggregate(t=Sum('tempo_liquido'))['t']
    horas_mes_val = horas_mes.total_seconds() / 3600 if horas_mes else 0
    
    meta_semanal_pct = int(min(100, (horas_semana_val / perfil.meta_semanal) * 100)) if perfil.meta_semanal else 0
    meta_mensal_pct = int(min(100, (horas_mes_val / perfil.meta_mensal) * 100)) if perfil.meta_mensal else 0
    
    # Comparação com semana anterior
    semana_passada_inicio = semana_inicio - timedelta(days=7)
    semana_passada_fim = semana_inicio - timedelta(days=1)
    horas_semana_passada = SessaoEstudo.objects.filter(data_registro__date__gte=semana_passada_inicio, data_registro__date__lte=semana_passada_fim).aggregate(t=Sum('tempo_liquido'))['t']
    horas_semana_passada_val = horas_semana_passada.total_seconds() / 3600 if horas_semana_passada else 0
    diff_semana = horas_semana_val - horas_semana_passada_val
    
    # Última sessão para repetir
    ultima_sessao = sessoes.first()
    
    # Evolução temporal (últimas 8 semanas)
    evolucao_semanal = []
    for i in range(7, -1, -1):
        semana_inicio_calc = hoje - timedelta(days=hoje.weekday() + (i * 7))
        semana_fim_calc = semana_inicio_calc + timedelta(days=6)
        horas = SessaoEstudo.objects.filter(data_registro__date__gte=semana_inicio_calc, data_registro__date__lte=semana_fim_calc).aggregate(t=Sum('tempo_liquido'))['t']
        horas_val = horas.total_seconds() / 3600 if horas else 0
        evolucao_semanal.append({'semana': f"{semana_inicio_calc.day}/{semana_inicio_calc.month}", 'horas': round(horas_val, 1)})
    evolucao_json = json.dumps(evolucao_semanal)

    contexto = {
        'form': form, 'periodo_atual': periodo, 'total_liquido': total_str,
        'tech_json': fmt(tech_qs), 'horas_por_tech_json': fmt(tech_qs), 
        'metodo_json': fmt(met_qs), 'horas_por_metodo_json': fmt(met_qs), 
        'todas_sessoes': sessoes.order_by('-data_registro') if mostrar_todas else sessoes.order_by('-data_registro')[:5],
        'page_obj': page_obj,
        'techs': Tecnologia.objects.all().order_by('nome'),
        'metodos': MetodoEstudo.objects.all().order_by('nome'),
        'perfil': perfil, 'streak': streak_atual, 'pct_nivel': pct_nivel,
        'titulo_dev': titulo, 'novas_conquistas': novas_conquistas,
        'conquistas_usuario': perfil.conquistas.all(),
        'session_saved': session_saved,
        'calendario': calendario,
        'mes_atual': f"{meses_pt[mes_ref-1]} / {ano_ref}",
        'mes_atual_num': mes_ref,
        'ano_atual_num': ano_ref,
        'prev_ano': prev_year, 'prev_mes': prev_month,
        'next_ano': next_year, 'next_mes': next_month,
        'mostrar_todas': mostrar_todas,
        'total_mes': total_mes,
        'sessions_by_day': json.dumps(sessions_by_day),
        'metodo_progresso': metodo_progresso,
        'today_iso': hoje_local.isoformat(),
        'total_sessoes': total_sessoes,
        'dias_estudados': dias_estudados,
        'media_dia': media_dia,
        'top_techs': top_techs,
        'horas_semana': horas_semana_val,
        'horas_mes': horas_mes_val,
        'meta_semanal_pct': meta_semanal_pct,
        'meta_mensal_pct': meta_mensal_pct,
        'diff_semana': diff_semana,
        'ultima_sessao': ultima_sessao,
        'evolucao_json': evolucao_json,
    }
    return render(request, 'core/index.html', contexto)

# === GALERIA DE CONQUISTAS ===
@login_required
def galeria_conquistas(request):
    from django.core.cache import cache
    
    perfil = PerfilUsuario.objects.select_related('user').prefetch_related(
        Prefetch('conquistas', queryset=Conquista.objects.only('id', 'nome', 'categoria', 'icone_fa', 'cor_hex'))
    ).get_or_create(user=request.user)[0]
    
    # Cache de conquistas disponíveis por 5 minutos
    cache_key = f'conquistas_visiveis_{request.user.id}'
    todas = cache.get(cache_key)
    if todas is None:
        todas = Conquista.objects.select_related('tecnologia_alvo', 'metodo_alvo').filter(
            Q(oculta=False) | Q(pk__in=perfil.conquistas.values('pk'))
        ).order_by('categoria', 'quantidade_necessaria')
        cache.set(cache_key, todas, 300)  # 5 minutos
    
    # 2. IDs das conquistas que o usuário já tem
    meus_ids = set(perfil.conquistas.values_list('id', flat=True))
    
    # 3. Dados estatísticos globais
    total_obj = SessaoEstudo.objects.aggregate(t=Sum('tempo_liquido'))['t'] 
    total_str = str(total_obj).split('.')[0] if total_obj else '0:00:00'
    total_horas = total_obj.total_seconds() / 3600 if total_obj else 0

    tech_hours = {i['tecnologia__nome']: i['t'].total_seconds() / 3600 for i in SessaoEstudo.objects.values('tecnologia__nome').annotate(t=Sum('tempo_liquido')) if i['tecnologia__nome']}
    metodo_hours = {i['metodo__nome']: i['t'].total_seconds() / 3600 for i in SessaoEstudo.objects.values('metodo__nome').annotate(t=Sum('tempo_liquido')) if i['metodo__nome']}
    
    datas = list(SessaoEstudo.objects.dates('data_registro', 'day').order_by('data_registro'))
    streak = 0
    max_streak = 0
    if datas:
        prev = None
        streak_run = 0
        for d in datas:
            if prev and d == prev + timedelta(days=1):
                streak_run += 1
            else:
                streak_run = 1
            max_streak = max(max_streak, streak_run)
            prev = d
        # streak atual
        hoje = timezone.now().date()
        datas_desc = list(reversed(datas))
        streak = 0
        check = datas_desc[0] if datas_desc else None
        if check and (check == hoje or check == hoje - timedelta(days=1)):
            for d in datas_desc:
                if d == check: streak += 1; check -= timedelta(days=1)
                else: break

    def progresso_categoria(valor_atual, categoria):
        conquistas = Conquista.objects.filter(categoria=categoria).order_by('quantidade_necessaria')
        if not conquistas:
            return None
        next_goal = None
        prev_goal = 0
        for c in conquistas:
            if valor_atual < c.quantidade_necessaria:
                next_goal = c.quantidade_necessaria
                break
            prev_goal = c.quantidade_necessaria
        if not next_goal:
            return {'atual': valor_atual, 'meta': prev_goal, 'pct': 100}
        span = max(next_goal - prev_goal, 1)
        pct = int(min(100, ((valor_atual - prev_goal) / span) * 100))
        return {'atual': valor_atual, 'meta': next_goal, 'pct': pct}
            
    # Título e Progresso
    xp_atual_nivel = perfil.xp_total % 1000
    pct_nivel = int((xp_atual_nivel / 1000) * 100)
    
    titulo = "Estagiário"
    if perfil.nivel > 5: titulo = "Júnior"
    if perfil.nivel > 10: titulo = "Pleno"
    if perfil.nivel > 20: titulo = "Sênior"
    if perfil.nivel > 50: titulo = "Tech Lead"

    def faltam_para(conquista: Conquista):
        if conquista.categoria == 'tempo':
            return max(0, conquista.quantidade_necessaria - total_horas)
        if conquista.categoria == 'streak':
            return max(0, conquista.quantidade_necessaria - streak)
        if conquista.categoria == 'tecnologia' and conquista.tecnologia_alvo:
            atual = tech_hours.get(conquista.tecnologia_alvo.nome, 0)
            return max(0, conquista.quantidade_necessaria - atual)
        if conquista.categoria == 'metodo' and conquista.metodo_alvo:
            atual = metodo_hours.get(conquista.metodo_alvo.nome, 0)
            return max(0, conquista.quantidade_necessaria - atual)
        return None

    conquistas_com_status = []
    for c in todas:
        conquista_dict = {
            'obj': c,
            'unlocked': c.pk in meus_ids,
            'faltam': faltam_para(c)
        }
        conquistas_com_status.append(conquista_dict)

    contexto = {
        'todas_conquistas': conquistas_com_status,
        'minhas_conquistas_ids': meus_ids,
        'perfil': perfil,
        'total_liquido': total_str,
        'total_horas': total_horas,
        'streak': streak,
        'titulo_dev': titulo,
        'pct_nivel': pct_nivel,
        'progresso_tempo': progresso_categoria(total_horas, 'tempo'),
        'progresso_streak': progresso_categoria(streak, 'streak'),
        'max_streak': max_streak,
    }
    return render(request, 'core/conquistas.html', contexto)

# === CRUD SESSÃO ===
@login_required
def editar_sessao(request, id):
    obj = get_object_or_404(SessaoEstudo, id=id)
    if request.method == 'POST':
        form = SessaoEstudoForm(request.POST, instance=obj)
        if form.is_valid(): form.save()
    return redirect('core:index')

@login_required
def editar_tempo(request, id):
    obj = get_object_or_404(SessaoEstudo, id=id)
    if request.method == 'POST':
        tempo_str = request.POST.get('tempo_liquido')
        if tempo_str:
            from datetime import datetime
            try:
                h, m, s = map(int, tempo_str.split(':'))
                obj.tempo_liquido = timedelta(hours=h, minutes=m, seconds=s)
                obj.save()
                return HttpResponse('OK')
            except:
                pass
    return HttpResponse('Error', status=400)

@login_required
def excluir_sessao(request, id):
    obj = get_object_or_404(SessaoEstudo, id=id)
    if request.method == 'POST': obj.delete()
    return redirect('core:index')

# === CRUD CONFIGURAÇÕES (Tech/Metodo) ===
@login_required
def salvar_tech(request):
    if request.method == 'POST' and request.POST.get('nome'):
        Tecnologia.objects.get_or_create(nome=request.POST.get('nome'))
    return redirect('core:index')

@login_required
def excluir_tech(request, id):
    get_object_or_404(Tecnologia, id=id).delete()
    return redirect('core:index')

@login_required
def salvar_metodo(request):
    if request.method == 'POST' and request.POST.get('nome'):
        MetodoEstudo.objects.get_or_create(nome=request.POST.get('nome'))
    return redirect('core:index')

@login_required
def excluir_metodo(request, id):
    get_object_or_404(MetodoEstudo, id=id).delete()
    return redirect('core:index')

@login_required
def salvar_metas(request):
    if request.method == 'POST':
        perfil = request.user.perfil
        perfil.meta_semanal = int(request.POST.get('meta_semanal', 0))
        perfil.meta_mensal = int(request.POST.get('meta_mensal', 0))
        perfil.save()
    return redirect('core:index')

@login_required
def estatisticas(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    hoje = timezone.now().date()
    
    # Evolução semanal
    evolucao_semanal = []
    for i in range(7, -1, -1):
        semana_inicio = hoje - timedelta(days=hoje.weekday() + (i * 7))
        semana_fim = semana_inicio + timedelta(days=6)
        horas = SessaoEstudo.objects.filter(data_registro__date__gte=semana_inicio, data_registro__date__lte=semana_fim).aggregate(t=Sum('tempo_liquido'))['t']
        horas_val = horas.total_seconds() / 3600 if horas else 0
        evolucao_semanal.append({'semana': f"{semana_inicio.day}/{semana_inicio.month}", 'horas': round(horas_val, 1)})
    
    # Distribuições
    tech_qs = SessaoEstudo.objects.values('tecnologia__nome').annotate(t=Sum('tempo_liquido')).order_by('-t')
    met_qs = SessaoEstudo.objects.values('metodo__nome').annotate(t=Sum('tempo_liquido')).order_by('-t')
    
    def fmt(qs):
        return json.dumps([{'nome': i[list(i.keys())[0]], 'sec': i['t'].total_seconds()} for i in qs])
    
    # Metas
    semana_inicio = hoje - timedelta(days=hoje.weekday())
    horas_semana = SessaoEstudo.objects.filter(data_registro__date__gte=semana_inicio).aggregate(t=Sum('tempo_liquido'))['t']
    horas_semana_val = horas_semana.total_seconds() / 3600 if horas_semana else 0
    
    mes_inicio = hoje.replace(day=1)
    horas_mes = SessaoEstudo.objects.filter(data_registro__date__gte=mes_inicio).aggregate(t=Sum('tempo_liquido'))['t']
    horas_mes_val = horas_mes.total_seconds() / 3600 if horas_mes else 0
    
    meta_semanal_pct = int(min(100, (horas_semana_val / perfil.meta_semanal) * 100)) if perfil.meta_semanal else 0
    meta_mensal_pct = int(min(100, (horas_mes_val / perfil.meta_mensal) * 100)) if perfil.meta_mensal else 0
    
    contexto = {
        'perfil': perfil,
        'evolucao_json': json.dumps(evolucao_semanal),
        'tech_json': fmt(tech_qs),
        'metodo_json': fmt(met_qs),
        'horas_semana': horas_semana_val,
        'horas_mes': horas_mes_val,
        'meta_semanal_pct': meta_semanal_pct,
        'meta_mensal_pct': meta_mensal_pct,
    }
    return render(request, 'core/estatisticas.html', contexto)

@staff_member_required
def popular_badges(request):
    created = seed_badges(reset=True)
    return HttpResponse(f"<h1>Sucesso!</h1><p>{created} Badges criadas.</p><a href='/conquistas/'>Voltar para Galeria</a>")

# === PACOTE GAMER VIEWS ===
@login_required
def dashboard_gamer(request):
    try:
        from .models import UserBadge
        from django.db.models import Prefetch
        
        # Query otimizada com prefetch_related
        profile = UserProfile.objects.select_related('user', 'equipped_frame', 'equipped_banner').prefetch_related(
            Prefetch('badges', queryset=Badge.objects.only('id', 'name', 'icon_class')),
            Prefetch('skills_desbloqueadas', queryset=SkillNode.objects.only('id', 'name', 'icon_class'))
        ).get_or_create(user=request.user)[0]
        
        recent_sessions = StudySession.objects.select_related('skill').filter(
            user=request.user
        ).only('id', 'skill__name', 'start_time', 'duration_minutes', 'xp_earned').order_by('-start_time')[:5]
        
        recent_badges = UserBadge.objects.select_related('badge').filter(
            user_profile=profile
        ).only('badge__name', 'badge__icon_class', 'earned_at').order_by('-earned_at')[:3]
        total_badges = profile.badges.count()
        
        today = timezone.now().date()
        daily_quest_completed = profile.last_checkin == today
        
        next_level_xp = profile.xp_to_next_level()
        progress_percent = int((profile.current_xp / next_level_xp) * 100) if next_level_xp else 0
        
        top_skills = profile.skills_desbloqueadas.all()[:3]
        next_boss = BossBattle.objects.filter(is_active=True).first()
        all_skills = SkillNode.objects.all().order_by('name')
        
        return render(request, 'core/dashboard_rpg.html', {
            'profile': profile,
            'recent_sessions': recent_sessions,
            'recent_badges': recent_badges,
            'total_badges': total_badges,
            'daily_quest_completed': daily_quest_completed,
            'next_level_xp': next_level_xp,
            'progress_percent': progress_percent,
            'top_skills': top_skills,
            'next_boss': next_boss,
            'all_skills': all_skills,
        })
    except Exception as e:
        return HttpResponse(f"<h1>Erro no Dashboard</h1><pre>{str(e)}</pre><p>Tipo: {type(e).__name__}</p>")

@login_required
def quest_board(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    quests = JobQuest.objects.filter(is_active=True)
    bosses_active = BossBattle.objects.filter(is_active=True)
    bosses_locked = BossBattle.objects.filter(is_active=False)[:3]
    return render(request, 'core/quests.html', {'quests': quests, 'bosses': bosses_active, 'locked_bosses': bosses_locked, 'profile': profile})

@login_required
def battle_arena(request, boss_id):
    boss = get_object_or_404(BossBattle, pk=boss_id, is_active=True)
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    
    if request.method == 'POST':
        repo_link = request.POST.get('repo_link')
        sos_requested = request.POST.get('sos_requested') == 'on'
        if repo_link:
            ProjectSubmission.objects.create(
                user=request.user,
                boss=boss,
                repo_link=repo_link,
                sos_requested=sos_requested
            )
            # Recompensas automáticas
            profile.adicionar_xp(boss.xp_reward)
            profile.dev_coins += boss.coin_reward
            profile.save()
            
            # Criar badge especial do boss
            from .models import Badge, UserBadge
            badge_slug = f'boss-{boss.id}'
            badge, created = Badge.objects.get_or_create(
                slug=badge_slug,
                defaults={
                    'name': f'Vencedor: {boss.title}',
                    'description': f'Derrotou o boss {boss.title}',
                    'icon_class': boss.boss_icon,
                    'xp_bonus': 0,
                    'coin_bonus': 0,
                    'is_secret': False
                }
            )
            UserBadge.objects.get_or_create(user_profile=profile, badge=badge)
            
            return redirect(f'/gamer/arena/{boss_id}/?success=Boss derrotado! +{boss.xp_reward} XP e +{boss.coin_reward} Coins!')
    
    submissions = ProjectSubmission.objects.filter(boss=boss).order_by('-created_at')
    my_submission = ProjectSubmission.objects.filter(boss=boss, user=request.user).first()
    
    return render(request, 'core/arena.html', {
        'boss': boss,
        'submissions': submissions,
        'my_submission': my_submission
    })

@login_required
def inventario(request):
    from .models import UserInventory, StoreItem
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    inventory, _ = UserInventory.objects.get_or_create(user=request.user)
    items = StoreItem.objects.all().order_by('price')
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        if item_id:
            item = get_object_or_404(StoreItem, pk=item_id)
            
            if action == 'buy':
                if item in inventory.items.all():
                    return redirect('/gamer/inventario/?error=Você já possui este item!')
                if profile.dev_coins >= item.price:
                    profile.dev_coins -= item.price
                    profile.save()
                    inventory.items.add(item)
                    return redirect('/gamer/inventario/?success=Item comprado com sucesso!')
                else:
                    return redirect('/gamer/inventario/?error=Saldo insuficiente de DevCoins!')
            
            elif action == 'equip':
                if item not in inventory.items.all():
                    return redirect('/gamer/inventario/?error=Você não possui este item!')
                if item.category == 'FRAME':
                    profile.equipped_frame = item
                    profile.save()
                    return redirect('/gamer/inventario/?success=Moldura equipada!')
                elif item.category == 'BANNER':
                    profile.equipped_banner = item
                    profile.save()
                    return redirect('/gamer/inventario/?success=Banner equipado!')
    
    return render(request, 'core/inventory.html', {'inventory': inventory, 'items': items, 'profile': profile})

@login_required
def create_session(request):
    if request.method == 'POST':
        skill_id = request.POST.get('skill')
        method = request.POST.get('method')
        duration = int(request.POST.get('duration', 0))
        notes = request.POST.get('notes', '')
        
        if skill_id and method and duration > 0:
            skill = get_object_or_404(SkillNode, pk=skill_id)
            profile = UserProfile.objects.get_or_create(user=request.user)[0]
            now = timezone.now()
            
            multipliers = {'VIDEO': 1.0, 'READING': 1.2, 'CODING': 1.5, 'PROJECT': 2.0}
            base_xp = duration * 2
            xp = int(base_xp * multipliers.get(method, 1.0))
            coins = duration // 10
            
            session = StudySession.objects.create(
                user=request.user,
                skill=skill,
                method=method,
                start_time=now,
                end_time=now + timedelta(minutes=duration),
                description=notes,
                xp_earned=xp,
                coins_earned=coins
            )
            
            profile.adicionar_xp(xp)
            profile.dev_coins += coins
            profile.skills_desbloqueadas.add(skill)
            
            today = timezone.now().date()
            if profile.last_checkin != today:
                if profile.last_checkin == today - timedelta(days=1):
                    profile.current_streak += 1
                else:
                    profile.current_streak = 1
                profile.last_checkin = today
                if profile.current_streak > profile.longest_streak:
                    profile.longest_streak = profile.current_streak
            
            profile.save()
            return redirect(f'/gamer/?success=Sessão registrada! +{xp} XP e +{coins} Coins!')
    return redirect('core:dashboard_gamer')


@login_required
def skill_tree(request):
    try:
        profile = UserProfile.objects.get_or_create(user=request.user)[0]
        skills = SkillNode.objects.all()
        
        if not skills.exists():
            return render(request, 'core/roadmap.html', {
                'mermaid_chart': 'graph TD\nA["Execute: python manage.py populate_tree"]',
                'profile': profile,
                'empty': True
            })
        
        unlocked_ids = set(profile.skills_desbloqueadas.values_list('id', flat=True))
        
        chart_data = []
        for skill in skills:
            status = 'unlocked' if skill.id in unlocked_ids else 'locked'
            node_id = f'node_{skill.id}'
            chart_data.append(f'{node_id}("{skill.name}"):::{status}')
            if skill.parent:
                parent_id = f'node_{skill.parent.id}'
                chart_data.append(f'{parent_id} --> {node_id}')
        
        mermaid_chart = 'graph TD\n' + '\n'.join(chart_data)
        return render(request, 'core/roadmap.html', {'mermaid_chart': mermaid_chart, 'profile': profile})
    except Exception as e:
        return HttpResponse(f'<h1>Erro Skill Tree</h1><pre>{str(e)}</pre><p>Rode: python manage.py populate_tree</p>')

@login_required
def conquistas_rpg(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    my_badges = UserBadge.objects.filter(user_profile=profile).select_related('badge')
    all_bosses = BossBattle.objects.all()
    defeated_bosses = ProjectSubmission.objects.filter(user=request.user).values_list('boss_id', flat=True)
    
    boss_medals = []
    for boss in all_bosses:
        boss_medals.append({
            'boss': boss,
            'defeated': boss.id in defeated_bosses
        })
    
    return render(request, 'core/conquistas_rpg.html', {
        'profile': profile,
        'my_badges': my_badges,
        'boss_medals': boss_medals
    })

@login_required
def trophy_room(request):
    victories = ProjectSubmission.objects.filter(user=request.user).values_list('boss_id', flat=True)
    all_bosses = BossBattle.objects.all().order_by('min_skill_level')
    return render(request, 'core/trophies.html', {'all_bosses': all_bosses, 'victories': victories})

@login_required
def war_room(request):
    from .models import CodeReview
    sos_signals = ProjectSubmission.objects.filter(sos_requested=True).select_related('user', 'boss').prefetch_related('reviews').order_by('-created_at')
    return render(request, 'core/war_room.html', {'sos_signals': sos_signals})

@login_required
def war_room_detail(request, submission_id):
    from .models import CodeReview, Notification
    submission = get_object_or_404(ProjectSubmission, pk=submission_id)
    reviews = submission.reviews.select_related('author').order_by('-created_at')
    
    if request.method == 'POST':
        CodeReview.objects.create(
            submission=submission,
            author=request.user,
            role=request.POST.get('role'),
            content=request.POST.get('content')
        )
        profile = UserProfile.objects.get_or_create(user=request.user)[0]
        profile.adicionar_xp(10)
        profile.dev_coins += 5
        profile.save()
        
        if submission.user != request.user:
            Notification.objects.create(
                user=submission.user,
                title='Reforços Chegaram! 🛡️',
                message=f'{request.user.username} enviou ajuda na sua missão.',
                type='INFO',
                link=f'/gamer/war-room/{submission_id}/'
            )
        
        return redirect(f'/gamer/war-room/{submission_id}/?success=Reforço enviado! +10 XP')
    
    return render(request, 'core/war_room_detail.html', {'submission': submission, 'reviews': reviews})

@login_required
def accept_solution(request, review_id):
    from .models import CodeReview, Notification
    review = get_object_or_404(CodeReview, pk=review_id)
    
    if request.user != review.submission.user:
        return redirect(f'/gamer/war-room/{review.submission.id}/?error=Apenas o comandante pode aceitar')
    
    review.is_accepted = True
    review.save()
    
    hero = UserProfile.objects.get_or_create(user=review.author)[0]
    hero.adicionar_xp(300)
    hero.dev_coins += 50
    hero.save()
    
    Notification.objects.create(
        user=review.author,
        title='Solução Aceita! 🏆',
        message=f'Sua ajuda foi aceita! +300 XP e +50 Coins',
        type='SUCCESS',
        link=f'/gamer/war-room/{review.submission.id}/'
    )
    
    return redirect(f'/gamer/war-room/{review.submission.id}/?success=Solução aceita! Herói recompensado')

@login_required
def user_profile(request):
    from .models import UserBadge, UserInventory, StoreItem
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    inventory, _ = UserInventory.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'edit':
            bio = request.POST.get('bio', '')
            github_link = request.POST.get('github_link', '')
            profile.bio = bio
            profile.github_link = github_link
            profile.save()
            return redirect('/gamer/profile/?success=Perfil atualizado!')
        
        elif action == 'equip':
            item_id = request.POST.get('item_id')
            if item_id:
                item = get_object_or_404(StoreItem, pk=item_id)
                if item in inventory.items.all():
                    if item.category == 'FRAME':
                        profile.equipped_frame = item
                    elif item.category == 'BANNER':
                        profile.equipped_banner = item
                    profile.save()
                    return redirect('/gamer/profile/?success=Item equipado!')
        
        elif action == 'unequip':
            item_type = request.POST.get('item_type')
            if item_type == 'frame':
                profile.equipped_frame = None
            elif item_type == 'banner':
                profile.equipped_banner = None
            profile.save()
            return redirect('/gamer/profile/?success=Item removido!')
    
    defeated_bosses = ProjectSubmission.objects.filter(user=request.user).select_related('boss')
    top_skills = profile.skills_desbloqueadas.all()[:5]
    recent_badges = UserBadge.objects.filter(user_profile=profile).select_related('badge').order_by('-earned_at')[:6]
    
    frames = inventory.items.filter(category='FRAME')
    banners = inventory.items.filter(category='BANNER')
    
    next_level_xp = profile.xp_to_next_level()
    progress_percent = int((profile.current_xp / next_level_xp) * 100) if next_level_xp else 0
    
    return render(request, 'core/profile.html', {
        'profile': profile,
        'defeated_bosses': defeated_bosses,
        'top_skills': top_skills,
        'recent_badges': recent_badges,
        'frames': frames,
        'banners': banners,
        'next_level_xp': next_level_xp,
        'progress_percent': progress_percent
    })
