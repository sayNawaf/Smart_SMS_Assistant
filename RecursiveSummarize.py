import openai
import textwrap
from time import time,sleep
from summarizer import Summarizer
import re

openai.api_key = ""
model2 = Summarizer()

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()





def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def gpt3_completion(prompt, engine='text-ada-001', temp=0.6, top_p=1.0, tokens=400, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            """filename = '%s_gpt3.txt' % time()
            with open('/content/drive/MyDrive/RecursiveSummarizer-main/gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)"""
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def Summarize(alltext):

    
    docLen = len(alltext)
    print(docLen)
    finalSummary = ""
    maxLenght = 500
    flag = 0
    finalSummaryLenght = float('inf') 
    while(True):
        if len(alltext) <= 5200:
            chunksize = 500
        
        else:
            chunksize = 5200
        
        chunks = textwrap.wrap(alltext,chunksize)
        result = list()
        count = 0

        for chunk in chunks:
            if len(alltext) >100000:
                sleep(0.3)
            if(len(" ".join(result)) + finalSummaryLenght) <= maxLenght:
                flag = 1
                break
            
            prompt = open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
            prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
            result.append(gpt3_completion(prompt))

        Summary = " ".join(result)
        finalSummary = finalSummary +"\n"+ Summary

        if len(finalSummary) <= maxLenght or flag == 1:
            break
        prevSummary = alltext
        alltext = finalSummary
        summaryLen = len(finalSummary)
        if finalSummaryLenght <= summaryLen:
            print("cannot reduce final summary lenght further than:",finalSummaryLenght)
            finalSummary = prevSummary
            break
        finalSummaryLenght = summaryLen
        finalSummary = ""

        print(finalSummaryLenght)
        #finalSummaryLenght
        


            
    if finalSummaryLenght >= 1000:
        
        
        finalSummary = model2(finalSummary, num_sentences=3)
    
    print("pppppppppppppppppppppppppp")
    print(len(finalSummary))
    print(finalSummary)
    save_file(finalSummary, 'finalSummary.txt' )
    return finalSummary