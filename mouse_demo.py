import os

from loop import sampling_loop

if __name__ == '__main__':
    with open("anthropic_api_key.txt", "r") as f:
        os.environ["ANTHROPIC_API_KEY"] = f.readline().replace("\n", "")

    # print(os.environ['ANTHROPIC_API_KEY'])
    # os.system("python3 app.py")
    messages = [{"role": "user",
                 "content": "Click the Yes Button and then click Back. And then click on the No button and then click back"}]

    sampling_loop(model="claude-3-7-sonnet-20250219", messages=messages,
                  max_tokens=2024,
                  tool_version="20250124",
                  thinking_budget=1024,
                  api_key=os.environ["ANTHROPIC_API_KEY"],
                  system_prompt_suffix="",

                  )
    #
    # response = client.beta.messages.with_raw_response.create(
    #     model="claude-3-7-sonnet-20250219",
    #     max_tokens=2024,
    #     tools=[
    #         {
    #           "type": "computer_20250124",
    #           "name": "computer",
    #           "display_width_px": 3840,
    #           "display_height_px": 2160,
    #           "display_number": 1,
    #         },{
    #       "type": "text_editor_20250124",
    #       "name": "str_replace_editor"
    #     },
    #     {
    #       "type": "bash_20250124",
    #       "name": "bash"
    #     }
    #     ],
    #     messages= messages,
    #     betas=["computer-use-2025-01-24"],
    #     thinking={"type": "enabled", "budget_tokens": 1024}
    # )
    #
