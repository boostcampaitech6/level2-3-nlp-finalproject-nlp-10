from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, TrainingArguments, Trainer
from datasets import Dataset
import evaluate

import pandas as pd
import numpy as np

def do_predict():
  # set model and data directory
  model_name_or_path = "../output/model_output/klue_roberta-large_trained"
  pred_data_path = '../data/FIN_NEWS_SUMMARY.csv' # combined news data
  pred_output_dir = '../output/roberta_large_pred.csv'
  
  id2label = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
  label2id = {"NEGATIVE": 0, "NEUTRAL": 1, "POSITIVE": 2}

  tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
  model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path, num_labels=3, id2label=id2label, label2id=label2id)

  def preprocess_function(examples):
      return tokenizer(examples["title"], truncation=True)

  #predict using news title
  pred_df = pd.read_csv(pred_data_path)
  dataset = Dataset.from_dict({'title':pred_df['title'].tolist()})
  tokenized_dataset = dataset.map(preprocess_function, batched=True)

  data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

  accuracy = evaluate.load("accuracy")

  def compute_metrics(eval_pred):
      predictions, labels = eval_pred
      predictions = np.argmax(predictions, axis=1)
      return accuracy.compute(predictions=predictions, references=labels)

  training_args = TrainingArguments(
      output_dir='./ckpt_output/',
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
      tokenizer=tokenizer,
      data_collator=data_collator,
      compute_metrics=compute_metrics,
  )
  
  prediction = trainer.predict(tokenized_dataset)
  print('-'*10,'Saving prediction result','-'*10)
  pred_result = {
    'news_id': pred_df['news_id'].tolist(),
    'title': pred_df['title'].tolist(),
    'pred_labels': [np.argmax(pred) for pred in prediction.predictions]
    }
  pred_result = pd.DataFrame(pred_result)
  pred_result.to_csv(pred_output_dir,index=False)
  
if __name__=='__main__':
  do_predict()
