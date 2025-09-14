# Desafio MBA Engenharia de Software com IA - Full Cycle

## 🎯 Sobre o Projeto

Sistema de busca inteligente com IA que permite fazer perguntas sobre documentos PDF e receber respostas precisas baseadas no conteúdo. O sistema utiliza embeddings e busca semântica para encontrar informações relevantes e gera respostas usando modelos de linguagem da OpenAI.

## 🚀 Como Executar

### 1. Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Chave de API da OpenAI

### 2. Configuração do Ambiente

1. Crie um ambiente virtual Python:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=text-embedding-3-small
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documentos
PDF_PATH=document.pdf
```

### 3. Inicialização da Infraestrutura

⚠️ **IMPORTANTE**: Certifique-se de que a porta 5432 esteja livre antes de iniciar o Docker. Se você já tiver PostgreSQL rodando localmente, pare o serviço ou altere a porta no `docker-compose.yml`.

Para verificar se a porta está em uso:
```bash
# No macOS/Linux
lsof -i :5432

# No Windows
netstat -an | findstr :5432
```

Inicie o banco de dados PostgreSQL com pgvector:
```bash
docker compose up -d
```

Verifique se os serviços estão rodando:
```bash
docker compose ps
```

### 4. Ingestão de Documentos

Execute a ingestão do documento PDF:
```bash
python src/ingest.py
```

Este processo irá:
- Carregar o documento PDF
- Dividir em chunks menores
- Gerar embeddings usando OpenAI
- Armazenar no banco vetorial PostgreSQL

### 5. Executando o Chat

Inicie o chat interativo:
```bash
python src/chat.py
```

O chat apresentará uma interface no terminal onde você pode:
- Fazer perguntas sobre o conteúdo do documento
- Receber respostas baseadas exclusivamente no contexto
- Digite 'sair', 'quit' ou 'exit' para encerrar


## 💬 Exemplo de Uso

```
🤖 CHAT INTERATIVO - Sistema de Busca IA
==================================================
Digite suas perguntas e receba respostas baseadas nos documentos.
Para sair, digite 'sair', 'quit' ou 'exit'.
--------------------------------------------------

Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

--------------------------------------------------

Faça sua pergunta: Quantos clientes temos em 2024?

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## 🛠️ Solução de Problemas

### Erro de conexão com banco de dados
- Verifique se o Docker está rodando: `docker compose ps`
- Reinicie os containers: `docker compose down && docker compose up -d`

### Erro de API da OpenAI
- Verifique se a chave da API está correta no arquivo `.env`
- Confirme se há créditos disponíveis na conta OpenAI

### Documento não encontrado
- Verifique se o arquivo PDF existe no caminho especificado
- Confirme a variável `PDF_PATH` no arquivo `.env`

## 🔧 Configurações Avançadas

### Modificar modelo de embeddings
Altere no arquivo `.env`:
```env
OPENAI_MODEL=text-embedding-3-large  # Para maior qualidade
```

### Ajustar parâmetros de busca
No arquivo `src/search.py`, modifique:
- `k=10` - Número de documentos recuperados
- `temperature=0` - Determinismo das respostas