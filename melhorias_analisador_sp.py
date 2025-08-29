#!/usr/bin/env python3
"""
Melhorias específicas para o analisador de São Paulo
Baseado na análise dos PDFs NF 17 - M4X e NF 282 - JNTO AD.EZ
"""

import re
from decimal import Decimal
from typing import Dict, Optional, List

def extrair_valor_sp_melhorado(texto: str, campo: str) -> Optional[Decimal]:
    """
    Extração melhorada de valores para São Paulo
    """
    patterns = {
        'valor_total': [
            r'VALOR TOTAL DO SERVIÇO = R\$ ([\d.,]+)',
            r'Valor Total.*?R\$ ([\d.,]+)',
        ],
        'valor_iss': [
            r'Valor do ISS \(R\$\)\s*([\d.,]+)',
            r'ISS.*?R\$\s*([\d.,]+)',
            # Padrão em tabela: buscar o 4º valor após "Valor do ISS"
            r'Valor do ISS.*?(?:R\$\s*[\d.,]+.*?){3}R\$\s*([\d.,]+)',
        ],
        'aliquota': [
            r'Alíquota \(%\)\s*([\d.,]+)',
            r'(\d+[,.]?\d*)\s*%',
        ],
        'base_calculo': [
            r'Base de Cálculo \(R\$\)\s*([\d.,]+)',
            r'Base.*?R\$\s*([\d.,]+)',
        ]
    }
    
    if campo not in patterns:
        return None
    
    for pattern in patterns[campo]:
        match = re.search(pattern, texto, re.IGNORECASE | re.MULTILINE)
        if match:
            try:
                valor_str = match.group(1).replace('.', '').replace(',', '.')
                return Decimal(valor_str)
            except:
                continue
    
    return None

def extrair_codigo_verificacao_sp(texto: str) -> Optional[str]:
    """
    Extrai código de verificação de São Paulo
    Formato: XXXX-XXXX (alfanumérico)
    """
    patterns = [
        r'Código de Verificação\s*([A-Z0-9]{4}-[A-Z0-9]{4})',
        r'Código.*?([A-Z0-9]{4}-[A-Z0-9]{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, texto, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def extrair_vencimento_sp(texto: str) -> Optional[str]:
    """
    Extrai vencimento de São Paulo
    Pode estar na discriminação dos serviços
    """
    patterns = [
        r'(?:Vencimento|VENCIMENTO):\s*(\d{2}/\d{2}/\d{4})',
        r'VENC[A-Z]*\s+(\d{2}/\d{2}/\d{4})',
        r'venc[a-z]*\s+(\d{2}/\d{2}/\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, texto, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def extrair_dados_bancarios_sp(texto: str) -> Dict[str, str]:
    """
    Extrai dados bancários de São Paulo
    Podem estar na discriminação dos serviços
    """
    dados = {}
    
    # Banco
    banco_match = re.search(r'BANCO:\s*([^(\n]+)', texto, re.IGNORECASE)
    if banco_match:
        dados['banco'] = banco_match.group(1).strip()
    
    # Agência
    ag_match = re.search(r'AG:\s*(\d+)', texto, re.IGNORECASE)
    if ag_match:
        dados['agencia'] = ag_match.group(1)
    
    # Conta Corrente
    cc_match = re.search(r'CC:\s*([\d\-]+)', texto, re.IGNORECASE)
    if cc_match:
        dados['conta'] = cc_match.group(1)
    
    return dados

def extrair_tributos_federais_sp(texto: str) -> Dict[str, Optional[Decimal]]:
    """
    Extrai tributos federais específicos de São Paulo
    IRRF, CSLL, COFINS, PIS/PASEP
    """
    tributos = {}
    
    patterns = {
        'irrf': r'IRRF.*?(\d+[.,]\d+)',
        'csll': r'CSLL.*?(\d+[.,]\d+)',
        'cofins': r'COFINS.*?(\d+[.,]\d+)',
        'pis': r'PIS(?:/PASEP)?.*?(\d+[.,]\d+)',
    }
    
    for tributo, pattern in patterns.items():
        match = re.search(pattern, texto, re.IGNORECASE)
        if match:
            try:
                valor_str = match.group(1).replace('.', '').replace(',', '.')
                tributos[tributo] = Decimal(valor_str)
            except:
                tributos[tributo] = None
        else:
            tributos[tributo] = None
    
    return tributos

def identificar_codigo_servico_sp(texto: str) -> Dict[str, str]:
    """
    Identifica código e descrição do serviço
    """
    resultado = {}
    
    # Código do serviço
    codigo_match = re.search(r'Código do Serviço\s*(\d+)', texto)
    if codigo_match:
        resultado['codigo'] = codigo_match.group(1)
    
    # Descrição específica baseada no código
    codigos_conhecidos = {
        '03116': 'Assessoria ou consultoria de qualquer natureza',
        '02496': 'Propaganda e publicidade, promoção de vendas'
    }
    
    if 'codigo' in resultado and resultado['codigo'] in codigos_conhecidos:
        resultado['descricao'] = codigos_conhecidos[resultado['codigo']]
    
    return resultado

def analisar_sp_melhorado(texto: str) -> Dict:
    """
    Análise melhorada para São Paulo baseada nos padrões identificados
    """
    resultado = {
        'estado': 'SP',
        'municipio': 'São Paulo',
        'valores': {},
        'tributos': {},
        'dados_adicionais': {}
    }
    
    # Valores principais
    resultado['valores']['valor_total'] = extrair_valor_sp_melhorado(texto, 'valor_total')
    resultado['valores']['valor_iss'] = extrair_valor_sp_melhorado(texto, 'valor_iss')
    resultado['valores']['aliquota'] = extrair_valor_sp_melhorado(texto, 'aliquota')
    resultado['valores']['base_calculo'] = extrair_valor_sp_melhorado(texto, 'base_calculo')
    
    # Tributos federais
    resultado['tributos'] = extrair_tributos_federais_sp(texto)
    
    # Dados adicionais
    resultado['dados_adicionais']['codigo_verificacao'] = extrair_codigo_verificacao_sp(texto)
    resultado['dados_adicionais']['vencimento'] = extrair_vencimento_sp(texto)
    resultado['dados_adicionais']['dados_bancarios'] = extrair_dados_bancarios_sp(texto)
    resultado['dados_adicionais']['servico'] = identificar_codigo_servico_sp(texto)
    
    # Status de tributação
    tributado = False
    if resultado['valores']['valor_iss'] and resultado['valores']['valor_iss'] > 0:
        tributado = True
    
    resultado['tributado'] = tributado
    
    return resultado

def main():
    """
    Teste das melhorias com exemplos dos PDFs analisados
    """
    print("="*60)
    print("TESTE DAS MELHORIAS PARA SÃO PAULO")
    print("="*60)
    
    # Exemplo 1: NF M4X
    texto_m4x = """
    VALOR TOTAL DO SERVIÇO = R$ 69.888,00
    Base de Cálculo (R$) 69.888,00
    Alíquota (%) 5,00%
    Valor do ISS (R$) 3.494,40
    Código de Verificação 2RED-BDYN
    Código do Serviço 03116
    Vencimento: 07/08/2025
    IRRF 1.048,32
    CSLL 698,88
    COFINS 2.096,64
    PIS/PASEP 454,27
    """
    
    print("\n📋 TESTE 1: NF M4X")
    resultado_m4x = analisar_sp_melhorado(texto_m4x)
    for categoria, dados in resultado_m4x.items():
        print(f"• {categoria.upper()}: {dados}")
    
    # Exemplo 2: NF JNTO AD.EZ
    texto_jnto = """
    VALOR TOTAL DO SERVIÇO = R$ 15.620,00
    Base de Cálculo (R$) 15.620,00
    Alíquota (%) 5,00%
    Valor do ISS (R$) 781,00
    Código de Verificação LUJB-BQE8
    Código do Serviço 02496
    BANCO: Santander (033)
    AG: 2006
    CC: 13002021-7
    VENCIMENTO: 18/08/2025
    """
    
    print("\n📋 TESTE 2: NF JNTO AD.EZ")
    resultado_jnto = analisar_sp_melhorado(texto_jnto)
    for categoria, dados in resultado_jnto.items():
        print(f"• {categoria.upper()}: {dados}")

if __name__ == "__main__":
    main()