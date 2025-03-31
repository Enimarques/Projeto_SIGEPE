from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Visitante
# from .reconhecimento_facial import ReconhecimentoFacial
from django.http import JsonResponse
import json

@login_required
def registrar_face(request, visitante_id):
    """View para registrar a face de um visitante"""
    try:
        visitante = Visitante.objects.get(id=visitante_id)
        messages.warning(request, 'Reconhecimento facial temporariamente desativado')
        return redirect('recepcao:detalhe_visitante', visitante_id=visitante_id)
    except Visitante.DoesNotExist:
        messages.error(request, 'Visitante não encontrado.')
        return redirect('recepcao:lista_visitantes')

@login_required
def verificar_face(request, visitante_id):
    """View para verificar a face de um visitante"""
    try:
        visitante = Visitante.objects.get(id=visitante_id)
        messages.warning(request, 'Reconhecimento facial temporariamente desativado')
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
