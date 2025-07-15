import pandas as pd
import requests
import json
import urllib.parse
import sys
import os  # Importar a biblioteca os
from dotenv import load_dotenv  # Importar a função

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- Configurações ---
# 1. Lê a chave de API do ambiente. Retorna None se não encontrar.
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

# 2. Nomes dos arquivos de entrada e saída
CSV_FILENAME = "enderecos.csv"
OUTPUT_FILENAME = "resultados_geocodificacao.json"
# --- Fim das Configurações ---


def criar_payload_lote(enderecos):
    """
    Cria o corpo (payload) da requisição em lote a partir de uma lista de endereços.
    """
    batch_items = []
    for endereco in enderecos:
        if not isinstance(endereco, str) or not endereco.strip():
            print(f"Aviso: Ignorando endereço inválido ou vazio: {endereco}")
            continue
            
        # Codifica o endereço para que ele possa ser usado em uma URL
        query_encoded = urllib.parse.quote(endereco)
        
        # --- CORREÇÃO APLICADA AQUI ---
        # A 'query' dentro do lote NÃO deve incluir a versão da API (/2/) no caminho.
        # O caminho correto começa diretamente com 'geocode/'.
        query_path = f"/geocode/{query_encoded}.json?limit=1"
        batch_items.append({"query": query_path})
    
    return {"batchItems": batch_items}

def main():
    """
    Função principal: lê o CSV, chama a API e salva os resultados.
    """
    # Valida se a chave da API foi inserida
    if not TOMTOM_API_KEY:
        print("ERRO: Chave 'TOMTOM_API_KEY' não encontrada.")
        print("Verifique se você criou um arquivo .env e inseriu a chave nele.")
        sys.exit(1)

    # 1. Lê os endereços do arquivo CSV usando pandas
    try:
        df = pd.read_csv(CSV_FILENAME, dtype=str).fillna('')
        if 'endereco' not in df.columns:
            print(f"ERRO: O arquivo CSV '{CSV_FILENAME}' precisa ter uma coluna chamada 'endereco'.")
            return
        enderecos = df['endereco'].tolist()
        print(f"✅ Encontrados {len(enderecos)} endereços no arquivo '{CSV_FILENAME}'.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{CSV_FILENAME}' não encontrado.")
        print("Por favor, crie o arquivo no mesmo diretório do script e tente novamente.")
        return
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o CSV: {e}")
        return

    # 2. Cria o payload para a requisição em lote
    payload = criar_payload_lote(enderecos)
    
    if not payload["batchItems"]:
        print("Nenhum endereço válido para processar. Encerrando.")
        return

    # 3. Envia a requisição POST para a API da TomTom
    # A URL base da API de lote já contém a versão /2/
    api_url = f"https://api.tomtom.com/search/2/batch.json?key={TOMTOM_API_KEY}"
    
    print("🚀 Enviando requisição para a API da TomTom...")
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        
        resultados = response.json()
        
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
            
        print(f"✔️ Sucesso! Os resultados foram salvos no arquivo '{OUTPUT_FILENAME}'.")

    except requests.exceptions.HTTPError as errh:
        print(f"\n❌ Erro HTTP: {errh.response.status_code} {errh.response.reason}")
        print("Detalhes:", errh.response.text)
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro de Conexão: Não foi possível se conectar à API. Verifique sua conexão com a internet.")
    except requests.exceptions.Timeout:
        print("\n❌ Erro de Timeout: A requisição demorou muito para responder.")
    except requests.exceptions.RequestException as err:
        print(f"\n❌ Ocorreu um erro na requisição: {err}")

if __name__ == "__main__":
    main()