from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool
from os import path
from entity_collector import get_entities


def make_retriever(db):

    chroma_directory = "./chroma_langchain_db"

    if not path.isdir(chroma_directory):
        entities = get_entities(db, ["SELECT Name FROM artists", "SELECT Title FROM albums"])
        _ = vector_store.add_texts(entities[0] + entities[1])
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory=chroma_directory,  # Where to save data locally, remove if not necessary
    )

    # retriever_tool gets the relevant entities for the query

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    description = (
        "Use to look up values to filter on. Input is an approximate spelling "
        "of the proper noun, output is valid proper nouns. Use the noun most "
        "similar to the search."
    )

    retriever_tool = create_retriever_tool(
        retriever,
        name="search_proper_nouns",
        description=description,
    )

    return retriever_tool
