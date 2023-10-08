import requests
from bs4 import BeautifulSoup

class Silver_Scraper:
    def __init__(self, url):
        self.url = url

    # 1. WIKI
    def get_wiki_text(self, chapter=None):
        '''
        ---
        param: chapter: string (chapter to get)

        return: text: string  (text of the chapter)
                chapters: list (list of the chapters)
        ---
        Is basically the same as the `get_text_from_url` function
        But in the future it will be optimized for wikipedia scraping

        ---
        ```
        The logic is very simple:
        1. get the page
        2. get the chapters
        3. if the chapter is in the chapters:
            3.1. get the text of the chapter
        4. else:
            4.1. get all the text
        5. return the text
        ```
        ---
        This the way that the function works:
        ```
        - If the chapter is been indicated
            - Iterate over the h2 and p tags
            - If the h2 tag is the chapter
                - Get the next h2 tag
                - Iterate over the next siblings
                - If the next sibling is the next h2 tag
                    - break
                - else
                    - append the text to the text list
        - else
            - Iterate over the h2 and p tags
            - Append the text to the text list

        - clean the text
        ```
        ---
        '''
        page = requests.get(self.url) # get the page
        soup = BeautifulSoup(page.content, 'html.parser') # create a BeautifulSoup object
        chapters = soup.find_all('h2') # find all the chapters
        chapters = [c.get_text() for c in chapters] # get the text of the chapters

        # print(chapters)
        if chapter in chapters:
            print(f"Getting chapter {chapter}")
            # iterate over the text if find p or h2
            text = []
            for t in soup.find_all(['p', 'h2']):
                if t.name == 'h2' and t.get_text() == chapter: # if the H2 text is the chapter
                        print("Found chapter")
                        # take all the text until the next h2
                        next_h2 = t.find_next('h2')
                        # loop over the next siblings
                        for t in t.find_next_siblings():
                            if t == next_h2:
                                break
                            else:
                                text.append(t.get_text())
        else:
            # find the text from p and h2
            text = [t.get_text() for t in soup.find_all(['p', 'h2'])]
        
        # join and clean
        text = ' '.join(text)
        text = text.replace("/", "-")
        return text, chapters

    def scraping_wiki(self, last_word):
        '''
        param:  last_word (string)
        return: wiki_text (string)
        -------------------------
        This last word should be in the form of:
        ```/wiki-<search_word>+<chapter_to_get>```

        1. get the word to search

        '''
        print("Getting wikipedia summary")
        word = last_word[6:] # get the word to search
        if "+" in word:
            word_ = word.split("+")[0] 
            chapter_ = word.split("+")[1]
            print(f"Getting chapter {chapter_} of {word_}")
            url = f"https://en.wikipedia.org/wiki/{word_}"
            text, chapters = self.get_wiki_text(url, chapter_)
            wiki_text = text.replace("/", " ") # so the UI won't be alterated for looking at the command
            return wiki_text
        else:
            chapter_ = None
            url = f"https://en.wikipedia.org/wiki/{word}"
            text, chapters = self.get_wiki_text(url)
            text = text.replace("/", " ")
            return text, chapters
    
    # 2. URL
    def get_text_from_url(self, chapter=None):
        '''
        ---
        param: chapter: string (chapter to get)

        return: text: string  (text of the chapter)
                chapters: list (list of the chapters)
        ---
        Is basically the same as the `get_wiki_text` function
        But in the future it will be optimized for wikipedia scraping

        ---
        ```
        The logic is very simple:
        1. get the page
        2. get the chapters
        3. if the chapter is in the chapters:
            3.1. get the text of the chapter
        4. else:
            4.1. get all the text
        5. return the text
        ```
        ---
        This the way that the function works:
        ```
        - If the chapter is been indicated
            - Iterate over the h2 and p tags    
            - If the h2 tag is the chapter
                - Get the next h2 tag
                - Iterate over the next siblings
                - If the next sibling is the next h2 tag
                    - break
                - else
                    - append the text to the text list
        - else
            - Iterate over the h2 and p tags
            - Append the text to the text list

        - clean the text
        ```
        ---
        '''
        page = requests.get(self.url) # get the page
        soup = BeautifulSoup(page.content, 'html.parser') # create a BeautifulSoup object
        chapters = soup.find_all('h2') # find all the chapters
        chapters = [c.get_text() for c in chapters] # get the text of the chapters

        # print(chapters)
        
        if chapter in chapters:
            print(f"Getting chapter {chapter}")
            # iterate over the text if find p or h2
            text = []
            for t in soup.find_all(['p', 'h2']):
                if t.name == 'h2': # if the tag is h2
                    if t.get_text() == chapter: # if the text is the chapter
                        print("Found chapter")
                        text.append(t.get_text()) # append the text
                        next_p = t.find_next('p') # find the next p
                        text.append(next_p.get_text()) # append the text
                        next_h2 = t.find_next('h2') # find the next h2
                        # all the text until the next_2
                        for t in t.find_next_siblings(): # iterate over the siblings
                            if t == next_h2:
                                break
                            else:
                                text.append(t.get_text())
                    else:
                        # handle the case where the chapter is not found
                        pass

            # join the text
            text = ' '.join(text)
            return text, chapters
        else:
            # find the text from p and h2
            text = [t.get_text() for t in soup.find_all(['p', 'h2'])]
            # join the text
            text = ' '.join(text)
            return text, chapters

    def scraping_url(self):
        print("Getting Text from Url")
        text, chapters = self.get_text_from_url()
        # replace the / with a space
        text = text.replace("/", " ")
        return text, chapters
            
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    scraper = Silver_Scraper(url)
    text, chapters = scraper.get_wiki_text("History")
    print(text)