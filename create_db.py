import os
import pickle
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

load_dotenv()

LL_MODEL = os.environ.get("LL_MODEL")


def create_index_db(source_chunks):
    model_id = LL_MODEL
    # model_kwargs = {'device': 'cpu'}
    model_kwargs = {'device': 'cuda'}
    embeddings = HuggingFaceEmbeddings(
      model_name=model_id,
      model_kwargs=model_kwargs
    )

    db = FAISS.from_documents(source_chunks, embeddings)
    return db


if __name__ == '__main__':    
    with open('./data/source_chunks.pkl', 'rb') as file:
        source_chunks = pickle.load(file)

    index_db = create_index_db(source_chunks)

    with open('./data/index_db.pkl', 'wb') as file:
        pickle.dump(index_db, file)    
