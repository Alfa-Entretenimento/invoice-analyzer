#!/usr/bin/env python3
"""
Script para analisar PDFs específicos que não foram identificados corretamente
Analisa NF 17 - M4X e NF 282 - JNTO AD.EZ
"""

import PyPDF2
import pdfplumber
import re
from pathlib import Path

def extrair_com_pypdf2(caminho_pdf):
    """Extrai texto usando PyPDF2"""
    try:
        with open(caminho_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto = ""
            for page in reader.pages:
                texto += page.extract_text() + "\n"
        return texto
    except Exception as e:
        return f"Erro PyPDF2: {e}"

def extrair_com_pdfplumber(caminho_pdf):
    """Extrai texto usando pdfplumber"""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += page.extract_text() + "\n"
        return texto
    except Exception as e:
        return f"Erro pdfplumber: {e}"

def analisar_padroes_sp(texto, nome_arquivo):
    """Analisa padrões específicos de São Paulo"""
    print(f"\n{'='*60}")
    print(f"ANÁLISE DE PADRÕES: {nome_arquivo}")
    print(f"{'='*60}")
    
    # 1. Identificação do Estado/Município
    if "PREFEITURA DO MUNICÍPIO DE SÃO PAULO" in texto:
        print("✓ ESTADO/MUNICÍPIO: São Paulo - SP")
    
    # 2. Número da Nota
    numero_nota = re.search(r'Número da Nota\s*(\d+)', texto)
    if numero_nota:
        print(f"✓ NÚMERO DA NOTA: {numero_nota.group(1)}")
    
    # 3. Data de Emissão
    data_emissao = re.search(r'Data e Hora de Emissão\s*(\d{2}/\d{2}/\d{4})', texto)
    if data_emissao:
        print(f"✓ DATA DE EMISSÃO: {data_emissao.group(1)}")
    
    # 4. Prestador de Serviços
    prestador = re.search(r'PRESTADOR DE SERVIÇOS.*?Nome/Razão Social:\s*([^\n]+)', texto, re.DOTALL)
    if prestador:
        print(f"✓ PRESTADOR: {prestador.group(1).strip()}")
    
    # 5. CNPJ do Prestador
    cnpj_prestador = re.search(r'CPF/CNPJ:\s*([\d\./\-]+)', texto)
    if cnpj_prestador:
        print(f"✓ CNPJ PRESTADOR: {cnpj_prestador.group(1)}")
    
    # 6. Tomador de Serviços
    tomador_match = re.search(r'TOMADOR DE SERVIÇOS.*?Nome/Razão Social:\s*([^\n]+)', texto, re.DOTALL)
    if tomador_match:
        print(f"✓ TOMADOR: {tomador_match.group(1).strip()}")
    
    # 7. Valor Total
    valor_total = re.search(r'VALOR TOTAL DO SERVIÇO = R\$ ([\d.,]+)', texto)
    if valor_total:
        valor = valor_total.group(1).replace('.', '').replace(',', '.')
        print(f"✓ VALOR TOTAL: R$ {valor}")
    
    # 8. Valor do ISS
    valor_iss = re.search(r'Valor do ISS \(R\$\)\s*([\d.,]+)', texto)
    if valor_iss:
        iss = valor_iss.group(1).replace('.', '').replace(',', '.')
        print(f"✓ VALOR ISS: R$ {iss}")
    
    # 9. Alíquota
    aliquota = re.search(r'Alíquota \(%\)\s*([\d.,]+)', texto)
    if aliquota:
        print(f"✓ ALÍQUOTA: {aliquota.group(1)}%")
    
    # 10. Base de Cálculo
    base_calculo = re.search(r'Base de Cálculo \(R\$\)\s*([\d.,]+)', texto)
    if base_calculo:
        base = base_calculo.group(1).replace('.', '').replace(',', '.')
        print(f"✓ BASE DE CÁLCULO: R$ {base}")
    
    # 11. Código do Serviço
    codigo_servico = re.search(r'Código do Serviço\s*(\d+)', texto)
    if codigo_servico:
        print(f"✓ CÓDIGO DO SERVIÇO: {codigo_servico.group(1)}")
    
    # 12. Descrição do Serviço
    descricao = re.search(r'DISCRIMINAÇÃO DOS SERVIÇOS\s*([^V]+?)(?=VALOR TOTAL|$)', texto, re.DOTALL)
    if descricao:
        desc_limpa = ' '.join(descricao.group(1).strip().split())
        print(f"✓ DESCRIÇÃO: {desc_limpa[:200]}...")
    
    # 13. Vencimento
    vencimento = re.search(r'Vencimento:\s*(\d{2}/\d{2}/\d{4})', texto)
    if vencimento:
        print(f"✓ VENCIMENTO: {vencimento.group(1)}")
    
    print("\n" + "-"*60)
    print("PADRÕES ÚNICOS ENCONTRADOS:")
    print("-"*60)
    
    # Buscar padrões específicos
    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        if 'VALOR TOTAL DO SERVIÇO' in linha:
            print(f"Linha {i}: {linha.strip()}")
        if 'Base de Cálculo' in linha:
            print(f"Linha {i}: {linha.strip()}")
        if 'Alíquota' in linha:
            print(f"Linha {i}: {linha.strip()}")
        if 'ISS' in linha and 'R$' in linha:
            print(f"Linha {i}: {linha.strip()}")

def main():
    arquivos = [
        '/Users/fabiowill/GabrielNF/notas/NF 17 - M4X - PJ - VENC 01.08.pdf',
        '/Users/fabiowill/GabrielNF/notas/NF 282 - JNTO AD.EZ - VENC 25.08.pdf'
    ]
    
    for arquivo in arquivos:
        if not Path(arquivo).exists():
            print(f"❌ Arquivo não encontrado: {arquivo}")
            continue
            
        nome_arquivo = Path(arquivo).name
        print(f"\n{'='*80}")
        print(f"PROCESSANDO: {nome_arquivo}")
        print(f"{'='*80}")
        
        # Extrair com PyPDF2
        print("\n📄 EXTRAÇÃO COM PyPDF2:")
        texto_pypdf2 = extrair_com_pypdf2(arquivo)
        if not texto_pypdf2.startswith("Erro"):
            print(f"✓ Texto extraído com sucesso ({len(texto_pypdf2)} caracteres)")
            analisar_padroes_sp(texto_pypdf2, f"{nome_arquivo} - PyPDF2")
        else:
            print(f"❌ {texto_pypdf2}")
        
        # Extrair com pdfplumber
        print(f"\n📄 EXTRAÇÃO COM pdfplumber:")
        texto_pdfplumber = extrair_com_pdfplumber(arquivo)
        if not texto_pdfplumber.startswith("Erro"):
            print(f"✓ Texto extraído com sucesso ({len(texto_pdfplumber)} caracteres)")
            analisar_padroes_sp(texto_pdfplumber, f"{nome_arquivo} - pdfplumber")
            
            # Salvar texto extraído para análise manual
            arquivo_texto = f"/Users/fabiowill/GabrielNF/debug_{nome_arquivo.replace(' ', '_').replace('.pdf', '.txt')}"
            with open(arquivo_texto, 'w', encoding='utf-8') as f:
                f.write(f"ARQUIVO: {nome_arquivo}\n")
                f.write("="*80 + "\n")
                f.write("TEXTO EXTRAÍDO COM pdfplumber:\n")
                f.write("="*80 + "\n")
                f.write(texto_pdfplumber)
            print(f"💾 Texto salvo em: {arquivo_texto}")
        else:
            print(f"❌ {texto_pdfplumber}")

if __name__ == "__main__":
    main()