import os
import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from app.utils.query_tool import get_database_info_str, ask_database
import sqlite3
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "chinook.db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 设置网络代理 全局代理测试通过
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

client = OpenAI(api_key=OPENAI_API_KEY)


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))


def execute_function_call(message, db_conn):
    if message.tool_calls[0].function.name == "ask_database":
        query = json.loads(message.tool_calls[0].function.arguments)["query"]
        results = ask_database(db_conn, query)
    else:
        results = f"Error: function {message.tool_calls[0].function.name} does not exist"
    return results


def process_nlp_query_with_db(query: str, db_path: str) -> str:
    try:
        # 创建数据库连接
        db_conn = sqlite3.connect(db_path)
        # 获取数据库 schema 信息
        database_schema_string = get_database_info_str(db_conn)
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "ask_database",
                    "description": "Use this function to answer user questions about this database. Input should be a fully formed SQL query.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": f"""
                                            SQL query extracting info to answer the user's question.
                                            SQL should be written using this database schema:
                                            {database_schema_string}
                                            The query should be returned in plain text, not in JSON.
                                            """,
                            }
                        },
                        "required": ["query"],
                    },
                }
            }
        ]
        messages = []

        messages.append({"role": "system",
                         "content": "Answer user questions by generating SQL queries against the Database."})
        messages.append({"role": "user", "content": query})
        chat_response = chat_completion_request(messages, tools, model="gpt-4o")
        assistant_message = chat_response.choices[0].message
        messages.append(assistant_message)

        if assistant_message.tool_calls:
            results = execute_function_call(assistant_message, db_conn)
            messages.append({"role": "tool", "tool_call_id": assistant_message.tool_calls[0].id,
                             "name": assistant_message.tool_calls[0].function.name, "content": results})

        final_response = chat_completion_request(messages, tools=tools, model="gpt-4o")
        final_result = final_response.choices[0].message.content

        # 关闭数据库连接
        db_conn.close()
        return final_result
    except Exception as e:
        logger.error(f"Error processing NLP query with DB: {str(e)}")
        raise


if __name__ == '__main__':
    query = f"show me the most recent example data item"
    process_nlp_query_with_db(query, )
