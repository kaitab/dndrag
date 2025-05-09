from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.agents.agent_toolkits import create_retriever_tool
from os import path, listdir
from .entity_collector import get_entities


def make_retriever(db):

    chroma_directory = "./chroma_langchain_db"
    add_texts = False
    if not path.isdir(chroma_directory):
        add_texts = True
        entities = []
        metadata = []
        json_dir = "./data/types_json"
        for filename in listdir(json_dir):
            with open(path.join(json_dir,filename),'r') as file:
                data = file.read()
            entities.append(data)
            metadata.append({'source': filename.replace(".json","")})
        
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory=chroma_directory,  # Where to save data locally, remove if not necessary
    )

    if add_texts:
        _ = vector_store.add_texts(entities, metadata=metadata)

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
