"""
Aplicação Flask para análise de Notas Fiscais
Interface web para upload e análise de NFS-e
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import tempfile
from analisador_nf_v2 import AnalisadorNotaFiscalV2, formatar_valor
from datetime import datetime
import json
from decimal import Decimal

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']

# Criar diretório temporário para uploads se não existir
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / 'nf_analyzer'
UPLOAD_FOLDER.mkdir(exist_ok=True)

class DecimalEncoder(json.JSONEncoder):
    """Encoder JSON customizado para lidar com Decimal"""
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

@app.route('/')
def index():
    """Página principal com formulário de upload"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint para análise de PDF"""
    try:
        # Verificar se arquivo foi enviado
        if 'pdf' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['pdf']
        
        # Verificar se arquivo foi selecionado
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verificar extensão
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Apenas arquivos PDF são aceitos'}), 400
        
        # Salvar arquivo temporariamente
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_path = UPLOAD_FOLDER / f"{timestamp}_{filename}"
        file.save(str(temp_path))
        
        try:
            # Analisar PDF com analisador V2
            analisador = AnalisadorNotaFiscalV2()
            nota = analisador.analisar(str(temp_path))
            
            # Preparar resposta
            resultado = {
                'success': True,
                'data': {
                    # Informações gerais
                    'numero': nota.numero,
                    'estado': nota.estado,
                    'municipio': nota.municipio,
                    'tipo_nf': nota.tipo_nf,
                    'data_emissao': nota.data_emissao,
                    'vencimento': nota.vencimento or 'Não informado',
                    'codigo_verificacao': nota.codigo_verificacao or 'Não informado',
                    
                    # Partes
                    'prestador': nota.prestador,
                    'tomador': nota.tomador,
                    
                    # Valores
                    'valor_total': formatar_valor(nota.valor_total),
                    'valor_total_raw': float(nota.valor_total),
                    
                    # Tributação
                    'tributado': nota.dados_tributarios.tributado,
                    'valor_iss': formatar_valor(nota.dados_tributarios.valor_iss),
                    'valor_iss_raw': float(nota.dados_tributarios.valor_iss) if nota.dados_tributarios.valor_iss else 0,
                    'aliquota_iss': float(nota.dados_tributarios.aliquota_iss) if nota.dados_tributarios.aliquota_iss else 0,
                    
                    # Retenções
                    'retencoes': {
                        'iss': formatar_valor(nota.dados_tributarios.retencao_iss),
                        'pis': formatar_valor(nota.dados_tributarios.retencao_pis),
                        'cofins': formatar_valor(nota.dados_tributarios.retencao_cofins),
                        'csll': formatar_valor(nota.dados_tributarios.retencao_csll),
                        'inss': formatar_valor(nota.dados_tributarios.retencao_inss),
                        'ir': formatar_valor(nota.dados_tributarios.retencao_ir),
                        'irrf': formatar_valor(nota.dados_tributarios.retencao_irrf) if hasattr(nota.dados_tributarios, 'retencao_irrf') else formatar_valor(None),
                    },
                    
                    # Informações adicionais
                    'confianca_extracao': nota.confianca_extracao,
                    'formato_detectado': nota.formato_detectado,
                    
                    # Observações
                    'observacoes': nota.dados_tributarios.observacoes
                }
            }
            
            # Identificar estado para bandeira
            estado_sigla = nota.estado.upper() if nota.estado not in ['DESCONHECIDO', 'ERRO_LEITURA'] else ''
            resultado['data']['estado_sigla'] = estado_sigla
            
            # Adicionar informações extras se disponíveis
            if nota.dados_tributarios.codigo_servico:
                resultado['data']['codigo_servico'] = nota.dados_tributarios.codigo_servico
            if nota.dados_tributarios.base_calculo:
                resultado['data']['base_calculo'] = formatar_valor(nota.dados_tributarios.base_calculo)
            if nota.dados_bancarios:
                resultado['data']['dados_bancarios'] = nota.dados_bancarios
            
            return jsonify(resultado)
            
        finally:
            # Limpar arquivo temporário
            if temp_path.exists():
                temp_path.unlink()
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao processar arquivo: {str(e)}'
        }), 500

@app.route('/sample')
def get_sample():
    """Retorna dados de exemplo para demonstração"""
    sample_data = {
        'success': True,
        'data': {
            'numero': '000004550',
            'estado': 'São Paulo',
            'estado_sigla': 'SP',
            'municipio': 'São Paulo',
            'tipo_nf': 'NFS-e São Paulo',
            'data_emissao': '01/08/2025',
            'vencimento': '11/08/2025',
            'codigo_verificacao': 'FEW7BLTA',
            'prestador': 'WEWORK SERVICOS DE ESCRITORIO LTDA.',
            'tomador': 'ALFA ENTRETENIMENTO S.A.',
            'valor_total': 'R$ 96.616,00',
            'valor_total_raw': 96616.00,
            'tributado': True,
            'valor_iss': 'R$ 4.830,80',
            'valor_iss_raw': 4830.80,
            'aliquota_iss': 5.0,
            'retencoes': {
                'iss': 'R$ 0,00',
                'pis': 'R$ 0,00',
                'cofins': 'R$ 0,00',
                'csll': 'R$ 0,00',
                'inss': 'R$ 0,00',
                'ir': 'R$ 0,00'
            },
            'observacoes': ['Tributado em São Paulo', 'ISS já recolhido']
        }
    }
    return jsonify(sample_data)

@app.errorhandler(413)
def too_large(e):
    """Handler para arquivos muito grandes"""
    return jsonify({'error': 'Arquivo muito grande. Máximo permitido: 16MB'}), 413

if __name__ == '__main__':
    print("\n🚀 Servidor Flask iniciando...")
    print("📍 Acesse: http://localhost:5001\n")
    app.run(debug=True, port=5001, host='127.0.0.1')