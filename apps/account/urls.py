from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'account'

urlpatterns = [
    path('logar_usuario', logar_usuario, name="logar_usuario"),
    path('deslogar_usuario', deslogar_usuario, name="deslogar_usuario"),
    path('alterar_senha/', alterar_senha, name='alterar_senha'),
    path('cadastrar_cliente', cadastrar_cliente, name="cadastrar_cliente"),
    path('cadastrar_funcionario', cadastrar_funcionario, name="cadastrar_funcionario"),
    path('cadastro/continue_cad_cliente', continue_cad_cliente, name="continue_cad_cliente"),
    path('continue_cad_funcionario', continue_cad_funcionario, name="continue_cad_funcionario"),
    path('cadastro/submit',  submit_continue_cad_cliente),
    path('submit', submit_continue_cad_funcionario),
]