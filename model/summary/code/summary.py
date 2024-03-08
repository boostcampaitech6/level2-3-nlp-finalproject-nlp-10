from transformers import AutoTokenizer, BartForConditionalGeneration, AutoConfig, Trainer, TrainingArguments, set_seed
import torch
import pandas as pd
import numpy as np
import os
import random
from tqdm import tqdm, trange
import json
from data_load import load_dataset
from torch.utils.data import Dataset, DataLoader, TensorDataset, RandomSampler
from make_dataset import make_dataset
import torch.nn as nn
import torch.optim as optim
from training import training, validation
import argparse
from make_summary_dataframe import make_summary_data

seed = 1997

random.seed(seed) # python random seed 고정
np.random.seed(seed) # numpy random seed 고정
torch.manual_seed(seed) # torch random seed 고정
torch.cuda.manual_seed_all(seed)

training_args = TrainingArguments
training_args.per_device_train_batch_size=10
training_args.per_device_eval_batch_size=10
training_args.learning_rate= 4e-05

if torch.cuda.is_available()==True:
    device = "cuda"
else:
    device = "cpu"

set_seed(seed)

model_name = "EbanLee/kobart-summary-v2"

parser = argparse.ArgumentParser(description="")

parser.add_argument("--do_train", default='False', type=str, help='train doing?')
parser.add_argument("--do_eval", default='False', type=str, help='eval doing?')
parser.add_argument("--use_local_model", default='False', type=str, help='eval doing?')
parser.add_argument("--make_dataframe", default='False', type=str, help='make summary file')

args = parser.parse_args()

if args.do_train == 'True': 
    print('!train_mode!')
    tokenizer = AutoTokenizer.from_pretrained(model_name)   #토크나이저에 스페셜토큰을 추가하는 등의 일을 아래의 training함수 내부에서 한다면 따로 받아야함
    model = training(training_args, model_name, device)
    torch.save(model, '../trained_model/model.pt')
    model.save_pretrained('../trained_model')
    tokenizer.save_pretrained('../save_tokenizer')
    print(f'Save Finish!')

else : 
    if args.use_local_model == 'True':
        model = torch.load('../trained_model/model.pt')
        print(f'\nLocal Model load Finish!\n')
    
    else: 
        model = BartForConditionalGeneration.from_pretrained(model_name)
        print(f'\nbase_model_name : {model_name}\n')

if args.do_eval == 'True':
    print(f'Validation Start!')
    #print(f'\n{model.state_dict()=}\n')
    validation(model, model_name, device)

if args.make_dataframe == 'True':
    print(f'make_dataset!')
    data_path = "../dataset/custom_data"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    make_summary_data(model, tokenizer, data_path, device)
