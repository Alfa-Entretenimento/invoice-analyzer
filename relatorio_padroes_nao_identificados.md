# Análise de PDFs Não Identificados - Relatório de Padrões

## Arquivos Analisados
1. **NF 17 - M4X - PJ - VENC 01.08.pdf**
2. **NF 282 - JNTO AD.EZ - VENC 25.08.pdf**

## Problemas Identificados

### 1. Extração de Texto
- **Problema**: PDFs com encoding problemático (caracteres CID)
- **Impacto**: PyPDF2 e pdfplumber não conseguem extrair texto corretamente
- **Solução**: Implementar OCR como fallback ou usar bibliotecas mais robustas

### 2. Padrões Específicos de São Paulo

#### NF 17 - M4X (Consultoria)
**Dados Extraídos:**
- Número: 00000017
- Valor Total: R$ 69.888,00
- ISS: R$ 3.494,40 (5,00%)
- Base de Cálculo: R$ 69.888,00
- Código Verificação: 2RED-BDYN
- Código Serviço: 03116 (Assessoria/consultoria)
- Vencimento: 07/08/2025
- Tributos Federais: IRRF (R$ 1.048,32), CSLL (R$ 698,88), COFINS (R$ 2.096,64), PIS/PASEP (R$ 454,27)

**Padrões Únicos:**
- Múltiplos tributos federais na mesma nota
- Vencimento na seção de discriminação
- Valor aproximado de tributos com referência IBPT
- RPS com numeração simples

#### NF 282 - JNTO AD.EZ (Publicidade)
**Dados Extraídos:**
- Número: 00000282
- Valor Total: R$ 15.620,00
- ISS: R$ 781,00 (5,00%)
- Base de Cálculo: R$ 15.620,00
- Código Verificação: LUJB-BQE8
- Código Serviço: 02496 (Propaganda e publicidade)
- Vencimento: 18/08/2025
- Dados Bancários: Santander (033), AG: 2006, CC: 13002021-7

**Padrões Únicos:**
- Dados bancários detalhados na discriminação
- Referência a unidades específicas (FTDs)
- Observações sobre retenções e instrução normativa
- Apenas ISS como tributo municipal

## Regex Patterns Desenvolvidos

### Valores Principais
```python
# Valor Total
r'VALOR TOTAL DO SERVIÇO = R\$ ([\d.,]+)'

# ISS
r'Valor do ISS \(R\$\)\s*([\d.,]+)'

# Alíquota
r'Alíquota \(%\)\s*([\d.,]+)'

# Base de Cálculo
r'Base de Cálculo \(R\$\)\s*([\d.,]+)'
```

### Dados Adicionais
```python
# Código de Verificação
r'Código de Verificação\s*([A-Z0-9]{4}-[A-Z0-9]{4})'

# Vencimento
r'(?:Vencimento|VENCIMENTO):\s*(\d{2}/\d{2}/\d{4})'

# Dados Bancários
r'BANCO:\s*([^(\n]+)'
r'AG:\s*(\d+)'
r'CC:\s*([\d\-]+)'
```

### Tributos Federais
```python
r'IRRF.*?(\d+[.,]\d+)'
r'CSLL.*?(\d+[.,]\d+)'
r'COFINS.*?(\d+[.,]\d+)'
r'PIS(?:/PASEP)?.*?(\d+[.,]\d+)'
```

## Códigos de Serviço Identificados
- **03116**: Assessoria ou consultoria de qualquer natureza
- **02496**: Propaganda e publicidade, promoção de vendas, planejamento de campanhas

## Melhorias Implementadas

### Função `analisar_sp_melhorado()`
- Extração robusta de valores monetários
- Identificação de códigos de verificação
- Extração de vencimento da discriminação
- Captura de dados bancários
- Identificação de tributos federais
- Reconhecimento de códigos de serviço

### Resultados dos Testes
**NF M4X:**
- ✅ Valor Total: R$ 69.888,00
- ✅ ISS: R$ 3.494,40
- ✅ Alíquota: 5,00%
- ✅ Código Verificação: 2RED-BDYN
- ✅ Vencimento: 07/08/2025
- ✅ Tributos Federais: IRRF, CSLL, COFINS, PIS

**NF JNTO:**
- ✅ Valor Total: R$ 15.620,00
- ✅ ISS: R$ 781,00
- ✅ Alíquota: 5,00%
- ✅ Código Verificação: LUJB-BQE8
- ✅ Vencimento: 18/08/2025
- ✅ Dados Bancários: Santander, AG: 2006

## Recomendações para Atualização

### 1. Atualizar `analisador_nf.py`
- Substituir função `analisar_tributacao_sp()`
- Implementar patterns mais robustos
- Adicionar extração de dados bancários
- Incluir tributos federais

### 2. Melhorar Extração de Texto
- Implementar OCR como fallback
- Testar bibliotecas alternativas (pymupdf, etc.)
- Adicionar pré-processamento de texto

### 3. Expandir Base de Códigos
- Criar mapeamento completo de códigos de serviço
- Implementar validação por tipo de serviço
- Adicionar descrições padronizadas

### 4. Implementar Validação Cruzada
- Verificar consistência entre valores
- Validar cálculos de ISS
- Comparar dados extraídos

## Arquivos Gerados
1. `/Users/fabiowill/GabrielNF/analise_pdfs_especificos.py` - Script de análise detalhada
2. `/Users/fabiowill/GabrielNF/analise_visual_pdfs.py` - Análise baseada no conteúdo visual
3. `/Users/fabiowill/GabrielNF/melhorias_analisador_sp.py` - Implementação das melhorias
4. `/Users/fabiowill/GabrielNF/relatorio_padroes_nao_identificados.md` - Este relatório

## Próximos Passos
1. Integrar melhorias no `analisador_nf.py`
2. Testar com conjunto maior de PDFs
3. Implementar OCR para casos problemáticos
4. Expandir para outros estados se necessário