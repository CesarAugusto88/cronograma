from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

import re


def valida_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.

    # CNPJs errados
    >>> validar_cnpj('abcdefghijklmn')
    False
    >>> validar_cnpj('123')
    False
    >>> validar_cnpj('')
    False
    >>> validar_cnpj(None)
    False
    >>> validar_cnpj('12345678901234')
    False
    >>> validar_cnpj('11222333000100')
    False

    # CNPJs corretos
    >>> validar_cnpj('11222333000181')
    '11222333000181'
    >>> validar_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validar_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """
    cnpj = ''.join(re.findall('\d', str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e
    # gera os 2 dígitos que faltam

    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cnpj
    return False


# Valida CNPJ
# REGRESSIVOS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
# def valida(cnpj):
#     cnpj = apenas_numeros(cnpj)

#     try:
#         if eh_sequencia(cnpj):
#             return False
#     except Exception:
#         return False

#     try:
#         novo_cnpj = calcula_digito(cnpj=cnpj, digito=1)
#         novo_cnpj = calcula_digito(cnpj=novo_cnpj, digito=2)
#     except Exception:
#         return False

#     if novo_cnpj == cnpj:
#         return True
#     else:
#         return False


# def calcula_digito(cnpj, digito):
#     if digito == 1:
#         regressivos = REGRESSIVOS[1:]
#         novo_cnpj = cnpj[:-2]
#     elif digito == 2:
#         regressivos = REGRESSIVOS
#         novo_cnpj = cnpj
#     else:
#         return None

#     total = 0
#     for indice, regressivo in enumerate(regressivos):
#         total += int(cnpj[indice]) * regressivo

#     digito = 11 - (total % 11)
#     digito = digito if digito <= 9 else 0

#     return f'{novo_cnpj}{digito}'


# def eh_sequencia(cnpj):
#     sequencia = cnpj[0] * len(cnpj)

#     if sequencia == cnpj:
#         return True
#     else:
#         return False


# def apenas_numeros(cnpj):
#     return re.sub(r'[^0-9]', '', cnpj)


# Valida CPF
def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11:
        return False

    novo_cpf = cpf[:-2]  # Elimina os dois últimos digitos do CPF
    reverso = 10         # Contador reverso
    total = 0

    # Loop do CPF
    for index in range(19):
        if index > 8:                   # Primeiro índice vai de 0 a 9,
            index -= 9                  # São os 9 primeiros digitos do CPF

        total += int(novo_cpf[index]) * reverso  # Valor total da multiplicação

        reverso -= 1                    # Decrementa o contador reverso
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d > 9:                   # Se o digito for > que 9 o valor é 0
                d = 0
            total = 0                   # Zera o total
            novo_cpf += str(d)          # Concatena o digito gerado no novo cpf

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Descobri que sequências avaliavam como verdadeiro, então também
    # adicionei essa checagem aqui
    if cpf == novo_cpf and not sequencia:
        return True
    else:
        return False


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
