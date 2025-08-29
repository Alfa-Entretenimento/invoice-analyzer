#!/usr/bin/env python3
"""
Script de teste para o analisador de notas fiscais
Testa com o PDF de exemplo fornecido
"""

from analisador_nf import AnalisadorNotaFiscal, exibir_resultado
import sys

def testar_nota():
    """Testa a análise com a nota fiscal fornecida"""
    caminho_pdf = "NF 4550 - WEWORK - VENC 11.08.pdf"
    
    print("\n🧪 TESTE DO ANALISADOR DE NOTAS FISCAIS")
    print("="*50)
    print(f"Arquivo de teste: {caminho_pdf}")
    
    try:
        analisador = AnalisadorNotaFiscal()
        nota = analisador.analisar(caminho_pdf)
        
        # Exibir resultado formatado
        exibir_resultado(nota)
        
        # Validações
        print("\n✅ VALIDAÇÕES:")
        
        # Validar estado
        assert nota.estado == "SP", f"❌ Estado incorreto: {nota.estado} (esperado: SP)"
        print("   ✓ Estado identificado corretamente: SP")
        
        # Validar número
        assert nota.numero == "000004550", f"❌ Número incorreto: {nota.numero}"
        print(f"   ✓ Número da nota correto: {nota.numero}")
        
        # Validar tributação
        assert nota.dados_tributarios.tributado == True, "❌ Tributação não identificada"
        print("   ✓ Tributação identificada corretamente")
        
        # Validar valor ISS
        if nota.dados_tributarios.valor_iss:
            print(f"   ✓ Valor ISS extraído: R$ {nota.dados_tributarios.valor_iss}")
        
        # Validar alíquota
        if nota.dados_tributarios.aliquota_iss:
            assert nota.dados_tributarios.aliquota_iss == 5, f"❌ Alíquota incorreta"
            print(f"   ✓ Alíquota correta: {nota.dados_tributarios.aliquota_iss}%")
        
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        
    except AssertionError as e:
        print(f"\n❌ Erro na validação: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro ao executar teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    testar_nota()