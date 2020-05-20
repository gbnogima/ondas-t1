from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from utils import Utils
import math
from fdtd1 import FDTD1
from fdtd2 import FDTD2

def transposeMatrixColumn(matrix, col):
	return [row[col] for row in matrix]

class Application(Tk):
	def updateCanvas(self, val):
		if(not hasattr(self, 'cbMatrixOp') or self.cbMatrixOp.current() == 0):
			matrix = self.voltage_matrix
		else:
			matrix = self.current_matrix

		if(not hasattr(self, 'cbVarOp') or self.cbVarOp.current() == 0):
			array = matrix[int(val)]
		else:
			array = transposeMatrixColumn(matrix, int(val))

		self.matplotCanvas([x for x in range(len(array))], array, matrix.max(), matrix.min())

	def getMatrix(self):
		if(not hasattr(self, 'cbInputOp') or self.cbInputOp.current() == 0):
			(current_matrix, voltage_matrix) = FDTD1.calculate(self.r.get())
		else:
			(current_matrix, voltage_matrix) = FDTD2.calculate(self.r.get())
		self.current_matrix = current_matrix
		self.voltage_matrix = voltage_matrix

	def radioSelect(self):
		self.getMatrix()
		self.slide1.set(0)
		self.updateCanvas(0)

	def cbMatrixOpSelect(self, value):
		self.slide1.set(0)
		self.updateCanvas(0)

	def cbVarOpSelect(self, value):
		if(self.cbVarOp.current() == 0):
			self.slide1.config(to=len(self.current_matrix)-1)
		else: 
			self.slide1.config(to=len(self.current_matrix[0])-1)
		self.slide1.set(0)
		self.updateCanvas(0)

	def cbInputOpSelect(self, value):
		self.getMatrix()
		if(self.cbVarOp.current() == 0):
			self.slide1.config(to=len(self.current_matrix)-1)
		else: 
			self.slide1.config(to=len(self.current_matrix[0])-1)
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

		txtInputOp = StringVar()
		lblInputOp = Label(container, textvariable=txtInputOp, font=("Roboto", 14))
		txtInputOp.set('Entrada:')
		lblInputOp.pack(pady=(20,0))
		self.cbInputOp = ttk.Combobox(container, values=["Entrada1", "Entrada2"])
		self.cbInputOp.current(0)
		self.cbInputOp.pack()
		self.cbInputOp.bind("<<ComboboxSelected>>", self.cbInputOpSelect)

		txtMatrixOp = StringVar()
		lblMatrixOp = Label(container, textvariable=txtMatrixOp, font=("Roboto", 14))
		txtMatrixOp.set('Exibir gráfico de:')
		lblMatrixOp.pack(pady=(20,0))
		self.cbMatrixOp = ttk.Combobox(container, values=["Tensão", "Corrente"])
		self.cbMatrixOp.current(0)
		self.cbMatrixOp.pack()
		self.cbMatrixOp.bind("<<ComboboxSelected>>", self.cbMatrixOpSelect)

		txtVarOp = StringVar()
		lblVarOp = Label(container, textvariable=txtVarOp, font=("Roboto", 14))
		txtVarOp.set('Variar em:')
		lblVarOp.pack(pady=(20,0))
		self.cbVarOp = ttk.Combobox(container, values=["X", "T"])
		self.cbVarOp.current(0)
		self.cbVarOp.pack()
		self.cbVarOp.bind("<<ComboboxSelected>>", self.cbVarOpSelect)

		self.slide1 = Scale(container, from_=0, to=len(self.current_matrix)-1, orient=HORIZONTAL, length=400, bd=0,
										bg='white', troughcolor='#ccc', command=self.updateCanvas)
		self.slide1.pack()

	def __init__(self, current_matrix, voltage_matrix, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		self.current_matrix = current_matrix
		self.voltage_matrix = voltage_matrix
		self.render()

	def matplotCanvas(self, x, y, max, min):
		self.a.clear()
		self.a.set_ylim(min - 0.01, max + 0.01)
		self.a.plot(x, y)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

(current_matrix, voltage_matrix) = FDTD1.calculate(0)
app = Application(current_matrix, voltage_matrix)
app.minsize(500,500)
app.title("Ondas Eletromagnéticas")
app.mainloop()