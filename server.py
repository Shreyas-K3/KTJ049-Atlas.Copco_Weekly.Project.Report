import streamlit as st

st.set_page_config(
    page_title="Atlas Copco - Admin / Server",
    page_icon="🛠️",
    layout="centered",
)

st.title("🛠️ Admin / Server – Access Settings")
st.caption("Set pre-approved names and the project access code. The client app will use these for login.")

# --- Safe import of data_store ---
try:
    from data_store import load_data, save_data, DEFAULT_DATA
except Exception as e:
    st.error(
        "❌ Could not import `data_store.py`.\n\n"
        "Make sure a file named **data_store.py** exists in the same folder as `server.py`."
    )
    st.code(str(e))
    st.stop()

# --- Load current data safely ---
try:
    data = load_data()
except Exception as e:
    st.warning("⚠️ Could not load existing data. Using default settings.")
    st.code(str(e))
    data = DEFAULT_DATA.copy()

st.markdown("---")

st.subheader("🔐 Access Control")

with st.form("access_form", clear_on_submit=False):
    # Project access code
    project_code = st.text_input(
        "Project Access Code",
        value=data.get("project_code", "ATLAS2025"),
        help="Users must enter this code on the client app to access the dashboard."
    )

    # Pre-approved names list
    allowed_names_str = "\n".join(data.get("allowed_names", []))
    allowed_names_input = st.text_area(
        "Pre-approved Names (one per line)",
        value=allowed_names_str,
        height=200,
        help="Only these names will be allowed to log in on the client dashboard."
    )

    st.markdown(
        "<small>🔎 Name on client side must exactly match one of the lines above (case-insensitive check).</small>",
        unsafe_allow_html=True,
    )

    # CLEAR submit button
    submitted = st.form_submit_button("✅ SAVE ACCESS SETTINGS")

if submitted:
    # Clean and split names
    names_list = [
        n.strip() for n in allowed_names_input.splitlines()
        if n.strip()
    ]

    data["project_code"] = project_code.strip()
    data["allowed_names"] = names_list

    try:
        save_data(data)
        st.success("✅ Access settings saved successfully!")
        st.write("**Current project code:**", data["project_code"])
        st.write("**Pre-approved names:**", data["allowed_names"])
    except Exception as e:
        st.error("❌ Failed to save settings.")
        st.code(str(e))

st.markdown("---")
st.info(
    "✔️ Now, on the **client app**, login will only work if:\n"
    "- Name is in the pre-approved list\n"
    "- Project code matches the one you set here"
)
