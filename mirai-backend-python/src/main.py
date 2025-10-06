
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configurações do Google Sheets
SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID", "1JstbxuG7JG4EMHHzcT9UZtJihkXlEz09gZza1vShJWk")
RANGE_NAME = os.getenv("GOOGLE_SHEET_RANGE_NAME", "TaxLab!A:M")

def get_service_account_info():
    try:
        # Tentar obter credenciais das variáveis de ambiente
        if os.getenv("GOOGLE_CREDENTIALS_JSON"):
            return json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
        else:
            return {
                "type": "service_account",
                "project_id": os.getenv("GOOGLE_PROJECT_ID", "mirai-dashboard-project"),
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n"),
                "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv("GOOGLE_CLIENT_EMAIL", "")}"
            }
    except Exception as e:
        print(f"Erro ao obter credenciais: {e}")
        return None

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def get_sheets_service():
    try:
        service_account_info = get_service_account_info()
        if not service_account_info:
            return None
            
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES)
        service = build("sheets", "v4", credentials=credentials)
        return service
    except Exception as e:
        print(f"Erro ao inicializar serviço Google Sheets: {e}")
        return None

# Dados mock para desenvolvimento/teste (ajustados para a nova estrutura)
def get_mock_data():
    return [
        {
            "data": "02/10/2025",
            "nome_do_colaborador": "Fernando",
            "quantos_leads_foram_trabalhados_hoje": 48,
            "quantos_contatos_foram_realizados_hoje": 4,
            "descreva_rapidamente_o_feedback_mais_comum_dos_leads": "48 mensagens efetivas sem ligações.",
            "quantas_reunioes_foram_agendadas_hoje": 0,
            "quantas_propostas_foram_enviadas_hoje": 0,
            "quantas_vendas_foram_fechadas_hoje": 0,
            "quais_foram_os_principais_impedimentos_ou_objecoes_do_dia": "",
            "algum_lead_demonstrou_interesse_para_acompanhamento_futuro": "",
            "qual_sera_a_acao_prioritaria_para_amanha": "",
            "alguma_sugestao_para_melhorar_abordagem_ou_processo": "",
            "algum_detalhe_adicional_que_deve_ser_registrado": ""
        },
        {
            "data": "03/10/2025",
            "nome_do_colaborador": "Fernando",
            "quantos_leads_foram_trabalhados_hoje": 53,
            "quantos_contatos_foram_realizados_hoje": 2,
            "descreva_rapidamente_o_feedback_mais_comum_dos_leads": "Não atendem, 3 whats caíram.",
            "quantas_reunioes_foram_agendadas_hoje": 0,
            "quantas_propostas_foram_enviadas_hoje": 0,
            "quantas_vendas_foram_fechadas_hoje": 0,
            "quais_foram_os_principais_impedimentos_ou_objecoes_do_dia": "",
            "algum_lead_demonstrou_interesse_para_acompanhamento_futuro": "",
            "qual_sera_a_acao_prioritaria_para_amanha": "",
            "alguma_sugestao_para_melhorar_abordagem_ou_processo": "",
            "algum_detalhe_adicional_que_deve_ser_registrado": ""
        },
        {
            "data": "06/10/2025",
            "nome_do_colaborador": "Vinícius",
            "quantos_leads_foram_trabalhados_hoje": 0,
            "quantos_contatos_foram_realizados_hoje": 0,
            "descreva_rapidamente_o_feedback_mais_comum_dos_leads": "",
            "quantas_reunioes_foram_agendadas_hoje": 0,
            "quantas_propostas_foram_enviadas_hoje": 0,
            "quantas_vendas_foram_fechadas_hoje": 0,
            "quais_foram_os_principais_impedimentos_ou_objecoes_do_dia": "",
            "algum_lead_demonstrou_interesse_para_acompanhamento_futuro": "",
            "qual_sera_a_acao_prioritaria_para_amanha": "",
            "alguma_sugestao_para_melhorar_abordagem_ou_processo": "",
            "algum_detalhe_adicional_que_deve_ser_registrado": ""
        },
        {
            "data": "06/10/2025",
            "nome_do_colaborador": "Aline",
            "quantos_leads_foram_trabalhados_hoje": 69,
            "quantos_contatos_foram_realizados_hoje": 7,
            "descreva_rapidamente_o_feedback_mais_comum_dos_leads": "Dois caiu na pessoa errada, 1 passou o contato do adm (chamei sem r",
            "quantas_reunioes_foram_agendadas_hoje": 0,
            "quantas_propostas_foram_enviadas_hoje": 0,
            "quantas_vendas_foram_fechadas_hoje": 0,
            "quais_foram_os_principais_impedimentos_ou_objecoes_do_dia": "",
            "algum_lead_demonstrou_interesse_para_acompanhamento_futuro": "",
            "qual_sera_a_acao_prioritaria_para_amanha": "",
            "alguma_sugestao_para_melhorar_abordagem_ou_processo": "",
            "algum_detalhe_adicional_que_deve_ser_registrado": ""
        },
        {
            "data": "06/10/2025",
            "nome_do_colaborador": "Fernando",
            "quantos_leads_foram_trabalhados_hoje": 67,
            "quantos_contatos_foram_realizados_hoje": 6,
            "descreva_rapidamente_o_feedback_mais_comum_dos_leads": "mais comum é sem interesse",
            "quantas_reunioes_foram_agendadas_hoje": 0,
            "quantas_propostas_foram_enviadas_hoje": 0,
            "quantas_vendas_foram_fechadas_hoje": 0,
            "quais_foram_os_principais_impedimentos_ou_objecoes_do_dia": "",
            "algum_lead_demonstrou_interesse_para_acompanhamento_futuro": "",
            "qual_sera_a_acao_prioritaria_para_amanha": "",
            "alguma_sugestao_para_melhorar_abordagem_ou_processo": "",
            "algum_detalhe_adicional_que_deve_ser_registrado": ""
        },
        {
            "data": "06/10/2025",
            "nome_do_colaborador": "Pâmela",
            "quantos_leads_foram_trabalhados_hoje": 29,
            "quantos_contatos_foram_realizados_hoje": 26,
            "descreva_rapidamente_o_feedback_mais_comum_dos_leads": "interações de como funciona",
            "quantas_reunioes_foram_agendadas_hoje": 0,
            "quantas_propostas_foram_enviadas_hoje": 0,
            "quantas_vendas_foram_fechadas_hoje": 0,
            "quais_foram_os_principais_impedimentos_ou_objecoes_do_dia": "",
            "algum_lead_demonstrou_interesse_para_acompanhamento_futuro": "",
            "qual_sera_a_acao_prioritaria_para_amanha": "",
            "alguma_sugestao_para_melhorar_abordagem_ou_processo": "",
            "algum_detalhe_adicional_que_deve_ser_registrado": ""
        }
    ]

# Função para filtrar dados por intervalo de datas
def filter_data_by_date(data, start_date, end_date):
    if not start_date and not end_date:
        return data
    
    filtered_data = []
    for item in data:
        try:
            item_date_str = item.get("data", "").strip()
            if not item_date_str:
                continue
                
            # A data na planilha está no formato DD/MM/YYYY
            item_date = datetime.strptime(item_date_str, "%d/%m/%Y")
            
            if start_date and end_date:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                if start_dt <= item_date <= end_dt:
                    filtered_data.append(item)
            elif start_date:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                if item_date >= start_dt:
                    filtered_data.append(item)
            elif end_date:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                if item_date <= end_dt:
                    filtered_data.append(item)
        except (ValueError, TypeError):
            # Ignorar itens com formato de data inválido
            continue
    return filtered_data

# Endpoint de health check
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "MirAI Dashboard Backend"
    })

# Endpoint para obter dados da planilha
@app.route("/api/data", methods=["GET"])
def get_sheet_data():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Tentar usar dados reais do Google Sheets
    service = get_sheets_service()
    if service:
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME
            ).execute()
            values = result.get("values", [])

            if not values:
                # Se não há dados reais, usar dados mock
                data = get_mock_data()
            else:
                headers = values[0] if values else []
                data = []
                for row in values[1:]:
                    row_dict = {}
                    for i, header in enumerate(headers):
                        if i < len(row):
                            # Normalizar nomes de cabeçalho
                            clean_header = header.lower().replace(" ", "_").replace("?", "").replace("(", "").replace(")", "")
                            row_dict[clean_header] = row[i]
                    data.append(row_dict)
        except Exception as e:
            print(f"Erro ao buscar dados do Google Sheets: {e}")
            data = get_mock_data()
    else:
        # Usar dados mock se não conseguir conectar
        data = get_mock_data()

    # Converter valores numéricos e formatar data
    for item in data:
        for key in ["quantos_leads_foram_trabalhados_hoje", "quantos_contatos_foram_realizados_hoje", 
                   "quantas_reunioes_foram_agendadas_hoje", "quantas_propostas_foram_enviadas_hoje", 
                   "quantas_vendas_foram_fechadas_hoje"]:
            if key in item and isinstance(item[key], str):
                try:
                    item[key] = int(item[key])
                except ValueError:
                    item[key] = 0
        # Converter o campo 'data' para o formato esperado (YYYY-MM-DD) para o frontend
        if "data" in item and isinstance(item["data"], str):
            try:
                item["data"] = datetime.strptime(item["data"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass # Manter o formato original se a conversão falhar

    filtered_data = filter_data_by_date(data, start_date, end_date)

    return jsonify({
        "success": True,
        "data": filtered_data,
        "total_records": len(filtered_data),
        "filter_applied": bool(start_date or end_date),
        "date_range": {"start": start_date, "end": end_date}
    })

# Endpoint para obter análises dos dados
@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Obter dados (mesmo processo do endpoint anterior)
    service = get_sheets_service()
    if service:
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME
            ).execute()
            values = result.get("values", [])

            if not values:
                data = get_mock_data()
            else:
                headers = values[0] if values else []
                data = []
                for row in values[1:]:
                    row_dict = {}
                    for i, header in enumerate(headers):
                        if i < len(row):
                            clean_header = header.lower().replace(" ", "_").replace("?", "").replace("(", "").replace(")", "")
                            row_dict[clean_header] = row[i]
                    data.append(row_dict)
        except Exception as e:
            print(f"Erro ao buscar dados do Google Sheets: {e}")
            data = get_mock_data()
    else:
        data = get_mock_data()

    # Converter valores numéricos e formatar data
    for item in data:
        for key in ["quantos_leads_foram_trabalhados_hoje", "quantos_contatos_foram_realizados_hoje", 
                   "quantas_reunioes_foram_agendadas_hoje", "quantas_propostas_foram_enviadas_hoje", 
                   "quantas_vendas_foram_fechadas_hoje"]:
            if key in item and isinstance(item[key], str):
                try:
                    item[key] = int(item[key])
                except ValueError:
                    item[key] = 0
        # Converter o campo 'data' para o formato esperado (YYYY-MM-DD) para o frontend
        if "data" in item and isinstance(item["data"], str):
            try:
                item["data"] = datetime.strptime(item["data"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass # Manter o formato original se a conversão falhar

    filtered_data = filter_data_by_date(data, start_date, end_date)

    # Calcular métricas
    total_leads = sum(item.get("quantos_leads_foram_trabalhados_hoje", 0) for item in filtered_data)
    total_contatos = sum(item.get("quantos_contatos_foram_realizados_hoje", 0) for item in filtered_data)
    total_reunioes = sum(item.get("quantas_reunioes_foram_agendadas_hoje", 0) for item in filtered_data)
    total_propostas = sum(item.get("quantas_propostas_foram_enviadas_hoje", 0) for item in filtered_data)
    total_vendas = sum(item.get("quantas_vendas_foram_fechadas_hoje", 0) for item in filtered_data)
    
    # Taxa de conversão
    taxa_conversao_reuniao = (total_reunioes / total_leads) * 100 if total_leads > 0 else 0
    taxa_conversao_proposta = (total_propostas / total_reunioes) * 100 if total_reunioes > 0 else 0
    taxa_conversao_venda = (total_vendas / total_propostas) * 100 if total_propostas > 0 else 0

    # Análise por responsável
    responsaveis = {}
    for item in filtered_data:
        responsavel = item.get("nome_do_colaborador", "Não informado")
        if responsavel not in responsaveis:
            responsaveis[responsavel] = {
                "nome": responsavel,
                "leads_trabalhados": 0,
                "contatos_realizados": 0,
                "reunioes_agendadas": 0,
                "propostas_enviadas": 0,
                "vendas_fechadas": 0,
                "dias_trabalhados": 0
            }
        
        responsaveis[responsavel]["leads_trabalhados"] += item.get("quantos_leads_foram_trabalhados_hoje", 0)
        responsaveis[responsavel]["contatos_realizados"] += item.get("quantos_contatos_foram_realizados_hoje", 0)
        responsaveis[responsavel]["reunioes_agendadas"] += item.get("quantas_reunioes_foram_agendadas_hoje", 0)
        responsaveis[responsavel]["propostas_enviadas"] += item.get("quantas_propostas_foram_enviadas_hoje", 0)
        responsaveis[responsavel]["vendas_fechadas"] += item.get("quantas_vendas_foram_fechadas_hoje", 0)
        # Contar dias trabalhados de forma mais robusta (contar entradas únicas por dia)
        responsaveis[responsavel]["dias_trabalhados"] = len(set(d.get("data") for d in filtered_data if d.get("nome_do_colaborador") == responsavel))

    return jsonify({
        "success": True,
        "analytics": {
            "resumo": {
                "total_leads": total_leads,
                "total_contatos": total_contatos,
                "total_reunioes": total_reunioes,
                "total_propostas": total_propostas,
                "total_vendas": total_vendas,
                "taxa_conversao_reuniao": round(taxa_conversao_reuniao, 2),
                "taxa_conversao_proposta": round(taxa_conversao_proposta, 2),
                "taxa_conversao_venda": round(taxa_conversao_venda, 2)
            },
            "por_responsavel": list(responsaveis.values()),
            "periodo_analisado": len(set(item.get("data") for item in filtered_data)) # Contar dias únicos
        },
        "filter_applied": bool(start_date or end_date),
        "date_range": {"start": start_date, "end": end_date}
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

