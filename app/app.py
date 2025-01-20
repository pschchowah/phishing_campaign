import streamlit as st

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


def login_page():
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.title("Phishing Campaign Manager")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "BOUMAN-8":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Invalid credentials")


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
