import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from dashboard.settings import BASE_DIR
import os
from PIL import Image
import numpy as np

class ChromadbOperations:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(BASE_DIR / 'database'))
        self.collection = self.client.get_or_create_collection(name='multimodal_collection',
                                                               embedding_function=OpenCLIPEmbeddingFunction(),
                                                               data_loader=ImageLoader())
        
    def insert_data(self, image_path):
        image_names = ["uploads/images/" + single_path for single_path in os.listdir(image_path)]
        image_ids = [str(i) for i in range(1, len(image_names)+1)]
        self.collection.add(ids=image_ids, uris=image_names)

    def query_with_text(self, query_text):
        query_result = self.collection.query(query_texts=[query_text], include=['data'], n_results=3)
        return query_result['uris'][0]

    def query_with_image(self, query_image_path: str):
        query_image = np.array(Image.open(query_image_path))
        query_results = self.collection.query(query_images=[query_image], include=['uris'], n_results=3)
        return query_results['uris'][0]
    
    def number_of_vectors(self):
        return self.collection.count()

    def create_vector_storage(self):
        self.__init__()

    def delete_vector_storage(self):
        self.client.delete_collection(name='multimodal_collection')