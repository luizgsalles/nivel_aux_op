# 🚀 Guia de Instalação e Uso - Versão 2.0

## 📦 Instalação das Dependências

Antes de rodar a aplicação, instale as bibliotecas necessárias:

```bash
pip install streamlit pandas reportlab
```

Ou usando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

**Versões recomendadas:**
- streamlit >= 1.29.0
- pandas >= 2.0.3  
- reportlab >= 4.0.7

## ▶️ Como Executar

### Opção 1: Execução Local (abre navegador automaticamente)

```bash
streamlit run avaliacao_enquadramento.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

### Opção 2: Execução em Terminal/Servidor

```bash
streamlit run avaliacao_enquadramento.py --server.headless true
```

## 📋 Como Usar a Aplicação

### 1. Preencher Nome do Avaliado
- Digite o **nome completo** do colaborador avaliado no campo no topo
- Este campo é **obrigatório**
- O nome aparecerá no resultado e no PDF

### 2. Avaliar os 10 Critérios

**⚡ A INTERFACE ATUALIZA EM TEMPO REAL!**

Para cada critério:

1. **Abra o dropdown** "Escolha o nível"
2. **Veja as opções** com prévia de 150 caracteres
3. **Selecione uma opção** (ex: "A - Carteira de 8-12 casos...")
4. **A DESCRIÇÃO COMPLETA APARECE IMEDIATAMENTE** em caixa azul abaixo! ⚡
5. **Leia e confirme** que é o nível adequado
6. **Mude quando quiser** - a descrição atualiza instantaneamente

**Não precisa clicar em nada extra!** A descrição aparece automaticamente.

### 3. Calcular Enquadramento
- Após preencher **TODOS os 10 critérios**, clique em **"🎯 Calcular Enquadramento"**
- O sistema calcula:
  - ✅ Nível predominante (moda estatística)
  - ✅ Aplica critérios de desempate se houver empate
  - ✅ Mostra distribuição completa por nível
  - ✅ Gera análise de consistência automática
  - ✅ Fornece recomendações personalizadas

### 4. Exportar PDF
- Após ver os resultados, clique em **"📥 Gerar e Baixar PDF"**
- Aguarde a geração (poucos segundos)
- Clique em **"📄 Clique aqui para baixar o PDF"**
- O PDF incluirá:
  - 📋 Nome do avaliado + data/hora
  - 🎯 Resultado do enquadramento
  - 📊 Distribuição por nível
  - 📝 Tabela de consolidação
  - 📖 Detalhamento de TODAS as respostas
- Arquivo: `Avaliacao_NomeColaborador_20241205_1430.pdf`

### 5. Resetar Avaliação
- Clique em **"🔄 Resetar Avaliação"** na barra lateral
- Limpa **TUDO** (nome + todas as seleções)
- Página recarrega automaticamente
- Pronto para nova avaliação!

## ⚡ Diferencial: Interface em Tempo Real

A aplicação **NÃO usa formulários tradicionais**:

✅ **Descrições aparecem instantaneamente** ao selecionar
✅ **Compare facilmente** diferentes níveis
✅ **Experiência fluida** sem delays
✅ **Tome decisões informadas** lendo tudo antes

## ⚠️ Resolução de Problemas

### Erro: "ModuleNotFoundError: No module named 'reportlab'"
```bash
pip install reportlab
```

Se usa Anaconda:
```bash
conda install -c conda-forge reportlab
```

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### Botão reset não limpa os campos
1. Clique em "🔄 Resetar Avaliação"
2. Aguarde 2-3 segundos
3. Se não funcionar, pressione F5 para recarregar

### PDF não gera
1. Instale reportlab: `pip install reportlab`
2. Preencha o nome do avaliado
3. Complete TODOS os 10 critérios
4. Clique em "Calcular" primeiro, depois "Gerar PDF"

### Descrições não aparecem
1. Certifique-se de selecionar uma opção (não "Selecione...")
2. A descrição aparece em **caixa azul** abaixo do dropdown
3. Role a página para baixo se necessário
4. Se persistir, recarregue a página (F5)

### Aplicação está lenta
- Feche outras abas do navegador
- Reinicie o Streamlit (Ctrl+C e rode novamente)

## 💡 Dicas de Uso

### Para Colaboradores (Auto-avaliação)
- ⏱️ **Tempo:** 15-20 minutos
- 📖 **Leia TODOS os níveis** antes de escolher
- 🎯 **Seja honesto** - marque onde está, não onde quer estar
- 🤔 **Em dúvida?** Marque o nível mais conservador
- 💾 **Salve o PDF** para comparar com avaliação do gestor

### Para Gestores
- ⏱️ **Tempo:** 20-25 minutos por colaborador
- 📊 **Use evidências** dos últimos 3-6 meses
- 🔍 **Compare** com outros auxiliares
- 🎯 **Seja objetivo** - marque o observado, não potencial
- 📝 **Gere PDF** para registro formal

### Interpretação dos Resultados

**Alta consistência (spread ≤1):**
- ✅ Profissional bem posicionado
- 👉 Ação: Validar e formalizar

**Consistência boa (spread ≤2):**
- ℹ️ Normal e esperado
- 👉 Ação: Desenvolver 1-2 critérios

**Consistência moderada (spread ≤3):**
- ⚠️ Requer PDI focado
- 👉 Ação: Plano nos critérios fracos

**Baixa consistência (spread >3):**
- ⚠️ Análise detalhada necessária
- 👉 Ação: Calibração + PDI individualizado

## 📊 Estrutura dos Arquivos

```
.
├── avaliacao_enquadramento.py  # App principal (599 linhas)
├── requirements.txt             # Dependências
├── README.md                    # Documentação completa
└── INSTALACAO.md               # Este guia
```

## 🔄 Atualizações

Para atualizar:

1. Baixe novos arquivos
2. Substitua os antigos
3. Reinstale dependências:
```bash
pip install -r requirements.txt --upgrade
```
4. Reinicie Streamlit:
```bash
Ctrl+C
streamlit run avaliacao_enquadramento.py
```

## 📞 Suporte

1. ✅ Verifique este guia
2. ✅ Leia o README.md
3. ✅ Confira dependências:
```bash
pip list | grep streamlit
pip list | grep pandas
pip list | grep reportlab
```
4. ✅ Leia mensagens de erro
5. ✅ Reinicie o Streamlit

---

**Versão 2.0 - Interface em tempo real com descrições instantâneas** ⚡
