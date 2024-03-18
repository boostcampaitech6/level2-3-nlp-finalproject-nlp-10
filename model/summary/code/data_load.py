import torch
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import json

def load_dataset(path):
    columns = ['passage', 'summary']
    total_df = pd.DataFrame(columns = columns)
    file_list = os.listdir(path)
    
    for file in tqdm(file_list, desc = f"read_data "):
        file_path = os.path.join(path, file)
        if file.endswith('.json'):
            with open(file_path, encoding='UTF-8') as  f:
                data = json.load(f)
    
            data = {k:[v] for k,v in data.items() if k in columns}
            data = pd.DataFrame(data)
        
        total_df = pd.concat([total_df, data], ignore_index=True)

    return total_df


def pd_load_dataset(path):
    df = pd.read_json(path)['documents']
    total = {'passage' : [], 'summary' : []}

    for d in tqdm(df, desc=f"make_df "):
        for s in d['abstractive']:
            total['summary'].append(s)

        total_s=''
        for texts in d['text']:
            for text in texts:
                total_s+=text['sentence']
        total['passage'].append(total_s.replace('\n', ' '))
    
    total_df = pd.DataFrame(total)

    return total_df
            

def load_report_dataset(path):  
    total_df = pd.DataFrame(columns = ['passage', 'summary'])
    dir_list = os.listdir(path)
    for dir_name in tqdm(dir_list, desc="Make DataFrame"):
        dir_path = os.path.join(path,dir_name)
        dir_list2 = os.listdir(dir_path)

        for detail_dir in dir_list2:
            detail_dir_path = os.path.join(dir_path, detail_dir)
            file_list = os.listdir(detail_dir_path)
            for file_name in tqdm(file_list, desc=f"{dir_name}/{detail_dir} Load"):
                if not file_name.endswith(".json"):
                    continue
                file_path = os.path.join(detail_dir_path, file_name)
                with open(file_path, encoding = "UTF-8") as f:
                    data = json.load(f)
                sub_df = pd.DataFrame({'passage':[data["Meta(Refine)"]['passage']], 'summary':[data["Annotation"]['summary1']]})    #summary1이 생성요약
                total_df = pd.concat([total_df, sub_df], axis=0, ignore_index=True)

    return total_df

