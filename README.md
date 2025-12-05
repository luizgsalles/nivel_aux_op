# Sistema de Avaliação de Enquadramento - Auxiliar Operacional

## 🎯 Descrição

Sistema completo para avaliação de enquadramento de profissionais em níveis (A-G) baseado em 10 critérios objetivos de competências, utilizando moda estatística com critérios de desempate automáticos. Interface interativa em tempo real que mostra descrições completas ao selecionar cada opção.

## 📋 Funcionalidades

- ✅ **Interface em tempo real** - Descrições aparecem instantaneamente ao selecionar
- ✅ Campo para nome do avaliado
- ✅ Avaliação em 10 critérios detalhados
- ✅ 7 níveis de progressão (A, A-B, B, C, D, E, F, G)
- ✅ Cálculo automático por **moda estatística**
- ✅ Sistema de **desempate automático** em 3 níveis
- ✅ Análise de consistência das respostas
- ✅ Recomendações personalizadas de desenvolvimento
- ✅ Tabela de consolidação completa
- ✅ **Exportação em PDF profissional**
- ✅ Interface intuitiva e responsiva
- ✅ Instruções de uso integradas para colaborador e gestor

## 🚀 Como Usar

### Instalação

```bash
# Instalar dependências
pip install streamlit pandas reportlab
```

Ou usando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
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

## 💡 Como Funciona a Interface

### Experiência do Usuário

1. **Preencha o nome** do colaborador no campo no topo
2. **Para cada critério:**
   - Abra o dropdown "Escolha o nível"
   - Veja a prévia de cada descrição (150 caracteres)
   - **Ao selecionar, a descrição COMPLETA aparece imediatamente** numa caixa azul
   - Leia a descrição completa para confirmar
3. **Clique em "Calcular Enquadramento"** após preencher todos os 10 critérios
4. **Veja os resultados** com análise completa
5. **Exporte em PDF** para compartilhar ou arquivar

### Diferencial: Atualização em Tempo Real

A interface **não usa formulários tradicionais**. Cada seleção atualiza instantaneamente, mostrando a descrição completa do nível escolhido. Isso permite que o avaliador:
- Leia todas as descrições antes de decidir
- Compare diferentes níveis facilmente
- Tome decisões mais informadas
- Tenha uma experiência fluida e intuitiva

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
- **A-B**: Transição - Entre A e B, ainda não mentora formalmente (apenas critério 8)
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

- **Spread ≤ 1**: Alta consistência ✅ - Profissional muito bem posicionado
- **Spread ≤ 2**: Consistência boa ℹ️ - Situação normal e esperada
- **Spread ≤ 3**: Consistência moderada ⚠️ - Requer plano de desenvolvimento focado
- **Spread > 3**: Baixa consistência ⚠️ - Necessita análise detalhada

## 📄 Exportação em PDF

O sistema gera um PDF profissional contendo:

- 📋 **Cabeçalho** - Nome do avaliado, data e hora da avaliação
- 🎯 **Resultado Principal** - Nível sugerido, método usado, frequência
- 📊 **Distribuição por Nível** - Tabela com contagem de cada nível
- 📝 **Tabela de Consolidação** - Todos os critérios e níveis marcados
- 📖 **Detalhamento Completo** - Descrição de cada critério e nível selecionado
- 🎨 **Layout Profissional** - Cores, formatação e estrutura organizada

O PDF é ideal para:
- Compartilhar com o colaborador avaliado
- Arquivar no histórico de avaliações
- Apresentar em reuniões de calibração
- Documentar processos de promoção

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

### 1. Resultado Consistente (80%+ no mesmo nível)
   - Validar com evidências concretas
   - Formalizar posicionamento
   - Estabelecer objetivos para próximo nível

### 2. Resultado com Variação (60-80% no nível predominante)
   - Identificar critérios abaixo do predominante
   - Criar plano de desenvolvimento focado
   - Revisão em 3-6 meses

### 3. Resultado Disperso (<60% de consistência)
   - Conversa de calibração gestor-colaborador
   - Revisar evidências com profundidade
   - Plano de desenvolvimento individualizado
   - Revisão em 60-90 dias

## 🛠️ Tecnologias Utilizadas

- **Streamlit** - Framework web interativo para Python
- **Pandas** - Manipulação e análise de dados
- **ReportLab** - Geração profissional de PDFs
- **Python 3.8+** - Linguagem de programação

## 🔧 Resolução de Problemas

### ModuleNotFoundError: No module named 'reportlab'
```bash
pip install reportlab
```

### Botão de reset não limpa as opções
O botão agora limpa corretamente todo o session_state e recarrega a página.

### PDF não está sendo gerado
1. Certifique-se de instalar: `pip install reportlab`
2. Verifique se preencheu o nome do avaliado
3. Verifique se completou todos os 10 critérios

### Descrições não aparecem ao selecionar
Se isso acontecer, recarregue a página (F5). A versão atual atualiza em tempo real automaticamente.

## 📦 Estrutura dos Arquivos

```
.
├── avaliacao_enquadramento.py  # Aplicação principal (599 linhas)
├── requirements.txt             # Dependências do projeto
├── README.md                    # Esta documentação
└── INSTALACAO.md               # Guia detalhado de instalação
```

## 💡 Melhorias Futuras Possíveis

- [ ] Comparação entre auto-avaliação e avaliação do gestor
- [ ] Histórico de avaliações ao longo do tempo
- [ ] Gráficos de evolução por critério
- [ ] Plano de desenvolvimento automático baseado em gaps
- [ ] Dashboard consolidado com múltiplos colaboradores
- [ ] Integração com sistema de metas e PDIs
- [ ] Exportação em XLSX além de PDF
- [ ] Sistema de comentários por critério

## 📝 Changelog

### Versão 2.0 (Atual)
- ✅ Interface em tempo real (sem formulários)
- ✅ Descrições aparecem instantaneamente ao selecionar
- ✅ Campo de nome do avaliado
- ✅ Exportação em PDF profissional
- ✅ Botão de reset corrigido
- ✅ Análise de consistência aprimorada

### Versão 1.0
- Versão inicial com formulários
- 10 critérios de avaliação
- Cálculo por moda estatística
- Critérios de desempate automáticos

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte o arquivo INSTALACAO.md para guia passo a passo
2. Verifique se todas as bibliotecas estão instaladas
3. Certifique-se de estar usando Python 3.8 ou superior
4. Em caso de erro, leia a mensagem de erro completa

## 📄 Licença

Uso interno - Controladoria / Gestão de Pessoas

---

**Desenvolvido com ❤️ para otimizar o processo de avaliação e desenvolvimento de pessoas**
