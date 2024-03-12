import torch
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import json
from prepocess import pre_processing


def load_dataset(path):
    df = pd.read_json(path)['documents']
    total = {'title' : [], 'context' : []}

    for d in tqdm(df, desc=f"make_df "):
        title = pre_processing(d['title'])
        total['title'].append(title)
        total['title'].append(title)

        total['context'].append(d['abstractive'])

        total_s=''
        for texts in d['text']:
            for text in texts:
                total_s+=text['sentence']
        total['context'].append(total_s)

    total_df = pd.DataFrame(total)

    return total_df

def read_csv(path, tokenizer):
    df = pd.read_csv(path)
    total = {'title' : [], 'context' : []}

    for d in tqdm(df, desc=f"make_df "):
        if len(tokenizer.tokenize(d['contents']))>60:
            title = pre_processing(d['title'])
            total['title'].append(title)
            total['context'].append(d['contents'])
            total['title'].append(title)
            total['context'].append(d['summary'])
        
    total_df = pd.DataFrame(total)

    return total_df
