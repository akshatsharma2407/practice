from flask import Flask,render_template,request
import mlflow
from preprocessing_utility import normalize_text
import dagshub
import pickle
import os

# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("AKSHAT")
if not dagshub_token:
    raise EnvironmentError("AKSHAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "akshatsharma2407"
repo_name = "practice"

app = Flask(__name__)

# load model from model registry
def get_latest_model_version(model_name):
    client = mlflow.MlflowClient()
    latest_version = client.get_latest_versions(model_name, stages=["Production"])
    if not latest_version:
        latest_version = client.get_latest_versions(model_name, stages=["None"])
    return latest_version[0].version if latest_version else None

model_name = "my_model"
model_version = get_latest_model_version(model_name)

model_uri = f'models:/{model_name}/{model_version}'
model = mlflow.pyfunc.load_model(model_uri)

vectorizer = pickle.load(open('models/vectorizer.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    text = request.form['text']


    #clean
    text = normalize_text(text)

    #bow
    features = vectorizer.transform([text])

    #prediction
    result = model.predict(features)

    #show
    if str(result[0]) == 0:
        return 'sad'
    else:
        return 'happy'

app.run(debug=True)