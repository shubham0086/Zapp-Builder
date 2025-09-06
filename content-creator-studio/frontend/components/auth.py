import streamlit as st
from typing import Optional

class AuthManager:
    def __init__(self):
        self.authenticated_key = 'authenticated'
        self.user_email_key = 'user_email'
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get(self.authenticated_key, False)
    
    def get_current_user(self) -> Optional[str]:
        """Get current user email"""
        if self.is_authenticated():
            return st.session_state.get(self.user_email_key)
        return None
    
    def render_login(self):
        """Render login form"""
        st.markdown("""
        <div style="max-width: 400px; margin: 0 auto; padding: 2rem;">
        """, unsafe_allow_html=True)
        
        st.title("🔐 Welcome to Content Creator Studio")
        st.markdown("*AI-powered content creation with CrewAI agents*")
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### Sign In")
            
            email = st.text_input(
                "Email",
                value="demo@example.com",
                placeholder="Enter your email"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                value="demo123",
                placeholder="Enter your password"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                login_btn = st.form_submit_button(
                    "🚀 Login",
                    type="primary",
                    use_container_width=True
                )
            
            with col2:
                demo_btn = st.form_submit_button(
                    "🎭 Demo Mode",
                    use_container_width=True
                )
            
            if login_btn or demo_btn:
                if self._validate_credentials(email, password) or demo_btn:
                    self._login_user(email)
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        # Additional options
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Sign Up", use_container_width=True):
                st.info("Sign up feature coming soon!")
        
        with col2:
            if st.button("🔑 Forgot Password?", use_container_width=True):
                st.info("Password reset coming soon!")
        
        # Demo credentials info
        with st.expander("🎭 Demo Credentials"):
            st.markdown("""
            **Demo Account:**
            - Email: `demo@example.com`
            - Password: `demo123`
            
            Or click "Demo Mode" to skip authentication.
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def _validate_credentials(self, email: str, password: str) -> bool:
        """Validate user credentials (simplified for demo)"""
        # In production, this would validate against a database
        demo_users = {
            "demo@example.com": "demo123",
            "admin@example.com": "admin123",
            "user@example.com": "user123"
        }
        
        return demo_users.get(email) == password
    
    def _login_user(self, email: str):
        """Log in user and set session state"""
        st.session_state[self.authenticated_key] = True
        st.session_state[self.user_email_key] = email
    
    def logout(self):
        """Log out user and clear session"""
        if self.authenticated_key in st.session_state:
            del st.session_state[self.authenticated_key]
        if self.user_email_key in st.session_state:
            del st.session_state[self.user_email_key]
    
    def render_user_info(self):
        """Render current user information"""
        if self.is_authenticated():
            user_email = self.get_current_user()
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"👤 **Logged in as:** {user_email}")
                
                with col2:
                    if st.button("🚪 Logout", use_container_width=True):
                        self.logout()
                        st.rerun()
        
        return self.is_authenticated()