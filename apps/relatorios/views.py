from django.db import models
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.db.models import Count, Avg, Q
import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from apps.recepcao.models import Visita

# Create your views here.

def dashboard(request):
    return render(request, 'relatorios/dashboard.html')

@require_GET
def api_cards(request):
    total_acessos = Visita.objects.count()
    visitantes_unicos = Visita.objects.values('visitante_id').distinct().count()
    alertas = Visita.objects.filter(status='cancelada').count()
    tempo_medio = Visita.objects.filter(status='finalizada', data_saida__isnull=False).annotate(
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
def api_graficos(request):
    # Pizza: distribuição por status
    pizza_labels = ['Em Andamento', 'Finalizada', 'Cancelada']
    pizza_values = [
        Visita.objects.filter(status='em_andamento').count(),
        Visita.objects.filter(status='finalizada').count(),
        Visita.objects.filter(status='cancelada').count(),
    ]
    # Linha: acessos por dia da semana (últimos 7 dias)
    from django.utils import timezone
    import datetime
    hoje = timezone.now().date()
    dias = [(hoje - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
    labels = [d.strftime('%a') for d in dias]
    acessos = [Visita.objects.filter(data_entrada__date=d).count() for d in dias]
    alertas = [Visita.objects.filter(data_entrada__date=d, status='cancelada').count() for d in dias]
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
def api_tabela(request):
    data_filtro = request.GET.get('data')
    tipo_filtro = request.GET.get('tipo')
    usuario_filtro = request.GET.get('usuario')
    qs = Visita.objects.select_related('visitante')
    if data_filtro:
        qs = qs.filter(data_entrada__date=data_filtro)
    if tipo_filtro:
        if tipo_filtro.lower() in ['em_andamento', 'finalizada', 'cancelada']:
            qs = qs.filter(status=tipo_filtro.lower())
        else:
            qs = qs.filter(objetivo__icontains=tipo_filtro)
    if usuario_filtro:
        qs = qs.filter(visitante__nome_completo__icontains=usuario_filtro)
    rows = [
        {
            'data': v.data_entrada.strftime('%Y-%m-%d %H:%M'),
            'tipo': v.get_status_display(),
            'usuario': v.visitante.nome_completo,
            'descricao': v.objetivo,
        }
        for v in qs.order_by('-data_entrada')[:100]
    ]
    return JsonResponse({'rows': rows})

# Exportação PDF
@require_GET
def exportar_pdf(request):
    data_filtro = request.GET.get('data')
    tipo_filtro = request.GET.get('tipo')
    usuario_filtro = request.GET.get('usuario')
    qs = Visita.objects.select_related('visitante')
    if data_filtro:
        qs = qs.filter(data_entrada__date=data_filtro)
    if tipo_filtro:
        if tipo_filtro.lower() in ['em_andamento', 'finalizada', 'cancelada']:
            qs = qs.filter(status=tipo_filtro.lower())
        else:
            qs = qs.filter(objetivo__icontains=tipo_filtro)
    if usuario_filtro:
        qs = qs.filter(visitante__nome_completo__icontains=usuario_filtro)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFont('Helvetica-Bold', 16)
    p.drawString(50, height - 50, 'Relatório de Visitas')
    p.setFont('Helvetica', 10)
    y = height - 80
    p.drawString(50, y, 'Data       | Tipo         | Usuário         | Descrição')
    y -= 15
    for v in qs.order_by('-data_entrada')[:100]:
        linha = f"{v.data_entrada.strftime('%Y-%m-%d %H:%M')} | {v.get_status_display():<12} | {v.visitante.nome_completo[:15]:<15} | {v.objetivo}"
        p.drawString(50, y, linha)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='relatorio_visitas.pdf')

# Exportação Excel
@require_GET
def exportar_excel(request):
    data_filtro = request.GET.get('data')
    tipo_filtro = request.GET.get('tipo')
    usuario_filtro = request.GET.get('usuario')
    qs = Visita.objects.select_related('visitante')
    if data_filtro:
        qs = qs.filter(data_entrada__date=data_filtro)
    if tipo_filtro:
        if tipo_filtro.lower() in ['em_andamento', 'finalizada', 'cancelada']:
            qs = qs.filter(status=tipo_filtro.lower())
        else:
            qs = qs.filter(objetivo__icontains=tipo_filtro)
    if usuario_filtro:
        qs = qs.filter(visitante__nome_completo__icontains=usuario_filtro)
    data = [
        {
            'Data': v.data_entrada.strftime('%Y-%m-%d %H:%M'),
            'Tipo': v.get_status_display(),
            'Usuário': v.visitante.nome_completo,
            'Descrição': v.objetivo,
        }
        for v in qs.order_by('-data_entrada')[:100]
    ]
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='relatorio_visitas.xlsx')
