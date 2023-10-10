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

### To run the app as a streamlit web app:
```
streamlit run main_st.py
```

### To run the app as a exe with wxpython:
```
python main.py 
```

---
## Dependencies
Still need to take off the ones that are not used. Still in development.
```
wxpython 
requests

pandas 
numpy
scipy

networkx
matplotlib

openai
torch
transformers
nltk
langchain

bs4
tdqm
PyPDF2

streamlit
streamlit_antd_components
streamlit_ace
streamlit_calendar
markdown2
markdown-checklist

python-dotenv
faiss-cpu
altair
tiktoken
```

