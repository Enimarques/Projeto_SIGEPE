from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Veiculo, HistoricoVeiculo
from apps.recepcao.models import Visitante
from django.contrib.auth.models import User

# Create your tests here.

class VeiculoModelTest(TestCase):
    def setUp(self):
        self.visitante = Visitante.objects.create(
            nome="João Teste",
            cpf="12345678900",
            telefone="11999999999"
        )
        
        self.veiculo = Veiculo.objects.create(
            placa="ABC1234",
            tipo="carro",
            modelo="Gol",
            cor="Preto",
            visitante=self.visitante
        )

    def test_criacao_veiculo(self):
        """Testa a criação de um veículo"""
        self.assertTrue(isinstance(self.veiculo, Veiculo))
        self.assertEqual(self.veiculo.__str__(), "ABC1234 - Gol (Carro)")

    def test_validacao_placa(self):
        """Testa a validação da placa"""
        # Placa inválida
        veiculo_invalido = Veiculo(
            placa="ABC123@",
            tipo="carro",
            modelo="Gol",
            cor="Preto"
        )
        with self.assertRaises(Exception):
            veiculo_invalido.full_clean()

    def test_bloqueio_veiculo(self):
        """Testa o bloqueio de veículo"""
        self.veiculo.bloqueado = True
        self.veiculo.motivo_bloqueio = "Teste de bloqueio"
        self.veiculo.save()
        
        self.assertEqual(self.veiculo.status, 'bloqueado')
        self.assertIsNotNone(self.veiculo.data_bloqueio)

    def test_registro_saida(self):
        """Testa o registro de saída"""
        self.veiculo.data_saida = timezone.now()
        self.veiculo.save()
        
        self.assertEqual(self.veiculo.status, 'saida')
        self.assertFalse(self.veiculo.esta_no_estacionamento)

class HistoricoVeiculoModelTest(TestCase):
    def setUp(self):
        self.veiculo = Veiculo.objects.create(
            placa="XYZ5678",
            tipo="moto",
            modelo="Honda",
            cor="Vermelho"
        )
        
        self.historico = HistoricoVeiculo.objects.create(
            veiculo=self.veiculo,
            data_entrada=timezone.now(),
            observacoes="Teste de histórico"
        )

    def test_criacao_historico(self):
        """Testa a criação de um registro de histórico"""
        self.assertTrue(isinstance(self.historico, HistoricoVeiculo))
        self.assertEqual(
            self.historico.__str__(),
            f"{self.veiculo.placa} - {self.historico.data_entrada.date()}"
        )

class VeiculoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        
        self.veiculo = Veiculo.objects.create(
            placa="DEF5678",
            tipo="carro",
            modelo="Civic",
            cor="Branco"
        )

    def test_home_veiculos(self):
        """Testa a view da home de veículos"""
        response = self.client.get(reverse('veiculos:home_veiculos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'veiculos/home_veiculos.html')

    def test_lista_veiculos(self):
        """Testa a view de listagem de veículos"""
        response = self.client.get(reverse('veiculos:lista_veiculos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'veiculos/lista_veiculos.html')
        self.assertTrue('page_obj' in response.context)

    def test_historico_veiculo(self):
        """Testa a view de histórico de veículo"""
        response = self.client.get(
            reverse('veiculos:historico_veiculo', args=[self.veiculo.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'veiculos/historico_veiculo.html')

    def test_bloquear_veiculo(self):
        """Testa o bloqueio de veículo"""
        response = self.client.post(
            reverse('veiculos:bloquear_veiculo', args=[self.veiculo.id]),
            {'motivo_bloqueio': 'Teste de bloqueio'}
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        
        # Verifica se o veículo foi bloqueado
        veiculo_atualizado = Veiculo.objects.get(id=self.veiculo.id)
        self.assertTrue(veiculo_atualizado.bloqueado)
        self.assertEqual(veiculo_atualizado.motivo_bloqueio, 'Teste de bloqueio')

    def test_desbloquear_veiculo(self):
        """Testa o desbloqueio de veículo"""
        # Primeiro bloqueia o veículo
        self.veiculo.bloqueado = True
        self.veiculo.motivo_bloqueio = "Bloqueio para teste"
        self.veiculo.save()
        
        response = self.client.get(
            reverse('veiculos:desbloquear_veiculo', args=[self.veiculo.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        
        # Verifica se o veículo foi desbloqueado
        veiculo_atualizado = Veiculo.objects.get(id=self.veiculo.id)
        self.assertFalse(veiculo_atualizado.bloqueado)
        self.assertIsNone(veiculo_atualizado.motivo_bloqueio)

    def test_exportar_excel(self):
        """Testa a exportação para Excel"""
        response = self.client.get(reverse('veiculos:exportar_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def test_exportar_pdf(self):
        """Testa a exportação para PDF"""
        response = self.client.get(reverse('veiculos:exportar_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

class VeiculoFormTest(TestCase):
    def setUp(self):
        self.visitante = Visitante.objects.create(
            nome="Maria Teste",
            cpf="98765432100",
            telefone="11988888888"
        )

    def test_veiculo_form_valido(self):
        """Testa formulário com dados válidos"""
        data = {
            'placa': 'ABC1234',
            'tipo': 'carro',
            'modelo': 'Gol',
            'cor': 'Preto',
            'visitante': self.visitante.id,
            'observacoes': 'Teste de formulário'
        }
        form = VeiculoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_veiculo_form_invalido(self):
        """Testa formulário com dados inválidos"""
        data = {
            'placa': 'ABC123@',  # Placa inválida
            'tipo': 'carro',
            'modelo': 'Gol',
            'cor': 'Preto'
        }
        form = VeiculoForm(data=data)
        self.assertFalse(form.is_valid())

    def test_saida_veiculo_form(self):
        """Testa formulário de saída de veículo"""
        veiculo = Veiculo.objects.create(
            placa="GHI9012",
            tipo="carro",
            modelo="Fiesta",
            cor="Azul"
        )
        
        data = {
            'placa': veiculo.id,
            'data_saida': timezone.now(),
            'observacoes': 'Teste de saída'
        }
        form = SaidaVeiculoForm(data=data)
        self.assertTrue(form.is_valid())
