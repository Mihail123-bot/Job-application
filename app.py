import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from database import Database
from components import render_kanban, render_calendar, render_stats
from streamlit_lottie import st_lottie
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="Job Application Tracker", page_icon="💼", layout="wide", initial_sidebar_state="expanded")
  # Add this enhanced CSS at the top of your app.py
st.markdown("""
      <style>
      @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
      * {
          font-family: 'Poppins', sans-serif;
      }
    
      .main {
          padding: 3rem;
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      }
    
      .stButton>button {
          width: 100%;
          padding: 0.75rem 1.5rem;
          border-radius: 15px;
          border: none;
          background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
          color: white;
          font-weight: 500;
          transform: translateY(0);
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          box-shadow: 0 10px 20px rgba(0, 13, 255, 0.15);
      }
    
      .stButton>button:hover {
          transform: translateY(-3px);
          box-shadow: 0 20px 40px rgba(0, 13, 255, 0.2);
      }
    
      .dashboard-card {
          background: rgba(255, 255, 255, 0.9);
          backdrop-filter: blur(10px);
          padding: 1.5rem;
          border-radius: 20px;
          box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.5);
          margin-bottom: 1.5rem;
          transform: translateY(0);
          transition: all 0.3s ease;
      }
    
      .dashboard-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
      }
    
      .metric-card {
          text-align: center;
          padding: 1.5rem;
          border-radius: 20px;
          background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
          color: white;
          box-shadow: 0 15px 35px rgba(255, 107, 107, 0.2);
          transform: translateY(0);
          transition: all 0.3s ease;
      }
    
      .metric-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 25px 45px rgba(255, 107, 107, 0.3);
      }
    
      .custom-header {
          font-size: 2.5rem;
          font-weight: 700;
          background: linear-gradient(120deg, #6B73FF, #FF6B6B);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          text-align: center;
          margin-bottom: 2rem;
          text-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
      }
    
      /* Status-specific styling */
      .status-applied {
          background: linear-gradient(135deg, #4158D0 0%, #C850C0 100%);
      }
    
      .status-interviewed {
          background: linear-gradient(135deg, #FFAF7B 0%, #D76D77 100%);
      }
    
      .status-offered {
          background: linear-gradient(135deg, #0BA360 0%, #3CBA92 100%);
      }
    
      /* Card content styling */
      .card-content {
          background: rgba(255, 255, 255, 0.95);
          padding: 1rem;
          border-radius: 15px;
          margin-top: 1rem;
          border: 1px solid rgba(255, 255, 255, 0.3);
      }
    
      /* Animated progress bar */
      .progress-bar {
          height: 8px;
          background: linear-gradient(90deg, #6B73FF 0%, #FF6B6B 100%);
          border-radius: 4px;
          transition: width 0.3s ease;
      }
      </style>
      """, unsafe_allow_html=True)
def load_lottie_animation(url):
    # Using a verified working Lottie animation URL
    url = "https://assets3.lottiefiles.com/packages/lf20_qm8eqzse.json"
    return requests.get(url).json()


def main():
    # Initialize database
    db = Database()
    
    # Get data once for use throughout the app
    data = db.get_all_applications()
    
    # Sidebar with cool animation
    with st.sidebar:
        lottie_career = load_lottie_animation("https://assets9.lottiefiles.com/packages/lf20_yqyt3qk1.json")
        st_lottie(lottie_career, height=200)
        st.title("🎯 Navigation")
        choice = st.selectbox("", ["Dashboard", "Kanban Board", "Calendar View", "Analytics"])

    if choice == "Dashboard":
        # Header with animation
        st.markdown('<h1 class="custom-header">Job Application Dashboard</h1>', unsafe_allow_html=True)
        
        # Quick Stats Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <h3>Total Applications</h3>
                    <h2>{}</h2>
                </div>
            """.format(len(data)), unsafe_allow_html=True)
            
        with col2:
            active = len(data[data['status'] == 'Applied'])
            st.markdown("""
                <div class="metric-card">
                    <h3>Active Applications</h3>
                    <h2>{}</h2>
                </div>
            """.format(active), unsafe_allow_html=True)
            
        with col3:
            interviews = len(data[data['status'] == 'Interviewed'])
            st.markdown("""
                <div class="metric-card">
                    <h3>Interviews</h3>
                    <h2>{}</h2>
                </div>
            """.format(interviews), unsafe_allow_html=True)
            
        with col4:
            offers = len(data[data['status'] == 'Offered'])
            st.markdown("""
                <div class="metric-card">
                    <h3>Offers</h3>
                    <h2>{}</h2>
                </div>
            """.format(offers), unsafe_allow_html=True)

        # Main Content
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("📝 Quick Add Application")
            
            company = st.text_input("Company Name", placeholder="Enter company name")
            position = st.text_input("Position", placeholder="Enter job position")
            status = st.selectbox("Status", ["Applied", "Interviewed", "Offered"])
            deadline = st.date_input("Application Deadline")
            
            if st.button("➕ Add Application"):
                db.add_application(company, position, status, deadline)
                st.success("Application Added Successfully!")
                st.balloons()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recent Applications
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("🕒 Recent Applications")
            recent = data.sort_values('created_at', ascending=False).head(5)
            for _, app in recent.iterrows():
                st.markdown(f"""
                    <div style='padding: 10px; border-left: 4px solid #2196F3; margin: 10px 0;'>
                        <h4>{app['company']}</h4>
                        <p>{app['position']} • {app['status']}</p>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Application Timeline
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("📈 Application Progress")
            if not data.empty:
                data['created_at'] = pd.to_datetime(data['created_at'])
                timeline_data = data.groupby([data['created_at'].dt.date, 'status']).size().reset_index()
                timeline_data.columns = ['date', 'status', 'count']
                
                fig = go.Figure()
                for status in ['Applied', 'Interviewed', 'Offered']:
                    status_data = timeline_data[timeline_data['status'] == status]
                    fig.add_trace(go.Scatter(
                        x=status_data['date'],
                        y=status_data['count'],
                        name=status,
                        mode='lines+markers',
                        line=dict(width=3),
                        marker=dict(size=8)
                    ))
                
                fig.update_layout(
                    title="Application Timeline",
                    xaxis_title="Date",
                    yaxis_title="Number of Applications",
                    hovermode="x unified",
                    showlegend=True,
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Status Distribution
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("📊 Status Distribution")
            fig = px.pie(data, names='status', 
                        color_discrete_sequence=['#2196F3', '#4CAF50', '#FFC107'],
                        hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif choice == "Kanban Board":
        render_kanban(db)
    elif choice == "Calendar View":
        render_calendar(db)
    else:
        render_stats(data)
if __name__ == "__main__":
    main()
