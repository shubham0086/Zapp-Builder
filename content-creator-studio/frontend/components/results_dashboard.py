import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any

class ResultsDashboard:
    def __init__(self):
        pass
    
    def render(self, results: Dict[str, Any]):
        """Render results dashboard with tabs"""
        if not results:
            st.info("🤖 Results will appear here after generation")
            return
        
        # Results header
        success_indicator = "✅" if results.get('success') else "⚠️"
        status_color = "#28a745" if results.get('success') else "#ffc107"
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {status_color} 0%, #20c997 100%); 
                    padding: 1rem; border-radius: 8px; color: white; margin-bottom: 1rem;">
            <h3>{success_indicator} Content Generation Complete!</h3>
            <p><strong>Request ID:</strong> {results.get('request_id', 'N/A')} | 
               <strong>Status:</strong> {results.get('status', 'Unknown').title()} |
               <strong>Duration:</strong> {results.get('total_duration', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Workflow steps indicator
        if 'workflow_steps' in results:
            st.markdown("**Workflow Steps Completed:**")
            steps_text = " → ".join([
                f"🔍 Research" if step == "research" else
                f"🎯 Lead Generation" if step == "lead_generation" else  
                f"📝 Content Creation" if step == "content_creation" else
                f"📧 Outreach" if step == "outreach" else step.title()
                for step in results['workflow_steps']
            ])
            st.markdown(f"*{steps_text}*")
            st.markdown("---")
        
        # Create tabs based on available results
        tab_names = []
        if results.get('research_brief'):
            tab_names.append("📋 Research")
        if results.get('leads'):
            tab_names.append("🎯 Leads")
        if results.get('content'):
            tab_names.append("📝 Content")
        if results.get('outreach_messages'):
            tab_names.append("📧 Outreach")
        if results.get('sources'):
            tab_names.append("🔗 Sources")
        tab_names.append("📤 Export")
        
        if not tab_names:
            st.warning("No results to display")
            return
        
        tabs = st.tabs(tab_names)
        tab_index = 0
        
        # Research Brief Tab
        if results.get('research_brief'):
            with tabs[tab_index]:
                st.markdown("### 📚 AI Research Brief")
                st.markdown(results['research_brief'])
                
                # Research metrics
                if 'sources' in results:
                    st.markdown(f"**Sources Found:** {len(results['sources'])} references")
            tab_index += 1
        
        # Leads Tab
        if results.get('leads'):
            with tabs[tab_index]:
                st.markdown("### 🎯 Generated Leads")
                self.render_leads(results['leads'])
            tab_index += 1
        
        # Content Tab
        if results.get('content'):
            with tabs[tab_index]:
                st.markdown("### 📝 Generated Content")
                self.render_content(results['content'])
            tab_index += 1
        
        # Outreach Tab
        if results.get('outreach_messages'):
            with tabs[tab_index]:
                st.markdown("### 📧 Outreach Messages")
                self.render_outreach(results['outreach_messages'])
            tab_index += 1
        
        # Sources Tab
        if results.get('sources'):
            with tabs[tab_index]:
                st.markdown("### 🔗 Research Sources")
                self.render_sources(results['sources'])
            tab_index += 1
        
        # Export Tab
        with tabs[tab_index]:
            st.markdown("### 📤 Export Options")
            self.render_export_options(results)
    
    def render_leads(self, leads):
        """Render leads data"""
        if not leads:
            st.info("No leads generated")
            return
        
        st.markdown(f"**Found {len(leads)} high-quality leads:**")
        
        for i, lead in enumerate(leads):
            with st.container():
                # Lead header
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"**{lead.get('name', 'Unknown')}**")
                    if lead.get('bio'):
                        st.caption(lead['bio'])
                    if lead.get('profile_url'):
                        st.markdown(f"[View Profile]({lead['profile_url']})")
                
                with col2:
                    st.markdown(f"📱 **{lead.get('platform', 'Unknown')}**")
                    if lead.get('tags'):
                        tags = " • ".join(lead['tags'][:3])
                        st.caption(f"Tags: {tags}")
                
                with col3:
                    score = lead.get('relevance_score', 0)
                    score_color = "#28a745" if score > 0.8 else "#ffc107" if score > 0.6 else "#dc3545"
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="color: {score_color}; font-size: 1.5rem; font-weight: bold;">
                            {score:.2f}
                        </div>
                        <div style="font-size: 0.8rem; color: #666;">
                            Relevance Score
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Lead metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    followers = lead.get('follower_count', 0)
                    if followers >= 1000:
                        st.metric("Followers", f"{followers/1000:.1f}K")
                    else:
                        st.metric("Followers", followers)
                
                with col2:
                    engagement = lead.get('engagement_rate', 0)
                    st.metric("Engagement", f"{engagement:.1%}")
                
                with col3:
                    priority = lead.get('outreach_priority', 'Medium')
                    priority_color = "#28a745" if priority == "High" else "#ffc107"
                    st.markdown(f"""
                    <div style="color: {priority_color}; font-weight: bold;">
                        {priority} Priority
                    </div>
                    """, unsafe_allow_html=True)
                
                if i < len(leads) - 1:
                    st.divider()
    
    def render_content(self, content_dict):
        """Render generated content for each platform"""
        if not content_dict:
            st.info("No content generated")
            return
        
        for platform, content in content_dict.items():
            st.markdown(f"#### 📱 {platform}")
            
            # Content preview
            with st.expander(f"Preview {platform} Content", expanded=True):
                st.text_area(
                    f"{platform} Content",
                    value=content,
                    height=200,
                    key=f"content_{platform}",
                    help="Generated content for this platform"
                )
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(f"📋 Copy", key=f"copy_{platform}"):
                    # In a real app, this would copy to clipboard
                    st.success(f"Content copied!")
            
            with col2:
                if st.button(f"✏️ Edit", key=f"edit_{platform}"):
                    st.info("Edit mode coming soon!")
            
            with col3:
                if st.button(f"📤 Share", key=f"share_{platform}"):
                    st.info("Direct sharing coming soon!")
            
            with col4:
                # Download individual content
                st.download_button(
                    label="💾 Save",
                    data=content,
                    file_name=f"{platform.lower().replace(' ', '_')}_content.txt",
                    mime="text/plain",
                    key=f"download_{platform}"
                )
            
            st.divider()
    
    def render_outreach(self, outreach_messages):
        """Render outreach messages"""
        if not outreach_messages:
            st.info("No outreach messages generated")
            return
        
        st.markdown(f"**Generated {len(outreach_messages)} personalized outreach messages:**")
        
        for i, message in enumerate(outreach_messages):
            with st.expander(f"📧 Message for {message.get('recipient_name', 'Unknown')} ({message.get('platform', 'Unknown')})", expanded=False):
                
                # Message details
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Subject:** {message.get('subject_line', 'No subject')}")
                    st.markdown(f"**Platform:** {message.get('platform', 'Unknown')}")
                
                with col2:
                    response_rate = message.get('estimated_response_rate', 0)
                    st.metric("Est. Response Rate", f"{response_rate:.1%}")
                    
                    best_time = message.get('best_send_time', 'Anytime')
                    st.markdown(f"**Best Send Time:** {best_time}")
                
                # Message body
                st.markdown("**Message:**")
                st.text_area(
                    "Outreach Message",
                    value=message.get('message_body', ''),
                    height=200,
                    key=f"outreach_{i}",
                    label_visibility="collapsed"
                )
                
                # Platform notes
                if message.get('platform_specific_notes'):
                    st.info(f"💡 **Platform Tips:** {message['platform_specific_notes']}")
                
                # Actions
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📋 Copy Message", key=f"copy_outreach_{i}"):
                        st.success("Message copied!")
                
                with col2:
                    if st.button(f"📧 Open Email Client", key=f"email_{i}"):
                        st.info("Email client integration coming soon!")
    
    def render_sources(self, sources):
        """Render research sources"""
        if not sources:
            st.info("No sources available")
            return
        
        st.markdown("**Research sources used by AI agents:**")
        
        for i, source in enumerate(sources, 1):
            if source.startswith('http'):
                st.markdown(f"{i}. [{source}]({source})")
            else:
                st.markdown(f"{i}. {source}")
        
        # Source quality indicator
        st.markdown(f"**Source Quality:** {len(sources)} references found")
        if len(sources) >= 5:
            st.success("✅ Comprehensive research with multiple sources")
        elif len(sources) >= 3:
            st.info("ℹ️ Good research coverage")
        else:
            st.warning("⚠️ Limited source coverage")
    
    def render_export_options(self, results):
        """Render export options"""
        st.markdown("Choose your export format:")
        
        col1, col2, col3 = st.columns(3)
        
        # JSON Export
        with col1:
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=json_str,
                file_name=f"content_studio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Text Export
        with col2:
            text_content = self._create_text_export(results)
            st.download_button(
                label="📝 Download Text",
                data=text_content,
                file_name=f"content_studio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # CSV Export (for leads)
        with col3:
            if results.get('leads'):
                csv_content = self._create_csv_export(results['leads'])
                st.download_button(
                    label="📊 Download CSV",
                    data=csv_content,
                    file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("📊 CSV (No Data)", disabled=True, use_container_width=True)
        
        st.divider()
        
        # Quick share options
        st.markdown("### 🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📧 Email Results", use_container_width=True):
                st.info("Email sharing coming soon!")
        
        with col2:
            if st.button("💾 Save to Dashboard", use_container_width=True):
                st.success("Results saved to your dashboard!")
        
        with col3:
            if st.button("🔄 Generate Again", use_container_width=True):
                # Clear results to start over
                if 'results' in st.session_state:
                    del st.session_state.results
                st.rerun()
    
    def _create_text_export(self, results: Dict) -> str:
        """Create text export of results"""
        text_parts = []
        
        text_parts.append(f"Content Creator Studio Export")
        text_parts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        text_parts.append(f"Request ID: {results.get('request_id', 'N/A')}")
        text_parts.append(f"Topic: {results.get('topic', 'N/A')}")
        text_parts.append("=" * 50)
        
        if results.get('research_brief'):
            text_parts.append("\nRESEARCH BRIEF:")
            text_parts.append("-" * 20)
            text_parts.append(results['research_brief'])
        
        if results.get('content'):
            text_parts.append("\nGENERATED CONTENT:")
            text_parts.append("-" * 20)
            for platform, content in results['content'].items():
                text_parts.append(f"\n{platform}:")
                text_parts.append(content)
                text_parts.append("")
        
        if results.get('leads'):
            text_parts.append("\nLEADS:")
            text_parts.append("-" * 20)
            for lead in results['leads']:
                text_parts.append(f"Name: {lead.get('name', 'N/A')}")
                text_parts.append(f"Platform: {lead.get('platform', 'N/A')}")
                text_parts.append(f"Score: {lead.get('relevance_score', 0):.2f}")
                text_parts.append("")
        
        return "\n".join(text_parts)
    
    def _create_csv_export(self, leads: List[Dict]) -> str:
        """Create CSV export of leads"""
        if not leads:
            return ""
        
        # CSV header
        csv_lines = ["Name,Platform,Followers,Engagement Rate,Relevance Score,Profile URL,Bio"]
        
        # CSV data
        for lead in leads:
            name = lead.get('name', '').replace(',', ';')
            platform = lead.get('platform', '')
            followers = lead.get('follower_count', 0)
            engagement = lead.get('engagement_rate', 0)
            score = lead.get('relevance_score', 0)
            url = lead.get('profile_url', '')
            bio = lead.get('bio', '').replace(',', ';')[:100]  # Truncate bio
            
            csv_lines.append(f"{name},{platform},{followers},{engagement},{score},{url},{bio}")
        
        return "\n".join(csv_lines)