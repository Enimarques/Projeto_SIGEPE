from django.contrib import admin
from django.utils.timezone import now
from .models import Pessoa , Setor , Usuario, Veiculo

class PessoaAdmin(admin.ModelAdmin):
  list_display = ('nome_completo','CPF','data_nascimento')  #as colunas que vao ser visiveis
  search_fields = ('nome_completo', 'CPF')        #os campos de pesquisa
  
class SetorAdmin (admin.ModelAdmin):
  list_display = ('nome', 'localização','disponibilidade')
  list_filter = ('nome','disponibilidade')

class UsuarioAdmin(admin.ModelAdmin):
  list_display = ('usuario', 'get_tipo_display')
  list_filter = ('tipo',)
  search_fields = ('usuario',)

class VeiculoAdmin(admin.ModelAdmin):
  list_display = ('placa', 'responsavel', 'horario_entrada', 'horario_saida')
  actions = ['registrar_saida']
  search_fields = ('placa', 'horario_entrada', 'responsavel')
  list_filter = ('placa','horario_entrada', 'horario_saida')


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Veiculo, VeiculoAdmin)
admin.site.register(Usuario, UsuarioAdmin)