import dagshub
import mlflow


mlflow.set_tracking_uri('https://dagshub.com/akshatsharma2407/practice.mlflow')
dagshub.init(repo_owner='akshatsharma2407', repo_name='practice', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)


