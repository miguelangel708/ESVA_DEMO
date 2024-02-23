import openai
import os
from llama_index.llms import OpenAI
from llama_index import (
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index import StorageContext, load_index_from_storage
from llama_index.retrievers import AutoMergingRetriever
from llama_index.indices.postprocessor import SentenceTransformerRerank
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.embeddings import HuggingFaceEmbedding

# OpenAI API key
openai.api_key = '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'

# Load LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)

# load vector index database
def load_automerging_index(
    llm,
    embed_model="sentence-transformers/all-MiniLM-L6-v2",
    save_dir="merging_index",
):
    if not os.path.exists(save_dir):
        print("no se encontró base de datos")
    else:
        merging_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=HuggingFaceEmbedding(model_name=embed_model),
    )
        automerging_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=merging_context,
        )
    return automerging_index

# load the model 
def get_automerging_query_engine(
    automerging_index,
    similarity_top_k=12,
    rerank_top_n=6,
):
    base_retriever = automerging_index.as_retriever(similarity_top_k=similarity_top_k)
    retriever = AutoMergingRetriever(
        base_retriever, automerging_index.storage_context, verbose=True
    )
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )
    auto_merging_engine = RetrieverQueryEngine.from_args(
        retriever, node_postprocessors=[rerank]
    )
    return auto_merging_engine

index = load_automerging_index(
    llm=llm,
    save_dir='./files/ft_merging_index',  #merging means that the docs are separated
)

query_engine = get_automerging_query_engine(index, similarity_top_k=6)

def process_answer(query, query_engine=query_engine):
    response = query_engine.query(query)
    source_documents = response.source_nodes[0].metadata['file_name']
    page_list = [int(i.metadata['page_label']) for i in response.source_nodes]
    #page_list = sorted(list(set(page_list)))
    #page_list = ', '.join(map(str, set(page_list)))
    page_list.sort()
    if(source_documents =="Instructivo_Diligenciamiento_Formato_Reporte_de_Eficiencia_de_Combustion_en_T_1PDJHb8.pdf"):
        source_documents = "Instructivo_Diligenciamiento_1PDJHb8"
    return response.response + f' \n Documento Fuente: {source_documents} \n Paginas: {page_list}'

# while True:
#   user_input = input("Ingrese la pregunta del pdf: ")
#   if user_input:
#       answer = process_answer(user_input)   ##send the input question and answer with the pdf info
#       print(answer)