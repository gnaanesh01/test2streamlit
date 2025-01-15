import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import tempfile
import os

# Helper function to convert strings to float
def parse_currency(value):
    return float(value.replace('$', '').replace(',', ''))

# Step 1: Calculate ROI Function
def calculate_roi_agentiq(revenue_increase, cost_savings, productivity_gains, development_costs, maintenance_costs, training_costs, licensing_costs, cloud_costs, support_ops_costs, people_removed, average_salary, time_saved_hours, hourly_rate):
    total_benefits = revenue_increase + cost_savings + productivity_gains
    total_costs = development_costs + maintenance_costs + training_costs + licensing_costs + cloud_costs + support_ops_costs
    net_benefits = total_benefits - total_costs
    roi = (net_benefits / total_costs) * 100
    people_cost_reduction = people_removed * average_salary
    time_saved_value = time_saved_hours * hourly_rate
    
    return {
        'Total Benefits': total_benefits,
        'Total Costs': total_costs,
        'Net Benefits': net_benefits,
        'ROI (%)': roi,
        'People Cost Reduction': people_cost_reduction,
        'Time Saved Value': time_saved_value
    }

# Step 2: Input Fields for Data Collection
st.title('ROI Calculator for Agentic AI')
st.subheader("Enter the details to calculate ROI")

# Revenue Inputs
st.subheader('Revenue & Productivity Gains')
revenue_increase = st.number_input('Revenue Increase ($)', value=100000)
cost_savings = st.number_input('Cost Savings ($)', value=50000)
productivity_gains = st.number_input('Productivity Gains ($)', value=30000)

# Cost Inputs
st.subheader('Costs')
development_costs = st.number_input('Development Costs ($)', value=40000)
maintenance_costs = st.number_input('Maintenance Costs ($)', value=10000)
training_costs = st.number_input('Training Costs ($)', value=5000)
licensing_costs = st.number_input('Licensing Costs ($)', value=7000)
cloud_costs = st.number_input('Cloud Costs ($)', value=12000)
support_ops_costs = st.number_input('Support & Ops Costs ($)', value=8000)

# People Inputs
st.subheader('People-Related Data')
people_removed = st.number_input('Number of People Removed', value=5)
average_salary = st.number_input('Average Salary ($)', value=70000)

# Time Inputs
st.subheader('Time Savings')
time_saved_hours = st.number_input('Time Saved (hours)', value=1000)
hourly_rate = st.number_input('Hourly Rate ($)', value=50)

# Step 3: Function to handle button click and calculate ROI
def on_calculate_button_clicked():
    inputs = {
        "revenue_increase": revenue_increase,
        "cost_savings": cost_savings,
        "productivity_gains": productivity_gains,
        "development_costs": development_costs,
        "maintenance_costs": maintenance_costs,
        "training_costs": training_costs,
        "licensing_costs": licensing_costs,
        "cloud_costs": cloud_costs,
        "support_ops_costs": support_ops_costs,
        "people_removed": people_removed,
        "average_salary": average_salary,
        "time_saved_hours": time_saved_hours,
        "hourly_rate": hourly_rate
    }
    
    try:
        # Calculate the ROI and results
        results = calculate_roi_agentiq(**inputs)
        
        # Display the results in a table
        st.write(pd.DataFrame([{
            'Total Benefits': f"${results['Total Benefits']:,.2f}",
            'Total Costs': f"${results['Total Costs']:,.2f}",
            'Net Benefits': f"${results['Net Benefits']:,.2f}",
            'ROI (%)': f"{results['ROI (%)']:.2f}%",
            'People Cost Reduction': f"${results['People Cost Reduction']:,.2f}",
            'Time Saved Value': f"${results['Time Saved Value']:,.2f}"
        }]))
        
        # Generate graphs
        generate_graphs(inputs, results)
        
        # Display the 'Why Sonata Software?' message
        st.markdown("""
            <h3>Why Sonata Software?</h3>
            <p>Sonata Software is the ideal partner for Agentic AI implementation due to its proven expertise in AI-driven transformations, a comprehensive Agent Marketplace, and end-to-end support services. By leveraging tailored AI strategies, Sonata helps businesses maximize ROI by driving revenue growth, enhancing productivity, and reducing operational costs. With a focus on delivering measurable business outcomes, Sonata ensures seamless integration and long-term success for AI initiatives.</p>
            """, unsafe_allow_html=True)
        
        # Generate and display summary report
        generate_summary(inputs, results)
    
    except ValueError as e:
        st.error(f"Error: {e}")

# Step 4: Generate graphs
def generate_graphs(inputs, results):
    revenue = inputs['revenue_increase'] + inputs['cost_savings'] + inputs['productivity_gains']
    total_costs = inputs['development_costs'] + inputs['maintenance_costs'] + inputs['training_costs'] + inputs['licensing_costs'] + inputs['cloud_costs'] + inputs['support_ops_costs']
    years = np.arange(1, 4)
    roi_trend = [((revenue - total_costs) / total_costs) * 100 + i * 10 for i in years]

    # Graph 1: Revenue Components
    revenue_data = pd.DataFrame({
        'Component': ['Revenue Increase', 'Cost Savings', 'Productivity Gains'],
        'Value': [inputs['revenue_increase'], inputs['cost_savings'], inputs['productivity_gains']]
    })
    st.subheader('Revenue Components')
    st.bar_chart(revenue_data.set_index('Component')['Value'])

    # Graph 2: Cost Breakdown
    cost_data = pd.DataFrame({
        'Component': ['Development', 'Maintenance', 'Training', 'Licensing', 'Cloud', 'Support & Ops'],
        'Value': [inputs['development_costs'], inputs['maintenance_costs'], inputs['training_costs'], inputs['licensing_costs'], inputs['cloud_costs'], inputs['support_ops_costs']]
    })
    st.subheader('Cost Breakdown')
    st.bar_chart(cost_data.set_index('Component')['Value'])

    # Graph 3: Total Benefits vs Total Costs
    comparison_data = pd.DataFrame({
        'Category': ['Total Benefits', 'Total Costs'],
        'Value': [results['Total Benefits'], results['Total Costs']]
    })
    st.subheader('Total Benefits vs Total Costs')
    st.bar_chart(comparison_data.set_index('Category')['Value'])

    # Graph 4: People Cost Reduction vs Time Saved Value
    savings_data = pd.DataFrame({
        'Category': ['People Cost Reduction', 'Time Saved Value'],
        'Value': [results['People Cost Reduction'], results['Time Saved Value']]
    })
    st.subheader('People Cost Reduction vs Time Saved Value')
    st.bar_chart(savings_data.set_index('Category')['Value'])

    # Graph 5: ROI Trend Over 3 Years
    st.subheader('ROI Trend Over 3 Years')
    st.line_chart(pd.Series(roi_trend, index=years))

    # Graph 6: Cumulative Savings Over Time
    cumulative_savings = np.cumsum([inputs['cost_savings'], inputs['productivity_gains'], inputs['people_removed'] * inputs['average_salary']])
    st.subheader('Cumulative Savings Over Time')
    st.line_chart(pd.Series(cumulative_savings, index=['Year 1', 'Year 2', 'Year 3']))

    # Graph 7: Net Benefits Over Time
    net_benefits_over_time = [results['Net Benefits'] * (1 + i * 0.05) for i in years]
    st.subheader('Net Benefits Over Time')
    st.line_chart(pd.Series(net_benefits_over_time, index=years))

# Step 5: Summary Report
def generate_summary(inputs, results):
    roi_status = "positive" if results['ROI (%)'] > 0 else "negative"
    
    summary_html = f"""
    <h2 style="color: #2E86C1;">ROI Summary Report</h2>
    <hr>
    <table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd; font-family: Arial, sans-serif; line-height: 1.6;">
        <tr style="background-color: #f2f2f2;">
            <td><strong>Total Benefits:</strong></td>
            <td>${results['Total Benefits']:,.2f}</td>
        </tr>
        <tr>
            <td><strong>Total Costs:</strong></td>
            <td>${results['Total Costs']:,.2f}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td><strong>Net Benefits:</strong></td>
            <td>${results['Net Benefits']:,.2f}</td>
        </tr>
        <tr>
            <td><strong>ROI:</strong></td>
            <td>{results['ROI (%)']:.2f}% ({roi_status})</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td><strong>People Cost Reduction:</strong></td>
            <td>${results['People Cost Reduction']:,.2f}</td>
        </tr>
        <tr>
            <td><strong>Time Saved Value:</strong></td>
            <td>${results['Time Saved Value']:,.2f}</td>
        </tr>
    </table>
    <hr>
    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Explanation:</strong> This ROI summary provides key financial metrics derived from adopting Agentic AI, highlighting significant cost reductions, time savings, and overall financial benefits. The ROI status indicates whether the investment yields a positive or negative return, helping stakeholders assess the financial impact effectively.</p>
    """

    st.markdown(summary_html, unsafe_allow_html=True)
    # Provide a download button for the summary report
    st.download_button(
        label="Download ROI Summary Report",
        data=summary_html,
        file_name="roi_summary_report.html",
        mime="text/html"
    )
    
    # Display the summary report directly in Streamlit

# Step 6: Button to trigger ROI calculation
if st.button('Calculate ROI'):
    on_calculate_button_clicked()
