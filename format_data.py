import os
import json


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


files = os.listdir('data/')
with open('medical.jsonl', 'w') as outfile:
    for i in files:
        content = open_file('data/%s' % i).strip()
        outfile.write(content + '\n')