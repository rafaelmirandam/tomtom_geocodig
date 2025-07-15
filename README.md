# Geocodificação de Endereços em Lote com TomTom API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Este projeto contém um script Python que automatiza a geocodificação de múltiplos endereços listados em um arquivo CSV. Ele utiliza a API de Lote (Batch API) da TomTom para processar os endereços de forma eficiente e segura.

## Funcionalidades

-   **Leitura de CSV:** Lê uma lista de endereços a partir de um arquivo `enderecos.csv`.
-   **Processamento em Lote:** Envia todos os endereços em uma única requisição para a API da TomTom, otimizando o tempo e o número de chamadas.
-   **Gerenciamento de API Key:** Utiliza um arquivo `.env` para gerenciar a chave da API de forma segura, mantendo-a fora do código-fonte.
-   **Exportação de Resultados:** Salva a resposta completa da API, com as coordenadas e outros detalhes, em um arquivo `resultados_geocodificacao.json`.

## Pré-requisitos

Antes de começar, você precisará ter:

-   [Python](https://www.python.org/downloads/) (versão 3.8 ou superior)
-   [Git](https://git-scm.com/downloads/)
-   Uma chave de API válida da [TomTom Developer Portal](https://developer.tomtom.com/).

## Instalação

Siga os passos abaixo para configurar o ambiente do projeto:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **(Recomendado) Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure sua chave de API:**
    Crie uma cópia do arquivo de exemplo `.env.example` e renomeie-a para `.env`.
    ```bash
    # No Windows (prompt de comando)
    copy .env.example .env

    # No macOS/Linux
    cp .env.example .env
    ```
    Em seguida, abra o arquivo `.env` e insira sua chave da API da TomTom.

    **`.env`**
    ```env
    TOMTOM_API_KEY="SUA_CHAVE_DE_API_REAL_AQUI"
    ```

## Como Usar

1.  **Prepare seus dados de entrada:**
    Abra o arquivo `enderecos.csv` e adicione os endereços que deseja geocodificar, um por linha, sob a coluna `endereco`.

    **`enderecos.csv`**
    ```csv
    endereco
    "Avenida Paulista, 1578, São Paulo, SP"
    "Praça da Sé, s/n, São Paulo, SP"
    "Rua do Russel, 632, Rio de Janeiro, RJ"
    ```

2.  **Execute o script:**
    Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando no seu terminal:
    ```bash
    python find_address.py
    ```

3.  **Verifique os resultados:**
    Após a execução, um novo arquivo chamado `resultados_geocodificacao.json` será criado na pasta do projeto, contendo a resposta da API para cada endereço solicitado.

## Estrutura do Projeto
    |
    ├── .gitignore          # Arquivos e pastas a serem ignorados pelo Git
    ├── .env.example        # Arquivo de exemplo para variáveis de ambiente
    ├── .env                # (Local) Arquivo com sua chave de API (ignorado pelo Git)
    ├── requirements.txt    # Lista de dependências Python do projeto
    ├── enderecos.csv       # (Local) Sua lista de endereços para geocodificar
    ├── buscar_enderecos_corrigido.py # O script principal
    └── README.md           # Este arquivo

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.