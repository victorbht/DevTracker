"""
Sistema de Export/Import de Dados
Permite exportar relatórios e importar sessões
"""

from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
import csv
import json
from io import BytesIO


class DataExporter:
    """Exportador de dados em múltiplos formatos"""
    
    def __init__(self, user):
        self.user = user
    
    def export_sessions_csv(self, start_date=None, end_date=None):
        """
        Exporta sessões de estudo em CSV
        """
        from .models import SessaoEstudo
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="sessoes_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Data', 'Tecnologia', 'Tópico', 'Método', 'Tempo (HH:MM:SS)', 'Exercícios', 'Acertos', 'Taxa Acerto %'])
        
        sessoes = SessaoEstudo.objects.select_related('tecnologia', 'metodo').all()
        
        if start_date:
            sessoes = sessoes.filter(data_registro__date__gte=start_date)
        if end_date:
            sessoes = sessoes.filter(data_registro__date__lte=end_date)
        
        for sessao in sessoes.order_by('-data_registro'):
            taxa_acerto = ''
            if sessao.qtd_exercicios > 0:
                taxa_acerto = f"{(sessao.qtd_acertos / sessao.qtd_exercicios * 100):.1f}"
            
            writer.writerow([
                sessao.data_registro.strftime('%d/%m/%Y %H:%M'),
                sessao.tecnologia.nome,
                sessao.topico,
                sessao.metodo.nome if sessao.metodo else '',
                str(sessao.tempo_liquido),
                sessao.qtd_exercicios,
                sessao.qtd_acertos,
                taxa_acerto
            ])
        
        return response
    
    def export_achievements_json(self):
        """
        Exporta conquistas em JSON
        """
        from .models import PerfilUsuario
        
        try:
            perfil = PerfilUsuario.objects.get(user=self.user)
        except PerfilUsuario.DoesNotExist:
            return HttpResponse('{"error": "Perfil não encontrado"}', content_type='application/json')
        
        conquistas = []
        for c in perfil.conquistas.all():
            conquistas.append({
                'nome': c.nome,
                'descricao': c.descricao,
                'categoria': c.categoria,
                'xp_reward': c.xp_reward,
                'icone': c.icone_fa,
                'cor': c.cor_hex
            })
        
        data = {
            'usuario': self.user.username,
            'exportado_em': timezone.now().isoformat(),
            'nivel': perfil.nivel,
            'xp_total': perfil.xp_total,
            'conquistas': conquistas,
            'total_conquistas': len(conquistas)
        }
        
        response = HttpResponse(
            json.dumps(data, indent=2, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="conquistas_{self.user.username}.json"'
        
        return response
    
    def export_full_report_html(self):
        """
        Exporta relatório completo em HTML
        """
        from .models import SessaoEstudo, PerfilUsuario
        from .analytics import AnalyticsEngine
        
        perfil = PerfilUsuario.objects.get_or_create(user=self.user)[0]
        analytics = AnalyticsEngine(self.user)
        
        # Estatísticas
        total_obj = SessaoEstudo.objects.aggregate(t=Sum('tempo_liquido'))['t']
        total_horas = total_obj.total_seconds() / 3600 if total_obj else 0
        
        productivity = analytics.get_productivity_score()
        mastery = analytics.get_technology_mastery()
        patterns = analytics.get_study_patterns()
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Relatório DevTracker - {self.user.username}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
                .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }}
                .stat-value {{ font-size: 36px; font-weight: bold; }}
                .stat-label {{ font-size: 14px; opacity: 0.9; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #34495e; color: white; }}
                .progress-bar {{ background: #ecf0f1; border-radius: 10px; height: 20px; overflow: hidden; }}
                .progress-fill {{ background: linear-gradient(90deg, #3498db, #2ecc71); height: 100%; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Relatório DevTracker</h1>
                <p><strong>Usuário:</strong> {self.user.username}</p>
                <p><strong>Gerado em:</strong> {timezone.now().strftime('%d/%m/%Y às %H:%M')}</p>
                
                <h2>📈 Visão Geral</h2>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value">{total_horas:.1f}h</div>
                        <div class="stat-label">Total de Estudo</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">Nível {perfil.nivel}</div>
                        <div class="stat-label">{perfil.xp_total} XP</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{productivity['score']}/100</div>
                        <div class="stat-label">Score de Produtividade</div>
                    </div>
                </div>
                
                <h2>🎯 Maestria em Tecnologias</h2>
                <table>
                    <tr>
                        <th>Tecnologia</th>
                        <th>Nível</th>
                        <th>Horas</th>
                        <th>Score</th>
                    </tr>
        """
        
        for tech in mastery[:10]:
            html += f"""
                    <tr>
                        <td>{tech['tecnologia']}</td>
                        <td>{tech['nivel']}</td>
                        <td>{tech['horas']}h</td>
                        <td>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {tech['score']}%"></div>
                            </div>
                        </td>
                    </tr>
            """
        
        html += f"""
                </table>
                
                <h2>📅 Padrões de Estudo</h2>
                <ul>
                    <li><strong>Duração média:</strong> {patterns['duracao_media']} minutos</li>
                    <li><strong>Preferência:</strong> Sessões {patterns['preferencia_duracao']}</li>
                    <li><strong>Dia favorito:</strong> {patterns.get('dia_favorito', 'N/A')}</li>
                </ul>
                
                <h2>🏆 Conquistas ({perfil.conquistas.count()})</h2>
                <table>
                    <tr>
                        <th>Nome</th>
                        <th>Categoria</th>
                        <th>XP</th>
                    </tr>
        """
        
        for c in perfil.conquistas.all():
            html += f"""
                    <tr>
                        <td>{c.nome}</td>
                        <td>{c.get_categoria_display()}</td>
                        <td>{c.xp_reward} XP</td>
                    </tr>
            """
        
        html += """
                </table>
            </div>
        </body>
        </html>
        """
        
        response = HttpResponse(html, content_type='text/html; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="relatorio_{self.user.username}.html"'
        
        return response


class DataImporter:
    """Importador de dados"""
    
    @staticmethod
    def import_sessions_from_csv(file, user):
        """
        Importa sessões de estudo de arquivo CSV
        Formato esperado: Data, Tecnologia, Tópico, Método, Tempo
        """
        from .models import SessaoEstudo, Tecnologia, MetodoEstudo
        import csv
        from io import TextIOWrapper
        
        results = {
            'imported': 0,
            'skipped': 0,
            'errors': []
        }
        
        try:
            # Decodifica arquivo
            text_file = TextIOWrapper(file, encoding='utf-8')
            reader = csv.DictReader(text_file)
            
            for row in reader:
                try:
                    # Parse data
                    data_str = row.get('Data', '').strip()
                    data = datetime.strptime(data_str, '%d/%m/%Y %H:%M')
                    
                    # Tecnologia
                    tech_nome = row.get('Tecnologia', '').strip()
                    tech, _ = Tecnologia.objects.get_or_create(nome=tech_nome)
                    
                    # Método
                    metodo_nome = row.get('Método', '').strip()
                    metodo = None
                    if metodo_nome:
                        metodo, _ = MetodoEstudo.objects.get_or_create(nome=metodo_nome)
                    
                    # Tempo
                    tempo_str = row.get('Tempo (HH:MM:SS)', '').strip()
                    h, m, s = map(int, tempo_str.split(':'))
                    tempo = timedelta(hours=h, minutes=m, seconds=s)
                    
                    # Cria sessão
                    SessaoEstudo.objects.create(
                        tecnologia=tech,
                        topico=row.get('Tópico', '').strip(),
                        metodo=metodo,
                        data_registro=timezone.make_aware(data),
                        tempo_liquido=tempo,
                        qtd_exercicios=int(row.get('Exercícios', 0) or 0),
                        qtd_acertos=int(row.get('Acertos', 0) or 0)
                    )
                    
                    results['imported'] += 1
                    
                except Exception as e:
                    results['errors'].append(f"Linha {reader.line_num}: {str(e)}")
                    results['skipped'] += 1
        
        except Exception as e:
            results['errors'].append(f"Erro geral: {str(e)}")
        
        return results
