// Main JavaScript for NFS-e Analyzer

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeBtn = document.getElementById('removeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const exportBtn = document.getElementById('exportBtn');

// File variable
let selectedFile = null;

// Event Listeners
selectBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
removeBtn.addEventListener('click', removeFile);
analyzeBtn.addEventListener('click', analyzeFile);
newAnalysisBtn.addEventListener('click', resetInterface);
exportBtn.addEventListener('click', exportResults);

// Drag and Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// Click on upload area
uploadArea.addEventListener('click', (e) => {
    if (!e.target.closest('button') && !e.target.closest('.file-info')) {
        fileInput.click();
    }
});

// Functions
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    if (!file.type.includes('pdf')) {
        showError('Por favor, selecione apenas arquivos PDF');
        return;
    }
    
    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showError('Arquivo muito grande. Tamanho máximo: 16MB');
        return;
    }
    
    selectedFile = file;
    displayFile(file);
}

function displayFile(file) {
    fileName.textContent = file.name;
    fileInfo.style.display = 'inline-flex';
    uploadArea.classList.add('has-file');
    analyzeBtn.style.display = 'inline-block';
    
    // Hide upload instructions
    uploadArea.querySelector('.upload-icon').style.display = 'none';
    uploadArea.querySelector('h2').style.display = 'none';
    uploadArea.querySelector('p').style.display = 'none';
    selectBtn.style.display = 'none';
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.classList.remove('has-file');
    analyzeBtn.style.display = 'none';
    
    // Show upload instructions
    uploadArea.querySelector('.upload-icon').style.display = 'block';
    uploadArea.querySelector('h2').style.display = 'block';
    uploadArea.querySelector('p').style.display = 'block';
    selectBtn.style.display = 'inline-block';
}

function analyzeFile() {
    if (!selectedFile) {
        showError('Por favor, selecione um arquivo PDF');
        return;
    }
    
    // Hide upload section and show loading
    document.querySelector('.upload-section').style.display = 'none';
    loading.style.display = 'block';
    
    // Create FormData
    const formData = new FormData();
    formData.append('pdf', selectedFile);
    
    // Send to server
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        
        if (data.success) {
            displayResults(data.data);
        } else {
            showError(data.error || 'Erro ao analisar o arquivo');
        }
    })
    .catch(error => {
        loading.style.display = 'none';
        showError('Erro de conexão: ' + error.message);
    });
}

function displayResults(data) {
    resultsSection.style.display = 'block';
    
    // Tax Status
    const taxStatus = document.getElementById('taxStatus');
    taxStatus.className = 'tax-status ' + (data.tributado ? 'tributado' : 'nao-tributado');
    taxStatus.innerHTML = `
        <div class="tax-status-icon ${data.tributado ? 'success' : 'warning'}">
            <i class="fas fa-${data.tributado ? 'check-circle' : 'exclamation-triangle'}"></i>
        </div>
        <h2>Nota Fiscal ${data.tributado ? 'TRIBUTADA' : 'NÃO TRIBUTADA'}</h2>
        ${data.tributado ? `
            <div class="tax-details">
                <div class="tax-detail-item">
                    <div class="label">Valor do ISS</div>
                    <div class="value">${data.valor_iss}</div>
                </div>
                <div class="tax-detail-item">
                    <div class="label">Alíquota</div>
                    <div class="value">${data.aliquota_iss}%</div>
                </div>
            </div>
        ` : '<p>Esta nota fiscal não possui tributação de ISS</p>'}
    `;
    
    // General Info
    const generalInfo = document.getElementById('generalInfo');
    generalInfo.innerHTML = createInfoItems([
        { label: 'Número', value: data.numero, highlight: true },
        { label: 'Tipo', value: data.tipo_nf },
        { label: 'Estado', value: `${data.estado} ${getStateFlag(data.estado_sigla)}` },
        { label: 'Município', value: data.municipio },
        { label: 'Data Emissão', value: data.data_emissao },
        { label: 'Vencimento', value: data.vencimento },
        { label: 'Código Verificação', value: data.codigo_verificacao }
    ]);
    
    // Parties Info
    const partiesInfo = document.getElementById('partiesInfo');
    partiesInfo.innerHTML = createInfoItems([
        { label: 'Prestador', value: data.prestador },
        { label: 'Tomador', value: data.tomador }
    ]);
    
    // Tax Info
    const taxInfo = document.getElementById('taxInfo');
    taxInfo.innerHTML = createInfoItems([
        { label: 'Valor Total', value: data.valor_total, highlight: true },
        { label: 'Status', value: data.tributado ? 'Tributado' : 'Não Tributado' },
        { label: 'Valor ISS', value: data.valor_iss },
        { label: 'Alíquota ISS', value: data.aliquota_iss ? `${data.aliquota_iss}%` : '-' }
    ]);
    
    // Retention Info
    const retentionInfo = document.getElementById('retentionInfo');
    const retentions = [];
    for (const [key, value] of Object.entries(data.retencoes)) {
        retentions.push({
            label: `Retenção ${key.toUpperCase()}`,
            value: value
        });
    }
    retentionInfo.innerHTML = createInfoItems(retentions);
    
    // Observations
    if (data.observacoes && data.observacoes.length > 0) {
        const observations = document.getElementById('observations');
        const observationsList = document.getElementById('observationsList');
        observations.style.display = 'block';
        observationsList.innerHTML = data.observacoes
            .map(obs => `<li>${obs}</li>`)
            .join('');
    }
    
    // Store data for export
    window.analysisData = data;
}

function createInfoItems(items) {
    return items
        .filter(item => item.value && item.value !== 'Não informado')
        .map(item => `
            <div class="info-item">
                <span class="info-label">${item.label}</span>
                <span class="info-value ${item.highlight ? 'highlight' : ''}">${item.value}</span>
            </div>
        `)
        .join('');
}

function getStateFlag(sigla) {
    const flags = {
        'SP': '🏛️',
        'BA': '🌴',
        'RJ': '🏖️',
        'MG': '⛰️'
    };
    return flags[sigla] || '';
}

function showError(message) {
    loading.style.display = 'none';
    document.querySelector('.upload-section').style.display = 'none';
    resultsSection.style.display = 'none';
    errorMessage.style.display = 'block';
    errorText.textContent = message;
}

function resetInterface() {
    // Reset everything
    selectedFile = null;
    fileInput.value = '';
    removeFile();
    
    // Show upload section
    document.querySelector('.upload-section').style.display = 'block';
    
    // Hide other sections
    loading.style.display = 'none';
    resultsSection.style.display = 'none';
    errorMessage.style.display = 'none';
    
    // Clear observations
    document.getElementById('observations').style.display = 'none';
    
    // Scroll to top
    window.scrollTo(0, 0);
}

function exportResults() {
    if (!window.analysisData) return;
    
    const data = window.analysisData;
    const content = `
ANÁLISE DE NOTA FISCAL DE SERVIÇO ELETRÔNICA
=============================================

INFORMAÇÕES GERAIS
------------------
Número: ${data.numero}
Tipo: ${data.tipo_nf}
Estado: ${data.estado}
Município: ${data.municipio}
Data de Emissão: ${data.data_emissao}
Vencimento: ${data.vencimento}
Código de Verificação: ${data.codigo_verificacao}

PARTES ENVOLVIDAS
-----------------
Prestador: ${data.prestador}
Tomador: ${data.tomador}

VALORES E TRIBUTAÇÃO
--------------------
Valor Total: ${data.valor_total}
Status: ${data.tributado ? 'TRIBUTADO' : 'NÃO TRIBUTADO'}
Valor ISS: ${data.valor_iss}
Alíquota ISS: ${data.aliquota_iss}%

RETENÇÕES
---------
${Object.entries(data.retencoes).map(([key, value]) => `Retenção ${key.toUpperCase()}: ${value}`).join('\n')}

${data.observacoes && data.observacoes.length > 0 ? `
OBSERVAÇÕES
-----------
${data.observacoes.join('\n')}
` : ''}

Análise gerada em: ${new Date().toLocaleString('pt-BR')}
    `.trim();
    
    // Create and download file
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analise_nf_${data.numero}_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Show success message
    const btn = document.getElementById('exportBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check"></i> Exportado com Sucesso!';
    btn.classList.add('btn-success');
    
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.classList.remove('btn-success');
    }, 2000);
}

// Sample Data Demo (optional)
document.addEventListener('DOMContentLoaded', () => {
    // Check if there's a demo parameter
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('demo') === 'true') {
        loadSampleData();
    }
});

function loadSampleData() {
    loading.style.display = 'block';
    document.querySelector('.upload-section').style.display = 'none';
    
    fetch('/sample')
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            if (data.success) {
                displayResults(data.data);
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            console.error('Error loading sample data:', error);
        });
}