from django.contrib import admin

from .models import Visitante , Setor , Usuario, Veiculo

class VisitanteAdmin(admin.ModelAdmin):
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
  list_display = ('placa', 'horario_entrada')
  search_fields = ('placa', 'horario_entrada')
  list_filter = ('placa',)

admin.site.register(Visitante, VisitanteAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Veiculo, VeiculoAdmin)
admin.site.register(Usuario, UsuarioAdmin)