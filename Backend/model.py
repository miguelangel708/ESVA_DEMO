
import openai
import os
from dataclasses import dataclass
from llama_index.llms.openai import OpenAI

@dataclass
class LoadModel:
    model_name: str
    model_temperature: str

    def load_model(self):
        """The load_model method loads the OpenAI api key and instanciates the gpt-3.5-turbo model and a defined temperature

        Returns:
            llm: Instanciated OpenAI LLM model
        """        
        # OpenAI API key

        openai.api_key =  os.environ['OpenAi-apiKey']
        # Load LLM
        llm = OpenAI(model = self.model_name, temperature = self.model_temperature)
        return llm