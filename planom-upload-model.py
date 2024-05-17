
import elasticsearch
from pathlib import Path
from eland.ml.pytorch import PyTorchModel
from eland.ml.pytorch.transformers import TransformerModel
import requests
import os

model_id= "sentence-transformers/all-mpnet-base-v2"

endpoint = os.getenv('ES_SERVER', 'ERROR') 
username = os.getenv('ES_USERNAME', 'ERROR') 
password = os.getenv('ES_PASSWORD', 'ERROR')

#es_url = f"https://{username}:{password}@{endpoint}:443"
es_url = f"http://{username}:{password}@{endpoint}"
#es_url = f"https://{username}:{password}@{endpoint}"


# Load a Hugging Face transformers model directly from the model hub
#tm = TransformerModel(f"{model_id}", "text_embedding")
tm = TransformerModel(model_id="sentence-transformers/all-mpnet-base-v2", task_type="text_embedding")

tmp_path = "models"
Path(tmp_path).mkdir(parents=True, exist_ok=True)
model_path, config, vocab_path = tm.save(tmp_path)

es = elasticsearch.Elasticsearch(es_url, timeout=300)  # 5 minute timeout
ptm = PyTorchModel(es, tm.elasticsearch_model_id())
try:
  ptm.import_model(model_path=model_path, config_path=None, vocab_path=vocab_path, config=config)
except Exception as error:
  # Handle the BadRequestError exception here
  if error.meta.status == 400 and error.message == "resource_already_exists_exception":
    print("Done -- the model was already loaded")
  else:
    print("An error occurred:", str(error))


# def deploy_model(model_id,es_url):
#   url = f"{es_url}/_ml/trained_models/{model_id}/deployment/_start"
#   response = requests.post(url)
#   if response.status_code == 200:
#     print("Model Deployed")
#   else:
#     print("Error deploying model: ", response.text)

# deploy_model(es_model_id,es_url)

# mapping = {
#     "mappings": {
#       "properties": {
#         "metadata": {
#           "type": "object"
#         },
#         "text": {
#           "type": "text"
#         },
#         "vector": {
#           "type": "dense_vector",
#           "dims": 768
#         }
#       }
#     }
# }
