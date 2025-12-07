import bcrypt
import secrets
from datetime import datetime, timedelta
from eduassist.data.database import get_db

BRANCHES = [
    "CSE",
    "CSE (AI & ML)",
    "CSE (Cyber Security)",
    "CSE (Data Science)",
    "ECE",
    "EEE",
    "MECH",
    "CIVIL",
    "CHEMICAL",
    "IT",
    "Aeronautical",
    "Other"
]

ROLES = ["student", "teacher", "admin"]

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_user(username: str, email: str, password: str, full_name: str, branch: str, role: str = "student"):
    password_hash = hash_password(password)
    
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, branch, role)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, username, email, full_name, branch, role
            """, (username, email, password_hash, full_name, branch, role))
            
            user = cursor.fetchone()
            conn.commit()
            return dict(user), None
        except Exception as e:
            if "duplicate key" in str(e).lower():
                if "username" in str(e).lower():
                    return None, "Username already exists"
                elif "email" in str(e).lower():
                    return None, "Email already exists"
            return None, str(e)

def authenticate_user(username_or_email: str, password: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, password_hash, full_name, branch, role
            FROM users
            WHERE username = %s OR email = %s
        """, (username_or_email, username_or_email))
        
        user = cursor.fetchone()
        
        if user and verify_password(password, user['password_hash']):
            user_dict = dict(user)
            del user_dict['password_hash']
            return user_dict, None
        
        return None, "Invalid credentials"

def get_user_by_id(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, full_name, branch, role, created_at
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        return dict(user) if user else None

def get_user_by_email(email: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, full_name, branch, role
            FROM users
            WHERE email = %s
        """, (email,))
        
        user = cursor.fetchone()
        return dict(user) if user else None

def generate_reset_token(email: str):
    token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(hours=1)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET reset_token = %s, reset_token_expiry = %s
            WHERE email = %s
            RETURNING id
        """, (token, expiry, email))
        
        result = cursor.fetchone()
        conn.commit()
        
        if result:
            return token
        return None

def reset_password_with_token(token: str, new_password: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, email FROM users
            WHERE reset_token = %s AND reset_token_expiry > %s
        """, (token, datetime.now()))
        
        user = cursor.fetchone()
        
        if not user:
            return False, "Invalid or expired reset token"
        
        new_hash = hash_password(new_password)
        cursor.execute("""
            UPDATE users
            SET password_hash = %s, reset_token = NULL, reset_token_expiry = NULL
            WHERE id = %s
        """, (new_hash, user['id']))
        
        conn.commit()
        return True, "Password reset successfully"

def update_user_role(user_id: int, new_role: str, admin_id: int):
    admin = get_user_by_id(admin_id)
    if not admin or admin['role'] != 'admin':
        return False, "Unauthorized"
    
    if new_role not in ROLES:
        return False, "Invalid role"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET role = %s WHERE id = %s
        """, (new_role, user_id))
        conn.commit()
        return True, "Role updated"
