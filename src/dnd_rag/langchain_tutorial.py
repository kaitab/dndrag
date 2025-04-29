from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langchain import hub
import os
import getpass
from entity_retriever import make_retriever


# Agent tools
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


class RAG():
    def __init__(self):
        
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

        llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
        # TODO change the database
        db = SQLDatabase.from_uri("sqlite:///Chinook.db")

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        tools = toolkit.get_tools()

        # prompt
        prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

        # prompt_template.messages[0].pretty_print()
        system_message = prompt_template.format(dialect="SQLite", top_k=5)

        # agent 
        agent_executor = create_react_agent(llm, tools, prompt=system_message)

        # TODO: need to update this with the entity types in our database

        suffix = (
            "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
            "the filter value using the 'search_proper_nouns' tool! Do not try to "
            "guess at the proper name - use this function to find similar ones."
        )

        system = f"{system_message}\n\n{suffix}"

        retriever_tool = make_retriever(db)

        print(retriever_tool.invoke("Alice Chains"))

        tools.append(retriever_tool)


        # build the agent
        self.agent = create_react_agent(llm, tools, prompt=system)

    def query(self, question: str) -> list[str]:
        messages = []
        for step in self.agent.stream(
            {"messages": [{"role": "user", "content": question}]},
            stream_mode="values",
        ):
            messages.append(step["messages"][-1])
        return messages


# # example user question

# question = "How many albums does alis in chains have?"

# rag = RAG()
# output = rag.query(question)
# print(output)
