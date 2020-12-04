from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail, mail_admins
from django.template.loader import render_to_string
from confidencechronogram import settings


class GerenciaCronograma(models.Manager):
    # usar search()
    def search(self, query):
        # return self.get_queryset().all()
        # busca com logico E. por padrão vírgula ',' é E
        # return elf.get_queryset().filter(
        #	name__icontains=query, description__icontains=query)
        # busca OU
        return self.get_queryset().filter(
            models.Q(estrutura__icontains=query) | \
            models.Q(cliente__icontains=query))


class Funcionario(models.Model):
    """ Tabela para cadastro com as informações do funcionário."""
    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )
    nome = models.CharField(max_length=60)
    cpf = models.CharField(blank=True, null=True, max_length=11)
    rg = models.CharField(blank=True, null=True, max_length=9)
    dt_nascimento = models.DateTimeField(verbose_name = 'Data de Nascimento', blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False, null=False)
    nacionalidade = models.CharField(blank=True, null=True, max_length=30)
    naturalidade = models.CharField(blank=True, null=True, max_length=30)
    profissao = models.CharField(blank=True, null=True, max_length=100)
    estado_civil = models.CharField(verbose_name = 'Estado Civil', blank=True, null=True, max_length=15)
    rua = models.CharField(verbose_name = 'Rua', max_length=60)
    numero = models.CharField(verbose_name = 'Número', max_length=10)
    complemento = models.CharField(blank=True, null=True, max_length=30)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    cep = models.CharField(blank=True, null=True, max_length=9)
    uf = models.CharField(blank=True, null=True, max_length=2)
    email = models.EmailField("E-mail", max_length=60)
    fone = models.CharField(verbose_name = 'Telefone', max_length=16)
    dt_admissao = models.DateTimeField(verbose_name = 'Data de Admissão', blank=True, null=True)
    cargo = models.CharField(blank=True, null=True, max_length=20)
    salario = models.FloatField(blank=True, null=True)
    
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)
    #Usuário
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # classe Meta serve p modificar nomes para plural
    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        #ordenar
        ordering = ['nome']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome


class Cliente(models.Model):
    """ Tabela para cadastro com as informações do cliente."""
    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")
    )
    nome = models.CharField(max_length=60)
    cpf = models.CharField(blank=True, null=True, max_length=11)
    rg = models.CharField(blank=True, null=True, max_length=9)
    dt_nascimento = models.DateTimeField(verbose_name = 'Data de Nascimento', blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False, null=False)
    nacionalidade = models.CharField(blank=True, null=True, max_length=30)
    naturalidade = models.CharField(blank=True, null=True, max_length=30)
    profissao = models.CharField(blank=True, null=True, max_length=100)
    estado_civil = models.CharField(verbose_name = 'Estado Civil', blank=True, null=True, max_length=15)
    rua = models.CharField(verbose_name = 'Rua', max_length=60)
    numero = models.CharField(verbose_name = 'Número', max_length=10)
    complemento = models.CharField(blank=True, null=True, max_length=30)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    cep = models.CharField(blank=True, null=True, max_length=9)
    uf = models.CharField(blank=True, null=True, max_length=2)
    email = models.EmailField("E-mail", max_length=60)
    fone = models.CharField(verbose_name = 'Telefone', max_length=16)
    
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # classe Meta serve p modificar nomes para plural
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #ordenar
        ordering = ['nome']


    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome


# Criar Foreinkey de Cliente ou tabém com funcionário...
class Cronograma(models.Model):
    """ Um cronograma da obra em que o cliente e
       a Empreiteira vão poder visualizar."""
    
    estrutura = models.CharField(verbose_name = 'Tipo de Estrutura', max_length=200) # (verbose_name = ' Tipo de Estrutura')
    # cliente como chave estrangeira (E aparecer o cliente que já está cadastrado)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT)

    proprietario = models.CharField(verbose_name = 'Proprietário',max_length=80)
    endereco = models.CharField(verbose_name = 'Endereço', max_length=200)
    tempo_total = models.CharField(verbose_name = 'Tempo total estimado', max_length=30)
    valor_total = models.DecimalField(verbose_name = 'Valor total estimado', max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)
    

    # classe Meta serve para modificar nomes para plural
    class Meta:
        verbose_name = 'Cronograma'
        verbose_name_plural = 'Cronogramas'
        #ordenar
        ordering = ['date_added']
    
    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return f"Cliente:{self.cliente}, Construção:{self.estrutura} " \
               f"Endereço:{self.endereco}, Valor:{self.valor_total}" \
               f"Funcionário: {self.funcionario}"

    def get_date_added(self):

        return self.date_added.strftime('%d/%m/%Y %H h : %M min')


########################################
class Empreiteira(models.Model):
    """ Um funcionário trabalha em uma Empreiteira que pode ser tercerizada 
    (ou a própria construtora) """
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(blank=True, null=True, max_length=14)
    email = models.EmailField("E-mail", blank=True, null=True, max_length=60)
    fone = models.CharField(verbose_name = 'Telefone', max_length=16)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)
    #Mao de Obra
    maos_de_obra = models.ManyToManyField('Mao_de_Obra', through='Detalhe_Mao_de_Obra')

    # classe Meta serve para modificar nomes para plural
    class Meta:
        verbose_name = 'Empreiteira'
        verbose_name_plural = 'Empreiteiras'
        #ordenar
        ordering = ['date_added']

    def __str__(self):
        return self.nome


class Funcionario_da_Obra(models.Model):
    """ Funcionário da obra é de uma 'Empreiteira' que está trabalhando para executar determinadas tarefas. - Pedreiro, Carpinteiro... -  e tem 
    sua 'Mão de Obra' """
    
    SEXO_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("N", "Nenhuma das opções")

    )
    nome = models.CharField(max_length=60)
    cpf = models.CharField(blank=True, null=True, max_length=11)
    rg = models.CharField(blank=True, null=True, max_length=9)
    dt_nascimento = models.DateTimeField(verbose_name = 'Data de Nascimento', blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False, null=False)
    profissao = models.CharField(blank=True, null=True, max_length=60)
    nacionalidade = models.CharField(blank=True, null=True, max_length=30)
    naturalidade = models.CharField(blank=True, null=True, max_length=30)
    profissao = models.CharField(blank=True, null=True, max_length=100)
    estado_civil = models.CharField(verbose_name = 'Estado Civil', blank=True, null=True, max_length=15)
    rua = models.CharField(verbose_name = 'Rua', max_length=60)
    numero = models.CharField(verbose_name = 'Número', max_length=10)
    complemento = models.CharField(blank=True, null=True, max_length=30)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    cep = models.CharField(blank=True, null=True, max_length=9)
    uf = models.CharField(blank=True, null=True, max_length=2)
    email = models.EmailField("E-mail", max_length=60)
    fone = models.CharField(verbose_name = 'Telefone', max_length=16)
    
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)

    maos_de_obra = models.ManyToManyField('Mao_de_Obra', through='Detalhe_Funcionario_da_Obra')
    
    class Meta:
        verbose_name = 'Funcionário da Obra'
        verbose_name_plural = 'Funcionários das Obras'
        ordering = ['nome']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome


class Mao_de_Obra(models.Model):
    nome = models.CharField(max_length=200)
    #unidade - m2, m3, hora...
    unidade = models.CharField(max_length=20)
    #Empreiteira - Detalhe Mão de Obra
    empreiteiras = models.ManyToManyField('Empreiteira', through='Detalhe_Mao_de_Obra')
    #Funcionário da Obra - Detalhe Funcionário da Obra
    funcionarios_da_obra = models.ManyToManyField('Funcionario_da_Obra', through='Detalhe_Funcionario_da_Obra')
    class Meta:
        verbose_name = 'Mão de Obra'
        verbose_name_plural = 'Mãos de Obra'
        ordering = ['nome']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome


# Tabela associação de Mão de obra e Funcionario da obra
class Detalhe_Mao_de_Obra(models.Model):
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    #Mao de Obra
    mao_de_obra = models.ForeignKey(Mao_de_Obra, on_delete=models.PROTECT)
    # #Funcionario da Obra
    # funcionario_da_obra = models.ForeignKey(Funcionario_da_Obra, on_delete=models.PROTECT)

    #Empreiteira
    empreiteira = models.ForeignKey(Empreiteira, on_delete=models.PROTECT)

    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)

    class Meta:
        verbose_name = 'Detalhe Mão de Obra'
        verbose_name_plural = 'Detalhes Mãos de Obra'
        ordering = ['date_added']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.valor_unitario


# Tabela associação de Mão de obra e Funcionario da obra
class Detalhe_Funcionario_da_Obra(models.Model):
    
    #Funcionário da Obra
    funcionario_da_obra = models.ForeignKey(Funcionario_da_Obra, on_delete=models.PROTECT)

    #Mão de Obra
    mao_de_obra = models.ForeignKey(Mao_de_Obra, on_delete=models.PROTECT)

    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)

    class Meta:
        verbose_name = 'Detalhe Funcionário da Obra'
        verbose_name_plural = 'Detalhes Funcionários da Obra'
        ordering = ['date_added']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.funcionario_da_obra


class Deposito(models.Model):
    """ Deposito de Vários materiais """
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(blank=True, null=True, max_length=14)
    email = models.EmailField("E-mail", blank=True, null=True, max_length=60)
    fone = models.CharField(verbose_name = 'Telefone', max_length=16)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)
    #Material
    materiais = models.ManyToManyField('Material', through='Detalhe_Material')

    class Meta:
        verbose_name = 'Depósito'
        verbose_name_plural = 'Depósitos'
        ordering = ['date_added']

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=200)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['date_added']

    def __str__(self):
        return self.nome

# Como Produto
class Material(models.Model):
    """ Materiais de determinado 'Deposito' """
    nome = models.CharField(max_length=200)
    #unidade - m2, m3, hora...
    unidade = models.CharField(max_length=20)
    #Deposito
    depositos = models.ManyToManyField('Deposito', through='Detalhe_Material')
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'
        ordering = ['nome']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return f"Material:{self.nome}"


class Detalhe_Material(models.Model):

    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    #Material
    material = models.ForeignKey(
        Material, on_delete=models.PROTECT, blank=True)
    #Deposito
    deposito = models.ForeignKey(
        Deposito, on_delete=models.PROTECT, blank=True)
    #Categoia
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, blank=True)

    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)

    class Meta:
        verbose_name = 'Detalhe Mateial'
        verbose_name_plural = 'Detalhes Materiais'
        ordering = ['date_added']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.valor_unitario


class Orgao(models.Model):
    """ Orgão que emite várias taxas """

    nome = models.CharField(max_length=200)
    cnpj = models.CharField(blank=True, null=True, max_length=14)
    email = models.EmailField("E-mail", blank=True, null=True, max_length=60)
    fone = models.CharField(verbose_name = 'Telefone', max_length=16)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)
    #Taxa
    taxas = models.ManyToManyField('Taxa', through='Detalhe_Taxa')

    class Meta:
        verbose_name = 'Orgão'
        verbose_name_plural = 'Orgãos'
        ordering = ['date_added']

    def __str__(self):
        return self.nome

class Taxa(models.Model):
    """ Taxas de determinado 'Orgão' """
    nome = models.CharField(max_length=60)
    unidade = models.CharField(max_length=20)
    #Orgao
    orgaos = models.ManyToManyField('Orgao', through='Detalhe_Taxa')

    class Meta:
        verbose_name = 'Taxa'
        verbose_name_plural = 'Taxas'
        ordering = ['nome']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return f"Taxa: {self.nome}"

# Tabela associação de Taxa e Orgão
class Detalhe_Taxa(models.Model):
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    #Orgão
    orgao = models.ForeignKey(Orgao, on_delete=models.PROTECT)
    #Taxa
    taxa = models.ForeignKey(Taxa, on_delete=models.PROTECT)
    
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)

    class Meta:
        verbose_name = 'Detalhe Taxa'
        verbose_name_plural = 'Detalhes Taxas'
        ordering = ['date_added']

    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.valor_unitario

########################################

# UM CRONOGRAMA TEM VÁRIAS TAREFAS.
class Tarefa(models.Model):
    """Tarefa específica do 'Cronograma'. 
    Tem Funcionarios da Obra que executa a 
    MAO DE OBRA (funcionario vinculado na tabela Mao_de_Obra) 
    que é de uma 'Empreiteira'
    O que importa são os valores que uma tarefa tem.
    Por isso separado "Mao de Obra', 'Material' e, 'Taxa'.
    """

    #funcionario user
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT)
    # Cronograma tem cliente e funcionario
    cronograma = models.ForeignKey(Cronograma, on_delete=models.PROTECT)

    # Detalhe Mao de Obra
    detalhe_mao_de_obra = models.ManyToManyField(Detalhe_Mao_de_Obra, blank=True)
    # Detalhe Material - É IMPORTANTE JUNTAR AS CHAVES ESTRANGEIRA
    #PARA PODER FAZER CONSULTAS. Por isso criado Detalhe Material
    detalhe_material = models.ManyToManyField(Detalhe_Material, blank=True)
    # Taxa
    detalhe_taxa = models.ManyToManyField(Detalhe_Taxa, blank=True)

    ident = models.CharField(verbose_name = 'Identificador', max_length=4)
    nome = models.CharField(verbose_name = 'Nome', max_length=40)
    descricao = models.TextField(verbose_name = 'Descrição da Tarefa')
    dt_inicial = models.DateField(verbose_name = 'Inicio')
    dt_final = models.DateField(verbose_name = 'Termino')
    progresso = models.CharField(verbose_name= 'Progresso %', max_length=3)
    dependencias = models.CharField(verbose_name='Dependências', max_length=10)

    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)

    # classe Meta serve para modificar nomes para plural
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        #ordenar
        ordering = ['date_added']


    # Dicionário das tarefas
    def to_dict(self):
        """ Cria dicionário das tarefas
        
        Returns:
            dicionário -- com variáveis de Task
        """

        
        return {
            "id": self.ident,
            "name": self.nome,
            "start": str(self.dt_inicial),
            "end": str(self.dt_final),
            "progress": self.progresso,
            "dependencies": self.dependencias,
            "custom_class": "bar-milestone" # optional
        }

            
# {
#             "id": "3",
#             "name": "Gabaríto da Obra",
#             "start": "2020-02-24",
#             "end": "2020-03-20",
#             "progress": "20",
#             "dependencies": "2",
#             "custom_class": "bar-milestone" # optional
#         },
#

    def save(self, *args, **kwargs):
        super(Tarefa, self).save(*args, **kwargs)
        data = {
            'tarefa': self.nome, 'descricao': self.descricao,
            'progresso': self.progresso
        }
        plain_text = render_to_string('emails/cliente.txt', data)
        html_email = render_to_string('emails/cliente.html', data)
        subject = "Tarefa Cadastrada/Alterada"
        to = self.cronograma.cliente.email
        send_mail(
            subject, plain_text, settings.EMAIL_HOST_USER, [to], html_email
        )
        mail_admins(
            subject, plain_text, settings.EMAIL_HOST_USER
        )


    def __str__(self):
        """Devolve uma representação em string do modelo."""        
        if len(self.descricao) >= 50:
            return f"{self.descricao[:50]}..."
        
        return f"{self.nome} {self.descricao}"


# Comentario feito por um cliente
class Comentario(models.Model):
    """Tabela de comentário com referencia de cliente e funcionário."""

    nome_cliente = models.CharField("Nome do cliente", max_length=60)
    assunto = models.CharField("Assunto", max_length=60)
    descricao = models.TextField(verbose_name = 'Descrição')
    arquivo = models.FileField(
        upload_to="chamado/arquivos/", null=True, blank=True
        )
    # referência do cliente para o funcionário dos chamados
    funcionario = models.ForeignKey(
        "Funcionario", on_delete=models.PROTECT, related_name='funcionario'
        )
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.PROTECT, related_name='cliente'
        )
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    date_update = models.DateTimeField(verbose_name = 'Data de atualização', auto_now=True)
    
    def save(self, *args, **kwargs):
        super(Comentario, self).save(*args, **kwargs)
        data = {
            'cliente': self.nome_cliente, 'descricao': self.descricao,
            'funcionario': self.funcionario.nome
        }
        plain_text = render_to_string('emails/cliente_comentario.txt', data)
        html_email = render_to_string('emails/cliente_comentario.html', data)
        subject = "Comentário Enviado/Alterado"
        to = self.funcionario.email
        send_mail(
            subject, plain_text, settings.EMAIL_HOST_USER, [to], html_email
        )
        mail_admins(
            subject, plain_text, settings.EMAIL_HOST_USER
        )
   
    # classe Meta serve p modificar nomes e plural
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        # ordenar
        ordering = ["date_added"]
    
    #delete
    def delete(self, *args, **kwargs):
        self.arquivo.delete()
        super().delete(*args, **kwargs)

    def get_date_added(self):
        """Mostra data de entrada formatada."""
        return self.date_added.strftime("%d/%m/%Y %H h : %M min")

    def __str__(self):
        return f"{self.cliente.nome} {self.funcionario.nome}"
