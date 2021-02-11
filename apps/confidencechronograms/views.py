from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User
import json


# import pickle
from apps.confidencechronograms.models import (
    Tarefa, Cliente, Funcionario, Cronograma, Comentario, Empreiteira,
    Funcionario_da_Obra, Mao_de_Obra, Deposito,
    Material, Categoria, Orgao, Taxa
)

from apps.confidencechronograms.forms import (
    TarefaForm, CronogramaForm, ComentarioForm, EmpreiteiraForm,
    Funcionario_da_ObraForm, Mao_de_ObraForm,
    OrgaoForm, TaxaForm, DepositoForm, MaterialForm,
    CategoriaForm, ClientesForm
)

from django.http import HttpResponse
from django.views.generic import View
# import datetime
from apps.confidencechronograms.utils import render_to_pdf
# from confidencechronogram import settings
# from django.core.mail import send_mail


def home(request):
    # return HttpResponse('Hello World!')
    # Usando render
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/cronogramaconfiavel/')
        messages.error(request, "Usuário ou senha inválida.")

    return redirect('/login/')


# enviar direto para user (funcionario/cliente)
@login_required(login_url="/login/")
def confidencechronogram(request):
    """ Verifica se é funcionario ou cliente."""
    usuario = request.user
    # select * from Funcionario where usuario_fun = usuario;
    funcionario = Funcionario.objects.filter(usuario=usuario)
    cliente = Cliente.objects.filter(usuario=usuario)

    if funcionario:
        return redirect("funcionario")
    elif cliente:
        return redirect("cliente")
    else:
        return HttpResponse("<h1>Contate um Administrador!</h1>")


# lista as tarefas do chronograma para o FUNCIONARIO
@login_required(login_url='/login/')
def list_chronogram_(request):
    """ retorna o cronograma com às tarefas (javascript)
    Mostrar o caminho crítico das atividades do cronograma: Atividades
    que não podem atrasar - As atividades ja vão estar no limite.
    Mostrar a porcentagem da conclusão das atividades para o cliente ter
    uma visão. javascript? Mostrar a porcentagem do valor investido conforme
    o valor total do models Chronogram.
    """
    usuario = request.user
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)

        # Criar usuario_admin em cronograma, tarefa ..
        # admin = Cliente.objects.get(usuario_admin=usuario)

        # filter mostra como está a saida em __str__
        # do models da classe
        # cronograma = Cronograma.objects.filter(client=cliente)
        # get mostra os atributos do objeto
        # e assim pode-se colocar qual atributo -"nome.atributo"

        # Se tiver mais de um funcionario por cronograma da erro.
        cronograma = Cronograma.objects.get(funcionario=funcionario)
        # print(cronograma)

    except Exception:
        # raise Http404()
        return HttpResponse(
            'Verifique o seu usuario Funcionario em CRONOGRAMAS.')

    if funcionario:
        # print(cronograma.id)
        # c = Cronograma.objects.first()
        # c = request.user.chronogram_set.get()

        tasks = [t.to_dict() for t in Tarefa.objects.filter(
            cronograma=cronograma.id)]

        context = {
            "tasks": json.dumps(tasks), "funcionario": funcionario,
            'cronograma': cronograma
        }

    elif not cliente:
        messages.info(request, 'Usuário diferente, contate um administrados!')
        return redirect('/login/')

    else:
        raise Http404()

    return render(request, "chronogram_funcionario.html", context)


# lista as tarefas do chronograma para o cliente
@login_required(login_url='/login/')
def list_chronogram(request):
    """ retorna o cronograma com às tarefas (javascript)
    Mostrar o caminho crítico das atividades do cronograma: Atividades
    que não podem atrasar - As atividades ja vão estar no limite.
    Mostrar a porcentagem da conclusão das atividades para o cliente ter
    uma visão. javascript? Mostrar a porcentagem do valor investido conforme
    o valor total do models Chronogram.
    """
    usuario = request.user
    try:
        cliente = Cliente.objects.get(usuario=usuario)
        # Criar usuario_admin em cronograma, tarefa ..
        # admin = Cliente.objects.get(usuario_admin=usuario)

        # filter mostra como está a saida em __str__
        # do models da classe
        # cronograma = Cronograma.objects.filter(client=cliente)
        # get mostra os atributos do objeto
        # e assim pode-se colocar qual atributo -"nome.atributo"
        cronograma = Cronograma.objects.get(cliente=cliente)

    except Exception:
        raise Http404()

    if cliente:
        # print(cronograma.id)
        # c = Cronograma.objects.first()
        # c = request.user.chronogram_set.get()

        tasks = [t.to_dict() for t in Tarefa.objects.filter(
            cronograma=cronograma.id)]

        context = {
            "tasks": json.dumps(tasks), "cliente": cliente,
            'cronograma': cronograma
        }

    elif not cliente:
        messages.info(request, 'Usuário diferente, contate um administrados!')
        return redirect('/login/')

    else:
        raise Http404()

    return render(request, "chronogram.html", context)

    # antigo:
    # tasks = [
    #     {
    #         "id": "1",
    #         "name": "Instalações preliminares de água e energia",
    #         "start": "2020-02-19",
    #         "end": "2020-02-21",
    #         "progress": "100",
    #         #"dependencies": "",
    #         "custom_class": "bar-milestone" # optional
    #     },
    #     {
    #         "id": "2",
    #         "name": "Fechamento da Construção",
    #         "start": "2020-02-22",
    #         "end": "2020-02-27",
    #         "progress": "20",
    #         "dependencies": "1",
    #         "custom_class": "bar-milestone" # optional
    #     },
    #     {
    #         "id": "3",
    #         "name": "Gabaríto da Obra",
    #         "start": "2020-02-24",
    #         "end": "2020-03-20",
    #         "progress": "20",
    #         "dependencies": "2",
    #         "custom_class": "bar-milestone" # optional
    #     },
    # ]
#
# -------Cliente--------------------------
# Cliente vai ver seus dados e pode editar


@login_required(login_url="/login/")
def dados_cliente(request):
    """ Mostra dados do cliente."""
    usuario = request.user
    try:
        # Mesmo objeto em html
        cliente = Cliente.objects.filter(usuario=usuario)
        # cliente = Cliente.objects.all()
    except Exception:
        raise Http404()
    if cliente:
        # variáveis usadas no html:
        dados = {"cliente": cliente}
    else:
        raise Http404()

    return render(request, "confidence-cliente.html", dados)


@login_required(login_url="/login/")
def cliente(request):
    dados = {}
    # pegar usuario solicitando
    usuario = request.user
    id_cliente = request.GET.get("id")
    if id_cliente:
        cliente = Cliente.objects.get(id=id_cliente)
        # se o mesmo cliente.usuario_cliid igual ao usuario
        # solicitando para restringir qualquer user ver os dados com o id
        if cliente.usuario == usuario:
            dados["cliente"] = Cliente.objects.get(id=id_cliente)
    return render(request, "cliente.html", dados)


# editar cliente
@login_required(login_url="/login/")
def submit_cliente(request):

    if request.POST:
        nome = request.POST.get("nome")
        fone = request.POST.get("fone")
        email = request.POST.get("email")
        rua = request.POST.get("rua")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")

        usuario = request.user
        id_cliente = request.POST.get("id_cliente")
        if id_cliente:
            cliente = Cliente.objects.get(id=id_cliente)
            if cliente.usuario == usuario:
                cliente.nome = nome
                cliente.fone = fone
                cliente.email = email
                cliente.rua = rua
                cliente.cidade = cidade
                cliente.cep = cep
                cliente.uf = uf
                cliente.save()

    return redirect("cliente")


@login_required(login_url="/login/")
def delete_cliente(request, id_cliente):
    usuario_cli = request.user
    try:
        cliente = Cliente.objects.get(id=id_cliente)
    except Exception:
        raise Http404()
    if usuario_cli == cliente.usuario:
        cliente.delete()
    else:
        raise Http404()
    return redirect("confidencechronogram")


# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decoretor
# @login_required(login_url='/login/')
def json_lista_cliente(request, id_usuario):
    # request.user
    usuario_cli = User.objects.get(id=id_usuario)
    cliente = Cliente.objects.filter(usuario=usuario_cli).values(
        "id", "nome"
    )
    # safe=False porque nao é dicionário.
    return JsonResponse(list(cliente), safe=False)


# PARA ACESSAR SOMENTE DA TABELA CORRESPONDENTE COM SOMENTE SEUS DADOS
# (hacker pode ver com ids)

# FUNCIONÁRIOS
# Mudado nome de lista_funcionarios para dados_funcionario
@login_required(login_url="/login/")
def dados_funcionario(request):
    """ Lista dados do funcionário."""
    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.filter(usuario=usuario_fun)

    except Exception:
        raise Http404()

    if funcionario:
        # variáveis usadas no html:
        # Mudando variáveis e rotas...
        dados = {"funcionario": funcionario}

    else:
        raise Http404()

    return render(request, "confidence-funcionario.html", dados)


@login_required(login_url="/login/")
def funcionario(request):
    dados = {}
    # pegar usuário solicitando
    usuario = request.user
    id_funcionario = request.GET.get("id")
    if id_funcionario:
        funcionario = Funcionario.objects.get(id=id_funcionario)
        # se o mesmo funcionario.usuario id igual ao usuario
        # solicitando para restringir qualquer user ver os dados com o id
        if funcionario.usuario == usuario:
            dados["funcionario"] = Funcionario.objects.get(id=id_funcionario)

    return render(request, "funcionario.html", dados)


# edita funcionario
@login_required(login_url="/login/")
def submit_funcionario(request):
    if request.POST:
        nome = request.POST.get("nome")
        fone = request.POST.get("fone")
        email = request.POST.get("email")
        rua = request.POST.get("rua")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")

        usuario_fun = request.user
        id_funcionario = request.POST.get("id_funcionario")
        if id_funcionario:
            funcionario = Funcionario.objects.get(id=id_funcionario)
            if funcionario.usuario == usuario_fun:
                funcionario.nome = nome
                funcionario.fone = fone
                funcionario.email = email
                funcionario.rua = rua
                funcionario.cidade = cidade
                funcionario.cep = cep
                funcionario.uf = uf

                funcionario.save()
        # Evento.objects.filter(id=id_funcionario).update(nome=nome,
        # endereco=endereco,fone1=fone1)

    return redirect("funcionario")


# REDIRECIONAR CORRETAMENTE
@login_required(login_url="/login/")
def delete_funcionario(request, id_funcionario):
    # Fazer verificações como esta nas outras funções.
    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.get(id=id_funcionario)
    except Exception:
        raise Http404()
    if usuario_fun == funcionario.usuario:
        funcionario.delete()
    else:
        raise Http404()
    return redirect("confidencechronogram")


# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decoretor
@login_required(login_url="/login/")
def json_lista_funcionario(request, id_usuario_fun):
    # request.user
    usuario_fun = User.objects.get(id=id_usuario_fun)
    funcionario = Funcionario.objects.filter(usuario=usuario_fun).values(
        "id", "nome"
    )
    # safe=False porque nao é dicionário.
    return JsonResponse(list(funcionario), safe=False)


# Lista clientes
@login_required(login_url="/login/")
def clientes_list(request):
    """ Lista clientes para Funcionários"""
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            clientes = Cliente.objects.all()
            # __icontains sem case sensitive
            clientes = clientes.filter(nome__icontains=termo_pesquisa)
        else:
            clientes_list = Cliente.objects.all().order_by('-date_added')
            paginator = Paginator(clientes_list, 7)
            page = request.GET.get('page')
            clientes = paginator.get_page(page)
        dados = {"funcionario": funcionario, "clientes": clientes}
    else:
        raise Http404()

    return render(request, "clientes_list.html", dados)


# alterar clientes
@login_required(login_url="/login/")
def alterar_clientes(request, id):
    """ Atualiza cliente."""
    cliente = Cliente.objects.get(id=id)
    form = ClientesForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect("clientes_list")
    return render(
        request, "alterar_clientes.html", {
            "form": form, 'cliente': cliente})


@login_required(login_url="/login/")
def excluir_clientes(request, id):
    if request.method == "POST":
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
    return redirect("clientes_list")


#########################################
# Criar Cronograma, Listar Cronogramas, Deletar-não.
@login_required(login_url="/login/")
def chronogram_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)

    except Exception:
        raise Http404()

    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            cronogramas = Cronograma.objects.all()
            # __icontains sem case sensitive
            cronogramas = cronogramas.filter(
                estrutura__icontains=termo_pesquisa)
        else:
            cronogramas_list = Cronograma.objects.all().order_by('-date_added')
            paginator = Paginator(cronogramas_list, 7)
            page = request.GET.get('page')
            cronogramas = paginator.get_page(page)
        dados = {"cronogramas": cronogramas}
    else:
        raise Http404()

    return render(request, "chronogram_list.html", dados)


@login_required(login_url="/login/")
def new_chronogram(request):
    """ Cria formulário do cronograma e envia objeto cliente."""
    # funcionario = request.user
    # user_funcionario = Funcionario.objects.get(usuario=funcionario)
    if request.method == "POST":
        form = CronogramaForm(request.POST)
        if form.is_valid():
            # funcionário que criou vinculado no cronograma - moficicado
            # novo = Cronograma(
            #     funcionario=user_funcionario, **form.cleaned_data)
            novo = Cronograma(**form.cleaned_data)
            novo.save()

            return redirect("chronogram_list")
    else:
        form = CronogramaForm()
    return render(request, "criar_cronograma.html", {"form": form})


# Update Chronogram
@login_required(login_url="/login/")
def update_chronogram(request, id):
    """ Atualiza Cronograma."""
    chronogram = Cronograma.objects.get(id=id)
    form = CronogramaForm(request.POST or None, instance=chronogram)
    if form.is_valid():
        form.save()
        return redirect("chronogram_list")
    return render(
        request, "chronogram_update.html", {
            "form": form, 'chronogram': chronogram})


@login_required(login_url="/login/")
def delete_chronogram(request, id):
    if request.method == "POST":
        chronogram = Cronograma.objects.get(id=id)
        chronogram.delete()
    return redirect("chronogram_list")


###############################################################
# Criar Tarefas, Listar tarefas, Deletar-.---------------------
@login_required(login_url="/login/")
def task_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
        # filter mostra como está a saida em __str__
        # do models da classe
        # cronograma = Cronograma.objects.filter(funcionario=funcionario)
        # get mostra od atributos do objeto
        # e assim pode-se colocar qual atributo

    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            tasks = Tarefa.objects.all()
            # __icontains sem case sensitive
            tasks = tasks.filter(nome__icontains=termo_pesquisa)
        else:
            tasks_list = Tarefa.objects.all().order_by('-cronograma')
            paginator = Paginator(tasks_list, 7)
            page = request.GET.get('page')
            tasks = paginator.get_page(page)

            # tasks = Tarefa.objects.order_by("-date_added").all()

            # Não encontra tabela confidence_chronograms_tarefa
            # tarefa = tasks.extra(where=[
            # "EXISTS(SELECT 1 FROM confidence_chronograms_tarefa
            # WHERE funcionario=funcionario)"
            # ])

        dados = {
            "tasks": tasks
        }
    else:
        raise Http404()
    return render(request, "task_list.html", dados)


@login_required(login_url="/login/")
def new_task(request):
    """ Cria formulário de tarefa."""
    funcionario = request.user
    if funcionario:
        if request.method == "POST":
            form = TarefaForm(request.POST)
            if form.is_valid():
                tf = form.save()
                tf.save()
                return redirect("task_list")
        else:
            form = TarefaForm()
    return render(request, "criar_tarefa.html", {"form": form})


# Update task
@login_required(login_url="/login/")
def update_task(request, id):
    """ Atualiza tarefa."""
    task = Tarefa.objects.get(id=id)
    form = TarefaForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect("task_list")
    return render(request, "task_update.html", {"form": form, 'task': task})


@login_required(login_url="/login/")
def delete_task(request, id):
    if request.method == "POST":
        task = Tarefa.objects.get(id=id)
        task.delete()
    return redirect("task_list")


# Comentário do Cliente
# FUNÇÕES DE UPLOAD
@login_required(login_url="/login/")
def uploadcomentario(request):
    """Essa função carrega o arquivo do cliente
       É chamada pelo cliente(específico) enviar o
       arquivo/comentario para o funcionário"""
    context = {}

    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context["url"] = fs.url(name)
    return render(request, "uploadcomentario.html", context)


# Lista comentario - clientes
@login_required(login_url="/login/")
def comentario_list(request):
    """ Lista comentario do Cliente """
    usuario = request.user
    dados = {}
    try:
        cliente = Cliente.objects.get(usuario=usuario)
        # funcionario = Funcionario.objects.all()
    except Exception:
        raise Http404()

    if cliente:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            comentarios = Comentario.objects.filter(cliente=cliente)
            # __icontains sem case sensitive
            comentarios = comentarios.filter(assunto__icontains=termo_pesquisa)
        else:
            # OK esta pegando so os comentarios referentes ao cliente que criou
            # ***É preciso atribuir automaticamente o cliente_ch***
            comentarios = Comentario.objects.filter(cliente=cliente)
            # print(cliente.nome)
        # se precisar dos dados do cliente
        dados = {"cliente": cliente, "comentarios": comentarios}
    else:
        raise Http404()

    return render(request, "comentario_list.html", dados)


# Lista comentario - funcionários
@login_required(login_url="/login/")
def comentario_list_fun(request):
    """ Lista comentario Para Funcionário Específico. """
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            comentarios = Comentario.objects.filter(funcionario=funcionario)
            # __icontains sem case sensitive
            comentarios = comentarios.filter(assunto__icontains=termo_pesquisa)
        else:
            comentarios_list = Comentario.objects.filter(
                funcionario=funcionario)
            paginator = Paginator(comentarios_list, 2)
            page = request.GET.get('page')
            comentarios = paginator.get_page(page)
        dados = {"funcionario": funcionario, "comentarios": comentarios}
    else:
        raise Http404()

    return render(request, "comentario_list_fun.html", dados)


@login_required(login_url="/login/")
def criar_comentario(request):
    """ Cria formulário do comentario e envia objeto cliente para pegar id.
    """
    usuario = request.user
    # é preciso pegar usuario com 'get' para atribuir em cliente de comentario.
    usuario_cli = Cliente.objects.get(usuario=usuario)
    # print(usuario_cli)
    if request.method == "POST":
        form = ComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            novo = Comentario(cliente=usuario_cli, **form.cleaned_data)
            novo.save()
            return redirect("comentario_list")
    else:
        form = ComentarioForm()
    return render(request, "criar_comentario.html", {"form": form})


# Update Comentário
@login_required(login_url="/login/")
def update_comentario(request, id):
    """ Atualiza Comentário."""
    comentario = Comentario.objects.get(id=id)
    form = ComentarioForm(request.POST or None, instance=comentario)
    if form.is_valid():
        form.save()
        return redirect("comentario_list")
    return render(
        request, "comentario_update.html", {
            "form": form, 'comentario': comentario})


@login_required(login_url="/login/")
def delete_comentario(request, id):
    if request.method == "POST":
        comentario = Comentario.objects.get(id=id)
        comentario.delete()
    return redirect("comentario_list")


# Valores das tarefas - em cliente
@login_required(login_url="/login/")
def price_task(request):
    """ Lista de nomes, datas e VALORES das tarefas"""
    context = {}
    cliente = request.user
    try:
        cliente = Cliente.objects.get(usuario=cliente)
        # filter mostra como está a saida em __str__
        # do models da classe
        # cronograma = Cronograma.objects.filter(client=cliente)
        # get mostra os atributos do objeto
        # e assim pope-se colocar qual atributo
        cronograma = Cronograma.objects.get(cliente=cliente)
    except Exception:
        raise Http404()
    if cliente:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        termo_pesquisa_mdo = request.GET.get('pesquisa_mdo', None)
        termo_pesquisa_mtrl = request.GET.get('pesquisa_mtrl', None)
        termo_pesquisa_tx = request.GET.get('pesquisa_tx', None)

        tasks = Tarefa.objects.all()
        mao_de_obra = Mao_de_Obra.objects.all()
        material = Material.objects.all()
        taxa = Taxa.objects.all()
        smdo = 0
        smtrl = 0
        stx = 0
        sttl = 0
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            # __icontains sem case sensitive
            tasks = tasks.filter(nome__icontains=termo_pesquisa)
        elif termo_pesquisa_mdo:
            # __icontains sem case sensitive
            mao_de_obra = mao_de_obra.filter(
                nome__icontains=termo_pesquisa_mdo)
        elif termo_pesquisa_mtrl:
            # __icontains sem case sensitive
            material = material.filter(nome__icontains=termo_pesquisa_mtrl)
        elif termo_pesquisa_tx:
            # __icontains sem case sensitive
            taxa = taxa.filter(nome__icontains=termo_pesquisa_tx)
        else:
            # OK esta pegando so os comentarios referentes ao cliente que criou
            # ***É preciso atribuir automaticamente o cliente
            # print(cronograma.id)
            # qs = Tarefa.objects.values_list()
            # print(qs)
            # # reloaded_qs = Tarefa.objects.all()
            # tasks.query = pickle.loads(pickle.dumps(qs.query))
            # # reloaded_qs = Tarefa.objects.all()
            # # reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            # print(tasks)

            # estou pegando todas desse cronograma
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            mao_de_obra = Mao_de_Obra.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS MÃOS DE OBRA DA CONSTRUÇÃO INTEIRA
            smdo = 0
            for tmdo in mao_de_obra:
                smdo += tmdo.valor_unitario * tmdo.quantidade

            material = Material.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DOS MATERIAIS DA CONSTRUÇÃO INTEIRA
            smtrl = 0
            for mtrl in material:
                smtrl += mtrl.valor_unitario * mtrl.quantidade

            taxa = Taxa.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS TAXAS DA CONSTRUÇÃO INTEIRA
            stx = 0
            for tx in taxa:
                stx += tx.valor_unitario * tx.quantidade

            # VALOR TOTAL DA CONSTRUÇÃO INTEIRA
            sttl = smdo + smtrl + stx

        context = {
            'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
            'mao_de_obra': mao_de_obra, 'material': material, 'taxa': taxa,
            'smdo': smdo, 'smtrl': smtrl, 'stx': stx, 'sttl': sttl
        }
    else:
        raise Http404()
    return render(request, "valores_list.html", context)


# Valores das maos de obra - em cliente
@login_required(login_url="/login/")
def price_mao_de_obra(request):
    """ Lista de nomes, datas e VALORES das maos de obra"""
    context = {}
    cliente = request.user
    try:
        cliente = Cliente.objects.get(usuario=cliente)
        # filter mostra como está a saida em __str__
        # do models da classe
        # cronograma = Cronograma.objects.filter(client=cliente)
        # get mostra os atributos do objeto
        # e assim pope-se colocar qual atributo
        cronograma = Cronograma.objects.get(cliente=cliente)
    except Exception:
        raise Http404()
    if cliente:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        tasks = Tarefa.objects.all()
        mao_de_obra = Mao_de_Obra.objects.all()
        smdo = 0
        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            # __icontains sem case sensitive
            mao_de_obra = mao_de_obra.filter(
                nome__icontains=termo_pesquisa)
        else:
            # OK esta pegando so os comentarios referentes ao cliente que criou
            # ***É preciso atribuir automaticamente o cliente
            # print(cronograma.id)
            # qs = Tarefa.objects.values_list()
            # print(qs)
            # # reloaded_qs = Tarefa.objects.all()
            # tasks.query = pickle.loads(pickle.dumps(qs.query))
            # reloaded_qs = Tarefa.objects.all()
            # reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            # print(tasks)

            # estou pegando todas desse cronograma
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            mao_de_obra = Mao_de_Obra.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS MÃOS DE OBRA DA CONSTRUÇÃO INTEIRA
            smdo = 0
            for tmdo in mao_de_obra:
                smdo += tmdo.valor_unitario * tmdo.quantidade

        context = {
            'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
            'mao_de_obra': mao_de_obra, 'smdo': smdo
        }
    else:
        raise Http404()
    return render(request, "valores_list_mao_de_obra.html", context)


# Valores das tarefas - em cliente
@login_required(login_url="/login/")
def price_material(request):
    """ Lista de nomes, datas e VALORES das tarefas"""
    context = {}
    cliente = request.user
    try:
        cliente = Cliente.objects.get(usuario=cliente)
        # filter mostra como está a saida em __str__
        # do models da classe
        # cronograma = Cronograma.objects.filter(client=cliente)
        # get mostra os atributos do objeto
        # e assim pope-se colocar qual atributo
        cronograma = Cronograma.objects.get(cliente=cliente)
    except Exception:
        raise Http404()
    if cliente:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        tasks = Tarefa.objects.all()

        material = Material.objects.all()
        smtrl = 0

        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            # __icontains sem case sensitive
            material = material.filter(nome__icontains=termo_pesquisa)
        else:
            # OK esta pegando so os comentarios referentes ao cliente que criou
            # ***É preciso atribuir automaticamente o cliente
            # print(cronograma.id)
            # qs = Tarefa.objects.values_list()
            # print(qs)
            # # reloaded_qs = Tarefa.objects.all()
            # tasks.query = pickle.loads(pickle.dumps(qs.query))
            # # reloaded_qs = Tarefa.objects.all()
            # # reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            # print(tasks)

            # estou pegando todas desse cronograma
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            material = Material.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DOS MATERIAIS DA CONSTRUÇÃO INTEIRA
            smtrl = 0
            for mtrl in material:
                smtrl += mtrl.valor_unitario * mtrl.quantidade

        context = {
            'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
            'material': material, 'smtrl': smtrl
        }
    else:
        raise Http404()
    return render(request, "valores_list_material.html", context)


# Valores das taxas - em cliente
@login_required(login_url="/login/")
def price_taxa(request):
    """ Lista de nomes, datas e VALORES das tarefas"""
    context = {}
    cliente = request.user
    try:
        cliente = Cliente.objects.get(usuario=cliente)
        # filter mostra como está a saida em __str__
        # do models da classe
        # cronograma = Cronograma.objects.filter(client=cliente)
        # get mostra os atributos do objeto
        # e assim pope-se colocar qual atributo
        cronograma = Cronograma.objects.get(cliente=cliente)
    except Exception:
        raise Http404()
    if cliente:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        tasks = Tarefa.objects.all()
        taxa = Taxa.objects.all()
        stx = 0

        # PESQUISAS DEVEM ESTAR DIRETO EM MODEL PESQUISANDO
        if termo_pesquisa:
            # __icontains sem case sensitive
            taxa = taxa.filter(nome__icontains=termo_pesquisa)
        else:
            # OK esta pegando so os comentarios referentes ao cliente que criou
            # ***É preciso atribuir automaticamente o cliente
            # print(cronograma.id)
            # qs = Tarefa.objects.values_list()
            # print(qs)
            # reloaded_qs = Tarefa.objects.all()Topografia do terrenoqs.query))
            # reloaded_qs = Tarefa.objects.all()
            # reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            # print(tasks)

            # estou pegando todas desse cronograma
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            taxa = Taxa.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS TAXAS DA CONSTRUÇÃO INTEIRA
            stx = 0
            for tx in taxa:
                stx += tx.valor_unitario * tx.quantidade

        context = {
            'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
            'taxa': taxa, 'stx': stx
        }
    else:
        raise Http404()
    return render(request, "valores_list_taxa.html", context)


# Gera pdf relatório tarefas
class GeneratePDF(View):
    """Gerar pdf de 'relatorio.html' para cliente."""
    def get(self, request, *args, **kwargs):
        context = {}
        cliente = request.user
        try:
            cliente = Cliente.objects.get(usuario=cliente)
            # filter mostra como está a saida em __str__
            # do models da classe
            # cronograma = Cronograma.objects.filter(client=cliente)
            # get mostra od atributos do objeto
            # e assim pope-se colocar qual atributo
            cronograma = Cronograma.objects.get(cliente=cliente)
        except Exception:
            raise Http404()
        if cliente:
            # pegar por tarefa para gerar valores dela
            # FAZER POR MY_FILTERS.PY
            # tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            # qs = Tarefa.objects.values_list()
            # print(qs)
            # # reloaded_qs = Tarefa.objects.all()
            # tasks.query = pickle.loads(pickle.dumps(qs.query))
            # # reloaded_qs = Tarefa.objects.all()
            # # reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            # print(tasks)

            # estou pegando todas desse cronograma
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            mao_de_obra = Mao_de_Obra.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS MÃOS DE OBRA DA CONSTRUÇÃO INTEIRA
            smdo = 0
            for tmdo in mao_de_obra:
                smdo += tmdo.valor_unitario * tmdo.quantidade

            material = Material.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DOS MATERIAIS DA CONSTRUÇÃO INTEIRA
            smtrl = 0
            for mtrl in material:
                smtrl += mtrl.valor_unitario * mtrl.quantidade

            taxa = Taxa.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS TAXAS DA CONSTRUÇÃO INTEIRA
            stx = 0
            for tx in taxa:
                stx += tx.valor_unitario * tx.quantidade

            # VALOR TOTAL DA CONSTRUÇÃO INTEIRA
            sttl = smdo + smtrl + stx

            context = {
                'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
                'mao_de_obra': mao_de_obra, 'material': material, 'taxa': taxa,
                'sttl': sttl
            }
            # data = {
            #     'today': datetime.date.today(),
            #     'amount': 39.99,
            #     'customer_name': 'Cooper Mann',
            #     'order_id': 1233434,
            # }
            pdf = render_to_pdf('relatorio.html', context)

        else:
            raise Http404()

        return HttpResponse(pdf, content_type='confidencechronograms/pdf')


# Gera pdf relatorio Mãos de Obra
class GeneratePDFMaodeObra(View):
    """Gerar pdf de 'relatorio_maos_de_obra.html' para cliente."""
    def get(self, request, *args, **kwargs):
        context = {}
        cliente = request.user
        try:
            cliente = Cliente.objects.get(usuario=cliente)
            cronograma = Cronograma.objects.get(cliente=cliente)
        except Exception:
            raise Http404()
        if cliente:
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)
            mao_de_obra = Mao_de_Obra.objects.filter(cronograma=cronograma.id)

            funcionarios = Mao_de_Obra.objects.filter(
                cronograma=cronograma.id).prefetch_related(
                'funcionarios_da_obra')
            lista = []
            for f in funcionarios:
                if len(f.funcionarios_da_obra.all()) > 0:
                    lista.append(str(f.funcionarios_da_obra.all()))
            lista2 = []
            for i in lista:
                # print(i)
                lista_frase = i.split()
                # print(lista_frase)
                remover_palavras = ['<QuerySet', '[<Funcionario_da_Obra:',
                                    '<Funcionario_da_Obra:']
                result = [
                    palavra for palavra in lista_frase if palavra not in (
                        remover_palavras)]
                result = [item.replace(">]>", "") for item in result]
                result = [item.replace(">", "") for item in result]
                # print(result)
                retorno = ' '.join(result)
                lista2.append(retorno)

            # lfun = l
            # i = 0
            # while i < len(lfun):
            #     j = i + 1
            #     while j < len(lfun):
            #         if lfun[j] == lfun[i]:
            #             del(lfun[j])
            #         else:
            #             j = j + 1
            #     i = i + 1
            # print(lfun)

            smdo = 0
            for tmdo in mao_de_obra:
                smdo += tmdo.valor_unitario * tmdo.quantidade
            material = Material.objects.filter(cronograma=cronograma.id)
            smtrl = 0
            for mtrl in material:
                smtrl += mtrl.valor_unitario * mtrl.quantidade

            taxa = Taxa.objects.filter(cronograma=cronograma.id)
            stx = 0
            for tx in taxa:
                stx += tx.valor_unitario * tx.quantidade
            sttl = smdo + smtrl + stx

            context = {
                'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
                'mao_de_obra': mao_de_obra, 'material': material, 'taxa': taxa,
                'smdo': smdo, 'sttl': sttl, 'lfun': lista2,
                'count': 0
            }
            pdf = render_to_pdf('relatorio_maos_de_obra.html', context)
        else:
            raise Http404()
        return HttpResponse(pdf, content_type='cronogramaconfiavel/pdf')


# Gera pdf relatorio Materiais
class GeneratePDFMaterial(View):
    """Gerar pdf de 'relatorio_materiais.html' para cliente."""
    def get(self, request, *args, **kwargs):
        context = {}
        cliente = request.user
        try:
            cliente = Cliente.objects.get(usuario=cliente)
            # filter mostra como está a saida em __str__
            # do models da classe
            # cronograma = Cronograma.objects.filter(client=cliente)
            # get mostra od atributos do objeto
            # e assim pope-se colocar qual atributo
            cronograma = Cronograma.objects.get(cliente=cliente)
        except Exception:
            raise Http404()
        if cliente:
            # pegar por tarefa para gerar valores dela
            # FAZER POR MY_FILTERS.PY
            # tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            # qs = Tarefa.objects.values_list()
            # print(qs)
            # # reloaded_qs = Tarefa.objects.all()
            # tasks.query = pickle.loads(pickle.dumps(qs.query))
            # # reloaded_qs = Tarefa.objects.all()
            # # reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            # print(tasks)

            # estou pegando todas desse cronograma
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            mao_de_obra = Mao_de_Obra.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS MÃOS DE OBRA DA CONSTRUÇÃO INTEIRA
            smdo = 0
            for tmdo in mao_de_obra:
                smdo += tmdo.valor_unitario * tmdo.quantidade

            material = Material.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DOS MATERIAIS DA CONSTRUÇÃO INTEIRA
            smtrl = 0
            for mtrl in material:
                smtrl += mtrl.valor_unitario * mtrl.quantidade

            taxa = Taxa.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS TAXAS DA CONSTRUÇÃO INTEIRA
            stx = 0
            for tx in taxa:
                stx += tx.valor_unitario * tx.quantidade

            # VALOR TOTAL DA CONSTRUÇÃO INTEIRA
            sttl = smdo + smtrl + stx

            context = {
                'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
                'mao_de_obra': mao_de_obra, 'material': material, 'taxa': taxa,
                'smtrl': smtrl, 'sttl': sttl
            }
            # data = {
            #     'today': datetime.date.today(),
            #     'amount': 39.99,
            #     'customer_name': 'Cooper Mann',
            #     'order_id': 1233434,
            # }
            pdf = render_to_pdf('relatorio_materiais.html', context)

        else:
            raise Http404()

        return HttpResponse(pdf, content_type='cronogramaconfiavel/pdf')


# Gera pdf relatorio Taxas
class GeneratePDFTaxa(View):
    """Gerar pdf de 'relatorio_taxas.html' para cliente."""
    def get(self, request, *args, **kwargs):
        context = {}
        cliente = request.user
        try:
            cliente = Cliente.objects.get(usuario=cliente)
            # filter mostra como está a saida em __str__
            # do models da classe
            # cronograma = Cronograma.objects.filter(client=cliente)
            # get mostra od atributos do objeto
            # e assim pope-se colocar qual atributo
            cronograma = Cronograma.objects.get(cliente=cliente)
        except Exception:
            raise Http404()
        if cliente:
            # pegar por tarefa para gerar valores dela
            # FAZER POR MY_FILTERS.PY
            # tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            # qs = Tarefa.objects.values_list()
            # print(qs)
            # # reloaded_qs = Tarefa.objects.all()
            # tasks.query = pickle.loads(pickle.dumps(qs.query))
            # # reloaded_qs = Tarefa.objects.all()
            # # reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            # print(tasks)

            # estou pegando todas desse cronograma
            tasks = Tarefa.objects.filter(cronograma=cronograma.id)

            mao_de_obra = Mao_de_Obra.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS MÃOS DE OBRA DA CONSTRUÇÃO INTEIRA
            smdo = 0
            for tmdo in mao_de_obra:
                smdo += tmdo.valor_unitario * tmdo.quantidade

            material = Material.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DOS MATERIAIS DA CONSTRUÇÃO INTEIRA
            smtrl = 0
            for mtrl in material:
                smtrl += mtrl.valor_unitario * mtrl.quantidade

            taxa = Taxa.objects.filter(cronograma=cronograma.id)
            # VALOR TOTAL DAS TAXAS DA CONSTRUÇÃO INTEIRA
            stx = 0
            for tx in taxa:
                stx += tx.valor_unitario * tx.quantidade

            # VALOR TOTAL DA CONSTRUÇÃO INTEIRA
            sttl = smdo + smtrl + stx

            context = {
                'tasks': tasks, 'cliente': cliente, 'cronograma': cronograma,
                'mao_de_obra': mao_de_obra, 'material': material, 'taxa': taxa,
                'stx': stx, 'sttl': sttl
            }
            # data = {
            #     'today': datetime.date.today(),
            #     'amount': 39.99,
            #     'customer_name': 'Cooper Mann',
            #     'order_id': 1233434,
            # }
            pdf = render_to_pdf('relatorio_taxas.html', context)

        else:
            raise Http404()

        return HttpResponse(pdf, content_type='cronogramaconfiavel/pdf')


# EMAIL- em models
# def e_mail(request):
#     subject = "Real programmer contact"
#     msg = "Congratulations for your success"
#     to = "cesarcosta.augustos@gmail.com"
#     res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
#     if(res == 1):
#         msg = "Mail Sent"
#     else:
#         msg = "Mail could not sent"
#     return HttpResponse(msg)


#############################################
# ---------Empreiteira.---------------------
@login_required(login_url="/login/")
def empreiteira_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            empreiteira = Empreiteira.objects.all()
            # __icontains sem case sensitive
            empreiteira = empreiteira.filter(nome__icontains=termo_pesquisa)
        else:
            empreiteira_list = (
                Empreiteira.objects.all().order_by('-date_added')
            )
            paginator = Paginator(empreiteira_list, 7)
            page = request.GET.get('page')
            empreiteira = paginator.get_page(page)
        dados = {"empreiteira": empreiteira}
    else:
        raise Http404()
    return render(request, "empreiteira_list.html", dados)


@login_required(login_url="/login/")
def nova_empreiteira(request):
    """ Cria formulário de empreiteira."""
    if request.method == "POST":
        form = EmpreiteiraForm(request.POST)
        if form.is_valid():
            emp = form.save()
            emp.save()
            return redirect("empreiteira_list")
    else:
        form = EmpreiteiraForm()
    return render(request, "criar_empreiteira.html", {"form": form})


@login_required(login_url="/login/")
def alterar_empreiteira(request, id):
    """ Atualiza empreiteira."""
    empreiteira = Empreiteira.objects.get(id=id)
    form = EmpreiteiraForm(request.POST or None, instance=empreiteira)
    if form.is_valid():
        form.save()
        return redirect("empreiteira_list")
    return render(
        request, "alterar_empreiteira.html", {
            "form": form, 'empreiteira': empreiteira})


@login_required(login_url="/login/")
def excluir_empreiteira(request, id):
    if request.method == "POST":
        empreiteira = Empreiteira.objects.get(id=id)
        empreiteira.delete()
    return redirect("empreiteira_list")


# ---------Mão de Obra.---------------------
@login_required(login_url="/login/")
def mao_de_obra_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        termo_pesquisa = request.GET.get('pesquisa', None)
        funcionarios = Funcionario_da_Obra.objects.all()
        mao_de_obra_list = Mao_de_Obra.objects.all().order_by('-date_added')
        paginator = Paginator(mao_de_obra_list, 7)
        page = request.GET.get('page')
        mao_de_obra = paginator.get_page(page)

        if termo_pesquisa:
            mao_de_obra = Mao_de_Obra.objects.all()
            # __icontains sem case sensitive
            mao_de_obra = mao_de_obra.filter(nome__icontains=termo_pesquisa)

        dados = {
            'mao_de_obra': mao_de_obra, 'funcionarios': funcionarios,
            # 'valor_total': json.dumps(vlt)
        }
    else:
        raise Http404()
    return render(request, "mao_de_obra_list.html", dados)


@login_required(login_url="/login/")
def nova_mao_de_obra(request):
    """ Cria formulário de Mão de Obra"""
    if request.method == "POST":
        form = Mao_de_ObraForm(request.POST)
        if form.is_valid():
            mdo = form.save()
            mdo.save()
            return redirect("mao_de_obra_list")
    else:
        form = Mao_de_ObraForm()
    return render(request, "criar_mao_de_obra.html", {"form": form})


@login_required(login_url="/login/")
def alterar_mao_de_obra(request, id):
    """ Atualiza mao_de_obra."""
    mao_de_obra = Mao_de_Obra.objects.get(id=id)
    form = Mao_de_ObraForm(request.POST or None, instance=mao_de_obra)
    if form.is_valid():
        form.save()
        return redirect("mao_de_obra_list")
    return render(
        request, "alterar_mao_de_obra.html", {
            "form": form, 'mao_de_obra': mao_de_obra})


@login_required(login_url="/login/")
def excluir_mao_de_obra(request, id):
    if request.method == "POST":
        mao_de_obra = Mao_de_Obra.objects.get(id=id)
        mao_de_obra.delete()
    return redirect("mao_de_obra_list")


# ---------Funcionario da Obra---------------------
@login_required(login_url="/login/")
def funcionario_da_obra_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            funcionario_da_obra = Funcionario_da_Obra.objects.all()
            # __icontains sem case sensitive
            funcionario_da_obra = funcionario_da_obra.filter(
                nome__icontains=termo_pesquisa)
        else:
            funcionario_list = (
                Funcionario_da_Obra.objects.all().order_by('-date_added')
            )
            paginator = Paginator(funcionario_list, 7)
            page = request.GET.get('page')
            funcionario_da_obra = paginator.get_page(page)
        dados = {"funcionario_da_obra": funcionario_da_obra}
    else:
        raise Http404()
    return render(request, "funcionario_da_obra_list.html", dados)


@login_required(login_url="/login/")
def novo_funcionario_da_obra(request):
    """ Cria formulário de Funcionario_da_Obra."""
    if request.method == "POST":
        form = Funcionario_da_ObraForm(request.POST)
        if form.is_valid():
            novo = Funcionario_da_Obra(**form.cleaned_data)
            novo.save()
            return redirect("funcionario_da_obra_list")
    else:
        form = Funcionario_da_ObraForm()
    return render(request, "criar_funcionario_da_obra.html", {"form": form})


# Altarar Funcionário da Obra
@login_required(login_url="/login/")
def alterar_funcionario_da_obra(request, id):
    """ Atualiza Funcionario_da_Obra."""
    funcionario_da_obra = Funcionario_da_Obra.objects.get(id=id)
    form = Funcionario_da_ObraForm(
        request.POST or None, instance=funcionario_da_obra)
    if form.is_valid():
        form.save()
        return redirect("funcionario_da_obra_list")
    return render(
        request, "alterar_funcionario_da_obra.html", {
            "form": form, 'funcionario_da_obra': funcionario_da_obra})


@login_required(login_url="/login/")
def excluir_funcionario_da_obra(request, id):
    if request.method == "POST":
        funcionario_da_obra = Funcionario_da_Obra.objects.get(id=id)
        funcionario_da_obra.delete()
    return redirect("funcionario_da_obra_list")


# ---------Deposito---------------------
@login_required(login_url="/login/")
def deposito_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            deposito = Deposito.objects.all()
            # __icontains sem case sensitive
            deposito = deposito.filter(nome__icontains=termo_pesquisa)
        else:
            deposito_list = Deposito.objects.all().order_by('-date_added')
            paginator = Paginator(deposito_list, 7)
            page = request.GET.get('page')
            deposito = paginator.get_page(page)
        dados = {"deposito": deposito}
    else:
        raise Http404()
    return render(request, "deposito_list.html", dados)


@login_required(login_url="/login/")
def novo_deposito(request):
    """ Cria formulário de deposito."""
    if request.method == "POST":
        form = DepositoForm(request.POST)
        if form.is_valid():
            novo = Deposito(**form.cleaned_data)
            novo.save()
            return redirect("deposito_list")
    else:
        form = DepositoForm()
    return render(request, "criar_deposito.html", {"form": form})


# alterar deposito
@login_required(login_url="/login/")
def alterar_deposito(request, id):
    """ Atualiza deposito."""
    deposito = Deposito.objects.get(id=id)
    form = DepositoForm(request.POST or None, instance=deposito)
    if form.is_valid():
        form.save()
        return redirect("deposito_list")
    return render(
        request, "alterar_deposito.html", {
            "form": form, 'deposito': deposito})


@login_required(login_url="/login/")
def excluir_deposito(request, id):
    if request.method == "POST":
        deposito = Deposito.objects.get(id=id)
        deposito.delete()
    return redirect("deposito_list")


# ---------Categoria do Material---------------------
@login_required(login_url="/login/")
def categoria_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            categoria = Categoria.objects.all()
            # __icontains sem case sensitive
            categoria = categoria.filter(nome__icontains=termo_pesquisa)
        else:
            categoria_list = Categoria.objects.all().order_by('-date_added')
            paginator = Paginator(categoria_list, 7)
            page = request.GET.get('page')
            categoria = paginator.get_page(page)
        dados = {"categoria": categoria}
    else:
        raise Http404()
    return render(request, "categoria_list.html", dados)


@login_required(login_url="/login/")
def nova_categoria(request):
    """ Cria formulário de categoria."""
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nova = Categoria(**form.cleaned_data)
            nova.save()
            return redirect("categoria_list")
    else:
        form = CategoriaForm()
    return render(request, "criar_categoria.html", {"form": form})


# alterar categoria
@login_required(login_url="/login/")
def alterar_categoria(request, id):
    """ Atualiza categoria."""
    categoria = Categoria.objects.get(id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect("categoria_list")
    return render(
        request, "alterar_categoria.html", {
            "form": form, 'categoria': categoria})


@login_required(login_url="/login/")
def excluir_categoria(request, id):
    if request.method == "POST":
        categoria = Categoria.objects.get(id=id)
        categoria.delete()
    return redirect("categoria_list")


# ---------Material---------------------
@login_required(login_url="/login/")
def material_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            material = Material.objects.all()
            # __icontains sem case sensitive
            material = material.filter(nome__icontains=termo_pesquisa)
        else:
            material_list = Material.objects.all().order_by('-date_added')
            paginator = Paginator(material_list, 7)
            page = request.GET.get('page')
            material = paginator.get_page(page)
        dados = {"material": material}
    else:
        raise Http404()
    return render(request, "material_list.html", dados)


@login_required(login_url="/login/")
def novo_material(request):
    """ Cria formulário de material."""
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            # mtrl = form.save()
            # mtrl.save()
            novo = Material(**form.cleaned_data)
            novo.save()
            return redirect("material_list")
    else:
        form = MaterialForm()
    return render(request, "criar_material.html", {"form": form})


# alterar material
@login_required(login_url="/login/")
def alterar_material(request, id):
    """ Atualiza material."""
    material = Material.objects.get(id=id)
    form = MaterialForm(request.POST or None, instance=material)
    if form.is_valid():
        form.save()
        return redirect("material_list")
    return render(
        request, "alterar_material.html", {
            "form": form, 'material': material})


@login_required(login_url="/login/")
def excluir_material(request, id):
    if request.method == "POST":
        material = Material.objects.get(id=id)
        material.delete()
    return redirect("material_list")


# ---------Orgão---------------------
@login_required(login_url="/login/")
def orgao_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        orgao_list = Orgao.objects.all().order_by('-date_added')
        paginator = Paginator(orgao_list, 4)
        page = request.GET.get('page')
        orgao = paginator.get_page(page)
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            orgao = Orgao.objects.all()
            # __icontains sem case sensitive
            orgao = orgao.filter(nome__icontains=termo_pesquisa)
        dados = {'orgao': orgao}
    else:
        raise Http404()
    return render(request, "orgao_list.html", dados)


@login_required(login_url="/login/")
def novo_orgao(request):
    """ Cria formulário de orgao."""
    if request.method == "POST":
        form = OrgaoForm(request.POST)
        if form.is_valid():
            novo = Orgao(**form.cleaned_data)
            novo.save()
            return redirect("orgao_list")
    else:
        form = OrgaoForm()
    return render(request, "criar_orgao.html", {"form": form})


# alterar orgao
@login_required(login_url="/login/")
def alterar_orgao(request, id):
    """ Atualiza orgao."""
    orgao = Orgao.objects.get(id=id)
    form = OrgaoForm(request.POST or None, instance=orgao)
    if form.is_valid():
        form.save()
        return redirect("orgao_list")
    return render(
        request, "alterar_orgao.html", {
            "form": form, 'orgao': orgao})


@login_required(login_url="/login/")
def excluir_orgao(request, id):
    if request.method == "POST":
        orgao = Orgao.objects.get(id=id)
        orgao.delete()
    return redirect("orgao_list")


# ---------Taxa---------------------
@login_required(login_url="/login/")
def taxa_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        # id pesquisa
        termo_pesquisa = request.GET.get('pesquisa', None)
        if termo_pesquisa:
            taxa = Taxa.objects.all()
            # __icontains sem case sensitive
            taxa = taxa.filter(nome__icontains=termo_pesquisa)
        else:
            taxa_list = Taxa.objects.all().order_by('-date_added')
            paginator = Paginator(taxa_list, 7)
            page = request.GET.get('page')
            taxa = paginator.get_page(page)
        dados = {"taxa": taxa}
    else:
        raise Http404()
    return render(request, "taxa_list.html", dados)


@login_required(login_url="/login/")
def nova_taxa(request):
    """ Cria formulário de taxa."""
    if request.method == "POST":
        form = TaxaForm(request.POST)
        if form.is_valid():
            # tx = form.save()
            # tx.save()
            novo = Taxa(**form.cleaned_data)
            novo.save()
            return redirect("taxa_list")
    else:
        form = TaxaForm()
    return render(request, "criar_taxa.html", {"form": form})


# alterar taxa
@login_required(login_url="/login/")
def alterar_taxa(request, id):
    """ Atualiza taxa."""
    taxa = Taxa.objects.get(id=id)
    form = TaxaForm(request.POST or None, instance=taxa)
    if form.is_valid():
        form.save()
        return redirect("taxa_list")
    return render(request, "alterar_taxa.html", {"form": form, 'taxa': taxa})


@login_required(login_url="/login/")
def excluir_taxa(request, id):
    if request.method == "POST":
        taxa = Taxa.objects.get(id=id)
        taxa.delete()
    return redirect("taxa_list")


@login_required(login_url="/login/")
def manual_cliente(request):
    """ Manual do cliente."""
    usuario = request.user
    try:
        cliente = Cliente.objects.filter(usuario=usuario)
    except Exception:
        raise Http404()
    if cliente:
        dados = {"cliente": cliente}
    else:
        raise Http404()

    return render(request, "manual_cliente.html", dados)


@login_required(login_url="/login/")
def manual_funcionario(request):
    """ Manual do cliente."""
    usuario = request.user
    try:
        funcionario = Funcionario.objects.filter(usuario=usuario)
    except Exception:
        raise Http404()
    if cliente:
        dados = {"funcionario": funcionario}
    else:
        raise Http404()

    return render(request, "manual_funcionario.html", dados)
