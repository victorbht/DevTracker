"""
Views adicionais para funcionalidades avançadas
Rankings, Analytics, Export/Import
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .leaderboards import LeaderboardManager, get_leaderboard_context, AchievementComparison
from .analytics import AnalyticsEngine, generate_weekly_report
from .export_import import DataExporter, DataImporter
from .cache_utils import CacheManager
import json


@login_required
def leaderboards_view(request):
    """
    Página de rankings e leaderboards
    """
    context = get_leaderboard_context(request.user)
    context['page_title'] = 'Rankings'
    
    return render(request, 'core/leaderboards.html', context)


@login_required
def analytics_dashboard(request):
    """
    Dashboard de analytics avançado
    """
    analytics = AnalyticsEngine(request.user)
    
    context = {
        'productivity': analytics.get_productivity_score(),
        'prediction': analytics.predict_next_week_hours(),
        'best_times': analytics.get_best_study_times(),
        'patterns': analytics.get_study_patterns(),
        'mastery': analytics.get_technology_mastery(),
        'next_achievements': analytics.get_achievement_prediction(),
        'page_title': 'Analytics'
    }
    
    return render(request, 'core/analytics_dashboard.html', context)


@login_required
def weekly_report_view(request):
    """
    Relatório semanal completo
    """
    report = generate_weekly_report(request.user)
    
    context = {
        'report': report,
        'page_title': 'Relatório Semanal'
    }
    
    return render(request, 'core/weekly_report.html', context)


@login_required
def export_data(request):
    """
    Página de exportação de dados
    """
    if request.method == 'POST':
        export_type = request.POST.get('export_type')
        exporter = DataExporter(request.user)
        
        if export_type == 'csv':
            return exporter.export_sessions_csv()
        elif export_type == 'json':
            return exporter.export_achievements_json()
        elif export_type == 'html':
            return exporter.export_full_report_html()
    
    return render(request, 'core/export_data.html', {'page_title': 'Exportar Dados'})


@login_required
@require_POST
def import_data(request):
    """
    Importação de sessões via CSV
    """
    if 'csv_file' not in request.FILES:
        return JsonResponse({'error': 'Nenhum arquivo enviado'}, status=400)
    
    file = request.FILES['csv_file']
    results = DataImporter.import_sessions_from_csv(file, request.user)
    
    return JsonResponse(results)


@login_required
def api_user_stats(request):
    """
    API JSON com estatísticas do usuário
    """
    from .cache_utils import get_user_total_hours, get_user_streak
    from .models import PerfilUsuario
    
    perfil = PerfilUsuario.objects.get_or_create(user=request.user)[0]
    
    data = {
        'username': request.user.username,
        'nivel': perfil.nivel,
        'xp_total': perfil.xp_total,
        'total_horas': get_user_total_hours(request.user),
        'streak': get_user_streak(request.user),
        'conquistas': perfil.conquistas.count()
    }
    
    return JsonResponse(data)


@login_required
def api_productivity_score(request):
    """
    API para score de produtividade
    """
    analytics = AnalyticsEngine(request.user)
    score = analytics.get_productivity_score()
    
    return JsonResponse(score)


@login_required
def api_global_ranking(request):
    """
    API para ranking global
    """
    limit = int(request.GET.get('limit', 50))
    period = request.GET.get('period', 'all')
    
    ranking = LeaderboardManager.get_global_ranking(limit=limit, period=period)
    
    return JsonResponse({'ranking': ranking})


@login_required
def api_my_position(request):
    """
    API para posição do usuário nos rankings
    """
    positions = LeaderboardManager.get_user_position(request.user)
    
    return JsonResponse(positions)


@login_required
def compare_achievements(request, username):
    """
    Compara conquistas com outro usuário
    """
    from django.contrib.auth.models import User
    
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('Usuário não encontrado', status=404)
    
    comparison = AchievementComparison.compare_with_user(request.user, other_user)
    
    if comparison is None:
        return HttpResponse('Erro ao comparar perfis', status=500)
    
    context = {
        'other_user': other_user,
        'comparison': comparison,
        'page_title': f'Comparar com {username}'
    }
    
    return render(request, 'core/compare_achievements.html', context)


@login_required
def rarest_achievements(request):
    """
    Mostra conquistas mais raras do usuário
    """
    rarest = AchievementComparison.get_rarest_achievements(request.user, limit=10)
    
    context = {
        'rarest_achievements': rarest,
        'page_title': 'Conquistas Raras'
    }
    
    return render(request, 'core/rarest_achievements.html', context)


@login_required
@require_POST
def warm_cache(request):
    """
    Pré-aquece o cache do usuário
    """
    CacheManager.warm_up_user_cache(request.user)
    
    return JsonResponse({'status': 'ok', 'message': 'Cache aquecido com sucesso'})


@login_required
@require_POST
def clear_cache(request):
    """
    Limpa o cache do usuário
    """
    CacheManager.clear_all_user_cache(request.user)
    
    return JsonResponse({'status': 'ok', 'message': 'Cache limpo com sucesso'})
