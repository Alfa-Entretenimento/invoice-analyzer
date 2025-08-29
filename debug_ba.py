#!/usr/bin/env python3
"""Debug da nota da BA"""

from analisador_nf import AnalisadorNotaFiscal
import re

analisador = AnalisadorNotaFiscal()
texto = analisador.extrair_texto_pdf("NF 4 - EBAC - VENC 11.08.pdf")

print("="*50)
print("TEXTO EXTRAÍDO (primeiros 1000 caracteres):")
print("="*50)
print(texto[:1000])

print("\n" + "="*50)
print("PROCURANDO SALVADOR NO TEXTO:")
print("="*50)

if 'SALVADOR' in texto.upper():
    print("✓ Encontrou 'SALVADOR'")
    index = texto.upper().find('SALVADOR')
    print(f"Contexto: ...{texto[max(0, index-50):index+100]}...")
else:
    print("✗ Não encontrou 'SALVADOR'")
    
print("\n" + "="*50)
print("PROCURANDO VALOR TOTAL:")
print("="*50)

match = re.search(r'VALOR TOTAL.*?R\$\s*([\d\.,]+)', texto, re.IGNORECASE)
if match:
    print(f"✓ Encontrou valor total: {match.group()}")
else:
    print("✗ Não encontrou valor total")
    
print("\n" + "="*50) 
print("PROCURANDO VALORES DE ISS E RETENÇÕES:")
print("="*50)

# Procurar ISS
match = re.search(r'Valor do ISS.*?([\d\.,]+)', texto, re.IGNORECASE)
if match:
    print(f"✓ ISS encontrado: {match.group()}")