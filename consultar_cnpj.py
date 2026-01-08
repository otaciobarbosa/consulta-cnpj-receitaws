import pandas as pd
import requests
import time
from datetime import datetime

def limpar_cnpj(cnpj):
    """Remove caracteres especiais do CNPJ"""
    if pd.isna(cnpj):
        return None
    return str(cnpj).replace('.', '').replace('/', '').replace('-', '').strip()

def consultar_cnpj(cnpj):
    """Consulta o CNPJ na API ReceitaWS"""
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit atingido! Aguardando 60 segundos...")
            time.sleep(60)
            return consultar_cnpj(cnpj)  # Tenta novamente
        else:
            print(f"Erro ao consultar CNPJ {cnpj}: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao consultar CNPJ {cnpj}: {str(e)}")
        return None

def main():
    # Ler a planilha
    import os
    
    # Pegar o diretório onde o script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Verificar primeiro se existe o arquivo real, senão usar o exemplo
    arquivo_real = os.path.join(script_dir, 'CNPJ ate 60000.xlsx')
    arquivo_exemplo = os.path.join(script_dir, 'exemplo_cnpjs.xlsx')
    
    if os.path.exists(arquivo_real):
        arquivo_entrada = arquivo_real
    elif os.path.exists(arquivo_exemplo):
        arquivo_entrada = arquivo_exemplo
        print("⚠ Usando arquivo de exemplo com CNPJs fictícios")
    else:
        print(f"ERRO: Nenhum arquivo encontrado!")
        print(f"Procure por: 'CNPJ ate 60000.xlsx' ou 'exemplo_cnpjs.xlsx'")
        print(f"Diretório do script: {script_dir}")
        return
    
    print(f"Lendo arquivo {os.path.basename(arquivo_entrada)}...")
    
    try:
        df = pd.read_excel(arquivo_entrada, engine='openpyxl')
    except Exception as e:
        print(f"ERRO ao ler o arquivo: {e}")
        return
    
    # Verificar se coluna B existe (assumindo que é a segunda coluna)
    # Na planilha, coluna B é a segunda coluna (índice 1)
    if len(df.columns) < 2:
        print("ERRO: A planilha não possui coluna B!")
        return
    
    # Pegar CNPJs da coluna B
    cnpjs = df.iloc[:, 1]  # Segunda coluna (índice 1)
    
    print(f"Total de {len(cnpjs)} CNPJs encontrados na coluna B")
    
    # Lista para armazenar resultados
    resultados = []
    
    # Processar cada CNPJ
    for idx, cnpj_raw in enumerate(cnpjs, 1):
        cnpj = limpar_cnpj(cnpj_raw)
        
        if not cnpj:
            print(f"[{idx}/{len(cnpjs)}] CNPJ vazio, pulando...")
            continue
        
        print(f"[{idx}/{len(cnpjs)}] Consultando CNPJ: {cnpj}")
        
        dados = consultar_cnpj(cnpj)
        
        if dados:
            # Extrair apenas as colunas solicitadas
            resultado = {
                'cnpj': cnpj_raw,  # CNPJ original da planilha
                'abertura': dados.get('abertura', ''),
                'situacao': dados.get('situacao', ''),
                'tipo': dados.get('tipo', '')
            }
            resultados.append(resultado)
            print(f"  ✓ Consultado")
        else:
            # Adicionar linha vazia se não conseguiu consultar
            resultados.append({
                'cnpj': cnpj_raw,
                'abertura': 'ERRO',
                'situacao': 'ERRO',
                'tipo': 'ERRO'
            })
        
        # Delay entre requisições para evitar rate limit (3 segundos)
        if idx < len(cnpjs):
            print(f"  Aguardando 20 segundos antes da próxima consulta...")
            time.sleep(20)
    
    # Salvar resultados em novo Excel
    arquivo_saida = os.path.join(script_dir, f'resultado_cnpj_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx')
    print(f"\nSalvando resultados em {arquivo_saida}...")
    
    df_resultado = pd.DataFrame(resultados)
    df_resultado.to_excel(arquivo_saida, index=False, engine='openpyxl')
    
    print(f"\n✓ Processo concluído!")
    print(f"✓ Total de CNPJs consultados: {len(resultados)}")
    print(f"✓ Arquivo salvo: {arquivo_saida}")

if __name__ == "__main__":
    main()
