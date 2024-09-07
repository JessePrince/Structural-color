import threading
from simulation.calculator import calc_si_response, calc_sisio2_response
import argparse


def parse_aruments():
    parser = argparse.ArgumentParser('Run dataset simulation', add_help=False)
    parser.add_argument('--num_samples', default=1e-4, type=float)
    parser.add_argument('--save_dir', default='data_output', type=str)
    parser.add_argument('--is_multithreading', default=True, type=bool)
    parser.add_argument('--material_type', default='si', choices=('si', 'sisio2', 'both'))
    parser.add_argument('--sim_points', default=200, type=int)
    parser.add_argument('--min_wl_si', default=450, type=int)
    parser.add_argument('--max_wl_si', default=800, type=int)
    parser.add_argument('--min_wl_sisio2', default=300, type=int)
    parser.add_argument('--max_wl_sisio2', default=600, type=int)
    
    
    return parser


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run dataset simulation', parents=[parse_aruments()])
    args = parser.parse_args()
    
    