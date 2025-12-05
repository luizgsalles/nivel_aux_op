# Sistema de Avaliação de Enquadramento - Auxiliar Operacional

## 🎯 Descrição

Sistema completo para avaliação de enquadramento de profissionais em níveis (A-G) baseado em 10 critérios objetivos de competências, utilizando moda estatística com critérios de desempate automáticos.

## 📋 Funcionalidades

- ✅ Avaliação em 10 critérios detalhados
- ✅ 7 níveis de progressão (A, A-B, B, C, D, E, F, G)
- ✅ Cálculo automático por **moda estatística**
- ✅ Sistema de **desempate automático** em 3 níveis
- ✅ Análise de consistência das respostas
- ✅ Recomendações personalizadas de desenvolvimento
- ✅ Tabela de consolidação completa
- ✅ Interface intuitiva e responsiva
- ✅ Instruções de uso integradas para colaborador e gestor

## 🚀 Como Usar

### Instalação

```bash
# Instalar dependências
pip install streamlit pandas
```

### Executar Localmente

```bash
# Rodar a aplicação
streamlit run avaliacao_enquadramento.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

### Executar no Terminal

```bash
streamlit run avaliacao_enquadramento.py --server.headless true
```

## 📊 Critérios de Avaliação

1. **Tamanho e Complexidade da Carteira de Casos**
2. **Autonomia e Necessidade de Supervisão**
3. **Competências em Sistemas (SYSEMP/THORPE/INTELIPOST)**
4. **Excel e Análise de Dados**
5. **Comunicação com Cliente/Transportadora**
6. **Gestão de Prazos e Priorização**
7. **Análise e Resolução de Problemas**
8. **Mentoria e Desenvolvimento de Outros**
9. **KPIs Principais (TMR, FCR, Qualidade)**
10. **Participação em Projetos e Melhorias**

## 🎓 Níveis de Progressão

- **A**: Iniciante - Supervisão direta constante, aprendendo processos básicos
- **A-B**: Transição - Entre A e B, ainda não mentora formalmente
- **B**: Básico - Validação periódica, autonomia em tarefas rotineiras
- **C**: Autônomo - Autonomia completa em casos simples padronizados
- **D**: Referência - Excelência em casos simples, mentor de A-B-C
- **E**: Transição - Mantém excelência em simples + inicia casos médios
- **F**: Intermediário - Domínio crescente de casos médios
- **G**: Avançado - Quase Assistente, autonomia 70-80% em casos médios

## 🧮 Lógica de Enquadramento

### Método Principal: Moda Estatística
O sistema conta quantas vezes cada nível (A-G) foi selecionado. O nível que aparece mais vezes é o enquadramento sugerido.

### Critérios de Desempate (em ordem de prioridade)
Quando há empate na moda, o sistema aplica automaticamente:

1. **Critério 1** - Tamanho e Complexidade da Carteira (mais objetivo e mensurável)
2. **Critério 9** - KPIs Principais (dados concretos de performance)
3. **Critério 2** - Autonomia e Supervisão (fundamental para progressão)

O sistema verifica qual dos níveis empatados aparece em 2 dos 3 critérios de desempate.

## 📈 Análise de Consistência

O sistema calcula automaticamente o "spread" entre os níveis marcados:

- **Spread ≤ 1**: Alta consistência ✅
- **Spread ≤ 2**: Consistência boa ℹ️
- **Spread ≤ 3**: Consistência moderada ⚠️
- **Spread > 3**: Baixa consistência - requer análise detalhada ⚠️

## 👥 Público-Alvo

### Para Colaboradores (Auto-avaliação)
- Tempo estimado: 15-20 minutos
- Leia TODOS os descritores de cada critério
- Seja honesto sobre sua realidade atual
- Em dúvida, marque o nível mais conservador

### Para Gestores (Avaliação)
- Tempo estimado: 20-25 minutos por colaborador
- Use evidências concretas dos últimos 3-6 meses
- Compare com outros Auxiliares do mesmo nível
- Seja objetivo - marque o observado, não o potencial

## ⚠️ Observações Importantes

- **Ferramenta Indicativa**: Gera resultado sugerido, não decisão final de promoção
- **Framework Completo**: Decisões formais usam o Framework de Promoção mais robusto
- **Divergências**: São oportunidades de conversa entre colaborador e gestor
- **Calibração**: Recomenda-se calibração entre gestores antes do uso extensivo

## 🔄 Próximos Passos Após Avaliação

1. **Resultado Consistente (80%+ no mesmo nível)**
   - Validar com evidências concretas
   - Formalizar posicionamento
   - Estabelecer objetivos para próximo nível

2. **Resultado com Variação (60-80% no nível predominante)**
   - Identificar critérios abaixo do predominante
   - Criar plano de desenvolvimento focado
   - Revisão em 3-6 meses

3. **Resultado Disperso (<60% de consistência)**
   - Conversa de calibração gestor-colaborador
   - Revisar evidências com profundidade
   - Plano de desenvolvimento individualizado
   - Revisão em 60-90 dias

## 🛠️ Extensibilidade

Para adicionar novos critérios, edite o dicionário `criterios` no arquivo Python:

```python
criterios = {
    "11. Novo Critério": {
        "A": "Descrição do nível A",
        "B": "Descrição do nível B",
        # ... demais níveis
    }
}
```

## 📊 Saídas do Sistema

1. **Nível Sugerido**: Baseado em moda estatística
2. **Método Usado**: Moda, Desempate ou Ordem Alfabética
3. **Distribuição**: Gráfico de frequência por nível
4. **Tabela de Consolidação**: Todos os critérios e níveis marcados
5. **Análise de Consistência**: Spread e recomendações
6. **Próximos Passos**: Baseados no padrão de resposta

## 💡 Melhorias Futuras Possíveis

- [ ] Exportação de resultados em PDF
- [ ] Histórico de avaliações ao longo do tempo
- [ ] Comparação entre auto-avaliação e avaliação do gestor
- [ ] Plano de desenvolvimento automático baseado em gaps
- [ ] Dashboard consolidado com múltiplos colaboradores
- [ ] Integração com sistema de metas e PDIs

## 📝 Licença

Uso interno - Controladoria / Gestão de Pessoas
