from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Application(Tk):

  def print_result(self, current, voltage):
    print("Corrente: \n")
    for i in current:
        for j in i:
            print("%.5f" % j, end = '    ')
        print("")

    print("\n\nTensão: \n")
    for i in voltage:
        for j in i:
            print("%.5f" % j, end = '    ')
        print("")

  def updateCanvas(self, val):
      self.matplotCanvas([x for x in range(len(self.current_matrix[int(val)]))], self.current_matrix[int(val)])

  def __init__(self, current_matrix, voltage_matrix, *args, **kwargs):
      Tk.__init__(self, *args, **kwargs)
      self.current_matrix = current_matrix
      container = Frame(self)
      container.pack(side="top", fill="both", expand = True)

      print('Tamanho', len(current_matrix), len(current_matrix[0]))

      f = Figure(figsize=(5,5), dpi=100)
      a = f.add_subplot(111)
      canvas = FigureCanvasTkAgg(f, self)
      self.a = a
      self.canvas = canvas
      self.print_result(current_matrix, voltage_matrix)
      self.matplotCanvas([x for x in range(len(current_matrix[0]))], current_matrix[0])
      slide1 = Scale(container, from_=0, to=len(current_matrix)-1, orient=HORIZONTAL, length=400, bd=0,
                bg='white', troughcolor='#ccc', command = self.updateCanvas)
      slide1.pack(side= BOTTOM)

  def matplotCanvas(self, x, y):
    self.a.clear()
    self.a.set_ylim(0, self.current_matrix.max() + 0.01)
    self.a.plot(x, y)
    self.canvas.draw()
    self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)


# app = Application()
# app.minsize(500,500)
# app.title("Ondas Eletromagnéticas")
# app.mainloop()
