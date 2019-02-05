import os
import htmlPy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = htmlPy.AppGUI(title=u"Sample application", maximized=True, plugins=True)
app.static_path = "."
app.template_path = "./template"
app.developer_mode = True
