from canvas import OrbitCanvas
import datetime
import planets
import pathlib


def create_picture(phi: float, psi: float, theta: float, zoom: float,
                   time: datetime.datetime, path: str = './plots'):
    """
    Function to create an image of planets and orbits
    :param phi: Viewing angle (x) in degrees
    :param psi: Viewing angle (y) in degrees
    :param theta: Viewing angle (z) in degrees
    :param zoom: Zoom value between 1.0 and 0.
    :param time: datedime.datetime object
    :param path: Path for saving
    :return: String name of created image file
    """
    canvas = OrbitCanvas(time=time)
    for planet in dir(planets):
        if planet[0].islower():
            canvas.add_planet(planets.__dict__[planet])

    canvas.set_phi(phi)
    canvas.set_psi(psi)
    canvas.set_theta(theta)
    canvas.set_zoom(zoom)

    save_name = time.strftime('%Y%m%d_%H%M%S')
    canvas.fig.savefig(f'{path:s}/{save_name:s}.png')
    return save_name


if __name__ == '__main__':
    # If wanted, existing plots can be deleted to keep only the most recent one
    # path = pathlib.Path('./plots')
    # plots = [p.name for p in path.iterdir()]
    # for plot in plots:
    #     (path / plot).unlink()

    create_picture(phi=-70., psi=0., theta=0., zoom=.4,
                   time=datetime.datetime.now())



