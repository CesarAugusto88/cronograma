from django import forms

from apps.confidencechronograms.models import (
    Cliente, Funcionario, Tarefa, Cronograma, Comentario, Empreiteira,
    Mao_de_Obra, Funcionario_da_Obra, Deposito,
    Categoria, Material, Taxa, Orgao
)
# Detalhe_Mao_de_Obra, Detalhe_Taxa, Detalhe_Funcionario_da_Obra, 
# Detalhe_Material, Detalhe_Mao_de_Obra_Tarefa


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'nome', 'cpf', 'rg', 'rua', 'numero', 'bairro', 'cidade',
            'cep', 'uf', 'email', 'fone', 'usuario'
            )


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario

        fields = (
            'nome', 'cpf', 'rg', 'rua', 'numero', 'bairro',
            'cidade', 'fone', 'usuario'
            )


class CronogramaForm(forms.ModelForm):
    class Meta:
        model = Cronograma
        fields = (
            'estrutura', 'cliente', 'proprietario', 'endereco',
            'tempo_total', 'valor_total'
            )


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = (
            'nome_cliente', 'assunto', 'descricao',
            'arquivo', 'funcionario'
        )


###########################
class EmpreiteiraForm(forms.ModelForm):
    class Meta:
        model = Empreiteira
        fields = ('nome', 'cnpj', 'email', 'fone')


class Funcionario_da_ObraForm(forms.ModelForm):
    class Meta:
        model = Funcionario_da_Obra
        fields = (
            'nome', 'cpf', 'rg', 'rua', 'numero', 'bairro', 'cidade',
            'email', 'fone', 'empreiteira'
            )


class Mao_de_ObraForm(forms.ModelForm):
    class Meta:
        model = Mao_de_Obra
        fields = (
            'nome', 'unidade', 'valor_unitario',
            'quantidade', 'funcionarios_da_obra'
            )

    # funcionarios_da_obra = forms.ModelMultipleChoiceField(
    #     queryset=Funcionario_da_Obra.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )


class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ('nome', 'cnpj', 'email', 'fone')


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = (
            'nome', 'unidade', 'valor_unitario',
            'quantidade', 'deposito', 'categoria', 'deposito'
            )


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nome',)


class OrgaoForm(forms.ModelForm):
    class Meta:
        model = Orgao
        fields = ('nome', 'cnpj', 'email', 'fone')


class TaxaForm(forms.ModelForm):
    class Meta:
        model = Taxa
        fields = ('nome', 'unidade', 'valor_unitario', 'quantidade', 'orgao')


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = (
             'cronograma', 'maos_de_obra', 'materiais', 'taxas', 'ident',
             'nome', 'descricao', 'dt_inicial', 'dt_final', 'progresso',
             'dependencias'
            )

    # maos_de_obra = forms.ModelMultipleChoiceField(
    #     queryset=Mao_de_Obra.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    # materiais = forms.ModelMultipleChoiceField(
    #     queryset=Material.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    # taxas = forms.ModelMultipleChoiceField(
    #     queryset=Taxa.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )


# Para alterar clientes pelo funcionario
class ClientesForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'nome', 'cpf', 'rg', 'rua', 'numero', 'bairro', 'cidade',
            'cep', 'uf', 'email', 'fone', 'usuario'
            )


# ---------------------------------------------
# class Detalhe_Mao_de_ObraForm(forms.ModelForm):
#     class Meta:
#         model = Detalhe_Mao_de_Obra
#         fields = (
#             'valor_unitario', 'quantidade', 'mao_de_obra',
#             'empreiteira'
#         )


# class Detalhe_Funcionario_da_ObraForm(forms.ModelForm):
#     class Meta:
#         model = Detalhe_Funcionario_da_Obra
#         fields = ('funcionario_da_obra', 'mao_de_obra')
# -------------------------------------------------------

# -------------------------------------------------------------
# class Detalhe_MaterialForm(forms.ModelForm):
#     class Meta:
#         model = Detalhe_Material
#         fields = (
#             'valor_unitario', 'quantidade', 'material', 'deposito', 
#             'categoria'
#         )
# -------------------------------------------------------------


# --------------------------------------------------
# class Detalhe_TaxaForm(forms.ModelForm):
#     class Meta:
#         model = Detalhe_Taxa
#         fields = ('valor_unitario', 'quantidade', 'orgao', 'taxa')
# --------------------------------------------------

# -------------------------------------------------------------
# class Detalhe_Mao_de_Obra_TarefaForm(forms.ModelForm):
#     class Meta:
#         model = Detalhe_Mao_de_Obra_Tarefa
#         fields = (
#             'mao_de_obra', 'tarefa'
#         )
# -------------------------------------------------------------
