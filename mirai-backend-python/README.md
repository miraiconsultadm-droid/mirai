# MirAI - Backend Comercial (Python Flask)

Este é o backend da aplicação de dashboard comercial da MirAI, desenvolvido em Python com o framework Flask. Ele é responsável por:

- **Extrair dados**: Conecta-se ao Google Sheets (que recebe os dados do Formsite via n8n) para obter os relatórios diários comerciais.
- **Processar dados**: Filtra e agrega os dados com base em parâmetros de data.
- **Servir dados**: Expõe endpoints RESTful para que o frontend possa consumir os dados processados e análises.
- **CORS**: Configurado para permitir requisições de qualquer origem, facilitando a integração com o frontend.

## Endpoints da API

- `GET /api/health`: Retorna o status de saúde do serviço.
- `GET /api/data?start_date=<YYYY-MM-DD>&end_date=<YYYY-MM-DD>`: Retorna os dados brutos do Google Sheets, filtrados por data opcionalmente.
- `GET /api/analytics?start_date=<YYYY-MM-DD>&end_date=<YYYY-MM-DD>`: Retorna métricas e análises agregadas dos dados, filtradas por data opcionalmente.

## Configuração de Variáveis de Ambiente

As credenciais do Google Service Account e o ID da planilha são configurados via variáveis de ambiente. É necessário definir as seguintes variáveis no ambiente de implantação (ex: Vercel):

- `GOOGLE_SPREADSHEET_ID`: O ID da sua planilha do Google Sheets.
- `GOOGLE_SHEET_RANGE_NAME`: O nome da aba e o intervalo de células (ex: `Respostas ao formulário 1!A:M`).
- `GOOGLE_CREDENTIALS_JSON`: (Opcional) Um JSON contendo todas as credenciais da conta de serviço. Se esta variável for definida, ela terá precedência sobre as variáveis individuais.

Alternativamente, as credenciais podem ser definidas individualmente:
- `GOOGLE_TYPE`: `service_account`
- `GOOGLE_PROJECT_ID`: ID do seu projeto Google Cloud.
- `GOOGLE_PRIVATE_KEY_ID`: ID da chave privada da conta de serviço.
- `GOOGLE_PRIVATE_KEY`: Chave privada da conta de serviço (incluindo `-----BEGIN PRIVATE KEY-----` e `-----END PRIVATE KEY-----`, com `\n` para quebras de linha).
- `GOOGLE_CLIENT_EMAIL`: Email da conta de serviço.
- `GOOGLE_CLIENT_ID`: ID do cliente da conta de serviço.
- `GOOGLE_AUTH_URI`: `https://accounts.google.com/o/oauth2/auth`
- `GOOGLE_TOKEN_URI`: `https://oauth2.googleapis.com/token`
- `GOOGLE_AUTH_PROVIDER_X509_CERT_URL`: `https://www.googleapis.com/oauth2/v1/certs`
- `GOOGLE_CLIENT_X509_CERT_URL`: URL do certificado X.509 do cliente.

## Desenvolvimento Local

1. Clone o repositório.
2. Crie e ative um ambiente virtual:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto com suas variáveis de ambiente do Google Sheets.
5. Execute o servidor:
   ```bash
   python src/main.py
   ```

O servidor estará disponível em `http://localhost:5000`.
