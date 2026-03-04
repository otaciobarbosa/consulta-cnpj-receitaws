# Consulta CNPJ - ReceitaWS

Script Python para consultar CNPJs em massa na API ReceitaWS e salvar os resultados em Excel.

## 📋 Funcionalidades

- ✅ Lê CNPJs da coluna B de uma planilha Excel
- ✅ Consulta cada CNPJ na API ReceitaWS (https://www.receitaws.com.br/)
- ✅ Controle automático de rate limiting (3 segundos entre requisições)
- ✅ Tratamento de erro "Too many requests" (aguarda 60s e retenta automaticamente)
- ✅ Salva resultados em novo arquivo Excel com as colunas:
  - CNPJ
  - Data de Abertura
  - Situação
  - Tipo (Matriz/Filial)
  - CNAE Principal (código e descrição)
  - CNAEs Secundários (códigos e descrições)

## 🚀 Instalação

### 1. Instale o Python

Baixe e instale o Python 3.x em: https://www.python.org/downloads/

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install pandas openpyxl requests
```

## 📖 Como Usar

### Modo de Teste (com CNPJs fictícios)

O projeto inclui um arquivo de exemplo `exemplo_cnpjs.xlsx` com 20 CNPJs fictícios para testar:

```bash
python consultar_cnpj.py
```

### Modo de Produção (com seus dados)

1. Coloque sua planilha Excel na pasta do projeto com o nome `exemplo_cnpjs.xlsx`
2. Certifique-se de que os CNPJs estão na **coluna B**
3. Execute o script:

```bash
python consultar_cnpj.py
```

### Gerar novo arquivo de exemplo

Para criar um novo arquivo de exemplo com CNPJs fictícios:

```bash
python gerar_exemplo.py
```

## 📂 Estrutura dos Arquivos

```
├── consultar_cnpj.py       # Script principal
├── gerar_exemplo.py         # Gerador de CNPJs fictícios
├── exemplo_cnpjs.xlsx       # Arquivo de exemplo (incluído)
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
└── .gitignore              # Arquivos ignorados pelo git
```

## ⚙️ Configurações

### Ajustar delay entre requisições

No arquivo `consultar_cnpj.py`, linha ~99:

```python
time.sleep(20)  # Altere para o valor desejado em segundos
```

### Limitar número de CNPJs (para teste)

No arquivo `consultar_cnpj.py`, após a linha 56:

```python
cnpjs = df.iloc[:, 1]
cnpjs = cnpjs.head(3)  # Adicione esta linha para processar apenas 3 CNPJs
```

## 📊 Formato da Planilha de Entrada

A planilha deve ter CNPJs na **coluna B**:

| Coluna A | Coluna B (CNPJ/CPF) |
|----------|---------------------|
| 1        | 12.345.678/0001-90  |
| 2        | 98.765.432/0001-10  |

## 💾 Arquivo de Saída

O script gera um arquivo com nome no formato:
- `resultado_cnpj_YYYYMMDD_HHMMSS.xlsx`

Exemplo: `resultado_cnpj_20260108_143025.xlsx`

## ⚠️ Observações Importantes

- A API ReceitaWS é gratuita mas possui limite de requisições
- O script adiciona delay automático para evitar bloqueio
- Em caso de erro 429 (Too many requests), aguarda 60 segundos automaticamente
- CNPJs inválidos ou que causem erro terão "ERRO" nas colunas
- Os arquivos com dados reais são ignorados pelo git (.gitignore)

## 📝 Licença

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo LICENSE para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
