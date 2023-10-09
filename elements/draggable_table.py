import wx
import wx.html2
import random

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Table Example", size=(800, 600))
        self.webview = wx.html2.WebView.New(self)
        self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.onWebviewLoaded, self.webview)
        
        # Generate a random HTML table with 5 rows and 5 columns
        rows = 5
        cols = 5
        table_content = "<table>"
        for i in range(rows):
            table_content += "<tr>"
            for j in range(cols):
                value = random.randint(1, 100)
                table_content += f"<td>{value}</td>"
            table_content += "</tr>"
        table_content += "</table>"
        
        # Set the HTML content with the table
        html_content = f"""
        <html>
        <head>
            <title>Table Example</title>
            <style>
                table {{
                    border-collapse: collapse;
                }}
                td {{
                    border: 1px solid black;
                    padding: 5px;
                }}
            </style>
        </head>
        <body>
            {table_content}
        </body>
        </html>
        """
        js_script_2 = '''
<script>
    // This is a JavaScript script that will be executed when the webview has finished loading
    // You can interact with the webview here
    let table = document.querySelector('table');
    let offsetX = 0;
    let offsetY = 0;
    let isDragging = false;

    // Add a mousedown event listener to the table to capture the starting position of the mouse
    table.addEventListener('mousedown', (event) => {
        offsetX = event.clientX - table.offsetLeft;
        offsetY = event.clientY - table.offsetTop;
        isDragging = true;
    });

    // Add a mousemove event listener to the document to move the table while the mouse is moved
    document.addEventListener('mousemove', (event) => {
        if (isDragging) {
            table.style.left = event.clientX - offsetX + 'px';
            table.style.top = event.clientY - offsetY + 'px';
            table.style.position = 'absolute';
        }
    });

    // Add a mouseup event listener to the document to stop the dragging by removing the mousemove event listener
    document.addEventListener('mouseup', (event) => {
        isDragging = false;
    });
</script>

'''

        html_content += js_script_2
        self.webview.SetPage(html_content, "")
        
    def onWebviewLoaded(self, event):
        # The webview has finished loading, so we can now interact with it
        pass
        
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
