# @ Copyright Fan Zhang, Hao Li, 2024
# Project Structural Color / ColorNet

import os
import sys
sys.path.append(os.getcwd())

import threading
from simulation.calculator import calc_si_response, calc_sisio2_response
import argparse
from pathlib import Path
import json
from tqdm import tqdm


def parse_aruments():
    parser = argparse.ArgumentParser('Run dataset simulation', add_help=False)
    parser.add_argument('--num_samples', default=1e6, type=float)
    parser.add_argument('--save_dir', default='data_output', type=str)
    parser.add_argument('--is_multithreading', default=True, type=bool)
    parser.add_argument('--material_type', default='si', choices=('si', 'sisio2', 'both'))
    parser.add_argument('--sim_points', default=200, type=int)
    parser.add_argument('--min_wl_si', default=450, type=int)
    parser.add_argument('--max_wl_si', default=800, type=int)
    parser.add_argument('--min_wl_sisio2', default=300, type=int)
    parser.add_argument('--max_wl_sisio2', default=600, type=int)
    parser.add_argument('--min_r_si', default=20, type=int)
    parser.add_argument('--max_r_si', default=200, type=int)
    parser.add_argument('--min_w_sisio2_inner', default=50, type=int)
    parser.add_argument('--max_w_sisio2_outer', default=4, type=int)
    
    
    return parser


def wrap_data(
    material_type: str,
    wavelength: list,
    response: list
) -> dict:
    sample_dict = {
        "type": material_type,
        "wl": wavelength,
        "resp": response
    }
    
    return sample_dict


def main(args):
    save_dir = Path(args.save_dir).mkdir(exist_ok=True, parents=True)
    num_cpu = os.cpu_count()
    
    sample_dict_list = []
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run dataset simulation', parents=[parse_aruments()])
    args = parser.parse_args()
    
    main(args)