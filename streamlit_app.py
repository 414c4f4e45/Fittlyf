import streamlit as st
import numpy as np

def perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
    """
    Performs an A/B test and returns the result.

    Args:
        control_visitors: Number of visitors in the control group.
        control_conversions: Number of conversions in the control group.
        treatment_visitors: Number of visitors in the treatment group.
        treatment_conversions: Number of conversions in the treatment group.
        confidence_level: Confidence level for the test (90, 95, or 99).

    Returns:
        A string indicating the result of the A/B test.
    """
    # Calculate conversion rates
    control_rate = control_conversions / control_visitors
    treatment_rate = treatment_conversions / treatment_visitors

    # Calculate pooled standard error
    pooled_se = np.sqrt((control_rate * (1 - control_rate) / control_visitors) +
                        (treatment_rate * (1 - treatment_rate) / treatment_visitors))

    # Calculate t-statistic
    t_statistic = (treatment_rate - control_rate) / pooled_se

    # Calculate degrees of freedom
    df = control_visitors + treatment_visitors - 2

    # Get critical t-value based on confidence level
    confidence_level_map = {
        0.9: np.abs(np.percentile(np.concatenate((np.random.standard_t(df, 100000), -np.random.standard_t(df, 100000))), 95)),
        0.95: np.abs(np.percentile(np.concatenate((np.random.standard_t(df, 100000), -np.random.standard_t(df, 100000))), 97.5)),
        0.99: np.abs(np.percentile(np.concatenate((np.random.standard_t(df, 100000), -np.random.standard_t(df, 100000))), 99.5))
    }
    t_critical = confidence_level_map.get(confidence_level, None)
    if t_critical is None:
        raise ValueError("Invalid confidence level. Choose from 90, 95, or 99.")

    # Compare t-statistic with critical t-value
    if t_statistic > t_critical:
        return "Experiment Group is Better"
    elif t_statistic < -t_critical:
        return "Control Group is Better"
    else:
        return "Indeterminate"

st.title("A/B Test Analysis")

# Get user input for test data
control_visitors = st.number_input("Control Visitors", min_value=0)
control_conversions = st.number_input("Control Conversions", min_value=0)
treatment_visitors = st.number_input("Treatment Visitors", min_value=0)
treatment_conversions = st.number_input("Treatment Conversions", min_value=0)
confidence_level = st.selectbox("Confidence Level", options=[0.9, 0.95, 0.99])

# Run the A/B test and display the result
if st.button("Run A/B Test"):
    try:
        result = perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions,
                                 confidence_level)
        st.success(f"A/B Test Result: {result}")
    except ValueError as e:
        st.error(f"Error: {e}")
