from django import forms
from django.forms import ModelForm

from apps.confidencechronograms.models import (
    Cliente, Funcionario, Tarefa, Cronograma, Comentario, Empreiteira,
    Mao_de_Obra, Funcionario_da_Obra, Deposito,
    Categoria, Material, Taxa, Orgao
)


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
            'tempo_total', 'valor_total', 'funcionario'
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
        fields = ('nome', 'cnpj', 'email', 'fone', 'cronogramas')


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
            'quantidade', 'funcionarios_da_obra', 'cronograma'
            )

    # funcionarios_da_obra = forms.ModelMultipleChoiceField(
    #     queryset=Funcionario_da_Obra.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    # ADICIONAR BOTÃO
    # widgets = {
    #     'funcionarios_da_obra': AddAnotherEditSelectedWidgetWrapper(
    #         forms.Select,
    #         reverse_lazy('novo_funcionario_da_bra'),
    #         reverse_lazy('alterar_funcionario_da_obra', args=['__fk__']),
    #     )
    # }
    # permission_required = 'libraryapp.can_edit'


class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ('nome', 'cnpj', 'email', 'fone')


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = (
            'nome', 'unidade', 'valor_unitario',
            'quantidade', 'deposito', 'categoria', 'deposito', 'cronograma'
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
        fields = (
            'nome', 'unidade', 'valor_unitario',
            'quantidade', 'orgao', 'cronograma'
            )


class DateInput(forms.DateInput):
    input_type = 'date'


class TarefaForm(ModelForm):
    class Meta:
        model = Tarefa

        localized_fields = ('dt_inicial', 'dt_final')

        fields = (
             'cronograma', 'maos_de_obra', 'materiais',
             'taxas', 'ident', 'dependencias',
             'nome', 'descricao', 'dt_inicial', 'dt_final', 'progresso',
            )

        widgets = {
            'dt_inicial': forms.DateInput(
                format='%d-%m-Y', attrs={'type': 'date'}),
            'dt_final': forms.DateInput(
                format='%d-%m-Y', attrs={'type': 'date'}),
            'progresso': forms.TextInput(attrs={'type': 'number',
                                                'step': '1', 'min': '0',
                                                'max': '100'}),
            }

        # def __init__(self, *args, **kwargs):
        #     super(TarefaForm, self).__init__(*args, **kwargs)
        #     # input_formats to parse HTML5 datetime-local
        #     # input to datetime field
        #     self.fields['dt_inicial'].input_formats = ('%Y-%m-%dT%H:%M',)
        #     self.fields['dt_final'].input_formats = ('%Y-%m-%dT%H:%M',)
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
    # ) widgets = {'my_date_field': DateInput()}


# Para alterar clientes pelo funcionario
class ClientesForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'nome', 'cpf', 'rg', 'rua', 'numero', 'bairro', 'cidade',
            'cep', 'uf', 'email', 'fone', 'usuario'
            )
