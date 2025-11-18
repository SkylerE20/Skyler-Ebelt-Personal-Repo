import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Student Engagement Analysis", layout="wide")

@st.cache_data
def load_data():
    return pd.read_parquet("student_analysis.parquet")

df = load_data()

# Title
st.title("Student Engagement & Intervention Analysis")
st.markdown("### Analyzing the relationship between TA-led interventions and student performance in online learning")

# Key Metrics at the top
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", f"{len(df):,}")

with col2:
    avg_grade = df['avg_grade_percentage'].mean()
    st.metric("Average Grade", f"{avg_grade:.1f}%")

with col3:
    total_interventions = df['intervention_interactions'].sum()
    st.metric("Total Intervention Interactions", f"{int(total_interventions):,}")

with col4:
    engaged_students = len(df[df['intervention_interactions'] > 0])
    st.metric("Students w/ Interventions", f"{engaged_students:,}")

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Engagement Tiers", "Correlations", "Grade Analysis"])

with tab1:
    st.header("Engagement Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Video Engagement")
        video_dist = df['video_engagement_tier'].value_counts().sort_index()
        fig = px.bar(x=video_dist.index, y=video_dist.values, 
                     labels={'x': 'Tier', 'y': 'Number of Students'},
                     title="Video Engagement Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Quiz Engagement")
        quiz_dist = df['quiz_engagement_tier'].value_counts().sort_index()
        fig = px.bar(x=quiz_dist.index, y=quiz_dist.values,
                     labels={'x': 'Tier', 'y': 'Number of Students'},
                     title="Quiz Engagement Distribution")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Intervention Engagement Tiers")
    
    intervention_dist = df['intervention_engagement_tier'].value_counts().sort_index()
    fig = px.bar(x=intervention_dist.index, y=intervention_dist.values,
                 labels={'x': 'Engagement Tier', 'y': 'Number of Students'},
                 title="Intervention Engagement Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Average grades by intervention tier
    st.subheader("Average Grade by Intervention Engagement")
    avg_by_tier = df.groupby('intervention_engagement_tier')['avg_grade_percentage'].mean().sort_index()
    fig = px.bar(x=avg_by_tier.index, y=avg_by_tier.values,
                 labels={'x': 'Intervention Tier', 'y': 'Average Grade (%)'},
                 title="Does Intervention Engagement Correlate with Grades?")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Correlation Analysis")
    
    numeric_cols = [
        'video_interactions', 'video_engagement_tier',
        'quiz_interactions', 'quiz_engagement_tier', 
        'intervention_interactions', 'intervention_engagement_tier',
        'avg_grade_percentage', 'grade_score'
    ]
    
    correlation_data = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title('Correlation Matrix: Engagement Metrics vs Grades', fontsize=14, pad=20)
    st.pyplot(fig)

with tab4:
    st.header("Grade Distribution")
    
    grade_dist = df['letter_grade'].value_counts().sort_index()
    fig = px.bar(x=grade_dist.index, y=grade_dist.values,
                 labels={'x': 'Letter Grade', 'y': 'Number of Students'},
                 title="Grade Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Scatter: intervention interactions vs grade
    st.subheader("Intervention Interactions vs Grade")
    fig = px.scatter(df, x='intervention_interactions', y='avg_grade_percentage',
                     color='letter_grade',
                     labels={'intervention_interactions': 'Number of Intervention Interactions',
                            'avg_grade_percentage': 'Average Grade (%)'},
                     title="Relationship Between Interventions and Performance")
    st.plotly_chart(fig, use_container_width=True)