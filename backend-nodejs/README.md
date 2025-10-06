# Backend Node.js para o Dashboard MirAI

Este é o backend Node.js para o Dashboard Comercial MirAI, responsável por intermediar a comunicação com o Google Sheets e fornecer os dados para o frontend. Ele utiliza uma Service Account para acesso seguro e transparente aos dados da planilha.

## Funcionalidades

- **API RESTful**: Fornece endpoints para buscar dados e análises comerciais.
- **Integração com Google Sheets**: Utiliza a API do Google Sheets para acessar dados de planilhas.
- **Autenticação Transparente**: Usa Service Account para autenticação, eliminando a necessidade de login do usuário.
- **Filtragem de Dados**: Suporta filtragem de dados por intervalo de datas.
- **Dados Mock**: Inclui dados mock para desenvolvimento e testes sem a necessidade de configurar o Google Sheets imediatamente.

## Configuração

### Pré-requisitos

Certifique-se de ter o Node.js (versão 18 ou superior) e npm/pnpm instalados em sua máquina.

- [Node.js](https://nodejs.org/en/download/)

### 1. Clonar o Repositório (se aplicável)

Se você recebeu este backend como parte de um projeto maior, navegue até o diretório `backend-nodejs`.

```bash
cd mirai-dashboard-final/backend-nodejs
```

### 2. Instalar Dependências

```bash
npm install
# ou pnpm install
```

### 3. Configuração do Google Service Account

Para acessar dados reais do Google Sheets, você precisará configurar uma Service Account:

1.  **Crie uma Service Account no Google Cloud Platform**: Siga as instruções para criar uma Service Account e gerar um arquivo JSON de chave. Você precisará do `private_key` e `client_email` deste arquivo.

2.  **Crie um arquivo `.env`**: Na raiz do diretório `backend-nodejs`, crie um arquivo chamado `.env` e adicione as seguintes variáveis de ambiente, substituindo os placeholders pelas suas credenciais:

    ```
    GOOGLE_PRIVATE_KEY_ID="SEU_PRIVATE_KEY_ID"
    GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nSEU_PRIVATE_KEY_AQUI\n-----END PRIVATE KEY-----\n"
    GOOGLE_CLIENT_EMAIL="SEU_CLIENT_EMAIL_AQUI"
    GOOGLE_CLIENT_ID="SEU_CLIENT_ID_AQUI"
    ```

    **Importante**: A `GOOGLE_PRIVATE_KEY` deve ser inserida com as quebras de linha (`\n`) como mostrado acima.

3.  **Compartilhe a Planilha Google Sheets**: Conceda permissão de leitura à sua Service Account (o `GOOGLE_CLIENT_EMAIL`) na planilha do Google Sheets que contém os dados. O `SPREADSHEET_ID` e `RANGE_NAME` também devem ser configurados no arquivo `index.js`.

4.  **Descomente o código de integração com Google Sheets**: No arquivo `index.js`, localize a função `getSheetsService` e descomente o código que inicializa o serviço do Google Sheets com as credenciais da Service Account. Faça o mesmo nos endpoints `/api/data` e `/api/analytics` para usar os dados reais em vez dos dados mock.

### 4. Executar o Backend

```bash
npm start
# ou pnpm start
```

O backend será executado na porta `5000`.

## Endpoints da API

- `GET /api/health`: Verifica o status do servidor.
- `GET /api/data`: Retorna todos os dados da planilha. Suporta `start_date` e `end_date` como parâmetros de query (ex: `/api/data?start_date=2024-01-01&end_date=2024-01-31`).
- `GET /api/analytics`: Retorna análises agregadas dos dados. Suporta `start_date` e `end_date` como parâmetros de query.

## Estrutura do Projeto

```
backend-nodejs/
├── node_modules/
├── index.js
├── package.json
├── package-lock.json
└── .env (arquivo a ser criado por você)
└── README.md
```
