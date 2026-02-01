import streamlit as st
import subprocess
import sys
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import psutil
import time
import re

st.set_page_config(page_title="PyCEFRL - Python Code Level Analyzer", layout="wide")

# --- System Stats Helper ---
def get_system_stats():
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    return cpu, ram

# Sidebar for mode selection and Stats
with st.sidebar:
    st.header("Settings")
    mode = st.selectbox("Select Analysis Mode", ["Directory", "GitHub Repository", "GitHub User"])
    
    st.divider()
    st.header("System Stats")
    cpu_metric = st.empty()
    ram_metric = st.empty()
    
    # Initial stats
    c, r = get_system_stats()
    cpu_metric.metric("CPU Usage", f"{c}%")
    ram_metric.metric("RAM Usage", f"{r}%")

st.title("🐍 PyCEFRL - Python Code Level Analyzer")
st.markdown("""
This tool analyzes the level of Python code inspired by the CEFR (Common European Framework of Reference for Languages).
Analyze code **in real-time** from:
- 📁 Local directory
- 🔗 GitHub repository URL
- 👤 GitHub user profile

**Real-time Features:**
- ⚡ Live progress tracking
- 📊 File-by-file updates
- 💻 System resource monitoring
""")

# Ensure dict.py has been run
if not os.path.exists('dicc.txt'):
    with st.spinner('Generating level dictionary...'):
        subprocess.run([sys.executable, 'dict.py'], check=True)
    st.success('Level dictionary generated!')

def run_analysis(mode_arg, value_arg):
    cmd = [sys.executable, '-u', 'pycerfl.py', mode_arg, value_arg]
    
    st.write(f"🚀 Starting analysis on {value_arg}...")
    
    # Create containers for different parts
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.expander("Real-time Analysis Logs", expanded=True)
    
    logs = []
    total_files = 0
    processed_files = 0
    
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True, 
        bufsize=1, 
        universal_newlines=True
    )
    
    # Read output line by line
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            logs.append(line)
            
            # Extract progress information from log lines
            if 'Found' in line and 'Python file(s) to analyze' in line:
                try:
                    total_files = int(line.split('Found ')[1].split(' Python')[0])
                except (ValueError, IndexError) as e:
                    # Failed to parse file count - log for debugging but continue
                    st.warning(f"Could not parse file count from: {line.strip()}")
            
            if 'Processing:' in line and processed_files < total_files:
                processed_files += 1
                if total_files > 0:
                    progress = min(processed_files / total_files, 1.0)  # Cap at 100%
                    progress_bar.progress(progress)
                    status_text.text(f"Processing file {processed_files}/{total_files}...")
            
            # Update log display - show last 25 lines for "tail" effect
            with log_container:
                st.code("".join(logs[-25:]))
            
            # Update system stats occasionally
            if len(logs) % 5 == 0:  # Update every 5 lines to avoid too much overhead
                c, r = get_system_stats()
                cpu_metric.metric("CPU Usage", f"{c}%")
                ram_metric.metric("RAM Usage", f"{r}%")

    if process.returncode != 0:
        progress_bar.progress(0)
        status_text.text("❌ Analysis failed")
        st.error("Error during analysis:")
        st.code("".join(logs)) # Show full logs on error
        return False
    
    progress_bar.progress(1.0)
    status_text.text("✅ Analysis complete!")
    
    # Show full logs in an expander after completion
    with st.expander("View Complete Analysis Logs"):
        st.code("".join(logs))
        
    st.success(f"✅ Analysis complete! Processed {processed_files} file(s).")
    return True

def display_results():
    # Check if results exist
    if not os.path.exists('data.json'):
        st.warning("No results found. Please run an analysis first.")
        return

    # Load summary data
    if os.path.exists('DATA_JSON/summary_data.json'):
        with open('DATA_JSON/summary_data.json', 'r') as f:
            summary = json.load(f)
        
        # Display overall levels
        if 'Levels' in summary:
            st.subheader("Level Distribution")
            levels = summary['Levels']
            
            # Create columns for metrics
            cols = st.columns(len(levels))
            for i, (level, count) in enumerate(levels.items()):
                with cols[i % len(cols)]:
                    st.metric(label=f"Level {level}", value=count)
            
            # Bar chart
            fig, ax = plt.subplots()
            ax.bar(levels.keys(), levels.values())
            ax.set_ylabel('Count')
            ax.set_title('Elements per Level')
            st.pyplot(fig)

    # Sankey Diagram
    if os.path.exists('data.csv'):
        st.subheader("Visualizations")
        
        try:
            df_csv = pd.read_csv('data.csv')
            
            # --- Helper to categorize classes ---
            def categorize_class(class_name):
                class_name = str(class_name).lower()
                if any(x in class_name for x in ['list', 'tuple', 'dict', 'set', 'array']):
                    return 'Data Structures'
                elif any(x in class_name for x in ['if', 'else', 'loop', 'for', 'while', 'try', 'except', 'break', 'continue', 'pass']):
                    return 'Control Flow'
                elif any(x in class_name for x in ['function', 'lambda', 'class', 'method', 'return', 'yield', 'super', 'decorator', 'init', 'self']):
                    return 'OOP & Functions'
                elif any(x in class_name for x in ['print', 'file', 'open', 'read', 'write', 'input']):
                    return 'I/O'
                elif any(x in class_name for x in ['import', 'from', 'module']):
                    return 'Modules'
                elif any(x in class_name for x in ['assign', 'operator', 'compare', 'binop']):
                    return 'Operations'
                else:
                    return 'Other'

            if 'Class' in df_csv.columns:
                df_csv['Category'] = df_csv['Class'].apply(categorize_class)

            # --- Tabs for different visualizations ---
            tab1, tab2, tab3 = st.tabs(["Bubble Chart", "File Heatmap", "Element Treemap"])

            with tab1:
                st.write("Bubble Chart: Category vs Level (Size represents frequency)")
                if 'Category' in df_csv.columns and 'Level' in df_csv.columns:
                    # Group by Category and Level
                    bubble_data = df_csv.groupby(['Category', 'Level']).size().reset_index(name='Count')
                    
                    if not bubble_data.empty:
                        # Define standard level order
                        level_order = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
                        
                        fig_bubble = go.Figure(data=go.Scatter(
                            x=bubble_data['Category'],
                            y=bubble_data['Level'],
                            mode='markers',
                            marker=dict(
                                size=bubble_data['Count'],
                                sizemode='area',
                                # Scale bubbles: 2 * max / (desired_max_px^2)
                                sizeref=2. * max(bubble_data['Count']) / (50.**2),
                                sizemin=5,
                                color=bubble_data['Count'],
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="Count")
                            ),
                            text=bubble_data.apply(lambda row: f"Count: {row['Count']}", axis=1),
                            hovertemplate="<b>%{x}</b><br>Level: %{y}<br>%{text}<extra></extra>"
                        ))

                        fig_bubble.update_layout(
                            xaxis=dict(title='Category'),
                            yaxis=dict(
                                title='Level',
                                categoryorder='array',
                                categoryarray=level_order
                            ),
                            height=600,
                            margin=dict(l=50, r=50, t=50, b=50)
                        )
                        
                        st.plotly_chart(fig_bubble, use_container_width=True)
                    else:
                        st.info("No data available for bubble chart.")

            with tab2:
                st.write("Heatmap of File vs Level Count")
                if 'File Name' in df_csv.columns and 'Level' in df_csv.columns:
                    # Create pivot table: Rows=File, Cols=Level, Values=Count
                    df_pivot = df_csv.pivot_table(index='File Name', columns='Level', aggfunc='size', fill_value=0)
                    
                    fig_heat = go.Figure(data=go.Heatmap(
                        z=df_pivot.values,
                        x=df_pivot.columns,
                        y=df_pivot.index,
                        colorscale='Viridis'
                    ))
                    fig_heat.update_layout(height=max(400, len(df_pivot)*20))
                    st.plotly_chart(fig_heat, use_container_width=True)

            with tab3:
                st.write("Treemap: Drill down into specific elements (Level -> Category -> Element)")
                if 'Category' in df_csv.columns and 'Level' in df_csv.columns and 'Class' in df_csv.columns:
                    # Clean up 'Class' column (optional, but good for visualization)
                    # We use the full class name for now as it contains specific details
                    
                    fig_treemap = px.treemap(
                        df_csv, 
                        path=['Level', 'Category', 'Class'], 
                        color='Level',
                        color_discrete_map={
                            'A1': '#1f77b4', 'A2': '#2ca02c', 
                            'B1': '#ff7f0e', 'B2': '#d62728', 
                            'C1': '#9467bd', 'C2': '#8c564b'
                        }
                    )
                    fig_treemap.update_layout(height=600)
                    st.plotly_chart(fig_treemap, use_container_width=True)
                
        except Exception as e:
            st.error(f"Could not generate visualizations: {e}")

    # Load file-specific data
    if os.path.exists('DATA_JSON/total_data.json'):
        with open('DATA_JSON/total_data.json', 'r') as f:
            total_data = json.load(f)
        
        st.subheader("Detailed File Analysis")
        
        # Convert to DataFrame for display
        rows = []
        for repo_name, files in total_data.items():
            for file_name, stats in files.items():
                row = {'Repository': repo_name, 'File': file_name}
                if 'Levels' in stats:
                    row.update(stats['Levels'])
                rows.append(row)
        
        if rows:
            df = pd.DataFrame(rows).fillna(0)
            st.dataframe(df)

    # Download buttons
    st.subheader("Downloads")
    col1, col2 = st.columns(2)
    
    with col1:
        if os.path.exists('data.json'):
            with open('data.json', 'rb') as f:
                st.download_button('Download JSON Report', f, file_name='pycefrl_data.json', mime='application/json')
    
    with col2:
        if os.path.exists('data.csv'):
            with open('data.csv', 'rb') as f:
                st.download_button('Download CSV Report', f, file_name='pycefrl_data.csv', mime='text/csv')

# Mode specific logic
if mode == "Directory":
    path = st.text_input("Enter directory path (absolute or relative)", value=".")
    
    # Show resolved absolute path
    if path and os.path.exists(path):
        st.info(f"📂 Resolved Path: {os.path.abspath(path)}")
    elif path:
        st.warning(f"⚠️ Path does not exist: {path}")
        
    if st.button("Analyze Directory", type="primary"):
        if path and os.path.exists(path):
            if run_analysis("directory", path):
                display_results()
        else:
            st.error("Please enter a valid directory path")

elif mode == "GitHub Repository":
    url = st.text_input("Enter GitHub Repository URL", placeholder="https://github.com/username/repository")
    
    # URL validation helper
    is_valid = False
    clone_url = None
    
    if url:
        # Basic GitHub URL validation - supports dots, hyphens, and underscores in repo names
        # Matches: https://github.com/user/repo or https://github.com/user/repo.git
        github_pattern = r'^https?://github\.com/([\w.-]+)/([\w.-]+?)(\.git)?/?$'
        match = re.match(github_pattern, url.rstrip('/'))
        
        if match:
            is_valid = True
            st.success("✓ Valid GitHub repository URL")
            # Normalize to clone URL (always ends with .git)
            base_url = url.rstrip('/').rstrip('.git')
            clone_url = base_url + '.git'
        else:
            st.warning("⚠️ Please enter a valid GitHub repository URL (e.g., https://github.com/user/repo)")
    
    if st.button("Analyze Repository", type="primary"):
        if url and is_valid and clone_url:
            if run_analysis("repo-url", clone_url):
                display_results()
        elif url:
            st.error("Please enter a valid GitHub repository URL")
        else:
            st.warning("Please enter a URL")

elif mode == "GitHub User":
    user = st.text_input("Enter GitHub Username", placeholder="octocat")
    
    if user:
        st.info(f"👤 Will analyze all Python repositories for user: **{user}**")
    
    if st.button("Analyze User", type="primary"):
        if user:
            if run_analysis("user", user):
                display_results()
        else:
            st.warning("Please enter a username")
