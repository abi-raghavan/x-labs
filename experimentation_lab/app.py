import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from db import create_experiment, get_experiment, list_experiments
from simulation import simulate_users
from metrics import users_by_variant, conversion_rate, revenue_per_user, absolute_lift, relative_lift
from stats import two_proportion_z_test, revenue_t_test
from risk import sample_ratio_mismatch, insufficient_sample_size


def main():
    st.set_page_config(page_title="x-labs Experimentation System", layout="wide")
    
    st.title("x-labs Experimentation System")
    
    page = st.sidebar.selectbox("Choose a page", ["Create Experiment", "Simulate Traffic", "Analyze Results"])
    
    if page == "Create Experiment":
        create_experiment_page()
    elif page == "Simulate Traffic":
        simulate_traffic_page()
    elif page == "Analyze Results":
        analyze_results_page()


def create_experiment_page():
    st.header("Create Experiment")
    
    with st.form("experiment_form"):
        name = st.text_input("Experiment Name")
        owner = st.text_input("Owner")
        primary_metric = st.selectbox("Primary Metric", ["conversion_rate", "revenue_per_user"])
        traffic_split = st.slider("Traffic Split (Control %)", 0.0, 1.0, 0.5, 0.05)
        sample_size = st.number_input("Sample Size", min_value=100, value=1000, step=100)
        start_date = st.date_input("Start Date", value=date.today())
        
        submitted = st.form_submit_button("Create Experiment")
        
        if submitted and name and owner:
            exp_id = create_experiment(
                name, owner, primary_metric, traffic_split, 
                sample_size, start_date.strftime("%Y-%m-%d")
            )
            st.success(f"Experiment created with ID: {exp_id}")


def simulate_traffic_page():
    st.header("Simulate Traffic")
    
    experiments = list_experiments()
    if not experiments:
        st.warning("No experiments found. Create an experiment first.")
        return
    
    exp_options = {f"{exp['name']} (ID: {exp['id']})": exp['id'] for exp in experiments}
    selected_exp = st.selectbox("Select Experiment", list(exp_options.keys()))
    
    if selected_exp:
        exp_id = exp_options[selected_exp]
        experiment = get_experiment(exp_id)
        
        st.subheader("Experiment Details")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {experiment['name']}")
            st.write(f"**Owner:** {experiment['owner']}")
            st.write(f"**Primary Metric:** {experiment['primary_metric']}")
        with col2:
            st.write(f"**Traffic Split:** {experiment['traffic_split']}")
            st.write(f"**Sample Size:** {experiment['sample_size']}")
            st.write(f"**Start Date:** {experiment['start_date']}")
        
        n_users = st.number_input("Number of Users to Simulate", 
                                 min_value=100, 
                                 value=experiment['sample_size'], 
                                 step=100)
        
        if st.button("Generate Traffic"):
            with st.spinner("Simulating users..."):
                df = simulate_users(n_users, f"exp_{exp_id}", experiment['traffic_split'])
                st.session_state[f'data_{exp_id}'] = df
                st.success(f"Generated {len(df)} users")
                
                variant_counts = users_by_variant(df)
                st.subheader("Variant Distribution")
                fig = px.bar(variant_counts, x='variant', y='count', 
                           title="Users by Variant")
                st.plotly_chart(fig)


def analyze_results_page():
    st.header("Analyze Results")
    
    experiments = list_experiments()
    if not experiments:
        st.warning("No experiments found. Create an experiment first.")
        return
    
    exp_options = {f"{exp['name']} (ID: {exp['id']})": exp['id'] for exp in experiments}
    selected_exp = st.selectbox("Select Experiment", list(exp_options.keys()))
    
    if selected_exp:
        exp_id = exp_options[selected_exp]
        
        if f'data_{exp_id}' not in st.session_state:
            st.warning("No simulation data found. Generate traffic first.")
            return
        
        df = st.session_state[f'data_{exp_id}']
        experiment = get_experiment(exp_id)
        
        st.subheader("Experiment Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_users = len(df)
            st.metric("Total Users", total_users)
        
        with col2:
            overall_conv = df['converted'].mean()
            st.metric("Overall Conversion Rate", f"{overall_conv:.2%}")
        
        with col3:
            overall_revenue = df['revenue'].mean()
            st.metric("Overall Revenue per User", f"${overall_revenue:.2f}")
        
        st.subheader("Conversion Rate Analysis")
        
        conv_data = conversion_rate(df)
        conv_data['conversion_rate'] = conv_data['sum'] / conv_data['count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(conv_data, x='variant', y='conversion_rate', 
                        title="Conversion Rate by Variant")
            st.plotly_chart(fig)
        
        with col2:
            abs_lift_val = absolute_lift(df)
            rel_lift_val = relative_lift(df)
            
            st.metric("Absolute Lift", f"{abs_lift_val:.3f}")
            st.metric("Relative Lift", f"{rel_lift_val:.2%}")
        
        st.subheader("Revenue Analysis")
        
        revenue_data = revenue_per_user(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(revenue_data, x='variant', y='revenue', 
                        title="Revenue per User by Variant")
            st.plotly_chart(fig)
        
        with col2:
            control_revenue = df[df['variant'] == 'control']['revenue']
            variant_revenue = df[df['variant'] == 'variant']['revenue']
            revenue_lift = variant_revenue.mean() - control_revenue.mean()
            st.metric("Revenue Lift", f"${revenue_lift:.2f}")
        
        st.subheader("Statistical Tests")
        
        control_data = df[df['variant'] == 'control']
        variant_data = df[df['variant'] == 'variant']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Conversion Rate Test**")
            z_test_result = two_proportion_z_test(
                control_data['converted'].sum(), len(control_data),
                variant_data['converted'].sum(), len(variant_data)
            )
            st.write(f"P-value: {z_test_result['p_value']:.4f}")
            ci = z_test_result['confidence_interval']
            st.write(f"95% CI: [{ci[0]:.4f}, {ci[1]:.4f}]")
        
        with col2:
            st.write("**Revenue Test**")
            t_test_result = revenue_t_test(
                control_data['revenue'].values,
                variant_data['revenue'].values
            )
            st.write(f"P-value: {t_test_result['p_value']:.4f}")
            ci = t_test_result['confidence_interval']
            st.write(f"95% CI: [${ci[0]:.2f}, ${ci[1]:.2f}]")
        
        st.subheader("Risk Detection")
        
        col1, col2 = st.columns(2)
        
        with col1:
            srm_detected = sample_ratio_mismatch(
                len(control_data), len(variant_data), experiment['traffic_split']
            )
            st.write("**Sample Ratio Mismatch**")
            if srm_detected:
                st.error("SRM Detected!")
            else:
                st.success("No SRM Detected")
        
        with col2:
            insufficient_power = insufficient_sample_size(len(df), 0.1)
            st.write("**Sample Size Check**")
            if insufficient_power:
                st.warning("Insufficient Sample Size")
            else:
                st.success("Adequate Sample Size")


if __name__ == "__main__":
    main()