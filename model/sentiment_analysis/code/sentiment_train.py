from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, TrainingArguments, Trainer
from datasets import Dataset, load_dataset
import evaluate

import numpy as np

def do_train():
  # set model name and data directory
  # training data source: "https://github.com/ukairia777/finance_sentiment_corpus.git"
  model_name = "klue/roberta-large"
  train_data = '../data/train.csv'
  eval_data = '../data/eval.csv'
  test_data = '../data/test.csv'
  ckpt_output = '../output/ckpt_output/'
  model_output = f'../output/model_output/{"_".join(model_name.split("/"))}_trained'
  
  id2label = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
  label2id = {"NEGATIVE": 0, "NEUTRAL": 1, "POSITIVE": 2}

  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3, id2label=id2label, label2id=label2id)

  def preprocess_function(examples):
      return tokenizer(examples["title"], truncation=True)

  dataset = load_dataset('csv', data_files={'train': train_data, 'eval': eval_data, 'test': test_data})
  tokenized_dataset = dataset.map(preprocess_function, batched=True)

  data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

  accuracy = evaluate.load("accuracy")

  def compute_metrics(eval_pred):
      predictions, labels = eval_pred
      predictions = np.argmax(predictions, axis=1)
      return accuracy.compute(predictions=predictions, references=labels)

  training_args = TrainingArguments(
      output_dir=ckpt_output,
      learning_rate=2e-5,
      per_device_train_batch_size=16,
      per_device_eval_batch_size=16,
      num_train_epochs=5,
      weight_decay=0.01,
      evaluation_strategy="epoch",
      save_strategy="epoch",
      save_total_limit=2,
      load_best_model_at_end=True,
  )

  trainer = Trainer(
      model=model,
      args=training_args,
      train_dataset=tokenized_dataset['train'],
      eval_dataset=tokenized_dataset['eval'],
      tokenizer=tokenizer,
      data_collator=data_collator,
      compute_metrics=compute_metrics,
  )
  
  trainer.train()
  print('-'*10, 'Training finished. Saving Model.', '-'*10)
  trainer.save_model(model_output)
  
  eval_metric = trainer.evaluate(tokenized_dataset['test'])
  print(eval_metric)

if __name__=='__main__':
  do_train()
