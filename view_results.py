'''
## 3. view_results.py

### Purpose:
Display simulation results and statistical analysis

### Functions:
- show_pipe_pressure_statistics():
    - User selects pipes from drop-down
    - Automatically find start and end node of each pipe
    - Show min/max/mean pressure at these nodes
    - Draw Plotly line chart for pressure over time

### Role:
- Visualization module for engineers
- Help check hydraulic behavior across the network
- Support reporting and decision-making
'''

# view_results.py
# Module: Visualization and Analysis of EPANET Simulation Results with Map View, Graph View, Table View

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Display pressure statistics and chart for selected pipes
def show_pipe_pressure_statistics(pressure_df, wn, pipe_ids):
    """
    For each selected pipe:
    - Get start and end nodes
    - Show min, max, average pressure
    - Draw Plotly pressure-time chart
    """
    node_pairs = [(wn.get_link(pid).start_node_name, wn.get_link(pid).end_node_name) for pid in pipe_ids]

    st.subheader("Pressure Statistics for Selected Pipes")

    for i, (start_node, end_node) in enumerate(node_pairs):
        for node in [start_node, end_node]:
            if node in pressure_df.columns:
                stats = pressure_df[node].agg(['min', 'max', 'mean'])
                st.markdown(f"**Node {node}**")
                st.write(stats.to_frame(name='Pressure (m)'))

                fig = px.line(
                    pressure_df,
                    y=node,
                    title=f"Pressure Over Time - Node {node}",
                    labels={"index": "Time Step", node: "Pressure (m)"}
                )
                st.plotly_chart(fig)
            else:
                st.warning(f"Node {node} not found in pressure results.")

# View network pressure results on Map
def show_network_map(pressure_df, wn, timestep=-1, parameter='pressure'):
    """
    Display node pressure results on a map with color-coded markers.
    """
    st.subheader("Network Map View - Pressure Distribution")

    node_positions = {}
    x_list = []
    y_list = []
    pressure_list = []
    id_list = []

    for node_name, node in wn.nodes():
        if hasattr(node, 'coordinates'):
            x, y = node.coordinates
        else:
            x, y = (0, 0)  # default position if not defined

        x_list.append(x)
        y_list.append(y)
        id_list.append(node_name)

        if node_name in pressure_df.columns:
            pressure_value = pressure_df[node_name].iloc[timestep]
        else:
            pressure_value = None

        pressure_list.append(pressure_value)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_list,
        y=y_list,
        mode='markers+text',
        marker=dict(
            size=12,
            color=pressure_list,
            colorscale='Viridis',
            colorbar=dict(title='Pressure (m)'),
            showscale=True
        ),
        text=id_list,
        hoverinfo='text'
    ))

    fig.update_layout(
        title="Pressure Map at Selected Timestep",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        height=600
    )

    st.plotly_chart(fig)

# View simulation results as Graph for selected nodes
def show_results_graph(pressure_df, selected_nodes):
    """
    Plot pressure vs time line chart for selected nodes
    """
    st.subheader("Results View - Graph")

    fig = go.Figure()
    for node in selected_nodes:
        if node in pressure_df.columns:
            fig.add_trace(go.Scatter(
                y=pressure_df[node],
                mode='lines',
                name=node
            ))
    fig.update_layout(
        title="Pressure Over Time",
        xaxis_title="Time Step",
        yaxis_title="Pressure (m)"
    )
    st.plotly_chart(fig)

# View simulation results as Table for selected nodes
def show_results_table(pressure_df, selected_nodes):
    """
    Show DataFrame table of pressure values for selected nodes
    """
    st.subheader("Results View - Table")

    df_show = pressure_df[selected_nodes]
    st.dataframe(df_show)

    csv = df_show.to_csv(index=True).encode('utf-8')
    st.download_button("Download Table as CSV", csv, file_name="pressure_results.csv")

