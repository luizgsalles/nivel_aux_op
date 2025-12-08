import streamlit as st
from collections import Counter
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Função para gerar PDF
def gerar_pdf(nome_avaliado, respostas, nivel_final, metodo_usado, max_frequencia, contagem, criterios_dict, observacao_empate=""):
    """Gera PDF com o resultado da avaliação"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container para os elementos do PDF
    elementos = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo para título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Estilo para subtítulos
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Título do documento
    elementos.append(Paragraph("Avaliação de Enquadramento", titulo_style))
    elementos.append(Paragraph("Auxiliar Operacional", titulo_style))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Informações do avaliado
    elementos.append(Paragraph(f"<b>Colaborador Avaliado:</b> {nome_avaliado}", normal_style))
    elementos.append(Paragraph(f"<b>Data da Avaliação:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}", normal_style))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Resultado principal
    elementos.append(Paragraph("Resultado da Avaliação", subtitulo_style))
    
    # Box com resultado
    resultado_data = [
        ['Enquadramento Sugerido:', f'Nível {nivel_final}'],
        ['Método Utilizado:', metodo_usado],
        ['Frequência:', f'{max_frequencia} de {len(criterios_dict)} critérios']
    ]
    
    resultado_table = Table(resultado_data, colWidths=[3*inch, 3*inch])
    resultado_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#2c5aa0'))
    ]))
    
    elementos.append(resultado_table)
    elementos.append(Spacer(1, 0.2*inch))
    
    if observacao_empate:
        elementos.append(Paragraph(f"<i>Observação: {observacao_empate}</i>", normal_style))
        elementos.append(Spacer(1, 0.2*inch))
    
    # Distribuição por nível
    elementos.append(Paragraph("Distribuição por Nível", subtitulo_style))
    
    dist_data = [['Nível', 'Frequência']]
    for nivel in ['A', 'A-B', 'B', 'C', 'D', 'E', 'F', 'G']:
        count = contagem.get(nivel, 0)
        if count > 0:
            marcador = ' ✓ (Predominante)' if nivel == nivel_final else ''
            dist_data.append([f'Nível {nivel}{marcador}', f'{count} {"vez" if count == 1 else "vezes"}'])
    
    dist_table = Table(dist_data, colWidths=[3*inch, 3*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    
    elementos.append(dist_table)
    elementos.append(PageBreak())
    
    # Tabela de consolidação
    elementos.append(Paragraph("Tabela de Consolidação - Critérios Avaliados", subtitulo_style))
    elementos.append(Spacer(1, 0.1*inch))
    
    consolidacao_data = [['#', 'Critério', 'Nível']]
    for idx, (criterio, nivel) in enumerate(respostas.items(), 1):
        criterio_nome = criterio.replace(f"{idx}. ", "")
        consolidacao_data.append([str(idx), criterio_nome, nivel])
    
    consolidacao_table = Table(consolidacao_data, colWidths=[0.5*inch, 4.5*inch, 1*inch])
    consolidacao_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    
    elementos.append(consolidacao_table)
    elementos.append(PageBreak())
    
    # Detalhamento das respostas
    elementos.append(Paragraph("Detalhamento das Respostas", subtitulo_style))
    elementos.append(Spacer(1, 0.1*inch))
    
    for idx, (criterio, nivel) in enumerate(respostas.items(), 1):
        criterio_nome = criterio.replace(f"{idx}. ", "")
        elementos.append(Paragraph(f"<b>{idx}. {criterio_nome}</b>", normal_style))
        elementos.append(Paragraph(f"<b>Nível selecionado: {nivel}</b>", normal_style))
        
        # Pegar descrição do nível
        descricao = criterios_dict[criterio][nivel]
        elementos.append(Paragraph(f"<i>{descricao}</i>", normal_style))
        elementos.append(Spacer(1, 0.15*inch))
    
    # Rodapé
    elementos.append(Spacer(1, 0.3*inch))
    elementos.append(Paragraph("_______________________________________________", normal_style))
    elementos.append(Paragraph("<i>Documento gerado automaticamente pelo Sistema de Avaliação de Enquadramento</i>", 
                               ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))
    
    # Construir PDF
    doc.build(elementos)
    buffer.seek(0)
    return buffer

# Configuração da página
st.set_page_config(
    page_title="Avaliação de Enquadramento - Nivelamento Operacional",
    page_icon="📊",
    layout="wide"
)



# Título principal
st.title("📊 Avaliação de Enquadramento - Nivelamento Operacional")
st.markdown("---")

# Dicionário com todas as dimensões e seus níveis

CRITERIOS_AUXILIAR = {
    "1. Tamanho e Complexidade da Carteira de Casos": {
        "A": "Carteira de 8-12 casos simples, executa sob supervisão direta do Nível D ou Assistente (valida 80-90% das ações antes de executar), TMR não é medido individualmente ainda ou está >10 dias, foco é aprender processos básicos",
        "B": "Carteira de 12-18 casos simples, executa com validação periódica do gestor (valida 50-60% das decisões, reuniões semanais vs diárias), TMR ~7-9 dias, começa a ter autonomia em casos mais rotineiros",
        "C": "Carteira de 18-25 casos simples com autonomia completa em processos padronizados, TMR <7 dias, FCR >65%, valida apenas dúvidas genuínas ou situações atípicas",
        "D": "Carteira de 25-30 casos simples com excelência consistente (TMR <6 dias, FCR >70%, prazo >95%), é referência técnica consultada por A-B-C, frequentemente tem melhor performance individual do setor",
        "E": "Mantém carteira de 25-30 casos simples com excelência (TMR <6d, FCR >70%) + resolve 2-3 casos médios iniciais/mês do Assistente sob supervisão do Assistente D-E-F (80% dos casos médios ainda precisa validar abordagem)",
        "F": "Reduz para 20-25 casos simples críticos + resolve 5-8 casos médios/mês com autonomia crescente (valida apenas 50-60% das decisões em casos médios), mantém excelência em ambos",
        "G": "Carteira mínima de 15-20 casos simples estratégicos + resolve 10-12 casos médios/mês com autonomia 70-80%, atua quase como Assistente A-B em desenvolvimento, pronto para promoção iminente"
    },
    "2. Autonomia e Necessidade de Supervisão": {
        "A": "Precisa de supervisão direta constante: check-in diário de 20-30min com Assistente D ou Nível D, não toma decisões sem validar antes (mesmo decisões simples), executa seguindo instruções passo a passo",
        "B": "Executa com acompanhamento periódico: validação semanal ou quando há dúvida, toma decisões simples autonomamente (ex: qual template usar, como priorizar casos do dia), mas valida decisões importantes antes de executar",
        "C": "Autonomia completa em casos padronizados: consulta gestor apenas em situações atípicas ou dúvidas genuínas (não mais que 2-3x por semana), toma decisões sozinho em 80-90% das situações do dia-a-dia",
        "D": "Autonomia total + ensina outros: é quem valida o trabalho de A-B-C, raramente precisa consultar Assistente ou Analista (apenas situações extraordinárias 1-2x por mês), toma todas as decisões dentro do escopo de casos simples sozinho",
        "E": "Autonomia em casos simples + aprende casos médios: mantém autonomia total em casos simples + desenvolve autonomia em casos médios sob supervisão próxima de Assistente (primeiros 2-3 meses valida 80%, depois reduz para 60-70%)",
        "F": "Autonomia consolidada em casos médios: valida apenas 50-60% das decisões de casos médios (vs 80% no nível E), toma decisões com informação 60-70% completa aceitando incerteza, demonstra julgamento crescente",
        "G": "Autonomia 70-80% em casos médios: valida apenas situações de alto risco ou precedente importante (~30-40% dos casos médios), atua quase como Assistente júnior, raramente precisa de supervisão próxima"
    },
    "3. Competências em Sistemas (SYSEMP/THORPE/INTELIPOST)": {
        "A": "Usa 40-50% das funcionalidades básicas: abre caso, altera status simples, consulta informações básicas, precisa de ajuda frequente (3-5x por semana), não sabe resolver quando sistema dá erro, usa apenas funcionalidades que foram treinadas explicitamente",
        "B": "Domina 60-70% funcionalidades operacionais: registra casos completos, altera múltiplos status, faz buscas com 2-3 filtros, exporta relatórios simples, resolve problemas básicos sozinho (erros comuns, campos obrigatórios), às vezes ainda precisa de ajuda (1-2x por semana)",
        "C": "Domina 80-90% funcionalidades: cria views personalizadas com múltiplos critérios, usa atalhos de teclado para eficiência, resolve problemas sozinho consultando documentação, ajuda colegas ocasionalmente quando perguntam (2-3x por semana)",
        "D": "Domina 95%+ funcionalidades: é consultado regularmente por colegas para dúvidas de sistema (5-10x por semana), identifica bugs e reporta com descrição clara de como reproduzir, propõe melhorias de usabilidade ou novos campos, conhece workarounds para limitações do sistema",
        "E": "Mantém domínio 95%+ em SYSEMP + desenvolve competência em sistemas de análise mais avançada (aprende funcionalidades de relatórios complexos, dashboards, integrações que Assistentes usam), começa a usar dados de múltiplos sistemas simultaneamente",
        "F": "Domina sistemas em nível intermediário de Assistente: cruza dados de 3-4 sistemas (SYSEMP + Thorpe + Intelipost + planilhas) identificando divergências, usa funcionalidades avançadas de filtros e exportação, consulta dados históricos de 6-12 meses para análise",
        "G": "Domina sistemas em nível avançado próximo de Assistente A-B: integra dados de múltiplas fontes, identifica padrões em datasets maiores (100-200 casos), usa sistemas quase no mesmo nível que Assistentes júnior, pode treinar Auxiliares A-B em funcionalidades avançadas"
    },
    "4. Excel e Análise de Dados": {
        "A": "Excel Básico: SOMA, MÉDIA, SE simples, filtros básicos, formata células (negrito, cor), copia e cola, trabalha com bases pequenas <500 linhas sem se perder, não usa fórmulas complexas",
        "B": "Excel Intermediário Inicial: PROCV básico, SOMASES com 2-3 critérios, tabelas dinâmicas simples (arrasta campos, soma/conta), formatação condicional básica (regras de cor por valor), trabalha com bases até 2-3k linhas, cria gráficos simples (colunas, linhas)",
        "C": "Excel Intermediário: Tabelas dinâmicas com campos calculados, gráficos diversos (barras empilhadas, dispersão), fórmulas aninhadas (SE com PROCV, SEERRO com PROCV), formatação condicional com fórmulas, trabalha com bases até 5-10k linhas, identifica erros comuns (#N/D, #REF!) e corrige",
        "D": "Excel Intermediário+/Avançado Inicial: ÍNDICE+CORRESP, PROCV com correspondência aproximada, dashboards básicos com 5-8 gráficos linkados, formatação profissional, macros gravadas (não escreve VBA mas grava e executa), trabalha com bases até 20-30k linhas, apresenta análises simples em reuniões",
        "E": "Mantém Excel Intermediário+ para casos simples + desenvolve análise de dados para casos médios: consolida dados de 2-3 fontes manualmente, calcula estatísticas básicas (média, mediana, desvio padrão), identifica outliers, cria tabelas resumo de 50-100 casos para análise de padrões",
        "F": "Excel Avançado Inicial: Power Query básico (importa e transforma dados de múltiplas abas), tabelas dinâmicas avançadas (múltiplos campos calculados, segmentadores), fórmulas matriciais simples, dashboards com 8-10 KPIs inter-relacionados, análises com múltiplas variáveis (100-200 casos)",
        "G": "Excel Avançado próximo de Assistente A: Power Query consolidando 3-5 fontes automaticamente, dashboards automatizados que atualizam ao refresh, macros simples em VBA (editados mas não escritos do zero), análises estatísticas intermediárias (correlações, tendências), apresenta insights analíticos estruturados"
    },
    "5. Comunicação com Cliente/Transportadora": {
        "A": "Contatos básicos roteirizados de 3-5min: segue script rigidamente, fica nervoso/inseguro em situações fora do script, escala imediatamente se cliente insiste ou faz pergunta não prevista, tom de voz hesitante, lê literalmente templates sem adaptar ao contexto",
        "B": "Contatos estruturados de 5-10min: segue estrutura mas adapta linguagem ao contexto (mais formal/informal conforme cliente), tem desenvoltura básica, gerencia objeções simples ('mas eu comprei ontem, por que ainda não chegou?'), escala quando cliente fica irritado ou situação foge muito do padrão, usa templates como base mas personaliza minimamente",
        "C": "Contatos com confiança até 15min: adapta tom emocional ao estado do cliente (empático quando frustrado, celebra quando resolve), gerencia clientes moderadamente insatisfeitos sem escalar (usa técnicas de de-escalação: validação emocional, foco em solução, compromissos realistas), negocia soluções simples dentro de alçada (pequenos descontos, ajuste de prazo), escala apenas situações de alto risco (ameaça Reclame Aqui, valor muito alto, cliente extremamente agressivo)",
        "D": "Contatos complexos de 15-20min: de-escalação efetiva de clientes muito insatisfeitos (70-80% dos casos acalma sem escalar), negocia soluções mais complexas (combinações de desconto + extensão prazo + cortesia), gerencia múltiplas objeções em sequência mantendo calma e empatia, raramente escala (apenas situações extraordinárias 1-2x por mês), constrói rapport que transforma reclamante em promotor",
        "E": "Mantém competência nível D em casos simples + desenvolve comunicação para casos médios sob supervisão: aprende a conduzir conversas de 10-20min com ambiguidade leve (cliente dá versões contraditórias, situação tem múltiplas interpretações possíveis), faz perguntas abertas estratégicas para coletar informações, ainda valida abordagem de comunicação crítica com Assistente antes de executar",
        "F": "Comunicação intermediária em casos médios: conduz conversas de 15-25min com múltiplas variáveis, adapta estratégia de comunicação conforme perfil do cliente (analítico quer dados, relacional quer empatia, dominante quer solução rápida), negocia soluções que envolvem 2-3 partes (cliente + transportadora + empresa), valida apenas situações de alto risco político",
        "G": "Comunicação avançada próxima de Assistente A-B: gerencia conversas complexas 20-30min, negocia com clientes difíceis com técnicas estruturadas (BATNA, interesses vs posições), coordena comunicação com múltiplos stakeholders simultaneamente, mantém documentação rigorosa de acordos, raramente precisa de supervisão na comunicação (70-80% autonomia)"
    },
    "6. Gestão de Prazos e Priorização": {
        "A": "Priorização guiada: gestor ou Nível D define diariamente o que fazer primeiro, não tem visão clara de toda a carteira, foca em 1-2 casos por vez sequencialmente, não antecipa prazos vencendo (espera ser alertado), usa apenas lista simples ou post-its sem sistema, às vezes perde prazos por falta de organização",
        "B": "Priorização básica autônoma: usa planilha ou sistema para ver prazos, prioriza casos urgentes (vencendo em 24-48h) vs normais, consegue gerenciar 3-4 casos simultaneamente sem se perder, identifica alguns prazos próximos (2-3 dias antes) mas não todos, ainda perde 1-2 prazos por mês, comunica quando vai atrasar mas às vezes já no dia do vencimento",
        "C": "Priorização efetiva com visão de carteira completa: usa matriz urgente/importante ou sistema similar, identifica todos os casos próximos de vencer prazo (5-7 dias antes) e age proativamente, gerencia 5-8 casos simultaneamente priorizando dinamicamente conforme situação evolui, raramente perde prazos (<1x por trimestre e por motivo justificável), comunica atrasos com 2-3 dias de antecedência propondo solução",
        "D": "Priorização otimizada e proativa: mantém TMR <6 dias consistentemente através de priorização eficiente, antecipa problemas antes de virarem urgências (identifica caso travado há 5-7 dias e age antes de virar crítico), trabalha em lote quando possível para eficiência (5 casos similares de uma vez), mantém visão consolidada de saúde da carteira (quantos casos em cada status, tendências), nunca perde prazos sem motivo de força maior, é modelo de organização para A-B-C",
        "E": "Mantém priorização nível D em casos simples + aprende priorização de casos médios mais complexos: desenvolve capacidade de balancear casos simples urgentes vs casos médios importantes mas menos urgentes, aprende a estimar tempo necessário para casos médios (não apenas simples), ajusta priorização quando caso médio se mostra mais complexo que esperado",
        "F": "Priorização híbrida sofisticada: balanceia carteira de 20-25 casos simples + 5-8 médios usando critérios múltiplos (urgência + importância + esforço + impacto), identifica casos médios que estão travando e toma ação preventiva, comunica proativamente quando carga está insustentável e negocia redistribuição ou extensão de prazo antes de comprometer qualidade",
        "G": "Priorização estratégica próxima de Assistente: mantém visão consolidada de 15-20 casos simples + 10-12 médios, prioriza dinamicamente ao longo do dia conforme situação evolui, identifica trade-offs e toma decisões conscientes (sacrificar prazo de caso X menos crítico para garantir qualidade de caso Y mais importante), mantém TMR competitivo em ambos os tipos de caso simultaneamente"
    },
    "7. Análise e Resolução de Problemas": {
        "A": "Execução de procedimentos: segue checklist ou passo a passo fornecido, não investiga causa raiz (apenas executa ação corretiva que foi orientada: 'cliente não recebeu, faz reenvio'), não formula hipóteses sobre por que problema aconteceu, consulta gestor para qualquer situação que foge do procedimento padrão, não conecta casos similares para identificar padrões",
        "B": "Análise básica: identifica problema imediato (não apenas sintoma superficial: 'pedido não foi entregue' → investiga e descobre que 'endereço estava incompleto'), formula 1-2 hipóteses simples sobre causa, valida hipóteses com gestor antes de agir, começa a conectar casos similares ocasionalmente ('já vi 2-3 casos assim essa semana, pode ser problema no sistema?')",
        "C": "Análise estruturada: identifica problema real vs sintoma, formula 2-3 hipóteses de causa, coleta informações sistematicamente para validar hipóteses (consulta múltiplos sistemas, fala com transportadora, valida versões diferentes), toma decisão com 70-80% de informação sem paralisia, documenta raciocínio além de ações (não apenas 'o que fiz' mas 'por que fiz'), identifica quando caso é atípico e escala apropriadamente",
        "D": "Análise profunda com padrões: além de resolver caso individual, identifica padrões sistêmicos (observa que 40% dos problemas de tipo X vêm de causa Y específica, documenta padrão, propõe ajuste preventivo), usa frameworks estruturados ocasionalmente (5 Porquês para chegar em causa raiz), diferencia correlação de causalidade (só porque A e B acontecem juntos não significa que A causa B), propõe pequenas melhorias de processo baseadas em padrões observados (2-3 por ano implementadas)",
        "E": "Mantém análise profunda em casos simples + desenvolve análise para casos médios com ambiguidade leve: aprende a analisar casos onde não há solução óbvia no playbook, quebra problema complexo em partes gerenciáveis, fórmula múltiplas hipóteses avaliando probabilidade relativa, coleta informações de forma estratégica (prioriza investigação no que tem maior impacto em decisão), ainda válida raciocínio com Assistente em casos médios críticos",
        "F": "Análise intermediária de casos médios: conduz investigações de 2-4h em casos com múltiplas variáveis interdependentes, cruza informações de 3-4 fontes identificando inconsistências, usa raciocínio contrafactual básico ('se hipótese X fosse verdadeira, deveria observar evidências A e B; observou A mas não B, então X provavelmente não é causa única'), documenta análise em formato estruturado (cronologia + stakeholders + hipóteses + evidências + recomendação), válida apenas situações extraordinárias",
        "G": "Análise avançada próxima de Assistente A-B: metodologia estruturada consolidada (5 Porquês rigoroso, Ishikawa quando apropriado, análise de Pareto identificando causas principais), diferencia causas raiz primárias vs secundárias vs contribuintes, propõe soluções que atacam causa raiz não apenas sintoma, documenta análises que servem de referência para colegas, autonomia 70-80% em análises de casos médios complexos"
    },
    "8. Mentoria e Desenvolvimento de Outros": {
        "A-B": "Ainda não mentora formalmente (foco é desenvolver competências próprias primeiro), pode ajudar colegas informalmente quando perguntam algo pontual (1-2x por semana, 5-10min), mas não tem responsabilidade estruturada de desenvolvimento de outros",
        "C": "Mentoria inicial de 1-2 Auxiliares A-B: shadowing reverso (Auxiliar júnior observa fazer 2-3 casos por semana), valida 30-40% dos casos do mentorado semanalmente fornecendo feedback estruturado (o que foi bem feito + 1-2 pontos de melhoria com sugestões), reunião semanal informal de 30min para tirar dúvidas e alinhar, feedback positivo do mentorado sobre utilidade da mentoria (>3.5/5.0)",
        "D": "Mentoria formal de 2-3 Auxiliares: rituais consistentes (check-in diário de 10-15min + reunião semanal de 45-60min estruturada), válida 40-50% dos casos fornecendo feedback detalhado e didático (não apenas 'está errado' mas 'está errado porque X, sugiro fazer Y da próxima vez'), shadowing bidirecional (Auxiliar júnior observa + Nível D observa júnior executar e dá feedback), documenta progresso trimestral, feedback positivo do mentorado (>4.0/5.0), pelo menos 1 mentorado promovido nos últimos 12-18 meses",
        "E": "Mantém mentoria nível D de 2-3 Auxiliares + começa mentoria informal de Auxiliares C que estão desenvolvendo casos médios: fornece coaching situacional quando Auxiliar C está tratando caso médio pela primeira vez (acompanha, orienta, válida raciocínio), compartilhar frameworks de análise que usa para casos médios, criar materiais didáticos simples (guias de 1-2 páginas, vídeos curtos 5-10min)",
        "F": "Mentoria ampliada: 2-3 Auxiliares A-B formalmente + 1-2 Auxiliares C-D em desenvolvimento de casos médios, investe 10-15% do tempo (8-12h/mês) em desenvolvimento de pessoas, conduz mini-treinamentos mensais de 60-90min para grupo de 4-6 Auxiliares sobre temas específicos (como analisar caso médio com ambiguidade, como negociar com cliente difícil, como usar sistema X de forma avançada), pelo menos 1-2 mentorados promovidos anualmente",
        "G": "Mentoria consolidada próxima de Assistente: desenvolve 3-4 Auxiliares simultaneamente em estágios diferentes, programa estruturado com objetivos trimestrais claros para cada mentorado, cria materiais didáticos extensivos que beneficiam time completo (biblioteca de casos de exemplo, playbooks, vídeos tutoriais), coordena programa de mentoria quando há múltiplos mentores garantindo consistência, avalia formalmente prontidão para promoção com input significativo em decisões, taxa de promoção de mentorados >30-40% anualmente demonstrando desenvolvimento acelerado"
    },
    "9. KPIs Principais (TMR, FCR, Qualidade)": {
        "A": "TMR não medido individualmente ou >10 dias (foco é aprendizado, não velocidade ainda), FCR não medido (muitos casos requerem várias interações enquanto aprende), Qualidade >70% medida por % de casos sem erros críticos que geram retrabalho, consistência ainda irregular (oscila muito semana a semana)",
        "B": "TMR ~7-9 dias (medido mas ainda acima da meta final), FCR ainda não medido consistentemente ou <60%, Qualidade >75%, redução mensurável de supervisão necessária ao longo do nível (começa precisando validar 60-70% das decisões, termina validando 30-40%), consistência melhorando (oscilação mensal está diminuindo)",
        "C": "TMR <7 dias, FCR >65%, Qualidade >80%, autonomia completa em casos padronizados (válida apenas situações atípicas <20% do tempo), mantém performance consistente mesmo em períodos de alta demanda ou quando há mudanças de processo, atinge metas em 80-90% dos meses",
        "D": "TMR <6 dias (frequentemente entre melhores 20-30% do time), FCR >70%, Qualidade >85%, consistência absoluta por 12+ meses (atinge ou supera metas em >95% dos meses), desvio padrão de performance é baixo (performance muito estável semana a semana), frequentemente é usado como benchmark interno ('veja como Fulano faz, esse é o padrão que esperamos')",
        "E": "Mantém excelência em casos simples (TMR <6d, FCR >70%, Qualidade >85%) + desenvolve performance em casos médios iniciais: TMR de casos médios ~12-15 dias (vs <7 dias que seria de Assistente experiente, mas razoável para quem está aprendendo), taxa de resolução >65% dos casos médios sem escalação adicional, não pode haver deterioração significativa de performance em casos simples ao assumir casos médios",
        "F": "Performance híbrida consolidada: mantém casos simples com TMR <6d + casos médios com TMR <12 dias e resolução >70% sem escalação, balanceia ambos os tipos mantendo qualidade >80% em ambos, consistência em 85-90% dos meses atingindo metas combinadas, demonstra que consegue gerenciar complexidade maior sem sacrificar resultado",
        "G": "Performance próxima de Assistente A-B: casos simples TMR <5.5d (top 10-20%) + casos médios TMR <10 dias e resolução >75% sem escalação, qualidade >85% em ambos tipos, consistência >90% dos meses, gap de performance vs Assistentes A-B é pequeno (<15-20% diferença), claramente pronto tecnicamente para promoção"
    },
    "10. Participação em Projetos e Melhorias": {
        "A": "Não participa de projetos ainda (foco é dominar operação básica do cargo), ocasionalmente é consultado para dar input operacional quando projeto impacta seu trabalho ('como você usa esse sistema hoje? o que é mais difícil?'), mas não tem responsabilidade ativa em projetos",
        "B": "Participa de projetos executando tarefas delegadas: recebe tarefas específicas e claras ('preencha essa planilha com dados de 50 casos', 'teste esse processo novo e dê feedback'), entrega no prazo com qualidade, contribui com ideias quando solicitado em reuniões, mas não tem ownership de workstream completo",
        "C": "Participa ativamente assumindo workstream específico: em projeto tático (3-6 meses, equipe 5-8 pessoas) assume frente específica com certa autonomia ('sou responsável por testar processo novo com 5 colegas e consolidar feedback'), coordena 1-3 pessoas na frente específica, reporta progresso semanalmente em reuniões de projeto, entrega workstream no prazo contribuindo para sucesso do projeto maior, propõe pequenas melhorias baseadas em observação de padrões (2-3 por ano)",
        "D": "Lidera mini-projetos táticos: lidera projeto pequeno/médio (2-4 meses, 3-5 pessoas, impacto 15-25% em métrica específica) com certa autonomia, cria mini-plano (objetivo + ações + cronograma + pessoas), coordena execução fazendo reuniões semanais de alinhamento, comprova impacto através de medição antes/depois, apresenta resultado em 15-20min para Assistente/Analista/Supervisor, pelo menos 1-2 projetos liderados com sucesso nos últimos 12-18 meses",
        "E": "Mantém capacidade de liderar mini-projetos + participa de projetos mais complexos liderados por Assistentes: assume workstream em projeto de médio porte (6-9 meses, 8-12 pessoas), coordena 3-5 pessoas na frente, maior visibilidade e complexidade que nível D, aprende observando como Assistentes estruturam e lideram projetos de maior escopo",
        "F": "Lidera projetos de complexidade intermediária: lidera projeto tático/médio (4-6 meses, 5-8 pessoas, R$ 30k-80k investimento, impacto 20-30%) com business case estruturado (problema + solução + custos + benefícios + ROI simples), cronograma com milestones, coordena equipe com reuniões semanais estruturadas, comprova impacto rigoroso sustentado >60 dias, apresenta em 20-30min para Coordenação, pelo menos 1 projeto/ano com sucesso documentado",
        "G": "Lidera projetos próximos de Assistente A: lidera projeto de médio porte (6-9 meses, 8-12 pessoas, R$ 80k-150k, impacto 30-40%), business case de 3-5 páginas com análise de alternativas, gestão profissional de projeto (WBS, cronograma, RACI, RAID log), gerencia stakeholders de múltiplas áreas, comprova impacto >90 dias com ROI >2:1, apresenta para Coordenação/Gerência, 1-2 projetos/ano demonstrando capacidade de transformação tática"
    }
}


CRITERIOS_ASSISTENTE = {
    "1. Tamanho e Complexidade da Carteira de Casos": {
        "A": "Carteira de 15-20 casos médios iniciais (10-12 simples residuais + 5-8 médios iniciais com ambiguidade leve), executa sob supervisão próxima do Analista (valida 70-80% das decisões críticas, check-in diário 20-30min), TMR não medido separadamente ou >15 dias, foco é aprender a tratar casos que fogem de playbooks",
        "B": "Carteira de 25-35 casos (20-25 médios + 5-10 simples residuais), executa com validação periódica (valida 40-50% das decisões, reunião semanal 30-45min vs diária), TMR ~10-12 dias para casos médios, começa a ter autonomia em casos médios padronizados",
        "C": "Carteira de 35-45 casos médios com autonomia completa no espectro de casos médios, TMR <7 dias, FCR >70%, valida apenas situações atípicas ou de alto impacto, é referência técnica para Assistentes A-B consultada 5-10x por semana",
        "D": "Carteira de 40-50 casos médios com excelência (TMR <5.5 dias, FCR >75%, prazo >97%), é referência formal consultada por todos Assistentes A-B-C (20-30x/semana), mentora 3-4 Auxiliares, frequentemente melhor performance individual do setor",
        "E": "Mantém 40-50 casos médios com excelência (TMR <5.5d, FCR >75%) + resolve 3-5 casos complexos iniciais/mês do Analista sob supervisão próxima (valida 80-90% decisões críticas nesses casos), casos complexos têm valores R$ 1.500-3.000 ou múltiplas partes envolvidas",
        "F": "Reduz para 25-35 casos médios críticos + resolve 8-12 casos complexos/mês com autonomia crescente (valida 50-60% decisões em casos complexos), casos complexos R$ 2.000-5.000, mantém excelência em ambos os escopos simultaneamente",
        "G": "Carteira mínima de 15-25 casos médios estratégicos + resolve 12-15 casos complexos/mês com autonomia 70-80%, casos complexos até R$ 5.000-8.000, atua quase como Analista A-B, pronto para promoção iminente"
    },
    "2. Autonomia e Necessidade de Supervisão": {
        "A": "Precisa de supervisão próxima constante do Analista: check-in diário de 20-30min, valida 70-80% das decisões críticas antes de executar (especialmente em casos médios que fogem de playbook), executa casos simples residuais com autonomia mas casos médios requerem validação frequente",
        "B": "Executa com acompanhamento periódico: reunião semanal de 30-45min vs diária, valida 40-50% das decisões (situações de maior impacto ou risco), toma decisões autônomas em casos médios padronizados mas valida quando há ambiguidade significativa ou valor >R$ 1.000",
        "C": "Autonomia completa em espectro de casos médios: valida apenas situações genuinamente atípicas ou de alto impacto estratégico (~20% do tempo), toma decisões sozinho em 80%+ das situações incluindo improvisação básica em casos médios, consulta Analista apenas 2-3x por semana",
        "D": "Autonomia total em casos médios + valida trabalho de outros: é quem valida decisões de Assistentes A-B-C, raramente precisa consultar Analista (apenas situações extraordinárias 1-2x por mês), toma todas as decisões dentro do escopo de casos médios sem supervisão",
        "E": "Mantém autonomia total em casos médios + desenvolve autonomia em casos complexos iniciais sob supervisão próxima: primeiros 2-3 meses valida 80-90% das decisões críticas em casos complexos, reduz gradualmente para 60-70% conforme Analista ganha confiança",
        "F": "Autonomia crescente em casos complexos: valida 50-60% das decisões em casos complexos (vs 80-90% no E), toma decisões com 60-70% informação aceitando incerteza, demonstra julgamento cada vez mais sólido, Analista precisa validar apenas situações de alto risco ou precedente",
        "G": "Autonomia 70-80% em casos complexos: valida apenas 30-40% das decisões (situações de altíssimo valor >R$ 5.000, precedentes críticos, múltiplos stakeholders complexos), atua com autonomia equivalente a Analista júnior, Analista confia em julgamento na maioria das situações"
    },
    "3. Competências em Sistemas e Ferramentas (SYSEMP/THORPE/INTELIPOST)": {
        "A": "Domina 90%+ funcionalidades operacionais do Auxiliar D + aprende funcionalidades avançadas: abre CRM, altera status complexos, transfere entre filas, cria views personalizadas com múltiplos critérios, exporta relatórios customizados, ainda precisa de ajuda ocasional em funcionalidades muito avançadas (1-2x por semana)",
        "B": "Domina 95%+ funcionalidades incluindo avançadas: cria views complexas com 5-7 critérios, relatórios customizados com filtros sofisticados, exportações em múltiplos formatos, identifica bugs com descrição clara, ajuda Auxiliares e Assistentes A com dúvidas (5-10x por semana), conhece workarounds para limitações",
        "C": "Domina 98%+ funcionalidades incluindo raras/especializadas: cria automações simples (alertas, notificações), relatórios avançados com fórmulas, integração básica com outros sistemas, é consultado por Assistentes A-B e até Auxiliares D (10-20x por semana), propõe melhorias de arquitetura ou novos campos",
        "D": "Domínio completo 100% + consultoria técnica: usa funcionalidades que apenas Analistas normalmente usam, cria workflows complexos quando sistema permite, treina Assistentes A-B-C e Auxiliares em funcionalidades avançadas (workshops 2-3h), é consultado até por Analistas sobre sistema (5-10x por semana), pode ser ponto focal com fornecedor do sistema",
        "E": "Mantém domínio completo em SYSEMP + desenvolve uso de ferramentas analíticas que Analistas usam: aprende ferramentas de BI (Looker Studio, Power BI básico), consulta banco de dados quando necessário (queries SQL simples se empresa permite), extrai e cruza dados de múltiplos sistemas para investigação de casos complexos",
        "F": "Uso avançado de ferramentas analíticas: cria dashboards básicos consolidando 3-4 sistemas, queries SQL intermediárias para análises específicas, usa ferramentas de BI para identificar padrões em 100-200 casos, exporta dados estruturados que Analistas usam em análises estratégicas",
        "G": "Uso de ferramentas próximo de Analista A-B: dashboards automatizados atualizando diariamente, queries SQL avançadas com joins de múltiplas tabelas, análises em BI que geram insights acionáveis, cria views/relatórios customizados que viram padrão do setor, competência técnica em sistemas rivaliza Analistas júnior"
    },
    "4. Excel e Análise de Dados": {
        "A": "Excel Intermediário: PROCV, SOMASES com 2-3 critérios, tabelas dinâmicas básicas, formatação condicional, gráficos simples, trabalha com bases até 2-3k linhas, cria relatórios de 1-2 páginas consolidando dados de casos médios",
        "B": "Excel Intermediário+: Tabelas dinâmicas com campos calculados, gráficos diversos (dispersão, barras empilhadas, heatmaps básicos), fórmulas aninhadas avançadas (SE + PROCV + SEERRO), formatação condicional com fórmulas, trabalha com bases até 5-10k linhas, identifica correlações simples visualmente",
        "C": "Excel Avançado Inicial: ÍNDICE+CORRESP, PROCV com correspondência aproximada, dashboards básicos com 5-8 KPIs linkados, macros gravadas (não escreve VBA mas grava e executa), trabalha com bases até 20-30k linhas, cria relatórios analíticos de 3-5 páginas com insights básicos",
        "D": "Excel Avançado: Power Query básico (importa e limpa dados de múltiplas fontes), tabelas dinâmicas avançadas (múltiplos campos calculados, segmentadores, timelines), fórmulas matriciais simples, dashboards com 10-15 KPIs inter-relacionados, macros editadas em VBA (não escritas do zero), análises com bases 30-50k linhas, apresenta insights estruturados",
        "E": "Mantém Excel Avançado + desenvolve análise estatística básica para casos complexos: calcula não apenas média mas mediana/percentis/desvio padrão, identifica outliers estatisticamente, usa correlação simples para validar hipóteses (Pearson), cria modelos simples de previsão (regressão linear básica), análises de 100-200 casos complexos",
        "F": "Excel Avançado + BI Intermediário: Power Query consolidando 3-5 fontes automaticamente, dashboards automatizados que atualizam ao refresh, macros VBA intermediárias (edita e adapta scripts existentes), estatística intermediária (teste t, análise de variância básica, regressão múltipla com 2-3 variáveis), análises de 200-400 casos com insights profundos",
        "G": "Excel Expert próximo de Analista: Power Query com transformações complexas (merge/append de múltiplas queries), VBA avançado (escreve scripts novos de 50-100 linhas), integração com APIs para importação automatizada, modelos estatísticos que Analistas usam (regressão múltipla avançada, séries temporais básicas), apresenta análises em formato executivo para Coordenação"
    },
    "5. Comunicação e Negociação com Stakeholders": {
        "A": "Contatos de média complexidade básica (10-15min): adapta tom ao contexto emocional do cliente, explica situações com ambiguidade leve sem jargões, coleta informações com perguntas abertas/fechadas estratégicas, negocia soluções simples (até 10-15% desconto, +7-10 dias prazo, cortesias pequenas), escala quando valor >R$ 500-1.000 ou cliente ameaça Reclame Aqui/Procon",
        "B": "Contatos de média complexidade consolidada (10-20min): gerencia clientes moderadamente insatisfeitos com de-escalação efetiva (60-70% resolve sem escalar), negocia soluções balanceando cliente e empresa (combinações de desconto + prazo + cortesia até R$ 1.000-1.500), coordena com transportadoras usando templates personalizados, escala quando valor >R$ 1.500 ou situação politicamente sensível",
        "C": "Contatos complexos com múltiplos stakeholders (15-25min): coordena comunicação entre cliente + transportadora + fornecedor quando aplicável, adapta mensagem para cada stakeholder (mais técnica para fornecedor, mais empática para cliente, mais assertiva para transportadora), negocia ajustes operacionais simples com transportadoras (antecipa/posterga 1-2 dias, horário específico), identifica quando situação exige escalação para Analista (>R$ 2.000, múltiplas partes com interesses muito conflitantes)",
        "D": "Comunicação estratégica em múltiplos canais (15-30min): participa de reuniões mensais com transportadoras apresentando análises de 15-20min, negocia com focais diretos de transportadoras (analistas/coordenadores), gerencia clientes VIP ou situações de crise potencial, coordena comunicação interna entre 3-4 áreas quando caso impacta múltiplos times, negocia dentro de alçada estabelecida (até R$ 2.000-2.500) autonomamente",
        "E": "Mantém comunicação nível D em casos médios + desenvolve comunicação para casos complexos iniciais: aprende a negociar situações de maior valor (R$ 3.000-5.000) e complexidade (múltiplos stakeholders com interesses conflitantes), prepara-se para negociações identificando BATNA básico, conduz conversas de 20-40min mantendo relacionamento positivo mesmo com conflito, ainda valida estratégia de comunicação crítica com Analista",
        "F": "Negociação complexa intermediária (20-40min): usa técnicas estruturadas (negociação baseada em interesses, identifica BATNA próprio e da outra parte), propõe soluções win-win criativas que expandem valor além de concessões simples, gerencia situações com assimetria de informação, negocia acordos que envolvem 3-4 partes simultaneamente (cliente + transportadora + fornecedor + áreas internas), documenta acordos com precisão criando term sheets quando apropriado",
        "G": "Negociação e comunicação executiva próxima de Analista: prepara meticulosamente para negociações complexas (análise BATNA completa, ZOPA mapeada, estratégia definida), conduz negociações de 30-60min de alto valor (até R$ 8.000-10.000), participa de reuniões estratégicas com transportadoras contribuindo ativamente (não apenas observando), gerencia stakeholders executivos ocasionalmente (coordenadores/gerentes de transportadoras, gerentes de áreas internas), competência de negociação rivaliza Analistas júnior"
    },
    "6. Análise de Causa Raiz e Resolução de Problemas Complexos": {
        "A": "Análise de casos médios iniciais: identifica problema real vs sintoma em casos com ambiguidade leve, formula 2-3 hipóteses sobre causa quando caso foge de playbook, coleta informações de 2-3 fontes sistematicamente, propõe solução consultando casos similares anteriores e validando com Analista, documenta raciocínio básico (não apenas ações mas por que tomou aquelas ações)",
        "B": "Análise estruturada de casos médios: usa metodologia básica (5 Porquês até 3-4 níveis, perguntas 'por que' iterativas), formula 2-3 hipóteses avaliando probabilidade relativa, coleta evidências de múltiplas fontes (sistemas + comunicações + documentos), toma decisões com 70-80% informação, identifica quando caso evolui para complexo e precisa escalar, documenta análise em formato semi-estruturado",
        "C": "Análise profunda multifacetada: aplica frameworks formais (5 Porquês rigoroso, Ishikawa básico identificando categorias de causas), quebra casos complexos médios em componentes gerenciáveis, formula múltiplas hipóteses concorrentes priorizando por probabilidade x impacto, usa raciocínio contrafactual básico ('se X fosse verdade deveria observar Y, não observo Y então X provavelmente não é causa'), documenta análise em 1-2 páginas estruturadas, identifica padrões em 20-30 casos similares",
        "D": "Análise sistêmica identificando padrões: além de resolver caso individual, identifica causas raiz sistêmicas em 50-100 casos (observa que 60% dos problemas tipo X vêm de causa Y específica), usa frameworks múltiplos conforme contexto (5 Porquês, Ishikawa, Análise de Pareto, FTA básico), diferencia causas raiz primárias vs secundárias vs contribuintes, propõe soluções estruturais que previnem recorrência (pequenas mudanças de processo, ajustes de sistema, treinamentos), documenta análises que servem de referência para A-B-C",
        "E": "Mantém análise profunda em casos médios + desenvolve análise para casos complexos iniciais: aprende metodologias que Analistas usam (análise contrafactual rigorosa, árvores de decisão com probabilidades, análise de cenários), investiga casos onde há múltiplas variáveis interdependentes e ambiguidade alta, coleta dados de 5-8 fontes incluindo entrevistas com stakeholders, análises levam 3-6h vs 1-2h de casos médios, ainda valida raciocínio analítico com Analista em casos críticos",
        "F": "Análise de casos complexos intermediária: conduz investigações profundas de 4-8h cruzando múltiplas fontes de evidência, entrevista 3-5 stakeholders com técnicas estruturadas (perguntas abertas exploratórias, perguntas fechadas de validação, escuta ativa), analisa dados quantitativos e qualitativos, identifica inconsistências entre versões de diferentes stakeholders e investiga discrepâncias, documenta análise em dossiê de 2-3 páginas (cronologia + stakeholders + hipóteses + evidências + recomendação), usa frameworks avançados (análise de opções com prós/contras/riscos de cada)",
        "G": "Análise de casos complexos avançada próxima de Analista: metodologias rigorosas de Analista (Ishikawa completo com todas categorias, Análise de Pareto quantitativa, raciocínio contrafactual testando hipóteses sistematicamente), investigações de 6-12h quando necessário, análises de impacto de negócio quantificadas (não apenas 'resolve o problema' mas 'problema custa R$ X, solução Y economiza R$ Z'), dossiês de 3-5 páginas que Analistas consideram 'quase nível de Analista', competência analítica rivaliza Analistas júnior"
    },
    "7. Gestão de Prazos, Priorização e Monitoramento Proativo": {
        "A": "Priorização de carteira pequena (15-20 casos): usa planilha + views de sistema para monitorar prazos, identifica casos próximos de vencer (3-5 dias antes) e age, prioriza dinamicamente considerando urgência/importância básica, comunica quando sobrecarga ameaça prazos (antes de efetivamente perder), mantém TMR >12-15 dias inicialmente mas melhora ao longo do nível",
        "B": "Priorização de carteira média (25-35 casos): múltiplas ferramentas (planilha + SYSEMP views customizadas + alertas), identifica diariamente casos próximos prazo ou travados (parados >5-7 dias sem progresso), prioriza usando matriz urgente/importante, follow-up calibrado à situação (educado após 48h, urgente após 72h, escala após 96h), mantém TMR ~10-12 dias, auto-consciência sobre performance (sabe quando está performando bem vs quando está lutando)",
        "C": "Priorização otimizada de carteira grande (35-45 casos): mantém visão consolidada de saúde da carteira (quantos em cada status, tendências, casos críticos), trabalha em lote quando eficiente (5-8 casos similares sequencialmente), identifica causas de travamento (esperando resposta de quem? bloqueado por que? preciso de qual informação?), decisão consciente de destravar ou escalar após 10 dias travado, TMR <7 dias, revisa 100% carteira semanalmente sistematicamente, raramente perde prazos (<1x por trimestre com justificativa válida)",
        "D": "Priorização de excelência em carteira máxima (40-50 casos): mantém TMR <5.5 dias (30-40% melhor que A-B-C) através de eficiência maximizada, antecipa problemas antes de virarem críticos (identifica padrões de travamento e age preventivamente), absorve picos de 60-70 casos temporariamente sem deterioração significativa de qualidade, comunica proativamente quando capacidade está no limite, nunca perde prazos sem força maior, é modelo de gestão de carteira para todos Assistentes",
        "E": "Mantém gestão excelente de 40-50 casos médios + aprende gestão de 3-5 casos complexos iniciais: desenvolve capacidade de balancear casos médios urgentes vs casos complexos importantes mas menos urgentes, aprende a estimar tempo necessário para investigação de casos complexos (pode levar 3-6h vs 30-60min de casos médios), ajusta priorização quando caso complexo se mostra mais difícil que esperado, não permite que casos complexos causem deterioração de TMR em casos médios",
        "F": "Priorização híbrida sofisticada (25-35 médios + 8-12 complexos): balanceia usando critérios múltiplos (urgência + importância + esforço + impacto + risco), aloca tempo de forma estratégica (blocos de 3-4h para casos complexos que requerem análise profunda, gaps de 30-60min para casos médios entre blocos), identifica trade-offs e toma decisões conscientes (pode precisar sacrificar TMR de caso médio menos crítico para garantir qualidade de caso complexo mais importante), mantém performance competitiva em ambos simultaneamente",
        "G": "Priorização estratégica de portfólio completo (15-25 médios + 12-15 complexos): visão consolidada e dinâmica ajustando ao longo do dia conforme situação evolui, identifica antecipadamente quando carga é insustentável e negocia redistribuição ou extensão de prazo antes de comprometer qualidade, priorização próxima de Analista júnior (considera não apenas urgência/importância mas também impacto estratégico no negócio, precedentes, visibilidade executiva), mantém TMR competitivo em ambos tipos (médios <6d, complexos <10d)"
    },
    "8. Mentoria e Desenvolvimento de Pessoas": {
        "A": "Mentoria informal de Auxiliares quando solicitado: ajuda ocasionalmente quando Auxiliares têm dúvidas (2-3x por semana, 10-15min cada), mas ainda não tem responsabilidade formal de desenvolvimento, foco principal é desenvolver competências próprias primeiro antes de ensinar sistematicamente outros",
        "B": "Mentoria estruturada de 1-2 Auxiliares E-F: rituais básicos (reunião quinzenal de 30-45min, shadowing ocasional), valida 20-30% dos casos do mentorado quando solicitado, fornece feedback sobre decisões e abordagem, compartilha frameworks e técnicas que usa para casos médios, feedback positivo dos mentorados sobre utilidade (>3.8/5.0)",
        "C": "Mentoria formal de 2-3 Auxiliares E-F-G: rituais consistentes (reunião quinzenal de 60min dedicada a desenvolvimento + coaching situacional 3-5x por semana quando surgem dúvidas), valida 30-40% dos casos médios que mentorados estão assumindo, fornece feedback estruturado balanceado (3 pontos positivos : 1 ponto de melhoria), adapta estilo ao perfil do mentorado (analítico vs intuitivo, confiante vs inseguro), documenta progresso e reporta evolução trimestralmente, pelo menos 1 mentorado promovido nos últimos 12-18 meses",
        "D": "Mentoria abrangente de 3-4 Auxiliares + referência para Assistentes A-B: mentora 3-4 Auxiliares E-F-G formalmente + fornece coaching situacional para Assistentes A-B quando solicitado (5-10x por semana), rituais estruturados (reunião individual quinzenal 60min + shadowing bidirecional semanal + validação 40-50% casos críticos), cria materiais didáticos (guias de 2-3 páginas sobre como tratar tipo específico de caso médio, vídeos tutoriais 10-15min, casos de estudo detalhados), conduz mini-treinamentos mensais 60-90min para grupos de 4-6 pessoas, pelo menos 1-2 mentorados promovidos anualmente",
        "E": "Mantém mentoria nível D de 3-4 Auxiliares + começa mentoria informal de 1-2 Assistentes A-B: coaching situacional quando Assistentes júnior enfrentam casos médios complexos ou atípicos (acompanha análise, valida raciocínio, fornece frameworks adicionais), compartilha técnicas de análise de casos complexos que está aprendendo com Analista, delega casos médios com supervisão para desenvolver Auxiliares G e Assistentes A",
        "F": "Mentoria ampliada multi-nível: 2-3 Auxiliares E-F-G + 1-2 Assistentes A-B-C, investe 15-20% do tempo (12-16h/mês) em desenvolvimento de pessoas, conduz treinamentos coletivos trimestrais de 2-4h sobre análise de casos complexos ou negociação avançada, cria biblioteca de conhecimento (10-15 casos de estudo documentados, 5-8 playbooks de casos médios complexos, múltiplos vídeos tutoriais), avalia prontidão para promoção fornecendo input formal significativo, 2-3 mentorados promovidos anualmente",
        "G": "Mentoria consolidada próxima de Analista: desenvolve 4-6 pessoas simultaneamente (2-3 Auxiliares + 2-3 Assistentes) em estágios diferentes, programa estruturado com objetivos trimestrais claros e métricas de progresso para cada mentorado, coordena programa de mentoria quando há múltiplos mentores (garante consistência de abordagem e calibração), prepara sucessores intencionalmente para assumir área funcional quando for promovido, taxa de promoção >30-40% dos mentorados anualmente, feedback de mentorados >4.5/5.0, competência de desenvolvimento rivaliza Analistas júnior"
    },
    "9. KPIs Principais (TMR, FCR, Qualidade de Resolução)": {
        "A": "TMR >12-15 dias inicialmente (casos médios naturalmente mais lentos que simples), FCR não medido consistentemente ou <60%, Qualidade >75% (% casos resolvidos sem retrabalho ou escalação por erro), valida 70-80% decisões críticas ainda, foco é desenvolver competência não velocidade",
        "B": "TMR ~10-12 dias, FCR 60-65%, Qualidade >80%, valida 40-50% decisões (redução vs 70-80% do A), mantém performance razoável mesmo em períodos de maior demanda, atinge metas em 70-80% dos meses, oscilação mensal está diminuindo (ganhando consistência)",
        "C": "TMR <7 dias, FCR >70%, Qualidade >85%, valida apenas 20% decisões (situações genuinamente atípicas), mantém performance consistente mesmo com carteira grande (35-45 casos) e em picos de demanda, atinge ou supera metas em 85-90% dos meses, desvio padrão baixo (performance estável semana a semana)",
        "D": "TMR <5.5 dias (frequentemente top 20% do time), FCR >75%, Qualidade >90%, autonomia quase total, consistência absoluta por 12+ meses (atinge metas em >95% dos meses), absorve picos de até 60-70 casos sem deterioração significativa, é benchmark interno ('veja performance do Fulano, esse é o padrão'), desvio padrão muito baixo",
        "E": "Mantém excelência em casos médios (TMR <5.5d, FCR >75%, Qualidade >90%) + desenvolve performance em casos complexos iniciais: TMR casos complexos ~18-20 dias (vs <12 que seria de Analista experiente), taxa resolução >65% casos complexos sem escalação adicional para Analista sênior, não pode haver deterioração significativa de performance em casos médios ao assumir complexos (máximo 10-15% piora temporária aceitável nos primeiros 2-3 meses)",
        "F": "Performance híbrida consolidada: casos médios TMR <6d + casos complexos TMR <15 dias e resolução >70-75%, qualidade >85% em ambos tipos, balanceia ambos mantendo metas combinadas, consistência em 85-90% dos meses, demonstra que consegue gerenciar maior complexidade sem sacrificar resultado, gap vs Analistas A-B está diminuindo",
        "G": "Performance próxima de Analista A-B: casos médios TMR <6d (top 10-20%) + casos complexos TMR <12 dias e resolução >75-80%, qualidade >88% em ambos, consistência >90% dos meses atingindo metas, gap de performance vs Analistas A-B é pequeno (<20% diferença), claramente pronto tecnicamente para promoção, desempenho já rivaliza Analistas júnior"
    },
    "10. Liderança de Projetos e Iniciativas de Melhoria": {
        "A": "Participa de projetos executando tarefas delegadas: recebe workstream ou tarefas específicas em projeto tático (4-6 meses, 6-10 pessoas), executa com qualidade e no prazo, contribui com perspectiva operacional quando solicitado, mas não tem ownership de frente completa ainda, propõe pequenas melhorias ocasionalmente (1-2 por ano)",
        "B": "Assume workstream específico em projetos táticos: em projeto de médio porte (6-9 meses, 8-12 pessoas) assume frente completa com autonomia crescente, coordena 2-4 pessoas na frente, reporta progresso semanal em reuniões de projeto, entrega workstream no prazo com qualidade, identifica oportunidades de melhoria baseadas em padrões (2-3 propostas por ano, pelo menos 1 implementada)",
        "C": "Lidera projetos táticos pequenos/médios: lidera projeto completo (4-6 meses, 4-6 pessoas, impacto 20-30%) com autonomia supervisionada, cria plano estruturado (objetivo SMART + ações + cronograma + pessoas + recursos), coordena execução com reuniões semanais de 45-60min, gerencia expectativas de stakeholders comunicando progresso mensalmente, comprova impacto através de medição antes/depois sustentada >60 dias, apresenta resultado 20-30min para Analista/Supervisor, pelo menos 1-2 projetos com sucesso documentado nos últimos 12-18 meses",
        "D": "Lidera múltiplos projetos táticos ou projetos de maior complexidade: lidera 2-3 projetos pequenos simultaneamente OU 1 projeto médio/grande (6-12 meses, 8-15 pessoas, R$ 100k-200k investimento, impacto 30-40%), business case estruturado de 3-5 páginas (problema quantificado + solução + alternativas consideradas + benefícios + custos + ROI), gestão profissional (cronograma com milestones, RACI, RAID log, steering mensal), gerencia stakeholders de 3-4 áreas diferentes, comprova impacto rigoroso >90 dias com ROI >2:1, apresenta para Coordenação 30-45min, pelo menos 1-2 projetos grandes/ano com impacto documentado",
        "E": "Mantém capacidade de liderar projetos táticos nível D + participa de projetos estratégicos liderados por Analistas: assume workstream significativo em projeto corporativo (9-15 meses, 15-25 pessoas, R$ 300k-600k), coordena 5-8 pessoas na frente específica, maior visibilidade e complexidade política (múltiplas áreas, stakeholders executivos), reporta para Analista líder do projeto mas com autonomia significativa na frente, aprende observando como Analistas estruturam projetos transformacionais",
        "F": "Lidera projetos de médio/grande porte: lidera projeto transformacional menor (9-12 meses, 10-18 pessoas, R$ 200k-400k, impacto 35-45%), business case robusto 5-8 páginas com análise de riscos detalhada e plano de mitigação, metodologia profissional PMI/Agile adaptada, governance com steering committee trimestral, gerencia stakeholders de 5-6 áreas incluindo liderança sênior (Coordenação/Gerência), change management estruturado (comunicação multi-canal, treinamentos, champions network), comprova impacto transformacional sustentado >6 meses ROI >2.5:1, apresenta para Gerência/Diretoria 45-60min",
        "G": "Lidera projetos estratégicos próximos de Analista: lidera projeto de grande porte (12-18 meses, 15-25 pessoas, R$ 400k-800k, impacto >50%), business case executivo 8-12 páginas defendendo investimento significativo, coordena equipe grande com sub-líderes, gerencia complexidade política alta (múltiplos VPs/Diretores como stakeholders), apresenta em steering executivo mensalmente, change management profissional em escala (impacta 50-100 pessoas), impacto documentado >R$ 300k-500k de valor criado ou custo evitado, competência de liderança de projetos rivaliza Analistas júnior"
    }
}



# Inicializar session_state para armazenar respostas
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}
if 'nome_avaliado' not in st.session_state:
    st.session_state.nome_avaliado = ""
if 'selecoes_temp' not in st.session_state:
    st.session_state.selecoes_temp = {}


# Seleção de cargo
if 'cargo_selecionado' not in st.session_state:
    st.session_state.cargo_selecionado = None

if not st.session_state.cargo_selecionado:
    st.markdown("### 🎯 Selecione o Cargo")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Auxiliar Operacional", use_container_width=True, type="primary"):
            st.session_state.cargo_selecionado = "Auxiliar Operacional"
            st.rerun()
    
    with col2:
        if st.button("📋 Assistente Operacional", use_container_width=True, type="primary"):
            st.session_state.cargo_selecionado = "Assistente Operacional"
            st.rerun()
    
    st.stop()  # Para aqui se cargo não foi selecionado

# Mostrar cargo selecionado
st.success(f"**Cargo:** {st.session_state.cargo_selecionado}")

# Selecionar critérios baseado no cargo
criterios = CRITERIOS_AUXILIAR if st.session_state.cargo_selecionado == "Auxiliar Operacional" else CRITERIOS_ASSISTENTE


# Campo de nome FORA do formulário para atualizar em tempo real

st.markdown("### 👤 Identificação")

col1, col2, col3 = st.columns(3)

with col1:
    nome_avaliado = st.text_input(
        "Nome do Avaliado:",
        value=st.session_state.nome_avaliado,
        key="nome_input"
    )
    st.session_state.nome_avaliado = nome_avaliado

with col2:
    setor = st.text_input(
        "Setor:",
        value=st.session_state.get('setor', ''),
        key="setor_input"
    )
    st.session_state.setor = setor

with col3:
    avaliador = st.text_input(
        "Nome do Avaliador:",
        value=st.session_state.get('avaliador', ''),
        key="avaliador_input"
    )
    st.session_state.avaliador = avaliador

st.markdown("---")
st.markdown("### 📝 Selecione o nível que melhor descreve o profissional em cada critério:")
st.markdown("")

# Containers para cada critério FORA do formulário
for idx, (criterio, niveis) in enumerate(criterios.items()):
    st.markdown(f"#### {criterio}")
    
    # Criar opções formatadas com descrições completas
    opcoes_display = ["Selecione..."]
    opcoes_map = {}  # Mapear display -> nível
    
    for nivel, descricao in niveis.items():
        # Truncar descrição para o dropdown (150 caracteres)
        desc_truncada = descricao[:150] + "..." if len(descricao) > 150 else descricao
        opcao_formatada = f"{nivel} - {desc_truncada}"
        opcoes_display.append(opcao_formatada)
        opcoes_map[opcao_formatada] = nivel
    
    # Selectbox para escolher o nível (FORA do form)
    opcao_selecionada = st.selectbox(
        f"Escolha o nível:",
        opcoes_display,
        key=f"select_{criterio}_{idx}",
        index=0
    )
    
    # Se um nível foi selecionado, mostrar descrição completa IMEDIATAMENTE
    if opcao_selecionada != "Selecione...":
        nivel_selecionado = opcoes_map[opcao_selecionada]
        # Mostrar descrição completa em um container azul
        st.info(f"**📖 Descrição completa do Nível {nivel_selecionado}:**\n\n{niveis[nivel_selecionado]}")
        st.session_state.selecoes_temp[criterio] = nivel_selecionado
    elif criterio in st.session_state.selecoes_temp:
        # Remover se foi desmarcado
        del st.session_state.selecoes_temp[criterio]
    
    st.markdown("---")

# Botão para calcular FORA do formulário
if st.button("🎯 Calcular Enquadramento", use_container_width=True, type="primary"):
    # Validações
    if not nome_avaliado or nome_avaliado.strip() == "":
        st.error("⚠️ Por favor, preencha o nome do colaborador avaliado.")
    elif len(st.session_state.selecoes_temp) < len(criterios):
        st.error(f"⚠️ Por favor, selecione um nível para todos os critérios. Você selecionou {len(st.session_state.selecoes_temp)} de {len(criterios)}.")
    else:
        # Copiar seleções temporárias para respostas definitivas
        st.session_state.respostas = st.session_state.selecoes_temp.copy()
        st.session_state.nome_avaliado = nome_avaliado
        st.rerun()

# Processar resultado se já foi calculado
if len(st.session_state.respostas) == len(criterios) and st.session_state.nome_avaliado:
        st.markdown("---")
        st.markdown(f"## 🎯 Resultado da Avaliação - {st.session_state.nome_avaliado}")
        st.markdown("")
        
        # Contar frequência de cada nível
        niveis_selecionados = list(st.session_state.respostas.values())
        contagem = Counter(niveis_selecionados)
        
        # Encontrar todos os níveis com a maior frequência (para detectar empates)
        max_frequencia = max(contagem.values())
        niveis_mais_frequentes = [nivel for nivel, freq in contagem.items() if freq == max_frequencia]
        
        # Verificar se há empate
        if len(niveis_mais_frequentes) == 1:
            nivel_final = niveis_mais_frequentes[0]
            metodo_usado = "Moda Estatística"
            observacao_empate = ""
        else:
            # Há empate - aplicar critérios de desempate
            st.warning("⚠️ Empate detectado! Aplicando critérios de desempate...")
            
            # Critérios de desempate em ordem de prioridade
            criterios_desempate = [
                "1. Tamanho e Complexidade da Carteira de Casos",
                "9. KPIs Principais (TMR, FCR, Qualidade)",
                "2. Autonomia e Necessidade de Supervisão"
            ]
            
            # Coletar os níveis dos critérios de desempate
            niveis_desempate = []
            for crit in criterios_desempate:
                if crit in st.session_state.respostas:
                    niveis_desempate.append(st.session_state.respostas[crit])
            
            # Contar qual dos níveis empatados aparece mais nos critérios de desempate
            contagem_desempate = Counter([n for n in niveis_desempate if n in niveis_mais_frequentes])
            
            if contagem_desempate:
                nivel_final = contagem_desempate.most_common(1)[0][0]
                metodo_usado = "Critérios de Desempate"
                observacao_empate = f"Empate entre: {', '.join(niveis_mais_frequentes)}. Resolvido pelos critérios de desempate."
            else:
                # Se mesmo assim não resolver, pega o primeiro dos empatados
                nivel_final = sorted(niveis_mais_frequentes)[0]
                metodo_usado = "Ordem Alfabética (empate não resolvido)"
                observacao_empate = f"Empate entre: {', '.join(niveis_mais_frequentes)}. Considere análise manual."
        
        # Exibir resultado em destaque
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success(f"""
            ### 🏆 Enquadramento Sugerido: Nível {nivel_final}
            
            **Método:** {metodo_usado}
            
            **Frequência:** {max_frequencia} de {len(criterios)} critérios
            """)
            
            if observacao_empate:
                st.info(f"ℹ️ {observacao_empate}")
        
        # Mostrar distribuição detalhada
        st.markdown("### 📊 Distribuição por Nível")
        
        # Criar colunas para mostrar a contagem
        cols = st.columns(7)
        niveis_ordenados = ['A', 'A-B', 'B', 'C', 'D', 'E', 'F', 'G']
        for idx, nivel in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G']):
            with cols[idx]:
                # Contar incluindo A-B como A ou B conforme apropriado
                count = contagem.get(nivel, 0)
                if nivel in ['A', 'B'] and 'A-B' in contagem:
                    count += contagem.get('A-B', 0)
                
                if nivel == nivel_final or (nivel in ['A', 'B'] and nivel_final == 'A-B'):
                    st.metric(label=f"Nível {nivel}", value=count, delta="Predominante")
                else:
                    st.metric(label=f"Nível {nivel}", value=count)
        
        # Mostrar tabela de consolidação
        st.markdown("### 📋 Tabela de Consolidação")
        
        # Adicionar resumo da contagem ANTES da tabela
        st.markdown("#### Resumo da Contagem por Nível:")
        col_resumo1, col_resumo2 = st.columns(2)
        
        with col_resumo1:
            for nivel in ['A', 'B', 'C', 'D']:
                count = contagem.get(nivel, 0)
                if nivel in ['A', 'B'] and 'A-B' in contagem:
                    count += contagem.get('A-B', 0)
                st.write(f"**Nível {nivel}:** {count} {'vez' if count == 1 else 'vezes'}")
        
        with col_resumo2:
            for nivel in ['E', 'F', 'G']:
                count = contagem.get(nivel, 0)
                st.write(f"**Nível {nivel}:** {count} {'vez' if count == 1 else 'vezes'}")
        
        if 'A-B' in contagem:
            st.write(f"**Nível A-B:** {contagem.get('A-B', 0)} {'vez' if contagem.get('A-B', 0) == 1 else 'vezes'}")
        
        st.markdown("---")
        
        # Criar tabela formatada
        import pandas as pd
        
        dados_tabela = []
        for idx, (criterio, nivel) in enumerate(st.session_state.respostas.items(), 1):
            dados_tabela.append({
                "#": idx,
                "Critério": criterio.replace(f"{idx}. ", ""),
                "Nível Marcado": nivel
            })
        
        df_consolidacao = pd.DataFrame(dados_tabela)
        st.dataframe(df_consolidacao, use_container_width=True, hide_index=True)
        
        # Mostrar resumo detalhado
        st.markdown("### 📖 Resumo Detalhado das Respostas")
        for criterio, nivel in st.session_state.respostas.items():
            with st.expander(f"{criterio}: **Nível {nivel}**"):
                # Encontrar o nome do critério sem o número
                criterio_nome = criterio
                st.write(criterios[criterio_nome][nivel])
        
        # Análise de consistência
        st.markdown("### 💡 Análise de Consistência")
        
        # Calcular spread dos níveis
        niveis_numericos = {'A': 1, 'A-B': 1.5, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
        valores_numericos = [niveis_numericos.get(n, 0) for n in niveis_selecionados if n in niveis_numericos]
        
        if valores_numericos:
            spread = max(valores_numericos) - min(valores_numericos)
            media_nivel = sum(valores_numericos) / len(valores_numericos)
            
            if spread <= 1:
                st.success(f"✅ **Alta Consistência**: O profissional demonstra consistência em praticamente todos os critérios no nível {nivel_final}. Avaliação muito coesa.")
            elif spread <= 2:
                st.info(f"ℹ️ **Consistência Boa**: O profissional está predominantemente no nível {nivel_final}, com pequenas variações em alguns critérios. Isso é natural e esperado.")
            elif spread <= 3:
                st.warning(f"⚠️ **Consistência Moderada**: O profissional apresenta variação de até 3 níveis entre critérios. Recomenda-se identificar os critérios mais fracos para plano de desenvolvimento focado.")
            else:
                st.error(f"⚠️ **Baixa Consistência**: O profissional apresenta grande variação entre níveis (spread de {int(spread)} níveis). Recomenda-se análise mais detalhada e plano de desenvolvimento individualizado.")
        
        # Próximos passos
        st.markdown("### 🎯 Próximos Passos Recomendados")
        
        if max_frequencia >= len(criterios) * 0.8:
            st.success(f"""
            **Situação Ideal**: O profissional demonstra consistência sólida no nível {nivel_final}.
            
            **Recomendações:**
            - Validar o enquadramento com evidências concretas dos últimos 3-6 meses
            - Se confirmado, formalizar o posicionamento no nível {nivel_final}
            - Estabelecer objetivos claros para progressão ao próximo nível
            """)
        elif max_frequencia >= len(criterios) * 0.6:
            st.info(f"""
            **Situação Normal**: O profissional está predominantemente no nível {nivel_final}, mas com variações.
            
            **Recomendações:**
            - Identificar os critérios abaixo do nível predominante
            - Criar plano de desenvolvimento focado nesses critérios específicos
            - Estabelecer timeline de 3-6 meses para revisão
            """)
        else:
            st.warning(f"""
            **Atenção Necessária**: Grande variação entre níveis detectada.
            
            **Recomendações:**
            - Realizar conversa de calibração entre gestor e colaborador
            - Revisar as evidências para cada critério com mais profundidade
            - Considerar se o colaborador está em transição entre níveis
            - Criar plano de desenvolvimento individualizado e detalhado
            - Agendar revisão em 60-90 dias
            """)
        
        # Botão para gerar e baixar PDF
        st.markdown("---")
        st.markdown("### 📄 Exportar Resultado")
        
        col_pdf1, col_pdf2, col_pdf3 = st.columns([1, 2, 1])
        with col_pdf2:
            if st.button("📥 Gerar e Baixar PDF", use_container_width=True, type="primary"):
                with st.spinner("Gerando PDF..."):
                    try:
                        pdf_buffer = gerar_pdf(
                            nome_avaliado=st.session_state.nome_avaliado,
                            respostas=st.session_state.respostas,
                            nivel_final=nivel_final,
                            metodo_usado=metodo_usado,
                            max_frequencia=max_frequencia,
                            contagem=contagem,
                            criterios_dict=criterios,
                            observacao_empate=observacao_empate
                        )
                        
                        # Nome do arquivo
                        nome_arquivo = f"Avaliacao_{st.session_state.nome_avaliado.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                        
                        st.download_button(
                            label="📄 Clique aqui para baixar o PDF",
                            data=pdf_buffer,
                            file_name=nome_arquivo,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        st.success("✅ PDF gerado com sucesso!")
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar PDF: {str(e)}")
                        st.info("Certifique-se de que todas as bibliotecas estão instaladas: pip install reportlab")

# Sidebar com informações
with st.sidebar:
    st.markdown("## ℹ️ Como usar")
    st.markdown("""
    **PARA O COLABORADOR (Auto-avaliação):**
    - Leia cada critério com atenção
    - Para cada um, leia TODOS os descritores (A-G)
    - Marque o que melhor representa sua realidade atual
    - Seja honesto - não marque o nível que "gostaria de estar"
    - Se em dúvida entre dois níveis, marque o mais conservador
    - Tempo estimado: 15-20 minutos
    
    **PARA O GESTOR:**
    - Use evidências dos últimos 3-6 meses
    - Seja objetivo - marque o que observa consistentemente
    - Compare com outros Auxiliares do mesmo nível
    - Tempo estimado: 20-25 minutos por colaborador
    """)
    
    st.markdown("---")
    st.markdown("## 📈 Critério de Enquadramento")
    st.markdown("""
    **Método Principal: MODA ESTATÍSTICA**
    
    O nível final é o que aparece com maior frequência nas respostas.
    
    **Critérios de Desempate** (em ordem):
    1. Carteira de Casos (mais objetivo)
    2. KPIs (dados concretos)
    3. Autonomia (fundamental)
    
    **IMPORTANTE:**
    - Esta é uma ferramenta indicativa
    - Decisões formais usam o Framework completo
    - Divergências são oportunidades de conversa
    """)
    
    if st.button("🔄 Resetar Avaliação", type="secondary"):
        # Limpar TUDO do session_state
        keys_to_delete = [key for key in st.session_state.keys()]
        for key in keys_to_delete:
            del st.session_state[key]
        st.success("✅ Avaliação resetada! Recarregando...")
        st.rerun()

