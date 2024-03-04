from transformers import AutoTokenizer, BartForConditionalGeneration, AutoConfig, Trainer, TrainingArguments, AutoFeatureExtractor, set_seed, AdamW
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
from rouge import Rouge

dataset_path = "../dataset"
train_dataset_path = os.path.join(dataset_path, "Training")
valid_dataset_path = os.path.join(dataset_path, "Validation")

def training(args, model_name, device):

    train_data1 = load_dataset(os.path.join(train_dataset_path, "training_dataset1"))
    train_data2 = load_dataset(os.path.join(train_dataset_path, "training_dataset2"))
    train_data3 = load_dataset(os.path.join(train_dataset_path, "training_dataset3"))
    train_data4 = load_dataset(os.path.join(train_dataset_path, "training_dataset4"))
    train_data = pd.concat([train_data1, train_data2, train_data3, train_data4], ignore_index=True)


    print("!!!!!!!")
    model_config = AutoConfig.from_pretrained(model_name)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name, config = model_config)

    for i in trange(len(train_data['passage']), desc="passage 토큰 길이 측정 "):
        cnt=0
        if len(tokenizer.tokenize(train_data['passage'][i]))>1022:
            cnt+=1

    print(f'1024토큰이 넘는 문서의 수 : {cnt}\n')
    print(train_data.columns)
        
    train_data = make_dataset(tokenizer, train_data['passage'], train_data['summary'])  #(input_ids, attention_mask, token_type_ids, overflow_to_sample_mapping)

    train_sampler = RandomSampler(train_data)
    train_loader = DataLoader(train_data, sampler=train_sampler, batch_size = args.per_device_train_batch_size)

    loss_fn = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    args.learning_rate= 4e-05
    optimizer = AdamW(model.parameters(), lr = args.learning_rate, eps=args.adam_epsilon)

    model.to(device)

    print(f'{args.learning_rate=}')

    print(f'\n!!!!!!!!!!!!!Train Start!!!!!!!!!!!!!!!!\n')

    global_step = 0

    model.zero_grad()
    torch.cuda.empty_cache()

    for _ in trange(int(args.num_train_epochs), desc="Epoch "):
        for batch in tqdm(train_loader, desc=f'training progress '):
            model.train()

            batch = tuple(t.to(device) for t in batch)
            
            context_input = {'input_ids':batch[0], 'attention_mask': batch[1], 'token_type_ids': batch[2]}
            target_input = {'input_ids':batch[3], 'attention_mask': batch[4], 'token_type_ids': batch[5]}

            # output = model(input_ids = context_input['input_ids'], attention_mask = context_input['attention_mask'],
            #                decoder_input_ids = target_input['input_ids']).logits
            # loss = loss_fn(output[:, :-1, :].reshape(-1, output.size(-1)), target_input['input_ids'][:,1:].reshape(-1))
            #위의 코드는 수정해야 사용할 수 있음
            loss = model(input_ids = context_input['input_ids'], attention_mask = context_input['attention_mask'],
                           labels = target_input['input_ids']).loss
        
            loss.backward()
            optimizer.step()
            model.zero_grad()
        
            if global_step%500==0:
                print(f'{global_step=} training{loss=}')

            global_step+=1

    print(f'\n!!!!!!!!!!!!!Train Finish!!!!!!!!!!!!!!!!\n')

    return model

def validation(model, model_name, device):
    valid_data1 = load_dataset(os.path.join(valid_dataset_path, "valid_dataset1"))
    valid_data2 = load_dataset(os.path.join(valid_dataset_path, "valid_dataset2"))
    valid_data3 = load_dataset(os.path.join(valid_dataset_path, "valid_dataset3"))
    valid_data4 = load_dataset(os.path.join(valid_dataset_path, "valid_dataset4"))
    valid_data = pd.concat([valid_data1, valid_data2, valid_data3, valid_data4], ignore_index=True)

    rouge = Rouge()
    model.to(device)
    context = valid_data['passage']
    target = valid_data['summary'].to_list()
    torch.cuda.empty_cache()

    with torch.no_grad():
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        outputs = []
        for i in trange(len(context), desc='eval '):
            token = tokenizer.encode(context[i], return_tensors='pt').to(device)
            summary_text_ids = model.generate(
                                    input_ids=token,
                                    bos_token_id=tokenizer.bos_token_id,
                                    eos_token_id=tokenizer.eos_token_id,
                                    length_penalty=2.0,
                                    max_length=300,
                                    min_length=50,
                                    num_beams=6,
                                    ).to("cpu")
            
            output = tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
            outputs.append(output)
        
    score = rouge.get_scores(outputs, target, avg=True)
    for k in score.keys():
        print(f'{k} = {score[k]}')

