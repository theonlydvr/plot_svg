from typing import List, Union, Dict

import matplotlib.pyplot as plt
import svgelements
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import matplotlib.collections as mcoll


def plot_svg(path: str, ignore_ids: List[str] = None, ax: plt.Axes = None) -> mcoll.PatchCollection:
    """ Plots the provided SVG file using a variety of matplotlib Patch objects

    Parameters
    ----------
    path : str
        the path to the SVG file
    ignore_ids : List[str]
        a list of SVG IDs that should not be plotted
    ax : plt.Axes
        the axes in which the SVG shapes will be plotted

    Returns
    -------
    mcoll.PatchCollection
        all SVG shapes represented as a PatchCollection
    """
    if ax is None:
        ax = plt.gca()
    if ignore_ids is None:
        ignore_ids = []
    doc = svgelements.SVG.parse(path)
    patches = plot_group(doc, ignore_ids)
    pc = mcoll.PatchCollection(patches, match_original=True)
    ax.add_collection(pc)
    return pc


def plot_func(obj: svgelements.SVGElement, ignore_ids: List[str]) -> List[mpatches.Patch]:
    """ Calls the appropriate plotting function depending on the provided SVGElement

    Parameters
    ----------
    obj : svgelements.SVGElement
        the SVGElement that should be plotted
    ignore_ids : List[str]
        a list of SVG IDs that should not be plotted

    Returns
    -------
    List[mpatches.Patch]
        list of new patches to be added to the plot
    """
    if isinstance(obj, svgelements.SVG) or isinstance(obj, svgelements.Group):
        return plot_group(obj, ignore_ids)
    elif isinstance(obj, svgelements.Path):
        return [plot_path(obj)]
    elif isinstance(obj, svgelements.Circle):
        return [plot_circle(obj)]
    elif isinstance(obj, svgelements.Ellipse):
        return [plot_ellipse(obj)]
    elif isinstance(obj, svgelements.Polygon):
        return [plot_polygon(obj)]
    elif isinstance(obj, svgelements.Polyline):
        return [plot_polygon(obj, closed=False)]
    elif isinstance(obj, svgelements.Rect):
        return [plot_rect(obj)]
    else:
        return []


def plot_group(group: svgelements.Group, ignore_ids: List[str]) -> List[mpatches.Patch]:
    """ Gets all shapes in an SVG Group as Patches

    Parameters
    ----------
    group : svgelements.Group
        the SVG Group to plot
    ignore_ids : List[str]
        a list of SVG IDs that should not be plotted

    Returns
    -------
    List[mpatches.Patch]
        list of new patches to be added to the plot
    """
    grp = []
    for obj in group:
        if obj.id not in ignore_ids:
            grp.extend(plot_func(obj, ignore_ids))
    return grp


def plot_path(path: svgelements.Path) -> mpatches.PathPatch:
    """ Generates a PathPatch for the provided SVG Path

    Parameters
    ----------
    path : svgelements.Path
        the SVG Path to plot

    Returns
    -------
    mpatches.PathPatch
        the SVG Path represented as a matplotlib PathPatch
    """
    vertices = []
    codes = []
    for seg in path:
        if isinstance(seg, svgelements.Move):
            vertices.append((seg.end.x, seg.end.y))
            codes.append(mpath.Path.MOVETO)
        elif isinstance(seg, svgelements.CubicBezier):
            if seg.control1 is not None:
                vertices.append((seg.control1.x, seg.control1.y))
            if seg.control2 is not None:
                vertices.append((seg.control2.x, seg.control2.y))
            vertices.append((seg.end.x, seg.end.y))
            if seg.control1 is not None and seg.control2 is not None:
                codes.extend([mpath.Path.CURVE4] * 3)
            else:
                codes.extend([mpath.Path.CURVE3] * 2)
        elif isinstance(seg, svgelements.QuadraticBezier):
            vertices.append((seg.control.x, seg.control.y))
            vertices.append((seg.end.x, seg.end.y))
            codes.extend([mpath.Path.CURVE3] * 2)
        elif isinstance(seg, svgelements.Close):
            vertices.append((vertices[-1][0], vertices[-1][1]))
            codes.append(mpath.Path.CLOSEPOLY)
        elif isinstance(seg, svgelements.Line):
            vertices.append((seg.end.x, seg.end.y))
            codes.append(mpath.Path.LINETO)
        elif isinstance(seg, svgelements.Arc):
            # PathPatch does not natively support arcs so they must be approximated with cubic Bezier curves
            for crv in seg.as_cubic_curves():
                vertices.append((crv.control1.x, crv.control1.y))
                vertices.append((crv.control2.x, crv.control2.y))
                vertices.append((crv.end.x, crv.end.y))
                codes.extend([mpath.Path.CURVE4] * 3)

    pp = mpatches.PathPatch(mpath.Path(vertices, codes), **get_attributes(path))
    return pp


def plot_circle(circle: svgelements.Circle) -> mpatches.Circle:
    """ Generates a Circle Patch for the provided SVG Circle

    Parameters
    ----------
    circle : svgelements.Circle
        the SVG Circle to plot

    Returns
    -------
    mpatches.Circle
        the SVG Circle represented as a matplotlib Circle
    """
    cp = mpatches.Circle((circle.implicit_center.x, circle.implicit_center.y), radius=circle.implicit_rx,
                         **get_attributes(circle))
    return cp


def plot_ellipse(ellipse: svgelements.Ellipse) -> mpatches.Ellipse:
    """ Generates an Ellipse Patch for the provided SVG Ellipse

    Parameters
    ----------
    ellipse : svgelements.Ellipse
        the SVG Ellipse to plot

    Returns
    -------
    mpatches.Ellipse
        the SVG Ellipse represented as a matplotlib Ellipse
    """
    ep = mpatches.Ellipse(ellipse.implicit_center, width=ellipse.implicit_rx * 2, height=ellipse.implicit_ry * 2,
                          angle=ellipse.rotation.as_degrees, **get_attributes(ellipse))
    return ep


def plot_polygon(polygon: Union[svgelements.Polygon, svgelements.Polyline], closed=True) -> mpatches.Polygon:
    """ Generates a Polygon Patch for the provided SVG Polygon or Polyline

    Parameters
    ----------
    polygon : Union[svgelements.Polygon, svgelements.Polyline]
        the SVG Polygon or Polyline to plot
    closed : bool
        indicates if the polygon should be closed (True for Polygon, False for Polyline)

    Returns
    -------
    mpatches.Polygon
        the SVG Polygon or Polyline represented as a matplotlib Polygon
    """
    points = [(p.x, p.y) for p in polygon.points]
    pp = mpatches.Polygon(points, closed=closed, **get_attributes(polygon))
    return pp


def plot_rect(rect: svgelements.Rect) -> mpatches.Rectangle:
    """ Generates a Rectangle Patch for the provided SVG Rectangle

    Parameters
    ----------
    rect : svgelements.Rectangle

    Returns
    -------
    mpatches.Rectangle
        the SVG Rectangle represented as a matplotlib Rectangle
    """
    rp = mpatches.Rectangle((rect.implicit_x, rect.implicit_y), width=rect.implicit_width, height=rect.implicit_height,
                            angle=rect.rotation.as_degrees, **get_attributes(rect))
    return rp


def get_attributes(shp: svgelements.Shape) -> Dict:
    """ Gets various visual attributes of the SVG shape for generating the Patch. Currently handles the following SVG
    attributes: fill, stroke, fill-opacity, stroke-opacity, opacity, stroke-width, stroke-dashoffset, stroke-dasharray,
    stroke-linejoin, and stroke-linecap

    Parameters
    ----------
    shp : svgelements.Shape
        the SVG Shape for which to get attributes

    Returns
    -------
    Dict
        the attributes for this Shape represented as a dictionary
    """
    if 'stroke-dasharray' in shp.values:
        if shp.values['stroke-dasharray'] != 'none':
            ls = (float(shp.values['stroke-dashoffset']),
                  tuple(float(s) for s in shp.values['stroke-dasharray'].split(', ')))
        else:
            ls = '-'
    else:
        ls = '-'
    attributes = {'fill': True if shp.values['fill'] != 'none' else False,
                  'facecolor': shp.fill.hexa if shp.fill.value is not None else 'none',
                  'edgecolor': shp.stroke.hexa if shp.stroke.value is not None else 'none',
                  'alpha': float(shp.values['opacity']) if 'opacity' in shp.values else 1,
                  'linewidth': shp.stroke_width,
                  'linestyle': ls,
                  'joinstyle': shp.values['stroke-linejoin'] if 'stroke-linejoin' in shp.values else None,
                  'capstyle': shp.values['stroke-linecap'] if 'stroke-linecap' in shp.values else None}
    return attributes
