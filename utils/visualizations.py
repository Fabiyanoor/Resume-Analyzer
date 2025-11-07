import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict

def create_skill_chart(skills_breakdown: Dict):
    """Create a radar chart for skills breakdown"""
    categories = list(skills_breakdown.keys())
    values = list(skills_breakdown.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],  # Close the radar
        theta=categories + [categories[0]],
        fill='toself',
        name='Skills Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Skills Breakdown Radar Chart"
    )
    
    return fig

def create_match_radar(category_scores: Dict):
    """Create radar chart for job match analysis"""
    categories = list(category_scores.keys())
    values = list(category_scores.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Job Match Analysis"
    )
    
    return fig