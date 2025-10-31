import argparse
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    result = query_rag(query_text)
    print(f"\nAnswer: {result['answer']}")
    print(f"Sources: {result['sources']}")


def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    # Create chain
    model = ChatOllama(model="llama3.3:70b")
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt_template | model
    
    # Invoke chain
    response = chain.invoke({"context": context_text, "question": query_text})
    response_text = response.content

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return {'answer': response_text, 'sources': sources}


if __name__ == "__main__":
    main()
