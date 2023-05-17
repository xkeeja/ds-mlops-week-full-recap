import numpy as np
from sklearn.preprocessing import OneHotEncoder


def preprocess(df):
    X = df[['Age', 'Tenure_in_org_in_months']]

    enc = OneHotEncoder(categories=[['M','F']], sparse_output=False)
    gender_enc = enc.fit_transform(df[['Gender']])

    X_processed = np.hstack((gender_enc, np.array(X)))
    y = df['GROSS']

    print("✅ Data preprocessed")

    return X_processed, y
