const express = require('express');
const cors = require('cors');
const { google } = require('googleapis');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Configurações do Google Sheets
const SPREADSHEET_ID = '1JstbxuG7JG4EMHHzcT9UZtJihkXlEz09gZza1vShJWk';
const RANGE_NAME = 'Data!A:M';

// Credenciais de Service Account (configurar via variáveis de ambiente)
const SERVICE_ACCOUNT_INFO = {
    type: "service_account",
    project_id: "mirai-dashboard-project",
    private_key_id: process.env.GOOGLE_PRIVATE_KEY_ID || "key_id_placeholder",
    private_key: (process.env.GOOGLE_PRIVATE_KEY || "-----BEGIN PRIVATE KEY-----\nkey_placeholder\n-----END PRIVATE KEY-----\n").replace(/\\n/g, '\n'),
    client_email: process.env.GOOGLE_CLIENT_EMAIL || "mirai-dashboard@mirai-dashboard-project.iam.gserviceaccount.com",
    client_id: process.env.GOOGLE_CLIENT_ID || "client_id_placeholder",
    auth_uri: "https://accounts.google.com/o/oauth2/auth",
    token_uri: "https://oauth2.googleapis.com/token",
    auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
    client_x509_cert_url: `https://www.googleapis.com/robot/v1/metadata/x509/${encodeURIComponent(process.env.GOOGLE_CLIENT_EMAIL || "mirai-dashboard@mirai-dashboard-project.iam.gserviceaccount.com")}`
};

// Função para inicializar o serviço do Google Sheets
async function getSheetsService() {
    try {
        // Para desenvolvimento, vamos usar dados mock
        // Em produção, descomente as linhas abaixo e configure as credenciais
        /*
        const auth = new google.auth.GoogleAuth({
            credentials: SERVICE_ACCOUNT_INFO,
            scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly']
        });
        
        const sheets = google.sheets({ version: 'v4', auth });
        return sheets;
        */
        return null;
    } catch (error) {
        console.error('Erro ao inicializar serviço Google Sheets:', error);
        return null;
    }
}

// Dados mock para desenvolvimento
function getMockData() {
    return [
        {
            data: '2024-10-01',
            vendedor: 'João Silva',
            cliente: 'Empresa A',
            produto: 'Produto X',
            valor: 1500.00,
            status: 'Fechado',
            origem: 'Website',
            regiao: 'Sudeste',
            categoria: 'Premium',
            descricao: 'Venda de produto premium',
            observacoes: 'Cliente satisfeito',
            meta_mensal: 50000,
            comissao: 150.00
        },
        {
            data: '2024-10-02',
            vendedor: 'Maria Santos',
            cliente: 'Empresa B',
            produto: 'Produto Y',
            valor: 2300.00,
            status: 'Em Negociação',
            origem: 'Indicação',
            regiao: 'Sul',
            categoria: 'Standard',
            descricao: 'Proposta em análise',
            observacoes: 'Aguardando aprovação',
            meta_mensal: 45000,
            comissao: 230.00
        },
        {
            data: '2024-10-03',
            vendedor: 'Carlos Oliveira',
            cliente: 'Empresa C',
            produto: 'Produto Z',
            valor: 800.00,
            status: 'Perdido',
            origem: 'Cold Call',
            regiao: 'Norte',
            categoria: 'Basic',
            descricao: 'Cliente optou por concorrente',
            observacoes: 'Preço foi o fator decisivo',
            meta_mensal: 40000,
            comissao: 0.00
        },
        {
            data: '2024-10-04',
            vendedor: 'Ana Costa',
            cliente: 'Empresa D',
            produto: 'Produto X',
            valor: 3200.00,
            status: 'Fechado',
            origem: 'Redes Sociais',
            regiao: 'Nordeste',
            categoria: 'Premium',
            descricao: 'Venda de grande porte',
            observacoes: 'Cliente fidelizado',
            meta_mensal: 55000,
            comissao: 320.00
        },
        {
            data: '2024-10-05',
            vendedor: 'Pedro Lima',
            cliente: 'Empresa E',
            produto: 'Produto Y',
            valor: 1800.00,
            status: 'Em Negociação',
            origem: 'Website',
            regiao: 'Centro-Oeste',
            categoria: 'Standard',
            descricao: 'Proposta personalizada',
            observacoes: 'Reunião agendada',
            meta_mensal: 42000,
            comissao: 180.00
        },
        // Dados adicionais para teste de filtros
        {
            data: '2024-09-28',
            vendedor: 'João Silva',
            cliente: 'Empresa F',
            produto: 'Produto Z',
            valor: 2100.00,
            status: 'Fechado',
            origem: 'Website',
            regiao: 'Sudeste',
            categoria: 'Standard',
            descricao: 'Venda recorrente',
            observacoes: 'Cliente antigo',
            meta_mensal: 50000,
            comissao: 210.00
        },
        {
            data: '2024-09-25',
            vendedor: 'Maria Santos',
            cliente: 'Empresa G',
            produto: 'Produto X',
            valor: 4500.00,
            status: 'Fechado',
            origem: 'Indicação',
            regiao: 'Sul',
            categoria: 'Premium',
            descricao: 'Grande contrato',
            observacoes: 'Negociação longa',
            meta_mensal: 45000,
            comissao: 450.00
        }
    ];
}

// Função para filtrar dados por intervalo de datas
function filterDataByDate(data, startDate, endDate) {
    if (!startDate && !endDate) {
        return data;
    }
    
    return data.filter(item => {
        const itemDate = new Date(item.data);
        
        if (startDate && !endDate) {
            return itemDate >= new Date(startDate);
        } else if (endDate && !startDate) {
            return itemDate <= new Date(endDate);
        } else if (startDate && endDate) {
            return itemDate >= new Date(startDate) && itemDate <= new Date(endDate);
        }
        
        return true;
    });
}

// Endpoint para obter dados da planilha
app.get('/api/data', async (req, res) => {
    try {
        const { start_date, end_date } = req.query;
        
        // const sheets = await getSheetsService();
        // if (sheets) {
        //     // Código para buscar dados reais do Google Sheets
        //     const response = await sheets.spreadsheets.values.get({
        //         spreadsheetId: SPREADSHEET_ID,
        //         range: RANGE_NAME,
        //     });
        //     const values = response.data.values;
        //     // Processar dados reais aqui
        // } else {
        //     // Usar dados mock para desenvolvimento
        // }
        
        const allData = getMockData();
        const filteredData = filterDataByDate(allData, start_date, end_date);
        
        res.json({
            success: true,
            data: filteredData,
            total_records: filteredData.length,
            filter_applied: !!(start_date || end_date),
            date_range: {
                start: start_date,
                end: end_date
            }
        });
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Endpoint para obter análises dos dados
app.get('/api/analytics', async (req, res) => {
    try {
        const { start_date, end_date } = req.query;
        
        const allData = getMockData();
        const data = filterDataByDate(allData, start_date, end_date);
        
        // Calcular métricas
        const totalVendas = data
            .filter(item => item.status === 'Fechado')
            .reduce((sum, item) => sum + item.valor, 0);
        
        const totalOportunidades = data.length;
        const vendasFechadas = data.filter(item => item.status === 'Fechado').length;
        const taxaConversao = totalOportunidades > 0 ? (vendasFechadas / totalOportunidades) * 100 : 0;
        
        // Análise por vendedor
        const vendedores = {};
        data.forEach(item => {
            const vendedor = item.vendedor;
            if (!vendedores[vendedor]) {
                vendedores[vendedor] = {
                    nome: vendedor,
                    total_vendas: 0,
                    vendas_fechadas: 0,
                    oportunidades: 0,
                    comissao_total: 0
                };
            }
            
            vendedores[vendedor].oportunidades += 1;
            vendedores[vendedor].comissao_total += item.comissao;
            
            if (item.status === 'Fechado') {
                vendedores[vendedor].total_vendas += item.valor;
                vendedores[vendedor].vendas_fechadas += 1;
            }
        });
        
        // Análise por região
        const regioes = {};
        data.forEach(item => {
            const regiao = item.regiao;
            if (!regioes[regiao]) {
                regioes[regiao] = {
                    nome: regiao,
                    total_vendas: 0,
                    oportunidades: 0
                };
            }
            
            regioes[regiao].oportunidades += 1;
            if (item.status === 'Fechado') {
                regioes[regiao].total_vendas += item.valor;
            }
        });
        
        res.json({
            success: true,
            analytics: {
                resumo: {
                    total_vendas: totalVendas,
                    total_oportunidades: totalOportunidades,
                    vendas_fechadas: vendasFechadas,
                    taxa_conversao: Math.round(taxaConversao * 100) / 100
                },
                por_vendedor: Object.values(vendedores),
                por_regiao: Object.values(regioes)
            },
            filter_applied: !!(start_date || end_date),
            date_range: {
                start: start_date,
                end: end_date
            }
        });
    } catch (error) {
        console.error('Erro ao buscar análises:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Endpoint de health check
app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString()
    });
});

// Iniciar servidor
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});

module.exports = app;
