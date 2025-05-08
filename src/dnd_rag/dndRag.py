from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, load_tools
from langchain.agents import AgentType, initialize_agent
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
        and parses them into valid graphql queries based on this schema:

        query {
            abilityScores {
                index
                name
                full_name
                desc
                skills: [Skill!]!
            }

            alignments {
                index 
                name
                abbreviation
                desc
            }

            backgrounds {
                index
                name
                bonds
                feature
                flaws
                ideals
                langauge_options
                personality_traits
                starting_equipment
                starting_equipment_options
                starting_proficiencies: [Proficiency!]!
            }

            conditions {
                index
                name
                desc
            }

            skills {
                index
                name
                desc
                ability_score: AbilityScore!
            }

            classes {
                index
                name
                hit_die
                proficiencies: [Proficiency!]!
                saving_throws: [AbilityScore!]!
                spellcasting: ClassSpellcasting
                spells: [Spell!]!
                starting_equipment: [Quantity!]!
                class_levels: [Level!]!
                sublcasses: [Subclass!]!
                multi_classing: Multiclassing!
                proficiency_choices: [ProficiencyChoice!]!
                starting_equipment_options: [StartingEquipmentChoice!]!
            }

            conditions {
                index
                name
                desc
            }

            damageTypes {
                index
                name
                desc
            }

            equipments {
                index
                name
                cost
                desc
                equipment_category: EquipmentCategory!
                weight
            }

            equipmentCategrories {
                index
                name
                equipment: [IEquipmentBase!]!
            }

            feats {
                item
                name
                desc
                prerequisites: [AbilityScorePrerequisite!]!
            }

            features {
                index
                name
                desc
                level
                parent: Feature
                class: Class!
                subclass: Subclass
                prerequisites: [FeatureScorePrerequisite!]!
                reference
                feature_specific: FeatureSpecific
            }

            languages {
                index
                name
                desc
                script
                type: LanguageType!
                typical_speakers
            }

            levels {
                index
                level
                ability_score_bonus
                class: Class!
                sublcass: Subclass
                features: [Features!]!
                prof_bonus
                spellcasting: LevelSpellCasting
                class_specific: ClassSpecific
                subclass_specific: SubclassSpecific
            }

            magicItems {
                index
                name
                desc
                rarity
                equipment_category
                image
            }

            magicSchools {
                index
                name
                desc
                spells: [Spell!]!
            }

            monsters {
                index
                name
                alignment
                desc
                actions
                challenge_rating
                proficiency_bonus
                charisma
                condition_immunities: [Condition!]!
                constitution
                damage_immunities
                constitution
                damage_immunities
                damage_resistances
                damage_vulnerabilities
                dexterity
                forms: [Monster!]
                hit_dice
                hit_points
                hit_points_roll
                intelligence
                languages
                legendary_actions: [LegendaryAction!]
                proficiencies: [MonsterProficiency!]!
                reactions: [Reaction!]
                senses
                size
                special_abilities [SpecialAbility!]
                speed: MonsterSpeed!
                strength
                subtype
                type: MonsterType!
                wisdom
                xp
                image
            }
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

        retriever_tool = make_retriever(db)

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
        return messages


# # example user question

question = "What are the names of the skills needed for the wis abilityScore?"

# rag = RAG()
# output = rag.query(question)
# print(output)
