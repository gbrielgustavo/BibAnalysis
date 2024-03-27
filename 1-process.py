from readris import ris
import pandas as pd
from openai import OpenAI
import chat
import json
import time

none = "### Empty field ###"

fileList = ['RIS/scopus.ris', 'RIS/1000.ris', 'RIS/1721.ris']

# A pandas dataframe
db = ris(fileList)

#db.to_csv('GPT/original.csv')
db.to_excel('GPT/original.xlsx')


systemRole ="""You are a scientific paper reviewer and summarizer. Focus in these: Setting (where the study was conducted), Focus (internal and/or external to the subject) Application (healthcare, management, engineering, etc.), Context, Objectives, Methods, and Results. For each one, give a short phrase or a couple of expressions describing it in a concise way. Data in JSON. Check an model / example of an answer:
{"setting": "private sector, public sector", "focus": "external-customers, internal-processes, internal-workers","application": "healthcare, management, ethics, sports, etc.", "context": "Government and private companies wants to do, entrepreneurship development", "objectives": "Propose a framework, increase productivity, influence customer", "methods": "Systematic literature review, empirical testing, statistical evaluation." "results": "framework, it was functional, results were positive.", "rateofSuccess": "positives, inconclusive, requires more studies, negatives, etc."}
 "Setting" (more than one can be selected, so think twice): classify if it was conducted in a government-related environment, you should classify it as "government"; in a nongovernmental environment, such as an ONG agency, hospital, school, "public sector"; in a company or private enterprise, "private sector"; if you are not shure you can use "other", but avoid using it and thing again, again and again before using it. Important: More than one option can be selected (e.g. can happen both in private and public sector).
 "Focus" topic: you need to classify in "internal" if internal to the organization/coutry/etc. (workers, citizens, processes, etc.), "external" if extenal to it. Add also where was the study's focus in a word, e.g. customers, internal processes, competition, citizens, workers, etc. More than one option can be selected and you can also use "other".
“Application” topic: describe in topics the area where it was conducted, such as healthcare, management, ethics, politics, sports, etc.More than one option can be selected and you can also use "other".
"Context": topic is a summary of the context.
"Objectives" Keywords of objectives
"Methods" Keywords of methods
"Results": a summary of the results.
"rateofSuccess': "Inconclusive", "Unsuccessful", "Partial Success", "Success", ""Not Reported/Can't identify".
For all of then, think twice, and then think again.
The user provides title, keywords, and abstract.
"""

dfIndex = ['title', 'FirstAuthor', 'Authors', 'abstract', 'keywords', 'year', 'doi', "type"]
dfIndex2 = ['responseId', 'logprobs', 'created', 'model', 'fingerprint', 'completionTokens', 'promptTokens', 'totalTokens', 'setting', 'focus', 'application', 'context', 'objectives', 'methods', 'results', 'rateofSuccess']

l = len(db)
for i in range(l):

    abstract = db['abstract'][i]
    title = db['title'][i]
    keywords = db['keywords'][i]

    print(str(i*100/l)+" % - "+str(i) + " of "+str(l)+" -  "+str(title)+"\n\n")

    
    # tests if the abstract is not empty
    if abstract == none:
        continue
    else:
        try:
            # builds the input
            userInput = "TITLE: "+str(title)+";;ABSTRACT: "+str(abstract)+";;KEYWORDS: "+str(keywords)
            
            # gets the chat gpt response
            rawResponse = chat.gpt(systemRole, userInput)
                
            rawResponse = rawResponse.model_dump()
            
            #Gets usefull information from the raw response
            responseId = rawResponse['id'] # Aswer id - String
            logprobs = rawResponse['choices'][0]['logprobs'] #- string
            created = rawResponse['created']
            model =  rawResponse['model']
            fingerprint = rawResponse['system_fingerprint']
            completionTokens = rawResponse['usage']['completion_tokens']
            promptTokens = rawResponse['usage']['prompt_tokens']
            totalTokens = rawResponse['usage']['total_tokens']


            rawAnswer = rawResponse['choices'][0]['message']['content'] # message content - String
            rawAnswer = json.loads(rawAnswer) #converts the full gpt answer to a dict

            setting = rawAnswer['setting']
            focus = rawAnswer['focus']
            application = rawAnswer['application']
            context = rawAnswer['context']
            objectives = rawAnswer['objectives']
            methods = rawAnswer['methods']
            results = rawAnswer['results']
            rateofSuccess = rawAnswer['rateofSuccess']
            

            summ = [ responseId ,  logprobs ,  created ,  model ,  fingerprint ,  completionTokens ,  promptTokens ,  totalTokens, setting, focus, application, context ,  objectives ,  methods ,  results, rateofSuccess ]

            for j in range(len(dfIndex2)):

                db.loc[i,dfIndex2[j]] = summ[j]
        except: print("GPT error")
    
    # every n requests we sleep to try to avoid exceeding our quota we also save the file parcially
    if i%10 == 0 and i!=0:
        db.to_excel('GPT/summary.xlsx')
        
        #print("\n\nSleeping\n\n")
        #time.sleep(3)
        
print(db)

db.to_csv('GPT/summary_Final.csv')
#db.to_excel('GPT/summary_Final.xlsx')


