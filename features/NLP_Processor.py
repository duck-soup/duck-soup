'''
input:
    - openaikey: string
    - summarizer_model: string
    - qa_model: string
    - text_generation_model: string
output:
    - NLP object 

----
class NLP:
  def __init__( openai_key = "", summarizer_model = None, qa_model = None, text_generation_model = None):
    self.openai_key = openai_key
    self.summarizer_model = summarizer_model
    self.qa_model = qa_model
    self.text_generation_model = text_generation_model

  def _log_in(self):
    if self.openai_key != "":
      try:
        openai.api_key = self.openai_key
      except:
        ValueError("Invalid OpenAI API key")
    else:
      ValueError("No OpenAI API key")

  def initialize_models(self):
    if self.summarizer_model != None:
      try:
        self.summarizer = pipeline("summarization", model=self.summarizer_model, tokenizer=self.summarizer_model, device=0)
      except:
        ValueError("Invalid summarizer model")

'''

import datetime
from transformers import pipeline
import datetime
import os
import openai


class NLP_opeanai:
    def __init__(self, name, openaikey):
        self.name = name
        self._log_in(openaikey)
    
    def _log_in(self, openai_key):
        try:
          openai.api_key = openai_key
        except:
          ValueError("Invalid OpenAI API key")
    
    def _get_response(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")
    
    def summarize(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        prompt = f"Summarize this: {prompt}"
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")

    def generate_text(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        prompt = f"Continue writing this: {prompt}"
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")

    def answer_question(self, prompt = 'Hello', temperature = 0.9, max_tokens = 300, top_p = 1, frequency_penalty = 0.0, presence_penalty = 0.6, stop = [" Human:", " AI:"]):
      try:
        response = openai.Completion.create(
          model="text-davinci-003",
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=top_p,
          prompt=prompt,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          stop=stop
        )
        self.total_tokens = response['usage']['total_tokens']
        return response['choices'][0]['text']
      except:
        ValueError("Invalid response")
   

class NLP:
    '''
    This class is the NLP processor
    It uses the transformers library to process the text
    ---
    Tasks:
        - Summarization        [DONE]
        - Question Answering   [DONE]
        - Text Generation      [DONE]
    '''
    DEFAULT_SUMMARIZER_MODEL = "t5-small"
    DEFAULT_QA_MODEL = "distilbert-base-uncased-distilled-squad"
    DEFAULT_TEXT_GENERATION_MODEL = "gpt2"

    def __init__(self, openAI_KEY = None, summarizer_model = None, qa_model = None, text_generation_model = None):
        '''
        This class initialise the transformers pipeline.
        Tasks:
            - summarization
            - question answering
            - text generation
        '''
        print(f"Initalizing NLP_Processor class")
        self.openAI_KEY = openAI_KEY
        start = datetime.datetime.now()
        # print("NLP class: Creating instance")
        if summarizer_model != None:
          try:
            self.summarizer = pipeline("summarization", model=summarizer_model, tokenizer=summarizer_model)
          except:
            summarizer_model = self.DEFAULT_SUMMARIZER_MODEL
            self.summarizer = pipeline("summarization", model=summarizer_model, tokenizer=summarizer_model)
        else:
          summarizer_model = self.DEFAULT_SUMMARIZER_MODEL
          self.summarizer = pipeline("summarization", model=summarizer_model, tokenizer=summarizer_model)

        if qa_model != None:
          try:
            self.qa = pipeline("question-answering", model=qa_model, tokenizer=qa_model)
          except:
            qa_model = self.DEFAULT_QA_MODEL
            self.qa = pipeline("question-answering", model=qa_model, tokenizer=qa_model)

        else:
          qa_model = self.DEFAULT_QA_MODEL
          self.qa = pipeline("question-answering", model=qa_model, tokenizer=qa_model)

        if text_generation_model != None:
          try:
            self.text_generator = pipeline("text-generation", model=text_generation_model, tokenizer=text_generation_model)
          except:
            text_generation_model = self.DEFAULT_TEXT_GENERATION_MODEL
            self.text_generator = pipeline("text-generation", model=text_generation_model, tokenizer=text_generation_model)
        else:
          text_generation_model = self.DEFAULT_TEXT_GENERATION_MODEL
          self.text_generator = pipeline("text-generation", model=text_generation_model, tokenizer=text_generation_model)

        end = datetime.datetime.now()
        time = (end - start).total_seconds()
        print(f"Initialization NLP_Processor completed: {time} seconds")

    def summarize(self, prompt, max_length=100, min_length=30, delete_prompt=True): # works
        '''
        ---
        param: 
            prompt: string
            max_length: int
            min_length: int
            delete_prompt: bool
        return:
            summary: string
        ---
        This function is used to summarize the text it uses the summarization pipeline from transformers
        It's only used to summarize the text, you can set the default model in the `__init__` function.
        For now it is initialised to the 'summarization' pipeline that huggingface provides by default.
        ---
        '''
        print("Generating summary") 
        
        # delete last word from prompt
        last_word = prompt.split()[-1]
        prompt = prompt.replace(last_word, "")
        summary = self.summarizer(prompt, max_length=max_length, min_length=min_length, truncation=True)
        summary = summary[0]['summary_text']
        return summary
    
    def generate_text(self, prompt, num = 100): # works
        '''
        ---
        param:
            prompt: string
            num: int (number of words to generate)
        return:
            generated: string (generated text)
        ---
        This function is used to generate text, it uses the text-generation pipeline from transformers.
        It's only used to generate text, you can set the default model in the `__init__` function.
        For now it is initialised to the 'text-generation' pipeline that huggingface provides by default.
        '''
        print(f"Generating {num} words")
        len_prompt = len(prompt.split())
        last_word = prompt.split()[-1]
        # delete last word from prompt
        prompt = prompt.replace(last_word, "")
        # generate text
        generated = self.text_generator(prompt, max_length=len_prompt+num, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1)
        generated = generated[0]['generated_text']
        return generated

    def answer_question(self, prompt, question):
        '''
        ---
        param:
            prompt: string
            question: string
        return:
            answer: string
        ---
        This function is used to answer questions, it uses the question-answering pipeline from transformers.
        It's only used to answer questions, you can set the default model in the `__init__` function.
        For now it is initialised to the 'question-answering' pipeline that huggingface provides by default.
        '''
        print("Answering question")
        answer = self.qa(prompt, question)
        answer = answer['answer']
        return answer


if __name__  == "__main__":
    # initialise the class
    nlp = NLP()
    # generate text
    generated = nlp.generate_text("Hello, how are you doing today?")
    print(f"Generated: {generated}")

    # summarize text
    summary = nlp.summarize(generated)
    print(f"Summary: {summary}")

    answer = nlp.answer_question(generated, "How are you doing today?")
    print(f"Answer: {answer}")
