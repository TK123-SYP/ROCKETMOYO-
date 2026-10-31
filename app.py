
import streamlit as st

st.set_page_config(
    page_title="ROCKETMOYO",
    page_icon="⚾",
    layout="wide"
)

dashboard_page = st.Page(
    "dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True
)
#manual page
manual_page = st.Page(
    "pages/1_Manual_Analysis.py",
    title="Manual Player Analysis",
    icon="⚾"
)
#report page
reports_page = st.Page(
    "pages/2_Player_Reports.py",
    title="Player Performance Reports",
    icon="📄"
)
pg = st.navigation({
    "ROCKETMOYO": [dashboard_page, manual_page, reports_page]
})

pg.run()
