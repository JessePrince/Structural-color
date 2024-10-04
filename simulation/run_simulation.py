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
import numpy as np
import simulation_engine


def parse_aruments():
    parser = argparse.ArgumentParser('Run dataset simulation', add_help=False)
    parser.add_argument('--num_samples', default=100, type=float)
    parser.add_argument('--save_dir', default='data_output', type=str)
    parser.add_argument('--is_multithreading', default=False, type=bool)
    parser.add_argument('--material_type', default='si', choices=('si', 'sisio2', 'both'))
    parser.add_argument('--sim_points', default=200, type=int)
    parser.add_argument('--min_wl_si', default=450, type=int)
    parser.add_argument('--max_wl_si', default=800, type=int)
    parser.add_argument('--min_wl_sisio2', default=300, type=int)
    parser.add_argument('--max_wl_sisio2', default=600, type=int)
    parser.add_argument('--min_r_si', default=20, type=int)
    parser.add_argument('--max_r_si', default=200, type=int)
    parser.add_argument('--min_w_sisio2_inner', default=50, type=int)
    parser.add_argument('--max_w_sisio2_inner', default=100, type=int)
    parser.add_argument('--min_w_sisio2_outer', default=1, type=int)
    parser.add_argument('--max_w_sisio2_outer', default=4, type=int)
    
    
    return parser

    
def main(args):
    save_dir = Path(args.save_dir)
    save_dir.mkdir(exist_ok=True, parents=True)
    
    num_cpu = os.cpu_count()
    
    params = {}

    # Handle sample radius based on material_type
    if args.material_type in ["si", "both"]:
        params["sample_radius"] = np.linspace(args.min_r_si, args.max_r_si, args.num_samples)

    if args.material_type in ["sisio2", "both"]:
        params["sample_radius_inner"] = np.linspace(args.min_w_sisio2_inner, args.max_w_sisio2_inner, args.num_samples // 2)
        params["sample_radius_outer"] = np.linspace(args.min_w_sisio2_outer, args.max_w_sisio2_outer, args.num_samples // 2)

    # Handle multithreading
    for key in params:
        params[key] = np.array_split(params[key], num_cpu)
    
    full_data_list = simulation_engine.start_threading(params, args)    
    
    with open(save_dir / f"{args.material_type}-{len(full_data_list)}-data.json", mode='w') as fp:
        json.dump(full_data_list, fp, indent=4)
        fp.close()
        
    print("Generation complete")
    print("Total num samples:", len(full_data_list))
    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run dataset simulation', parents=[parse_aruments()])
    args = parser.parse_args()
    main(args)
    