from pyexpat.errors import messages

import anthropic
from anthropic import Anthropic
import os
import json
from anthropic import (
    Anthropic,
    AnthropicBedrock,
    AnthropicVertex,
    APIError,
    APIResponseValidationError,
    APIStatusError,
)
from anthropic.types.beta import (
    BetaCacheControlEphemeralParam,
    BetaContentBlockParam,
    BetaImageBlockParam,
    BetaMessage,
    BetaMessageParam,
    BetaTextBlock,
    BetaTextBlockParam,
    BetaToolResultBlockParam,
    BetaToolUseBlockParam,
)
async def sampling_loop(
        *,
        model: str,
        messages: list[dict],
        api_key: str,
        max_tokens: int = 4096,
        tool_version: str,
        thinking_budget: int | None = None,
        max_iterations: int = 5,  # Add iteration limit to prevent infinite loops
):
    """
    A simple agent loop for Claude computer use interactions.

    This function handles the back-and-forth between:
    1. Sending user messages to Claude
    2. Claude requesting to use tools
    3. Your app executing those tools
    4. Sending tool results back to Claude
    """
    # Set up tools and API parameters
    client = Anthropic(api_key=api_key)
    beta_flag = "computer-use-2025-01-24" if "20250124" in tool_version else "computer-use-2024-10-22"
    # Configure tools - you should already have these initialized elsewhere
    tools = [
        {"type": f"computer_{tool_version}", "name": "computer",
         "display_width_px": 3840, "display_height_px": 2160},
        # {"type": f"text_editor_{tool_version}", "name": "str_replace_editor"},
        # {"type": f"bash_{tool_version}", "name": "bash"}
    ]

    # Main agent loop (with iteration limit to prevent runaway API costs)
    iterations = 0
    while True and iterations < max_iterations:
        iterations += 1
        # Set up optional thinking parameter (for Claude 3.7 Sonnet)
        thinking = None
        if thinking_budget:
            thinking = {"type": "enabled", "budget_tokens": thinking_budget}

        # Call the Claude API
        print("---- Iteration:",iterations,"----")
        response = client.beta.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            tools=tools,
            betas=[beta_flag],
            thinking=thinking
        )

        # Add Claude's response to the conversation history
        response_content = response.content
        # print()
        # print("response_content",response_content)
        messages.append({"role": "assistant", "content": response_content})

        # Check if Claude used any tools
        tool_results = []
        for block in response_content:
            if block.type == "tool_use":
                # In a real app, you would execute the tool here
                # For example: result = run_tool(block.name, block.input)
                result=
                # Format the result for Claude
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # If no tools were used, Claude is done - return the final messages
        if not tool_results:
            return messages
        # Add tool results to messages for the next iteration with Claude
        messages.append({"role": "user", "content": tool_results})
        print(messages)


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
                  api_key=os.environ["ANTHROPIC_API_KEY"]
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
