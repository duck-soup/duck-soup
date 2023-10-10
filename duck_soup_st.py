'''
Here I'm implementing the application with streamlit that should allow us a better testing 
and translation to the web app format.

'''
import streamlit as st
import datetime
import yaml
import os
from features.ai import NLP_opeanai
import streamlit as st
import streamlit_antd_components as sac
from streamlit_ace import st_ace
from streamlit_ace import KEYBINDINGS
from utils import get_random_title
import streamlit.components.v1 as components
from streamlit_calendar import calendar
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from utils import css, bot_template, user_template, bot_template_creation
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.prompts import PromptTemplate
import streamlit as st
from langchain.chat_models import ChatOpenAI
from database import DatabaseManager, DbSettings, DbAIAssistants

st.set_page_config(layout="wide")

class DuckSoup_st:
    def __init__(self):
        load_dotenv()
        st.write(css, unsafe_allow_html=True)
        self.db = DatabaseManager('notes.db')
        self.settings_db = DbSettings('settings.db')
        self.ai_assistants_db = DbAIAssistants('ai_assistants.db')
        # initialise the model


        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None
        if "with_assistant_ai" not in st.session_state:
            st.session_state.with_assistant_ai = False

    def init_css(self):
        css = '''               
            <style>
                .markdown-text-container {
                    color: black;
                    background-color: beige;
                    width: 100%;
                    height: 100%;
                    padding: 10px;
                    border-radius: 10px;
                    border: 1px transparent;
                    overflow-y: scroll;
                }
            </style>'''
        st.write(css, unsafe_allow_html=True)

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
                'home_dir': 'vault_test',
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
    
    def configurations_from_db(self):
        # get the settings from the database
        settings = self.settings_db.get_all()
        if settings == []:
            # set the default settings
            settings = ['OpenAI', 'OpenAI', 'OpenAI', '']
            self.settings_db.insert(*settings)
        settings = settings[0]
        self.summarizer_model = settings[0]
        self.qa_model = settings[1]
        self.text_generation_model = settings[2]
        self.openai_key = settings[3]

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

    def get_files_from_database(self):
        self.files = [file[2] for file in self.db.get_all()]
    
    def create_file_menu(self, with_db = False):
        icon_docs = 'folder' if not with_db else 'database'
        if self.files != []:
            with st.sidebar:
                children = [sac.MenuItem('Upload', icon='upload')] + [sac.MenuItem(f'{file}', icon='card-text', tag=f'Tag{i}') for i,file in enumerate(self.files)]
                menu = sac.menu([
                    sac.MenuItem('Docs', icon=icon_docs, children = children),
                    sac.MenuItem('Calendar', icon='calendar'),
                    sac.MenuItem('AI Assistant', icon='robot'),
                    sac.MenuItem('Settings', icon='gear', children=[
                        sac.MenuItem('AI', icon='robot'),
                        sac.MenuItem('Vault', icon='lock'),
                        sac.MenuItem('Theme', icon='brush'),
                        sac.MenuItem('About', icon='info-circle'),
                    ]),
                    # add calendar
                        
                ], open_all=False)
            return menu

    def open_selected_file(self, with_db = False):
        if not with_db:
            with open(self.home_dir + '/' + self.selected_file, 'r') as f:
                content = f.read()
        else:
            # use the database
            content = self.db.get_by_title(self.selected_file)[3]
            if content == '':
                # use emoji and title
                content = self.db.get_by_title(self.selected_file)[1] + '\n' + self.db.get_by_title(self.selected_file)[2]
        return content

    def text_editor(self, with_db = False):
        self.init_css()
        with st.form(key='text_editor'):
            c1,c2,c3 = st.columns([1,1,1])
            if c1.form_submit_button('New', use_container_width=True):
                self.OnNew(with_db)
                st.experimental_rerun()
            if c2.form_submit_button('Save',use_container_width=True):
                self.OnSave(with_db)
            if c3.form_submit_button('Delete', use_container_width=True):
                self.OnDelete(with_db)
                st.experimental_rerun()

            tab1,tab2 = st.tabs([f'Text Editor', f'Markdown Preview'])

            with tab1:
                text = st_ace(placeholder=self.selected_file, value = self.open_selected_file(with_db), height=500)
            with tab2:
                css_for_markdown = '''
                    <div class="markdown-text-container">
                    {{text}}
                '''
                st.markdown(css_for_markdown.replace('{{text}}',text), unsafe_allow_html=True)
        self.text = text

    def OnNew(self, with_db = False):                     # When the user clicks on the NEW-BUTTON or presses Ctrl+N
        '''
        It creates a new file in the home directory.
        The name of the file is a random emoji and a random title.
        '''
        emoj, titl = get_random_title(self.files)
        if not with_db:
            with open(os.path.join(self.home_dir, titl +  '.txt'), 'w') as f:
                f.write(emoj)
                # add in the new line with the title
                f.write('\n' + f"# {titl}" + '\n')
        else:
            # use the database
            self.db.insert(emoj, titl, '', '', '', '')
        self.get_files_from_archive()

    def OnSave(self, with_db = False):                    # When the user clicks on the SAVE BUTTON or presses Ctrl+S
        if not with_db:
            try:
                with open(os.path.join(self.home_dir, self.selected_file), 'w') as f:
                    f.write(self.text)
                st.success('Saved')
            except:
                st.error('No file selected')      
        else:
            # use the database
            self.db.update(self.db.get_by_title(self.selected_file)[0], '', self.selected_file, self.text, '', '', '')
            st.success('Saved')  

    def OnDelete(self, with_db = False):                  # When the user clicks on the DELETE BUTTON or presses Ctrl+D
        if with_db:
            self.db.delete(self.selected_file)
            st.success('Deleted')
            return
        else:
            try:
                os.remove(os.path.join(self.home_dir, self.selected_file))
                st.success('Deleted')
            except:
                st.error('No file selected')

    def Onsettings(self):
        if self.selected_file == 'AI':
            with st.form(key='settings'):
                c1,c2 = st.columns([1,1])
                with c1:
                    self.summarizer_model = st.selectbox('Summarizer', ['OpenAI', 'BART', 'T5', 'Pegasus'])
                    self.qa_model = st.selectbox('QA', ['OpenAI', 'BART', 'T5', 'Pegasus'])
                    self.text_generation_model = st.selectbox('Text Generation', ['OpenAI', 'BART', 'T5', 'Pegasus'])
                with c2:
                    self.openai_key = st.text_input('OpenAI Key', value=self.openai_key, type='password')

                save_b = st.form_submit_button('Save', use_container_width=True)
                if save_b and not self.with_db:
                    self.configurations()
                    with open('config.yaml', 'w') as f:
                        yaml.dump({
                            'home_dir': self.home_dir,
                            'summarizer_model': self.summarizer_model,
                            'qa_model': self.qa_model,
                            'text_generation_model': self.text_generation_model,
                            'openai_key': self.openai_key
                        }, f)

                elif save_b and self.with_db:
                    self.settings_db.update(self.summarizer_model, self.qa_model, self.text_generation_model, self.openai_key)
                    st.experimental_rerun()
        
        elif self.selected_file == 'Vault' and not self.with_db:
            with st.form(key='settings'):
                self.home_dir = st.text_input('Home Directory', placeholder=self.home_dir)
                save_b = st.form_submit_button('Save')
                if save_b:
                    self.configurations()
                    with open('config.yaml', 'w') as f:
                        yaml.dump({
                            'home_dir': self.home_dir,
                            'summarizer_model': self.summarizer_model,
                            'qa_model': self.qa_model,
                            'text_generation_model': self.text_generation_model,
                            'openai_key': self.openai_key
                        }, f)
                    st.experimental_rerun()
        
        elif self.selected_file == 'Vault' and self.with_db:
            st.success('No settings for Vault - Currently in DB mode')
        elif self.selected_file == 'Theme':
            color_choose = st.color_picker('Pick A Color', '#00f900')

    def OnCalendar(self):
        calendar_options = {
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "initialView": "resourceTimelineDay",
            "resourceGroupField": "building",
            "resources": [
                {"id": "a", "building": "Building A", "title": "Building A"},
                {"id": "b", "building": "Building A", "title": "Building B"},
                {"id": "c", "building": "Building B", "title": "Building C"},
                {"id": "d", "building": "Building B", "title": "Building D"},
                {"id": "e", "building": "Building C", "title": "Building E"},
                {"id": "f", "building": "Building C", "title": "Building F"},
            ],
        }
        calendar_events = [
            {
                "title": "Event 1",
                "start": "2023-10-24T08:30:00",
                "end": "2023-10-25T10:30:00",
                "resourceId": "a",
            },
            {
                "title": "Event 2",
                "start": "2023-07-31T07:30:00",
                "end": "2023-07-31T10:30:00",
                "resourceId": "b",
            },
            {
                "title": "Event 3",
                "start": "2023-07-31T10:40:00",
                "end": "2023-07-31T12:30:00",
                "resourceId": "a",
            }
        ]
        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """

        cal = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
        st.write(cal)
    
    def OnUpload(self):
        self.init_css()
        txt = st.sidebar.file_uploader('Upload a file', type=['txt'])
        if txt:
            text = txt.read()
            # transform the text into a list of lines
            text = text.decode('utf-8').split('\n')
            # get the title
            title = text[1].replace('#','').strip()
            # get the emoji
            emoji = text[0]
            # get the content
            content = '\n'.join(text[2:])
            # get the date
            date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # get the last modified
            last_modified = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # get the tags
            tags = ''
            # insert into the database
            #st.write(emoji, title, content, date, last_modified, tags)

            with st.form(key='upload'):
                upload_space_button = st.empty()
                c1,c2,c3,c4 = st.columns([1,1,1,1])
                emoji = c1.text_input('Emoji', value=emoji)
                title = c2.text_input('Title', value=title)
                date = c3.date_input('Date', value='today')
                time = c4.time_input('Time', value='now')
                tab1, tab2 = st.tabs(['Text Editor', 'Markdown Preview'])
                with tab1:
                    content = st_ace(placeholder=title, value = content, height=500)
                with tab2:
                    css_for_markdown = '''
                        <div class="markdown-text-container">
                        {{text}}
                    '''
                    st.markdown(css_for_markdown.replace('{{text}}',content), unsafe_allow_html=True)

                date_and_time = datetime.datetime.combine(date, time).strftime("%d/%m/%Y %H:%M:%S")
                upload_button = upload_space_button.form_submit_button('Upload', use_container_width=True)
                if upload_button and self.with_db:
                    self.db.insert(emoji, title, content, date_and_time, last_modified, tags)
                    st.experimental_rerun()
                elif upload_button and not self.with_db:
                    with open(os.path.join(self.home_dir, title + '.txt'), 'w') as f:
                        f.write(emoji)
                        f.write('\n' + f"# {title}" + '\n')
                        f.write(content)
                    st.experimental_rerun()

    def OnAIAssistant(self):
        # need to create a new page when we can set the role of the ai assistant and the parameters of the model
        with_ai_assistant = st.toggle('AI Assistant', value=st.session_state.with_assistant_ai)
        if self.openai_key == '' or self.openai_key == None:
            st.info('Please go in ⚙️ Settings and update your OpenAI API Key')
            st.stop()
        st.session_state.with_assistant_ai = with_ai_assistant
        if st.session_state.with_assistant_ai and self.ai_assistants_db.get_all() == []:
            with st.form(key= 'AI_Assistant'):
                # add parameters for the AI assistant
                save_button = st.form_submit_button('Save Now') 
                name, temperature, role, image = self.CreateAI()
                if save_button:
                    # save the parameters in the database
                    self.ai_assistants_db.insert(name, temperature, role, image)
                    st.experimental_rerun()
        elif st.session_state.with_assistant_ai and self.ai_assistants_db.get_all() != []:
            self.CreateAI()

    def OnNewAI(self):
        with st.form('AI_Assistant_new'):
            name = st.text_input('Name', value='Elon')
            c1,c2 = st.columns([1,1])
            image = c2.text_input('Image', value = 'data:image/jpeg;base64,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')
            temperature = st.slider('Temperature', 0.0, 1.0, 0.5)
            c1.write(bot_template_creation.replace("{{MSG}}", name).replace('{{IMAGE}}', image), unsafe_allow_html=True)
            c1.markdown
            model = ChatOpenAI(openai_api_key=st.session_state.open_ai_key)
            from langchain.schema import (
                AIMessage,
                HumanMessage,
                SystemMessage
            )
            role = st.text_area('Role', value = 'You are a stand-up comedian that always try to make a joke about what the user says.')
            chat_due = st.text_input(label='Chat', key = 'chat_2')
            if chat_due:
                message = role + '\n' + chat_due
                answer = model([HumanMessage(content=message)])
                st.write(answer)

            if st.form_submit_button('Save', use_container_width=True, type='primary'):
                self.ai_assistants_db.insert(name, temperature, role, image)
                st.success('Saved')
                st.experimental_rerun()
            return name, temperature, role, image
        
    def CreateAI(self):
        st.write(st.session_state.choosen_ai if st.session_state.choosen_ai else 'No AI choosen')

        if self.ai_assistants_db.get_all() == []:
            self.OnNewAI()
        else:
            buttons =  [sac.ButtonsItem(label='New AI')] + [sac.ButtonsItem(label=f'{ai[1]}') for ai in self.ai_assistants_db.get_all()]
            choosen = sac.buttons(buttons, format_func='title', align='center', shape='round', index = 1)
            if choosen == 'New AI':
                self.OnNewAI()
                st.stop()
            else:
                if choosen != st.session_state.choosen_ai:
                    st.write('Changed')
                    st.session_state.choosen_ai = choosen
                    st.session_state.langchain_messages = []
                    st.experimental_rerun()
                # get ai from name 
                ai = self.ai_assistants_db.get_by_name(choosen)
                st.session_state.choosen_ai = choosen
                if ai:
                    with st.form(key = f'{ai[1]}'):
                        name = ai[1]
                        temperature = ai[2]
                        role = ai[3]
                        image = ai[4]

                        c1,c2 = st.columns([1,1])
                        name = c1.text_input('Name', value=name)
                        image = c2.text_input('Image', value = image)
                        st.write(bot_template_creation.replace("{{MSG}}", name).replace('{{IMAGE}}', image), unsafe_allow_html=True)
                        role = st.text_area('Role', value = role)
                        temperature = st.slider('Temperature', 0.0, 1.0, temperature)
                        model = ChatOpenAI(openai_api_key=st.session_state.open_ai_key)
                        from langchain.schema import (
                            AIMessage,
                            HumanMessage,
                            SystemMessage
                        )
                        chat_due = st.text_input(label='Chat', key = 'chat_2', placeholder='Hi, can you help me?')
                        if chat_due:
                            message = role + '\n' + chat_due
                            answer = model([HumanMessage(content=message)])
                            st.write(bot_template_creation.replace("{{MSG}}", answer.content).replace('{{IMAGE}}', image), unsafe_allow_html=True)

                        if st.form_submit_button('Save', use_container_width=True, type='primary'):
                            # get id from name
                            self.ai_assistants_db.update_from_name(name, temperature, role, image)
                            st.success('Saved')
                            st.experimental_rerun()

                        if st.form_submit_button('Delete', use_container_width=True, type='secondary'):
                            self.ai_assistants_db.delete_from_name(name)
                            st.success('Deleted')
                            st.experimental_rerun()

                        return name, temperature, role, image
    
    def ChatAgent(self):
        ai = self.ai_assistants_db.get_by_name(st.session_state.choosen_ai)
        name = ai[1]
        temperature = ai[2]
        role = ai[3]
        image = ai[4]
        # Set up memory
        msgs = StreamlitChatMessageHistory(key="langchain_messages")
        memory = ConversationBufferMemory(chat_memory=msgs)
        if len(msgs.messages) == 0:
            msgs.add_ai_message("How can I help you?")

        view_messages = st.expander("View the message contents in session state")

        # Get an OpenAI API Key before continuing
        if self.openai_key:
            openai_api_key = self.openai_key
        else:
            openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
        if not openai_api_key:
            st.info("Enter an OpenAI API Key to continue")
            st.stop()

        # Set up the LLMChain, passing in memory
        template = f"""Your role: {role}"""+""" {history}
        Human: {human_input} """ + f"""
        {name}""" 
        prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
        llm_chain = LLMChain(llm=OpenAI(openai_api_key=openai_api_key), prompt=prompt, memory=memory)

        # Render current messages from StreamlitChatMessageHistory
        def render_messages():
            with st.sidebar.expander("Chat History", expanded=True):
                if st.button('Restart Memory', use_container_width=True):
                    st.session_state.langchain_messages = []
                    st.experimental_rerun()

                for i, msg in enumerate(msgs.messages):
                    if i % 2 != 0:
                        st.write(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
                    else:
                        st.write(bot_template_creation.replace("{{MSG}}", msg.content).replace('{{IMAGE}}', image), unsafe_allow_html=True)

        # If user inputs a new prompt, generate and draw a new response
        if prompt := st.chat_input():
            response = llm_chain.run(prompt)
    
        render_messages()

    def ChatFeatures(self):
        # get open_ai_key from the config file
        st.session_state.open_ai_key = self.openai_key
        try:
            open_ai_key = st.session_state.open_ai_key
        except:
            open_ai_key = st.text_input(
            "Please enter your OpenAI API key", type="password")
            save_button = st.button("Save key")
            if save_button and not self.with_db:
                # save to config file
                with open('config.yaml', 'r') as f:
                    config = yaml.safe_load(f)
                config['openai_key'] = open_ai_key
                with open('config.yaml', 'w') as f:
                    yaml.dump(config, f)
            elif save_button and self.with_db:
                # save to db
                self.settings_db.update_key(open_ai_key)
            # save as session state
            st.session_state.open_ai_key = open_ai_key

        if st.session_state.with_assistant_ai:
            # get name of selected ai
            self.ChatAgent()

    def get_text(self):
        try:
            return self.text
        except:
            return ''
    
    def run(self):  
        with st.sidebar:
            db_or_file =  sac.buttons([
                sac.ButtonsItem(label='Database', icon='database'),
                sac.ButtonsItem(label='Folder', icon='folder'),
            ])
        self.with_db = True if db_or_file == 'Database' else False
        if self.with_db:
            self.configurations_from_db()
        else:
            self.configurations()
        with_db = self.with_db
        if db_or_file == 'Database':
            self.get_files_from_database()
        else:
            self.get_files_from_archive()

        selected = self.create_file_menu(with_db)
        commands = ['AI', 'Vault', 'Theme', 'About', 'Calendar', 'Upload']
        try:
            self.selected_file =  selected if selected in self.files else self.files[0] if selected not in commands else selected
        except:
            self.selected_file = self.files[0] if self.files != [] else 'No files'
        
        if selected in commands and selected in ['AI', 'Vault', 'Theme', 'About']:
            self.Onsettings()
        elif selected == 'Calendar':
            self.OnCalendar()
        elif selected == 'Upload':
            self.OnUpload()
        elif selected == 'AI Assistant':
            self.OnAIAssistant()

        if selected in self.files:
            self.text_editor(with_db)
            

        self.ChatFeatures()

if __name__ == '''__main__''':
    app = DuckSoup_st()
    app.run()
