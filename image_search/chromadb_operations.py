import open_clip
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from dashboard.settings import BASE_DIR
import os

class ChromadbOperations:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(BASE_DIR / 'database'))
        self.collection = self.client.get_or_create_collection(name='multimodal_collection',
                                                               embedding_function=OpenCLIPEmbeddingFunction(),
                                                               data_loader=ImageLoader())
        
    def insert_data(self, image_path):
        image_names = [(str(image_path) + '/' + single_path) for single_path in os.listdir(image_path)]
        image_ids = [str(i) for i in range(1, len(image_names)+1)]
        self.collection.add(ids=image_ids, uris=image_names)