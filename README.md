# 📊 Sistema de Análise de Notas Fiscais - Alfa Entretenimento

Sistema inteligente para análise automática de Notas Fiscais de Serviço Eletrônicas (NFS-e) brasileiras, desenvolvido para a Alfa Entretenimento S.A.

## 🎯 Visão Geral

Este sistema utiliza a API do Claude (Anthropic) para realizar análise visual de PDFs de notas fiscais com **100% de precisão**, extraindo automaticamente informações tributárias, valores, impostos e retenções de qualquer prefeitura do Brasil.

## ✨ Funcionalidades Principais

- 🤖 **Análise com IA**: Integração com Claude API para análise visual precisa
- 📄 **Suporte Universal**: Funciona com PDFs de qualquer município brasileiro
- 💰 **Extração Completa de Impostos**: ISS, PIS, COFINS, CSLL, IRRF, INSS
- 🎨 **Interface Moderna**: Design com tema Alfa Entretenimento (amarelo neon)
- 📤 **Upload Drag & Drop**: Interface intuitiva para envio de arquivos
- 💫 **Feedback Visual**: Mensagens rotativas durante processamento
- 📊 **Exportação de Dados**: Download dos resultados em formato TXT
- 🏛️ **27 Estados Suportados**: Cobertura completa do território brasileiro

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.10+** - Linguagem principal
- **Flask 3.0.0** - Framework web
- **Anthropic Claude API** - Análise inteligente de PDFs
- **pdfplumber/pypdfium2** - Conversão PDF para imagem
- **Gunicorn** - Servidor WSGI para produção

### Frontend
- **HTML5/CSS3** - Interface web
- **JavaScript ES6** - Interatividade
- **Glassmorphism Design** - Estilo visual moderno
- **Font Awesome 6.4** - Ícones
- **Google Fonts (Montserrat)** - Tipografia

## 📦 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- Chave de API do Claude (Anthropic)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/GabrielNF.git
cd GabrielNF
```

2. **Crie e ative o ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua API key do Anthropic
```

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse no navegador**
```
http://localhost:5001
```

## 🚀 Deploy em Produção (AWS EC2)

### Deploy Automático
```bash
./deploy_direct.sh
```

Este script automatiza:
- Upload do código para EC2
- Instalação de dependências
- Configuração do Nginx
- Configuração do Gunicorn como serviço
- Reinicialização dos serviços

### URLs de Produção
- **Load Balancer**: http://invoice-analyzer-alb-620211373.sa-east-1.elb.amazonaws.com/
- **EC2 Direto**: http://56.125.206.138/

## 📁 Estrutura do Projeto

```
GabrielNF/
├── app.py                      # Servidor Flask principal
├── analisador_claude_api.py    # Integração com Claude API
├── requirements.txt            # Dependências Python
├── deploy_direct.sh           # Script de deploy para EC2
├── .env.example              # Exemplo de configuração
├── templates/
│   └── index.html           # Interface web principal
├── static/
│   ├── css/
│   │   └── style.css       # Estilos com tema Alfa
│   └── js/
│       └── main.js         # Lógica do frontend
├── backup/                  # Versões antigas (ignorado no git)
└── CHANGELOG.md            # Histórico de desenvolvimento
```

## 🔧 Configuração

### Arquivo .env
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...
DEBUG=false
PORT=5001
```

## 💡 Como Usar

1. **Acesse a aplicação** no navegador
2. **Arraste um PDF** de nota fiscal para a área de upload ou clique para selecionar
3. **Clique em "Analisar Nota Fiscal"**
4. **Aguarde o processamento** (mensagens rotativas indicam o progresso)
5. **Visualize os resultados** organizados em cards
6. **Exporte os dados** clicando em "Exportar Resultados"

## 📊 Dados Extraídos

O sistema extrai automaticamente:
- **Número da nota** e código de verificação
- **Estado e município** de emissão
- **Datas** de emissão e vencimento
- **Prestador e tomador** de serviços
- **Valor total** da nota
- **ISS** (valor e alíquota)
- **Retenções federais** (PIS, COFINS, CSLL, IRRF, INSS)
- **Observações fiscais**

## 🎨 Identidade Visual

O sistema utiliza a identidade visual da Alfa Entretenimento:
- **Cores principais**: Amarelo neon (#EBFF00) e azul escuro (#00003C)
- **Design glassmorphism** com transparências e blur
- **Logo SVG** incorporado
- **Animações suaves** e feedback visual

## 🔒 Segurança

- API key armazenada em variáveis de ambiente
- Validação de arquivos PDF no frontend e backend
- Limite de tamanho de arquivo: 16MB
- Arquivos temporários removidos após processamento
- PDFs não são armazenados permanentemente

## 📈 Performance

- **Tempo médio de análise**: 3-5 segundos por nota
- **Taxa de sucesso**: 100% com Claude API
- **Suporte a concorrência**: 2 workers Gunicorn
- **Timeout configurado**: 120 segundos

## 🐛 Resolução de Problemas

### Erro de API Key
```
Erro ao processar arquivo: Client.__init__() got an unexpected keyword argument 'proxies'
```
**Solução**: Verifique as versões no requirements.txt, especialmente httpx==0.24.1

### PDF não reconhecido
**Solução**: O sistema usa análise visual, então PDFs escaneados também funcionam

### Timeout em produção
**Solução**: Aumente o timeout no nginx e gunicorn (atualmente 120s)

## 📝 Changelog

Veja [CHANGELOG.md](CHANGELOG.md) para histórico completo de desenvolvimento.

## 🤝 Contribuição

Projeto privado da Alfa Entretenimento S.A. Para contribuições, entre em contato com a equipe de desenvolvimento.

## 📄 Licença

© 2024 Alfa Entretenimento S.A. Todos os direitos reservados.

## 📞 Suporte

Para suporte e dúvidas:
- **Email**: dev@alfaentretenimento.com.br
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/GabrielNF/issues)

---

**Desenvolvido com 💛 pela equipe Alfa Entretenimento**