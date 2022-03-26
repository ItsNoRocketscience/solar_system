import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk


class OrbitWindow(tk.Frame):
    def __init__(self, root: tk.Tk = None, canvas=None):
        tk.Frame.__init__(self, root)
        self.grid()
        self.master.resizable(False, False)
        self.canvas = canvas
        self.tk_canvas = FigureCanvasTkAgg(canvas.fig, master=self)
        self.tk_canvas.draw()
        self.tk_canvas.get_tk_widget().grid(row=1, column=1)

        self.time_slider = tk.Scale(self, from_=-365, to=365, orient='horizontal',
                                    command=self.change_time, showvalue=False, label='Time')
        self.time_slider.grid(row=0, column=0, columnspan=3, sticky='EW')

        self.theta_slider = tk.Scale(self, from_=-180, to=180, orient='vertical',
                                     command=self.change_theta, showvalue=False,  # label='Rotation - Z',
                                     resolution=10, tickinterval=10)
        self.theta_slider.grid(row=1, column=0, rowspan=2, sticky='NSEW')

        self.phi_slider = tk.Scale(self, from_=-180, to=180, orient='vertical',
                                   command=self.change_phi, showvalue=False,  # label='Rotation - X',
                                   resolution=10, tickinterval=10)
        self.phi_slider.grid(row=1, column=2, rowspan=2, sticky='NSEW')

        self.zoom_var = tk.DoubleVar()
        self.zoom_var.set(1.0)
        self.zoom_slider = tk.Scale(self, from_=1., to=.1, orient='horizontal',
                                    showvalue=False, variable=self.zoom_var,
                                    command=self.change_zoom, resolution=.05,
                                    label='Zoom')
        self.zoom_slider.grid(row=2, column=1, sticky='EW')
        self.change_zoom(None)

        self.psi_slider = tk.Scale(self, from_=-180, to=180, orient='horizontal',
                                   command=self.change_psi, showvalue=False, label='Rotation - Y',
                                   resolution=10, tickinterval=20)
        self.psi_slider.grid(row=3, column=0, columnspan=3, sticky='EW')
        self.change_time(None)

    def change_phi(self, event):
        phi = self.phi_slider.get()
        # print(phi)
        self.canvas.set_phi(phi)
        self.tk_canvas.draw()

    def change_psi(self, event):
        psi = self.psi_slider.get()
        # print(psi)
        self.canvas.set_psi(psi)
        self.tk_canvas.draw()

    def change_theta(self, event):
        theta = self.theta_slider.get()
        # print(theta)
        self.canvas.set_theta(theta)
        self.tk_canvas.draw()

    def change_zoom(self, event):
        zoom = self.zoom_var.get()
        self.canvas.set_zoom(zoom)
        self.zoom_slider.config(label=f'Zoom: {zoom:.2f}')
        self.tk_canvas.draw()

    def change_time(self, event):
        day = self.time_slider.get()
        time_str = self.canvas.set_delta_day(day)
        self.time_slider.config(label=time_str)
        self.tk_canvas.draw()
