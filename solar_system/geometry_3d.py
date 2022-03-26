# Some 3D geometry
import numpy as np


class Vector(np.ndarray):
    """
    General class for n dimensional vector

    Defined as subclass of numpy ndarray class.
    Uses basically all of its functionality.
    In addition this class adds:
        - Vector initialization with coordinated directly (instead of tuple)
        - Dimension and length attributes
        - Method "unit" for creating a vector with unit length
        - Method "from_points" for creating vector from two others
    """
    def __new__(cls, *coords):
        vec = np.asarray(coords).view(cls)
        vec.dim = vec.size
        vec.length = np.sqrt(np.sum([s**2 for s in vec]))
        return vec

    @classmethod
    def from_points(cls, pt1, pt2):
        return cls(*[pt2[i] - pt1[i] for i in range(pt1.dim)])

    def unit(self):
        return Vector(*[self[i] / self.length for i in range(self.dim)])


def rotate_x(vec, phi: float):
    """
    Rotate a 3d-vector around the first (x) axis
    :param vec: Vector object to rotate
    :param phi: Rotation angles (in degrees)
    :return: Rotated 3d vector
    Dimension of vector is not checked for faster execution
    """
    phi = np.pi * phi / 180.
    x_ = vec[0] * 1. + vec[1] * 0. + vec[2] * 0.
    y_ = vec[0] * 0. + vec[1] * np.cos(phi) - vec[2] * np.sin(phi)
    z_ = vec[0] * 0. + vec[1] * np.sin(phi) + vec[2] * np.cos(phi)

    return Vector(x_, y_, z_)


def rotate_y(vec, psi: float):
    """
    Rotate a 3d-vector around the second (y) axis
    :param vec: Vector object to rotate
    :param psi: Rotation angles (in degrees)
    :return: Rotated 3d vector
    Dimension of vector is not checked for faster execution
    """
    psi = np.pi * psi / 180.
    x_ = vec[0] * np.cos(psi) + vec[1] * 0. + vec[2] * np.sin(psi)
    y_ = vec[0] * 0. + vec[1] * 1. - vec[2] * 0.
    z_ = -vec[0] * np.sin(psi) + vec[1] * 0. + vec[2] * np.cos(psi)

    return Vector(x_, y_, z_)


def rotate_z(vec, theta: float):
    """
    Rotate a 3d-vector around the third (z) axis
    :param vec: Vector object to rotate
    :param theta: Rotation angles (in degrees)
    :return: Rotated 3d vector
    Dimension of vector is not checked for faster execution
    """
    theta = np.pi * theta / 180.
    x_ = vec[0] * np.cos(theta) - vec[1] * np.sin(theta) + vec[2] * 0.
    y_ = vec[0] * np.sin(theta) + vec[1] * np.cos(theta) + vec[2] * 0.
    z_ = vec[0] * 0. + vec[1] * 0. + vec[2] * 1.

    return Vector(x_, y_, z_)


def project(p: Vector, u: Vector, v: Vector, n: Vector):
    """
    Project a 3d point on a plane with own coordinate system
    :param p: Origin vector of point to project
    :param u: First axis of plane coordinate system (x)
    :param v: Second axis of plane coordinate system (y)
    :param n: Normal vector of plane
    :return: 2d vector of point on plane
    Dimensions of vectors is not checked for faster execution.
    Origin of plane is assumed to be equal to global one.
    """
    jp = np.column_stack((u, v, n))
    p_proj = p - (p.dot(n) / n.dot(n)) * n
    p_trans = np.matmul(p_proj, jp)
    return Vector(p_trans[0], p_trans[1])


def angle2d(vec1: Vector, vec2: Vector, negative: bool = True):
    """
    Calculate angle between two 2d vectors
    :param vec1: First vector
    :param vec2: Second vector
    :param negative: Flag to allow negative Vectors (default: True)
    :return: Angle in degrees
    Dimension of vectors is not checked for faster execution
    """
    if negative:
        # Use atan2 function if negative angle is allowed
        alpha = np.arctan2(vec2[1], vec2[0]) - np.arctan2(vec1[1], vec1[0])
        alpha = alpha * 180. / np.pi
    else:
        # Use cosine relation for only positive angles 0 and 180°
        l1 = vec1.length
        l2 = vec2.length
        dot = 0
        for i in range(vec1.dim):
            dot += vec1[i] * vec2[i]
        alpha = np.arccos(dot / l1 / l2) * 180. / np.pi
    return alpha


def rotate_xyz(vector: Vector, angle_x: float = 0., angle_y: float = 0., angle_z: float = 0.):

    """
    Rotate a 3d-vector around the third (z) axis
    :param vector: Vector to rotate
    :param angle_x: Rotation angle around x-axis (in degrees)
    :param angle_y: Rotation angle around y-axis (in degrees)
    :param angle_z: Rotation angle around z-axis (in degrees)
    :return: Rotated 3d vector
    Dimension of vector is not checked for faster execution
    """
    vec = rotate_x(vector, angle_x)
    vec = rotate_y(vec, angle_y)
    vec = rotate_z(vec, angle_z)
    return vec


def project_ellipse(a: float, b: float,
                    ce: Vector, ne: Vector,
                    ue: Vector, ve: Vector,
                    npr: Vector,
                    up: Vector, vp: Vector):
    """
    Project an ellipse on a plane in 3d space
    Source: https://www.geometrictools.com/Documentation/ParallelProjectionEllipse.pdf

    :param vp: Second plane vector of projection plane
    :param up: First plane vector of projection plane
    :param ve: Second plane vector of ellipse plane
    :param ue: First plane vector of ellipse plane
    :param ne: Normal vector of ellipse plane
    :param ce: Origin point of ellipse
    :param a: Semi-major axis of ellipse
    :param b: Semi-minor axis of ellipse
    :param npr: Normal vector of projection plane
    :return: Tuple with both ellipsis semi-axis and angle
    """
    je = np.column_stack((ue, ve))
    jp = np.column_stack((up, vp))
    i3 = np.identity(3)
    _np = npr[np.newaxis]

    _a = np.matmul(np.matmul(
        jp.T, (i3 - (_np * _np.T) / np.matmul(_np, _np.T))), je)
    ainv = np.linalg.inv(_a)
    delta = np.array([[1., 0.], [0., a/b]])
    m = np.matmul(np.matmul(ainv.T, delta ** 2), ainv)

    d, r = np.linalg.eig(m)

    if d[0] == 0. or d[1] == 0.:
        raise ValueError('Division by zero!')
    d0 = a / np.sqrt(d[0])
    d1 = a / np.sqrt(d[1])

    axis = Vector(*np.matmul(r, Vector(1, 0)))
    angle = angle2d(Vector(1, 0), axis, negative=True)
    return d0, d1, angle
