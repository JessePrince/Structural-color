# @ Copyright Fan Zhang, Hao Li, 2024
# Project Structural Color / ColorNet

from scattnlay import scattnlay, scattcoeffs
import numpy as np


def SetXM(
    inner_width: int,
    outer_width: int,
    WL: int, 
    index_Si: float | int, 
    index_SiO2: float | int
) -> tuple[np.ndarray, np.ndarray]:

    inner_r = inner_width
    outer_r = inner_r + outer_width

    nm = 1.0
    x = 2.0 * np.pi * np.array([inner_r, outer_r], dtype=np.float64) / WL
    m = np.array([index_Si, index_SiO2], dtype=np.complex128) / nm
    
    
    return x, m


def calc_si_response(
    from_wl: int,
    to_wl: int,
    wl_points: int,
    core_r: int
) -> tuple[np.ndarray, list]:
    """Calculate response of Si core, with given radius and wavelength profile

    Args:
        from_wl (int): Starting wavelength
        to_wl (int): Ending wavelength
        wl_points (int): Points used for discret calculation

    Returns:
        tuple[np.ndarray, list]: wavelength and response(scattering cross section), shape of wl_points
        
    Examples:
    
        >>> from_wl = 450,
        >>> to_wl = 800,
        >>> wl_points = 200,
        >>> core_r = 75,
        >>> wls, response = calc_si_response(from_wl, to_wl, wl_points, core_r)

    """
    # Load data from Si.txt
    data = np.loadtxt('Si.txt', skiprows=1)  # skip the header row
    wavelength_data = data[:, 0]
    real_data = data[:, 1]
    imag_data = data[:, 2]

    WLs = np.linspace(from_wl, to_wl, wl_points)


    # Interpolate the real and imaginary parts for the given wavelengths
    real_interp = np.interp(WLs, wavelength_data, real_data)
    imag_interp = np.interp(WLs, wavelength_data, imag_data)

    # Calculate the complex refractive index
    index_NP = np.sqrt(real_interp + 1j * imag_interp)

    x = np.ones((1), dtype=np.float64)
    m = np.ones((1), dtype=np.complex128)

    Qsca_vec = []
    core_r_vec = []
    an_vec = []
    bn_vec = []

    for i, WL in enumerate(WLs):
        x[0] = 2.0 * np.pi * core_r / WL
        m[0] = index_NP[i]  # Use interpolated index_NP for this wavelength
        _, _, Qsca, _, _, _, _, _, _, _ = scattnlay(
            np.array(x), np.array(m),
            mp=True
        )
        print(np.array([Qsca]))
        _, an, bn = scattcoeffs(x, m, 24)
        Qsca_vec.append(Qsca)
        core_r_vec.append(core_r)
        an_vec.append(np.abs(an)[0])
        bn_vec.append(np.abs(bn)[0])

    an_vec = np.array(an_vec)
    bn_vec = np.array(bn_vec)
    
    return WLs, Qsca_vec


def calc_sisio2_response(
    from_wl: int,
    to_wl: int,
    wl_points: int,
    inner_width: int,
    outer_width: int
) -> tuple[np.ndarray, list]:
    """Calculate response of Si-SiO2 core-shell structure

    Args:
        from_wl (int): Starting wavelength
        to_wl (int): Ending wavelength
        wl_points (int): points of the discret calculation
        inner_width (int): inner width(Si) of the structure
        outer_width (int): outer width(SiO2) of the structure

    Returns:
        tuple[np.ndarray, list]: wavelength and response(scattering cross section), shape of wl_points
        
    Examples:
        >>> from_wl = 300
        >>> to_wl = 600
        >>> wl_points = 200
        >>> inner_width = 50
        >>> outer_width = 4
        >>> wl, response = calc_sisio2_response(from_wl, to_wl, wl_points, inner_width, outer_width)
    """
    # Load data from Si_Green_2008.txt
    data_Si = np.loadtxt('Si_Green_2008.txt', skiprows=1)  # skip the header row
    wavelength_data_Si = data_Si[:, 0] * 1e3  # 转换为nm
    real_data_Si = data_Si[:, 1]
    imag_data_Si = data_Si[:, 2]

    # Load data from SiO2_Gao_2008.txt
    data_SiO2 = np.loadtxt('SiO2_Gao.txt', skiprows=1)  # skip the header row
    wavelength_data_SiO2 = data_SiO2[:, 0] * 1e3  # 转换为nm
    real_data_SiO2 = data_SiO2[:, 1]
    imag_data_SiO2 = data_SiO2[:, 2]

    WLs = np.linspace(from_wl, to_wl, wl_points)

    # Interpolate Si refractive index
    real_interp_Si = np.interp(WLs, wavelength_data_Si, real_data_Si)
    imag_interp_Si = np.interp(WLs, wavelength_data_Si, imag_data_Si)
    index_Si = real_interp_Si + 1j * imag_interp_Si

    # Interpolate SiO2 refractive index
    real_interp_SiO2 = np.interp(WLs, wavelength_data_SiO2, real_data_SiO2)
    imag_interp_SiO2 = np.interp(WLs, wavelength_data_SiO2, imag_data_SiO2)
    index_SiO2 = real_interp_SiO2 + 1j * imag_interp_SiO2


    Qsca_vec = []

    
    for i, WL in enumerate(WLs):
        current_index_Si = index_Si[i]  
        current_index_SiO2 = index_SiO2[i]  
        x, m= SetXM(inner_width, outer_width, WL=WL, index_Si=current_index_Si, index_SiO2=current_index_SiO2)

        
        _, _, Qsca, _, _, _, _, _, _, _ = scattnlay(np.array(x), np.array(m))

        Qsca_vec.append(Qsca)

    return WLs, Qsca_vec

