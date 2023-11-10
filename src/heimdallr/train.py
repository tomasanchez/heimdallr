"""Train
Script to train the model.
"""
import os

import joblib
import pandas as pd
import spacy
from sklearn.model_selection import train_test_split

from heimdallr.adapters.assignment_reader import SklearnTopicPredictor
from heimdallr.dependencies import NLP_SPANISH

# convert to pandas dataframe


if __name__ == "__main__":
    print("Training the model...")
    # train the model
    print("Step 1. Loading the data...")
    upper_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(upper_dir, "db", "training.csv")
    df = pd.read_csv(path)
    print(f"Data loaded successfully. Detected {len(df)} rows.")
    print("Step 2. Preprocessing the data...")
    # create train and test set
    train, test = train_test_split(df, test_size=0.33, random_state=42)
    print("Training Data Shape:", train.shape)
    print("Testing Data Shape:", test.shape)

    # convert to list
    content_list = train["content"].tolist()
    train1 = []
    for sentences in content_list:
        train1.append("".join(sentences))
    labelsTrain1 = train["topic"].tolist()

    # load spaCy
    print("Step 3. Loading spaCy...")
    nlp = spacy.load(NLP_SPANISH)
    topic_predictor = SklearnTopicPredictor(nlp=nlp, download=True)
    topic_predictor.pipeline.fit(train1, labelsTrain1)

    # save the model
    print("Step 4. Saving the model...")
    model_path = os.path.join(upper_dir, "models", "topic_predictor_dev.joblib")
    joblib.dump(topic_predictor.pipeline, model_path)
    print(f"Model trained and saved at: {model_path}")
