from django.urls import path, re_path
from . import views
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # --------------redireciona para HOME---------------------------
    path('', views.home, name='home'),
    path('', RedirectView.as_view(url='/home/')),
    path('contato/', views.contact, name='contact'),
    # Lista (tarefas) do cronograma
    path('cronograma/', views.list_chronogram, name='list_chronogram'),
    # Lista (tarefas) do cronograma para Funcionario
    path('cronograma-funcionario/', views.list_chronogram_, name='list_chronogram_'),
    # path('', views.index)
    # Se encontrar url vazia(normal, local), redireciona para chronogram
    # path('', RedirectView.as_view(url='/chronogram/')),
    path('login/', views.login_user, name='login_user'),
    path('login/submit', views.submit_login, name='submit_login'),
    path('logout/', views.logout_user, name='logout_user'),

    path(
        "cronogramaconfiavel/", views.confidencechronogram,
        name="confidencechronogram"),
    # -----------cliente-----------------------------------------------------
    path("cronogramaconfiavel/cliente", views.dados_cliente, name="cliente"),
    path(
        "cronogramaconfiavel/lista/<int:id_cliente>/",
        views.json_lista_cliente),
    path("cronogramaconfiavel/clie/", views.cliente),
    path("cronogramaconfiavel/clie/submit", views.submit_cliente),
    # path(
    # "cronogramaconfiavel/clie/delete/<int:id_cliente>/",
    # views.delete_cliente, name="del_cliente"),

    # -------------funcionários--------------------------
    path(
        "cronogramaconfiavel/funcionario",
        views.dados_funcionario, name="funcionario"),
    path(
        "cronogramaconfiavel/lista/<int:id_funcionario>/",
        views.json_lista_funcionario),
    path("cronogramaconfiavel/func/", views.funcionario),
    path("cronogramaconfiavel/func/submit", views.submit_funcionario),
    # path(
    #    "cronogramaconfiavel/func/delete/<int:id_funcionario>/",
    #    views.delete_funcionario, name="del_funcionario"
    # ),
    ###########################################################################
    # Lista clientes
    # Clientes para verificação de funcionario
    path(
        "cronogramaconfiavel/clientes/",
        views.clientes_list, name="clientes_list"),
    path(
        "cronogramaconfiavel/clientes/alterar/<int:id>/",
        views.alterar_clientes, name="alterar_clientes"),
    path(
        "cronogramaconfiavel/clientes/excluir/<int:id>/",
        views.excluir_clientes, name="excluir_clientes"),
    # Cronograma - com busca
    path(
        "cronogramaconfiavel/chronogram/",
        views.chronogram_list, name="chronogram_list"),
    path(
        "cronogramaconfiavel/chronogram/newchronogram/",
        views.new_chronogram, name="new_chronogram"),
    path(
        "cronogramaconfiavel/chronogram/update/<int:id>/",
        views.update_chronogram, name="update_chronogram"),
    path(
        "cronogramaconfiavel/chronogram/delete/<int:id>/",
        views.delete_chronogram, name="delete_chronogram"),
    # Tarefa - com busca
    path("cronogramaconfiavel/task/", views.task_list, name="task_list"),
    path("cronogramaconfiavel/task/newtask/", views.new_task, name="new_task"),
    path(
        "cronogramaconfiavel/task/update/<int:id>/",
        views.update_task, name="update_task"),
    path(
        "cronogramaconfiavel/task/delete/<int:id>/",
        views.delete_task, name="delete_task"),
    # ------------Comentário-Cliente-------------------------------------------
    path(
        "cronogramaconfiavel/uploadcomentario/",
        views.uploadcomentario, name="uploadcomentario"),
    path(
        "cronogramaconfiavel/comentarios/",
        views.comentario_list, name="comentario_list"),
    path(
        "cronogramaconfiavel/comentarios/criarcomentarios/",
        views.criar_comentario, name="criar_comentario"),
    path(
        "cronogramaconfiavel/comentarios/update/<int:id>/",
        views.update_comentario, name="update_comentario"),
    path(
        "cronogramaconfiavel/comentarios/delete/<int:id>/",
        views.delete_comentario, name="delete_comentario"),
    # visualizar a lista de comentarios pelo funcionario também
    path(
        "cronogramaconfiavel/comentarios/funcionario",
        views.comentario_list_fun, name="comentario_list_fun"),
    # tarefas
    path(
        "cronogramaconfiavel/task/tasks",
        views.price_task, name="price_task"),
    # Valores de mãos de obra
    path(
        "cronogramaconfiavel/maos-de-obra/price-mao-de-obra",
        views.price_mao_de_obra, name="price_mao_de_obra"),
    # Valores de materiais
    path(
        "cronogramaconfiavel/materiais/price",
        views.price_material, name="price_material"),
    # Valores de taxas
    path(
        "cronogramaconfiavel/taxas/price",
        views.price_taxa, name="price_taxa"),

    # Email-views
    # path("cronogramaconfiavel/sendmail", views.e_mail, name="e_mail"),
    #################################
    # empreiteira
    path(
        "cronogramaconfiavel/empreiteira/",
        views.empreiteira_list, name="empreiteira_list"),
    path(
        "cronogramaconfiavel/empreiteira/nova-empreiteira/",
        views.nova_empreiteira, name="nova_empreiteira"),
    path(
        "cronogramaconfiavel/empreiteira/alterar/<int:id>/",
        views.alterar_empreiteira, name="alterar_empreiteira"),
    path(
        "cronogramaconfiavel/empreiteira/excluir/<int:id>/",
        views.excluir_empreiteira, name="excluir_empreiteira"),
    # Mão de Obra
    path(
        "cronogramaconfiavel/mao-de-obra/", views.mao_de_obra_list,
        name="mao_de_obra_list"),
    path(
        "cronogramaconfiavel/mao-de-obra/nova-mao-de-obra/",
        views.nova_mao_de_obra, name="nova_mao_de_obra"),
    path(
        "cronogramaconfiavel/mao-de-obra/alterar/<int:id>/",
        views.alterar_mao_de_obra, name="alterar_mao_de_obra"),
    path(
        "cronogramaconfiavel/mao-de-obra/excluir/<int:id>/",
        views.excluir_mao_de_obra, name="excluir_mao_de_obra"),
    # Funcionário da Obra
    path(
        "cronogramaconfiavel/funcionario-da-obra/",
        views.funcionario_da_obra_list, name="funcionario_da_obra_list"),
    path(
        "cronogramaconfiavel/funcionario-da-obra/novo-funcionario-da-obra/",
        views.novo_funcionario_da_obra, name="novo_funcionario_da_obra"),
    path(
        "cronogramaconfiavel/funcionario-da-obra/alterar/<int:id>/",
        views.alterar_funcionario_da_obra, name="alterar_funcionario_da_obra"),
    path(
        "cronogramaconfiavel/funcionario-da-obra/excluir/<int:id>/",
        views.excluir_funcionario_da_obra, name="excluir_funcionario_da_obra"),
    # deposito
    path(
        "cronogramaconfiavel/deposito/",
        views.deposito_list, name="deposito_list"),
    path(
        "cronogramaconfiavel/deposito/novo-deposito/",
        views.novo_deposito, name="novo_deposito"),
    path(
        "cronogramaconfiavel/deposito/alterar/<int:id>/",
        views.alterar_deposito, name="alterar_deposito"),
    path(
        "cronogramaconfiavel/deposito/excluir/<int:id>/",
        views.excluir_deposito, name="excluir_deposito"),

    # Categoria
    path(
        "cronogramaconfiavel/categoria/",
        views.categoria_list, name="categoria_list"),
    path(
        "cronogramaconfiavel/categoria/nova-categoria/",
        views.nova_categoria, name="nova_categoria"),
    path(
        "cronogramaconfiavel/categoria/alterar/<int:id>/",
        views.alterar_categoria, name="alterar_categoria"),
    path(
        "cronogramaconfiavel/categoria/excluir/<int:id>/",
        views.excluir_categoria, name="excluir_categoria"),
    # Material
    path(
        "cronogramaconfiavel/material/", views.material_list,
        name="material_list"),
    path(
        "cronogramaconfiavel/material/novo-material/",
        views.novo_material, name="novo_material"),
    path(
        "cronogramaconfiavel/material/alterar/<int:id>/",
        views.alterar_material, name="alterar_material"),
    path(
        "cronogramaconfiavel/material/excluir/<int:id>/",
        views.excluir_material, name="excluir_material"),
    # Orgão
    path(
        "cronogramaconfiavel/orgao/", views.orgao_list, name="orgao_list"),
    path(
        "cronogramaconfiavel/orgao/novo-orgao/",
        views.novo_orgao, name="novo_orgao"),
    path(
        "cronogramaconfiavel/orgao/alterar/<int:id>/",
        views.alterar_orgao, name="alterar_orgao"),
    path(
        "cronogramaconfiavel/orgao/excluir/<int:id>/",
        views.excluir_orgao, name="excluir_orgao"),
    # Taxa
    path(
        "cronogramaconfiavel/taxa/", views.taxa_list, name="taxa_list"),
    path(
        "cronogramaconfiavel/taxa/nova-taxa/",
        views.nova_taxa, name="nova_taxa"),
    path(
        "cronogramaconfiavel/taxa/alterar/<int:id>/",
        views.alterar_taxa, name="alterar_taxa"),
    path(
        "cronogramaconfiavel/taxa/excluir/<int:id>/",
        views.excluir_taxa, name="excluir_taxa"),

    # relatórios PDF
    re_path(r'^pdf/$', views.GeneratePDF.as_view(), name="relatorio"),
    re_path(r'^pdf-mao-de-obra/$', views.GeneratePDFMaodeObra.as_view(),
            name="relatorio_maos_de_obra"),
    re_path(r'^pdf-material/$', views.GeneratePDFMaterial.as_view(),
            name="relatorio_materiais"),
    re_path(r'^pdf-taxa/$', views.GeneratePDFTaxa.as_view(),
            name="relatorio_taxas"),

    # Para aparecer arquivos do diretório media quando DEBUG=False
    re_path(
        r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT}),
    re_path(
        r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
