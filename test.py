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
        js_script = """
<script>
    // This is a JavaScript script that will be executed when the webview has finished loading
    // You can interact with the webview here

    // Make the table cells draggable
    let cells = document.getElementsByTagName("td");
    for (let i = 0; i < cells.length; i++) {
        let cell = cells[i];
        cell.draggable = true;
        cell.addEventListener("dragstart", handleDragStart);
        cell.addEventListener("dragover", handleDragOver);
        cell.addEventListener("drop", handleDrop);
    }

    // Make the table resizable
    let table = document.getElementsByTagName("table")[0];
    let colResizer = document.createElement("div");
    colResizer.style.width = "5px";
    colResizer.style.height = table.offsetHeight + "px";
    colResizer.style.backgroundColor = "gray";
    colResizer.style.position = "absolute";
    colResizer.style.top = "0";
    colResizer.style.right = "0";
    colResizer.style.cursor = "col-resize";
    table.parentElement.appendChild(colResizer);

    let isResizing = false;
    let lastDownX = 0;
    colResizer.addEventListener("mousedown", handleMouseDown);

    function handleDragStart(event) {
        event.dataTransfer.setData("text", event.target.innerHTML);
        event.currentTarget.style.opacity = "0.5";
    }

    function handleDragOver(event) {
        event.preventDefault();
        event.dataTransfer.dropEffect = "move";
    }

    function handleDrop(event) {
        event.preventDefault();
        let data = event.dataTransfer.getData("text");
        event.target.innerHTML = data;
        event.currentTarget.style.opacity = "1";
    }

    function handleMouseDown(event) {
        lastDownX = event.clientX;
        isResizing = true;
    }

    function handleMouseMove(event) {
        if (!isResizing) {
            return;
        }
        let offsetRight = table.parentElement.offsetLeft + table.parentElement.offsetWidth;
        let delta = event.clientX - lastDownX;
        let newWidth = table.offsetWidth + delta;
        if (newWidth < 50) {
            newWidth = 50;
        }
        if (newWidth > table.parentElement.offsetWidth - 50) {
            newWidth = table.parentElement.offsetWidth - 50;
        }
        table.style.width = newWidth + "px";
        colResizer.style.right = offsetRight - table.offsetWidth + "px";
        lastDownX = event.clientX;
    }

    function handleMouseUp(event) {
        if (isResizing) {
            isResizing = false;
        }
    }

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
</script>
"""

        js_script = '''
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

        html_content += js_script
        self.webview.SetPage(html_content, "")
        
    def onWebviewLoaded(self, event):
        # The webview has finished loading, so we can now interact with it
        pass
        
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
