'''' 1. table_network.py

### Purpose:
Manage network input data for EPANET modeling.

### Functions:
- load_xlsx(): Load data from Excel (3 sheets: node, pipe, demand)
- load_csv(): Load data from 3 CSV files
- parse_inp_file(): Parse existing EPANET .inp file into DataFrames
- validate_network(): Check network logic (duplicate IDs, isolated nodes, invalid pipes)
- create_network(): Generate EPANET network object for export
- draw_graph(): Draw network using Graphviz

### Role:
- Handle all user input (manual / import)
- Validate data structure
- Export .inp file for simulation
'''
# Module: Data Input, Validation, and Network Creation for EPANET

import streamlit as st
import pandas as pd
from epanettools.epanettools import Network, EPANetSimulation
from graphviz import Digraph
import tempfile

# Load network data from Excel file (3 sheets)
def load_xlsx(file):
    xls = pd.ExcelFile(file)
    nodes = pd.read_excel(xls, 'node')
    pipes = pd.read_excel(xls, 'pipe')
    demands = pd.read_excel(xls, 'demand')
    return nodes, pipes, demands

# Load network data from 3 CSV files
def load_csv(files_dict):
    nodes = pd.read_csv(files_dict['node'])
    pipes = pd.read_csv(files_dict['pipe'])
    demands = pd.read_csv(files_dict['demand'])
    return nodes, pipes, demands

# Parse EPANET .inp file to DataFrames
def parse_inp_file(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".inp") as tmp:
        tmp.write(file.read())
        tmp.flush()
        sim = EPANetSimulation(tmp.name)

    nodes_data = []
    pipes_data = []
    demands_data = []

    for node in sim.network.nodes:
        nodes_data.append([
            'tank' if node.node_type == 'Tank' else 'node',
            node.id,
            0, 0, node.elevation
        ])

    for link in sim.network.links:
        if link.link_type == 'Pipe':
            pipes_data.append([
                link.id, link.start_node.id, link.end_node.id,
                link.length, link.diameter, link.roughness
            ])

    for j in sim.network.junctions:
        demands_data.append([j.id, j.base_demand])

    return (
        pd.DataFrame(nodes_data, columns=['type', 'id', 'x', 'y', 'elevation']),
        pd.DataFrame(pipes_data, columns=['id', 'from', 'to', 'length', 'diameter', 'roughness']),
        pd.DataFrame(demands_data, columns=['node_id', 'demand (m3/s)'])
    )

# Validate network logic: Check ID duplicates, isolated nodes, missing connections
def validate_network(nodes_df, pipes_df, demands_df):
    errors = []
    suggestions = []

    node_ids = nodes_df['id'].dropna().tolist()
    pipe_ids = pipes_df['id'].dropna().tolist()
    demand_ids = demands_df['node_id'].dropna().tolist()

    duplicate_nodes = nodes_df['id'][nodes_df['id'].duplicated()]
    if not duplicate_nodes.empty:
        errors.append(f"Duplicate node IDs: {', '.join(duplicate_nodes.unique())}")
        suggestions.append("Remove or rename duplicate node IDs.")

    duplicate_pipes = pipes_df['id'][pipes_df['id'].duplicated()]
    if not duplicate_pipes.empty:
        errors.append(f"Duplicate pipe IDs: {', '.join(duplicate_pipes.unique())}")
        suggestions.append("Ensure each pipe ID is unique.")

    for _, row in pipes_df.iterrows():
        if row['from'] not in node_ids:
            errors.append(f"Pipe {row['id']} connects from unknown node '{row['from']}'")
            suggestions.append(f"Add node '{row['from']}' to node table.")
        if row['to'] not in node_ids:
            errors.append(f"Pipe {row['id']} connects to unknown node '{row['to']}'")
            suggestions.append(f"Add node '{row['to']}' to node table.")

    for node in demand_ids:
        if node not in node_ids:
            errors.append(f"Demand specified at non-existent node '{node}'")
            suggestions.append(f"Check demand node '{node}' or add it to node table.")

    connected = set(pipes_df['from']).union(set(pipes_df['to']))
    isolated = [n for n in node_ids if n not in connected and nodes_df[nodes_df['id'] == n]['type'].values[0] != 'tank']
    if isolated:
        errors.append(f"Isolated nodes with no connected pipes: {', '.join(isolated)}")
        suggestions.append(f"Connect isolated nodes with pipes.")

    return errors, suggestions

# Create EPANET network object from DataFrames
def create_network(nodes_df, pipes_df, demands_df):
    net = Network()
    for _, row in nodes_df.iterrows():
        if row['type'] == 'tank':
            net.addTank(row['id'], row['x'], row['y'], row['elevation'])
        else:
            net.addNode(row['id'], row['x'], row['y'], row['elevation'])
    for _, row in pipes_df.iterrows():
        net.addPipe(row['id'], row['from'], row['to'], row['length'], row['diameter'], row['roughness'])
    for _, row in demands_df.iterrows():
        if pd.notna(row['node_id']):
            net.addDemand(row['node_id'], row['demand (m3/s)'], 'BASE')
    return net

# Draw network graph using Graphviz
def draw_graph(pipes_df):
    dot = Digraph()
    for _, row in pipes_df.iterrows():
        dot.edge(row['from'], row['to'], label=f"{row['id']} ({row['diameter']}mm)")
    return dot
