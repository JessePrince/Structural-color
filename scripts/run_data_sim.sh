#!/bin/bash

python simulation/run_simulation.py \
    --num_samples 10 \
    --save_dir data_output \
    --is_multithreading True \
    --material_type both \
    --sim_points 300 \
    --min_wl_si 450 \
    --max_wl_si 800 \
    --min_wl_sisio2 300 \
    --max_wl_sisio2 600 \
    