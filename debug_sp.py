#!/usr/bin/env python3
"""Debug da nota de SP"""

from analisador_nf import AnalisadorNotaFiscal
import re
from decimal import Decimal

analisador = AnalisadorNotaFiscal()
texto = analisador.extrair_texto_pdf("NF 4550 - WEWORK - VENC 11.08.pdf")

print("="*50)
print("PROCURANDO ISS NA LINHA:")
print("="*50)

# Procurar a linha específica
linhas = texto.split('\n')
for i, linha in enumerate(linhas):
    if 'Valor do ISS' in linha:
        print(f"Linha {i}: {linha}")
        print(f"Linha {i+1}: {linhas[i+1] if i+1 < len(linhas) else ''}")
        
print("\n" + "="*50)
print("TESTANDO PADRÃO ESPECÍFICO:")
print("="*50)

# Testar padrão específico
match = re.search(r'Valor do ISS[^\d]*R\$\s*([\d\.,]+)', texto, re.IGNORECASE)
if match:
    print(f"✓ Encontrou com padrão específico: {match.group()}")
    print(f"  Valor capturado: {match.group(1)}")
else:
    print("✗ Padrão específico não funcionou")
    
# Testar padrão alternativo
match2 = re.search(r'R\$\s*4\.830[,.]80', texto)
if match2:
    print(f"✓ Encontrou com padrão alternativo: {match2.group()}")

print("\n" + "="*50)
print("TESTANDO ANÁLISE COMPLETA:")
print("="*50)

nota = analisador.analisar("NF 4550 - WEWORK - VENC 11.08.pdf")
print(f"Estado: {nota.estado}")
print(f"Tributado: {nota.dados_tributarios.tributado}")
print(f"Valor ISS: {nota.dados_tributarios.valor_iss}")
print(f"Observações: {nota.dados_tributarios.observacoes}")