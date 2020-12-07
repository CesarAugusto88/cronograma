from django import forms

from apps.confidencechronograms.models import Cliente, Funcionario


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
            'nome', 'cpf', 'rg', 'rua', 'numero', 'bairro', 'cidade',
            'cep', 'uf', 'email', 'fone', 'usuario'
            )
