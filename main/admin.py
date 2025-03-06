from django.contrib import admin
from django.utils.timezone import now
from .models import Visitante , Setor , Visita
from veiculos.models import Veiculo

class VisitanteAdmin(admin.ModelAdmin):
  list_display = ('nome_completo','CPF','data_nascimento')  #as colunas que vao ser visiveis
  search_fields = ('nome_completo', 'CPF')        #os campos de pesquisa
  
class SetorAdmin (admin.ModelAdmin):
  list_display = ('nome', 'localização','disponibilidade')
  list_filter = ('nome','disponibilidade')

class VisitaAdmin (admin.ModelAdmin):
  list_display = ('visitante','setor','data_entrada','data_saida')
  list_filter = ('setor',)
  search_fields = ('pessoa__nome_completo',)

class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'responsavel', 'horario_entrada', 'horario_saida', 'status')
    list_filter = ('status', 'horario_entrada', 'horario_saida')
    search_fields = ('placa', 'responsavel')
    readonly_fields = ('horario_entrada', 'status')

'''class MovimentacaoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'horario_entrada', 'horario_saida')    
    list_filter = ('horario_entrada', 'horario_saida')
    search_fields = ('veiculo__placa', 'veiculo__responsavel')
    readonly_fields = ('horario_entrada',)
    def save_model(self, request, obj, form, change):
        if change:
            obj.horario_saida = now()
        super().save_model(request, obj, form, change)'''


admin.site.register(Visitante, VisitanteAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Visita, VisitaAdmin)
admin.site.register(Veiculo, VeiculoAdmin)