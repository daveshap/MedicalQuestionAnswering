import os
import openai
from time import time,sleep
from random import seed,choice
import json


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')
bools = ['prompt_bool_diagnosis.txt', 'prompt_bool_medication.txt', 'prompt_bool_prognosis.txt', 'prompt_bool_tests.txt']


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def gpt3_completion(prompt, engine='text-davinci-002', temp=0.0, top_p=1.0, tokens=50, freq_pen=0.0, pres_pen=0.0, stop=['<<END>>']):
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
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    result = list()
    for filename in bools:
        demarc = filename.replace('prompt_bool_','').replace('.txt','').upper()
        for i in range(0, 50):
            seed()
            medical_file = choice(os.listdir('contexts/'))  # pick a random medical file
            medical_text = open_file('contexts/%s' % medical_file)  # read the medical file
            prompt = open_file(filename).replace('<<CONTEXT>>', medical_text)  # populate the prompt
            completion = gpt3_completion(prompt)  # get the boolean answer!
            boolean = completion.lower()
            print('\n\n\n', medical_file, filename, boolean, i)
            if boolean == 'no':
                info = {'prompt': '%s \n\nLIST ALL %s: ' % (medical_text, demarc), 'completion': ' None Found'}
                print(info)
                result.append(info)
            if boolean == 'yes':
                new_filename = filename.replace('bool', 'list')  # update the prompt filename to find the answer
                prompt = open_file(new_filename).replace('<<CONTEXT>>', medical_text)  # populate the prompt
                completion = gpt3_completion(prompt)  # get the list answer!
                info = {'prompt': '%s \n\nLIST ALL %s: ' % (medical_text, demarc), 'completion': ' ' + completion}
                print(info)
                result.append(info)
            outfilename = 'completion_%s.json' % time()
            with open('data/%s' % outfilename, 'w') as outfile:
                json.dump(info, outfile)