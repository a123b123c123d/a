from eduassist.data.database import get_db
from eduassist.services.auth_service import get_user_by_id

CATEGORIES = [
    "General Discussion",
    "Academic Help",
    "Exam Preparation",
    "Placements & Career",
    "Projects",
    "Campus Life",
    "Announcements"
]

def create_post(user_id: int, title: str, content: str, category: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO forum_posts (user_id, title, content, category)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, content, category, created_at
        """, (user_id, title, content, category))
        
        post = cursor.fetchone()
        conn.commit()
        return dict(post)

def get_posts(page: int = 1, per_page: int = 10, category: str = None):
    offset = (page - 1) * per_page
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if category and category != "All":
            cursor.execute("""
                SELECT p.id, p.user_id, p.title, p.content, p.category, p.created_at, p.updated_at,
                       u.username, u.full_name, u.branch, u.role as user_role,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes,
                       (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = FALSE) as comment_count
                FROM forum_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.is_deleted = FALSE AND p.category = %s
                ORDER BY p.created_at DESC
                LIMIT %s OFFSET %s
            """, (category, per_page, offset))
        else:
            cursor.execute("""
                SELECT p.id, p.user_id, p.title, p.content, p.category, p.created_at, p.updated_at,
                       u.username, u.full_name, u.branch, u.role as user_role,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes,
                       (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = FALSE) as comment_count
                FROM forum_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.is_deleted = FALSE
                ORDER BY p.created_at DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
        
        posts = cursor.fetchall()
        return [dict(p) for p in posts]

def get_post_by_id(post_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.title, p.content, p.category, p.created_at, p.updated_at, p.user_id,
                   u.username, u.full_name, u.branch, u.role as user_role,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes
            FROM forum_posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = %s AND p.is_deleted = FALSE
        """, (post_id,))
        
        post = cursor.fetchone()
        return dict(post) if post else None

def toggle_reaction(post_id: int, user_id: int, reaction_type: str):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, reaction_type FROM post_reactions
            WHERE post_id = %s AND user_id = %s
        """, (post_id, user_id))
        
        existing = cursor.fetchone()
        
        if existing:
            if existing['reaction_type'] == reaction_type:
                cursor.execute("""
                    DELETE FROM post_reactions WHERE id = %s
                """, (existing['id'],))
            else:
                cursor.execute("""
                    UPDATE post_reactions SET reaction_type = %s WHERE id = %s
                """, (reaction_type, existing['id']))
        else:
            cursor.execute("""
                INSERT INTO post_reactions (post_id, user_id, reaction_type)
                VALUES (%s, %s, %s)
            """, (post_id, user_id, reaction_type))
        
        conn.commit()
        return True

def get_user_reaction(post_id: int, user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT reaction_type FROM post_reactions
            WHERE post_id = %s AND user_id = %s
        """, (post_id, user_id))
        
        result = cursor.fetchone()
        return result['reaction_type'] if result else None

def add_comment(post_id: int, user_id: int, content: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO post_comments (post_id, user_id, content)
            VALUES (%s, %s, %s)
            RETURNING id, content, created_at
        """, (post_id, user_id, content))
        
        comment = cursor.fetchone()
        conn.commit()
        return dict(comment)

def get_comments(post_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.content, c.created_at,
                   u.username, u.full_name, u.role as user_role
            FROM post_comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = %s AND c.is_deleted = FALSE
            ORDER BY c.created_at ASC
        """, (post_id,))
        
        comments = cursor.fetchall()
        return [dict(c) for c in comments]

def delete_post(post_id: int, user_id: int):
    user = get_user_by_id(user_id)
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM forum_posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            return False, "Post not found"
        
        if user['role'] != 'admin' and post['user_id'] != user_id:
            return False, "Unauthorized"
        
        cursor.execute("""
            UPDATE forum_posts SET is_deleted = TRUE WHERE id = %s
        """, (post_id,))
        
        conn.commit()
        return True, "Post deleted"

def delete_comment(comment_id: int, user_id: int):
    user = get_user_by_id(user_id)
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM post_comments WHERE id = %s", (comment_id,))
        comment = cursor.fetchone()
        
        if not comment:
            return False, "Comment not found"
        
        if user['role'] != 'admin' and comment['user_id'] != user_id:
            return False, "Unauthorized"
        
        cursor.execute("""
            UPDATE post_comments SET is_deleted = TRUE WHERE id = %s
        """, (comment_id,))
        
        conn.commit()
        return True, "Comment deleted"

def get_total_posts(category: str = None):
    with get_db() as conn:
        cursor = conn.cursor()
        if category and category != "All":
            cursor.execute("""
                SELECT COUNT(*) as count FROM forum_posts WHERE is_deleted = FALSE AND category = %s
            """, (category,))
        else:
            cursor.execute("""
                SELECT COUNT(*) as count FROM forum_posts WHERE is_deleted = FALSE
            """)
        result = cursor.fetchone()
        return result['count']
