import os
import time
from google.cloud import storage
from tensorflow.keras import Sequential, layers, optimizers


def initialize_model(shape):
    model = Sequential()
    model.add(layers.Input(shape=shape))
    model.add(layers.Dense(20, activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(10, activation="relu"))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(rate=0.2))
    model.add(layers.Dense(1, activation="linear"))

    print("✅ Model initialized")

    return model


def compile_model(model, learning_rate=0.02):
    optimizer = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mae"])

    print("✅ Model compiled")

    return model


def save_model_gcs(model):
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    model_path = os.path.join(os.getcwd(),'models',f'{timestamp}.h5')
    model.save(model_path)

    print("✅ Model saved locally")

    model_filename = f'{timestamp}.h5' # e.g. "20230208-161047.h5" for instance
    client = storage.Client()
    bucket = client.bucket(os.environ.get('BUCKET_NAME'))
    blob = bucket.blob(f"models/{model_filename}")
    blob.upload_from_filename(model_path)

    print("✅ Model saved to GCS bucket")

    return None
