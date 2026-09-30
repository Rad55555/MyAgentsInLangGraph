from datetime import datetime

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os

load_dotenv()

@tool
def get_current_time() -> str:
    """Return the current local date and time."""
    return datetime.now().astimezone().isoformat(timespec="seconds")

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a+b

if __name__ == "__main__":
    model= ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    ).bind_tools([get_current_time, add_numbers])

    tools = {"get_current_time": get_current_time, "add_numbers": add_numbers}
    # prompt = "what time is 123 plus 456? Use a tool to calculate it."
    messages = []

    # Ask the model. It can respond with a tool request.
    # The outer loop preserves messages, so the model can use earlier turns as conversation context. The inner loop runs zero or more tools for each prompt, then returns to the outer loop once the model produces a final answer.
    while True:
        prompt = input("\nYou: ").strip()

        if prompt.lower() in {"/quit", "/exit"}:
            break
        if not prompt:
            continue

        messages.append(HumanMessage(content=prompt))

        while True:
            response = model.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                print(f"Agent: {response.content}")
                break

            for tool_call in response.tool_calls:
                selected_tool = tools[tool_call["name"]]
                print(f"Action: {tool_call['name']}({tool_call['args']})")

                result = selected_tool.invoke(tool_call["args"])
                print(f"Observation: {result}")

                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

    # Ask the model to turn the tool result into a final answer.
    # final_response= model.invoke(messages)
    # print(final_response.content)
    # print(get_current_time.invoke({}))




