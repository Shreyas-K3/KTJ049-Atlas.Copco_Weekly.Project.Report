import streamlit as st
import time
from app.db import get_project_by_code, add_comment
from app.utils import load_css

def app():
    load_css("app/style.css")

    # --- Authentication State ---
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.project_data = None

    # --- Login Screen ---
    if not st.session_state.logged_in:
        st.title("Client Login")
        col1, col2 = st.columns(2)
        with col1:
            name_input = st.text_input("Your Name")
        with col2:
            code_input = st.text_input("Project Code", type="password") # Hidden for shoulder surfing

        if st.button("View Dashboard"):
            if code_input and name_input:
                project = get_project_by_code(code_input)
                if project:
                    st.session_state.logged_in = True
                    st.session_state.client_name = name_input
                    st.session_state.project_code = code_input
                    st.rerun()
                else:
                    st.error("Invalid Project Code.")
            else:
                st.warning("Please enter name and code.")
        return

    # --- Dashboard ---
    # Refresh data on load
    project = get_project_by_code(st.session_state.project_code)
    
    # If project code changed by admin and client is active, this handles the kick-out
    if not project:
        st.error("Project not found. Code may have changed.")
        if st.button("Back to Login"):
            st.session_state.logged_in = False
            st.rerun()
        return

    # Header
    st.title(project.project_name)
    st.caption(project.title)
    st.markdown("---")

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Overall Progress", f"{project.project_progress}%")
        st.progress(project.project_progress / 100)
    with c2:
        st.metric("Pending RFI", project.pending_rfi)
    with c3:
        st.metric("Days Spent", project.days_spent)

    # Links Row
    st.markdown("<br>", unsafe_allow_html=True)
    l1, l2 = st.columns(2)
    with l1:
        if project.model_review_link:
            st.link_button("🏗️ Review Model", project.model_review_link, use_container_width=True)
    with l2:
        if project.rfi_sheet_link:
            st.link_button("📋 RFI Sheet", project.rfi_sheet_link, use_container_width=True)

    # Alert Note
    if project.alert_note:
        st.markdown(f"""
        <div class="alert-box">
            🔔 {project.alert_note}
        </div>
        """, unsafe_allow_html=True)

    # Text Content
    st.subheader("Current Progress")
    st.info(project.current_progress or "No updates yet.")

    st.subheader("Next Week Plan")
    st.info(project.next_week_plan or "No updates yet.")

    st.markdown("---")
    st.write("Feedback and inputs are welcome. For any clarifications or additional details, feel free to reach out.")

    # Interaction Section
    with st.expander("Submit Feedback", expanded=True):
        reviewed = st.checkbox("I have reviewed the model")
        
        # Disable/Enable logic
        if reviewed:
            comment_text = st.text_area("Your Comment (Optional)", key="user_comment")
            if st.button("Submit Feedback"):
                if comment_text.strip():
                    add_comment(
                        project.project_code,
                        st.session_state.client_name,
                        comment_text
                    )
                    st.success("Feedback submitted successfully!")
                    # Prevent re-submission or editing
                    st.empty()
                else:
                    st.warning("Please write a comment before submitting.")
        else:
            st.text_area("Your Comment", disabled=True, placeholder="Please check 'I have reviewed the model' first.")
            st.button("Submit Feedback", disabled=True)
