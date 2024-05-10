import os
import time
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.test')

es_host = os.getenv('ELASTIC_HOST', 'localhost')
es_port = os.getenv('ELASTIC_PORT', '9200')
es_url = f'http://{es_host}:{es_port}'

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=[es_url], verify_certs=False)
    while es_client.ping():
        break

    time.sleep(1)
