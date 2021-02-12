from django.contrib import admin
from django.contrib.auth.models import Group
from apps.confidencechronograms.models import (
    Cronograma, Tarefa, Cliente, Funcionario, Comentario, Empreiteira,
    Mao_de_Obra, Funcionario_da_Obra, Deposito, Material, Categoria,
    Orgao, Taxa)

admin.site.site_header = 'Admin Cronograma Confiável'


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'rua', 'fone')
    list_filter = ('nome',)
    search_fields = ['nome', 'fone']


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'rua', 'fone')
    list_filter = ('nome',)
    search_fields = ['nome', 'fone']


class CronogramaAdmin(admin.ModelAdmin):
    list_display = (
        'estrutura', 'cliente', 'tempo_total',
        'endereco', 'valor_total', 'date_added')
    list_filter = ('estrutura', 'cliente',)
    search_fields = ['cliente', 'estrutura']


class TarefaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'dt_inicial', 'dt_final', 'date_added')
    list_filter = ('dt_inicial',)
    search_fields = ['descricao', 'dt_inicial']


class Comentario_Admin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'assunto', 'date_added')
    search_fields = ['nome_cliente']


admin.site.register(Cronograma, CronogramaAdmin)
admin.site.register(Tarefa, TarefaAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Comentario, Comentario_Admin)

admin.site.register(Empreiteira)
admin.site.register(Mao_de_Obra)
admin.site.register(Funcionario_da_Obra)
admin.site.register(Deposito)
admin.site.register(Material)
admin.site.register(Categoria)
admin.site.register(Orgao)
admin.site.register(Taxa)
admin.site.unregister(Group)
