'''
Author: @robertoscalas
Date:   2023-02-01 12:00:00
Description: 
------------------------------------------------------------
The idea is to create a note taking app that will be able to:
------------------------------------------------------------
- Create notes                [DONE]
- Read notes                  [DONE]
- Delete notes                [DONE]
- Update notes                [DONE]
- Scrape Wikipedia            [DONE]
- Scrape any URL              [DONE]
- Store the notes in a vault  [DONE]
- Change the vault directory  [DONE]
- MD viewer                   [DONE]
- Emojis Picker               [DONE]
- Automatic Icon Page         [DONE]
- Use AI to process text      [DONE]
- Use AI to generate text     [DONE]
- Use AI to answer questions  [DONE]
- Use AI to summarize text    [DONE]

------------------------------------------------------------
- Change the vault password   [NOT DONE]
- Change the theme of the app [NOT DONE]
- Search for notes            [NOT DONE]
- Encrypt notes               [NOT DONE]

---
Need now to create a window to show the links
after that need to better select the links that i need (the one from see also section only)

---
'''
import wx
from duck_soup import DuckSoupApp

if __name__ == '__main__':
    app = wx.App()
    DuckSoupApp(None, title='duck-soup')
    app.MainLoop()