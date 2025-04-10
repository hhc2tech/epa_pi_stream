# app.py
# Main Application to Run EPANET Simulation on Streamlit Cloud

import streamlit as st
import pandas as pd
from table_network import load_xlsx, load_csv, parse_inp_file, validate_network, create_network, draw_graph
from run_simulation import run_simulation_with_wntr, export_csv
from view_results import show_pipe_pressure_statistics, show_network_map, show_results_graph, show_results_table

st.set_page_config(page_title="EPANET Cloud Simulation", layout="wide")
st.title("EPANET Water Distribution Network Simulation")

st.sidebar.header("Data Input Options")
data_source = st.sidebar.selectbox("Select Data Source", ["Sample Data", "Upload XLSX", "Upload CSV", "Upload INP"])

# Data Loading
if data_source == "Sample Data":
    nodes = pd.read_csv("sample_nodes.csv")
    pipes = pd.read_csv("sample_pipes.csv")
    demands = pd.read_csv("sample_demands.csv")
elif data_source == "Upload XLSX":
    uploaded_file = st.sidebar.file_uploader("Upload XLSX File", type=["xlsx"])
    if uploaded_file:
        nodes, pipes, demands = load_xlsx(uploaded_file)
elif data_source == "Upload CSV":
    uploaded_nodes = st.sidebar.file_uploader("Upload Nodes CSV", type=["csv"])
    uploaded_pipes = st.sidebar.file_uploader("Upload Pipes CSV", type=["csv"])
    uploaded_demands = st.sidebar.file_uploader("Upload Demands CSV", type=["csv"])
    if uploaded_nodes and uploaded_pipes and uploaded_demands:
        files = {"node": uploaded_nodes, "pipe": uploaded_pipes, "demand": uploaded_demands}
        nodes, pipes, demands = load_csv(files)
elif data_source == "Upload INP":
    uploaded_inp = st.sidebar.file_uploader("Upload INP File", type=["inp"])
    if uploaded_inp:
        nodes, pipes, demands = parse_inp_file(uploaded_inp)

# Data Display & Validation
if 'nodes' in locals():
    st.subheader("Network Data - Nodes")
    st.dataframe(nodes)

    st.subheader("Network Data - Pipes")
    st.dataframe(pipes)

    st.subheader("Network Data - Demands")
    st.dataframe(demands)

    errors, suggestions = validate_network(nodes, pipes, demands)
    if errors:
        st.error("Data Validation Errors:")
        for e in errors:
            st.write(e)
    else:
        st.success("No Data Errors Found.")

        graph = draw_graph(pipes)
        st.graphviz_chart(graph)

        net = create_network(nodes, pipes, demands)

        if st.button("Export INP File"):
            net.writeInputFile("generated_network.inp")
            with open("generated_network.inp", "rb") as f:
                st.download_button("Download INP File", f, file_name="generated_network.inp")

        if st.button("Run Simulation"):
            pressure_df, flow_df, wn = run_simulation_with_wntr("generated_network.inp")
            st.success("Simulation Completed.")

            st.subheader("Select Pipes to View Pressure Statistics")
            selected_pipes = st.multiselect("Select Pipes", pipes['id'].unique())

            if selected_pipes:
                show_pipe_pressure_statistics(pressure_df, wn, selected_pipes)

            st.subheader("View Pressure on Map")
            timestep = st.slider("Select Timestep", 0, len(pressure_df)-1, 0)
            show_network_map(pressure_df, wn, timestep)

            st.subheader("View Results - Graph")
            selected_nodes = st.multiselect("Select Nodes for Graph", nodes['id'].unique())
            if selected_nodes:
                show_results_graph(pressure_df, selected_nodes)

            st.subheader("View Results - Table")
            show_results_table(pressure_df, selected_nodes)

            export_csv(pressure_df, flow_df, prefix="final_")
