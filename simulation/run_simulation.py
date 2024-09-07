import threading
from simulation.calculator import calc_si_response, calc_sisio2_response
import argparse


def parse_aruments():
    parser = argparse.ArgumentParser('Run dataset simulation', add_help=False)
    parser.add_argument('--num_samples', default=1e-4, type=float)
    parser.add_argument('--save_dir', default='data_output', type=str)
    parser.add_argument('--is_multithreading', default=True, type=bool)
    parser.add_argument('--material_type', default='si', choices=('si', 'sisio2', 'both'))
    parser.add_argument('--wavelength_range', default=)
    
    return parser