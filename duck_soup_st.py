'''
Here I'm implementing the application with streamlit that should allow us a better testing 
and translation to the web app format.

'''
import streamlit as st
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
from utils import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

st.set_page_config(layout="wide")

class DuckSoup_st:
    def __init__(self):
        load_dotenv()
        st.write(css, unsafe_allow_html=True)

        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

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
    
    def create_file_menu(self):
        with st.sidebar:
            menu = sac.menu([
                sac.MenuItem('Docs', icon='lock', children=[sac.MenuItem(f'{file}', icon='card-text', tag=f'Tag{i}') for i,file in enumerate(self.files)]),
                sac.MenuItem('Settings', icon='gear', children=[
                    sac.MenuItem('AI', icon='robot'),
                    sac.MenuItem('Vault', icon='lock'),
                    sac.MenuItem('Theme', icon='brush'),
                    sac.MenuItem('About', icon='info-circle'),
                ]),
                # add calendar
                sac.MenuItem('Calendar', icon='calendar'),
                    
            ], open_all=True)
        return menu

    def open_selected_file(self):
        with open(self.home_dir + '/' + self.selected_file, 'r') as f:
            content = f.read()
        return content

    def text_editor(self):
        self.init_css()
        c1,c2 = st.tabs([f'Text Editor', f'Markdown Preview'])
        with c1:
            text = st_ace(placeholder=self.selected_file, value = self.open_selected_file(), height=500)
        with c2:
            css_for_markdown = '''
                <div class="markdown-text-container">
                 {{text}}
            '''
            st.markdown(css_for_markdown.replace('{{text}}',text), unsafe_allow_html=True)
        self.text = text

    def OnNew(self):                     # When the user clicks on the NEW-BUTTON or presses Ctrl+N
        emoj, titl = get_random_title(self.files)
        with open(os.path.join(self.home_dir, titl +  '.txt'), 'w') as f:
            f.write(emoj)
            # add in the new line with the title
            f.write('\n' + f"# {titl}" + '\n')
        self.get_files_from_archive()

    def OnSave(self):                    # When the user clicks on the SAVE BUTTON or presses Ctrl+S
        try:
            with open(os.path.join(self.home_dir, self.selected_file), 'w') as f:
                f.write(self.text)
            st.success('Saved')
        except:
            st.error('No file selected')        

    def OnDelete(self):                  # When the user clicks on the DELETE BUTTON or presses Ctrl+D
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
                    self.openai_key = st.text_input('OpenAI Key')
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
        
        elif self.selected_file == 'Vault':
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
    
    def ChatFeatures(self):

        # get open_ai_key from the config file
        try:
            open_ai_key = st.session_state.open_ai_key
        except:
            open_ai_key = st.text_input(
            "Please enter your OpenAI API key", type="password")
            if st.button("Save key"):
                # save to config file
                with open('config.yaml', 'r') as f:
                    config = yaml.safe_load(f)
                config['openai_key'] = open_ai_key
                with open('config.yaml', 'w') as f:
                    yaml.dump(config, f)

            # save as session state
            st.session_state.open_ai_key = open_ai_key



        def get_pdf_text(pdf_docs):
            text = ""
            for pdf in pdf_docs:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text

        def get_text_chunks(text):
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
            return chunks

        def get_vectorstore(text_chunks):
            embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.open_ai_key)
            # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
            vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
            return vectorstore

        def get_conversation_chain(vectorstore):
            llm = ChatOpenAI(openai_api_key=st.session_state.open_ai_key)
            # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

            memory = ConversationBufferMemory(
                memory_key='chat_history', return_messages=True)
            conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(),
                memory=memory
            )
            return conversation_chain

        def handle_userinput(user_question):
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']

            with st.sidebar.expander("Chat History", expanded=True):
                for i, message in enumerate(st.session_state.chat_history):
                    if i % 2 == 0:
                        st.write(user_template.replace(
                            "{{MSG}}", message.content), unsafe_allow_html=True)
                    else:
                        st.write(bot_template.replace(
                            "{{MSG}}", message.content), unsafe_allow_html=True)

        def main():
            user_question = st.chat_input("Ask a question about your documents:")
            if user_question:
                handle_userinput(user_question)

            with st.sidebar:
                # from other sources
                selection = st.radio("Select your source", ["Docs", "PDFs"], horizontal=True)
                if st.button("Process", key="process"):#, value=True):
                    if selection == "PDFs":
                        pdf_docs = st.file_uploader(
                            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
                        raw_text = get_pdf_text(pdf_docs)
                    elif selection == "Docs":
                        raw_text = self.get_text()
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)

                    st.session_state.conversation = get_conversation_chain(
                        vectorstore)

        main()
        # done

    def get_text(self):
        return self.text
    
    def run(self):  
        self.configurations()
        self.get_files_from_archive()
        st.write(self.home_dir)
        selected = self.create_file_menu()
        commands = ['AI', 'Vault', 'Theme', 'About', 'Calendar']
        self.selected_file =  selected if selected in self.files else self.files[0] if selected not in commands else selected
        st.write(self.selected_file)
        
        if selected in commands and selected != 'Calendar':
            self.Onsettings()
        elif selected == 'Calendar':
            self.OnCalendar()

        if selected in self.files:
            self.text_editor()
            c1,c2 = st.sidebar.columns([1,1])
            if c1.button('New', key='new', use_container_width=True):
                self.OnNew()
                st.experimental_rerun()
            if c2.button('Save', key='save', use_container_width=True):
                self.OnSave()
            if st.sidebar.button('Delete', key='delete', use_container_width=True):
                self.OnDelete()
                st.experimental_rerun()
            self.ChatFeatures()


if __name__ == '''__main__''':
    app = DuckSoup_st()
    app.run()
