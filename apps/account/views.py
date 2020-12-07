from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm)
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash)
from django.contrib.auth.models import User

from apps.confidencechronograms.models import Cliente, Funcionario
# com o forms vou conseguir resolver para incluir o usuario_cli e usuario_fun
from .forms import ClienteForm, FuncionarioForm


# Cadastro de cliente
def cadastrar_cliente(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('account:continue_cad_cliente')
    else:
        form_usuario = UserCreationForm()
    return render(
        request, 'cadastro_cliente.html', {'form_usuario': form_usuario})


# mostra continue cadastro cliente
@login_required(login_url="/login/")
def continue_cad_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            # 'nome', 'rua', 'razao_social', 'tipo_pessoa', 'cpf', 'rg',
            # 'cep', 'uf', 'email', 'fone', 'usuario_cli'
            nome = form.cleaned_data['nome']
            rua = form.cleaned_data['rua']
            cpf = form.cleaned_data['cpf']
            rg = form.cleaned_data['rg']
            cep = form.cleaned_data['cep']
            uf = form.cleaned_data['uf']
            email = form.cleaned_data['email']
            fone = form.cleaned_data['fone']
            usuario_cli = form.cleaned_data['usuario']
            novo = Cliente(
                nome=nome, rua=rua, cpf=cpf, rg=rg,
                cep=cep, uf=uf, email=email, fone=fone,
                usuario=usuario_cli
            )
            novo.save()
            return redirect("funcionario")
    else:
        form = ClienteForm()
    return render(request, "continue_cad_cliente.html", {"form": form})


@login_required(login_url="/login/")
def submit_continue_cad_cliente(request):
    if request.POST:
        nome = request.POST.get("nome")
        fone = request.POST.get("fone")
        rua = request.POST.get("rua")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")
        usuario_id = request.POST.get("usuario_id")
        Funcionario.objects.create(
            nome=nome,
            fone=fone,
            rua=rua,
            cidade=cidade,
            cep=cep,
            uf=uf,
            usuario_id=usuario_id
        )
    return redirect("/confidencechronogram/funcionario")


# cadastro de funcinário
def cadastrar_funcionario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('account:continue_cad_funcionario')
    else:
        form_usuario = UserCreationForm()
    return render(
        request, 'cadastro_funcionario.html', {'form_usuario': form_usuario})


# mostra continue cadastro funcionário
@login_required(login_url="/login/")
def continue_cad_funcionario(request):
    """ Continuação do Cadastro do Funcionário.
    """
    if request.method == "POST":
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("funcionario")
    else:
        form = FuncionarioForm()
    return render(request, "continue_cad_funcionario.html", {"form": form})
    # if request.method == "POST":
    #     form = FuncionarioForm(request.POST)
    #     if form.is_valid():
    #         #'nome', 'rua', 'cpf', 'rg', 'fone', 'bloqueado', 'usuario_fun'
    #         nome = form.cleaned_data['nome']
    #         rua = form.cleaned_data['rua']
    #         cpf = form.cleaned_data['cpf']
    #         rg = form.cleaned_data['rg']
    #         fone = form.cleaned_data['fone']
    #         bloqueado = form.cleaned_data['bloqueado']
    #         usuario_fun = form.cleaned_data['usuario_fun']
    #         novo = Funcionario(
    #             nome=nome, rua=rua, cpf=cpf,
    #             rg=rg, fone=fone, bloqueado=bloqueado,
    #             suario_fun=usuario_fun
    #         )
    #         novo.save()
    #         return redirect("funcionario")
    # else:
    #     form = FuncionarioForm()
    # return render(request, "continue_cad_funcionario.html", {"form": form})


@login_required(login_url="/login/")
def submit_continue_cad_funcionario(request):
    if request.POST:
        nome = request.POST.get("nome")
        fone = request.POST.get("fone")
        rua = request.POST.get("rua")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")
        usuario_id = request.POST.get("usuario_id")
        Funcionario.objects.create(
            nome=nome,
            fone=fone,
            rua=rua,
            cidade=cidade,
            cep=cep,
            uf=uf,
            usuario_id=usuario_id
        )
    return redirect("/confidencechronogram/funcionario")


def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})


@login_required(login_url='/logar_usuario')
def deslogar_usuario(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/login/')
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})
