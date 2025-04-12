from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from main.forms import VisitaForm
from main.models import Visita

class RegistrarVisitaViewTests(TestCase):
  def setUp(self):
    self.client = Client()
    self.url = reverse('main:registrar_visita')

  def test_registrar_visita_get(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'visitas/registrar_visita.html')
    self.assertIsInstance(response.context['form'], VisitaForm)

  def test_registrar_visita_post_valid(self):
    data = {
      'campo1': 'valor1',  # substitua pelos campos reais do formulário VisitaForm
      'campo2': 'valor2',
    }
    response = self.client.post(self.url, data)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('main:home_sistema'))
    self.assertTrue(Visita.objects.filter(campo1='valor1').exists())  # substitua pelos campos reais do modelo Visita

    messages = list(get_messages(response.wsgi_request))
    self.assertEqual(len(messages), 1)
    self.assertEqual(str(messages[0]), 'Visita registrada com sucesso!')

  def test_registrar_visita_post_invalid(self):
    data = {
      'campo1': '',  # dados inválidos
    }
    response = self.client.post(self.url, data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'visitas/registrar_visita.html')
    self.assertIsInstance(response.context['form'], VisitaForm)
    self.assertFalse(response.context['form'].is_valid())