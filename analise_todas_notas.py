#!/usr/bin/env python3
"""
Script para analisar todas as notas e identificar padrões
"""

import os
import glob
import PyPDF2
import pdfplumber
from collections import defaultdict
import re

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um PDF usando múltiplas estratégias"""
    texto = ""
    
    # Tentar PyPDF2 primeiro
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto += texto_pagina + "\n"
    except Exception as e:
        print(f"  Erro PyPDF2: {e}")
    
    # Se não conseguiu texto suficiente, tentar pdfplumber
    if len(texto) < 100:
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto += texto_pagina + "\n"
        except Exception as e:
            print(f"  Erro pdfplumber: {e}")
    
    return texto

def identificar_estado(texto):
    """Tenta identificar o estado da nota fiscal"""
    texto_upper = texto.upper()
    
    # Padrões de identificação
    padroes = {
        'SP': ['SÃO PAULO', 'PREFEITURA DO MUNICÍPIO DE SÃO PAULO', 'SAO PAULO'],
        'RJ': ['RIO DE JANEIRO', 'PREFEITURA DA CIDADE DO RIO DE JANEIRO'],
        'MG': ['BELO HORIZONTE', 'MINAS GERAIS', 'PREFEITURA DE BELO HORIZONTE'],
        'BA': ['SALVADOR', 'BAHIA', 'PREFEITURA MUNICIPAL DO SALVADOR'],
        'PR': ['CURITIBA', 'PARANÁ', 'PREFEITURA MUNICIPAL DE CURITIBA'],
        'SC': ['FLORIANÓPOLIS', 'SANTA CATARINA', 'FLORIANOPOLIS'],
        'RS': ['PORTO ALEGRE', 'RIO GRANDE DO SUL'],
        'PE': ['RECIFE', 'PERNAMBUCO'],
        'CE': ['FORTALEZA', 'CEARÁ'],
        'GO': ['GOIÂNIA', 'GOIÁS', 'GOIANIA'],
        'DF': ['BRASÍLIA', 'DISTRITO FEDERAL', 'BRASILIA'],
        'ES': ['VITÓRIA', 'ESPÍRITO SANTO', 'VITORIA', 'ESPIRITO SANTO'],
        'MT': ['CUIABÁ', 'MATO GROSSO', 'CUIABA'],
        'MS': ['CAMPO GRANDE', 'MATO GROSSO DO SUL'],
        'PA': ['BELÉM', 'PARÁ', 'BELEM', 'PARA']
    }
    
    for estado, palavras in padroes.items():
        for palavra in palavras:
            if palavra in texto_upper:
                return estado
    
    return 'DESCONHECIDO'

def extrair_valor_iss(texto):
    """Tenta extrair o valor do ISS"""
    # Padrões comuns para ISS
    padroes = [
        r'Valor do ISS[:\s]*R?\$?\s*([\d\.,]+)',
        r'ISS[:\s]*R?\$?\s*([\d\.,]+)',
        r'Valor ISS[:\s]*R?\$?\s*([\d\.,]+)',
        r'Total ISS[:\s]*R?\$?\s*([\d\.,]+)',
        r'Imposto sobre Serviços[:\s]*R?\$?\s*([\d\.,]+)'
    ]
    
    for padrao in padroes:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            valor_str = match.group(1).replace('.', '').replace(',', '.')
            try:
                valor = float(valor_str)
                if valor > 0:
                    return valor
            except:
                pass
    
    return 0

def extrair_valor_total(texto):
    """Tenta extrair o valor total"""
    padroes = [
        r'VALOR TOTAL[^R$]*R?\$?\s*([\d\.,]+)',
        r'Total da Nota[:\s]*R?\$?\s*([\d\.,]+)',
        r'Valor Total dos Serviços[:\s]*R?\$?\s*([\d\.,]+)',
        r'Total Geral[:\s]*R?\$?\s*([\d\.,]+)',
        r'Total[:\s]*R?\$?\s*([\d\.,]+)'
    ]
    
    for padrao in padroes:
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            valor_str = match.group(1).replace('.', '').replace(',', '.')
            try:
                valor = float(valor_str)
                if valor > 0:
                    return valor
            except:
                pass
    
    return 0

def analisar_nota(caminho_pdf):
    """Analisa uma nota fiscal"""
    nome_arquivo = os.path.basename(caminho_pdf)
    print(f"\n📄 Analisando: {nome_arquivo}")
    
    texto = extrair_texto_pdf(caminho_pdf)
    
    if len(texto) < 50:
        print("  ⚠️  Não foi possível extrair texto do PDF")
        return {
            'arquivo': nome_arquivo,
            'estado': 'ERRO_LEITURA',
            'valor_total': 0,
            'valor_iss': 0,
            'tributado': False,
            'texto_extraido': len(texto) > 0
        }
    
    estado = identificar_estado(texto)
    valor_iss = extrair_valor_iss(texto)
    valor_total = extrair_valor_total(texto)
    
    print(f"  Estado: {estado}")
    print(f"  Valor Total: R$ {valor_total:,.2f}")
    print(f"  Valor ISS: R$ {valor_iss:,.2f}")
    print(f"  Tributado: {'SIM' if valor_iss > 0 else 'NÃO'}")
    
    return {
        'arquivo': nome_arquivo,
        'estado': estado,
        'valor_total': valor_total,
        'valor_iss': valor_iss,
        'tributado': valor_iss > 0,
        'texto_extraido': True
    }

def main():
    """Função principal"""
    print("="*60)
    print("🔍 ANÁLISE DE TODAS AS NOTAS FISCAIS")
    print("="*60)
    
    # Buscar todos os PDFs
    pdfs = []
    pdfs.extend(glob.glob('notas/*.pdf'))
    pdfs.extend(glob.glob('*.pdf'))
    
    # Filtrar apenas notas fiscais
    pdfs = [pdf for pdf in pdfs if 'NF' in os.path.basename(pdf).upper()]
    
    print(f"\n📊 Total de notas encontradas: {len(pdfs)}")
    
    # Analisar todas
    resultados = []
    estados_encontrados = defaultdict(int)
    
    for pdf in sorted(pdfs):
        resultado = analisar_nota(pdf)
        resultados.append(resultado)
        estados_encontrados[resultado['estado']] += 1
    
    # Resumo
    print("\n" + "="*60)
    print("📈 RESUMO DA ANÁLISE")
    print("="*60)
    
    print("\n🏛️ ESTADOS ENCONTRADOS:")
    for estado, quantidade in sorted(estados_encontrados.items()):
        if estado != 'ERRO_LEITURA':
            print(f"  {estado}: {quantidade} nota(s)")
    
    if 'ERRO_LEITURA' in estados_encontrados:
        print(f"\n⚠️  Notas com erro de leitura: {estados_encontrados['ERRO_LEITURA']}")
    
    # Estatísticas de tributação
    tributadas = sum(1 for r in resultados if r['tributado'])
    nao_tributadas = len(resultados) - tributadas
    
    print(f"\n💰 TRIBUTAÇÃO:")
    print(f"  Tributadas: {tributadas}")
    print(f"  Não tributadas: {nao_tributadas}")
    
    # Valor total
    valor_total_geral = sum(r['valor_total'] for r in resultados)
    valor_iss_total = sum(r['valor_iss'] for r in resultados)
    
    print(f"\n📊 VALORES TOTAIS:")
    print(f"  Valor Total das Notas: R$ {valor_total_geral:,.2f}")
    print(f"  ISS Total: R$ {valor_iss_total:,.2f}")
    
    # Salvar relatório
    with open('relatorio_analise.txt', 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DE ANÁLISE DE NOTAS FISCAIS\n")
        f.write("="*50 + "\n\n")
        
        for r in resultados:
            f.write(f"Arquivo: {r['arquivo']}\n")
            f.write(f"Estado: {r['estado']}\n")
            f.write(f"Valor Total: R$ {r['valor_total']:,.2f}\n")
            f.write(f"Valor ISS: R$ {r['valor_iss']:,.2f}\n")
            f.write(f"Tributado: {'SIM' if r['tributado'] else 'NÃO'}\n")
            f.write("-"*30 + "\n")
    
    print(f"\n✅ Relatório salvo em: relatorio_analise.txt")
    
    return resultados

if __name__ == "__main__":
    main()