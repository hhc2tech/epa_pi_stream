'''
## 2. run_simulation.py

### Purpose:
Execute hydraulic simulation using WNTR from .inp file

### Functions:
- run_simulation_with_wntr(inp_path): Run extended period simulation
- export_csv(): Export simulation results (pressure, flowrate) to CSV files

### Role:
- Core simulation module
- Extract detailed time-series results (pressure & flowrate)
- Provide ready-to-use CSV exports for reporting
'''
# run_simulation.py
# Module: Run EPANET hydraulic simulation using WNTR

import wntr
import pandas as pd

# Run EPANET simulation using WNTR API
def run_simulation_with_wntr(inp_path):
    """
    Execute hydraulic simulation from .inp file
    Return pressure and flowrate time series data
    """
    wn = wntr.network.WaterNetworkModel(inp_path)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    # Extract result time series
    pressure_df = results.node['pressure']    # Pressure at nodes over time (m)
    flow_df = results.link['flowrate']        # Flowrate in pipes over time (m3/s)

    return pressure_df, flow_df, wn

# Export pressure and flowrate results to CSV
def export_csv(pressure_df, flow_df, prefix=""):
    """
    Export simulation results DataFrame to CSV files for reporting
    """
    pressure_path = f"{prefix}pressure.csv"
    flow_path = f"{prefix}flowrate.csv"

    pressure_df.to_csv(pressure_path)
    flow_df.to_csv(flow_path)

    return pressure_path, flow_path

