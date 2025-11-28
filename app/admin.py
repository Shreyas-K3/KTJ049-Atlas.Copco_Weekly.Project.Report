import streamlit as st
import pandas as pd
import time
from app.db import upsert_project, get_project_by_code, list_project_codes, list_comments
from app.utils import load_css

def app():
    load_css("app/style.css")
    st.title("Admin Panel 🛠️")

    # --- Select Project ---
    existing_codes = list_project_codes()
    mode = st.radio("Mode", ["Edit Existing", "Create New"], horizontal=True)
    
    selected_code = None
    project_data = {}

    if mode == "Edit Existing":
        if not existing_codes:
            st.warning("No projects found. Create one.")
            mode = "Create New" # Fallback
        else:
            selected_code = st.selectbox("Select Project Code", existing_codes)
            if selected_code:
                # Load existing data
                p_obj = get_project_by_code(selected_code)
                if p_obj:
                    project_data = p_obj.__dict__

    # --- Form ---
    with st.form("project_form"):
        st.subheader("Project Details")
        
        # We use simple keys to map to DB columns
        c1, c2 = st.columns(2)
        p_code = c1.text_input("Project Code (Secret)", value=project_data.get("project_code", ""))
        p_name = c2.text_input("Project Name", value=project_data.get("project_name", ""))
        
        title = st.text_input("Title", value=project_data.get("title", "Weekly Project Update"))
        
        c3, c4, c5 = st.columns(3)
        prog = c3.number_input("Progress (%)", 0, 100, value=project_data.get("project_progress", 0))
        rfi = c4.number_input("Pending RFI", value=project_data.get("pending_rfi", 0))
        days = c5.number_input("Days Spent", value=project_data.get("days_spent", 0))
        
        link1 = st.text_input("Model Review Link", value=project_data.get("model_review_link", ""))
        link2 = st.text_input("RFI Sheet Link", value=project_data.get("rfi_sheet_link", ""))
        
        alert = st.text_input("Alert Note (Bold)", value=project_data.get("alert_note", ""))
        
        curr_prog = st.text_area("Current Progress", value=project_data.get("current_progress", ""))
        next_plan = st.text_area("Next Week Plan", value=project_data.get("next_week_plan", ""))

        submitted = st.form_submit_button("Update Project")

        if submitted:
            if not p_code or not p_name:
                st.error("Project Code and Name are required.")
            else:
                data = {
                    "project_code": p_code,
                    "project_name": p_name,
                    "title": title,
                    "project_progress": prog,
                    "pending_rfi": rfi,
                    "days_spent": days,
                    "model_review_link": link1,
                    "rfi_sheet_link": link2,
                    "alert_note": alert,
                    "current_progress": curr_prog,
                    "next_week_plan": next_plan
                }
                upsert_project(data)
                st.success(f"Project '{p_name}' saved successfully!")
                time.sleep(1)
                st.rerun()

    # --- Live Comments View ---
    if mode == "Edit Existing" and selected_code:
        st.markdown("---")
        st.subheader(f"Live Comments: {selected_code}")
        
        # Auto-refresh mechanism (Polling)
        if st.toggle("Auto-refresh comments (10s)", value=True):
            time.sleep(10)
            st.rerun()

        comments = list_comments(selected_code)
        if comments:
            df = pd.DataFrame(comments)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No comments yet.")
