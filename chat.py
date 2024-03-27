from openai import OpenAI


OPENAI_API_KEY = "insert your key here"

def gpt(systemRole, userInput, max_tokens=3000):
    if len(userInput)>=50:
        client = OpenAI(api_key=OPENAI_API_KEY)
       
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            seed=42, # I set the seed  to produce answers that are more reproductable
            response_format={ "type": "json_object" },
            messages=[{"role": "system", "content": systemRole},
                        {"role": "user", "content": userInput}],
            max_tokens=max_tokens,
            temperature=0 #0 to produce answers that are more reproductable 
        )

        

        
        
        return response
    else: return ('Error: not enough words')


