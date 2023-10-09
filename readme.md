## Setup
### On Mac:
```
virtualenv env_main -p python3
source env_main/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### On Windows:
```
virtualenv env_main -p python3
env_main\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### To run the app:
```
python main.py 
```

1. Open the settings and link a folder to the app as Vault.
2. Press CMD + N to create a new file.
3. Write what you want.
4. Press CMD + S to save the file.

---
## Dependencies
Still need to take off the ones that are not used. Still in development.
```
pandas 
numpy
networkx 
matplotlib
scipy
torch
transformers
nltk
requests
bs4
wcpython
```
# TextEditor
With this editor open source you can scrape data from the web, you can summarize and paraphrase text.

- Command + S: Save
-  Command + A: Summarise
- Command + O: Open-file
- Command + N: New-file
- Command + Q: Exit
- Command + W: Wiki-search
- Command + U: Url search
- Command + G: Generate text
- Command + ;: Open the emoji panel_mains

Features:
---
    SCRAPING                                             [4/4]
    - Scrape text from wikipedia                         [DONE]
        - Select the chapter                             [DONE]
    - Scrape text from a url                             [DONE]
        - Select the chapter                             [DONE]
    - Read csv from a url                                [DONE]

    NATURAL LANGUAGE PROCESSING                          [1/3]
    - Summarize text                                     [DONE] # Deafult model - sufficent
    - Generate text -    Paraphrase text                 [DONE] # Default model - absolute garbage
    - Question Answering                                 [NOT DONE]

    DATA MANAGMENT                                       [3/4]
    - Connect to a folder and save the data as md files. [DONE]
    - config file for default settings                   [DONE]
    - Custom Folder for Vault                            [DONE]
    - Set custom models from HuggingFace                 [DONE] 

    EDITOR                                               [5/8]
    - Open a file                                        [DONE]
    - Save a file                                        [DONE]
    - Delete Note                                        [DONE]
    - Add Note                                           [DONE]
    - Edit Note                                          [DONE]
    - MD file Editor                                     [DONE]
    - Emojis picker                                      [DONE]
    - Plot the data                                      [NOT DONE] 
    - Search Note                                        [NOT DONE]


    ANALYSIS                                             [3/5]
    - Highlight words from analysis                      [DONE]
    - Last word                                          [DONE]
    - Word Count                                         [DONE]
    - Most common words                                  [DONE]
    - Connections Plot NX                                [NOT DONE]


    ---------------------------------------------------------------
    Total: 20/30    
    ---------------------------------------------------------------
---

### Notes
Issues:
---
- Even when text is selected, the wiki scraper will work taking the last word of the text. [FIXED]
- Delete Note Button is not working.                                                       [FIXED]
---
It might need a tokenizer feature to save space in memory.
---

Complications:
---

Questions:
- It's possible to deploy a model in HuggingFace and then use it in the TextEditor? 
   - Technically yes, I should be able to set the model weights to the values that I want.
    - I would need to find a way to save the model weights in a file and then load it in the TextEditor.
- It's problematic to think about a system like this that automatically fine tuned with the data.

---
Ideas: 

I want to create a graph that represent the connections between the words and the notes in the text.

- The nodes will be the words.
- The edges will be the notes.
- The weight of the edges will be the number of times that the word appears in the note.

Need to set a title to every note.
- I want elasticity, I don't want to have to set the title manually.
- It will be assign automatically, but I want to be able to change it.
- Hierarchy of the text. Set title base on the hierarchy of the text tags -> h1, h2, h3, h4, h5, h6, p.
- Title can be obtained from:
    - QA Model -> Question: What is this text about? Answer: "George Washington"
    - Counting most common words ? bad approach

ISSUES:

When changing the model we loose the home_dir variable.
