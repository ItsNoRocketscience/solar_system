# Class definition of planet
# Should include the keplerian elements:
# - Semi-major axis (a) in m, km, or AU
# - Eccentricity (e) no unit: 0 -> circle
# - Inclination (i) in degrees °
# - Longitude of ascending node (o) in degrees °
# - Argument of periapsis (w) in degrees °
# - True anomaly at t0 (v0) in degrees
#
# In addition the following are specified
# - Gravitational constant (mu)
# - Radius for plotting (r)
# - Color for plotting

import geometry_3d as geo
import datetime

# Epoch t0
T0 = datetime.datetime(2000, 1, 1, 12)


class Planet:
    def __init__(self, master=None,
                 a: float = 0., e: float = 0., v0: float = 0.,
                 i: float = 0., o: float = 0., w: float = 0.,
                 r: float = 0., color: str = 'k', mu: float = 0.,
                 name: str = None):
        """
        Class definition for a planet orbiting a central mass
        :param master: Object of central mass (other planet)
        :param a: Orbit-Parameter: Semi-Major axis (a)
        :param e: Orbit-Parameter: Eccentricity (e)
        :param v0: Orbit-Parameter: True anomaly at epoch t0 (nu_0)
        :param i: Orbit-Parameter: Inclination (i)
        :param o: Orbit-Parameter: Longitude of ascending node (Omega)
        :param w: Orbit-Parameter: Argument of periapsis (omega)
        :param r: Radius of planet
        :param color: Color for painting
        :param mu: Gravitational parameter of planet
        :param name: Name of planet
        All distances are specified in m (SI) and all angles in degrees
        """
        self.name = name
        # If master is None, then this planet is the most central element (e.g. sun)
        self.master = master
        self.mu = mu
        if self.master is not None:
            # Calculate orbital period (and inverse)
            self.n = (self.master.mu / a**3)**0.5
            self.orbit_period = 2 * 3.14 / self.n
        else:
            self.n = 0.
        self.r = r
        self.a = a
        self.e = e
        self.i = i
        self.o = o
        self.w = w
        self.v0 = v0
        # Mean anomaly at epoch t0
        self.m0 = mean_from_true(v0, e)
        self.b = (a**2. - a**2. * e**2.)**.5 # Semi-minor axis
        # Vectors of orbit ellipse plane
        self.ue = geo.rotate_z(geo.rotate_y(geo.rotate_z(
            geo.Vector(1, 0, 0), self.w), self.i), self.o)
        self.ve = geo.rotate_z(geo.rotate_y(geo.rotate_z(
            geo.Vector(0, 1, 0), self.w), self.i), self.o)
        self.ne = geo.rotate_z(geo.rotate_y(geo.Vector(0, 0, 1), self.i), self.o)
        # Vectors of semi-major and semi-minor axis
        self.a_vec = self.a * self.ue
        self.b_vec = self.b * self.ve
        # List of matplotlib objects associated with this planet
        self.shapes = []
        self.color = color

    def get_v(self, t: datetime.datetime = None):
        """
        Calculation of true anomaly (angle on ellipse) at a certain time
        :param t: datetime.datetime object
        :return: True anomaly at time t
        """
        if self.master is None:
            return
        dt = t - T0
        dt = dt.total_seconds()
        # Mean anomaly m increases linearly along the orbit
        m = self.m0 + (self.n * dt) * 180. / geo.np.pi
        m = m % 360
        v = true_from_mean(m, self.e)
        return v

    def get_position(self, t: datetime.datetime = None):
        """
        Get xyz-position of planet at a certain time
        :param t: datetime.datetime object
        :return: Vector with xyz coordinates of planet
        """
        if self.master is None:
            # Most central planet is always in the center
            return geo.Vector(0., 0., 0.)
        # Get true anomaly
        v = self.get_v(t)
        # Calculate distance from central mass
        r = self.a * (1 - self.e**2) / (1 + self.e * geo.np.cos(v * geo.np.pi / 180.))
        # Create vector and rotate in ellipsis planet
        r_vec = r * geo.rotate_z(geo.Vector(1, 0, 0), v)
        r_vec = geo.rotate_z(geo.rotate_y(geo.rotate_z(r_vec, self.w), self.i), self.o)
        # Position of planet is relative to position of central mass
        return self.master.get_position(t) - r_vec

    def get_orbit_center(self, t: datetime.datetime = None):
        """
        Get xyz-position of center of orbit ellipse
        :param t: datetime.datetime object
        :return: Vector with xyz coordinates of planet
        """
        if self.master is None:
            return None

        return self.master.get_position(t) + (self.a_vec * self.e)

    def remove_shapes(self):
        """
        Delete all matplotlib shapes associated with planet
        """
        for shape in self.shapes:
            shape.remove()
        self.shapes = []


def mean_from_true(v, e):
    """
    Calculate mean anomaly from true anomaly
    (Source: https://en.wikipedia.org/wiki/Mean_anomaly#Formulae)
    :param v: True anomaly (nu)
    :param e: Eccentricity (e)
    :return: Mean anomaly (m)
    """
    v = v * geo.np.pi / 180.
    m = geo.np.arctan2((1 - e**2)**0.5 * geo.np.sin(v) / (1 + e * geo.np.cos(v)),
                       (e + geo.np.cos(v)) / (1 + e * geo.np.cos(v))) - \
        e * (1 - e**2)**0.5 * geo.np.sin(v) / (1 + e * geo.np.cos(v))
    return m * 180. / geo.np.pi


def true_from_mean(m, e):
    """
    Calculate true anomaly from mean anomaly
    (Source: https://en.wikipedia.org/wiki/True_anomaly#From_the_mean_anomaly)
    :param m: Mean anomaly (m)
    :param e: Eccentricity (e)
    :return: True anomaly (nu)
    """
    m = m * geo.np.pi / 180.
    v = m + (2 * e - 1 / 4 * e**3) * geo.np.sin(m) + \
        5 / 4 * e**2 * geo.np.sin(2 * m) + \
        13 / 12 * e**3 * geo.np.sin(3 * m)
    return v * 180. / geo.np.pi
