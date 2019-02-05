import htmlPy
from driver import app

class BackEnd(htmlPy.Object):

	def __init__(self, app):
		super(BackEnd, self).__init__()
		self.app = app
		
	@htmlPy.Slot(str)
	def say_hello_world(self, x="Yo"):
		print(x)
		app.evaluate_javascript("console.log('" + x + "')")

	@htmlPy.Slot(str)
	def go(self, dest="./index.html"):
		self.app.template = (dest, {})
		
	@htmlPy.Slot()
	def listenForAdvancement(self):
		#add loop for listening for input, or whatever we end up deciding
		#do not infinite loop, as this will disable gui, listen, and return to gui if not available
		pass
		
app.bind(BackEnd(app))
app.template = ("./index.html", {})

if __name__ == "__main__":
	app.start()
