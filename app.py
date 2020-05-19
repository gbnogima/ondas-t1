from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from utils import Utils
import math
from fdtd2 import FDTD

class Application(Tk):
	def updateCanvas(self, val):
		if(not hasattr(self, 'comboBox') or self.comboBox.current() == 0):
			self.matplotCanvas([x for x in range(len(self.voltage_matrix[int(val)]))], self.voltage_matrix[int(val)], self.voltage_matrix.max())
		else:
			self.matplotCanvas([x for x in range(len(self.current_matrix[int(val)]))], self.current_matrix[int(val)], self.current_matrix.max())

	def radioSelect(self):
		(current_matrix, voltage_matrix) = FDTD.calculate(self.r.get())
		self.current_matrix = current_matrix
		self.voltage_matrix = voltage_matrix
		self.slide1.set(0)
		self.updateCanvas(0)

	def comboSelect(self, value):
		self.slide1.set(0)
		self.updateCanvas(0)

	def renderPlot(self, container):
		f = Figure(figsize=(5, 5), dpi=100)
		self.a = f.add_subplot(111)
		self.canvas = FigureCanvasTkAgg(f, self)
		# Utils.print_result(self.current_matrix, self.voltage_matrix)
		self.updateCanvas(0)
			
	def render(self):
		container = Frame(self)
		self.container = container
		container.pack(side="top", fill="both", expand=True)
		self.renderPlot(container)
		self.r = DoubleVar()
		resText = StringVar()
		label = Label(container, textvariable=resText, font=("Roboto", 19))
		resText.set('Resistência:')
		label.pack(pady=(20,0))
		R1 = Radiobutton(container, text="∞ (carga em aberto)", variable=self.r, value=float(math.inf),
											command=self.radioSelect)
		R1.pack()

		R2 = Radiobutton(container, text="0 (carga em curto-circuito)", variable=self.r, value=0.0,
											command=self.radioSelect)
		R2.pack()

		R3 = Radiobutton(container, text="100", variable=self.r, value=100.0,
											command=self.radioSelect)
		R3.pack()

		opText = StringVar()
		label2 = Label(container, textvariable=opText, font=("Roboto", 14))
		opText.set('Exibir gráfico de:')
		label2.pack(pady=(20,0))
		self.comboBox = ttk.Combobox(container, values=["Tensão", "Corrente"])
		self.comboBox.current(0)
		self.comboBox.pack()
		self.comboBox.bind("<<ComboboxSelected>>", self.comboSelect)

		self.slide1 = Scale(container, from_=0, to=len(self.current_matrix)-1, orient=HORIZONTAL, length=400, bd=0,
										bg='white', troughcolor='#ccc', command=self.updateCanvas)
		self.slide1.pack()

	def __init__(self, current_matrix, voltage_matrix, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		self.current_matrix = current_matrix
		self.voltage_matrix = voltage_matrix
		self.render()

	def matplotCanvas(self, x, y, max):
		self.a.clear()
		self.a.set_ylim(0, max + 0.01)
		self.a.plot(x, y)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

(current_matrix, voltage_matrix) = FDTD.calculate(0)
app = Application(current_matrix, voltage_matrix)
app.minsize(500,500)
app.title("Ondas Eletromagnéticas")
app.mainloop()