import streamlit as st

st.logo("app/phish_clicks_logo/png/phish-n-clicks-logo-hori-purple.png", size="large")
# Loading CSS style
st.markdown(
    "<style>" + open("app/style.css").read() + "</style>", unsafe_allow_html=True
)

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


def login_page():
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.title("Phishing Campaign Manager")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        # Fetch credentials from Streamlit secrets
        stored_username = st.secrets["authentication"]["username"]
        stored_password = st.secrets["authentication"]["password"]

        if login_button:
            if username == stored_username and password == stored_password:
                st.session_state["authenticated"] = True
            else:
                st.error("Invalid username or password")


if not st.session_state["authenticated"]:
    login_page()
else:
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    # Navigation
    navigation = st.navigation(
        [
            st.Page("app_pages/homepage.py", title="Campaign Launch"),
            st.Page("app_pages/events_overview.py", title="Events Overview"),
            st.Page("app_pages/email_dashboard.py", title="Email Dashboard"),
        ]
    )
    navigation.run()
