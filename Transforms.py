import matplotlib.pyplot as plt
import matplotlib.transforms as trf


def translate(svg, x, y):
    for obj in svg.values():
        if isinstance(obj, dict):
            translate(obj, x, y)
        else:
            obj.set_transform(trf.Affine2D().translate(x, y) + plt.gca().transData)


def scale(svg, sx, sy):
    for obj in svg.values():
        if isinstance(obj, dict):
            scale(obj, sx, sy)
        else:
            obj.set_transform(trf.Affine2D().scale(sx, sy) + plt.gca().transData)
