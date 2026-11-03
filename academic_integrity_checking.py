from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import pandas as pd
import openai
import re
import time
import json
from io import BytesIO, StringIO
import docx
import fitz  # PyMuPDF for PDF handling
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import base64

def initialize_integrity_state():
    """Initialize session state variables for academic integrity checking"""
    if "active_integrity_tab" not in st.session_state:
        st.session_state.active_integrity_tab = "Plagiarism Check"
        
    if "integrity_history" not in st.session_state:
        st.session_state.integrity_history = []
        
    if "plagiarism_results" not in st.session_state:
        st.session_state.plagiarism_results = None
        
    if "grammar_results" not in st.session_state:
        st.session_state.grammar_results = None
        
    if "citation_results" not in st.session_state:
        st.session_state.citation_results = None

def extract_text_from_docx(uploaded_file):
    """Extract text from a .docx file"""
    try:
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {str(e)}")
        return None

def extract_text_from_pdf(uploaded_file):
    """Extract text from a .pdf file"""
    try:
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def check_plagiarism(text, api_key):
    """Check text for potential plagiarism using AI"""
    
    prompt = f"""
    Analyze the following text for potential plagiarism. 
    
    Text to analyze:
    ```
    {text[:4000]}  # Limit to first 4000 chars for API limits
    ```
    
    Please provide:
    1. A plagiarism risk score (0-100%)
    2. Highlighted sections that may be plagiarized 
    3. Explanation of why these sections seem suspicious
    4. Recommendations for addressing potential plagiarism issues
    
    Format your response as JSON with these exact keys:
    - "plagiarism_score": float (0-100)
    - "suspicious_sections": list of objects with "text" and "reason" keys
    - "explanation": string
    - "recommendations": list of strings
    
    Only return valid JSON. If the text is too short or unclear, return a default low score with appropriate explanation.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an academic integrity analysis tool that evaluates text for potential plagiarism."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON if it's wrapped in code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        result = json.loads(response_text)
        return result
    
    except Exception as e:
        st.error(f"Error checking plagiarism: {str(e)}")
        # Return a default response
        return {
            "plagiarism_score": 0,
            "suspicious_sections": [],
            "explanation": "Error processing plagiarism check. Please try again or review manually.",
            "recommendations": ["Manual review recommended due to processing error."]
        }

def check_grammar_style(text, api_key):
    """Check text for grammar and academic style issues using AI"""
    
    prompt = f"""
    Analyze the following academic text for grammar, clarity, and style issues.
    
    Text to analyze:
    ```
    {text[:4000]}  # Limit to first 4000 chars for API limits
    ```
    
    Please provide:
    1. Overall writing quality score (0-100%)
    2. Specific grammar issues found
    3. Style and clarity issues
    4. Recommendations for improvement
    
    Format your response as JSON with these exact keys:
    - "writing_score": float (0-100)
    - "grammar_issues": list of objects with "text" and "suggestion" keys
    - "style_issues": list of objects with "text" and "suggestion" keys
    - "recommendations": list of strings
    
    Only return valid JSON. If the text is too short or unclear, return a default response with appropriate explanation.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an academic writing analysis tool that evaluates text for grammar, clarity, and style."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON if it's wrapped in code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        result = json.loads(response_text)
        return result
    
    except Exception as e:
        st.error(f"Error checking grammar and style: {str(e)}")
        # Return a default response
        return {
            "writing_score": 0,
            "grammar_issues": [],
            "style_issues": [],
            "recommendations": ["Manual review recommended due to processing error."]
        }

def analyze_citations(text, api_key):
    """Analyze citations in academic text using AI"""
    
    prompt = f"""
    Analyze the following academic text for citation patterns and issues.
    
    Text to analyze:
    ```
    {text[:4000]}  # Limit to first 4000 chars for API limits
    ```
    
    Please provide:
    1. Citation quality score (0-100%)
    2. Citations found (in any format like APA, MLA, Chicago, etc.)
    3. Citation issues or inconsistencies
    4. Areas that may need additional citation
    5. Recommendations for improving citations
    
    Format your response as JSON with these exact keys:
    - "citation_score": float (0-100)
    - "citations_found": list of strings
    - "citation_issues": list of strings
    - "areas_needing_citation": list of strings
    - "recommendations": list of strings
    
    Only return valid JSON. If the text is too short or unclear, return a default response with appropriate explanation.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an academic citation analysis tool that evaluates text for proper citation usage."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON if it's wrapped in code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        result = json.loads(response_text)
        return result
    
    except Exception as e:
        st.error(f"Error analyzing citations: {str(e)}")
        # Return a default response
        return {
            "citation_score": 0,
            "citations_found": [],
            "citation_issues": ["Error processing citation analysis."],
            "areas_needing_citation": [],
            "recommendations": ["Manual review recommended due to processing error."]
        }

def generate_integrity_report(plagiarism_results, grammar_results, citation_results):
    """Generate a comprehensive academic integrity report"""
    
    prompt = f"""
    Create a comprehensive academic integrity report based on these analysis results:
    
    Plagiarism Analysis:
    {json.dumps(plagiarism_results, indent=2)}
    
    Grammar & Style Analysis:
    {json.dumps(grammar_results, indent=2)}
    
    Citation Analysis:
    {json.dumps(citation_results, indent=2)}
    
    The report should include:
    1. An executive summary
    2. Detailed findings in each category
    3. Overall academic integrity assessment
    4. Specific recommendations for improvement
    5. Next steps
    
    Format the report in markdown with clear sections and bullet points where appropriate.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an academic integrity reporting tool that creates comprehensive reports based on analysis results."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        report_text = response.choices[0].message.content.strip()
        return report_text
    
    except Exception as e:
        st.error(f"Error generating integrity report: {str(e)}")
        # Return a default response
        return """
        # Academic Integrity Report
        
        ## Executive Summary
        Unable to generate a complete report due to processing error. Please review the individual analysis results.
        
        ## Recommendations
        Manual review of the document is recommended.
        """

def display_academic_integrity_tools():
    """Main function to display academic integrity tools interface"""
    
    # Initialize session state
    initialize_integrity_state()
    
    st.title("🔍 Academic Integrity Checking Tools")
    
    # Navigation tabs
    integrity_tabs = [
        "Plagiarism Check",
        "Grammar & Style Check",
        "Citation Analyzer",
        "Comprehensive Report",
        "Originality Database"
    ]
    
    selected_tab = st.radio("Academic Integrity Tools", integrity_tabs, horizontal=True)
    st.session_state.active_integrity_tab = selected_tab
    
    st.markdown("---")
    
    # File uploader for all tabs
    uploaded_file = st.file_uploader("Upload document for analysis", type=["txt", "pdf", "docx"])
    
    # Text input as an alternative
    text_input = st.text_area("Or paste text for analysis:", height=200)
    
    # Get the text to analyze
    analysis_text = ""
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        
        if file_type == "txt":
            analysis_text = uploaded_file.getvalue().decode("utf-8")
        elif file_type == "docx":
            analysis_text = extract_text_from_docx(uploaded_file)
        elif file_type == "pdf":
            analysis_text = extract_text_from_pdf(uploaded_file)
            
        if analysis_text:
            st.success(f"✅ Successfully extracted text from {uploaded_file.name}")
            # Show a preview
            with st.expander("Preview extracted text"):
                st.text(analysis_text[:1000] + ("..." if len(analysis_text) > 1000 else ""))
    elif text_input:
        analysis_text = text_input
    
    # Get API key
    api_key = st.text_input("Enter OpenAI API Key (required for analysis)", type="password")
    if api_key:
        openai.api_key = api_key  # Set the API key
    
    # Each tab's content
    if analysis_text:
        # Tab 1: Plagiarism Check
        if st.session_state.active_integrity_tab == "Plagiarism Check":
            st.header("Plagiarism Check")
            
            st.write("""
            This tool analyzes academic texts for potential plagiarism using AI. It identifies suspicious 
            passages and provides recommendations for maintaining academic integrity.
            """)
            
            if st.button("Check for Plagiarism"):
                with st.spinner("Analyzing text for potential plagiarism..."):
                    try:
                        plagiarism_results = check_plagiarism(analysis_text, api_key)
                        st.session_state.plagiarism_results = plagiarism_results
                        
                        # Display the results
                        st.success("✅ Plagiarism analysis complete!")
                        
                        # Plagiarism score with gauge
                        score = plagiarism_results.get("plagiarism_score", 0)
                        st.subheader("Plagiarism Risk Score")
                        
                        # Create score meter
                        col1, col2, col3 = st.columns([1,2,1])
                        with col2:
                            if score < 15:
                                meter_color = "green"
                                risk_level = "Low Risk"
                            elif score < 30:
                                meter_color = "orange"
                                risk_level = "Moderate Risk"
                            else:
                                meter_color = "red"
                                risk_level = "High Risk"
                                
                            st.markdown(f"""
                            <div style="text-align: center;">
                                <div style="margin: 0 auto; width: 150px; height: 150px; border-radius: 50%; background: conic-gradient({meter_color} {score}%, #f0f0f0 0deg); position: relative;">
                                    <div style="position: absolute; top: 25px; left: 25px; width: 100px; height: 100px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">
                                        {score}%
                                    </div>
                                </div>
                                <p style="margin-top: 10px; font-size: 18px; font-weight: bold;">{risk_level}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Suspicious sections
                        st.subheader("Potentially Problematic Sections")
                        
                        suspicious_sections = plagiarism_results.get("suspicious_sections", [])
                        if suspicious_sections:
                            for i, section in enumerate(suspicious_sections):
                                with st.expander(f"Suspicious Section {i+1}"):
                                    st.markdown(f"""
                                    **Text:** 
                                    ```
                                    {section.get('text', '')}
                                    ```
                                    
                                    **Reason:** {section.get('reason', 'No reason provided')}
                                    """)
                        else:
                            st.info("No suspicious sections were identified.")
                        
                        # Explanation and recommendations
                        st.subheader("Analysis Explanation")
                        st.write(plagiarism_results.get("explanation", "No explanation provided."))
                        
                        st.subheader("Recommendations")
                        recommendations = plagiarism_results.get("recommendations", [])
                        for rec in recommendations:
                            st.write(f"• {rec}")
                            
                        # Add to history
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        if "integrity_history" in st.session_state:
                            st.session_state.integrity_history.append({
                                "type": "Plagiarism Check",
                                "timestamp": timestamp,
                                "score": score,
                                "risk_level": risk_level,
                                "suspicious_count": len(suspicious_sections)
                            })
                            
                        # Download report option
                        report_text = f"""
                        # Plagiarism Check Report
                        
                        **Date:** {timestamp}
                        **Plagiarism Risk Score:** {score}% ({risk_level})
                        
                        ## Analysis Explanation
                        {plagiarism_results.get("explanation", "No explanation provided.")}
                        
                        ## Potentially Problematic Sections
                        
                        {("No suspicious sections were identified." if not suspicious_sections else "")}
                        """
                        
                        for i, section in enumerate(suspicious_sections):
                            report_text += f"""
                            ### Suspicious Section {i+1}
                            
                            **Text:** 
                            ```
                            {section.get('text', '')}
                            ```
                            
                            **Reason:** {section.get('reason', 'No reason provided')}
                            """
                            
                        report_text += """
                        ## Recommendations
                        
                        """
                        
                        for rec in recommendations:
                            report_text += f"* {rec}\n"
                            
                        st.download_button(
                            label="Download Plagiarism Report",
                            data=report_text,
                            file_name="plagiarism_check_report.md",
                            mime="text/markdown"
                        )
                            
                    except Exception as e:
                        st.error(f"Error running plagiarism check: {str(e)}")
                        st.info("Please make sure you've entered a valid OpenAI API key and have sufficient credits.")
        
        # Tab 2: Grammar & Style Check
        elif st.session_state.active_integrity_tab == "Grammar & Style Check":
            st.header("Grammar & Academic Style Check")
            
            st.write("""
            This tool analyzes academic writing for grammar, clarity, and style issues. It helps improve
            the overall quality and readability of academic documents.
            """)
            
            if st.button("Check Grammar & Style"):
                with st.spinner("Analyzing grammar and academic style..."):
                    try:
                        grammar_results = check_grammar_style(analysis_text, api_key)
                        st.session_state.grammar_results = grammar_results
                        
                        # Display the results
                        st.success("✅ Grammar and style analysis complete!")
                        
                        # Writing quality score with gauge
                        score = grammar_results.get("writing_score", 0)
                        st.subheader("Writing Quality Score")
                        
                        # Create score meter
                        col1, col2, col3 = st.columns([1,2,1])
                        with col2:
                            if score >= 80:
                                meter_color = "green"
                                quality_level = "Excellent"
                            elif score >= 60:
                                meter_color = "lightgreen"
                                quality_level = "Good"
                            elif score >= 40:
                                meter_color = "orange"
                                quality_level = "Adequate"
                            else:
                                meter_color = "red"
                                quality_level = "Needs Improvement"
                                
                            st.markdown(f"""
                            <div style="text-align: center;">
                                <div style="margin: 0 auto; width: 150px; height: 150px; border-radius: 50%; background: conic-gradient({meter_color} {score}%, #f0f0f0 0deg); position: relative;">
                                    <div style="position: absolute; top: 25px; left: 25px; width: 100px; height: 100px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">
                                        {score}%
                                    </div>
                                </div>
                                <p style="margin-top: 10px; font-size: 18px; font-weight: bold;">{quality_level}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Grammar issues
                        st.subheader("Grammar Issues")
                        
                        grammar_issues = grammar_results.get("grammar_issues", [])
                        if grammar_issues:
                            for i, issue in enumerate(grammar_issues):
                                with st.expander(f"Grammar Issue {i+1}"):
                                    st.markdown(f"""
                                    **Original Text:** 
                                    ```
                                    {issue.get('text', '')}
                                    ```
                                    
                                    **Suggestion:** {issue.get('suggestion', 'No suggestion provided')}
                                    """)
                        else:
                            st.info("No significant grammar issues were identified.")
                        
                        # Style issues
                        st.subheader("Style & Clarity Issues")
                        
                        style_issues = grammar_results.get("style_issues", [])
                        if style_issues:
                            for i, issue in enumerate(style_issues):
                                with st.expander(f"Style Issue {i+1}"):
                                    st.markdown(f"""
                                    **Original Text:** 
                                    ```
                                    {issue.get('text', '')}
                                    ```
                                    
                                    **Suggestion:** {issue.get('suggestion', 'No suggestion provided')}
                                    """)
                        else:
                            st.info("No significant style or clarity issues were identified.")
                        
                        # Recommendations
                        st.subheader("Recommendations for Improvement")
                        recommendations = grammar_results.get("recommendations", [])
                        for rec in recommendations:
                            st.write(f"• {rec}")
                            
                        # Add to history
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        if "integrity_history" in st.session_state:
                            st.session_state.integrity_history.append({
                                "type": "Grammar & Style Check",
                                "timestamp": timestamp,
                                "score": score,
                                "quality_level": quality_level,
                                "grammar_issues": len(grammar_issues),
                                "style_issues": len(style_issues)
                            })
                            
                        # Download report option
                        report_text = f"""
                        # Grammar & Style Check Report
                        
                        **Date:** {timestamp}
                        **Writing Quality Score:** {score}% ({quality_level})
                        
                        ## Grammar Issues
                        
                        {("No significant grammar issues were identified." if not grammar_issues else "")}
                        """
                        
                        for i, issue in enumerate(grammar_issues):
                            report_text += f"""
                            ### Grammar Issue {i+1}
                            
                            **Original Text:** 
                            ```
                            {issue.get('text', '')}
                            ```
                            
                            **Suggestion:** {issue.get('suggestion', 'No suggestion provided')}
                            """
                            
                        report_text += """
                        ## Style & Clarity Issues
                        
                        """
                        
                        if not style_issues:
                            report_text += "No significant style or clarity issues were identified.\n\n"
                            
                        for i, issue in enumerate(style_issues):
                            report_text += f"""
                            ### Style Issue {i+1}
                            
                            **Original Text:** 
                            ```
                            {issue.get('text', '')}
                            ```
                            
                            **Suggestion:** {issue.get('suggestion', 'No suggestion provided')}
                            """
                            
                        report_text += """
                        ## Recommendations for Improvement
                        
                        """
                        
                        for rec in recommendations:
                            report_text += f"* {rec}\n"
                            
                        st.download_button(
                            label="Download Grammar & Style Report",
                            data=report_text,
                            file_name="grammar_style_report.md",
                            mime="text/markdown"
                        )
                            
                    except Exception as e:
                        st.error(f"Error running grammar and style check: {str(e)}")
                        st.info("Please make sure you've entered a valid OpenAI API key and have sufficient credits.")
        
        # Tab 3: Citation Analyzer
        elif st.session_state.active_integrity_tab == "Citation Analyzer":
            st.header("Citation Analyzer")
            
            st.write("""
            This tool analyzes the citation patterns in academic texts. It identifies missing citations,
            checks for consistency, and provides recommendations for proper citation practices.
            """)
            
            if st.button("Analyze Citations"):
                with st.spinner("Analyzing citations..."):
                    try:
                        citation_results = analyze_citations(analysis_text, api_key)
                        st.session_state.citation_results = citation_results
                        
                        # Display the results
                        st.success("✅ Citation analysis complete!")
                        
                        # Citation quality score with gauge
                        score = citation_results.get("citation_score", 0)
                        st.subheader("Citation Quality Score")
                        
                        # Create score meter
                        col1, col2, col3 = st.columns([1,2,1])
                        with col2:
                            if score >= 80:
                                meter_color = "green"
                                quality_level = "Excellent"
                            elif score >= 60:
                                meter_color = "lightgreen"
                                quality_level = "Good"
                            elif score >= 40:
                                meter_color = "orange"
                                quality_level = "Adequate"
                            else:
                                meter_color = "red"
                                quality_level = "Needs Improvement"
                                
                            st.markdown(f"""
                            <div style="text-align: center;">
                                <div style="margin: 0 auto; width: 150px; height: 150px; border-radius: 50%; background: conic-gradient({meter_color} {score}%, #f0f0f0 0deg); position: relative;">
                                    <div style="position: absolute; top: 25px; left: 25px; width: 100px; height: 100px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">
                                        {score}%
                                    </div>
                                </div>
                                <p style="margin-top: 10px; font-size: 18px; font-weight: bold;">{quality_level}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Citations found
                        st.subheader("Citations Found")
                        
                        citations_found = citation_results.get("citations_found", [])
                        if citations_found:
                            with st.expander("View All Citations", expanded=True):
                                for citation in citations_found:
                                    st.markdown(f"• {citation}")
                        else:
                            st.warning("No citations were found in the document.")
                        
                        # Citation issues
                        st.subheader("Citation Issues")
                        
                        citation_issues = citation_results.get("citation_issues", [])
                        if citation_issues:
                            for i, issue in enumerate(citation_issues):
                                st.markdown(f"• {issue}")
                        else:
                            st.info("No citation issues were identified.")
                        
                        # Areas needing citation
                        st.subheader("Areas Needing Citation")
                        
                        areas_needing_citation = citation_results.get("areas_needing_citation", [])
                        if areas_needing_citation:
                            for i, area in enumerate(areas_needing_citation):
                                with st.expander(f"Area {i+1} Needing Citation"):
                                    st.markdown(f"{area}")
                        else:
                            st.info("No specific areas needing additional citation were identified.")
                        
                        # Recommendations
                        st.subheader("Recommendations for Citations")
                        recommendations = citation_results.get("recommendations", [])
                        for rec in recommendations:
                            st.write(f"• {rec}")
                            
                        # Add to history
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        if "integrity_history" in st.session_state:
                            st.session_state.integrity_history.append({
                                "type": "Citation Analysis",
                                "timestamp": timestamp,
                                "score": score,
                                "quality_level": quality_level,
                                "citations_found": len(citations_found),
                                "citation_issues": len(citation_issues)
                            })
                            
                        # Download report option
                        report_text = f"""
                        # Citation Analysis Report
                        
                        **Date:** {timestamp}
                        **Citation Quality Score:** {score}% ({quality_level})
                        
                        ## Citations Found ({len(citations_found)})
                        
                        {("No citations were found in the document." if not citations_found else "")}
                        """
                        
                        for citation in citations_found:
                            report_text += f"* {citation}\n"
                            
                        report_text += """
                        ## Citation Issues
                        
                        """
                        
                        if not citation_issues:
                            report_text += "No citation issues were identified.\n\n"
                            
                        for issue in citation_issues:
                            report_text += f"* {issue}\n"
                            
                        report_text += """
                        ## Areas Needing Citation
                        
                        """
                        
                        if not areas_needing_citation:
                            report_text += "No specific areas needing additional citation were identified.\n\n"
                            
                        for i, area in enumerate(areas_needing_citation):
                            report_text += f"### Area {i+1}\n{area}\n\n"
                            
                        report_text += """
                        ## Recommendations for Citations
                        
                        """
                        
                        for rec in recommendations:
                            report_text += f"* {rec}\n"
                            
                        st.download_button(
                            label="Download Citation Analysis Report",
                            data=report_text,
                            file_name="citation_analysis_report.md",
                            mime="text/markdown"
                        )
                            
                    except Exception as e:
                        st.error(f"Error analyzing citations: {str(e)}")
                        st.info("Please make sure you've entered a valid OpenAI API key and have sufficient credits.")
        
        # Tab 4: Comprehensive Report
        elif st.session_state.active_integrity_tab == "Comprehensive Report":
            st.header("Comprehensive Academic Integrity Report")
            
            st.write("""
            This tool generates a comprehensive academic integrity report combining plagiarism detection,
            grammar/style analysis, and citation checking.
            """)
            
            # Check if we have already run the individual analyses
            plagiarism_results = st.session_state.get("plagiarism_results")
            grammar_results = st.session_state.get("grammar_results")
            citation_results = st.session_state.get("citation_results")
            
            # Show status of each analysis
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if plagiarism_results:
                    st.success("✅ Plagiarism analysis complete")
                else:
                    st.warning("⚠️ Plagiarism analysis not run")
            
            with col2:
                if grammar_results:
                    st.success("✅ Grammar analysis complete")
                else:
                    st.warning("⚠️ Grammar analysis not run")
            
            with col3:
                if citation_results:
                    st.success("✅ Citation analysis complete")
                else:
                    st.warning("⚠️ Citation analysis not run")
            
            # Option to run all analyses first
            if not (plagiarism_results and grammar_results and citation_results):
                if st.button("Run All Analyses First"):
                    with st.spinner("Running all analyses... This may take a minute."):
                        try:
                            if not plagiarism_results:
                                plagiarism_results = check_plagiarism(analysis_text, api_key)
                                st.session_state.plagiarism_results = plagiarism_results
                                st.success("✅ Plagiarism analysis complete")
                            
                            if not grammar_results:
                                grammar_results = check_grammar_style(analysis_text, api_key)
                                st.session_state.grammar_results = grammar_results
                                st.success("✅ Grammar analysis complete")
                            
                            if not citation_results:
                                citation_results = analyze_citations(analysis_text, api_key)
                                st.session_state.citation_results = citation_results
                                st.success("✅ Citation analysis complete")
                                
                        except Exception as e:
                            st.error(f"Error running analyses: {str(e)}")
                            st.info("Please make sure you've entered a valid OpenAI API key and have sufficient credits.")
            
            # Generate comprehensive report
            if plagiarism_results and grammar_results and citation_results:
                if st.button("Generate Comprehensive Report"):
                    with st.spinner("Generating comprehensive academic integrity report..."):
                        try:
                            report = generate_integrity_report(
                                plagiarism_results,
                                grammar_results,
                                citation_results
                            )
                            
                            # Display the report
                            st.success("✅ Comprehensive report generated!")
                            st.markdown(report)
                            
                            # Add to history
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            if "integrity_history" in st.session_state:
                                st.session_state.integrity_history.append({
                                    "type": "Comprehensive Report",
                                    "timestamp": timestamp,
                                    "plagiarism_score": plagiarism_results.get("plagiarism_score", 0),
                                    "grammar_score": grammar_results.get("writing_score", 0),
                                    "citation_score": citation_results.get("citation_score", 0)
                                })
                            
                            # Visualization of scores
                            st.subheader("Overall Integrity Scores")
                            
                            # Create a radar chart of the three scores
                            categories = ['Plagiarism Integrity\n(higher is better)', 'Grammar & Style', 'Citation Quality']
                            
                            # Convert plagiarism score (where lower is better) to integrity score (where higher is better)
                            plagiarism_integrity = 100 - plagiarism_results.get("plagiarism_score", 0)
                            
                            values = [
                                plagiarism_integrity,
                                grammar_results.get("writing_score", 0),
                                citation_results.get("citation_score", 0)
                            ]
                            
                            # Create radar chart
                            fig = plt.figure(figsize=(10, 6))
                            ax = fig.add_subplot(111, polar=True)
                            
                            # Compute angle for each category
                            angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
                            
                            # Close the polygon
                            values = values + [values[0]]
                            angles = angles + [angles[0]]
                            
                            # Plot data
                            ax.plot(angles, values, linewidth=2, linestyle='solid')
                            
                            # Fill area
                            ax.fill(angles, values, alpha=0.25)
                            
                            # Set category labels
                            ax.set_xticks(angles[:-1])
                            ax.set_xticklabels(categories)
                            
                            # Set y-limits
                            ax.set_ylim(0, 100)
                            
                            # Add score values at each point
                            for i, value in enumerate(values[:-1]):  # Skip the duplicated first value
                                ax.text(angles[i], value + 5, f"{value:.0f}%", 
                                       ha='center', va='center', fontsize=10,
                                       bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
                            
                            plt.title("Academic Integrity Assessment")
                            
                            st.pyplot(fig)
                            
                            # Download report option
                            st.download_button(
                                label="Download Comprehensive Report",
                                data=report,
                                file_name="academic_integrity_comprehensive_report.md",
                                mime="text/markdown"
                            )
                            
                        except Exception as e:
                            st.error(f"Error generating comprehensive report: {str(e)}")
                            st.info("Please make sure you've entered a valid OpenAI API key and have sufficient credits.")
            
        # Tab 5: Originality Database
        elif st.session_state.active_integrity_tab == "Originality Database":
            st.header("Originality Database")
            
            st.write("""
            The Originality Database allows you to track submissions and maintain records of 
            analyzed documents for academic integrity.
            """)
            
            # Show history of analyses
            if "integrity_history" in st.session_state and st.session_state.integrity_history:
                st.subheader("Analysis History")
                
                # Create a dataframe from history
                history_data = []
                for item in st.session_state.integrity_history:
                    history_data.append({
                        "Type": item.get("type", "Unknown"),
                        "Timestamp": item.get("timestamp", "Unknown"),
                        "Score": item.get("score", item.get("plagiarism_score", 0)),
                        "Details": f"{item.get('risk_level', item.get('quality_level', 'N/A'))}"
                    })
                
                history_df = pd.DataFrame(history_data)
                st.dataframe(history_df)
                
                # Option to clear history
                if st.button("Clear History"):
                    st.session_state.integrity_history = []
                    st.rerun()
            else:
                st.info("No analysis history available. Run some analyses to build your database.")
            
            # Upload to database functionality (simulated)
            st.subheader("Add Document to Database")
            
            document_name = st.text_input("Document Name/Title")
            author_name = st.text_input("Author Name")
            course_info = st.text_input("Course/Class Information")
            
            if st.button("Add to Database") and document_name and analysis_text:
                # Simulate adding to a database
                with st.spinner("Adding document to originality database..."):
                    # Create a hash of the document content
                    import hashlib
                    document_hash = hashlib.md5(analysis_text.encode()).hexdigest()
                    
                    # In a real implementation, this would be stored in a database
                    # For this demo, we'll just display the hash and a success message
                    st.success("✅ Document added to database successfully!")
                    st.code(document_hash, language="text")
                    
                    # Show what would be stored
                    stored_data = {
                        "name": document_name,
                        "author": author_name,
                        "course": course_info,
                        "hash": document_hash,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "content_preview": analysis_text[:100] + "...",
                        "word_count": len(analysis_text.split())
                    }
                    
                    st.json(stored_data)
            
            # Database search and management (simulated)
            st.subheader("Search Database")
            
            search_query = st.text_input("Search for documents")
            
            if search_query:
                st.info("This is a simulated feature. In a real implementation, this would search a database of previously analyzed documents.")
                
                # Show a simulated search result
                st.markdown(f"""
                **Search results for: "{search_query}"**
                
                No exact matches found. Showing similar documents:
                
                1. Example Research Paper (Similarity: 23%)
                2. Introduction to Academic Integrity (Similarity: 17%)
                3. Student Guide to Citations (Similarity: 12%)
                """)
    else:
        st.info("Please upload a document or paste text to begin analysis.")
        
        # Show sample academic integrity guidelines
        with st.expander("Academic Integrity Guidelines", expanded=True):
            st.markdown("""
            ## Academic Integrity Guidelines
            
            ### What is Academic Integrity?
            Academic integrity is the commitment to and demonstration of honest and moral behavior in an academic setting. This is most relevant at the university level and includes:
            
            - Avoiding plagiarism (using someone else's words or ideas without proper attribution)
            - Properly citing sources
            - Completing your own work without unauthorized assistance
            - Being honest about research results
            
            ### Why is Academic Integrity Important?
            - Ensures the validity of your educational experience
            - Protects the reputation and value of your degree
            - Develops critical thinking and writing skills
            - Prepares you for ethical professional practice
            
            ### Common Academic Integrity Violations
            1. **Plagiarism**: Using others' work without proper citation
            2. **Fabrication**: Making up data or results
            3. **Cheating**: Using unauthorized assistance on assignments or exams
            4. **Self-Plagiarism**: Reusing your own work without permission
            5. **Improper Collaboration**: Working with others when instructed to work alone
            
            ### How to Maintain Academic Integrity
            - Always cite your sources properly
            - Take careful notes when researching
            - Plan ahead to avoid last-minute pressure
            - Ask your instructor if you're unsure about collaboration
            - Use plagiarism-checking tools to verify originality
            
            Our tool helps you maintain academic integrity by checking your work for potential issues before submission.
            """)
    
    # Information about the tools
    with st.sidebar:
        st.subheader("About Academic Integrity Tools")
        st.write("""
        These tools help ensure your academic work meets integrity standards. They analyze:
        
        - **Plagiarism**: Identifies potentially unoriginal content
        - **Grammar & Style**: Improves clarity and academic writing quality
        - **Citations**: Checks for proper attribution of sources
        - **Comprehensive Report**: Combines all analyses into one report
        - **Originality Database**: Tracks and manages analyzed documents
        """)
        
        st.info("Note: These tools use AI to assist in academic integrity checking but should not replace instructor guidance or institutional policies.")

# For testing the module independently
if __name__ == "__main__":
    # Set API key (for testing)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Display the interface
    display_academic_integrity_tools()
