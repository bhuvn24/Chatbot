# src/utils/visualizer.py
import matplotlib.pyplot as plt
import io
import streamlit as st

def generate_chart(data: dict, title: str):
    """Generate simple line chart, e.g., for stock prices."""
    fig, ax = plt.subplots()
    ax.plot(data.get('dates', []), data.get('prices', []), marker='o')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

def display_chart_in_response(query: str, data: dict):
    if "chart" in query.lower() or "trend" in query.lower():
        chart_buf = generate_chart(data, "Financial Trend")
        st.image(chart_buf, caption="Generated Visualization")