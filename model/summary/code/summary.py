from transformers import AutoTokenizer, BartForConditionalGeneration, AutoConfig, Trainer, TrainingArguments, AutoFeatureExtractor, set_seed
import torch
import pandas as pd
import numpy as np
import os
import random
from argparse import ArgumentParser
from tqdm import tqdm, trange
import json
from data_load import load_dataset
from torch.utils.data import Dataset, DataLoader, TensorDataset, RandomSampler
from make_dataset import make_dataset
import torch.nn as nn
import torch.optim as optim
from training import training, validation
import argparse

seed = 1997

random.seed(seed) # python random seed 고정
np.random.seed(seed) # numpy random seed 고정
torch.manual_seed(seed) # torch random seed 고정
torch.cuda.manual_seed_all(seed)

training_args = TrainingArguments
training_args.per_device_train_batch_size=10
training_args.per_device_eval_batch_size=10

if torch.cuda.is_available()==True:
    device = "cuda"
else:
    device = "cpu"


set_seed(seed)

model_name = "ainize/kobart-news"

parser = argparse.ArgumentParser(description="")

parser.add_argument("--do_train", default=False, type=bool, help='train doing?')
parser.add_argument("--do_eval", default=True, type=bool, help='eval doing?')
parser.add_argument("--use_trained_model", default=False, type=bool, help='eval doing?')

args = parser.parse_args()

if args.do_train : 
    model = training(training_args, model_name, device)
    torch.save(model, '../trained_model/model.pt')
    print(f'Model Save Finish!')

else : 
    if args.use_trained_model:
        model = torch.load('../trained_model/model.pt')
        print(f'\nModel load Finish!\n')
    
    else: 
        model = BartForConditionalGeneration.from_pretrained(model_name)
        print(f'\nbase_model!\n')

if args.do_eval:
    print(f'Validation Start!')
    #print(f'\n{model.state_dict()=}\n')
    validation(model, model_name, device)









    



