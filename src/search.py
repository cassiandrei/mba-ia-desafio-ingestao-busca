import os

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

load_dotenv()


def search_prompt(question=None):
    """
    Função principal que executa busca semântica e gera resposta usando IA.

    Args:
        question (str): A pergunta do usuário a ser respondida

    Returns:
        str: A resposta gerada pela IA baseada no contexto encontrado
    """
    # Inicializa o modelo de embeddings da OpenAI para converter texto em vetores
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_MODEL", "text-embedding-3-small")
    )

    # Conecta ao banco de dados vetorial PostgreSQL (PGVector)
    # que armazena os documentos em formato de embeddings para busca semântica
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    # Realiza busca por similaridade semântica no banco de dados
    # Retorna os 10 documentos mais similares à pergunta com seus scores
    results = store.similarity_search_with_score(question, k=10)

    # Cria um template de prompt personalizado que será preenchido com contexto e pergunta
    template_question = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE,
    )

    # Inicializa o modelo de chat da OpenAI com temperatura 0 (respostas determinísticas)
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

    # Cria pipeline de processamento: Template -> LLM -> Parser de texto
    pipeline = template_question | llm | StrOutputParser()

    # Executa o pipeline com contexto dos 2 documentos mais relevantes e a pergunta
    result = pipeline.invoke(
        {
            # Junta o conteúdo dos 2 documentos mais relevantes como contexto
            "contexto": "\n\n".join(
                [doc.page_content.strip() for doc, _ in results[:2]]
            ),
            "pergunta": question,
        }
    )
    return result


if __name__ == "__main__":
    # Exemplo de uso: busca informações sobre o faturamento da empresa
    resposta = search_prompt("Qual o faturamento da Empresa SuperTechIABrazil?")
    print(resposta)
 
 