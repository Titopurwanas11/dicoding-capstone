import argparse
import os
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, SentenceTransformerTrainingArguments, SentenceTransformerTrainer, losses
from datasets import Dataset
from transformers import EarlyStoppingCallback
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser(description="Train a Bi-Encoder model on Triplet data with optimizations.")
    parser.add_argument("--train_csv", type=str, required=True, help="Path to training CSV.")
    parser.add_argument("--eval_csv", type=str, default=None, help="Path to evaluation CSV.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the trained model.")
    parser.add_argument("--base_model", type=str, default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", help="Base model name.")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs.")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size.")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate.")
    
    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)
    
    print(f"Loading base model: {args.base_model}")
    model = SentenceTransformer(args.base_model)
    
    print(f"Loading training data from: {args.train_csv}")
    if not os.path.exists(args.train_csv):
        raise FileNotFoundError(f"Train CSV not found at: {args.train_csv}")
        
    df_train = pd.read_csv(args.train_csv)
    
    required_cols = ["anchor", "positive", "negative"]
    if not all(col in df_train.columns for col in required_cols):
        raise ValueError(f"CSV must contain headers: {required_cols}")

    # Split train and eval if no separate eval_csv is provided
    if args.eval_csv and os.path.exists(args.eval_csv):
        print(f"Loading evaluation data from: {args.eval_csv}")
        df_eval = pd.read_csv(args.eval_csv)
    else:
        print("No separate evaluation CSV provided. Splitting training data 90/10...")
        df_train, df_eval = train_test_split(df_train, test_size=0.1, random_state=42)
        df_train = df_train.reset_index(drop=True)
        df_eval = df_eval.reset_index(drop=True)
    
    # Convert to Dataset format
    train_dataset = Dataset.from_pandas(df_train).shuffle(seed=42)
    eval_dataset = Dataset.from_pandas(df_eval)
    
    print(f"Training samples: {len(train_dataset)}, Evaluation samples: {len(eval_dataset)}")
    
    print("Setting up training configurations...")
    training_args = SentenceTransformerTrainingArguments(
        output_dir=args.output_path,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.lr,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
        fp16=torch.cuda.is_available(),
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        save_total_limit=2,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine"
    )
    
    train_loss = losses.MultipleNegativesRankingLoss(model)
    
    current_batch_size = args.batch_size
    current_grad_accum = 1
    success = False
    
    print("Starting Bi-Encoder training with optimization...")
    while not success and current_batch_size >= 1:
        print(f"Trying training with batch_size: {current_batch_size}, gradient_accumulation_steps: {current_grad_accum}")
        training_args.per_device_train_batch_size = current_batch_size
        training_args.per_device_eval_batch_size = current_batch_size
        training_args.gradient_accumulation_steps = current_grad_accum
        
        trainer = SentenceTransformerTrainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            loss=train_loss,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
        )
        
        try:
            trainer.train()
            success = True
        except RuntimeError as e:
            if "out of memory" in str(e).lower() and torch.cuda.is_available():
                print(f"WARNING: CUDA Out Of Memory detected. Halving batch size and doubling gradient accumulation.")
                torch.cuda.empty_cache()
                current_batch_size = current_batch_size // 2
                current_grad_accum = current_grad_accum * 2
                if current_batch_size < 1:
                    print("ERROR: Minimum batch size reached. Cannot train model.")
                    raise e
            else:
                raise e
    
    print(f"Saving fine-tuned model to: {args.output_path}")
    model.save_pretrained(args.output_path)
    print("Bi-Encoder training complete!")

if __name__ == "__main__":
    main()
