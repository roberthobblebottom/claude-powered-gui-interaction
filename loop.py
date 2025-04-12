"""
Agentic sampling loop that calls the Anthropic API and local implementation of anthropic-defined computer use tools.
"""

import platform
from datetime import datetime

import anthropic
from anthropic.types.beta import (
    BetaImageBlockParam,
    BetaMessageParam,
    BetaTextBlockParam,
    BetaToolResultBlockParam
)

from tools import (
    ToolResult,
    BaseComputerTool
)

# This system prompt is optimized for the Docker environment in this repository and
# specific tool combinations enabled.
# We encourage modifying this system prompt to ensure the model has context for the
# environment it is running in, and to provide any additional information that may be
# helpful for the task at hand.
SYSTEM_PROMPT = f"""

<SYSTEM_CAPABILITY>
* You are utilising an linux mint computer using {platform.machine()} architecture .
* When using your computer function calls, they take a while to run and send back to you.  Where possible/feasible, try to chain multiple of these calls all into one function calls request.
* The current date is {datetime.today().strftime('%A, %B %-d, %Y')}.
</SYSTEM_CAPABILITY>


"""


# async
async def sampling_loop(
    *,
    model: str,
    system_prompt_suffix: str,
    messages: list[BetaMessageParam],
    api_key: str,
    max_tokens: int = 4096,
    thinking_budget: int | None = None,
    token_efficient_tools_beta: bool = False,
    computer_tool:BaseComputerTool
):
    """
    Agentic sampling loop for the assistant/tool interaction of computer use.
    """
    system = BetaTextBlockParam(
        type="text",
        text=f"{SYSTEM_PROMPT}{' ' + system_prompt_suffix if system_prompt_suffix else ''}",
    )
    iteration = 0
    while True:
        iteration +=1
        client = anthropic.Anthropic(api_key=api_key, max_retries=4)

        extra_body = {}
        if thinking_budget:
            # Ensure we only send the required fields for thinking
            extra_body = {
                "thinking": {"type": "enabled", "budget_tokens": thinking_budget}
            }

        # Call the API
        # we use raw_response to provide debug information to streamlit. Your
        # implementation may be able call the SDK directly with:
        # `response = client.messages.create(...)` instead.

        tools = [
            {"type": f"computer_20250124", "name": "computer", "display_width_px": 3840,
             "display_height_px": 2160},
        ]
        raw_response = client.beta.messages.create(
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            system=[system],
            tools=tools,
            betas= ["computer-use-2025-01-24"],
            extra_body=extra_body,
        )

        response_content = raw_response.content
        print('------iteration',iteration,"-----")
        print(response_content,"\n\n\n")
        messages.append(
            {
                "role": "assistant",
                "content": response_content,
            }
        )
        tool_result_content  = []
        for block in response_content:
            if block.type == "tool_use":
                if "coordinate" in block.input.keys():
                    coordinate = block.input['coordinate']
                else:
                    coordinate = None
                result = await computer_tool(action = block.input["action"],coordinate=coordinate)


                tool_result_content.append(
                    _make_api_tool_result(result, block.id)
                )

        if not tool_result_content:
            return messages

        messages.append({"content": tool_result_content, "role": "user"})




def _make_api_tool_result(
    result: ToolResult, tool_use_id: str
) -> BetaToolResultBlockParam:
    """Convert an agent ToolResult to an API ToolResultBlockParam."""
    tool_result_content: list[BetaTextBlockParam | BetaImageBlockParam] | str = []
    is_error = False
    if result.error:
        is_error = True
        tool_result_content = _maybe_prepend_system_tool_result(result, result.error)
    else:
        if result.output:
            tool_result_content.append(
                {
                    "type": "text",
                    "text": _maybe_prepend_system_tool_result(result, result.output),
                }
            )
        if result.base64_image:
            tool_result_content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": result.base64_image,
                    },
                }
            )
    return {
        "type": "tool_result",
        "content": tool_result_content,
        "tool_use_id": tool_use_id,
        "is_error": is_error,
    }


def _maybe_prepend_system_tool_result(result: ToolResult, result_text: str):
    if result.system:
        result_text = f"<system>{result.system}</system>\n{result_text}"
    return result_text
