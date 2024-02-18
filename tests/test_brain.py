import numpy
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.transforms as trf

from plot_svg import plot_svg


@image_comparison(baseline_images=['brain'], remove_text=True,
                  extensions=['png'], style='mpl20')
def test_duke():
    fig, ax = plt.subplots()
    doc = plot_svg('tests/img/C1_80.svg', ax=ax)
    doc.set_transform(
        trf.Affine2D().translate(-539.875, -863.956) + trf.Affine2D().scale(1 / 56.756,
                                                                            1 / 56.756) + plt.gca().transData)
    xl = [-2.1, -2.37, -2.15, -1.25, -2.25, -2.55, -1.75, -1.4, -1.75, -1.5, -1.95, -1.45, -1.8, -2, -2.1, -1.9, -1.8,
          -1.8, -1.7, -1.6, -1.5, -1.85, -1.6, -1.45, -1.75, -2, -3.15, -3.4, -3.35, -3.25, -3, -3.2, -3.2, -3]
    yl = [5.95, 6.05, 5.6, 5.65, 5.95, 5.95, 5.9, 5.55, 3.9, 4.15, 3.95, 4.35, 3.85, 4.1, 3.95, 4.35, 4, 6.8, 7.05,
          7.25, 7.05, 7.1, 7.05, 6.95, 6.95, 7.1, 4.1, 4.25, 4.35, 4.2, 3.7, 4.8, 4.55, 4.2]
    xr = [1.6, 1.75, 1.54, 2.3, 1.6, 1.4, 1.35, 2, 1.45, 2.15, 2.15, 1.85, 1.75, 1.55, 1.65, 1.85, 1.95, 1.8, 1.75,
          1.65, 2.05, 1.45, 1.95, 2.1, 1.8, 1.8, 3.15, 3, 3.25, 3.35, 3, 3.25, 3.25, 2.8]
    yr = [5.8, 6.1, 5.85, 5.8, 5.95, 5.95, 6, 5.75, 4.4, 4.35, 4.25, 4.35, 4.15, 4.2, 3.95, 4.35, 4.2, 7, 6.9, 7.1,
          6.95, 6.95, 6.85, 7.25, 7.1, 7, 4, 4.45, 4.15, 4.45, 3.7, 4.6, 4.55, 4.4]
    locs = [*([0] * 8), *([1] * 9), *([2] * 9), *([3] * 8)]

    plt.scatter(x=xl, y=-numpy.asarray(yl), c=locs, edgecolors='black')
    plt.scatter(x=xr, y=-numpy.asarray(yr), c=locs, edgecolors='black')
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    plt.xlim(-8, 8)
    plt.ylim(-10, 0)
