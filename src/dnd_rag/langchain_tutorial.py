from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langchain import hub
import os
import getpass


# Agent tools
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")





llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")


# TODO change the database
db = SQLDatabase.from_uri("sqlite:///Chinook.db")


toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()


#prompt
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
prompt_template.messages[0].pretty_print()
system_message = prompt_template.format(dialect="SQLite", top_k=5)




# agent 
agent_executor = create_react_agent(llm, tools, prompt=system_message)



print(tools)



import ast
import re


def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

# TODO: need to update this with the entity types in our database
artists = query_as_list(db, "SELECT Name FROM artists")
albums = query_as_list(db, "SELECT Title FROM albums")
albums[:5]







#embeddings

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

print(vector_store)



# retriever_tool gets the relevant entities for the query
from langchain.agents.agent_toolkits import create_retriever_tool


#TODO update this with the entity types we will get above
_ = vector_store.add_texts(artists + albums)
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

print(retriever_tool.invoke("Alice Chains"))


suffix = (
    "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
    "the filter value using the 'search_proper_nouns' tool! Do not try to "
    "guess at the proper name - use this function to find similar ones."
)

system = f"{system_message}\n\n{suffix}"

tools.append(retriever_tool)



# build the agent
agent = create_react_agent(llm, tools, prompt=system)




# example user question

question = "How many albums does alis in chain have?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
