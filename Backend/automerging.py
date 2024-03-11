import os
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from dataclasses import dataclass

@dataclass
class DataProcessing:
    llm: any 
    embed_model_name: str
    rerank_model: str
    save_dir: str
    similarity_top_k: int
    rerank_top_n: int

    # load vector index database
    def load_automerging_index(self):
        """The load_automerging_index method checks if and index already exist and if not creates the index by embedding the available documentation

        Args:
            llm: Large Language model

        Returns:
            automerging_index: returns the index to do the querys
        """        
        Settings.llm = self.llm 
        Settings.embed_model = HuggingFaceEmbedding(model_name = self.embed_model_name)
        
        automerging_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir = self.save_dir)
        )
        return automerging_index

    # load the model 
    def get_automerging_query_engine(self):
        """The get_automerging_query_engine method takes the automerging index and creates the query engine that reranks the more relevant answers

        Args:
            automerging_index: Index database

        Returns:
            auto_merging_engine: Auto merging engine to do querys
        """        
        automerging_index = self.load_automerging_index()
        base_retriever = automerging_index.as_retriever(similarity_top_k = self.similarity_top_k)
        retriever = AutoMergingRetriever(
            base_retriever, automerging_index.storage_context, verbose = True
        )
        rerank = SentenceTransformerRerank(
            top_n = self.rerank_top_n, model = self.rerank_model
        )
        auto_merging_engine = RetrieverQueryEngine.from_args(
            retriever, node_postprocessors=[rerank]
        )
        return auto_merging_engine
    
