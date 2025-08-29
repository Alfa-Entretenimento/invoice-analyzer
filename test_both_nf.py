#!/usr/bin/env python3
"""
Script de teste para validar análise de ambas as notas fiscais
Testa SP (WeWork) e BA (EBAC)
"""

from analisador_nf import AnalisadorNotaFiscal, exibir_resultado
import sys

def testar_notas():
    """Testa a análise de ambas as notas fiscais"""
    
    print("\n" + "="*60)
    print("🧪 TESTE DE ANÁLISE DE NOTAS FISCAIS")
    print("="*60)
    
    # Teste 1: São Paulo (WeWork)
    print("\n📄 TESTE 1: Nota Fiscal de São Paulo (WeWork)")
    print("-"*50)
    
    try:
        analisador_sp = AnalisadorNotaFiscal()
        nota_sp = analisador_sp.analisar("NF 4550 - WEWORK - VENC 11.08.pdf")
        
        print(f"✓ Estado: {nota_sp.estado}")
        print(f"✓ Número: {nota_sp.numero}")
        print(f"✓ Valor Total: R$ {nota_sp.valor_total}")
        print(f"✓ Tributada: {'SIM' if nota_sp.dados_tributarios.tributado else 'NÃO'}")
        
        if nota_sp.dados_tributarios.valor_iss:
            print(f"✓ Valor ISS: R$ {nota_sp.dados_tributarios.valor_iss}")
            print(f"✓ Alíquota: {nota_sp.dados_tributarios.aliquota_iss}%")
        
        print(f"✓ Retenções:")
        print(f"  - ISS: R$ {nota_sp.dados_tributarios.retencao_iss or 0}")
        print(f"  - PIS: R$ {nota_sp.dados_tributarios.retencao_pis or 0}")
        print(f"  - COFINS: R$ {nota_sp.dados_tributarios.retencao_cofins or 0}")
        
        # Validação SP
        assert nota_sp.estado == "SP", f"Estado incorreto: {nota_sp.estado}"
        assert nota_sp.dados_tributarios.tributado == True, "SP deveria estar tributada"
        assert nota_sp.dados_tributarios.valor_iss > 0, "SP deveria ter valor de ISS"
        print("\n✅ Nota de SP validada corretamente!")
        
    except Exception as e:
        print(f"\n❌ Erro ao analisar nota SP: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Teste 2: Bahia (EBAC)
    print("\n📄 TESTE 2: Nota Fiscal da Bahia (EBAC)")
    print("-"*50)
    
    try:
        analisador_ba = AnalisadorNotaFiscal()
        nota_ba = analisador_ba.analisar("NF 4 - EBAC - VENC 11.08.pdf")
        
        print(f"✓ Estado: {nota_ba.estado}")
        print(f"✓ Número: {nota_ba.numero}")
        print(f"✓ Valor Total: R$ {nota_ba.valor_total}")
        print(f"✓ Tributada: {'SIM' if nota_ba.dados_tributarios.tributado else 'NÃO'}")
        
        if nota_ba.dados_tributarios.valor_iss:
            print(f"✓ Valor ISS: R$ {nota_ba.dados_tributarios.valor_iss}")
            print(f"✓ Alíquota: {nota_ba.dados_tributarios.aliquota_iss}%")
        
        print(f"✓ Retenções:")
        print(f"  - PIS: R$ {nota_ba.dados_tributarios.retencao_pis or 0}")
        print(f"  - COFINS: R$ {nota_ba.dados_tributarios.retencao_cofins or 0}")
        print(f"  - IR: R$ {nota_ba.dados_tributarios.retencao_ir or 0}")
        print(f"  - CSLL: R$ {nota_ba.dados_tributarios.retencao_csll or 0}")
        
        # Validação BA
        assert nota_ba.estado == "BA", f"Estado incorreto: {nota_ba.estado}"
        assert nota_ba.dados_tributarios.tributado == True, "BA deveria estar tributada"
        assert nota_ba.dados_tributarios.valor_iss > 0, "BA deveria ter valor de ISS"
        print("\n✅ Nota da BA validada corretamente!")
        
    except Exception as e:
        print(f"\n❌ Erro ao analisar nota BA: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Resumo comparativo
    print("\n" + "="*60)
    print("📊 RESUMO COMPARATIVO")
    print("="*60)
    
    print("\n┌─────────────────┬──────────────────┬──────────────────┐")
    print("│     CAMPO       │   SÃO PAULO      │     BAHIA        │")
    print("├─────────────────┼──────────────────┼──────────────────┤")
    print(f"│ Número          │ {nota_sp.numero:^16} │ {nota_ba.numero:^16} │")
    print(f"│ Valor Total     │ R$ {nota_sp.valor_total:^13} │ R$ {nota_ba.valor_total:^13} │")
    print(f"│ Tributada       │ {'SIM' if nota_sp.dados_tributarios.tributado else 'NÃO':^16} │ {'SIM' if nota_ba.dados_tributarios.tributado else 'NÃO':^16} │")
    print(f"│ Valor ISS       │ R$ {nota_sp.dados_tributarios.valor_iss or 0:^13} │ R$ {nota_ba.dados_tributarios.valor_iss or 0:^13} │")
    print(f"│ Alíquota        │ {str(nota_sp.dados_tributarios.aliquota_iss) + '%' if nota_sp.dados_tributarios.aliquota_iss else '-':^16} │ {str(nota_ba.dados_tributarios.aliquota_iss) + '%' if nota_ba.dados_tributarios.aliquota_iss else '-':^16} │")
    print("└─────────────────┴──────────────────┴──────────────────┘")
    
    print("\n✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")

if __name__ == "__main__":
    testar_notas()