from transformers import AutoTokenizer, BartForConditionalGeneration, TrainingArguments, set_seed
import torch
import pandas as pd
import numpy as np
import os
from tqdm import tqdm, trange
import random
from data_load import load_dataset, read_csv
from make_dataset import make_dataset
from torch.utils.data import DataLoader, RandomSampler

seed = 1997

random.seed(seed) # python random seed 고정
np.random.seed(seed) # numpy random seed 고정
torch.manual_seed(seed) # torch random seed 고정
torch.cuda.manual_seed_all(seed)
set_seed(seed)

training_args=TrainingArguments
training_args.per_device_train_batch_size=11
training_args.per_device_eval_batch_size=11
training_args.learning_rate= 2e-05
training_args.num_train_epochs = 1

dataset_path = "../dataset"
train_data_path = os.path.join(dataset_path, "Training")
valid_data_path = os.path.join(dataset_path, "Validation")

model_name = 'hyunwoongko/kobart'

def training(training_args, model_name, device):
    tokenizer = AutoTokenizer.from_pretrained('EbanLee/kobart-summary-v1')
    model = BartForConditionalGeneration.from_pretrained(model_name)

    file_list = os.listdir(train_data_path)
    train_data = pd.DataFrame(columns = ['title', 'context'])

    for file_name in file_list:     #학습 데이터 제작
        if file_name.endswith('.json'):
            dataset = load_dataset(os.path.join(train_data_path, file_name), tokenizer)    #df = {'title' : [],'context' : []} title2개, 본문과 요약문 2세트씩
            
        elif file_name.endswith('.csv'):
            dataset = read_csv(os.path.join(train_data_path, file_name), tokenizer)    #df = {'title' : [],'context' : []}
        
        else: continue        
        train_data = pd.concat([train_data, dataset], ignore_index=True)

    train_data = make_dataset(tokenizer, train_data['context'], train_data['title'])  #(input_ids, attention_mask, token_type_ids, overflow_to_sample_mapping)

    train_sampler = RandomSampler(train_data)
    train_loader = DataLoader(train_data, sampler=train_sampler, batch_size = training_args.per_device_train_batch_size)

    optimizer = torch.optim.AdamW(model.parameters(), lr = training_args.learning_rate, eps=training_args.adam_epsilon)
    model.to(device)

    print(f'\n!!!!!!!!!!!!!Train Start!!!!!!!!!!!!!!!!\n')

    global_step = 0

    model.zero_grad()
    torch.cuda.empty_cache()

    for _ in trange(int(training_args.num_train_epochs), desc="Epoch "):
        for batch in tqdm(train_loader, desc=f'training progress '):
            model.train()

            batch = tuple(t.to(device) for t in batch)
            
            context_input = {'input_ids':batch[0], 'attention_mask': batch[1], 'token_type_ids': batch[2]}
            target_input = {'input_ids':batch[3], 'attention_mask': batch[4], 'token_type_ids': batch[5]}

            loss = model(input_ids = context_input['input_ids'], attention_mask = context_input['attention_mask'],
                            labels = target_input['input_ids']).loss
        
            loss.backward()
            optimizer.step()
            model.zero_grad()
        
            if global_step%1000==0:
                print(f"\n{global_step=}, LR = {optimizer.param_groups[0]['lr']}, training_loss = {round(loss.item(), 8)}")

            if global_step%10000==0:
                torch.save(model, '../trained_model/model.pt')
                print('save finish - model.pt')

            global_step+=1

    print(f'\n!!!!!!!!!!!!!Train Finish!!!!!!!!!!!!!!!!\n')

    return model.to("cpu"), tokenizer

#-------------------------------------------------------
if torch.cuda.is_available()==True:
    device = "cuda"
else:
    device = "cpu"

model, tokenizer = training(training_args, model_name, device)
torch.save(model, '../trained_model/model.pt')
model.save_pretrained('../trained_model')
tokenizer.save_pretrained('../save_tokenizer')
print(f'Save Finish!')