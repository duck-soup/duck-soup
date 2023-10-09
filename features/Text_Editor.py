
from ai import NLP_opeanai as NLP
from silver_scraper import Silver_Scraper

import tkinter as tk
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

class TextEditor:
    def __init__(self, root):
        '''
        ---
        param: root (tkinter root)
        return: None
        --- 
        Initialize the text editor with a text area.
        Initialize the NLP processor to read and process the text.
        '''
        self.root = root
        # size
        self.text_entry = tk.Text(root, height=40, width=150)
        # position
        self.text_entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5) 
        # style
        self.text_entry.config(highlightthickness=0,
                bd=0,
                    width=100, height=40,font=("Arial", 12),
                    # get backgroung color of the window
                    selectbackground='#e8e8e8',
                    highlightbackground='#e8e8e8',
                    highlightcolor='#e8e8e8',
                    selectborderwidth=0,
                    # round border
                    borderwidth=5,
                    relief="groove",
                    wrap="word",
        )
        
        # initialize the NLP processor
        self.NLP_Processor = NLP(name="2", openaikey='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')
        self.binds()

# ----------------------------- HELPERS -------------------------
    def get_text(self):
        '''
        ---
        param: None
        return: text (string)
        ---
        This function gets the text from the text entry and returns it as a string
        '''
        text = self.text_entry.get("1.0", "end-1c")
        return text
    
# ---------------------------- BINDS ----------------------------
    def interpreter(self, event):
        self.prompt = self.get_text()
        self.last_word = self.prompt.split()[-1]
        # 1. TEXT GENERATION
        if self.last_word == "/gen": # works
            generated_text = self.NLP_Processor.generate_text(self.prompt)
            # add text to the text entry
            self.text_entry.insert(tk.END, generated_text)
            print("Generated text")
        
        # 2. SUMMARIZATION
        elif self.last_word == "/summary": # works
            summary = self.NLP_Processor.summarize(self.prompt)
            # add text to the text entry
            self.text_entry.insert(tk.END, summary)
            print("Summarized text")
       
        # 3. QUESTION ANSWERING
        elif self.last_word[:3] == "/qa": # works
            question_entry = tk.Entry(self.root, width=100)
            question_entry.grid(row=1, column=0, columnspan=4)
            question_entry.focus()
            # if enter is pressed
            def get_answer(event):
                # get the question
                question = question_entry.get()
                # get the answer
                answer = self.NLP_Processor.answer_question(self.prompt, question)
                # add text to the text entry
                self.text_entry.insert(tk.END, answer)
                print("Answered question")
            # bind the get_answer function to the enter key
            question_entry.bind("<Return>", get_answer)

        # 4. WIKIPEDIA scraping
        elif self.last_word[:6] == "/wiki-": # works
            # get the url
            wiki_word = self.last_word[6:]
            url = 'https://en.wikipedia.org/wiki/' + wiki_word
            # get the text and the chapters from url
            Scraper = Silver_Scraper(url) # create a scraper object
            text, chapters = Scraper.get_wiki_text()
            # add text to textarea
            self.text_entry.insert(tk.END, text)
            # add chapters to listbox inside textarea

            listbox = tk.Listbox(self.root, height=10, width=20)
            listbox.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)
            for chapter in chapters:
                listbox.insert(tk.END, chapter)

            color = self.text_entry.cget("background")
            listbox.config(background=color)
            # create button to delete listbox
            def delete_listbox(event):
                listbox.destroy()
                delete_button.destroy()
            delete_button = tk.Button(self.root, text="Hide", command=lambda: delete_listbox(event))
            delete_button.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)
            
            # if chapter is selected
            def select_chapter(event):
                # get selected chapter
                chapter = listbox.get(listbox.curselection())
                # get text from wikipedia
                text, chapters = Scraper.get_wiki_text(chapter)
                # replace the / with a space
                text = text.replace("/", " ")
                # delete textarea
                self.text_entry.delete(1.0, tk.END)
                # insert generated text
                self.text_entry.insert(tk.END, text)
                # destroy window
            
            # bind event to listbox if double clicked
            listbox.bind("<<ListboxSelect>>", select_chapter)
        
        # 5. URL scraping
        elif self.last_word[:5] == "/url-":
            # get the url
            url = self.last_word[5:]
            # get the text and the chapters from url
            Scraper = Silver_Scraper(url)
            text, chapters = Scraper.scraping_url()
            # same as above
            self.text_entry.insert(tk.END, text)
            # add chapters to listbox inside textarea
            # same as above
            listbox = tk.Listbox(self.root, height=10, width=5)
            listbox.grid(row=0, column=5, sticky="nsew", padx=5, pady=5)
            for chapter in chapters:
                listbox.insert(tk.END, chapter)
                
            color = self.text_entry.cget("background")
            listbox.config(background=color)
            # create button to delete listbox
            # same as above
            def delete_listbox(event):
                listbox.destroy()
                delete_button.destroy()
            delete_button = tk.Button(self.root, text="Hide", command=lambda: delete_listbox(event))
            delete_button.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)

            # if chapter is selected
            # same as above
            def select_chapter(event):
                # get selected chapter
                chapter = listbox.get(listbox.curselection())
                # get text from wikipedia
                text, chapters = Scraper.get_text_from_url(chapter)
                # replace the / with a space
                text = text.replace("/", " ")
                # delete textarea
                self.text_entry.delete(1.0, tk.END)
                # insert generated text
                self.text_entry.insert(tk.END, text)
                # destroy window

            # bind event to listbox if double clicked
            listbox.bind("<<ListboxSelect>>", select_chapter)

        else:
            print('No generate command found')
        return None

    def summary_highlighted_text(self, event, text_area = None):
        '''
        This function is called when the user presses command + s
        It creates a summary of the highlighted text and replaces it with the summary
        '''
        if not text_area:
            print("Generating summary") 
            self.prompt = self.text_entry.selection_get()         # get selected text
            summary = self.NLP_Processor.summarize(self.prompt)        # create summary
            # put instead of selected text
            self.text_entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_entry.insert(tk.INSERT, summary)   
        else:
            print("Generating summary") 
            prompt = text_area.selection_get()
            summary = self.NLP_Processor.summarize(prompt)
            print(summary)
            text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
            text_area.insert(tk.INSERT, summary)
            print("Summary generated")
        return None 

    def wiki_highlighted_text(self, event):
        '''
        This function is called when the user presses command + s
        It creates a summary of the highlighted text and replaces it with the summary
        '''
        print("Looking up on Wikipedia")
        self.prompt = self.text_entry.selection_get()         # get selected text
        url = 'https://en.wikipedia.org/wiki/' + self.prompt
        # get the text and the chapters from url
        Scraper = Silver_Scraper(url) # create a scraper object
        text, chapters = Scraper.get_wiki_text()
        # open a new window
        new_window = tk.Toplevel(self.root)

        new_window.title(f"{self.prompt} - Wikipedia")
        # geometry
        new_window.geometry("800x600")
        # add text to textarea
        text_entry = tk.Text(new_window, height=50, width=150)
        text_entry.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
        text_entry.insert(tk.END, text)
        # add chapters to listbox inside textarea

        listbox = tk.Listbox(new_window, height=10, width=20)
        listbox.grid(row=0, column=6, sticky="nsew", padx=5, pady=5)
        for chapter in chapters:
            listbox.insert(tk.END, chapter)

        color = self.text_entry.cget("background")
        listbox.config(background=color)
        # create button to delete listbox
        def delete_listbox(event):
            listbox.destroy()
            delete_button.destroy()
        delete_button = tk.Button(self.root, text="Hide", command=lambda: delete_listbox(event))
        delete_button.grid(row=1, column=5, sticky="nsew", padx=5, pady=5)
        
        # if chapter is selected
        def select_chapter(event):
            # get selected chapter
            chapter = listbox.get(listbox.curselection())
            # get text from wikipedia
            text, chapters = Scraper.get_wiki_text(chapter)
            # replace the / with a space
            text = text.replace("/", " ")
            # delete textarea
            text_entry.delete(1.0, tk.END)
            # insert generated text
            text_entry.insert(tk.END, text)
            # destroy window
        # add button to append note to the end of the text
        def add_note():
            # get note fro main window
            note = text_entry.get(1.0, tk.END)
            # add note to the end of the text
            self.text_entry.insert(tk.END, note)
        # create button
        add_note_button = tk.Button(new_window, text="Add note", command=add_note)
        add_note_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # bind event to listbox if double clicked
        listbox.bind("<<ListboxSelect>>", select_chapter)

        # bind command + s to summary_highlighted_text
        new_window.bind("<Command-s>", self.summary_highlighted_text(event, text_area=text_entry))
        # bind command + w to wiki_highlighted_text
        new_window.bind("<Control-w>", self.wiki_highlighted_text(event))

    def is_command(self, event): # works
        '''
        This function is called every time a new character is inserted in the text area
        It handles the styling of the text if it is a command
        '''
        # check if '/' is in text
        prompt = self.get_text()
        if '/' in prompt:
            print("Command found")
            # get index of '/'
            index = prompt.index('/')
            # change the color of the text until the end
            self.text_entry.tag_add("command", "1.0 + " + str(index) + "c", "end")
            self.text_entry.tag_config("command", foreground="grey")
            # make it bold
            self.text_entry.tag_add("bold", "1.0 + " + str(index) + "c", "end")
            self.text_entry.tag_config("bold", font="bold")
            # make it bigger
            self.text_entry.tag_add("big", "1.0 + " + str(index) + "c", "end")
            self.text_entry.tag_config("big", font=("Helvetica", 20))
        else:
            #print("No command found")
            self.text_entry.tag_delete("command")
            self.text_entry.tag_delete("bold")
            self.text_entry.tag_delete("big")

        text = self.get_text()

        # analyze the text
        def analyze_text():
            no_words = stopwords.words("english")
            from collections import Counter
            # 1.  Process the text
            words = text.split() # split the text into words
            words = [word.strip(".,!?:;") for word in words] # strip the words from the symbols
            words = [word for word in words if word not in no_words]  # take out the no words
            # 2. Show total n of words
            length_w = len(words) # get the length of the words
            word_count_label = tk.Label(self.root, text=f"Word count: {length_w}")
            word_count_label.grid(row=2, column=0)
            # 3. Get the most common words
            word_count = Counter(words)
            most_common_words = word_count.most_common(5) # get the 5 most common words
            # create a  list box to show the most common words
            listbox = tk.Listbox(self.root, height=5, width=20)
            listbox.grid(row=0, column=6, sticky="nsew", padx=5, pady=5)
            for word in most_common_words:
                listbox.insert(tk.END, word)

            # when selected, show the word in the text area
            def select_word(event):
                # set styling of the word to default
                self.text_entry.tag_delete("highlight")
                # get selected word
                word = listbox.get(listbox.curselection())
                word = word[0]
                print(word)
                #1. get all the indexes of the word
                indexes = [i for i, x in enumerate(words) if x == word]
                # highlight the word for all the indexes
                starting_index = "1.0"
                for index in indexes:
                    starting_index = self.text_entry.search(word, starting_index, stopindex=tk.END)
                    ending_index = starting_index + f"+{len(word)}c"
                    self.text_entry.tag_add("highlight", starting_index, ending_index)
                    self.text_entry.tag_config("highlight", background="yellow")
                    starting_index = ending_index

            # bind event to listbox if double clicked
            listbox.bind("<<ListboxSelect>>", select_word)

            # button to hide the listbox
            def delete_listbox(event):
                # delete all listbox
                listbox.destroy()
                # delete button
                delete_button.destroy()

            delete_button = tk.Button(self.root, text="Hide", command=lambda: delete_listbox(event))
            delete_button.grid(row=1, column=6, sticky="nsew", padx=5, pady=5)


        analyze_text()
# ---------------------------------------------------------------
    def binds(self):
        '''
        parameters: None
        ---
        This function binds the functions to the keys
        ---
        1. bind the is_command function to the text entry
        2. bind the generate_text function to the enter key
        3. bind the summary_highlighted_text function to command + s
        4. bind the wiki_search function to control + w

        '''
        # bind the is_command function to the text entry
        self.text_entry.bind("<KeyRelease>", self.is_command)
        # bind the generate_text function to the enter key
        self.text_entry.bind("<Return>", self.interpreter)
        # bind the summary_highlighted_text function to command + s
        self.text_entry.bind("<Command-s>", self.summary_highlighted_text)
        # bind the wiki_search function to control + w 
        self.text_entry.bind("<Control-w>", self.wiki_highlighted_text)

if __name__ == "__main__":
    root = tk.Tk()
    text_ = TextEditor(root)
    root.mainloop()