from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Visitante
from .reconhecimento_facial import ReconhecimentoFacial
from django.views.decorators.csrf import csrf_exempt
from .models import Visitante
from django.http import JsonResponse
import json

@login_required
def registrar_face(request, visitante_id):
    """View para registrar a face de um visitante"""
    try:
        visitante = Visitante.objects.get(id=visitante_id)
        reconhecimento = ReconhecimentoFacial()
        
        if reconhecimento.capturar_face(visitante_id):
            visitante.face_id = str(visitante_id)
            visitante.save()
            messages.success(request, 'Face registrada com sucesso!')
        else:
            messages.error(request, 'Não foi possível registrar a face. Tente novamente.')
            
        return redirect('recepcao:detalhe_visitante', visitante_id=visitante_id)
        
    except Visitante.DoesNotExist:
        messages.error(request, 'Visitante não encontrado.')
        return redirect('recepcao:lista_visitantes')

@login_required
def verificar_face(request, visitante_id):
    """View para verificar a face de um visitante"""
    try:
        visitante = Visitante.objects.get(id=visitante_id)
        
        if not visitante.face_id:
            messages.error(request, 'Este visitante ainda não tem face registrada.')
            return redirect('recepcao:detalhe_visitante', visitante_id=visitante_id)
            
        reconhecimento = ReconhecimentoFacial()
        if reconhecimento.verificar_face(visitante_id):
            messages.success(request, 'Face verificada com sucesso!')
        else:
            messages.error(request, 'Verificação facial falhou. Tente novamente.')
            
        return redirect('recepcao:detalhe_visitante', visitante_id=visitante_id)
        
    except Visitante.DoesNotExist:
        messages.error(request, 'Visitante não encontrado.')
        return redirect('recepcao:lista_visitantes')

@csrf_exempt
def registrar_face_api(request):
    return JsonResponse({
        'success': False,
        'message': 'Reconhecimento facial temporariamente desativado'
    })

@csrf_exempt
def verificar_face_api(request):
    return JsonResponse({
        'success': False,
        'message': 'Reconhecimento facial temporariamente desativado'
    })

@csrf_exempt
def verificar_face_frame_api(request):
    return JsonResponse({
        'success': False,
        'message': 'Reconhecimento facial temporariamente desativado'
    })
