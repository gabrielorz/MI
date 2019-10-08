"""
Geometric utilities

Medical Images 2019- MUEI ETSEIB
"""
def compute_window_viewport_transform(window, width, height):
    """
    Returns a tuple (sx, sy, tx, ty) that represents the geometric transformation of rasterization
    """
    sx = width/window.width
    sy = - height/window.height
    tx = -sx*window.xmin
    ty = height -sy*window.ymin
    return (sx, sy, tx, ty)
