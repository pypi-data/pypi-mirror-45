import numpy as np

a = np.array(((0, 0),
              (1, 0.5),
              (1, -0.5)))

def R(angle_deg):
    t = angle_deg / 180.0 * np.pi
    R = np.array(((np.cos(t), np.sin(t)),
                  (-np.sin(t), np.cos(t))))
    return R

def rotate(a, angle_deg):
    """Rotate anti-clockwise"""
    return np.dot(a, R(angle_deg))

def swapxy(a):
    """Swap x/y"""
    return np.fliplr(a)

def flipx(a):
    """Flip x"""
    T = np.array(((-1, 0),
                  (0, 1)))
    return np.dot(a, T)

def flipy(y):
    """Flip y"""
    T = np.array(((1, 0),
                  (0, -1)))
    return np.dot(a, T)
