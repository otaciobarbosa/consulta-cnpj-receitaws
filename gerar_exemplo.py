import pandas as pd
import random

def gerar_cnpj_ficticio():
    """Gera um CNPJ fictício com formato válido"""
    # Gera números aleatórios para o CNPJ
    base = [random.randint(0, 9) for _ in range(12)]
    
    # Calcula primeiro dígito verificador
    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma1 = sum(a * b for a, b in zip(base, peso1))
    resto1 = soma1 % 11
    dv1 = 0 if resto1 < 2 else 11 - resto1
    base.append(dv1)
    
    # Calcula segundo dígito verificador
    peso2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma2 = sum(a * b for a, b in zip(base, peso2))
    resto2 = soma2 % 11
    dv2 = 0 if resto2 < 2 else 11 - resto2
    base.append(dv2)
    
    # Formata o CNPJ
    cnpj = ''.join(map(str, base))
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

# Gerar 20 CNPJs fictícios
dados = {
    'Código': list(range(1, 21)),
    'CNPJ/CPF': [gerar_cnpj_ficticio() for _ in range(20)]
}

df = pd.DataFrame(dados)

# Salvar no Excel
arquivo_saida = 'exemplo_cnpjs.xlsx'
df.to_excel(arquivo_saida, index=False, engine='openpyxl')

print(f"✓ Arquivo {arquivo_saida} criado com sucesso!")
print(f"✓ Total de {len(df)} CNPJs fictícios gerados")
