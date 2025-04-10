'''
4. test_run.py

### Purpose:
Quick testing tool for developers / engineers

### Workflow:
- Run simulation from a given .inp file
- Show summary statistics of pressure & flow
- Export results to CSV for verification

### Role:
- Validate code correctness
- Provide example execution for new users
- Easy integration testing
'''
# test_run.py
# Module: Quick Testing Script for EPANET Simulation

from run_simulation import run_simulation_with_wntr, export_csv
import os

# Define sample input file (generated from network table or existing file)
inp_file = "sample_network.inp"  # Make sure this file exists in your working directory

# Check if file exists
if not os.path.exists(inp_file):
    print(f"Input file '{inp_file}' not found. Please generate or provide it before running test.")
else:
    print("Running EPANET Simulation using WNTR...")

    # Run simulation
    pressure_df, flow_df, wn = run_simulation_with_wntr(inp_file)

    # Display quick statistics summary
    print("\n--- Pressure Summary (m) ---")
    print(pressure_df.describe())

    print("\n--- Flowrate Summary (m3/s) ---")
    print(flow_df.describe())

    # Export results to CSV files
    pressure_path, flow_path = export_csv(pressure_df, flow_df, prefix="test_")

    print(f"\nResults exported successfully:")
    print(f"Pressure data -> {pressure_path}")
    print(f"Flowrate data -> {flow_path}")

