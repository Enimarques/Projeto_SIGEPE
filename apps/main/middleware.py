import time
from .views import registrar_tempo_resposta

class TempoRespostaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        inicio = time.time()
        response = self.get_response(request)
        fim = time.time()
        duracao_ms = (fim - inicio) * 1000
        registrar_tempo_resposta(duracao_ms)
        return response 