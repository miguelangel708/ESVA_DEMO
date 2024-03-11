from model import LoadModel
from automerging import DataProcessing
from generate_answer import GetAnswer

llm = LoadModel('gpt-3.5-turbo', 0.1).load_model()
query_engine = DataProcessing(llm, 'sentence-transformers/all-MiniLM-L6-v2', 'BAAI/bge-reranker-base','./files/ft_merging_index', 12, 6).get_automerging_query_engine()
get_answer = GetAnswer(query_engine)
