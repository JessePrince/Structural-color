#!/bin/bash

python simulation/run_simulation.py \
    --num_samples 1000 \
    --save_dir simulation/data_output \
    --material_type both \
    --sim_points 200 \
    --min_wl_si 450 \
    --max_wl_si 800 \
    --min_wl_sisio2 300 \
    --max_wl_sisio2 600 \
    --min_r_si 20 \
    --max_r_si 200 \
    --min_w_sisio2_inner 50 \
    --max_w_sisio2_inner 100 \
    --min_w_sisio2_outer 1 \
    --max_w_sisio2_outer 4 \
    --si_profile_dir simulation/Si_Green_2008.txt \
    --sio2_profile_dir simulation/SiO2_Gao.txt 