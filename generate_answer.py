from dataclasses import dataclass

@dataclass
class GetAnswer:

    query_engine: any

    def generate_answer(query, query_engine):
        response = query_engine.query(query)
        source_documents = response.source_nodes[0].metadata['file_name']
        page_list = [int(i.metadata['page_label']) for i in response.source_nodes]
        #page_list = sorted(list(set(page_list)))
        #page_list = ', '.join(map(str, set(page_list)))
        page_list.sort()
        if(source_documents =="Instructivo_Diligenciamiento_Formato_Reporte_de_Eficiencia_de_Combustion_en_T_1PDJHb8.pdf"):
            source_documents = "Instructivo_Diligenciamiento_1PDJHb8"
        return response.response + f' \n Documento Fuente: {source_documents} \n Paginas: {page_list}'
