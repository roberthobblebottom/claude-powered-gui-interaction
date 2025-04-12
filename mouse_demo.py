import os
import asyncio
from loop import sampling_loop
from tools import ComputerTool20250124


async def m(messages):
    os.environ["WIDTH"] = '3840'
    os.environ["HEIGHT"] = '2160'
    await sampling_loop(model="claude-3-7-sonnet-20250219", messages=messages,
                        max_tokens=2024,
                        thinking_budget=1024,
                        api_key=os.environ["ANTHROPIC_API_KEY"],
                        system_prompt_suffix="", computer_tool=ComputerTool20250124()
                        )


def run_flask():
    os.system("python3 app.py")


if __name__ == '__main__':
    with open("anthropic_api_key.txt", "r") as f:
        os.environ["ANTHROPIC_API_KEY"] = f.readline().replace("\n", "")

    messages = [{"role": "user",
                 "content": "Click the Yes Button and then click Back. And then click on the No button and then click back"}]
    asyncio.run(m(messages))
