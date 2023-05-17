import os
from tensorflow import keras
from google.cloud import storage


def load_model():
    bucket_name = os.environ.get('BUCKET_NAME')

    print('Loading latest model from GCS...')

    client = storage.Client()
    blobs = list(client.get_bucket(bucket_name).list_blobs(prefix="model"))

    try:
        latest_blob = max(blobs, key=lambda x: x.updated)
        latest_model_path_to_save = os.path.join(os.getcwd(), latest_blob.name)
        latest_blob.download_to_filename(latest_model_path_to_save)

        latest_model = keras.models.load_model(latest_model_path_to_save)

        print("✅ Latest model downloaded from cloud storage")

        return latest_model

    except:
        print(f"\n❌ No model found in GCS bucket {bucket_name}")

        return None
