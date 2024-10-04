from tqdm import tqdm
from calculator import calc_si_response, calc_sisio2_response
import concurrent.futures



def wrap_data(
    material_type: str,
    wavelength: list,
    response: list
) -> dict:
    return {
        "type": material_type,
        "wl": wavelength,
        "resp": response
    }

def thread_si_calc(
    sample_radius,
    min_wl_si,
    max_wl_si,
    sim_points
    ):
    sample_dict_list = []
    for radius in tqdm(sample_radius, desc="Simulation for si"):
            wl, response = calc_si_response(min_wl_si, max_wl_si, sim_points, radius)
            sample = wrap_data("si", wl.tolist(), response)
            sample_dict_list.append(sample)
            
    return sample_dict_list


def thread_sisio2_calc(
    sample_radius_in,
    sample_radius_out,
    min_wl_sisio2,
    max_wl_sisio2,
    sim_points
):
    sample_dict_list = []
    for inner_rad in tqdm(sample_radius_in, desc="Simulation loop for inner radius"):
        for outter_rad in tqdm(sample_radius_out, desc="Simulation loop for outter radius"):
            wl, response = calc_sisio2_response(min_wl_sisio2, max_wl_sisio2, sim_points, inner_rad, outter_rad)
            sample = wrap_data("sisio2", wl.tolist(), response)
            sample_dict_list.append(sample)
            
    return sample_dict_list


def start_threading(
    params,
    args
):
    sample_data_dict = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_simulation = {}

        # Submit si simulation tasks
        if args.material_type in ["si", "both"] and "sample_radius" in params:
            for sample_chunk in params["sample_radius"]:
                future = executor.submit(thread_si_calc, sample_chunk, args.min_wl_si, args.max_wl_si, args.sim_points)
                future_to_simulation[future] = "si"

        # Submit sisio2 simulation tasks
        if args.material_type in ["sisio2", "both"] and "sample_radius_inner" in params and "sample_radius_outer" in params:
            for inner_chunk, outer_chunk in zip(params["sample_radius_inner"], params["sample_radius_outer"]):
                future = executor.submit(thread_sisio2_calc, inner_chunk, outer_chunk, args.min_wl_sisio2, args.max_wl_sisio2, args.sim_points)
                future_to_simulation[future] = "sisio2"

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_simulation):
            result = future.result()
            sample_data_dict.extend(result)

    return sample_data_dict
    