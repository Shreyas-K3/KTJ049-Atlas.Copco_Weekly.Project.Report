import streamlit as st

def load_css(file_name):
    """Loads custom CSS file."""
    # Use st.file_contents for safe path handling on Streamlit Cloud
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: Could not find CSS file at {file_name}")

def roadmap_svg(size="32"): # Changed default size to match client.py usage
    """Returns a simple SVG icon for a roadmap/journey."""
    # Added inline style for better text alignment
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#FF0000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="roadmap-icon" style="vertical-align: middle; margin-right: 8px;">
        <path d="M12 22s-8-4-8-10c0-4.4 3.6-8 8-8s8 3.6 8 8c0 6-8 10-8 10z"></path>
        <circle cx="12" cy="10" r="3"></circle>
        <path d="M12 10l0 12"></path>
    </svg>
    """

def create_circular_meter(label, value, max_value, color):
    """Generates custom HTML/CSS for a circular meter."""
    # Safety check to prevent ZeroDivisionError if max_value is 0
    if max_value == 0:
        percentage = 0
    else:
        percentage = (value / max_value) * 100
        
    if percentage > 100: percentage = 100 # Cap at 100% for display
    
    # CSS for the meter is in style.css, this just generates the HTML structure
    return f"""
    <div class="meter-card">
        <div class="circular-meter" style="--p:{percentage}; --c:{color};">
            <div class="meter-label">{label}</div>
            <div class="meter-value">{value}{'%' if max_value == 100 else ''}</div>
        </div>
    </div>
    """
