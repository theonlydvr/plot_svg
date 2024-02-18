from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt

from plot_svg import plot_svg


@image_comparison(baseline_images=['dukechain'], remove_text=True,
                  extensions=['png'], style='mpl20')
def test_duke():
    fig, ax = plt.subplots()
    plot_svg('tests/img/dukechain.svg', ax=ax)
    ax.invert_yaxis()
    ax.axis('equal')
