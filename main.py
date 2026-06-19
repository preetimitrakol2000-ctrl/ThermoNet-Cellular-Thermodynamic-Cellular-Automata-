import ctypes
import os
import sys
import time
from feature_extractor import FeatureExtractor
from predictor import ThermalStabilityPredictor

def compile_thermal_backend():
    """Compiles the C cellular automata framework."""
    print("[*] Compiling backend thermodynamic simulation engine...")
    ext = "dll" if sys.platform.startswith("win") else "so"
    os.system(f"gcc -shared -o thermo_sim.{ext} -fPIC thermo_sim.c")
    return f"./thermo_sim.{ext}"

def main():
    lib_path = compile_thermal_backend()
    thermo_lib = ctypes.CDLL(lib_path)
    
    # Grid dimensions (Must match values declared in C)
    GRID_SIZE = 100 # 10x10 matrix
    c_double_array = ctypes.c_double * GRID_SIZE
    
    thermo_lib.diffuse_heat.argtypes = [c_double_array, c_double_array, ctypes.c_double]
    thermo_lib.enforce_boundaries.argtypes = [c_double_array, ctypes.c_double]

    # Initialize thermal grids (0.0°C everywhere initially)
    current_grid = c_double_array(*[0.0] * GRID_SIZE)
    next_grid = c_double_array(*[0.0] * GRID_SIZE)
    
    # Material Diffusivity coefficient (e.g., Copper vs Steel profile)
    alpha = 0.125 
    heat_source = 100.0 # Heat source at boundary edge
    
    predictor = ThermalStabilityPredictor()
    
    print("[*] Executing Cellular Automata thermal updates across time states...")
    
    # Simulate 5 discrete time steps
    for t in range(1, 6):
        thermo_lib.enforce_boundaries(current_grid, heat_source)
        thermo_lib.diffuse_heat(current_grid, next_grid, ctypes.c_double(alpha))
        
        # Swap grid references (Double Buffering memory pattern)
        current_grid, next_grid = next_grid, current_grid
        
        # Extract features and pass them into the ML pipeline
        metrics = FeatureExtractor.calculate_thermal_metrics(current_grid, 10, 10)
        predicted_time = predictor.predict_time_to_equilibrium(metrics["mean_temp"], metrics["thermal_variance"])
        
        print(f" -> Iteration {t} | Grid Mean Temp: {metrics['mean_temp']:.2f}°C | Est. Equilibrium Time: {predicted_time:.2f}s")
        time.sleep(0.1)

    print("\n[+] Simulation and analysis completed successfully.\n")

if __name__ == "__main__":
    main()
