"""Reusable UI components for the application."""

import streamlit as st
from typing import Dict, Tuple
from ..config.settings import Settings
from ..services.translation_service import (
    translate_text, get_available_languages, 
    LANGUAGE_NAMES, LANGUAGE_NATIVE
)


def render_top_bar():
    """Render the top navigation bar with logo, language selector and auth buttons."""
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; border-bottom: 1px solid #e5e5e5; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 36px; height: 36px; background: #1a1a1a; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.875rem;">JE</div>
                <span style="font-size: 1rem; font-weight: 600; color: #1a1a1a;">JNTU EduAssist</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])
    
    with col2:
        render_language_dropdown()
    
    with col3:
        render_auth_buttons_login()
    
    with col4:
        render_auth_buttons_signup()


def render_language_dropdown():
    """Render globe icon language selector."""
    languages = list(LANGUAGE_NAMES.keys())
    current_lang = st.session_state.get('selected_language', 'english')
    
    selected = st.selectbox(
        "Language",
        options=languages,
        index=languages.index(current_lang) if current_lang in languages else 0,
        format_func=lambda x: f"{LANGUAGE_NATIVE.get(x, x).upper()[:3]}",
        key="lang_dropdown",
        label_visibility="collapsed"
    )
    
    if selected != current_lang:
        st.session_state.selected_language = selected
        st.rerun()


def render_auth_buttons_login():
    """Render login button."""
    user = st.session_state.get('user')
    
    if user:
        if st.button("Logout", key="top_logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("LOGIN", key="top_login", use_container_width=True):
            st.session_state.show_auth_modal = "login"
            st.session_state.current_page = "auth"
            st.rerun()


def render_auth_buttons_signup():
    """Render signup button."""
    user = st.session_state.get('user')
    
    if user:
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: center; padding: 8px 0; font-size: 0.875rem;">
                <span style="color: #1a1a1a; font-weight: 500;">{user['full_name'][:10]}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("SIGN UP", key="top_signup", use_container_width=True):
            st.session_state.show_auth_modal = "signup"
            st.session_state.current_page = "auth"
            st.rerun()


def render_auth_buttons():
    """Render login/signup buttons or welcome message."""
    user = st.session_state.get('user')
    
    if user:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: flex-end; gap: 8px; padding: 8px 0;">
                    <span style="color: #666;">Welcome,</span>
                    <span style="color: #1a1a1a; font-weight: 600;">{user['full_name']}</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Logout", key="top_logout_alt", use_container_width=True):
                st.session_state.user = None
                st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="top_login_alt", use_container_width=True):
                st.session_state.show_auth_modal = "login"
                st.session_state.current_page = "auth"
        with col2:
            if st.button("Sign Up", key="top_signup_alt", use_container_width=True):
                st.session_state.show_auth_modal = "signup"
                st.session_state.current_page = "auth"


def render_header():
    """Render the main application header."""
    lang = st.session_state.get('selected_language', 'english')
    title = translate_text("JNTU EduAssist AI", lang)
    subtitle = translate_text("Your Multilingual Educational Assistant for JNTU Students. Advanced AI-powered platform designed to provide instant answers, study materials, and comprehensive academic support.", lang)
    label = translate_text("EDUCATIONAL PLATFORM", lang)
    
    st.markdown(f"""
        <div class="main-header">
            <div class="label" style="font-size: 0.75rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #999; margin-bottom: 1rem;">{label}</div>
            <h1 style="font-size: 2.75rem; font-weight: 600; color: #1a1a1a; margin-bottom: 1rem; line-height: 1.1;">{title}</h1>
            <p style="font-size: 1rem; color: #666; line-height: 1.6; max-width: 550px;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def render_language_selector() -> str:
    """Legacy language selector - now uses dropdown."""
    return st.session_state.get('selected_language', 'english')


def render_dashboard():
    """Render the dashboard with app cards."""
    lang = st.session_state.get('selected_language', 'english')
    user = st.session_state.get('user')
    
    dashboard_title = translate_text("YOUR LEARNING DASHBOARD", lang)
    
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; margin-top: 2rem;">
            <span style="font-size: 0.75rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #999;">{dashboard_title}</span>
            <span style="font-size: 0.75rem; color: #999;">01</span>
        </div>
    """, unsafe_allow_html=True)
    
    apps = [
        {
            "number": "01",
            "title": translate_text("Ask Questions", lang),
            "desc": translate_text("Get instant answers to your coursework with AI-powered assistance built on semantic search technology.", lang),
            "key": "ask",
            "requires_login": False,
            "badge": None
        },
        {
            "number": "02",
            "title": translate_text("Check Results", lang),
            "desc": translate_text("Fetch your academic results directly from JNTUH servers quickly and easily.", lang),
            "key": "results",
            "requires_login": False,
            "badge": "NEW"
        },
        {
            "number": "03",
            "title": translate_text("Practice Questions", lang),
            "desc": translate_text("Generate practice questions to test your knowledge and prepare for exams.", lang),
            "key": "practice",
            "requires_login": False,
            "badge": None
        },
        {
            "number": "04",
            "title": translate_text("Discussion Forum", lang),
            "desc": translate_text("Connect with fellow students and teachers to discuss academics and share knowledge.", lang),
            "key": "forum",
            "requires_login": True,
            "badge": None
        }
    ]
    
    st.markdown('<div style="border: 1px solid #e5e5e5; border-radius: 12px; overflow: hidden;">', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, app in enumerate(apps):
        with cols[idx % 2]:
            badge_html = ""
            if app["badge"]:
                badge_html = f'<div style="position: absolute; top: 1.5rem; right: 1.5rem; background: #1a1a1a; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.05em;">{app["badge"]}</div>'
            elif app["requires_login"]:
                badge_text = translate_text("LOGIN", lang)
                badge_html = f'<div style="position: absolute; top: 1.5rem; right: 1.5rem; background: #1a1a1a; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.05em;">{badge_text}</div>'
            
            service_label = translate_text("SERVICE", lang)
            open_text = translate_text("OPEN", lang)
            
            st.markdown(f"""
                <div style="background: white; padding: 2rem; position: relative; border-bottom: 1px solid #e5e5e5; min-height: 200px;">
                    {badge_html}
                    <div style="font-size: 0.7rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; color: #999; margin-bottom: 1rem;">{service_label} {app["number"]}</div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.75rem;">{app["title"]}</h3>
                    <p style="font-size: 0.875rem; color: #666; line-height: 1.5; margin-bottom: 1.5rem;">{app["desc"]}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"{open_text} \u2192", key=f"open_{app['key']}", use_container_width=True):
                if app["requires_login"] and not user:
                    st.session_state.show_auth_modal = "login"
                    st.session_state.current_page = "auth"
                else:
                    st.session_state.active_tab = app["key"]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def get_icon_svg(icon_name: str) -> str:
    """Return icon character for app cards."""
    icons = {
        "chat_bubble": "Q",
        "assessment": "R",
        "quiz": "P",
        "forum": "F"
    }
    return icons.get(icon_name, "?")


def render_course_selector(
    degree_options: Dict,
    get_branch_options_fn,
    get_year_options_fn,
    get_semester_options_fn,
    courses: Dict
) -> Tuple[str, str, str, str, Dict]:
    """Render course selection UI."""
    lang = st.session_state.get('selected_language', 'english')
    
    section_title = translate_text("SELECT YOUR COURSE", lang)
    
    st.markdown(f"""
        <div style="font-size: 0.75rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #999; margin-bottom: 1rem; margin-top: 2rem;">{section_title}</div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_degree = st.selectbox(
            translate_text("Degree Type", lang),
            options=[""] + list(degree_options.keys()),
            format_func=lambda x: translate_text("Select Degree", lang) if x == "" else degree_options.get(x, x),
            key="degree_select"
        )
    
    branch_options = get_branch_options_fn(courses, selected_degree) if selected_degree else {}
    
    with col2:
        branch_keys = list(branch_options.keys())
        selected_branch = st.selectbox(
            translate_text("Branch", lang),
            options=[""] + branch_keys,
            format_func=lambda x: translate_text("Select Branch", lang) if x == "" else f"{branch_options.get(x, {}).get('abbreviation', x)} - {branch_options.get(x, {}).get('name', x)}",
            key="branch_select",
            disabled=not selected_degree
        )
    
    year_options = get_year_options_fn(courses, selected_degree, selected_branch) if selected_branch else {}
    
    with col3:
        selected_year = st.selectbox(
            translate_text("Year", lang),
            options=[""] + list(year_options.keys()),
            format_func=lambda x: translate_text("Select Year", lang) if x == "" else year_options.get(x, x),
            key="year_select",
            disabled=not selected_branch
        )
    
    semester_options = get_semester_options_fn(courses, selected_degree, selected_branch, selected_year) if selected_year else {}
    
    with col4:
        selected_semester = st.selectbox(
            translate_text("Semester", lang),
            options=[""] + list(semester_options.keys()),
            format_func=lambda x: translate_text("Select Semester", lang) if x == "" else semester_options.get(x, x),
            key="semester_select",
            disabled=not selected_year
        )
    
    return selected_degree, selected_branch, selected_year, selected_semester, branch_options


def render_subject_card(subject_key: str, subject_data: Dict):
    """Render a subject card with links."""
    lang = st.session_state.get('selected_language', 'english')
    
    st.markdown(f"""
        <div class="subject-card">
            <h4 style="font-size: 1.1rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.5rem;">{subject_data.get('name', subject_key)}</h4>
            <p style="font-size: 0.875rem; color: #666;"><strong>{translate_text("Code", lang)}:</strong> {subject_data.get('code', 'N/A')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    link_col1, link_col2, link_col3 = st.columns(3)
    with link_col1:
        st.link_button(translate_text("Syllabus", lang), subject_data.get('syllabus_link', '#'), use_container_width=True)
    with link_col2:
        st.link_button(translate_text("Notes", lang), subject_data.get('notes_link', '#'), use_container_width=True)
    with link_col3:
        st.link_button(translate_text("Papers", lang), subject_data.get('previous_papers_link', '#'), use_container_width=True)
    
    topics = subject_data.get('topics', [])
    if topics:
        with st.expander(translate_text("View Topics", lang)):
            topic_list = ", ".join([topic.replace("_", " ").title() for topic in topics])
            st.write(topic_list)


def render_sidebar(
    selected_degree: str,
    selected_branch: str,
    selected_year: str,
    selected_semester: str,
    degree_options: Dict,
    branch_options: Dict,
    year_options: Dict,
    semester_options: Dict
):
    """Render the sidebar with quick info and tips."""
    lang = st.session_state.get('selected_language', 'english')
    
    with st.sidebar:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <div style="width: 28px; height: 28px; background: #1a1a1a; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.75rem;">JE</div>
                <span style="font-size: 0.9rem; font-weight: 600; color: #1a1a1a;">{translate_text('JNTU EduAssist', lang)}</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown(f"### {translate_text('Quick Info', lang)}")
        if selected_degree:
            st.success(f"**{translate_text('Degree', lang)}:** {degree_options.get(selected_degree, '')}")
        if selected_branch and selected_branch in branch_options:
            branch_info = branch_options[selected_branch]
            st.info(f"**{translate_text('Branch', lang)}:** {branch_info.get('abbreviation', '')} ({branch_info.get('name', '')})")
        if selected_year:
            st.write(f"**{translate_text('Year', lang)}:** {year_options.get(selected_year, '')}")
        if selected_semester:
            st.write(f"**{translate_text('Semester', lang)}:** {semester_options.get(selected_semester, '')}")
        
        st.markdown("---")
        st.markdown(f"### {translate_text('Tips', lang)}")
        st.markdown(f"""
        - {translate_text('Select your course details first', lang)}
        - {translate_text('Use the Results tab to check grades', lang)}
        - {translate_text('Generate practice questions', lang)}
        - {translate_text('Ask questions in chat', lang)}
        """)
        
        st.markdown("---")
        if st.button(translate_text("Clear Chat History", lang), use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown(f"### {translate_text('About', lang)}")
        st.markdown(f"""
        **JNTU EduAssist AI** {translate_text('helps JNTUH students with', lang)}:
        - {translate_text('Course materials & syllabi', lang)}
        - {translate_text('Academic results lookup', lang)}
        - {translate_text('Practice question generation', lang)}
        - {translate_text('Q&A assistance', lang)}
        """)
