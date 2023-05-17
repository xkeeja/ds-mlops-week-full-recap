from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from solution.fastapi.script.load_model import load_model


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.model = load_model()


@app.get("/")
def root():
    return dict(greeting="Welcome to my salary predictor!")


@app.get("/predict")
def predict(gender, age, tenure):

    if gender == 'M':
        X = [[1, 0, int(age), int(tenure)]]
    else:
        X = [[0, 1, int(age), int(tenure)]]

    model = app.state.model
    assert model is not None

    y_pred = model.predict(X)

    return dict(salary=float(y_pred))
