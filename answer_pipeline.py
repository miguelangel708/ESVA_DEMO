import openai
import os
from dataclasses import dataclass
from model import LoadModel
from automerging import DataProcessing
from generate_answer import GetAnswer

key = '_'
load_llm = LoadModel(key,'gpt-3.5-turbo', 0.1)
llm = LoadModel.load_model()
data_processing = DataProcessing(llm, 'sentence-transformers/all-MiniLM-L6-v2', 'BAAI/bge-reranker-base','./files/ft_merging_index', 12, 6)
query_engine = data_processing.get_automerging_query_engine()
get_answer = GetAnswer(query_engine)
