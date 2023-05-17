import os

import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping

from solution.ml.tools.preprocess import preprocess
from solution.ml.tools.model import initialize_model, compile_model, save_model_gcs


def train():
    # load raw data
    csv_path = os.path.join(os.getcwd(),'data','raw_salaries.csv')
    df = pd.read_csv(csv_path)

    # preprocess data
    X, y = preprocess(df)

    # initialize & compile model
    model = initialize_model(X.shape[1:])
    model = compile_model(model)

    # train model
    es = EarlyStopping(
        monitor="val_loss",
        patience=10,
        restore_best_weights=True,
        verbose=0
    )

    print("Training model...")

    _ = model.fit(
        X,
        y,
        validation_split=0.3,
        epochs=500,
        batch_size=16,
        callbacks=[es],
        verbose=0
    )

    print("✅ Training complete")

    # save model
    print("Saving model to GCS bucket...")
    save_model_gcs(model)


if __name__ == '__main__':
    train()
