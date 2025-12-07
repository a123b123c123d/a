import streamlit as st
from eduassist.services.auth_service import (
    create_user, authenticate_user, 
    generate_reset_token, reset_password_with_token,
    get_user_by_email, BRANCHES, ROLES
)
from eduassist.services.translation_service import translate_text

def render_auth_page():
    lang = st.session_state.get('selected_language', 'english')
    
    if st.session_state.get('user'):
        render_profile(lang)
    else:
        auth_mode = st.session_state.get('show_auth_modal', 'login')
        
        tab_names = [
            translate_text("Login", lang),
            translate_text("Sign Up", lang),
            translate_text("Forgot Password", lang)
        ]
        
        default_idx = 0
        if auth_mode == 'signup':
            default_idx = 1
        
        tab1, tab2, tab3 = st.tabs(tab_names)
        
        with tab1:
            render_login_form(lang)
        
        with tab2:
            render_signup_form(lang)
        
        with tab3:
            render_forgot_password_form(lang)

def render_login_form(lang):
    st.markdown(f"### {translate_text('Login to Your Account', lang)}")
    
    with st.form("login_form"):
        username_or_email = st.text_input(translate_text("Username or Email", lang))
        password = st.text_input(translate_text("Password", lang), type="password")
        
        submitted = st.form_submit_button(translate_text("Login", lang), use_container_width=True)
        
        if submitted:
            if not username_or_email or not password:
                st.error(translate_text("Please fill in all fields", lang))
            else:
                user, error = authenticate_user(username_or_email, password)
                if user:
                    st.session_state.user = user
                    st.session_state.current_page = 'home'
                    st.success(f"{translate_text('Welcome back', lang)}, {user['full_name']}!")
                    st.rerun()
                else:
                    st.error(translate_text(error or "Login failed", lang))

def render_signup_form(lang):
    st.markdown(f"### {translate_text('Create a New Account', lang)}")
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input(translate_text("Username", lang) + "*")
            email = st.text_input(translate_text("Email", lang) + "*")
            password = st.text_input(translate_text("Password", lang) + "*", type="password")
        
        with col2:
            full_name = st.text_input(translate_text("Full Name", lang) + "*")
            branch = st.selectbox(translate_text("Branch/Department", lang) + "*", BRANCHES)
            confirm_password = st.text_input(translate_text("Confirm Password", lang) + "*", type="password")
        
        role = st.selectbox(translate_text("I am a...", lang), ["student", "teacher"])
        
        submitted = st.form_submit_button(translate_text("Sign Up", lang), use_container_width=True)
        
        if submitted:
            if not all([username, email, password, full_name, branch, confirm_password]):
                st.error(translate_text("Please fill in all required fields", lang))
            elif password != confirm_password:
                st.error(translate_text("Passwords do not match", lang))
            elif len(password) < 6:
                st.error(translate_text("Password must be at least 6 characters", lang))
            elif "@" not in email:
                st.error(translate_text("Please enter a valid email address", lang))
            else:
                user, error = create_user(username, email, password, full_name, branch, role)
                if user:
                    st.session_state.user = user
                    st.session_state.current_page = 'home'
                    st.success(translate_text("Account created successfully! You are now logged in.", lang))
                    st.rerun()
                else:
                    st.error(translate_text(error or "Registration failed", lang))

def render_forgot_password_form(lang):
    st.markdown(f"### {translate_text('Reset Your Password', lang)}")
    
    if st.session_state.get('reset_token_sent'):
        st.info(translate_text("A reset token has been generated. In a real app, this would be sent via email.", lang))
        
        with st.form("reset_password_form"):
            token = st.text_input(translate_text("Reset Token", lang))
            new_password = st.text_input(translate_text("New Password", lang), type="password")
            confirm_password = st.text_input(translate_text("Confirm New Password", lang), type="password")
            
            submitted = st.form_submit_button(translate_text("Reset Password", lang), use_container_width=True)
            
            if submitted:
                if not all([token, new_password, confirm_password]):
                    st.error(translate_text("Please fill in all fields", lang))
                elif new_password != confirm_password:
                    st.error(translate_text("Passwords do not match", lang))
                elif len(new_password) < 6:
                    st.error(translate_text("Password must be at least 6 characters", lang))
                else:
                    success, message = reset_password_with_token(token, new_password)
                    if success:
                        st.success(translate_text(message, lang))
                        st.session_state.reset_token_sent = False
                        st.rerun()
                    else:
                        st.error(translate_text(message, lang))
        
        if st.button(translate_text("Request New Token", lang)):
            st.session_state.reset_token_sent = False
            st.rerun()
    else:
        with st.form("forgot_password_form"):
            email = st.text_input(translate_text("Enter your email address", lang))
            
            submitted = st.form_submit_button(translate_text("Send Reset Token", lang), use_container_width=True)
            
            if submitted:
                if not email:
                    st.error(translate_text("Please enter your email", lang))
                else:
                    user = get_user_by_email(email)
                    if user:
                        token = generate_reset_token(email)
                        if token:
                            st.session_state.reset_token = token
                            st.session_state.reset_token_sent = True
                            st.info(f"{translate_text('Reset token (for demo)', lang)}: {token}")
                            st.rerun()
                    else:
                        st.error(translate_text("No account found with this email", lang))

def render_profile(lang):
    user = st.session_state.user
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); border-radius: 50%; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 2rem; color: white;">{user['full_name'][0].upper()}</span>
            </div>
            <h2 style="margin-bottom: 0.5rem;">{translate_text('Welcome', lang)}, {user['full_name']}!</h2>
            <p style="color: #a1a1aa;">{user['email']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{translate_text('Username', lang)}</div>
                <div style="color: #f5f5f7; font-size: 1.1rem; margin-top: 0.5rem;">@{user['username']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{translate_text('Branch', lang)}</div>
                <div style="color: #f5f5f7; font-size: 1.1rem; margin-top: 0.5rem;">{user.get('branch', 'Not set')}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">{translate_text('Role', lang)}</div>
                <div style="color: #6366f1; font-size: 1.1rem; margin-top: 0.5rem; font-weight: 600;">{translate_text(user['role'].title(), lang)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if user['role'] == 'admin':
            st.markdown(f"""
                <div class="stat-card" style="border-color: #6366f1;">
                    <div class="stat-label">{translate_text('Admin Access', lang)}</div>
                    <div style="color: #22c55e; font-size: 1.1rem; margin-top: 0.5rem;">{translate_text('Enabled', lang)}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(translate_text("Logout", lang), use_container_width=True):
        st.session_state.user = None
        st.success(translate_text("Logged out successfully!", lang))
        st.rerun()
