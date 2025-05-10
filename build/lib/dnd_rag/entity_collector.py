import ast
import re
from langchain_community.utilities import SQLDatabase


def query_as_list(db: SQLDatabase, query: str) -> list[str]:
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))


def get_entities(db: SQLDatabase, db_queries) -> list[list[str]]:
    entity_lists = []
    for query in db_queries:
        entity_lists.append(query_as_list(db, query))
    return entity_lists
