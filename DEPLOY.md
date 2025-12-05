# 🚀 Guia de Deploy no Streamlit Cloud

## 📁 Arquivos Necessários

Para fazer o deploy no Streamlit Cloud (ou GitHub), você precisa destes arquivos:

```
seu-repositorio/
├── avaliacao_enquadramento.py  # Aplicação principal
├── requirements.txt             # Dependências Python
├── runtime.txt                  # Versão do Python (opcional)
├── packages.txt                 # Dependências do sistema (opcional)
└── .streamlit/
    └── config.toml              # Configurações do Streamlit (opcional)
```

## 🔧 Arquivos de Configuração

### 1. requirements.txt
```
streamlit>=1.28.0
pandas>=1.5.0
reportlab>=3.6.0
Pillow>=9.0.0
```

**Por que essas versões?**
- `>=` permite versões mais recentes (mais flexível)
- Versões testadas e estáveis
- Compatível com Streamlit Cloud
- Pillow é dependência do reportlab

### 2. runtime.txt (opcional)
```
python-3.9
```

Especifica a versão do Python. Streamlit Cloud suporta:
- python-3.9
- python-3.10
- python-3.11

### 3. packages.txt (opcional)
```
build-essential
```

Dependências de sistema Linux necessárias para compilar algumas bibliotecas.

### 4. .streamlit/config.toml (opcional)
Configurações visuais e de servidor do Streamlit.

## 📤 Como Fazer Deploy no Streamlit Cloud

### Passo 1: Preparar GitHub

1. **Crie um repositório no GitHub:**
   - Acesse https://github.com/new
   - Nome: `avaliacao-enquadramento` (ou outro nome)
   - Visibilidade: Público ou Privado

2. **Faça upload dos arquivos:**
   - Opção A: Via interface do GitHub (arrastar e soltar)
   - Opção B: Via Git CLI:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/seu-usuario/seu-repo.git
   git push -u origin main
   ```

### Passo 2: Deploy no Streamlit Cloud

1. **Acesse Streamlit Cloud:**
   - Vá para https://share.streamlit.io/
   - Faça login com sua conta GitHub

2. **Criar novo app:**
   - Clique em "New app"
   - Selecione seu repositório
   - Branch: `main` (ou `master`)
   - Main file path: `avaliacao_enquadramento.py`
   - Clique em "Deploy!"

3. **Aguarde o deploy:**
   - Leva 2-5 minutos
   - Você verá os logs em tempo real
   - Quando terminar, seu app estará no ar!

### Passo 3: Compartilhar

Sua URL será algo como:
```
https://seu-usuario-avaliacao-enquadramento-xxx.streamlit.app
```

Compartilhe com sua equipe!

## ⚠️ Resolução de Problemas no Deploy

### Erro: "Error installing requirements"

**Solução 1: Versões incompatíveis**
- Use `>=` ao invés de `==` no requirements.txt
- Exemplo: `streamlit>=1.28.0` ao invés de `streamlit==1.29.0`

**Solução 2: Dependências faltando**
- Adicione Pillow ao requirements.txt
- Verifique se packages.txt está presente

**Solução 3: Python muito antigo**
- Use `python-3.9` ou superior no runtime.txt

### Erro: "Module not found"

Certifique-se de que TODOS os arquivos estão no repositório:
- ✅ avaliacao_enquadramento.py
- ✅ requirements.txt
- ✅ runtime.txt
- ✅ packages.txt
- ✅ .streamlit/config.toml

### Erro: "Build failed"

1. Verifique os logs no Streamlit Cloud
2. Procure por linhas com "ERROR"
3. Geralmente indica:
   - Sintaxe errada no requirements.txt
   - Pacote não existe
   - Versão incompatível

### App carrega mas dá erro ao executar

Teste localmente primeiro:
```bash
streamlit run avaliacao_enquadramento.py
```

Se funciona local mas não no cloud, pode ser:
- Caminho de arquivo errado
- Dependência de sistema faltando (adicione em packages.txt)

## 🔄 Como Atualizar o App Deployed

Após fazer mudanças:

1. **Atualize o código no GitHub:**
   ```bash
   git add .
   git commit -m "Descrição das mudanças"
   git push
   ```

2. **Streamlit Cloud detecta automaticamente:**
   - Ele faz redeploy automático
   - Leva 1-2 minutos
   - Seu app será atualizado!

## 💡 Dicas Importantes

### 1. Teste Local Primeiro
Sempre teste localmente antes de fazer deploy:
```bash
pip install -r requirements.txt
streamlit run avaliacao_enquadramento.py
```

### 2. Mantenha Simples
- Menos dependências = deploy mais rápido
- Use versões estáveis testadas

### 3. Documentação
- README.md ajuda outros desenvolvedores
- Explique como usar o app

### 4. Secrets (se necessário no futuro)
Para dados sensíveis, use Streamlit Secrets:
- Vá em "Settings" no Streamlit Cloud
- Adicione suas secrets
- Acesse via `st.secrets["chave"]`

## 📊 Recursos do Streamlit Cloud

### Gratuito inclui:
- ✅ 1 app privado ou ilimitados públicos
- ✅ 1 GB de RAM
- ✅ 1 CPU compartilhado
- ✅ Deploy automático via GitHub
- ✅ HTTPS gratuito
- ✅ Sem limite de usuários

### Limitações:
- ⚠️ Apps hibernam após inatividade
- ⚠️ RAM limitada (1 GB)
- ⚠️ CPU compartilhado (pode ser lento com múltiplos usuários)

Para apps de produção pesados, considere:
- Streamlit Cloud Pro ($20/mês)
- AWS/GCP/Azure
- Heroku
- Railway

## 🔗 Links Úteis

- [Documentação Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Deploy Tutorial](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [Fórum Streamlit](https://discuss.streamlit.io/)

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs no Streamlit Cloud
2. Consulte este guia
3. Teste localmente
4. Pesquise no [Fórum Streamlit](https://discuss.streamlit.io/)

---

**Boa sorte com o deploy! 🚀**
