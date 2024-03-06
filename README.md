<div align="center">
    <a href="">
      <img alt="Banner" src="documents/banner.png" alt="banner">
    </a>
</div>

<br/>

<!-- Table of contents -->
<div>
  <h1>Table of Contents</h1>
  <ul>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#vector-database-overview">Vector Database Overview</a></li>
    <ul>
      <li><a href="#chromadb">Chromadb</a></li>
    </ul>
    <li><a href="#embedding-model">Embedding Model</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#note">Note</a></li>
  </ul>
</div>

# Introduction
It is an AI powered Django application. This application can be used to store large number of images and retrieve images with text and image queries. User can upload images in a zip file. The images will be passed into the embedding model to generate embedding.The application will then create a vector collection to store the image vectors. This vector store is called the knowledge base. When user make a query whether it is image or text, it is converted into vector embedding and similar vectors are retrieved from the vector store. The retrieved similar vectors refers to some image, that images then showed to the user.

<div align="center">
    <img src="documents/application-demo.gif">
</div>

<br>

# Vector Database Overview

<h3>What is Vector Database?</h3>

> It is the collection of learnable embeddings which has a certain dimension. It enables us to compact unstructured data in a single dimension. The exact same kind of database operations can be performed in Vector Database. It uses several mathematical functions to find similarity between query and stored embeddings.

Learn more about distance functions [here](https://weaviate.io/blog/distance-metrics-in-vector-search).

<ul>
  <li>Cosine Similarity.</li>
  <li>DOT Product.</li>
  <li>Euclidean Distance.</li>
</ul>

> The query whether it is text or image, it is converted into embedding vector by doing a forward pass from the embedding/feature extractor model. Then distance is calculated between query vector and stored embedding vector using above distance calculator functions.

<h3>Which vector database is used?</h3>

> There are handful of vector database available for use. Some works in local and some are cloud based database. Each one has its won advantages and disadvantages.

<ul>
  <li><a href="https://qdrant.tech/">Qdrant</a></li>
  <li><a href="https://docs.pinecone.io/docs/overview">Pinecone</a></li>
  <li><a href="https://docs.trychroma.com/">Chroma DB</a></li>
</ul>

## Chromadb
Chromadb is one of the best in my view because of its vast functionalities and integrations. It provides a wrapper function over [HuggingFace](https://huggingface.co/models) models which is very useful. Using this functions, we can choose any model for our specific use case.

# Embedding Model

Embedding model is a pre-trained model that is assigned with the task of generating embedding from data. In this application I have used a pre-trained transformer model [sentence-transformers/clip-ViT-B-32](https://huggingface.co/sentence-transformers/clip-ViT-B-32). This model generates embedding of size `512` for both text and image.

# Installation

Clone the project repository. Go to the project root directory and create a virtual environment with python 3.11.4 and activate it using following commands.

NOTE: Following commands only works for Linux Operating System.

```command
virtualenv venv
source venv/bin/activate
```

When your virtual environment is activated then go for installing dependencies. Run the following commands for installing required libraries and packages.

```command
pip install -r requirements.txt
```

After successfully installing all the dependencies run the following command for executing the Django application.

```command
python manage.py runserver
```

# Note

For using this application user must have to create an account. The file upload section only allows zip files. When user logged in, the application creates a collection and deletes it when user logged out. Once user logged out the vector collections will be lost.