#!/usr/bin/env python3
"""
Fine-tuning Script for TrueSight Deepfake Detection Models
=========================================================

This script fine-tunes the video and audio models for improved deepfake detection accuracy.
"""

import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoModelForImageClassification, 
    AutoFeatureExtractor,
    Wav2Vec2Model, 
    Wav2Vec2Processor,
    TrainingArguments, 
    Trainer
)
from datasets import Dataset as HFDataset
import librosa
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from loguru import logger
import argparse


class VideoDeepfakeDataset(Dataset):
    """Dataset class for video deepfake detection fine-tuning"""
    
    def __init__(self, real_videos, fake_videos, feature_extractor, max_frames=40):
        self.real_videos = real_videos
        self.fake_videos = fake_videos
        self.feature_extractor = feature_extractor
        self.max_frames = max_frames
        
        # Combine datasets with labels
        self.video_paths = real_videos + fake_videos
        self.labels = [0] * len(real_videos) + [1] * len(fake_videos)  # 0 for real, 1 for fake
    
    def __len__(self):
        return len(self.video_paths)
    
    def __getitem__(self, idx):
        video_path = self.video_paths[idx]
        label = self.labels[idx]
        
        # Extract frames from video
        frames = self.extract_frames(video_path)
        
        # Preprocess frames
        inputs = self.feature_extractor(
            images=frames, 
            return_tensors="pt", 
            padding=True
        )
        
        return {
            "pixel_values": inputs["pixel_values"],
            "labels": torch.tensor(label, dtype=torch.long)
        }
    
    def extract_frames(self, video_path):
        """Extract frames from video file"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Sample frames evenly
        if total_frames <= self.max_frames:
            # If video has fewer frames than max, take all frames
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
        else:
            # Sample frames evenly
            step = total_frames / self.max_frames
            for i in range(self.max_frames):
                frame_idx = int(i * step)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame_rgb)
        
        cap.release()
        return frames


class AudioDeepfakeDataset(Dataset):
    """Dataset class for audio deepfake detection fine-tuning"""
    
    def __init__(self, real_audios, fake_audios, processor, target_sr=16000, max_length=480000):  # 30 sec at 16kHz
        self.real_audios = real_audios
        self.fake_audios = fake_audios
        self.processor = processor
        self.target_sr = target_sr
        self.max_length = max_length
        
        # Combine datasets with labels
        self.audio_paths = real_audios + fake_audios
        self.labels = [0] * len(real_audios) + [1] * len(fake_audios)  # 0 for real, 1 for fake
    
    def __len__(self):
        return len(self.audio_paths)
    
    def __getitem__(self, idx):
        audio_path = self.audio_paths[idx]
        label = self.labels[idx]
        
        # Load and preprocess audio
        audio_input = self.load_audio(audio_path)
        
        # Process with Wav2Vec2 processor
        inputs = self.processor(
            audio_input, 
            sampling_rate=self.target_sr,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length
        )
        
        return {
            "input_values": inputs["input_values"],
            "labels": torch.tensor(label, dtype=torch.long)
        }
    
    def load_audio(self, audio_path):
        """Load and preprocess audio file"""
        audio, sr = librosa.load(audio_path, sr=self.target_sr)
        
        # Pad or trim to max length
        if len(audio) > self.max_length:
            audio = audio[:self.max_length]
        else:
            # Pad with zeros
            pad_length = self.max_length - len(audio)
            audio = np.pad(audio, (0, pad_length), mode='constant')
        
        return audio


def fine_tune_video_model(train_dataset, val_dataset, output_dir="./models/video_finetuned"):
    """Fine-tune the video deepfake detection model"""
    logger.info("Starting video model fine-tuning...")
    
    # Load pre-trained model
    model = AutoModelForImageClassification.from_pretrained(
        "facebook/deit-base-patch16-224",
        num_labels=2,  # REAL vs FAKE
        ignore_mismatched_sizes=True
    )
    
    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        dataloader_pin_memory=True,
        remove_unused_columns=False,
        report_to=None,  # Disable reporting to keep logs clean
    )
    
    # Define compute metrics function
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        accuracy = (predictions == labels).mean()
        
        # Calculate precision, recall, f1
        from sklearn.metrics import precision_recall_fscore_support
        precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='binary')
        
        return {
            'accuracy': accuracy,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )
    
    # Train the model
    trainer.train()
    
    # Save the fine-tuned model
    trainer.save_model(output_dir)
    logger.info(f"Video model fine-tuning completed. Model saved to {output_dir}")
    
    return trainer


def fine_tune_audio_model(train_dataset, val_dataset, output_dir="./models/audio_finetuned"):
    """Fine-tune the audio deepfake detection model"""
    logger.info("Starting audio model fine-tuning...")
    
    # Load pre-trained model
    model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-large-960h")
    
    # Add classification head
    model.classifier = nn.Linear(model.config.hidden_size, 2)  # REAL vs FAKE
    
    # Custom model with classification head
    class Wav2Vec2ForClassification(nn.Module):
        def __init__(self, wav2vec2_model):
            super().__init__()
            self.wav2vec2 = wav2vec2_model
            self.classifier = nn.Linear(wav2vec2_model.config.hidden_size, 2)
            self.dropout = nn.Dropout(0.1)
        
        def forward(self, input_values, labels=None):
            outputs = self.wav2vec2(input_values)
            hidden_states = outputs.last_hidden_state
            # Mean pooling
            pooled_output = torch.mean(hidden_states, dim=1)
            pooled_output = self.dropout(pooled_output)
            logits = self.classifier(pooled_output)
            
            loss = None
            if labels is not None:
                loss_fct = nn.CrossEntropyLoss()
                loss = loss_fct(logits.view(-1, 2), labels.view(-1))
            
            return {
                'loss': loss,
                'logits': logits
            }
    
    model = Wav2Vec2ForClassification(model)
    
    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,  # Smaller batch size due to audio length
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        dataloader_pin_memory=True,
        remove_unused_columns=False,
        report_to=None,  # Disable reporting to keep logs clean
    )
    
    # Define compute metrics function
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        accuracy = (predictions == labels).mean()
        
        # Calculate precision, recall, f1
        from sklearn.metrics import precision_recall_fscore_support
        precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='binary')
        
        return {
            'accuracy': accuracy,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )
    
    # Train the model
    trainer.train()
    
    # Save the fine-tuned model
    trainer.save_model(output_dir)
    logger.info(f"Audio model fine-tuning completed. Model saved to {output_dir}")
    
    return trainer


def prepare_datasets(data_dir, test_size=0.2):
    """Prepare datasets for fine-tuning"""
    logger.info(f"Preparing datasets from {data_dir}")
    
    # Get real and fake video paths
    real_videos = []
    fake_videos = []
    
    real_video_dir = os.path.join(data_dir, "real_videos")
    fake_video_dir = os.path.join(data_dir, "fake_videos")
    
    if os.path.exists(real_video_dir):
        real_videos = [os.path.join(real_video_dir, f) for f in os.listdir(real_video_dir) 
                      if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    if os.path.exists(fake_video_dir):
        fake_videos = [os.path.join(fake_video_dir, f) for f in os.listdir(fake_video_dir) 
                      if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    # Split into train and validation
    real_train, real_val = train_test_split(real_videos, test_size=test_size, random_state=42)
    fake_train, fake_val = train_test_split(fake_videos, test_size=test_size, random_state=42)
    
    # Prepare audio datasets similarly
    real_audios = []
    fake_audios = []
    
    real_audio_dir = os.path.join(data_dir, "real_audios")
    fake_audio_dir = os.path.join(data_dir, "fake_audios")
    
    if os.path.exists(real_audio_dir):
        real_audios = [os.path.join(real_audio_dir, f) for f in os.listdir(real_audio_dir) 
                      if f.lower().endswith(('.wav', '.mp3', '.flac', '.m4a'))]
    
    if os.path.exists(fake_audio_dir):
        fake_audios = [os.path.join(fake_audio_dir, f) for f in os.listdir(fake_audio_dir) 
                      if f.lower().endswith(('.wav', '.mp3', '.flac', '.m4a'))]
    
    # Split audio datasets
    real_audio_train, real_audio_val = train_test_split(real_audios, test_size=test_size, random_state=42)
    fake_audio_train, fake_audio_val = train_test_split(fake_audios, test_size=test_size, random_state=42)
    
    return {
        'video': {
            'train': (real_train, fake_train),
            'val': (real_val, fake_val)
        },
        'audio': {
            'train': (real_audio_train, fake_audio_train),
            'val': (real_audio_val, fake_audio_val)
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Fine-tune TrueSight deepfake detection models")
    parser.add_argument("--data_dir", type=str, required=True, 
                       help="Directory containing real and fake media files")
    parser.add_argument("--output_dir", type=str, default="./models/finetuned", 
                       help="Output directory for fine-tuned models")
    parser.add_argument("--model_type", type=str, choices=['video', 'audio', 'both'], default='both',
                       help="Type of model to fine-tune")
    
    args = parser.parse_args()
    
    # Prepare datasets
    datasets = prepare_datasets(args.data_dir)
    
    if args.model_type in ['video', 'both']:
        logger.info("Fine-tuning video model...")
        
        # Initialize feature extractor
        feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/deit-base-patch16-224")
        
        # Create datasets
        video_train_dataset = VideoDeepfakeDataset(
            datasets['video']['train'][0], 
            datasets['video']['train'][1], 
            feature_extractor
        )
        
        video_val_dataset = VideoDeepfakeDataset(
            datasets['video']['val'][0], 
            datasets['video']['val'][1], 
            feature_extractor
        )
        
        # Fine-tune video model
        fine_tune_video_model(
            video_train_dataset, 
            video_val_dataset, 
            output_dir=os.path.join(args.output_dir, "video")
        )
    
    if args.model_type in ['audio', 'both']:
        logger.info("Fine-tuning audio model...")
        
        # Initialize processor
        processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
        
        # Create datasets
        audio_train_dataset = AudioDeepfakeDataset(
            datasets['audio']['train'][0], 
            datasets['audio']['train'][1], 
            processor
        )
        
        audio_val_dataset = AudioDeepfakeDataset(
            datasets['audio']['val'][0], 
            datasets['audio']['val'][1], 
            processor
        )
        
        # Fine-tune audio model
        fine_tune_audio_model(
            audio_train_dataset, 
            audio_val_dataset, 
            output_dir=os.path.join(args.output_dir, "audio")
        )
    
    logger.info("Fine-tuning completed successfully!")


if __name__ == "__main__":
    main()