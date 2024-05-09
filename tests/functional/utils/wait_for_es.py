import logging
import os
import time
from elasticsearch import Elasticsearch

es_host = os.getenv('ELASTIC_HOST', 'localhost')
es_port = os.getenv('ELASTIC_PORT', '9200')
es_url = f"http://{es_host}:{es_port}"

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=[es_url], verify_certs=False)
    while not es_client.ping():
        print("Waiting for Elasticsearch to be ready...")
        break
    print("Waiting for Elasticsearch to be ready...123")
