# research_tools_integration.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import time

# Import the individual research tool modules
from citation_management import display_citation_management
from literature_review_assistance import display_literature_review_assistant
from research_methodology_guidance import display_methodology_guidance
from data_analysis_tools import display_data_analysis_tools
from academic_integrity_checking import display_academic_integrity_tools

def display_research_tools():
    """Main function to display the research tools dashboard"""
    st.title("🔬 Research Tools Integration")
    
    # Create tabs for different research tools
    research_tabs = st.tabs([
        "Citation Management",
        "Literature Review Assistant",
        "Research Methodology",
        "Data Analysis",
        "Academic Integrity"
    ])
    
    # Tab 1: Citation Management
    with research_tabs[0]:
        display_citation_management()
    
    # Tab 2: Literature Review Assistant
    with research_tabs[1]:
        display_literature_review_assistant()
    
    # Tab 3: Research Methodology Guidance
    with research_tabs[2]:
        display_methodology_guidance()
    
    # Tab 4: Data Analysis Tools
    with research_tabs[3]:
        display_data_analysis_tools()
    
    # Tab 5: Academic Integrity Tools
    with research_tabs[4]:
        display_academic_integrity_tools()

def integrate_cms_with_app():
    """Function to integrate the research tools with the main app"""
    display_research_tools()

# For testing this module independently
if __name__ == "__main__":
    st.set_page_config(page_title="Research Tools", layout="wide")
    display_research_tools()
