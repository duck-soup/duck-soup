import os
import wx
import wx.html2
import yaml
import markdown
import networkx as nx
from features.ai import NLP_opeanai
from features.silver_scraper import Silver_Scraper
from collections import Counter
from utils import get_random_title, css_table, css_table_
from elements.graph_panel import GraphPanel
from markdown_checklist.extension import ChecklistExtension

class DuckSoupApp(wx.Frame):
    def __init__(self, parent, title):
        self.size = wx.DisplaySize()
        self.size = (int(self.size[0]*0.8), int(self.size[1]*0.8))
        super().__init__(parent, title=title, size=(self.size[0], self.size[1]))
        self.emojis = ['🍇', '🍈', '🍉', '🍊', '🍋', '🍌', '🍍', '🥭', '🍎', '🍏', '🍐', '🍑', '🍒', '🍓', '🫐', '🥝', '🍅', '🫒', '🥥', '🥑', '🍆', '🥔', '🥕', '🌽', '🌶️', '🫑', '🥒', '🥬', '🥦', '🧄', '🧅', '🍄', '🥜', '🫘', '🌰', '🍞', '🥐', '🥖', '🫓', '🥨', '🥯', '🥞', '🧇', '🧀', '🍖', '🍗', '🥩', '🥓', '🍔', '🍟', '🍕', '🌭', '🥪', '🌮', '🌯', '🫔', '🥙', '🧆', '🥚', '🍳', '🥘', '🍲', '🫕', '🥣', '🥗', '🍿', '🧈', '🧂', '🥫', '🍱', '🍘', '🍙', '🍚', '🍛', '🍜', '🍝', '🍠', '🍢', '🍣', '🍤', '🍥', '🥮', '🍡', '🥟', '🥠', '🥡', '🦪', '🍦', '🍧', '🍨', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬', '🍭', '🍮', '🍯', '🍼', '🥛', '☕', '🫖', '🍵', '🍶', '🍾', '🍷', '🍸', '🍹', '🍺', '🍻', '🥂', '🥃', '🫗', '🥤', '🧋', '🧃', '🧉', '🧊', '🥢', '🍽️', '🍴', '🥄', '🫙']
        self.InitUI()
        self.Show()

    def get_last_word(self, text):
        '''
        ---
        param:
            text: string
        return:
            last_word: string
        ---
        This function returns the last word of a string of text.
        '''
        words = text.split()
        if words:
            return words[-1]
        return ''
    
    def get_text(self):
        '''
        ---
        return:
            text: string
        ---
        This function returns the text in the text control. (text_ctrl) 
        The main text control of the app using for writing and editing notes.
        ---
        '''
        return self.text_ctrl.GetValue()

    def get_counter_dict(self):
        '''
        ---
        return:
            counter: dict (key: word, value: number of times the word appears)
        ---
        This function returns a dictionary with the unique words  and their counts values in the text control.
        It uses the Counter class from the collections module. It is imported at the top of the file.
        '''
        # count the number of times each word appears
        words = self.get_text().split()
        counter = Counter(words)
        return counter

    def configurations(self):
        '''
        This function reads the config.txt file and set the home directory.

        The config.txt file should have the following format:
        ```
        home_dir = 'path/to/home/directory' # the one that you want to use as Vault to keep your notes
        ```
        ---
        In the next step it will be used to set the defaults modes for the AI models.
        It uses the open-source library transformers from huggingface to power the AI models.

        `summarizer = 'summarization'`

        `qa         = 'question-answering'`

        `text_generation = 'text-generation'`

        ---        
        TODO:
        
        - Summarization      [To be implemented] 
        - Question-Answering [To be implemented]
        - Text-Generation    [To be implemented]

        - Change the Theme of the app

        '''
        try:
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            # create a new config file with default values
            config = {
                'home_dir': '',
                'list_file_background_color': 'white',
                'list_file_foreground_color': 'black',
                'list_words_background_color': 'white',
                'list_words_foreground_color': 'black',
                'openai_key': '',
                'panel_background_color': 'white',
                'qa_model': 'OpenAI',
                'summarizer_model': 'OpenAI',
                'text_ctrl_1_background_color': 'white',
                'text_ctrl_1_foreground_color': 'black',
                'text_ctrl_background_color': 'white',
                'text_ctrl_foreground_color': 'black',
                'text_generation_model': 'OpenAI',
                'text_summary_background_color': 'white',
                'text_summary_foreground_color': 'black',


            }
            with open('config.yaml', 'w') as f:
                yaml.dump(config, f)
            
        self.home_dir = config['home_dir']
        self.summarizer_model = config['summarizer_model']
        self.qa_model = config['qa_model']
        self.text_generation_model = config['text_generation_model']
        self.openai_key = config['openai_key']

        # if openai_key is not set, then use the default one
        if self.openai_key != '' and self.summarizer_model == 'OpenAI' and self.qa_model == 'OpenAI' and self.text_generation_model == 'OpenAI':
            self.nlp = NLP_opeanai('Gianni',self.openai_key)
        else:
            #self.nlp = NLP()
            pass

    def get_files_from_archive(self):
        '''
        ---
        return:
            files: list (list of files in the home directory)
        ---
        This function returns a list of files in the home directory.
        The home directory is the one that you want to use as Vault to keep your notes.
        - it is initialized in the self.configurations() function.
        - the default value is store in the "config.txt" file, under the "home_dir" variable.
        ---
        '''
        self.configurations()
        files = []
        for file in os.listdir(self.home_dir):
            if file.endswith('.txt'):
                files.append(file)

        self.files = files
        return files
    
    def check_first_icon(self):
        # check if the first word is a emoji
        text = self.get_text()
        if len(text.strip()) == 0:
            return False
        first_word = text.split()[0]
        if first_word in self.emojis:
            self.text_ctrl.SetStyle(0, len(first_word)+1, wx.TextAttr(wx.NullColour, wx.NullColour, wx.Font(75, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_EXTRAHEAVY)))
            return True
        else:
            self.text_ctrl.SetStyle(0, len(first_word)+1, wx.TextAttr(wx.NullColour, wx.NullColour, wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)))
            return False
    
    def check_network(self):
        '''
        This function checks if we want to show a graph
        '''
       # get all text from the text control
        text = self.get_text()
        print('Looking for a LIST OF EDGES')
        start = None
        end = None
        connect = False
        connect_ = False
        for i, line in enumerate(str(text).splitlines()): 
            if "<connect" in line:
                start = i+1
                connect = True
            elif "connect>" in line:
                end = i
                connect_ = True
        self.start_idx_edges = start
        self.end_idx_edges = end
        if connect and connect_:
            return True
        else:
            return False

    def get_list_of_edges(self):
        # get all text from the text control
        text = self.get_text()
        # now using self.start_idx_edges and self.end_idx_edges we can get the list of edges
        list_of_edges = []
        for i, line in enumerate(str(text).splitlines()):
            if i >= self.start_idx_edges and i < self.end_idx_edges:
                list_of_edges.append(line)
        # clean the list of edges
        # ['(o,i)', '(i,o)'] -> [('o','i'), ('i','o')]
        list_of_edges = [tuple(edge.replace('(','').replace(')','').replace(' ','').split(',')) for edge in list_of_edges]
        return list_of_edges
    
    # --------------------BINDINGS--------------------

    def OnTextChange(self, event):                      # When the user types something in the text control - Analyzes the text
        '''
        This function is called when the user types something in the text control.
        It will be used to do some of the Analysis of the text.
        All the Analysis would be display in the Stats panel_main.

        - Last word          [DONE] 
        - Number of words    [DONE] 
        - Counter            [DONE] (word, count, percentage)
        - Checking if the first word is an emoji to change the font size
        ---
        Since it's been called every time the user types something, it's not a good idea to do heavy computations here.
        - Count the number of words [DONE]

        ---
        '''
        ######################### This part is for the graph
        is_there_an_icon_page = self.check_first_icon()
        is_there_a_network = self.check_network()
        if is_there_a_network:
            list_of_edges = self.get_list_of_edges()
            # get unique nodes
            nodes = list(set([node for edge in list_of_edges for node in edge]))

            # create a new window
            self.new_frame = wx.Frame(self.panel_main, -1, 'Network', size=(800, 600))
            self.graph = nx.DiGraph()
            self.graph.add_nodes_from(nodes)
            self.graph.add_edges_from(list_of_edges)
            self.panel = GraphPanel(self.new_frame, self.graph)
            # creatge a sizer for the frame
            self.second_sizer = wx.BoxSizer(wx.VERTICAL)
            self.second_sizer.Add(self.panel, 1, wx.EXPAND)
            self.new_frame.SetSizer(self.second_sizer)
            self.new_frame.Layout()
            self.new_frame.Show()


        ###################################################

        text = self.get_text()
        last_word = self.get_last_word(text)
        number_of_word = len(self.get_text().split())

        # counter 
        counter = self.get_counter_dict()
        # sort the counter by the number of times the word appears
        counter = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
        # add value to list
        self.list_words.DeleteAllItems()
        for word, count in counter.items():
            percentage = round(count/number_of_word*100, 2)
            self.list_words.Append([word, count, percentage])
        
        # check if theres a network dont show from <connect> to connect>

        # Check if the first word is an emoji to set the icon of the page
        if is_there_an_icon_page:
            # get value of self.text_ctrl
            html = markdown.markdown(self.text_ctrl.GetValue(), extensions=[ChecklistExtension(), 'tables', 'fenced_code', 'codehilite'])
            first_word = text.split()[0]
            html = html.replace(first_word, f'<span style="font-size: 75px;">{first_word}</span>')
        else:
            html = markdown.markdown(self.text_ctrl.GetValue(), extensions=[ChecklistExtension(), 'tables', 'fenced_code', 'codehilite'])

        if is_there_a_network:
            # remove all the <connect> and </connect>
            html = html.replace('<connect>', '').replace('</connect>', '')
            # remove all the <node> and </node>
            html = html.replace('<node>', '').replace('</node>', '')
            # remove all the <edge> and </edge>
            html = html.replace('<edge>', '').replace('</edge>', '')

        # apply css to the html table and checkbox
        html = html + css_table
        # change stats label to the number of words
        self.button_stats.SetLabel(f'Stats - {number_of_word} words')
        self.browser.SetPage(html, "")

    def detect_shortcuts(self, event):                  # Detects the shortcuts - Every time a key is pressed
        '''
        ---
        This function detects the shortcuts and calls the corresponding functions.
        The function run every time a key is pressed.
        ---
        - Command + S: Save
        - Command + A: Summarise
        - Command + O: Open-file
        - Command + N: New-file
        - Command + Q: Exit
        - Command + W: Wiki-search
        - Command + U: Url search
        - Command + G: Generate text
        - Command + ;: Open the emoji panel_mains

        ---
        '''
        key_code = event.GetKeyCode()
        if key_code == ord("S") and event.CmdDown():
            print("Save - Control + S pressed!")
            self.OnSave(event)
        # if control + s is pressed
        elif key_code == ord("A") and event.CmdDown():
            print("Summarise - Control + A pressed!")
            self.OnSummarise(event)
        # if control + o is pressed
        elif key_code == ord("O") and event.CmdDown():
            print("Open-file - Control + O pressed!")
            self.OnOpen(event)
        # if control + n is pressed
        elif key_code == ord("N") and event.CmdDown():
            print("New-file - Control + N pressed!")
            self.OnNew(event)
        # if control + q is pressed
        elif key_code == ord("Q") and event.CmdDown():
            print("Exit - Control + Q pressed!")
            self.OnExit(event)

        elif key_code == ord("W") and event.CmdDown():
            print("Wikipedia - Control + W pressed!")
            self.OnWikipedia_search(event)

        elif key_code == ord("U") and event.CmdDown():
            self.OnSrapingUrl(event)

        elif key_code == ord("G") and event.CmdDown():
            self.OnGeneratingText(event)
        # add command + ;  for emoji    
        elif key_code == ord(";") and event.CmdDown():
            self.OnEmojify(event)

        # if / is pressed
        elif key_code == ord("/") and event.CmdDown():
            print("Tasks - / pressed!")
            self.OnTasks(event)

        else:
            event.Skip()
    
    # ----------------- Scraping Functions -----------------
    def OnWikipedia_search(self, event):               # When the user press Ctrl + W the Wikipedia search is triggered
        '''
        This function is called when the user clicks on the Wikipedia shortcut button.
        
        '''
        self.old_text = self.get_text()
        # get highlighted text otherwise get the last word
        highlighted_text = self.text_ctrl.GetStringSelection()
        if highlighted_text != '':
            wiki_search_term = highlighted_text
        else:
            wiki_search_term = self.get_last_word(self.old_text)
        print('wiki_search')
        url = f"https://en.wikipedia.org/wiki/{wiki_search_term}"
        self.scraper = Silver_Scraper(url)
        text, chapters, links = self.scraper.get_wiki_text("History")

        self.text_ctrl.SetValue(self.old_text + text)
        size = self.text_ctrl.GetSize()
        w, h = size
        # create a new window for the chapters
        self.window_chapter = wx.Frame(self, -1, 'Chapters', size=(200, 600))
        self.list_ctrl = wx.ListCtrl(self.window_chapter, -1, style=wx.LC_REPORT, size=(w//2, h), pos=(w-200, 0))
        self.list_ctrl.InsertColumn(0, 'Chapters', width=200)
        for i, chapter in enumerate(chapters):
            self.list_ctrl.InsertItem(i, chapter)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect_chapter)
        self.window_chapter.Show()
        
    def OnSelect_chapter(self, event):
        '''
        This function is called when the user selects a chapter from the H2 list in at the wikipedia page.
        '''
        # get the selected chapter
        chapter = self.list_ctrl.GetItemText(event.GetIndex())
        text, chapters, links = self.scraper.get_wiki_text(chapter)
        self.text_ctrl.SetValue(self.old_text + text)
        print(links)

    def OnSrapingUrl(self, event):                     # When the user press Ctrl + U the Url Scraping is triggered
        '''
        --- 
        This function is called when the user use the shortcut Ctrl + U.
        '''
        self.old_text = self.get_text()
        # get highlighted text otherwise get the last word
        highlighted_text = self.text_ctrl.GetStringSelection()
        
        if highlighted_text != '':
            url_ = highlighted_text

            print('Url Scraping')
            self.scraper = Silver_Scraper(url_)
            text, chapters = self.scraper.get_wiki_text("History")
            self.text_ctrl.SetValue(self.old_text + text)
            size = self.text_ctrl.GetSize()
            w, h = size
            # create a new window for the chapters
            self.window_chapter = wx.Frame(self, -1, 'Chapters', size=(200, 600))
            self.list_ctrl = wx.ListCtrl(self.window_chapter, -1, style=wx.LC_REPORT, size=(w//2, h), pos=(w-200, 0))
            self.list_ctrl.InsertColumn(0, 'Chapters', width=200)
            for i, chapter in enumerate(chapters):
                self.list_ctrl.InsertItem(i, chapter)
            self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect_chapter_url)
            self.window_chapter.Show()
        else:
            print('No Url')

    def OnSelect_chapter_url(self, event):
        '''
        This function is called when the user selects a chapter from the H2 list in at the wikipedia page.
        '''
        # get the selected chapter
        chapter = self.list_ctrl.GetItemText(event.GetIndex())
        text, chapters = self.scraper.get_wiki_text(chapter)
        self.text_ctrl.SetValue(self.old_text + text)

    # ----------------- Document Management Functions -----------------
    def OnNew(self, event):                     # When the user clicks on the NEW-BUTTON or presses Ctrl+N
        # create a new text file in the self.dirname directory
        # get all files in the directory
        files = os.listdir(self.home_dir)
        emoj, titl = get_random_title(files)
        with open(os.path.join(self.home_dir, titl +  '.txt'), 'w') as f:
            f.write(emoj)
            # add in the new line with the title
            f.write('\n' + f"# {titl}" + '\n')
        self.filename = titl + '.txt'
        self.create_archive(self.panel_main)

    def OnOpen(self, event, filename = None):   # When the user clicks on the OPEN-BUTTON or presses Ctrl+O
        if filename is None:
            self.dirname = ''
            dlg = wx.FileDialog(self, 'Choose a file', self.dirname, '', '*.*', wx.FD_OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'r')
                self.text_ctrl.SetValue(f.read())
                f.close()
            dlg.Destroy()
        else:
            self.filename = filename
            with open(filename, 'r') as f:
                self.text_ctrl.SetValue(f.read())

    def OnSave(self, event):                    # When the user clicks on the SAVE BUTTON or presses Ctrl+S
        try:
            print('Saving file')
            text = self.text_ctrl.GetValue()
            print(text)
            # join the directory name and the file name
            self.filename = os.path.join(self.home_dir, self.filename)
            with open(self.filename, 'w') as f:
                f.write(text)
        except:
            print('Saving file as')
            self.OnSaveAs(event)

    def OnSaveAs(self, event):                  # When the user clicks on the SAVE_AS BUTTON or presses Ctrl+Shift+S
        self.dirname = ''
        dlg = wx.FileDialog(self, 'Choose a file', self.dirname, '', '*.*', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.text_ctrl.GetValue())
            f.close()
        dlg.Destroy()

    def OnExit(self, event):                    # When the user clicks on the EXIT BUTTON or presses Ctrl+Q
        self.Close(True)
    # ----------------- Text Manipulation Functions -----------------
    def OnEmojify(self, event):                 # When the user clicks on the EMOJIFY BUTTON or presses Ctrl+E
        print("Emojify - Control + ; pressed!")
        dlg = wx.MultiChoiceDialog(self, 'Select Emojis', 'Emojis', self.emojis)
        if dlg.ShowModal() == wx.ID_OK:
            # get the selected emojis
            selected_emojis = [self.emojis[i] for i in dlg.GetSelections()]
            # append the emojis to the text
            self.text_ctrl.SetValue(self.text_ctrl.GetValue() + ' '.join(selected_emojis))
    # ----------------- NLP Functions -----------------
    def OnSummarise(self, event):               # When the user clicks on the SUMMARISE BUTTON or presses Ctrl+A
        print("Summarise - Control + A pressed!")
        # get value of highlighted text
        value = self.text_ctrl.GetValue()
        # get the start and end of the selection
        start, end = self.text_ctrl.GetSelection()
        # get the selected text
        selected_text = value[start:end]
        # if there is no selected text, summarise the whole text
        if selected_text == '':
            summary = self.nlp.summarize(value)
        else:
            summary = self.nlp.summarize(selected_text)
        text =  summary
        self.text_summary.SetValue(text)   
    
    def OnGeneratingText(self, event):          # When the user clicks on the GENERATE TEXT BUTTON or presses Ctrl+G
        print("Generating Text - Control + G pressed!")
        # get value of highlighted text
        value = self.text_ctrl.GetValue()
        # get the start and end of the selection
        start, end = self.text_ctrl.GetSelection()
        # get the selected text
        selected_text = value[start:end]
        # if there is no selected text, summarise the whole text
        if selected_text == '':
            generated_text = self.nlp.generate_text(value)
        else:
            generated_text = self.nlp.generate_text(selected_text)
        text =  generated_text
        self.text_summary.SetValue(text)  

    # ----------------- Settings -------------------------------------
    def OnSettings(self, event):                # When the user clicks on the SETTINGS BUTTON or presses Ctrl+Shift+S
        '''
        This function opens a new window with the settings.
        ---
        The settings are:
        - Summariser          -> not implemented yet    - it will allow to choose the summariser model    
        - Question Answering  -> not implemented yet    - it will allow to choose the qa model
        - Text Generation     -> not implemented yet    - it will allow to choose the text_generation model
        - Home Directory      -> this is the directory where the notes are saved

        it would be possible to use different model for different subtasks as we know.

        ---
        This all method needs to be written in a different way.
        We are going to implement a list of sections:
        '''

        # Define the options for the AI models
        option_summariser       = ["t5-small", "facebook/bart-large-cnn","OpenAI"]
        option_qa               = ["distilbert-base-uncased-distilled-squad", "bert-large-uncased-whole-word-masking-finetuned-squad", 'OpenAI']
        option_text_generation  = ['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl', 'OpenAI']
        
        # Create the main window and the sizer to divide it into two sections
        self.window_settings = wx.Frame(None, title='Settings', size=(self.size[0]//1, self.size[1]//1))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.window_settings.SetSizer(self.sizer)
        
        # Add a panel to the left section for the buttons
        self.panel_buttons = wx.Panel(self.window_settings)
        self.sizer.Add(self.panel_buttons, 0, wx.EXPAND | wx.ALL, 10)
        self.sizer.AddSpacer(20) # Add some space between the panels
        self.panel_settings = wx.Panel(self.window_settings)
        self.sizer.Add(self.panel_settings, 1, wx.EXPAND | wx.ALL, 10)
        
        # Add the buttons to the left panel
        self.BUTTON_AI_SETTINGS = wx.Button(self.panel_buttons, label='AI Settings', pos=(10, 20))
        self.BUTTON_VAULT_SETTINGS = wx.Button(self.panel_buttons, label='Vault Settings', pos=(10, 50))    
        
        # Add the settings to the right panel
        self.label_openai_key = wx.StaticText(self.panel_settings, label='OpenAI Key', pos=(10, 20))
        self.text_openai_key = wx.TextCtrl(self.panel_settings, pos=(10, 50), size=(200, 20))
        self.label_summariser = wx.StaticText(self.panel_settings, label='Summariser', pos=(10, 80))
        self.choice_summariser = wx.Choice(self.panel_settings, choices=option_summariser, pos=(10, 100), size=(200, 20))
        self.choice_summariser.Bind(wx.EVT_CHOICE, self.OnChoice_Summariser)
        self.label_qa = wx.StaticText(self.panel_settings, label='Question Answering', pos=(10, 150), size=(200, 20))
        self.choice_qa = wx.Choice(self.panel_settings, choices=option_qa, pos=(10, 180), size=(200, 20))
        self.choice_qa.Bind(wx.EVT_CHOICE, self.OnChoice_QA)
        self.label_text_generation = wx.StaticText(self.panel_settings, label='Text Generation', pos=(10, 230), size=(200, 20))
        self.choice_text_generation = wx.Choice(self.panel_settings, choices=option_text_generation, pos=(10, 260), size=(200, 20))
        self.choice_text_generation.Bind(wx.EVT_CHOICE, self.OnChoice_TextGeneration)

        # get values from config.yaml
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        try:
            self.text_openai_key.SetValue(config['openai_key'])
        except:
            pass
        self.choice_summariser.SetStringSelection(config['summarizer_model'])
        self.choice_qa.SetStringSelection(config['qa_model'])
        self.choice_text_generation.SetStringSelection(config['text_generation_model'])

        self.dirname = ''
        self.button = wx.Button(self.panel_settings, label='Choose Home Directory', pos=(10, 350), size=(200, 20))
        self.button.Bind(wx.EVT_BUTTON, self.OnSelectDir)

        # hide them all 
        self.label_openai_key.Hide()
        self.text_openai_key.Hide()
        self.label_summariser.Hide()
        self.choice_summariser.Hide()
        self.label_text_generation.Hide()
        self.choice_text_generation.Hide()
        self.label_qa.Hide()
        self.choice_qa.Hide()
        self.button.Hide()

        # hide all ai settings
        def VAULT_SET(event):
            self.label_openai_key.Hide()
            self.text_openai_key.Hide()
            self.label_summariser.Hide()
            self.choice_summariser.Hide()
            self.label_text_generation.Hide()
            self.choice_text_generation.Hide()
            self.label_qa.Hide()
            self.choice_qa.Hide()
            # show all vault settings
            #self.label_home_dir.Show()
            self.button.Show()

        def AI_SET(event):
            self.label_openai_key.Show()
            self.text_openai_key.Show()
            self.label_summariser.Show()
            self.choice_summariser.Show()
            self.label_text_generation.Show()
            self.choice_text_generation.Show()
            self.label_qa.Show()
            self.choice_qa.Show()
            # hide all vault settings
            self.button.Hide()
        # Bind the buttons to the functions
        self.BUTTON_AI_SETTINGS.Bind(wx.EVT_BUTTON, AI_SET)
        self.BUTTON_VAULT_SETTINGS.Bind(wx.EVT_BUTTON, VAULT_SET)

        self.save_settings = wx.Button(self.panel_buttons, label='Save Settings', pos=(10, 300), size=(200, 20))
        self.save_settings.Bind(wx.EVT_BUTTON, self.OnSaveSettings)
        self.window_settings.Show()

    def OnSaveSettings(self, event):            # When the user clicks on the SAVE SETTINGS button
        print('Saving Settings')
        summariser = self.OnChoice_Summariser(event)
        qa = self.OnChoice_QA(event)
        text_generation = self.OnChoice_TextGeneration(event)
        print('Summariser_model: ', summariser)
        print('Question Answering_Model ', qa)
        print('Text Generation Model: ', text_generation)

        # write on the config file
        # open the config file
        with open('config.yaml', 'r') as f:
            # read the yaml
            yaml_dict = yaml.safe_load(f)

        # update the yaml with new models
        yaml_dict['summarizer_model'] = summariser
        yaml_dict['qa_model'] = qa
        yaml_dict['text_generation_model'] = text_generation

        print('------------')
        print('This would be the new config file:')
        print(yaml.dump(yaml_dict))
        print('------------')

        # delete the old config file
        os.remove('config.yaml')
        # create a new config file
        with open('config.yaml', 'w') as f:
            yaml.dump(yaml_dict, f)
        
        # if all of them are OpenAI
        if summariser == 'OpenAI' and qa == 'OpenAI' and text_generation == 'OpenAI':
            # get the key
            key = self.text_openai_key.GetValue()
            # write the key in the config file
            with open('config.yaml', 'r') as f:
                # read the yaml
                yaml_dict = yaml.safe_load(f)
            # update the yaml with new models
            yaml_dict['openai_key'] = key
            # delete the old config file
            os.remove('config.yaml')
            # create a new config file
            with open('config.yaml', 'w') as f:
                yaml.dump(yaml_dict, f)
            # create the NLP object
            self.nlp = NLP_opeanai('Gianni Open', key)
            self.window_settings.Close()
        else:
            # create the NLP object
            #self.nlp = NLP('Gianni', summariser, qa, text_generation)
            #self.window_settings.Close()
            pass

    def OnChoice_Summariser(self,event):        # When the user SELECT a summariser
        choice = self.choice_summariser.GetStringSelection()
        return choice

    def OnChoice_QA(self,event):                # When the user SELECT a qa model
        choice = self.choice_qa.GetStringSelection()
        return choice

    def OnChoice_TextGeneration(self,event):    # When the user SELECT a text_generation model
        choice = self.choice_text_generation.GetStringSelection()
        return choice

    def OnSelectDir(self, event):               # When the user SELECT VAULT button 
        '''
        This function allows to select the directory where the Vault is saved.
        It saves the directory in the config.txt file.
        '''
        dlg = wx.DirDialog(self, 'Change Vault', self.dirname, wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            print('You selected: %s' % dlg.GetPath())
            self.dirname = dlg.GetPath()
            self.home_dir = self.dirname

        # save config in the config.yaml
        config = {}
        try:
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            pass

        config['home_dir'] = str(self.home_dir)

        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)

        dlg.Destroy()
        self.window_settings.Close()
        self.files = self.get_files_from_archive()
        self.create_archive(self.panel_main)
        # update the button files
        self.button_files.SetLabel('Archive   : ' + str(len(self.files)))

    def OnTasks(self, event):                  # When the user clicks on the TASKS button
        # open dialog select task
        tasks = {
            '🍩 Summarise': self.OnSummarise,
            '🍪 Wiki Search': self.OnWikipedia_search,
            '🧊 Generate Text': self.OnGeneratingText,
            '🍩 Url Search': self.OnSrapingUrl,
        }
        tasks_ = list(tasks.keys())
        # split at the first space
        dlg = wx.SingleChoiceDialog(self, 'Select Task', 'Tasks', tasks_)
        if dlg.ShowModal() == wx.ID_OK:
            task = dlg.GetStringSelection()
            print('You selected: %s' % task)
            tasks[task](event)
        dlg.Destroy()

    # ----------------- UI -----------------
    def MainBar(self): # create the navigation bar 
        ''' 

        This function creates a navigation bar.
        | File    | Settings               | [DONE] / [DONE]
        
        -----------------------------------
        | New     | Settings               | [DONE] / [DONE]
        | Open    | Select Vault           | [DONE] / [NOT DONE]
        | Save    | Select Summariser      | [DONE] / [NOT DONE]
        | Save As | Select QA              | [DONE] / [NOT DONE]
        | Exit    | Select Text Generation | [DONE] / [NOT DONE]

        '''
        self.CreateStatusBar()
        # 1. Create bar
        menu_bar = wx.MenuBar()
         
        file_menu = wx.Menu()
        AI_menu = wx.Menu()
        Shortcuts_menu = wx.Menu()
        Scraping_menu = wx.Menu()
        settings_menu = wx.Menu()

        # Headers
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(AI_menu, '&AI')
        menu_bar.Append(Shortcuts_menu, '&Shortcuts')
        menu_bar.Append(Scraping_menu, '&Scraping')
        menu_bar.Append(settings_menu, '&Settings')

        # 2. Add items to the Headers
        file_menu.Append(wx.ID_NEW, '&New')
        file_menu.Append(wx.ID_OPEN, '&Open')
        file_menu.Append(wx.ID_SAVE, '&Save')
        file_menu.Append(wx.ID_SAVEAS, 'Save &As')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, 'E&xit')


        Shortcuts_menu.Append(wx.ID_ANY, '&Emoji                       ⌘ + ;')
        Shortcuts_menu.AppendSeparator()

        Shortcuts_menu.Append(wx.ID_ANY, '&Summarise                   ⌘ + A')
        Shortcuts_menu.Append(wx.ID_ANY, '&Wikipedia Search            ⌘ + W')
        Shortcuts_menu.Append(wx.ID_ANY, '&Generate Text               ⌘ + G')
        Shortcuts_menu.Append(wx.ID_ANY, '&Scraping Url                ⌘ + U')

        Scraping_menu.Append(wx.ID_ANY, '&Scraping Url                 ⌘ + S')
        Scraping_menu.Append(wx.ID_ANY, '&Wikipedia Search             ⌘ + W')

        AI_menu.Append(wx.ID_ANY, '&Summarise                            ⌘ + A')
        AI_menu.Append(wx.ID_ANY, '&Generate Text                       ⌘ + G')
        settings_menu.Append(wx.ID_SETUP, '&Settings')

        # 3. ASSIGN FUNCTIONS TO THE options
        self.Bind(wx.EVT_TOOL, self.OnNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_TOOL, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_TOOL, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_TOOL, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_TOOL, self.OnSettings, id=wx.ID_SETUP)

        # 4. Set the menu bar
        self.SetMenuBar(menu_bar)

    def create_archive(self, panel_stats):
        self.files = self.get_files_from_archive()
        try:
            # modify the list of files
            number_of_files = len(self.files)
            self.list.Set(self.files)
            self.list.SetSelection(number_of_files-1)
            self.main_sizer.Show(self.left_sizer)
            self.main_sizer.Layout()
        except:
            # create the list of files
            self.left_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.list = wx.ListBox(panel_stats, choices=self.files, size=(120,300), style=wx.LB_SINGLE|wx.VSCROLL|wx.HSCROLL)
            self.left_sizer.Add(self.list, proportion=1, flag=wx.EXPAND)
            self.main_sizer.Add(self.left_sizer, 1, wx.EXPAND)
            self.main_sizer.Hide(self.left_sizer)

    # ------------------ MAIN LOOP ------------------
    def InitUI(self): # create the UI - main loop
        '''
        Here we define the logic of the UI. 
        And we create the main loop.
        '''
        self.MainBar()
        self.configurations()
        panel_main = wx.Panel(self)
        self.panel_main = panel_main

        # MAIN SIZER
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        def create_all_sizers():
            self.stats_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.text_editor_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        create_all_sizers()

        self.text_ctrl = wx.TextCtrl(panel_main, style=wx.TE_MULTILINE, size = (180,300))
        # add padding to the text editor
        self.text_ctrl.Bind(wx.EVT_KEY_DOWN, self.detect_shortcuts)
        self.text_ctrl.Bind(wx.EVT_TEXT, self.OnTextChange) # bind the text change event
        self.text_editor_sizer.Add(self.text_ctrl, 1, wx.EXPAND|wx.ALL, 10)
        # color is white
        self.text_ctrl.SetBackgroundColour(wx.Colour(255,255,255))
        # color of the panel is white
        panel_main.SetBackgroundColour(wx.Colour(255,255,255))
        # add padding to 
        self.main_sizer.Add(self.text_editor_sizer, 1, wx.EXPAND)

        # create a sizer on top of the text editor
        # add it to the main sizer on top of the text editor
        self.main_sizer.Add(self.top_sizer, 0, wx.EXPAND)
        # SIzer for Markdown
        import wx.html2 as webview # for 
        self.browser = webview.WebView.New(panel_main , size = (180,300))
        # set the margin of the browser
        self.browser.Hide()
        self.text_editor_sizer.Add(self.browser, 1, wx.EXPAND)

        # hide the browser
        self.show_browser = wx.Button(panel_main, label = 'Markdown', size = (100,30))
        def button_show_browser(event):
            if self.browser.IsShown():
                # change name of the button
                self.show_browser.SetLabel('Markdown')
                self.browser.Hide()
                # show the text editor
                self.text_editor_sizer.Show(self.text_ctrl)
                self.main_sizer.Layout()
                # hide the full markdown button
                button_full_markdown.Hide()
                self.text_editor_sizer.Layout()
            else:
                self.browser.Show()
                button_full_markdown.Show()
                # hide the markdown button
                self.text_editor_sizer.Hide(self.show_browser)
                self.text_editor_sizer.Show(self.text_ctrl)
                self.text_editor_sizer.Layout()
        self.show_browser.Bind(wx.EVT_BUTTON,button_show_browser)

        button_full_markdown = wx.Button(panel_main, label = 'Full Markdown', size = (100,30))
        
        def button_full_markdown_(event):
            # show button to markdown
            self.text_editor_sizer.Show(self.show_browser)
            self.text_editor_sizer.Hide(self.text_ctrl)
            self.text_editor_sizer.Show(self.browser)
            # hide the button
            button_full_markdown.Hide()
            # change label to show browser
            self.show_browser.SetLabel('Text Editor')
            self.text_editor_sizer.Layout()
            self.main_sizer.Layout()
        button_full_markdown.Bind(wx.EVT_BUTTON,button_full_markdown_)
        button_full_markdown.Hide()

        self.top_sizer.Add(self.show_browser, 0, wx.EXPAND)
        self.top_sizer.Add(button_full_markdown, 0, wx.EXPAND)

        # ----- ANALYTICS -----
        # add a list for the words  
        self.list_words = wx.ListCtrl(panel_main, size = (300,300), style = wx.LC_REPORT)
        self.list_words.InsertColumn(0, 'Word', width=100)
        self.list_words.InsertColumn(1, 'Count', width=100)
        self.list_words.InsertColumn(2, 'Percentage', width=100)


        def on_selected_word(event):
            # get selected item
            item = self.list_words.GetFocusedItem()
            word = self.list_words.GetItem(item, 0).GetText()
            # now iterate through the text and find the word indexes to change the color
            # get all text as a string
            text = self.text_ctrl.GetValue()
            # split the text into words at the spaces

            def coloring_words_by_indexes(word, text, color = 'blue'):
                # set all text to black
                self.text_ctrl.SetStyle(0, len(text), wx.TextAttr('black'))
                # set default font
                self.text_ctrl.SetStyle(0, len(text), wx.TextAttr(wx.NullColour, wx.NullColour, wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)))
                for i in range(len(text)):
                    # start every space 
                    if text[i] == ' ':
                        # if the word is found
                        if text[i+1:i+len(word)+1] == word:
                            print('found')
                            start_index = i+1
                            end_index = i+len(word)+1
                            self.text_ctrl.SetStyle(start_index, end_index, wx.TextAttr(color))
                            self.text_ctrl.SetStyle(start_index, end_index, wx.TextAttr(wx.NullColour, wx.NullColour, wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)))
            coloring_words_by_indexes(word, text)

        self.list_words.Bind(wx.EVT_LIST_ITEM_SELECTED, on_selected_word)
        self.stats_sizer.Add(self.list_words, 0, wx.EXPAND)

        # add a textarea for the summary or generated text and adding it to the sizer # last modification
        self.text_summary = wx.TextCtrl(panel_main, style=wx.TE_MULTILINE, size = (300,300))
        self.text_ask_ai = wx.TextCtrl(panel_main, style=wx.TE_MULTILINE, size = (10,20))
        self.button_insert = wx.Button(panel_main, label='Insert')
        self.button_ask_AI = wx.Button(panel_main, label='Ask AI')
        
        self.stats_sizer.Add(self.button_insert, 0, wx.EXPAND)
        self.stats_sizer.Add(self.text_summary, 1, wx.EXPAND) 
        self.stats_sizer.Add(self.text_ask_ai, 1, wx.EXPAND)

        self.stats_sizer.Add(self.button_ask_AI, 0, wx.EXPAND)
        # add button event
        def button_click_insert(event):
            # take cursor position
            cursor_position = self.text_ctrl.GetInsertionPoint()
            # insert the text
            self.text_ctrl.WriteText(self.text_summary.GetValue())
            # set the cursor position
            self.text_ctrl.SetInsertionPoint(cursor_position)
        self.button_insert.Bind(wx.EVT_BUTTON, button_click_insert)
        self.main_sizer.Add(self.stats_sizer, 0, wx.EXPAND)

        def button_click_ask_AI(event):
            self.AI_Chatbot = NLP_opeanai('Bot',self.openai_key)
            # get the text from the text area
            question = self.text_ask_ai.GetValue()
            chrono = self.text_summary.GetValue()
            chrono = chrono + f"\n\n Human: \n {question}"
            answer = self.AI_Chatbot.generate_text(chrono)
            # divide answer into two parts
            first_part = "".join(answer.split(':')[0])
            second_part = "".join(answer.split(':')[1:])

            answer = f"{first_part}: \n {second_part}"
            chrono = chrono + f"{answer}"
            self.text_summary.SetValue(chrono)
        self.button_ask_AI.Bind(wx.EVT_BUTTON, button_click_ask_AI)



        # hide the sizer
        self.main_sizer.Hide(self.stats_sizer)
        # ------------------------------------------ ARCHIVE ------------------------------------------
        self.files = self.get_files_from_archive()
        self.create_archive(panel_main)

        # ----- BUTTON FILES -----
       

        # Create a new text area to visualize the selected file
        text_ctrl_1 = wx.TextCtrl(panel_main, style=wx.TE_MULTILINE, size = (500,300))
        self.left_sizer.Add(text_ctrl_1, 1, wx.EXPAND)
        
        button_delete = wx.Button(panel_main, label='Delete')
        button_rename = wx.Button(panel_main, label='Rename')
        #add monoline text area
        self.text_rename = wx.TextCtrl(panel_main, style=wx.TE_PROCESS_ENTER, size = (20,20))
        self.left_sizer.Add(self.text_rename, 1, wx.EXPAND)

        self.left_sizer.Add(button_delete, 0, wx.ALL) # or wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL
        self.left_sizer.Hide(button_delete)
        self.left_sizer.Add(button_rename, 0, wx.ALL) # or wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL
        self.left_sizer.Hide(button_rename)

        def OnSelect(event):
            selected_file = self.list.GetStringSelection()
            with open(self.home_dir + '/' + selected_file, 'r') as f:
                # read the file
                text = f.read()
                # put the text in the text area
                text_ctrl_1.SetValue(text)
                # show the delete button
                self.left_sizer.Show(button_delete)
                # set name of the file to rename
                self.text_rename.SetValue(selected_file)
                # show the rename button
                self.left_sizer.Show(button_rename)
                # show the rename text area
                self.left_sizer.Show(self.text_rename)
            
            def button_click_delete(event):
                # delete the file
                os.remove(self.home_dir + '/' + selected_file)
                # remove the file from the list
                self.list.Delete(self.list.GetSelection())
                self.main_sizer.Layout()

            def button_rename_(event):
                # rename the file
                os.rename(self.home_dir + '/' + selected_file, self.home_dir + '/' + self.text_rename.GetValue())
                # remove the file from the list
                self.list.Delete(self.list.GetSelection())
                self.main_sizer.Layout()
                # now restart the files
                self.files = self.get_files_from_archive()
                self.create_archive(panel_main)

            button_delete.Bind(wx.EVT_BUTTON, button_click_delete)
            button_rename.Bind(wx.EVT_BUTTON, button_rename_)

        def OnDoubleClick(event):
            selected_file = self.list.GetStringSelection()
            with open(self.home_dir + '/' + selected_file, 'r') as f:
                # read the file
                text = f.read()
                # put the text in the text area
                self.text_ctrl.SetValue(text)
            self.filename = selected_file
        
        self.list.Bind(wx.EVT_LISTBOX_DCLICK, OnDoubleClick)
        self.list.Bind(wx.EVT_LISTBOX, OnSelect)

        #---------------------------------------- BUTTONS ARCHIVE and STATS ----------------------------------------
        # Create the two main buttons for the main sizer: Archive and Stats
        self.button_files = wx.Button(panel_main, label=f'Archive    :  {len(self.files)} notes', style = wx.ALIGN_LEFT, size = (200,20))
        self.button_stats = wx.Button(panel_main, label=f'AI & Analysis', style = wx.ALIGN_LEFT)

        def hide_stats(event):
            self.main_sizer.Hide(self.stats_sizer)
            self.main_sizer.Layout()

        # Setting the function for the buttons
        def button_click_files(event):
            if not self.main_sizer.IsShown(self.left_sizer):
                self.main_sizer.Show(self.left_sizer)
            else:
                self.main_sizer.Hide(self.left_sizer)
            self.main_sizer.Layout()
            hide_stats(event)

        def hide_files(event):
            self.main_sizer.Hide(self.left_sizer)
            self.main_sizer.Layout()


        self.button_files.Bind(wx.EVT_ENTER_WINDOW, button_click_files)

        def button_click_stats(event):
            '''
            It's a simple show/hide button for the stats sizer.
            '''
            if not self.main_sizer.IsShown(self.stats_sizer):
                self.main_sizer.Show(self.stats_sizer)
            else:
                self.main_sizer.Hide(self.stats_sizer)
            self.main_sizer.Layout()
            hide_files(event)
            # hide the files

        self.button_stats.Bind(wx.EVT_ENTER_WINDOW, button_click_stats)

        self.button_stats.Bind(wx.EVT_BUTTON, button_click_stats)
        self.button_files.Bind(wx.EVT_BUTTON, button_click_files)

        # Add the buttons to the main sizer
        # add the buttons to the main sizer horizontally
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.button_files, 0, wx.EXPAND)
        self.button_sizer.Add(self.button_stats, 0, wx.EXPAND)
        self.main_sizer.Add(self.button_sizer, 0, wx.EXPAND)
        panel_main.SetSizer(self.main_sizer)


        # set color for the background

        text_ctrl_1.SetForegroundColour('black')
        text_ctrl_1.SetBackgroundColour('white')
        self.list.SetForegroundColour('black')
        self.list.SetBackgroundColour('white')

    # -----------------------------------------------   