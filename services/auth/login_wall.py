import streamlit as st

def render_login():
    if st.session_state.get("user_id") is not None:
        return True

    st.title("AI Real-time GYM Trainer")
    st.markdown("Enter your username to start")

    with st.form("login_form",clear_on_submit=False):
        username=st.text_input("Name (unique)",placeholder="unique name")
        submit_button=st.form_submit_button("start session",width="stretch")
    if submit_button:
        if not username:
            st.error("Name cannot be empty.")
            return False
        st.session_state['username']=username
        st.session_state['user_id']="1"
        st.rerun()
    return False