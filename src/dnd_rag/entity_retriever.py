from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_core.documents import Document
from os import path, listdir
from .entity_collector import get_entities


def make_retriever_txt(db):

    chroma_directory = "./chroma_langchain_db"
    add_texts = False
    if not path.isdir(chroma_directory):
        add_texts = True
        documents = []
        json_dir = "./data/types_txt"
        for filename in listdir(json_dir):
            with open(path.join(json_dir,filename),'r') as file:
                data = file.read()
            document = Document(page_content=data, 
                                metadata={"source": filename.replace(".txt", "")}, id=filename.replace(".txt", ""))
            documents.append(document)
        
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory=chroma_directory,  # Where to save data locally, remove if not necessary
    )

    if add_texts:
        _ = vector_store.add_documents(documents=documents)

    # retriever_tool gets the relevant entities for the query

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    description = (
        "Look up schema to use when crafting a valid GraphQL query. "
        "Input is the suspected object types from a user query, ouput is the GraphQL schema for those object types."
    )

    retriever_tool = create_retriever_tool(
        retriever,
        name="search_graphql_schema",
        description=description,
    )

    return retriever_tool
