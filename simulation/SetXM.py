import numpy as np


def SetXM(design, WL=None, index_Si=None, index_SiO2=None):

    if WL is None:
        WL = 500  # nm

    if design == 1:
        core_width = 0.0
        inner_width = 50  # nm Si
        outer_width = 4  # nm SiO2

    core_r = core_width
    inner_r = core_r + inner_width
    outer_r = inner_r + outer_width

    nm = 1.0
    x = 2.0 * np.pi * np.array([inner_r, outer_r], dtype=np.float64) / WL
    m = np.array([index_Si, index_SiO2], dtype=np.complex128) / nm
    
    
    return x, m, WL