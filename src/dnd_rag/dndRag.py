from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, load_tools
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import init_chat_model
from langchain import hub
import os
import getpass
from .entity_retriever import make_retriever_txt


# Agent tools
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, StateGraph


class RAG():
    def __init__(self):
        
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

        llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
        # TODO change the database
        db = SQLDatabase.from_uri("sqlite:///Chinook.db")

        # toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        # tools = toolkit.get_tools()
        tools = load_tools.load_tools(
            ["graphql"],
            graphql_endpoint="https://www.dnd5eapi.co/graphql/2014"
        )

        # prompt
        prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

        # prompt_template.messages[0].pretty_print()
        # system_message = prompt_template.format(dialect="SQLite", top_k=5)
        system_message = """
        You are a parser that understands the meaning of natural language queries 
        and parses them into valid graphql queries, constructing your query from 
        any of the following Query object types:

        type Query {
            abilityScores
            alignments
            backgrounds
            classes
            conditions
            damageTypes
            equipmentCategories
            equipments
            feats
            features
            languages
            levels
            magicItems
            magicSchools
            monsters
            proficiencies
            races
            skills
            spells
            subclasses
            subraces
            traits
            weaponProperties
        }

        Before constructing your query, you MUST look through the graphql schemas for each of these objects, and 
        the use the schema of the most relevant Query objects to build your valid graphql query. Do NOT skip
        this step.

        Your valid graphql query shold have the following schema:

        query {
            {context}
        }
        """

        # agent 
        agent_executor = create_react_agent(llm, tools, prompt=system_message)

        # TODO: need to update this with the entity types in our database
        
        # entities = get_entities(db, ["query{\n abilityScores{ \n name \n full_name \n desc \n}\n}"])
        

        suffix = (
            "If you need to filter on a proper noun like a Name, you must ALWAYS first look up "
            "the filter value using the 'search_proper_nouns' tool! Do not try to "
            "guess at the proper name - use this function to find similar ones."
        )

        system = f"{system_message}\n\n{suffix}"

        retriever_tool = make_retriever_txt(db)

        # print(retriever_tool.invoke("Alice Chains"))

        tools.append(retriever_tool)


        # build the agent
        self.agent = create_react_agent(llm, tools, prompt=system)
        # self.agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    def query(self, question: str) -> list[str]:
        messages = []
        for step in self.agent.stream(
            input={"messages": [{"role": "user", "content": question}]},
            stream_mode="values"
        ):
            messages.append(step["messages"][-1])
            step["messages"][-1].pretty_print()
        return messages
