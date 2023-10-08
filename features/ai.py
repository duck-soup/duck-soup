import os
import openai

class NLP:
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
   
if __name__ == "__main__":
    # test all methods
    nlp = NLP('duck-soup', '__INSERT_YOUR_OPENAI_API_KEY_HERE__')
    prompt = "The quick brown fox jumps over the lazy red dog. The dog is red."
    summary = nlp.summarize(prompt)
    generated = nlp.generate_text(prompt)
    question = prompt + " # What is the color of the dog?"
    answer = nlp.answer_question(question)

    print('------------------')
    print('This is the summary: ')
    print('')
    print(summary)
    print('------------------')
    print('This is the generated text: ')
    print('')
    print(generated)
    print('------------------')
    print(f'This is the answer: {answer} to the question: {question}')
    print('')
    print(answer)
    print('------------------')


