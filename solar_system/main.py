# Main skript for testing with tkinter window
from window import OrbitWindow
from canvas import OrbitCanvas
import datetime
import planets

time = datetime.datetime.now()

canvas = OrbitCanvas(time=time)

window = OrbitWindow(canvas=canvas)

canvas.add_planet(planets.sun)
canvas.add_planet(planets.mercury)
canvas.add_planet(planets.venus)
canvas.add_planet(planets.earth)
canvas.add_planet(planets.mars)
canvas.add_planet(planets.jupiter)
# canvas.add_planet(planets.saturn)
# canvas.add_planet(planets.uranus)
# canvas.add_planet(planets.neptune)

# canvas.add_planet(planets.moon)
window.zoom_slider.set(0.40)
window.phi_slider.set(-70.)
# canvas.redraw_planets()

window.mainloop()
