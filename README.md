
# EPA Stream App

## Project Overview

This project provides a web-based tool for modeling and simulating a water distribution network using EPANET API, WNTR, and Streamlit Cloud. The tool allows for flexible input of network data, running hydraulic simulations, and visualizing results.

## Problem Statement

- Water Supply Pumping Station: 3600 m³/h = 1.0 m³/s.
- Main Pipe D200, length 2000m.
- 6 Branch Pipes D90, each ~100-300m long.
- Each D90 branch supplies 3-5 sub-branches D22, D34, each ~50-150m long.
- All end nodes are water consumption points.

## Project Structure

### Modules

| File               | Functionality                            |
|-------------------|-------------------------------------------|
| table_network.py   | Data input (manual, CSV, XLSX, INP), validation, and network creation |
| run_simulation.py  | Running simulation using WNTR, exporting results |
| view_results.py    | Viewing results on Map, Graph, and Table |
| test_run.py        | Quick test script to verify simulation run |

### Sample Data

- sample_nodes.csv - Node data
- sample_pipes.csv - Pipe data
- sample_demands.csv - Demand data
- sample_epanet_data.xlsx - Excel file with 3 sheets (node, pipe, demand)

### Requirements

Libraries used:
- streamlit
- pandas
- plotly
- wntr
- epanettools
- openpyxl
- xlsxwriter
- graphviz

## Results

- Automatic network data generation based on requirements.
- Export INP file for EPANET.
- Simulation results for pressure and flowrate.
- Visualization of network on map.
- View results as dynamic graph and table.
- Export results as CSV.

## Usage

1. Clone the repository or upload files to Streamlit Cloud.
2. Install requirements.
3. Run `streamlit run app.py`.
4. Input data and run simulation.
5. View and export results.

