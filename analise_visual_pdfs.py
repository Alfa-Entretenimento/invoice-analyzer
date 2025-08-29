#!/usr/bin/env python3
"""
Script para analisar PDFs baseado no conteúdo visual já disponível
"""

def analisar_nf_m4x():
    """
    Análise da NF 17 - M4X baseada no conteúdo visual
    """
    print("="*60)
    print("ANÁLISE: NF 17 - M4X - PJ - VENC 01.08.pdf")
    print("="*60)
    
    print("\n🏛️ IDENTIFICAÇÃO DO EMISSOR:")
    print("• Estado/Município: São Paulo - SP")
    print("• Órgão: PREFEITURA DO MUNICÍPIO DE SÃO PAULO")
    print("• Sistema: NFS-e (Nota Fiscal Eletrônica de Serviços)")
    
    print("\n📋 DADOS DA NOTA:")
    print("• Número da Nota: 00000017")
    print("• Data e Hora de Emissão: 01/08/2025 09:01:39")
    print("• Código de Verificação: 2RED-BDYN")
    print("• RPS Nº: 17, emitido em 01/08/2025")
    
    print("\n👤 PRESTADOR DE SERVIÇOS:")
    print("• CPF/CNPJ: 54.748.959/0001-60")
    print("• Nome/Razão Social: M4X CONSULTORIA LTDA")
    print("• Endereço: R CACONDE 49, APT 21 - JARDIM PAULISTA - CEP: 01425-011")
    print("• Município: São Paulo - SP")
    print("• Inscrição Municipal: 1.316.641-7")
    
    print("\n🏢 TOMADOR DE SERVIÇOS:")
    print("• Nome/Razão Social: ALFA ENTRETENIMENTO S.A.")
    print("• CPF/CNPJ: 55.369.927/0001-04")
    print("• Endereço: R TEODORO SAMPAIO 744, CONJ 108 - PINHEIROS - CEP: 05406-000")
    print("• Município: São Paulo - SP")
    print("• E-mail: -----")
    print("• Inscrição Municipal: 1.376.096-6")
    
    print("\n💰 VALORES FISCAIS:")
    print("• Valor Total do Serviço: R$ 69.888,00")
    print("• Base de Cálculo (R$): 69.888,00")
    print("• Alíquota (%): 5,00%")
    print("• Valor do ISS (R$): 3.494,40")
    print("• Crédito (R$): 0,00")
    print("• INSS: -")
    print("• IRRF: 1.048,32")
    print("• CSLL: 698,88")
    print("• COFINS: 2.096,64")
    print("• PIS/PASEP: 454,27")
    
    print("\n🔖 CÓDIGO DO SERVIÇO:")
    print("• Código: 03116")
    print("• Descrição: Assessoria ou consultoria de qualquer natureza, não contida em outros itens desta lista.")
    
    print("\n📝 DISCRIMINAÇÃO DOS SERVIÇOS:")
    print("• PRESTAÇÃO DE SERVIÇOS DE CONSULTORIA")
    print("• VALOR LÍQUIDO: R$ 65.589,89")
    print("• Vencimento: 07/08/2025")
    
    print("\n📊 TRIBUTOS:")
    print("• Valor Aprovimado dos Tributos / Fonte: R$ 11.412,71 (16,33%) / IBPT")
    
    print("\n🔍 PADRÕES ÚNICOS IDENTIFICADOS:")
    print("• Layout padrão São Paulo com tabela de valores detalhada")
    print("• Campo 'Vencimento' na seção de discriminação")
    print("• Múltiplos tributos federais (IRRF, CSLL, COFINS, PIS/PASEP)")
    print("• Código de verificação alfanumérico (2RED-BDYN)")
    print("• RPS com numeração simples (17)")
    print("• Valor aproximado de tributos com referência IBPT")

def analisar_nf_jnto():
    """
    Análise da NF 282 - JNTO AD.EZ baseada no conteúdo visual
    """
    print("\n" + "="*60)
    print("ANÁLISE: NF 282 - JNTO AD.EZ - VENC 25.08.pdf")
    print("="*60)
    
    print("\n🏛️ IDENTIFICAÇÃO DO EMISSOR:")
    print("• Estado/Município: São Paulo - SP")
    print("• Órgão: PREFEITURA DO MUNICÍPIO DE SÃO PAULO")
    print("• Sistema: NFS-e (Nota Fiscal Eletrônica de Serviços)")
    
    print("\n📋 DADOS DA NOTA:")
    print("• Número da Nota: 00000282")
    print("• Data e Hora de Emissão: 14/08/2025 15:36:48")
    print("• Código de Verificação: LUJB-BQE8")
    
    print("\n👤 PRESTADOR DE SERVIÇOS:")
    print("• CPF/CNPJ: 44.524.280/0001-02")
    print("• Nome/Razão Social: JNTO AD EZ COMUNICACAO LTDA")
    print("• Endereço: R MOURATO COELHO 90, SALA 83 - PINHEIROS - CEP: 05417-000")
    print("• Município: São Paulo - SP")
    print("• Inscrição Municipal: 7.164.253-1")
    
    print("\n🏢 TOMADOR DE SERVIÇOS:")
    print("• Nome/Razão Social: ALFA ENTRETENIMENTO S.A.")
    print("• CPF/CNPJ: 55.369.927/0001-04")
    print("• Endereço: R TEODORO SAMPAIO 744, CONJ 108 - PINHEIROS - CEP: 05406-000")
    print("• Município: São Paulo - SP")
    print("• E-mail: -----")
    print("• Inscrição Municipal: 1.376.096-6")
    
    print("\n📝 DISCRIMINAÇÃO DOS SERVIÇOS:")
    print("• Prestação de Serviços")
    print("• Descrição: 142 FTDs")
    print("• DADOS BANCÁRIOS:")
    print("  - BANCO: Santander (033)")
    print("  - AG: 2006")
    print("  - CC: 13002021-7")
    print("  - VENCIMENTO: 18/08/2025")
    print("• Observação sobre retenção de 1.5% de IRRF e Instrução Normativa SRF nº 123/92")
    
    print("\n💰 VALORES FISCAIS:")
    print("• Valor Total do Serviço: R$ 15.620,00")
    print("• Base de Cálculo (R$): 15.620,00")
    print("• Alíquota (%): 5,00%")
    print("• Valor do ISS (R$): 781,00")
    print("• Crédito (R$): 0,00")
    print("• INSS, IRRF, CSLL, COFINS, PIS/PASEP: -")
    
    print("\n🔖 CÓDIGO DO SERVIÇO:")
    print("• Código: 02496")
    print("• Descrição: Propaganda e publicidade, promoção de vendas, planejamento de campanhas e materiais publicitários.")
    
    print("\n🔍 PADRÕES ÚNICOS IDENTIFICADOS:")
    print("• Layout padrão São Paulo simplificado")
    print("• Seção de dados bancários detalhada na discriminação")
    print("• Referência a FTDs (unidade de medida específica)")
    print("• Código de verificação alfanumérico (LUJB-BQE8)")
    print("• Observações sobre retenções e instrução normativa")
    print("• Apenas ISS como tributo municipal")
    print("• Vencimento dentro da discriminação dos serviços")

def gerar_resumo_padroes():
    """
    Gera resumo dos padrões encontrados para atualização do analisador
    """
    print("\n" + "="*80)
    print("RESUMO DE PADRÕES PARA ATUALIZAÇÃO DO ANALISADOR")
    print("="*80)
    
    print("\n🔧 MELHORIAS NECESSÁRIAS:")
    
    print("\n1. EXTRAÇÃO DE TEXTO:")
    print("   • Problema: PDFs com encoding problemático (cid characters)")
    print("   • Solução: Implementar OCR como fallback ou usar diferentes métodos de extração")
    
    print("\n2. PADRÕES SÃO PAULO:")
    print("   • Valor Total: padrão 'VALOR TOTAL DO SERVIÇO = R$ X.XXX,XX'")
    print("   • Base de Cálculo: buscar em tabela após 'Valor Total das Deduções'")
    print("   • ISS: buscar 'Valor do ISS (R$)' na tabela de valores")
    print("   • Alíquota: buscar 'Alíquota (%)' na tabela")
    print("   • Código de Verificação: formatos 'XXXX-XXXX' alfanuméricos")
    
    print("\n3. CAMPOS ESPECÍFICOS:")
    print("   • Vencimento pode estar na discriminação dos serviços")
    print("   • Dados bancários podem estar na discriminação")
    print("   • Múltiplos tributos federais (IRRF, CSLL, COFINS, PIS/PASEP)")
    print("   • Campo 'Valor Aproximado dos Tributos' com referência IBPT")
    
    print("\n4. CÓDIGOS DE SERVIÇO:")
    print("   • 03116: Assessoria/consultoria")
    print("   • 02496: Propaganda e publicidade")
    
    print("\n5. REGEX PATTERNS SUGERIDOS:")
    print("   • Valor Total: r'VALOR TOTAL DO SERVIÇO = R\\$ ([\\d.,]+)'")
    print("   • ISS: r'Valor do ISS \\(R\\$\\)\\s*([\\d.,]+)'")
    print("   • Alíquota: r'Alíquota \\(%\\)\\s*([\\d.,]+)'")
    print("   • Base Cálculo: r'Base de Cálculo \\(R\\$\\)\\s*([\\d.,]+)'")
    print("   • Código Verif: r'Código de Verificação\\s*([A-Z0-9]{4}-[A-Z0-9]{4})'")
    print("   • Vencimento: r'(?:Vencimento|VENCIMENTO):\\s*(\\d{2}/\\d{2}/\\d{4})'")

def main():
    analisar_nf_m4x()
    analisar_nf_jnto()
    gerar_resumo_padroes()
    
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA")
    print("="*80)
    print("Os padrões identificados podem ser usados para atualizar o analisador_nf.py")

if __name__ == "__main__":
    main()