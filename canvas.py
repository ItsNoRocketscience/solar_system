# Canvas definition with viewing angles etc.
from matplotlib.patches import Ellipse, Arc, Circle
from matplotlib.figure import Figure
import geometry_3d as geo
import datetime

# Margin for angle, should projection not be possible
eps_angle = .1
# Aspect ratio


class OrbitCanvas:
    def __init__(self, time: datetime.datetime, width: float = 800,
                 height: float = 480, dpi: float = 100):
        """
        Canvas to plot planet with orbits on
        :param time: datetime.datetime object
        :param width: Width of figure in pixels
        :param height: Height of figure in pixels
        :param dpi: DPI setting for figure
        """
        # Matplotlib figure and axis
        self.fig = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
        self.aspect_ratio = width / height
        self.fig.set_tight_layout(True)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        # Set initial limit for axis
        self.lim = 1.
        # Zoom between 1. (whole picture) and 0. (infinite zoom)
        self.zoom = 1.0
        # Starting time for usage in tkinter window with time delta
        self.time0 = time
        self.time = time
        # Viewing angles
        self.phi = 0.
        self.psi = 0.
        self.theta = 0.
        # List of planets
        self.planets = []
        # Vectors of projection plane
        self.up = geo.Vector(1, 0, 0)
        self.vp = geo.Vector(0, 1, 0)
        self.np = geo.Vector(0, 0, 1)
        # Text objects
        self.date_text = None
        self.time_text = None
        # Initially Text objects
        self.add_timestamp()

    def set_axis_limits(self, new_lim: float):
        """
        Adjust axis limits and apply zoom factor
        :param new_lim: New limit value for x-axis
        """
        self.lim = max(self.lim, new_lim)
        lim = self.lim * self.zoom
        self.ax.set_xlim((-lim * self.aspect_ratio,
                          lim * self.aspect_ratio))
        self.ax.set_ylim((-lim, lim))

    def set_zoom(self, zoom):
        """
        Set new zoom factor for canvas
        :param zoom: New zoom factor (between 1. and 0.)
        """
        self.zoom = zoom
        self.set_axis_limits(0.)
        self.redraw_planets()

    def set_delta_day(self, day: float):
        """
        For usage with tkinter window: Set a delta day
        :param day: Number of days to start time (float)
        """
        # Remove text objects
        self.date_text.remove()
        self.time_text.remove()
        # Set new time
        self.time = self.time0 + datetime.timedelta(days=day)
        self.redraw_planets()
        self.add_timestamp()
        # Return time string for showing in tkinter window
        return self.time.strftime('%d/%m/%Y')

    def rotate_vectors(self):
        """
        Rotate Vectors of projection plane according to viewing angles
        """
        self.up = geo.rotate_xyz(geo.Vector(1, 0, 0), self.phi, self.psi, self.theta)
        self.vp = geo.rotate_xyz(geo.Vector(0, 1, 0), self.phi, self.psi, self.theta)
        self.np = geo.rotate_xyz(geo.Vector(0, 0, 1), self.phi, self.psi, self.theta)

    def set_phi(self, phi: float):
        """
        Set new value for x-axis viewing angle
        :param phi: float value for x-axis viewing angle
        A separate function is used for every axis, so projection errors
        can more easily be handled
        """
        self.phi = phi
        self.rotate_vectors()
        # Redraw planets and orbits
        try:
            self.redraw_planets()
        except ValueError:
            # If projection is not successful, angle is shifted slightly and redone
            self.phi = phi + eps_angle
            self.rotate_vectors()
            self.redraw_planets()

    def set_psi(self, psi: float):
        """
        Set new value for y-axis viewing angle
        :param psi: float value for y-axis viewing angle
        A separate function is used for every axis, so projection errors
        can more easily be handled
        """
        self.psi = psi
        self.rotate_vectors()
        # Redraw planets and orbits
        try:
            self.redraw_planets()
        except ValueError:
            # If projection is not successful, angle is shifted slightly and redone
            self.psi = psi + eps_angle
            self.rotate_vectors()
            self.redraw_planets()

    def set_theta(self, theta: float):
        """
        Set new value for z-axis viewing angle
        :param theta: float value for z-axis viewing angle
        A separate function is used for every axis, so projection errors
        can more easily be handled
        """
        self.theta = theta
        self.rotate_vectors()
        # Redraw planets and orbits
        try:
            self.redraw_planets()
        except ValueError:
            # If projection is not successful, angle is shifted slightly and redone
            self.theta = theta + eps_angle
            self.rotate_vectors()
            self.redraw_planets()

    def add_planet(self, planet):
        """
        Add a new planet object for drawing
        :param planet: planet.Planet object
        """
        self.planets.append(planet)

    def redraw_planets(self):
        """
        Redraw all planets on canvas
        """
        if not self.planets:
            return
        # Remove all shapes for each planet
        for planet in self.planets:
            try:
                planet.remove_shapes()
            except ValueError:
                pass
            self.draw_planet(planet)
        # Adjust axis limits
        self.set_axis_limits(max([p.a for p in self.planets]))
        # Create planet annotations
        self.annotate_planets()

    def draw_planet(self, planet):
        """
        Draw planet and orbit on canvas
        :param planet: planet.Planet object
        """
        if planet.master is None:
            # Draw central planet in the middle
            shape = Circle((0, 0), planet.r, color=planet.color)
            planet.shapes.append(self.ax.add_patch(shape))
        else:
            # For all other planets the orbit must be projected on viewing plane
            # Defining vectors of viewing planet
            up = self.up
            vp = self.vp
            np = self.np
            # Center of planet orbit
            ce = planet.get_orbit_center(self.time)
            # Position of center on viewing planet
            orbit_center = geo.project(ce, up, vp, np)
            # Remaining parameters necessary for projection
            a = planet.a
            b = planet.b
            ue = planet.ue
            ve = planet.ve
            ne = planet.ne
            # Perform projection to get semi axis lengths and angle of ellipse
            d0, d1, angle = geo.project_ellipse(a, b, ce, ne, ue, ve, np, up, vp)
            # Position of planet on viewing plane
            planet_pos = geo.project(planet.get_position(self.time), up, vp, np)

            # In addition to the complete orbit outline, an arc is created
            # from the current planet position to certain time before
            planet_angle = geo.angle2d(geo.Vector(1, 0), planet_pos - orbit_center)
            # Angle of current planet position
            planet_angle = (planet_angle - angle + 360.) % 360.
            # Time or 1/12th orbit before
            dt = datetime.timedelta(seconds=planet.orbit_period * 1/12)
            # Calculate other angle for arc
            next_angle = geo.angle2d(
                geo.Vector(1, 0), geo.project(planet.get_position(self.time - dt),
                                              up, vp, np) - orbit_center)
            next_angle = (next_angle - angle + 360.) % 360.
            # Theta values for arc creation
            thetas = (planet_angle, next_angle)
            theta_1 = min(thetas)
            theta_2 = max(thetas)
            # If arc spans over 0° theta values must be adjusted
            if (theta_2 - theta_1) > 180.:
                _theta_tmp = theta_1
                theta_1 = theta_2 - 360.
                theta_2 = _theta_tmp

            # Draw orbit outline
            orbit_outline = Ellipse(orbit_center, width=2 * d0, height=2 * d1, angle=angle,
                                    color='silver', lw=1.0, ls='--', fill=False)
            planet.shapes.append(self.ax.add_patch(orbit_outline))
            # Draw arc of planet
            orbit = Arc(orbit_center, width=2 * d0, height=2 * d1, angle=angle,
                        theta1=theta_1, theta2=theta_2,
                        lw=2.0, color=planet.color, fill=False)
            planet.shapes.append(self.ax.add_patch(orbit))

            # Draw circle around current planets position
            # Size of circle is independent of zoom and axis limits
            shape = Circle(planet_pos, self.lim / 1.5E1 * self.zoom,
                           ls='-', lw=1.0, color=planet.color, fill=False)
            planet.shapes.append(self.ax.add_patch(shape))

    def annotate_planets(self):
        """
        Create annotation with planet names
        """
        # Get axis limit for deciding whether planet should be annotated
        x_lim = self.ax.get_xlim()[1]
        for planet in self.planets:
            if planet.master is None:
                # No naming of central planet
                continue
            d0 = max(planet.shapes[0].width, planet.shapes[0].height)
            if x_lim / 2 / d0 > 5:
                # Scale too small for planet to be annotated
                continue

            planet_pos = planet.shapes[2].get_center()
            text_pos = (planet_pos[0], planet_pos[1] + self.lim / 1.5E1 * self.zoom)
            planet.shapes.append(
                self.ax.annotate(planet.name, planet_pos, text_pos, ha='center', va='bottom',
                                 bbox=dict(facecolor='white', alpha=.8, edgecolor='none',
                                           boxstyle='round,pad=0.1'))
            )

    def add_timestamp(self):
        """
        Add text objects with current date and time
        """
        date_str = self.time.strftime('%A %d. %B %Y')
        self.date_text = self.ax.text(0.5, 1, date_str, ha='center', va='top',
                                      fontsize=15, transform=self.ax.transAxes,
                                      bbox=dict(facecolor='white', edgecolor='none'))

        time_str = self.time.strftime('%H:%M:%S')
        self.time_text = self.ax.text(0.5, 0.95, time_str, ha='center', va='top',
                                      fontsize=13, transform=self.ax.transAxes,
                                      bbox=dict(facecolor='white', edgecolor='none'))
