import streamlit as st
import pandas as pd
import numpy as np
from data import generate_users
from features import prepare_features
from model import train_conversion_model
from recommend import recommend_optimal_incentive


st.set_page_config(page_title="RideShare Incentive Engine", layout="wide")

st.title("RideShare Incentive Engine")
st.markdown("AI-powered incentive optimization for maximum rider conversion")
st.markdown("---")

if 'conversion_model' not in st.session_state:
    with st.spinner("Initializing ML conversion model..."):
        historical_riders = generate_users(2000)
        rider_features, conversion_targets = prepare_features(historical_riders)
        st.session_state.conversion_model = train_conversion_model(rider_features, conversion_targets)
        st.session_state.sample_riders = historical_riders.head(8)

with st.expander("Historical Data Sample", expanded=False):
    st.dataframe(
        st.session_state.sample_riders.rename(columns={
            'rider_id': 'ID',
            'weekly_rides': 'Weekly Rides',
            'monthly_rides': 'Monthly Rides',
            'days_since_last_ride': 'Days Since Last',
            'average_trip_value': 'Avg Trip ($)',
            'promotion_acceptance_rate': 'Promo Rate',
            'will_book_ride': 'Converted'
        }), 
        use_container_width=True
    )

st.markdown("")

st.header("Rider Profile")
st.markdown("Enter rider characteristics to generate an optimal incentive recommendation")
st.markdown("")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Activity Metrics")
    monthly_rides = st.number_input(
        "Monthly Rides", 
        min_value=0, 
        max_value=100, 
        value=12, 
        help="Total rides in last 30 days"
    )
    days_inactive = st.number_input(
        "Days Since Last Ride", 
        min_value=0, 
        max_value=365, 
        value=2, 
        help="Days since rider's last trip"
    )

with col2:
    st.subheader("Spending Behavior")
    average_trip_cost = st.number_input(
        "Average Trip Value ($)", 
        min_value=5.0, 
        max_value=150.0, 
        value=28.50, 
        step=0.50, 
        help="Average fare per trip"
    )
    promotion_response_rate = st.slider(
        "Promotion Response Rate", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.35, 
        step=0.05, 
        help="Historical rate of accepting promotions"
    )

st.markdown("")

if st.button("Generate Recommendation", type="primary", use_container_width=True):
    rider_profile = np.array([
        monthly_rides // 4,  # Weekly rides approximation
        monthly_rides,
        days_inactive,
        average_trip_cost,
        promotion_response_rate
    ])
    
    recommendation_result = recommend_optimal_incentive(st.session_state.conversion_model, rider_profile)
    
    st.markdown("---")
    st.header("Recommendation Results")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("Recommended Incentive")
        st.metric(
            label="Optimal Incentive", 
            value=recommendation_result['recommended_incentive'],
            help="Incentive option with highest predicted conversion probability"
        )
        st.metric(
            label="Conversion Probability", 
            value=f"{recommendation_result['expected_conversion_rate']:.1%}",
            help="Predicted likelihood that rider will complete a booking"
        )
    
    with col2:
        st.subheader("Performance Comparison")
        incentive_comparison = pd.DataFrame([
            {
                "Incentive Option": incentive_type,
                "Conversion Rate": f"{conversion_rate:.1%}",
                "Conversion Score": conversion_rate
            }
            for incentive_type, conversion_rate in recommendation_result['all_incentive_scores'].items()
        ]).sort_values("Conversion Score", ascending=False)
        
        st.dataframe(
            incentive_comparison.drop(columns=['Conversion Score']),
            use_container_width=True,
            hide_index=True
        )
    
    st.subheader("Analysis")
    best_incentive = recommendation_result['recommended_incentive']
    conversion_rate = recommendation_result['expected_conversion_rate']
    
    if conversion_rate >= 0.8:
        confidence_level = "Very High"
        rationale = f"Rider exhibits strong engagement patterns. **{best_incentive}** optimizes conversion probability at {conversion_rate:.1%}."
    elif conversion_rate >= 0.6:
        confidence_level = "High"
        rationale = f"Rider demonstrates good engagement indicators. **{best_incentive}** recommended with {conversion_rate:.1%} expected conversion."
    elif conversion_rate >= 0.4:
        confidence_level = "Moderate"
        rationale = f"Rider shows moderate engagement levels. **{best_incentive}** provides optimal conversion opportunity at {conversion_rate:.1%}."
    else:
        confidence_level = "Low"
        rationale = f"Rider exhibits limited engagement signals. **{best_incentive}** offers highest conversion potential at {conversion_rate:.1%}, though overall probability remains constrained."
    
    st.info(f"**Confidence Level: {confidence_level}** - {rationale}")
    
    st.markdown("")

st.markdown("---")
st.caption("Powered by machine learning models trained on historical rider behavior and conversion data")