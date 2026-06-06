import argparse
import os
import pandas as pd
from sentence_transformers import CrossEncoder, InputExample
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser(description="Train a Cross-Encoder model on Labeled Pairs.")
    parser.add_argument("--train_csv", type=str, required=True, help="Path to training CSV.")
    parser.add_argument("--eval_csv", type=str, default=None, help="Path to evaluation CSV.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the trained model.")
    parser.add_argument("--base_model", type=str, default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", help="Base model name.")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs.")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size.")
    parser.add_argument("--warmup_steps", type=int, default=0, help="Warmup steps. Set to 0 to auto-calculate 10% of total steps.")
    
    args = parser.parse_args()

    # Create output directory if not exists
    os.makedirs(args.output_path, exist_ok=True)
    
    print(f"Loading base Cross-Encoder: {args.base_model}")
    model = CrossEncoder(args.base_model, num_labels=1, max_length=512)
    
    print(f"Loading training data from: {args.train_csv}")
    if not os.path.exists(args.train_csv):
        raise FileNotFoundError(f"Train CSV not found at: {args.train_csv}")
        
    df_train = pd.read_csv(args.train_csv)
    
    # Validation of CSV headers
    required_cols = ["cv_text", "jd_text", "label"]
    if not all(col in df_train.columns for col in required_cols):
        raise ValueError(f"CSV must contain headers: {required_cols}")

    # Auto-split eval dataset (80/20) if no separate eval_csv provided
    if args.eval_csv and os.path.exists(args.eval_csv):
        df_eval = pd.read_csv(args.eval_csv)
        print(f"Using provided eval data: {len(df_eval)} samples")
    else:
        df_train, df_eval = train_test_split(df_train, test_size=0.2, random_state=42)
        print(f"Auto-split: {len(df_train)} train, {len(df_eval)} eval")

    # Calculate dynamic warmup steps if set to 0
    if args.warmup_steps == 0:
        total_steps = (len(df_train) // args.batch_size) * args.epochs
        args.warmup_steps = int(total_steps * 0.1)
        print(f"Auto-calculated warmup_steps: {args.warmup_steps}")

    train_examples = [
        InputExample(texts=[str(row['cv_text']), str(row['jd_text'])], label=float(row['label']))
        for _, row in df_train.iterrows()
    ]
    
    eval_examples = [
        InputExample(texts=[str(row['cv_text']), str(row['jd_text'])], label=float(row['label']))
        for _, row in df_eval.iterrows()
    ]

    print(f"Training examples: {len(train_examples)}, Evaluation examples: {len(eval_examples)}")
    
    train_loader = DataLoader(train_examples, shuffle=True, batch_size=args.batch_size)
    
    # Custom loss wrapper to log progress
    import torch.nn as nn
    class LoggingBCEWithLogitsLoss(nn.Module):
        def __init__(self):
            super().__init__()
            self.loss_fn = nn.BCEWithLogitsLoss()
            self.step = 0
            
        def forward(self, logits, labels):
            loss = self.loss_fn(logits, labels)
            self.step += 1
            if self.step % 50 == 0:
                print(f"Step {self.step} - Loss: {loss.item():.4f}")
            return loss
            
    print("Starting Cross-Encoder training...")
    model.fit(
        train_dataloader=train_loader,
        epochs=args.epochs,
        loss_fct=LoggingBCEWithLogitsLoss(),
        warmup_steps=args.warmup_steps,
        output_path=args.output_path
    )
    
    print(f"Saving Cross-Encoder model to {args.output_path}...")
    model.save(args.output_path)
    
    print(f"Cross-Encoder training complete! Model saved to {args.output_path}")

if __name__ == "__main__":
    main()
