import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

def render_kanban(db):
    st.markdown('<h1 class="custom-header">Interactive Kanban Board</h1>', unsafe_allow_html=True)
    
    data = db.get_all_applications()
    
    # Kanban Columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(120deg, #3b48ff, #666fed); padding: 10px; border-radius: 10px; color: white;'>
                <h3 style='text-align: center;'>Applied</h3>
            </div>
        """, unsafe_allow_html=True)
        
        applied = data[data['status'] == 'Applied']
        for _, row in applied.iterrows():
            cols = render_card(row)
            if cols:
                with cols[0]:
                    if st.button(f"📈 Move to Interview #{row['id']}", key=f"move_int_{row['id']}"):
                        db.update_status(row['id'], 'Interviewed')
                        st.rerun()
                with cols[1]:
                    if st.button(f"🗑️ Delete #{row['id']}", key=f"del_app_{row['id']}"):
                        db.delete_application(row['id'])
                        st.rerun()    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(120deg, #FFA726, #FB8C00); padding: 10px; border-radius: 10px; color: white;'>
                <h3 style='text-align: center;'>Interviewed</h3>
            </div>
        """, unsafe_allow_html=True)
        
        interviewed = data[data['status'] == 'Interviewed']
        for _, row in interviewed.iterrows():
            cols = render_card(row)
            if cols:
                with cols[0]:
                    if st.button(f"🎉 Move to Offered #{row['id']}", key=f"move_off_{row['id']}"):
                        db.update_status(row['id'], 'Offered')
                        st.rerun()
                with cols[1]:
                    if st.button(f"🗑️ Delete #{row['id']}", key=f"del_int_{row['id']}"):
                        db.delete_application(row['id'])
                        st.rerun()
    with col3:
        st.markdown("""
            <div style='background: linear-gradient(120deg, #66BB6A, #43A047); padding: 10px; border-radius: 10px; color: white;'>
                <h3 style='text-align: center;'>Offered</h3>
            </div>
        """, unsafe_allow_html=True)
        
        offered = data[data['status'] == 'Offered']
        for _, row in offered.iterrows():
            cols = render_card(row)
            if cols:
                with cols[1]:
                    if st.button(f"🗑️ Delete #{row['id']}", key=f"del_off_{row['id']}"):
                        db.delete_application(row['id'])
                        st.rerun()

def render_calendar(db):
    st.markdown('<h1 class="custom-header">Calendar View</h1>', unsafe_allow_html=True)
    
    data = db.get_all_applications()
    if not data.empty:
        data['deadline'] = pd.to_datetime(data['deadline'])
        
        # Calendar Stats with gradient background
        upcoming_deadlines = len(data[data['deadline'] > datetime.now()])
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);">
                <h3>Upcoming Deadlines</h3>
                <h2>{upcoming_deadlines}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        today = datetime.now()
        dates = pd.date_range(today, today + timedelta(days=30))
        
        for date in dates:
            day_applications = data[data['deadline'].dt.date == date.date()]
            if not day_applications.empty:
                # Date header with gradient
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4158D0 0%, #C850C0 100%);
                               padding: 15px; border-radius: 15px; color: white; margin: 10px 0;
                               box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                        <h3>{date.strftime('%Y-%m-%d')} ({len(day_applications)} applications)</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                for _, app in day_applications.iterrows():
                    # Application cards with different colors based on status
                    gradient = {
                        'Applied': 'linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%)',
                        'Interviewed': 'linear-gradient(135deg, #4158D0 0%, #C850C0 100%)',
                        'Offered': 'linear-gradient(135deg, #0BA360 0%, #3CBA92 100%)'
                    }.get(app['status'], 'linear-gradient(135deg, #6B73FF 0%, #000DFF 100%)')
                    
                    st.markdown(f"""
                        <div style="background: {gradient}; margin: 10px 20px;
                                  padding: 15px; border-radius: 15px; color: white;
                                  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                                  transform: translateY(0);
                                  transition: all 0.3s ease;">
                            <h4 style="margin: 0;">{app['company']}</h4>
                            <p style="margin: 5px 0;"><strong>Position:</strong> {app['position']}</p>
                            <p style="margin: 5px 0;"><strong>Status:</strong> {app['status']}</p>
                            <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.2);
                                      border-radius: 2px; margin-top: 10px;">
                                <div style="width: {get_progress_width(app['status'])}%;
                                          height: 100%; background: white;
                                          border-radius: 2px;"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

def render_stats(data):
    st.markdown('<h1 class="custom-header">Application Analytics</h1>', unsafe_allow_html=True)
    
    if not data.empty:
        # Advanced Analytics Dashboard
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            fig1 = px.pie(data, names='status', 
                         title='Application Status Distribution',
                         color_discrete_sequence=['#2196F3', '#FFA726', '#66BB6A'],
                         hole=0.4)
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            data['created_at'] = pd.to_datetime(data['created_at'])
            weekly_apps = data.groupby([pd.Grouper(key='created_at', freq='W'), 'status']).size().reset_index()
            weekly_apps.columns = ['week', 'status', 'count']
            
            fig2 = px.bar(weekly_apps, x='week', y='count', color='status',
                         title='Weekly Application Progress',
                         color_discrete_sequence=['#2196F3', '#FFA726', '#66BB6A'])
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

def get_progress_width(status):
    return {
        'Applied': 33,
        'Interviewed': 66,
        'Offered': 100
    }.get(status, 0)

def render_card(row, status_class="status-applied"):
    card_html = f"""
        <div class="dashboard-card {status_class}">
            <div class="card-content">
                <h4 style="color: #1a1a1a; margin: 0;">{row['company']}</h4>
                <p style="color: #4a4a4a; margin: 8px 0;">
                    <strong>Position:</strong> {row['position']}
                </p>
                <p style="color: #4a4a4a; margin: 8px 0;">
                    <strong>Deadline:</strong> {row['deadline']}
                </p>
                <div class="progress-bar" style="width: {get_progress_width(row['status'])}%"></div>
            </div>
        </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    return col1, col2
