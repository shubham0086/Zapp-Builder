import streamlit as st
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        self.user_info_key = 'user_info'
        self.recent_projects_key = 'recent_projects'
        self.settings_key = 'user_settings'
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information"""
        default_info = {
            'email': st.session_state.get('user_email', 'demo@example.com'),
            'plan': 'Free',
            'credits': 100,
            'projects_created': 5,
            'last_login': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'member_since': '2024-01-01'
        }
        
        return st.session_state.get(self.user_info_key, default_info)
    
    def update_user_info(self, info: Dict[str, Any]):
        """Update user information"""
        current_info = self.get_user_info()
        current_info.update(info)
        st.session_state[self.user_info_key] = current_info
    
    def get_recent_projects(self) -> List[Dict[str, Any]]:
        """Get recent projects for the user"""
        default_projects = [
            {
                'id': 'proj_001',
                'topic': 'AI in Healthcare Innovation',
                'platforms': ['LinkedIn', 'Newsletter'],
                'created_at': '2024-01-15',
                'status': 'completed'
            },
            {
                'id': 'proj_002', 
                'topic': 'Remote Work Productivity Tips',
                'platforms': ['X (Twitter)', 'Instagram'],
                'created_at': '2024-01-14',
                'status': 'completed'
            },
            {
                'id': 'proj_003',
                'topic': 'Sustainable Technology Trends',
                'platforms': ['YouTube', 'Blog'],
                'created_at': '2024-01-13',
                'status': 'completed'
            },
            {
                'id': 'proj_004',
                'topic': 'Personal Branding for Entrepreneurs',
                'platforms': ['LinkedIn', 'Instagram'],
                'created_at': '2024-01-12',
                'status': 'completed'
            },
            {
                'id': 'proj_005',
                'topic': 'Digital Marketing Automation',
                'platforms': ['Newsletter', 'Blog'],
                'created_at': '2024-01-11',
                'status': 'completed'
            }
        ]
        
        return st.session_state.get(self.recent_projects_key, default_projects)
    
    def add_project(self, project: Dict[str, Any]):
        """Add a new project to recent projects"""
        projects = self.get_recent_projects()
        
        # Add new project at the beginning
        projects.insert(0, project)
        
        # Keep only the 10 most recent projects
        projects = projects[:10]
        
        st.session_state[self.recent_projects_key] = projects
    
    def get_user_settings(self) -> Dict[str, Any]:
        """Get user settings and preferences"""
        default_settings = {
            'default_tone': 'Professional',
            'preferred_platforms': ['LinkedIn', 'X (Twitter)'],
            'max_results': 20,
            'include_hashtags': True,
            'include_cta': True,
            'auto_research': True,
            'notification_email': True,
            'theme': 'light'
        }
        
        return st.session_state.get(self.settings_key, default_settings)
    
    def update_settings(self, settings: Dict[str, Any]):
        """Update user settings"""
        current_settings = self.get_user_settings()
        current_settings.update(settings)
        st.session_state[self.settings_key] = current_settings
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get user usage statistics"""
        return {
            'total_projects': len(self.get_recent_projects()),
            'total_content_pieces': 25,
            'total_leads_generated': 150,
            'avg_engagement_lift': 0.35,
            'most_used_platform': 'LinkedIn',
            'credits_used_this_month': 45,
            'credits_remaining': 55
        }
    
    def save_generation_result(self, result: Dict[str, Any]):
        """Save a content generation result"""
        # Create project entry
        project = {
            'id': result.get('request_id', f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            'topic': result.get('topic', 'Unknown Topic'),
            'platforms': result.get('platforms', []),
            'created_at': datetime.now().strftime('%Y-%m-%d'),
            'status': 'completed' if result.get('success') else 'failed',
            'workflow_steps': result.get('workflow_steps', []),
            'content_count': len(result.get('content', {})),
            'leads_count': len(result.get('leads', [])) if result.get('leads') else 0
        }
        
        self.add_project(project)
        
        # Update user stats
        user_info = self.get_user_info()
        user_info['projects_created'] = user_info.get('projects_created', 0) + 1
        user_info['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.update_user_info(user_info)
    
    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific project by ID"""
        projects = self.get_recent_projects()
        for project in projects:
            if project['id'] == project_id:
                return project
        return None
    
    def clear_session_data(self):
        """Clear all session data except authentication"""
        keys_to_keep = ['authenticated', 'user_email']
        keys_to_remove = []
        
        for key in st.session_state.keys():
            if key not in keys_to_keep:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    def export_user_data(self) -> Dict[str, Any]:
        """Export all user data for backup/download"""
        return {
            'user_info': self.get_user_info(),
            'recent_projects': self.get_recent_projects(),
            'settings': self.get_user_settings(),
            'usage_stats': self.get_usage_stats(),
            'exported_at': datetime.now().isoformat()
        }