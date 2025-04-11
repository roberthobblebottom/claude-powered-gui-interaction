import anthropic
import  os

if __name__ == '__main__':
    with open( "anthropic_api_key.txt","r") as f:
        os.environ["ANTHROPIC_API_KEY"]= f.read()
    client = anthropic.Anthropic()
    # print(os.environ['ANTHROPIC_API_KEY'])
    os.system("python3 app.py")
    #
    # response = client.beta.messages.create(
    #     model="claude-3-7-sonnet-20250219",
    #     max_tokens=1024,
    #     tools=[
    #         {
    #           "type": "computer_20250124",
    #           "name": "computer",
    #           "display_width_px": 1024,
    #           "display_height_px": 768,
    #           "display_number": 1,
    #         },
    #
    #     ],
    #     messages=[{"role": "user", "content": "Click the Yes Button"}],
    #     betas=["computer-use-2025-01-24"],
    #     thinking={"type": "enabled", "budget_tokens": 1024}
    # )
    # print(response)