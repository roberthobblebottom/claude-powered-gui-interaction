import anthropic
import  os

if __name__ == '__main__':
    with open( "anthropic_api_key.txt","r") as f:
        os.environ["ANTHROPIC_API_KEY"]= f.read()
    client = anthropic.Anthropic()
    # print(os.environ['ANTHROPIC_API_KEY'])

