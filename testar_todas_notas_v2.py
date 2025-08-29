#!/usr/bin/env python3
"""
Teste completo do analisador V2 com todas as notas
"""

import os
import glob
from analisador_nf_v2 import AnalisadorNotaFiscalV2, exibir_resultado_detalhado, formatar_valor
from collections import defaultdict
from decimal import Decimal

def testar_todas_notas():
    """Testa o analisador V2 com todas as notas disponíveis"""
    
    print("\n" + "="*70)
    print("🚀 TESTE DO ANALISADOR V2 - ANÁLISE COMPLETA")
    print("="*70)
    
    # Buscar todos os PDFs
    pdfs = []
    pdfs.extend(glob.glob('notas/*.pdf'))
    pdfs.extend(glob.glob('*.pdf'))
    
    # Filtrar apenas notas fiscais
    pdfs = [pdf for pdf in pdfs if 'NF' in os.path.basename(pdf).upper()]
    pdfs = sorted(pdfs)
    
    print(f"\n📊 Total de notas encontradas: {len(pdfs)}")
    
    # Estatísticas
    resultados = []
    estados_count = defaultdict(int)
    tributadas = 0
    nao_tributadas = 0
    erros = 0
    valor_total_geral = Decimal('0')
    valor_iss_total = Decimal('0')
    total_retencoes = Decimal('0')
    
    # Analisar cada nota
    for i, pdf_path in enumerate(pdfs, 1):
        nome_arquivo = os.path.basename(pdf_path)
        print(f"\n[{i}/{len(pdfs)}] Analisando: {nome_arquivo}")
        print("-" * 50)
        
        try:
            analisador = AnalisadorNotaFiscalV2()
            nota = analisador.analisar(pdf_path)
            
            # Exibir resumo
            print(f"✓ Número: {nota.numero}")
            print(f"✓ Estado: {nota.estado}")
            print(f"✓ Município: {nota.municipio}")
            print(f"✓ Valor Total: {formatar_valor(nota.valor_total)}")
            print(f"✓ Tributado: {'SIM' if nota.dados_tributarios.tributado else 'NÃO'}")
            
            if nota.dados_tributarios.valor_iss:
                print(f"✓ ISS: {formatar_valor(nota.dados_tributarios.valor_iss)}")
            
            if nota.dados_tributarios.total_retencoes() > 0:
                print(f"✓ Retenções: {formatar_valor(nota.dados_tributarios.total_retencoes())}")
            
            print(f"✓ Confiança: {nota.confianca_extracao:.0%}")
            
            # Atualizar estatísticas
            estados_count[nota.estado] += 1
            
            if nota.estado != 'ERRO_LEITURA':
                if nota.dados_tributarios.tributado:
                    tributadas += 1
                else:
                    nao_tributadas += 1
                
                valor_total_geral += nota.valor_total
                
                if nota.dados_tributarios.valor_iss:
                    valor_iss_total += nota.dados_tributarios.valor_iss
                
                total_retencoes += nota.dados_tributarios.total_retencoes()
            else:
                erros += 1
            
            resultados.append({
                'arquivo': nome_arquivo,
                'nota': nota
            })
            
        except Exception as e:
            print(f"❌ Erro ao processar: {e}")
            erros += 1
            estados_count['ERRO'] += 1
    
    # Exibir estatísticas finais
    print("\n" + "="*70)
    print("📊 ESTATÍSTICAS FINAIS")
    print("="*70)
    
    print("\n🏛️ DISTRIBUIÇÃO POR ESTADO:")
    for estado, count in sorted(estados_count.items()):
        if estado not in ['ERRO_LEITURA', 'ERRO', 'DESCONHECIDO']:
            print(f"   {estado}: {count} nota(s)")
    
    if estados_count.get('DESCONHECIDO', 0) > 0:
        print(f"   DESCONHECIDO: {estados_count['DESCONHECIDO']} nota(s)")
    
    if erros > 0:
        print(f"\n⚠️ Erros de leitura: {erros}")
    
    print(f"\n💰 ANÁLISE TRIBUTÁRIA:")
    print(f"   Notas Tributadas: {tributadas}")
    print(f"   Notas Não Tributadas: {nao_tributadas}")
    if tributadas > 0:
        print(f"   Taxa de Tributação: {tributadas/(tributadas+nao_tributadas):.1%}")
    
    print(f"\n📈 VALORES CONSOLIDADOS:")
    print(f"   Valor Total das Notas: {formatar_valor(valor_total_geral)}")
    print(f"   ISS Total: {formatar_valor(valor_iss_total)}")
    print(f"   Retenções Totais: {formatar_valor(total_retencoes)}")
    
    if valor_total_geral > 0:
        taxa_iss = (valor_iss_total / valor_total_geral * 100) if valor_total_geral > 0 else 0
        print(f"   Taxa Efetiva ISS: {taxa_iss:.2f}%")
    
    # Análise de confiança
    confiances = [r['nota'].confianca_extracao for r in resultados if r['nota'].estado != 'ERRO_LEITURA']
    if confiances:
        confianca_media = sum(confiances) / len(confiances)
        print(f"\n🎯 QUALIDADE DA EXTRAÇÃO:")
        print(f"   Confiança Média: {confianca_media:.0%}")
        print(f"   Alta Confiança (>80%): {sum(1 for c in confiances if c > 0.8)} notas")
        print(f"   Média Confiança (60-80%): {sum(1 for c in confiances if 0.6 <= c <= 0.8)} notas")
        print(f"   Baixa Confiança (<60%): {sum(1 for c in confiances if c < 0.6)} notas")
    
    # Salvar relatório detalhado
    with open('relatorio_analise_v2.json', 'w', encoding='utf-8') as f:
        import json
        relatorio = {
            'total_notas': len(pdfs),
            'estados': dict(estados_count),
            'tributadas': tributadas,
            'nao_tributadas': nao_tributadas,
            'erros': erros,
            'valor_total': str(valor_total_geral),
            'iss_total': str(valor_iss_total),
            'retencoes_totais': str(total_retencoes),
            'notas': []
        }
        
        for r in resultados:
            nota = r['nota']
            relatorio['notas'].append({
                'arquivo': r['arquivo'],
                'numero': nota.numero,
                'estado': nota.estado,
                'municipio': nota.municipio,
                'valor_total': str(nota.valor_total),
                'tributado': nota.dados_tributarios.tributado,
                'valor_iss': str(nota.dados_tributarios.valor_iss) if nota.dados_tributarios.valor_iss else '0',
                'confianca': nota.confianca_extracao
            })
        
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Relatório detalhado salvo em: relatorio_analise_v2.json")
    
    # Mostrar nota com análise mais detalhada como exemplo
    print("\n" + "="*70)
    print("📋 EXEMPLO DE ANÁLISE DETALHADA (Primeira nota tributada):")
    print("="*70)
    
    for r in resultados:
        if r['nota'].dados_tributarios.tributado and r['nota'].estado != 'ERRO_LEITURA':
            exibir_resultado_detalhado(r['nota'])
            break
    
    print("\n✅ ANÁLISE COMPLETA FINALIZADA!")
    
    return resultados

if __name__ == "__main__":
    resultados = testar_todas_notas()