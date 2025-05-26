from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .models import Veiculo, HistoricoVeiculo
from .forms import VeiculoForm, SaidaVeiculoForm
import xlsxwriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from xhtml2pdf import pisa
import xlwt
from django.db.models import Count
from apps.autenticacao.decorators import agente_guarita_or_admin_required
from django.utils.timezone import localtime
from apps.autenticacao.decorators import block_recepcionista
from django.views.decorators.http import require_GET

@block_recepcionista
@agente_guarita_or_admin_required
def home_veiculos(request):
    hoje = datetime.now().date()
    
    # Veículos no estacionamento
    veiculos_presentes = Veiculo.objects.filter(
        data_entrada__isnull=False,
        data_saida__isnull=True,
        bloqueado=False
    ).count()
    
    # Total de veículos registrados hoje
    veiculos_hoje = Veiculo.objects.filter(
        data_entrada__date=hoje
    ).count()
    
    # Total de veículos registrados no mês
    veiculos_mes = Veiculo.objects.filter(
        data_entrada__year=hoje.year,
        data_entrada__month=hoje.month
    ).count()
    
    # Veículos bloqueados
    veiculos_bloqueados = Veiculo.objects.filter(bloqueado=True).count()
    
    context = {
        'veiculos_presentes': veiculos_presentes,
        'veiculos_hoje': veiculos_hoje,
        'veiculos_mes': veiculos_mes,
        'veiculos_bloqueados': veiculos_bloqueados,
    }
    
    return render(request, 'veiculos/home_veiculos.html', context)

@login_required(login_url='autenticacao:login_sistema')
def lista_veiculos(request):
    veiculos = Veiculo.objects.all().order_by('-data_entrada')
    
    # Paginação
    paginator = Paginator(veiculos, 10)  # 10 veículos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'veiculos/lista_veiculos.html', {'page_obj': page_obj})

@login_required(login_url='autenticacao:login_sistema')
def historico_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    historico = HistoricoVeiculo.objects.filter(veiculo=veiculo).order_by('-data_entrada')
    
    # Paginação
    paginator = Paginator(historico, 10)  # 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'veiculos/historico_veiculo.html', {
        'veiculo': veiculo,
        'page_obj': page_obj
    })

@login_required(login_url='autenticacao:login_sistema')
def exportar_excel(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    # Formatação
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#D9D9D9',
        'border': 1
    })
    
    # Cabeçalhos
    headers = ['Placa', 'Modelo', 'Tipo', 'Cor', 'Status', 'Data Entrada', 'Data Saída']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Dados
    veiculos = Veiculo.objects.all()
    for row, veiculo in enumerate(veiculos, start=1):
        worksheet.write(row, 0, veiculo.placa)
        worksheet.write(row, 1, veiculo.modelo)
        worksheet.write(row, 2, veiculo.get_tipo_display())
        worksheet.write(row, 3, veiculo.cor)
        worksheet.write(row, 4, veiculo.get_status_display())
        worksheet.write(row, 5, veiculo.data_entrada.strftime('%d/%m/%Y %H:%M'))
        worksheet.write(row, 6, veiculo.data_saida.strftime('%d/%m/%Y %H:%M') if veiculo.data_saida else '')
    
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=veiculos.xlsx'
    return response

@login_required(login_url='autenticacao:login_sistema')
def exportar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=veiculos.pdf'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Relatório de Veículos")
    
    # Cabeçalhos da tabela
    p.setFont("Helvetica-Bold", 12)
    headers = ['Placa', 'Modelo', 'Tipo', 'Status']
    x_positions = [50, 150, 300, 400]
    
    for i, header in enumerate(headers):
        p.drawString(x_positions[i], height - 100, header)
    
    # Dados
    p.setFont("Helvetica", 10)
    y = height - 120
    veiculos = Veiculo.objects.all()
    
    for veiculo in veiculos:
        if y < 100:  # Nova página se necessário
            p.showPage()
            y = height - 50
            p.setFont("Helvetica-Bold", 12)
            for i, header in enumerate(headers):
                p.drawString(x_positions[i], height - 50, header)
            p.setFont("Helvetica", 10)
            y = height - 70
        
        p.drawString(x_positions[0], y, veiculo.placa)
        p.drawString(x_positions[1], y, veiculo.modelo)
        p.drawString(x_positions[2], y, veiculo.get_tipo_display())
        p.drawString(x_positions[3], y, veiculo.get_status_display())
        y -= 20
    
    p.showPage()
    p.save()
    return response

@login_required(login_url='autenticacao:login_sistema')
def bloquear_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo_bloqueio')
        if motivo:
            veiculo.bloqueado = True
            veiculo.motivo_bloqueio = motivo
            veiculo.save()
            messages.success(request, 'Veículo bloqueado com sucesso!')
            return redirect('veiculos:lista_veiculos')
        else:
            messages.error(request, 'É necessário informar o motivo do bloqueio.')
    
    return render(request, 'veiculos/bloquear_veiculo.html', {'veiculo': veiculo})

@login_required(login_url='autenticacao:login_sistema')
def desbloquear_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    veiculo.bloqueado = False
    veiculo.motivo_bloqueio = None
    veiculo.data_bloqueio = None
    veiculo.save()
    messages.success(request, 'Veículo desbloqueado com sucesso!')
    return redirect('veiculos:lista_veiculos')

@login_required
def registro_entrada(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.status = 'DENTRO'
            veiculo.save()
            
            # Criar histórico
            HistoricoVeiculo.objects.create(
                veiculo=veiculo,
                data_entrada=timezone.now(),
                observacoes=form.cleaned_data.get('observacoes', '')
            )
            
            messages.success(request, 'Veículo registrado com sucesso!')
            return redirect('veiculos:home_veiculos')
    else:
        form = VeiculoForm()
    
    return render(request, 'veiculos/registro_entrada.html', {'form': form})

@login_required(login_url='autenticacao:login_sistema')
def registro_saida(request):
    if request.method == 'POST':
        form = SaidaVeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.cleaned_data['veiculo']
            veiculo.data_saida = timezone.now()
            veiculo.save()
            
            # Atualizar o registro no histórico
            historico = HistoricoVeiculo.objects.filter(
                veiculo=veiculo,
                data_saida__isnull=True
            ).first()
            
            if historico:
                historico.data_saida = veiculo.data_saida
                historico.save()
            
            messages.success(request, 'Saída registrada com sucesso!')
            return redirect('veiculos:lista_veiculos')
    else:
        form = SaidaVeiculoForm()
    
    return render(request, 'veiculos/registro_saida.html', {'form': form})

class HistoricoVeiculosView(LoginRequiredMixin, ListView):
    model = HistoricoVeiculo
    template_name = 'veiculos/historico.html'
    context_object_name = 'historicos'
    ordering = ['-data_entrada']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Histórico de Veículos'
        return context

def exportar_historico_pdf(request):
    historicos = HistoricoVeiculo.objects.all().order_by('-data_entrada')
    template = get_template('veiculos/relatorios/historico_pdf.html')
    context = {'historicos': historicos}
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="historico_veiculos.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF')
    return response

def exportar_historico_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="historico_veiculos.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Histórico de Veículos')
    
    # Estilo para cabeçalho
    header_style = xlwt.XFStyle()
    header_style.font.bold = True
    
    # Cabeçalhos
    columns = ['Placa', 'Modelo', 'Tipo', 'Data Entrada', 'Data Saída', 'Visitante']
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)
    
    # Dados
    historicos = HistoricoVeiculo.objects.all().order_by('-data_entrada')
    for row_num, historico in enumerate(historicos, 1):
        ws.write(row_num, 0, historico.veiculo.placa)
        ws.write(row_num, 1, historico.veiculo.modelo)
        ws.write(row_num, 2, historico.veiculo.get_tipo_display())
        ws.write(row_num, 3, historico.data_entrada.strftime('%d/%m/%Y %H:%M'))
        ws.write(row_num, 4, historico.data_saida.strftime('%d/%m/%Y %H:%M') if historico.data_saida else '')
        ws.write(row_num, 5, str(historico.visitante) if historico.visitante else '')
    
    wb.save(response)
    return response

class ListaVeiculosView(LoginRequiredMixin, ListView):
    model = Veiculo
    template_name = 'veiculos/lista_veiculos.html'
    context_object_name = 'veiculos'
    ordering = ['-data_entrada']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Veículos Cadastrados'
        return context

def exportar_veiculos_pdf(request):
    veiculos = Veiculo.objects.all().order_by('-data_entrada')
    template = get_template('veiculos/relatorios/veiculos_pdf.html')
    context = {'veiculos': veiculos}
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="veiculos_cadastrados.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF')
    return response

def exportar_veiculos_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="veiculos_cadastrados.xls"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Veículos Cadastrados')
    
    # Estilo para cabeçalho
    header_style = xlwt.XFStyle()
    header_style.font.bold = True
    
    # Cabeçalhos
    columns = ['Placa', 'Modelo', 'Tipo', 'Cor', 'Data Entrada', 'Status', 'Visitante']
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)
    
    # Dados
    veiculos = Veiculo.objects.all().order_by('-data_entrada')
    for row_num, veiculo in enumerate(veiculos, 1):
        ws.write(row_num, 0, veiculo.placa)
        ws.write(row_num, 1, veiculo.modelo)
        ws.write(row_num, 2, veiculo.get_tipo_display())
        ws.write(row_num, 3, veiculo.get_cor_display())
        ws.write(row_num, 4, veiculo.data_entrada.strftime('%d/%m/%Y %H:%M'))
        ws.write(row_num, 5, veiculo.get_status_display())
        ws.write(row_num, 6, str(veiculo.visitante) if veiculo.visitante else '')
    
    wb.save(response)
    return response

def veiculo_info_json(request):
    veiculo_id = request.GET.get('veiculo_id')
    if not veiculo_id:
        return JsonResponse({'erro': 'ID não informado'}, status=400)
    try:
        veiculo = Veiculo.objects.get(id=veiculo_id)
        data = {
            'placa': veiculo.placa,
            'modelo': veiculo.modelo,
            'cor': veiculo.get_cor_display() if hasattr(veiculo, 'get_cor_display') else veiculo.cor,
            'tipo': veiculo.get_tipo_display() if hasattr(veiculo, 'get_tipo_display') else veiculo.tipo,
            'data_entrada': localtime(veiculo.data_entrada).strftime('%d/%m/%Y %H:%M'),
            'visitante': str(veiculo.visitante) if veiculo.visitante else '',
        }
        return JsonResponse(data)
    except Veiculo.DoesNotExist:
        return JsonResponse({'erro': 'Veículo não encontrado'}, status=404)

@require_GET
@login_required(login_url='autenticacao:login_sistema')
def veiculo_info_por_placa_json(request):
    placa = request.GET.get('placa')
    if not placa:
        return JsonResponse({'erro': 'Placa não informada'}, status=400)
    veiculo = Veiculo.objects.filter(placa__iexact=placa).order_by('-data_entrada').first()
    if veiculo:
        data = {
            'placa': veiculo.placa,
            'modelo': veiculo.modelo,
            'cor': veiculo.get_cor_display() if hasattr(veiculo, 'get_cor_display') else veiculo.cor,
            'tipo': veiculo.get_tipo_display() if hasattr(veiculo, 'get_tipo_display') else veiculo.tipo,
            'nome_condutor': veiculo.nome_condutor,
            'nome_passageiro': veiculo.nome_passageiro,
            'observacoes': veiculo.observacoes,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'erro': 'Veículo não encontrado'}, status=404)
