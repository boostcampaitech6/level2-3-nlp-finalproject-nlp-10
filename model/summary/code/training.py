from transformers import AutoTokenizer, AdamW
import torch
import pandas as pd
import os
from tqdm import tqdm, trange
from data_load import load_dataset, pd_load_dataset, load_report_dataset
from torch.utils.data import DataLoader, RandomSampler
from make_dataset import make_dataset
from rouge import Rouge

dataset_path = "../dataset"
book_data_path = os.path.join(dataset_path, "book_sum")    #폴더 안에 하나의 문서당 하나의 json파일 있는 형태
doc_data_path = os.path.join(dataset_path, "doc_sum")      #하나의 hson파일 안에 모든 문서 데이터들 있는 형태
report_data_path = os.path.join(dataset_path, "report_sum")
custom_data_path = os.path.join(dataset_path, "custom_data")
book_train_dataset_path = os.path.join(book_data_path, "Training")
doc_train_dataset_path = os.path.join(doc_data_path, "Training")
report_train_dataset_path = os.path.join(report_data_path, "Training")
book_valid_dataset_path = os.path.join(book_data_path, "Validation")
doc_valid_dataset_path = os.path.join(doc_data_path, "Validation")
report_valid_dataset_path = os.path.join(report_data_path, "Validation")

load_book_data = True
load_doc_data = True
load_report_data = True

def training(args, model, tokenizer, device):
    train_data = pd.DataFrame(columns = ['passage', 'summary'])

    if load_book_data==True:
        train_data1 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset1"))
        train_data2 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset2"))
        train_data3 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset3"))
        train_data4 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset4"))
        train_data = pd.concat([train_data, train_data1, train_data2, train_data3, train_data4], ignore_index=True)
        print(f"book_data_length = {len(train_data1) + len(train_data2) + len(train_data3) + len(train_data4)}")
    
    if load_doc_data==True:
        train_data1 = pd_load_dataset(os.path.join(doc_train_dataset_path, "edit_training_dataset.json"))
        train_data2 = pd_load_dataset(os.path.join(doc_train_dataset_path, "law_training_dataset.json"))
        train_data3 = pd_load_dataset(os.path.join(doc_train_dataset_path, "paper_training_dataset.json"))
        train_data = pd.concat([train_data, train_data1, train_data2, train_data3], ignore_index=True)
        print(f"doc_data_length = {len(train_data1) + len(train_data2) + len(train_data3)}")
    
    if load_report_data == True:        
        train_data1 = load_report_dataset(report_valid_dataset_path)
        train_data = pd.concat([train_data, train_data1], ignore_index=True)
        print(f"report_data_length = {len(train_data1)}")

    print(f"{len(train_data)=}")

    print(f'{train_data.columns=}')
    train_data = make_dataset(tokenizer, train_data['passage'], train_data['summary'])  #(input_ids, attention_mask, token_type_ids, overflow_to_sample_mapping)

    # for i in trange(len(train_data['passage']), desc="passage 토큰 길이 측정 "):
    #     cnt=0
    #     if len(tokenizer.tokenize(train_data['passage'][i]))>1022:
    #         cnt+=1

    # print(f'1024토큰이 넘는 문서의 수 : {cnt}\n')

    train_sampler = RandomSampler(train_data)
    train_loader = DataLoader(train_data, sampler=train_sampler, batch_size = args.per_device_train_batch_size)

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

            loss = model(input_ids = context_input['input_ids'], attention_mask = context_input['attention_mask'],
                           labels = target_input['input_ids']).loss
        
            loss.backward()
            optimizer.step()
            model.zero_grad()
        
            if global_step%1000==0:
                print(f' {global_step=}, Loss={loss.item():.7f}')

            global_step+=1

        model.save_pretrained('../trained_model')
        tokenizer.save_pretrained('../save_tokenizer')

    print(f'\n!!!!!!!!!!!!!Train Finish!!!!!!!!!!!!!!!!\n')

    return model

def validation(model, model_name, device):
    ''' valid data들 다 합치기 '''
    valid_data1 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset1"))
    valid_data2 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset2"))
    valid_data3 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset3"))
    valid_data4 = load_dataset(os.path.join(book_valid_dataset_path, "valid_dataset4"))
    valid_data = pd.concat([valid_data1, valid_data2, valid_data3, valid_data4], ignore_index=True)

    # valid_data1 = pd_load_dataset(os.path.join(doc_valid_dataset_path, "edit_valid_dataset.json"))
    # valid_data2 = pd_load_dataset(os.path.join(doc_valid_dataset_path, "law_valid_dataset.json"))
    # valid_data3 = pd_load_dataset(os.path.join(doc_valid_dataset_path, "paper_valid_dataset.json"))
    # valid_data = pd.concat([valid_data, valid_data1, valid_data2, valid_data3], ignore_index=True)
    
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
                                    max_length=220,
                                    min_length=30,
                                    num_beams=6,
                                    repetition_penalty=1.7,
                                    ).to("cpu")
            
            output = tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
            outputs.append(output)
        
    score = rouge.get_scores(outputs, target, avg=True)
    for k in score.keys():
        print(f'{k} = {score[k]}')

