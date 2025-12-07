"""Theme and styling configuration - Minimal, elegant, expensive design."""

import streamlit as st


MODERN_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #ffffff;
    --bg-secondary: #fafafa;
    --bg-card: #ffffff;
    --bg-card-hover: #f9f9f9;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --text-muted: #999999;
    --accent-primary: #1a1a1a;
    --accent-secondary: #333333;
    --accent-green: #22c55e;
    --accent-orange: #f59e0b;
    --accent-red: #ef4444;
    --border-color: #e5e5e5;
    --border-light: #f0f0f0;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.08);
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp > header {
    background: transparent !important;
}

.top-bar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 2rem;
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.logo-icon {
    width: 40px;
    height: 40px;
    background: var(--accent-primary);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 1rem;
}

.logo-text {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
}

.nav-section {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.lang-selector {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: var(--bg-secondary);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    font-size: 0.875rem;
    color: var(--text-secondary);
    cursor: pointer;
}

.main-header {
    padding: 3rem 0 2rem 0;
    margin-bottom: 2rem;
}

.main-header .label {
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.main-header h1 {
    font-size: 3rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin-bottom: 1rem !important;
    line-height: 1.1 !important;
}

.main-header p {
    font-size: 1.125rem !important;
    color: var(--text-secondary) !important;
    line-height: 1.6 !important;
    max-width: 600px;
}

.section-title {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    margin-bottom: 1.5rem !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
}

.section-title::before {
    display: none !important;
}

.section-counter {
    font-size: 0.75rem;
    color: var(--text-muted);
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.app-card {
    background: var(--bg-card);
    padding: 2rem;
    position: relative;
    border-bottom: 1px solid var(--border-color);
    border-right: 1px solid var(--border-color);
    transition: background 0.2s ease;
}

.app-card:hover {
    background: var(--bg-card-hover);
}

.app-card:nth-child(2n) {
    border-right: none;
}

.app-card:nth-last-child(-n+2) {
    border-bottom: none;
}

.app-card-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.app-card-badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: var(--accent-primary);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: var(--radius-sm);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.app-card h3 {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.75rem !important;
}

.app-card p {
    font-size: 0.9rem !important;
    color: var(--text-secondary) !important;
    line-height: 1.5 !important;
    margin-bottom: 1.5rem !important;
}

.app-card-link {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-primary);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: gap 0.2s ease;
}

.app-card-link:hover {
    gap: 0.75rem;
}

.app-card-link .arrow {
    font-size: 1rem;
}

.subject-card {
    background: var(--bg-card);
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    margin: 0.75rem 0;
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
}

.subject-card:hover {
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-sm);
}

.subject-card h4 {
    color: var(--text-primary) !important;
    margin-bottom: 0.75rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

.subject-card p {
    color: var(--text-secondary) !important;
    font-size: 0.875rem !important;
}

.results-card {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-color);
    margin: 1.5rem 0;
    box-shadow: var(--shadow-sm);
}

.forum-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.forum-card:hover {
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-sm);
}

.forum-card h4 {
    color: var(--text-primary) !important;
    margin: 0.75rem 0 !important;
    font-weight: 600 !important;
}

.forum-card .category-tag {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    border: 1px solid var(--border-color);
}

.forum-card .meta {
    color: var(--text-muted);
    font-size: 0.85rem;
}

div[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-color) !important;
}

div[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

div[data-testid="stSidebar"] h2 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
}

.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within {
    border-color: var(--accent-primary) !important;
}

.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: none !important;
}

.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
}

.stButton > button {
    background: var(--accent-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
    font-size: 0.875rem !important;
}

.stButton > button:hover {
    background: var(--accent-secondary) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: var(--bg-secondary) !important;
    border-color: var(--accent-primary) !important;
}

.login-btn {
    background: transparent !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

.login-btn:hover {
    background: var(--bg-secondary) !important;
}

.signup-btn {
    background: var(--accent-primary) !important;
    color: white !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-radius: var(--radius-lg) !important;
    padding: 0.25rem !important;
    gap: 0.25rem !important;
    border: 1px solid var(--border-color) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 0.875rem !important;
}

.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    box-shadow: var(--shadow-sm) !important;
}

div[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.25rem !important;
    margin: 0.75rem 0 !important;
}

.stAlert {
    border-radius: var(--radius-md) !important;
}

div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
}

.stRadio > label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.stRadio > div {
    gap: 0.5rem !important;
}

div[data-testid="stTable"] {
    background: var(--bg-card) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    border: 1px solid var(--border-color) !important;
}

div[data-testid="stTable"] th {
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

div[data-testid="stTable"] td {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.stForm {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.5rem !important;
}

hr {
    border-color: var(--border-color) !important;
    margin: 2rem 0 !important;
}

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    text-align: center;
}

.stat-card .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
}

.stat-card .stat-label {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-top: 0.5rem;
}

.login-badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: var(--accent-primary);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: var(--radius-sm);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeIn 0.3s ease-out;
}

.stLinkButton > a {
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
}

.stLinkButton > a:hover {
    background: var(--bg-card-hover) !important;
    border-color: var(--accent-primary) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    padding-top: 1rem !important;
}
</style>
"""


def apply_theme():
    """Apply the modern minimal theme CSS to the Streamlit app."""
    st.markdown(MODERN_THEME_CSS, unsafe_allow_html=True)
