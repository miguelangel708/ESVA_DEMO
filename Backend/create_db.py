import os
from dataclasses import dataclass
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


@dataclass
class CreateDatabase:
    llm: any
    embed_model_name: str
    dir_path: str
    persist_dir: str
    

    def create_database(self):
        """The create_database method, reads the documents on a defined path, creates the index and stores it

        Returns:
           index (any): index database of documents
        """        

        Settings.llm = self.llm 
        Settings.embed_model = HuggingFaceEmbedding(model_name = self.embed_model_name)
        document = SimpleDirectoryReader(input_dir = self.dir_path).load_data()

        index = VectorStoreIndex.from_documents(document)
        index.storage_context.persist(persist_dir = self.persist_dir)
