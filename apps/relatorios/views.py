from django.db import models
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.db.models import Count, Avg, Q
from django.contrib.auth.decorators import login_required
from apps.autenticacao.services.auth_service import AuthenticationService
from apps.recepcao.models import Visita, Setor
import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Create your views here.

@login_required
def dashboard(request):
    # Verificar se é assessor para filtrar por gabinete
    is_assessor = AuthenticationService.is_assessor(request.user)
    departamento = None
    
    if is_assessor:
        try:
            departamento = request.user.setor_responsavel
        except:
            pass
    
    # Buscar todos os setores para o filtro (apenas se não for assessor)
    setores = Setor.objects.filter(ativo=True).order_by('tipo', 'nome_vereador', 'nome_local') if not is_assessor else []
    
    context = {
        'is_assessor': is_assessor,
        'departamento': departamento,
        'setores': setores
    }
    
    return render(request, 'relatorios/dashboard.html', context)

@require_GET
@login_required
def api_cards(request):
    # Verificar se é assessor para filtrar por gabinete
    is_assessor = AuthenticationService.is_assessor(request.user)
    departamento = None
    
    if is_assessor:
        try:
            departamento = request.user.setor_responsavel
        except:
            pass
    
    # Obter filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    setor_id = request.GET.get('setor')
    localizacao = request.GET.get('localizacao')
    objetivo = request.GET.get('objetivo')
    status = request.GET.get('status')
    
    # Filtrar visitas por departamento se for assessor
    visitas_queryset = Visita.objects.all()
    if departamento:
        visitas_queryset = visitas_queryset.filter(setor=departamento)
    
    # Aplicar filtros adicionais
    if data_inicio:
        from datetime import datetime
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            visitas_queryset = visitas_queryset.filter(data_entrada__date__gte=data_inicio_obj)
        except (ValueError, TypeError):
            pass
    
    if data_fim:
        from datetime import datetime, time
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            data_fim_completa = datetime.combine(data_fim_obj, time.max)
            visitas_queryset = visitas_queryset.filter(data_entrada__lte=data_fim_completa)
        except (ValueError, TypeError):
            pass
    
    if setor_id and not is_assessor:  # Assessores já têm filtro automático
        try:
            visitas_queryset = visitas_queryset.filter(setor_id=setor_id)
        except (ValueError, TypeError):
            pass
    
    if localizacao:
        visitas_queryset = visitas_queryset.filter(localizacao=localizacao)
    
    if objetivo:
        visitas_queryset = visitas_queryset.filter(objetivo=objetivo)
    
    if status:
        visitas_queryset = visitas_queryset.filter(status=status)
    
    total_acessos = visitas_queryset.count()
    visitantes_unicos = visitas_queryset.values('visitante_id').distinct().count()
    alertas = visitas_queryset.filter(status='cancelada').count()
    
    # Calcular tempo médio apenas para visitas finalizadas
    visitas_finalizadas = visitas_queryset.filter(status='finalizada', data_saida__isnull=False)
    tempo_medio = visitas_finalizadas.annotate(
        duracao_segundos=(models.F('data_saida') - models.F('data_entrada'))
    ).aggregate(media=Avg(models.ExpressionWrapper(models.F('data_saida') - models.F('data_entrada'), output_field=models.DurationField())))['media']
    tempo_medio_s = round(tempo_medio.total_seconds() if tempo_medio else 0, 1)
    
    data = {
        'acessos': total_acessos,
        'visitantes': visitantes_unicos,
        'alertas': alertas,
        'tempo_medio': tempo_medio_s
    }
    return JsonResponse(data)

@require_GET
@login_required
def api_graficos(request):
    # Verificar se é assessor para filtrar por gabinete
    is_assessor = AuthenticationService.is_assessor(request.user)
    departamento = None
    
    if is_assessor:
        try:
            departamento = request.user.setor_responsavel
        except:
            pass
    
    # Obter filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    setor_id = request.GET.get('setor')
    localizacao = request.GET.get('localizacao')
    objetivo = request.GET.get('objetivo')
    status = request.GET.get('status')
    
    # Filtrar visitas por departamento se for assessor
    visitas_queryset = Visita.objects.all()
    if departamento:
        visitas_queryset = visitas_queryset.filter(setor=departamento)
    
    # Aplicar filtros adicionais
    if data_inicio:
        from datetime import datetime
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            visitas_queryset = visitas_queryset.filter(data_entrada__date__gte=data_inicio_obj)
        except (ValueError, TypeError):
            pass
    
    if data_fim:
        from datetime import datetime, time
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            data_fim_completa = datetime.combine(data_fim_obj, time.max)
            visitas_queryset = visitas_queryset.filter(data_entrada__lte=data_fim_completa)
        except (ValueError, TypeError):
            pass
    
    if setor_id and not is_assessor:  # Assessores já têm filtro automático
        try:
            visitas_queryset = visitas_queryset.filter(setor_id=setor_id)
        except (ValueError, TypeError):
            pass
    
    if localizacao:
        visitas_queryset = visitas_queryset.filter(localizacao=localizacao)
    
    if objetivo:
        visitas_queryset = visitas_queryset.filter(objetivo=objetivo)
    
    if status:
        visitas_queryset = visitas_queryset.filter(status=status)
    
    # Pizza: distribuição por status
    pizza_labels = ['Em Andamento', 'Finalizada', 'Cancelada']
    pizza_values = [
        visitas_queryset.filter(status='em_andamento').count(),
        visitas_queryset.filter(status='finalizada').count(),
        visitas_queryset.filter(status='cancelada').count(),
    ]
    
    # Linha: acessos por dia da semana (últimos 7 dias)
    from django.utils import timezone
    import datetime
    hoje = timezone.now().date()
    dias = [(hoje - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
    labels = [d.strftime('%a') for d in dias]
    acessos = [visitas_queryset.filter(data_entrada__date=d).count() for d in dias]
    alertas = [visitas_queryset.filter(data_entrada__date=d, status='cancelada').count() for d in dias]
    
    data = {
        'pizza': {
            'labels': pizza_labels,
            'values': pizza_values,
        },
        'linha': {
            'labels': labels,
            'acessos': acessos,
            'alertas': alertas,
        }
    }
    return JsonResponse(data)

@require_GET
@login_required
def api_tabela(request):
    # Verificar se é assessor para filtrar por gabinete
    is_assessor = AuthenticationService.is_assessor(request.user)
    departamento = None
    
    if is_assessor:
        try:
            departamento = request.user.setor_responsavel
        except:
            pass
    
    # Obter filtros
    data_filtro = request.GET.get('data')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo_filtro = request.GET.get('tipo')
    status = request.GET.get('status')
    usuario_filtro = request.GET.get('usuario')
    setor_id = request.GET.get('setor')
    localizacao = request.GET.get('localizacao')
    objetivo = request.GET.get('objetivo')
    
    qs = Visita.objects.select_related('visitante', 'setor')
    
    # Filtrar por departamento se for assessor
    if departamento:
        qs = qs.filter(setor=departamento)
    
    # Filtro de data específica (tem prioridade sobre data única)
    if data_inicio or data_fim:
        from datetime import datetime, time
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                qs = qs.filter(data_entrada__date__gte=data_inicio_obj)
            except (ValueError, TypeError):
                pass
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                data_fim_completa = datetime.combine(data_fim_obj, time.max)
                qs = qs.filter(data_entrada__lte=data_fim_completa)
            except (ValueError, TypeError):
                pass
    elif data_filtro:
        qs = qs.filter(data_entrada__date=data_filtro)
    
    if status:
        qs = qs.filter(status=status)
    elif tipo_filtro:
        if tipo_filtro.lower() in ['em_andamento', 'finalizada', 'cancelada']:
            qs = qs.filter(status=tipo_filtro.lower())
        else:
            qs = qs.filter(objetivo__icontains=tipo_filtro)
    
    if setor_id and not is_assessor:  # Assessores já têm filtro automático
        try:
            qs = qs.filter(setor_id=setor_id)
        except (ValueError, TypeError):
            pass
    
    if localizacao:
        qs = qs.filter(localizacao=localizacao)
    
    if objetivo:
        qs = qs.filter(objetivo=objetivo)
    
    if usuario_filtro:
        qs = qs.filter(
            Q(visitante__nome_completo__icontains=usuario_filtro) |
            Q(visitante__CPF__icontains=usuario_filtro)
        )
    
    rows = [
        {
            'data': v.data_entrada.strftime('%Y-%m-%d %H:%M'),
            'tipo': v.get_status_display(),
            'usuario': v.visitante.nome_completo,
            'setor': str(v.setor),
            'localizacao': v.get_localizacao_display(),
            'objetivo': v.get_objetivo_display(),
            'descricao': v.objetivo,
        }
        for v in qs.order_by('-data_entrada')[:100]
    ]
    return JsonResponse({'rows': rows})

# Exportação PDF
@require_GET
@login_required
def exportar_pdf(request):
    # Verificar se é assessor para filtrar por gabinete
    is_assessor = AuthenticationService.is_assessor(request.user)
    departamento = None
    
    if is_assessor:
        try:
            departamento = request.user.setor_responsavel
        except:
            pass
    
    # Obter filtros
    data_filtro = request.GET.get('data')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo_filtro = request.GET.get('tipo')
    status = request.GET.get('status')
    usuario_filtro = request.GET.get('usuario')
    setor_id = request.GET.get('setor')
    localizacao = request.GET.get('localizacao')
    objetivo = request.GET.get('objetivo')
    
    qs = Visita.objects.select_related('visitante', 'setor')
    
    # Filtrar por departamento se for assessor
    if departamento:
        qs = qs.filter(setor=departamento)
    
    # Filtro de data específica (tem prioridade sobre data única)
    if data_inicio or data_fim:
        from datetime import datetime, time
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                qs = qs.filter(data_entrada__date__gte=data_inicio_obj)
            except (ValueError, TypeError):
                pass
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                data_fim_completa = datetime.combine(data_fim_obj, time.max)
                qs = qs.filter(data_entrada__lte=data_fim_completa)
            except (ValueError, TypeError):
                pass
    elif data_filtro:
        qs = qs.filter(data_entrada__date=data_filtro)
    
    if status:
        qs = qs.filter(status=status)
    elif tipo_filtro:
        if tipo_filtro.lower() in ['em_andamento', 'finalizada', 'cancelada']:
            qs = qs.filter(status=tipo_filtro.lower())
        else:
            qs = qs.filter(objetivo__icontains=tipo_filtro)
    
    if setor_id and not is_assessor:  # Assessores já têm filtro automático
        try:
            qs = qs.filter(setor_id=setor_id)
        except (ValueError, TypeError):
            pass
    
    if localizacao:
        qs = qs.filter(localizacao=localizacao)
    
    if objetivo:
        qs = qs.filter(objetivo=objetivo)
    
    if usuario_filtro:
        qs = qs.filter(
            Q(visitante__nome_completo__icontains=usuario_filtro) |
            Q(visitante__CPF__icontains=usuario_filtro)
        )
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Título do relatório
    p.setFont('Helvetica-Bold', 16)
    titulo = 'Relatório de Visitas'
    if departamento:
        if departamento.tipo in ['gabinete', 'gabinete_vereador']:
            titulo += f' - Gabinete {departamento.nome_vereador}'
        else:
            titulo += f' - Departamento {departamento.nome_local}'
    
    p.drawString(50, height - 50, titulo)
    p.setFont('Helvetica', 10)
    y = height - 80
    p.drawString(50, y, 'Data       | Tipo         | Usuário         | Setor              | Localização | Objetivo')
    y -= 15
    
    for v in qs.order_by('-data_entrada')[:100]:
        linha = f"{v.data_entrada.strftime('%Y-%m-%d %H:%M')} | {v.get_status_display():<12} | {v.visitante.nome_completo[:15]:<15} | {str(v.setor)[:20]:<20} | {v.get_localizacao_display():<10} | {v.get_objetivo_display()}"
        p.drawString(50, y, linha)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50
    
    p.save()
    buffer.seek(0)
    
    filename = 'relatorio_visitas.pdf'
    if departamento:
        if departamento.tipo in ['gabinete', 'gabinete_vereador']:
            filename = f'relatorio_gabinete_{departamento.nome_vereador.replace(" ", "_")}.pdf'
        else:
            filename = f'relatorio_departamento_{departamento.nome_local.replace(" ", "_")}.pdf'
    
    return FileResponse(buffer, as_attachment=True, filename=filename)

# Exportação Excel
@require_GET
@login_required
def exportar_excel(request):
    # Verificar se é assessor para filtrar por gabinete
    is_assessor = AuthenticationService.is_assessor(request.user)
    departamento = None
    
    if is_assessor:
        try:
            departamento = request.user.setor_responsavel
        except:
            pass
    
    # Obter filtros
    data_filtro = request.GET.get('data')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo_filtro = request.GET.get('tipo')
    status = request.GET.get('status')
    usuario_filtro = request.GET.get('usuario')
    setor_id = request.GET.get('setor')
    localizacao = request.GET.get('localizacao')
    objetivo = request.GET.get('objetivo')
    
    qs = Visita.objects.select_related('visitante', 'setor')
    
    # Filtrar por departamento se for assessor
    if departamento:
        qs = qs.filter(setor=departamento)
    
    # Filtro de data específica (tem prioridade sobre data única)
    if data_inicio or data_fim:
        from datetime import datetime, time
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                qs = qs.filter(data_entrada__date__gte=data_inicio_obj)
            except (ValueError, TypeError):
                pass
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                data_fim_completa = datetime.combine(data_fim_obj, time.max)
                qs = qs.filter(data_entrada__lte=data_fim_completa)
            except (ValueError, TypeError):
                pass
    elif data_filtro:
        qs = qs.filter(data_entrada__date=data_filtro)
    
    if status:
        qs = qs.filter(status=status)
    elif tipo_filtro:
        if tipo_filtro.lower() in ['em_andamento', 'finalizada', 'cancelada']:
            qs = qs.filter(status=tipo_filtro.lower())
        else:
            qs = qs.filter(objetivo__icontains=tipo_filtro)
    
    if setor_id and not is_assessor:  # Assessores já têm filtro automático
        try:
            qs = qs.filter(setor_id=setor_id)
        except (ValueError, TypeError):
            pass
    
    if localizacao:
        qs = qs.filter(localizacao=localizacao)
    
    if objetivo:
        qs = qs.filter(objetivo=objetivo)
    
    if usuario_filtro:
        qs = qs.filter(
            Q(visitante__nome_completo__icontains=usuario_filtro) |
            Q(visitante__CPF__icontains=usuario_filtro)
        )
    
    data = [
        {
            'Data': v.data_entrada.strftime('%Y-%m-%d %H:%M'),
            'Status': v.get_status_display(),
            'Visitante': v.visitante.nome_completo,
            'CPF': v.visitante.CPF or '',
            'Setor': str(v.setor),
            'Localização': v.get_localizacao_display(),
            'Objetivo': v.get_objetivo_display(),
            'Observações': v.observacoes or '',
        }
        for v in qs.order_by('-data_entrada')[:100]
    ]
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')
    buffer.seek(0)
    
    filename = 'relatorio_visitas.xlsx'
    if departamento:
        if departamento.tipo in ['gabinete', 'gabinete_vereador']:
            filename = f'relatorio_gabinete_{departamento.nome_vereador.replace(" ", "_")}.xlsx'
        else:
            filename = f'relatorio_departamento_{departamento.nome_local.replace(" ", "_")}.xlsx'
    
    return FileResponse(buffer, as_attachment=True, filename=filename)
