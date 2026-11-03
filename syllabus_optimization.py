import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import docx
import fitz  # PyMuPDF for PDFs
import re
import json
import openai
import networkx as nx
import datetime
from dateutil import parser
from io import BytesIO
import calendar
import holidays
from datetime import datetime, date, timedelta, time

def ensure_datetime(date_obj):
    """Convert a date object to datetime if needed"""
    if isinstance(date_obj, date) and not isinstance(date_obj, datetime):
        # Convert date to datetime with time at midnight
        return datetime.combine(date_obj, time.min)
    return date_obj

def display_syllabus_optimization():
    """Main function to display the Syllabus Optimization Engine page"""
    
    st.title("🗓️ Syllabus Optimization Engine")
    
    # Set up tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs([
        "Syllabus Analysis", 
        "Topic Sequencing", 
        "Workload Distribution",
        "Calendar Optimization"
    ])
    
    # Initialize session state variables if they don't exist
    if "syllabus_content" not in st.session_state:
        st.session_state.syllabus_content = ""
    if "syllabus_topics" not in st.session_state:
        st.session_state.syllabus_topics = []
    if "syllabus_assignments" not in st.session_state:
        st.session_state.syllabus_assignments = []
    if "semester_start" not in st.session_state:
        st.session_state.semester_start = datetime.now().replace(month=(1 if datetime.now().month < 6 else 8), day=1)
    if "semester_end" not in st.session_state:
        st.session_state.semester_end = st.session_state.semester_start + timedelta(days=120)  # ~4 months
    if "course_metadata" not in st.session_state:
        st.session_state.course_metadata = {
            "course_code": "",
            "course_name": "",
            "credit_hours": 3,
            "meetings_per_week": 2,
            "session_length_mins": 75
        }
    
    # -------------------- TAB 1: SYLLABUS ANALYSIS --------------------
    with tab1:
        st.header("📄 Syllabus Analysis")
        
        # Allow user to upload a syllabus file
        st.subheader("Upload Your Syllabus")
        uploaded_file = st.file_uploader("Upload syllabus document (.pdf, .docx, .txt)", 
                                        type=["pdf", "docx", "txt"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            course_code = st.text_input("Course Code", st.session_state.course_metadata["course_code"])
            course_name = st.text_input("Course Name", st.session_state.course_metadata["course_name"])
        
        with col2:
            credit_hours = st.number_input("Credit Hours", min_value=1, max_value=6, 
                                           value=st.session_state.course_metadata["credit_hours"])
            meetings_per_week = st.number_input("Class Meetings Per Week", min_value=1, max_value=5, 
                                               value=st.session_state.course_metadata["meetings_per_week"])
            session_length = st.number_input("Session Length (minutes)", min_value=30, max_value=180, 
                                           value=st.session_state.course_metadata["session_length_mins"])
        
        # Update session state
        st.session_state.course_metadata = {
            "course_code": course_code,
            "course_name": course_name,
            "credit_hours": credit_hours,
            "meetings_per_week": meetings_per_week,
            "session_length_mins": session_length
        }
        
        # Set semester dates
        st.subheader("Semester Information")
        
        col1, col2 = st.columns(2)
        with col1:
            semester_start = st.date_input("Semester Start Date", st.session_state.semester_start)
        with col2:
            semester_end = st.date_input("Semester End Date", st.session_state.semester_end)
        
        # Update session state - ensure these are datetime objects
        st.session_state.semester_start = ensure_datetime(semester_start)
        st.session_state.semester_end = ensure_datetime(semester_end)
        
        # Process uploaded file
        if uploaded_file is not None:
            with st.spinner("Extracting syllabus content..."):
                # Extract text based on file type
                if uploaded_file.name.endswith('.pdf'):
                    text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.name.endswith('.docx'):
                    text = extract_text_from_docx(uploaded_file)
                else:  # .txt
                    text = uploaded_file.getvalue().decode("utf-8")
                
                st.session_state.syllabus_content = text
                
                # Extract key components from syllabus
                topics, assignments = extract_syllabus_components(text)
                
                if topics:
                    st.session_state.syllabus_topics = topics
                
                if assignments:
                    st.session_state.syllabus_assignments = assignments
        
        # Alternative: Allow manual entry of syllabus info
        st.subheader("Or Enter Syllabus Information Manually")
        
        manual_topics_tab, manual_assignments_tab = st.tabs(["Topics", "Assignments"])
        
        with manual_topics_tab:
            topics_text = st.text_area("Enter course topics (one per line)",
                                    "\n".join(st.session_state.syllabus_topics) if st.session_state.syllabus_topics else "",
                                    height=200)
            
            if st.button("Update Topics"):
                topics = [t.strip() for t in topics_text.split("\n") if t.strip()]
                st.session_state.syllabus_topics = topics
                st.success(f"Updated {len(topics)} topics")
        
        with manual_assignments_tab:
            # Create a DataFrame for assignments if it doesn't exist
            if not st.session_state.syllabus_assignments:
                st.session_state.syllabus_assignments = [{
                    "name": "Assignment 1",
                    "type": "Homework",
                    "weight": 10,
                    "due_date": st.session_state.semester_start + timedelta(days=14),
                    "estimated_hours": 3
                }]
            
            assignments_df = pd.DataFrame(st.session_state.syllabus_assignments)
            edited_df = st.data_editor(
                assignments_df,
                column_config={
                    "name": "Assignment Name",
                    "type": st.column_config.SelectboxColumn(
                        "Type",
                        options=["Homework", "Quiz", "Exam", "Project", "Paper", "Presentation", "Other"],
                    ),
                    "weight": st.column_config.NumberColumn(
                        "Weight (%)",
                        min_value=0,
                        max_value=100,
                        format="%d %%",
                    ),
                    "due_date": st.column_config.DateColumn("Due Date"),
                    "estimated_hours": st.column_config.NumberColumn(
                        "Est. Hours",
                        min_value=0,
                        max_value=40,
                    ),
                },
                num_rows="dynamic",
                use_container_width=True,
            )
            
            if st.button("Update Assignments"):
                st.session_state.syllabus_assignments = edited_df.to_dict('records')
                st.success(f"Updated {len(edited_df)} assignments")
        
        # Run Analysis button
        if st.button("📊 Run Syllabus Analysis", use_container_width=True):
            with st.spinner("Analyzing syllabus..."):
                analysis_results = analyze_syllabus(
                    st.session_state.syllabus_content,
                    st.session_state.syllabus_topics,
                    st.session_state.syllabus_assignments,
                    st.session_state.course_metadata,
                    st.session_state.semester_start,
                    st.session_state.semester_end
                )
                
                # Display analysis results
                st.subheader("Analysis Results")
                st.json(analysis_results)
                
                # Display visualization of workload distribution
                if st.session_state.syllabus_assignments:
                    st.subheader("Current Workload Distribution")
                    fig = visualize_workload_distribution(
                        st.session_state.syllabus_assignments,
                        st.session_state.semester_start,
                        st.session_state.semester_end
                    )
                    st.pyplot(fig)
                    
                # Get AI recommendations
                recommendations = get_syllabus_recommendations(
                    analysis_results, 
                    st.session_state.syllabus_topics, 
                    st.session_state.syllabus_assignments
                )
                
                st.subheader("AI Recommendations")
                st.write(recommendations)
    
    # -------------------- TAB 2: TOPIC SEQUENCING --------------------
    with tab2:
        st.header("🔄 Topic Sequencing Optimization")
        
        # Display current topics
        if st.session_state.syllabus_topics:
            st.subheader("Current Topic Sequence")
            for i, topic in enumerate(st.session_state.syllabus_topics, 1):
                st.write(f"{i}. {topic}")
            
            # Option to specify topic prerequisites
            st.subheader("Define Topic Dependencies")
            st.write("Select which topics are prerequisites for others")
            
            # Create a matrix for dependencies
            dependency_matrix = create_dependency_matrix(st.session_state.syllabus_topics)
            
            # Generate an optimized sequence
            if st.button("Generate Optimized Topic Sequence", use_container_width=True):
                with st.spinner("Analyzing topic dependencies and generating optimal sequence..."):
                    # Generate the dependency graph
                    optimized_sequence, graph = optimize_topic_sequence(
                        st.session_state.syllabus_topics,
                        dependency_matrix
                    )
                    
                    # Display the optimized sequence
                    st.subheader("Optimized Topic Sequence")
                    for i, topic in enumerate(optimized_sequence, 1):
                        st.write(f"{i}. {topic}")
                    
                    # Visualize the topic dependency graph
                    st.subheader("Topic Dependency Graph")
                    fig = visualize_dependency_graph(graph, st.session_state.syllabus_topics)
                    st.pyplot(fig)
                    
                    # Get AI explanation
                    explanation = get_sequence_explanation(
                        st.session_state.syllabus_topics,
                        optimized_sequence
                    )
                    
                    st.subheader("Explanation of Optimization")
                    st.write(explanation)
        else:
            st.info("Please add course topics in the Syllabus Analysis tab first.")
    
    # -------------------- TAB 3: WORKLOAD DISTRIBUTION --------------------
    with tab3:
        st.header("⚖️ Workload Distribution Analysis")
        
        if st.session_state.syllabus_assignments:
            # Display current assignment distribution
            st.subheader("Current Assignment Distribution")
            
            # Create a timeline visualization
            fig = visualize_assignment_timeline(
                st.session_state.syllabus_assignments,
                st.session_state.semester_start,
                st.session_state.semester_end
            )
            st.pyplot(fig)
            
            # Show workload heatmap
            st.subheader("Weekly Workload Heatmap")
            fig = visualize_workload_heatmap(
                st.session_state.syllabus_assignments,
                st.session_state.semester_start,
                st.session_state.semester_end
            )
            st.pyplot(fig)
            
            # Analyze workload and show statistics
            workload_stats = analyze_workload(
                st.session_state.syllabus_assignments,
                st.session_state.semester_start,
                st.session_state.semester_end
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Weekly Workload", f"{workload_stats['avg_weekly_hours']:.1f} hrs")
            with col2:
                st.metric("Max Weekly Workload", f"{workload_stats['max_weekly_hours']:.1f} hrs")
            with col3:
                st.metric("Workload Standard Deviation", f"{workload_stats['std_dev']:.1f} hrs")
            
            # Optimize workload button
            if st.button("Optimize Workload Distribution", use_container_width=True):
                with st.spinner("Optimizing assignment scheduling..."):
                    optimized_assignments = optimize_workload(
                        st.session_state.syllabus_assignments,
                        st.session_state.semester_start,
                        st.session_state.semester_end
                    )
                    
                    # Update the assignments
                    st.session_state.optimized_assignments = optimized_assignments
                    
                    # Show optimized distribution
                    st.subheader("Optimized Assignment Distribution")
                    
                    # Show the optimized timeline
                    fig = visualize_assignment_timeline(
                        optimized_assignments,
                        st.session_state.semester_start,
                        st.session_state.semester_end
                    )
                    st.pyplot(fig)
                    
                    # Show optimized workload heatmap
                    st.subheader("Optimized Weekly Workload Heatmap")
                    fig = visualize_workload_heatmap(
                        optimized_assignments,
                        st.session_state.semester_start,
                        st.session_state.semester_end
                    )
                    st.pyplot(fig)
                    
                    # Show change in statistics
                    optimized_stats = analyze_workload(
                        optimized_assignments,
                        st.session_state.semester_start,
                        st.session_state.semester_end
                    )
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("New Average Weekly Workload", 
                                 f"{optimized_stats['avg_weekly_hours']:.1f} hrs",
                                 f"{optimized_stats['avg_weekly_hours'] - workload_stats['avg_weekly_hours']:.1f}")
                    with col2:
                        st.metric("New Max Weekly Workload", 
                                 f"{optimized_stats['max_weekly_hours']:.1f} hrs",
                                 f"{optimized_stats['max_weekly_hours'] - workload_stats['max_weekly_hours']:.1f}")
                    with col3:
                        st.metric("New Workload Std Dev", 
                                 f"{optimized_stats['std_dev']:.1f} hrs",
                                 f"{optimized_stats['std_dev'] - workload_stats['std_dev']:.1f}")
                    
                    # Show the specific changes made
                    st.subheader("Recommended Assignment Changes")
                    changes = identify_assignment_changes(
                        st.session_state.syllabus_assignments,
                        optimized_assignments
                    )
                    
                    for change in changes:
                        st.info(change)
                    
                    # Option to apply changes
                    if st.button("Apply Optimized Schedule"):
                        st.session_state.syllabus_assignments = optimized_assignments
                        st.success("Applied optimized assignment schedule!")
                        st.rerun()
        else:
            st.info("Please add assignments in the Syllabus Analysis tab first.")
    
    # -------------------- TAB 4: CALENDAR OPTIMIZATION --------------------
    with tab4:
        st.header("📅 Semester Calendar Optimization")
        
        # Create calendar visualization
        st.subheader("Semester Calendar View")
        
        # Select country for holidays
        country = st.selectbox(
            "Select Country for Holiday Calendar",
            ["US", "UK", "Canada", "Australia", "India"],
            index=0
        )
        
        # Identify institutional events (holidays, breaks, etc.)
        year = st.session_state.semester_start.year
        holiday_calendar = get_holidays(country, year)
        
        # Visualize calendar with assignments, topics, and holidays
        calendar_fig = visualize_semester_calendar(
            st.session_state.semester_start,
            st.session_state.semester_end,
            st.session_state.syllabus_assignments,
            st.session_state.syllabus_topics,
            holiday_calendar,
            st.session_state.course_metadata
        )
        
        st.pyplot(calendar_fig)
        
        # Identify scheduling conflicts
        conflicts = identify_scheduling_conflicts(
            st.session_state.semester_start,
            st.session_state.semester_end,
            st.session_state.syllabus_assignments,
            holiday_calendar
        )
        
        if conflicts:
            st.subheader("⚠️ Identified Scheduling Conflicts")
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No major scheduling conflicts identified!")
        
        # Generate full semester schedule
        if st.button("Generate Complete Optimized Syllabus", use_container_width=True):
            with st.spinner("Generating optimized syllabus..."):
                # Combine topic sequencing and workload optimization
                optimized_schedule = generate_optimized_syllabus(
                    st.session_state.syllabus_topics,
                    st.session_state.syllabus_assignments,
                    st.session_state.semester_start,
                    st.session_state.semester_end,
                    st.session_state.course_metadata,
                    holiday_calendar
                )
                
                # Display the complete schedule
                st.subheader("Complete Optimized Schedule")
                
                # Show calendar with optimized schedule
                optimized_calendar = visualize_optimized_schedule(
                    optimized_schedule,
                    st.session_state.semester_start,
                    st.session_state.semester_end,
                    holiday_calendar
                )
                
                st.pyplot(optimized_calendar)
                
                # Generate syllabus document
                st.subheader("Generated Optimized Syllabus")
                syllabus_doc = generate_syllabus_document(
                    optimized_schedule,
                    st.session_state.course_metadata,
                    st.session_state.semester_start,
                    st.session_state.semester_end
                )
                
                # Preview and download options
                st.text_area("Syllabus Preview", syllabus_doc, height=300)
                
                # Prepare download as docx
                docx_buffer = generate_syllabus_docx(
                    optimized_schedule,
                    st.session_state.course_metadata,
                    st.session_state.semester_start,
                    st.session_state.semester_end
                )
                
                st.download_button(
                    label="Download Optimized Syllabus (DOCX)",
                    data=docx_buffer,
                    file_name=f"{st.session_state.course_metadata['course_code']}_Optimized_Syllabus.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

# ======================== HELPER FUNCTIONS ========================

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file"""
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_text_from_docx(uploaded_file):
    """Extract text from a DOCX file"""
    try:
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {str(e)}")
        return ""

def extract_syllabus_components(text):
    """Extract topics and assignments from syllabus text using AI"""
    try:
        # Use OpenAI to extract structured information from syllabus
        prompt = f"""
        Extract the following information from this syllabus:
        1. A list of course topics/modules
        2. A list of assignments with due dates, types (exam, homework, etc.), and weights if available
        
        Format the response as JSON with these keys:
        - "topics": [list of topic strings]
        - "assignments": [list of objects with "name", "type", "due_date" (if available), "weight" (if available)]
        
        Syllabus content:
        {text[:4000]}  # Limiting to first 4000 chars to stay within token limits
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You extract structured information from syllabus documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
            
        result = json.loads(result_text)
        
        # Process topics
        topics = result.get("topics", [])
        
        # Process assignments
        assignments = []
        for assignment in result.get("assignments", []):
            # Convert date strings to datetime objects if available
            due_date = None
            if "due_date" in assignment and assignment["due_date"]:
                try:
                    due_date = parser.parse(assignment["due_date"])
                except:
                    pass
            
            assignments.append({
                "name": assignment.get("name", "Unnamed Assignment"),
                "type": assignment.get("type", "Other"),
                "weight": float(assignment.get("weight", 0)),
                "due_date": due_date or datetime.now() + timedelta(days=30),  # Default if not found
                "estimated_hours": float(assignment.get("estimated_hours", 3))  # Default estimate
            })
        
        return topics, assignments
        
    except Exception as e:
        st.error(f"Error extracting components: {str(e)}")
        return [], []

def analyze_syllabus(syllabus_content, topics, assignments, metadata, semester_start, semester_end):
    """Analyze syllabus for potential improvements"""
    # Ensure semester_start and semester_end are datetime objects for subtraction
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    results = {
        "total_topics": len(topics),
        "total_assignments": len(assignments),
        "semester_weeks": (semester_end_dt - semester_start_dt).days // 7,
        "topics_per_week": len(topics) / ((semester_end_dt - semester_start_dt).days / 7) if topics else 0,
        "assignment_distribution": {},
        "workload_balance": {},
        "potential_issues": []
    }
    
    # Check if topics are evenly distributed
    if len(topics) > 0:
        weeks = (semester_end_dt - semester_start_dt).days / 7
        if len(topics) / weeks > 2:
            results["potential_issues"].append("High topic density: More than 2 topics per week on average")
    
    # Analyze assignment distribution
    if assignments:
        # Count assignments by type
        type_counts = {}
        for assignment in assignments:
            assignment_type = assignment.get("type", "Other")
            type_counts[assignment_type] = type_counts.get(assignment_type, 0) + 1
        results["assignment_distribution"] = type_counts
        
        # Check workload balance
        weekly_workload = {}
        for assignment in assignments:
            due_date = assignment.get("due_date")
            if due_date:
                # Convert due_date to datetime if needed
                due_date_dt = ensure_datetime(due_date)
                
                # Calculate week_num
                week_num = (due_date_dt - semester_start_dt).days // 7
                weekly_workload[week_num] = weekly_workload.get(week_num, 0) + assignment.get("estimated_hours", 3)
        
        results["workload_balance"] = weekly_workload
        
        # Check for workload spikes
        weekly_hours = list(weekly_workload.values())
        if weekly_hours:
            avg_workload = sum(weekly_hours) / len(weekly_hours)
            max_workload = max(weekly_hours)
            if max_workload > 2 * avg_workload:
                results["potential_issues"].append(f"Workload spike detected: Max weekly workload ({max_workload:.1f} hrs) is more than twice the average ({avg_workload:.1f} hrs)")
    
    # Check credit hours vs. workload
    total_estimated_hours = sum(assignment.get("estimated_hours", 3) for assignment in assignments)
    expected_hours = metadata["credit_hours"] * 3 * results["semester_weeks"]  # Rule of thumb: 3 hours outside class per credit hour
    
    if total_estimated_hours > expected_hours * 1.2:
        results["potential_issues"].append(f"Excessive workload: Estimated {total_estimated_hours:.1f} hours exceeds the expected {expected_hours:.1f} hours by more than 20%")
    elif total_estimated_hours < expected_hours * 0.8:
        results["potential_issues"].append(f"Light workload: Estimated {total_estimated_hours:.1f} hours is less than 80% of the expected {expected_hours:.1f} hours")
    
    # Check assignment weights
    total_weight = sum(assignment.get("weight", 0) for assignment in assignments)
    if total_weight < 99 or total_weight > 101:
        results["potential_issues"].append(f"Assignment weights total {total_weight:.1f}%, instead of 100%")
    
    return results

def visualize_workload_distribution(assignments, semester_start, semester_end):
    """Visualize workload distribution across the semester"""
    # Ensure semester_start and semester_end are datetime objects for subtraction
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Create a dataframe with weekly workload
    weeks = (semester_end_dt - semester_start_dt).days // 7 + 1
    weekly_workload = [0] * weeks
    
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if due_date:
            # Convert due_date to datetime if needed
            due_date_dt = ensure_datetime(due_date)
            
            week_idx = min((due_date_dt - semester_start_dt).days // 7, weeks - 1)
            weekly_workload[week_idx] += assignment.get("estimated_hours", 3)
    
    # Create the visualization
    fig, ax = plt.subplots(figsize=(10, 5))
    week_labels = [f"Week {i+1}" for i in range(weeks)]
    ax.bar(week_labels, weekly_workload)
    ax.set_xlabel("Week of Semester")
    ax.set_ylabel("Estimated Hours")
    ax.set_title("Student Workload Distribution")
    plt.xticks(rotation=45, ha="right")
    
    # Add a horizontal line for average workload
    avg_workload = sum(weekly_workload) / weeks
    ax.axhline(y=avg_workload, color='r', linestyle='--', label=f"Avg: {avg_workload:.1f} hrs")
    ax.legend()
    
    # Add annotations for high workload weeks
    for i, hours in enumerate(weekly_workload):
        if hours > avg_workload * 1.5:
            ax.annotate(f"{hours:.1f} hrs",
                      xy=(i, hours),
                      xytext=(0, 5),
                      textcoords="offset points",
                      ha='center', va='bottom')
    
    plt.tight_layout()
    return fig

def get_syllabus_recommendations(analysis_results, topics, assignments):
    """Get AI recommendations for syllabus improvements"""
    # Convert analysis results to a readable format
    analysis_text = json.dumps(analysis_results, indent=2)
    
    # Create the prompt
    prompt = f"""
    As an educational expert, analyze this syllabus data and provide specific recommendations for improvement:
    
    Analysis Results:
    {analysis_text}
    
    Topics ({len(topics)}):
    {topics[:5]}{"..." if len(topics) > 5 else ""}
    
    Assignments ({len(assignments)}):
    {[(a['name'], a['type'], a['due_date'].strftime('%Y-%m-%d') if hasattr(a['due_date'], 'strftime') else a['due_date'], a['weight']) for a in assignments[:3]]}{"..." if len(assignments) > 3 else ""}
    
    Provide 3-5 specific, actionable recommendations to improve this syllabus in terms of:
    1. Topic sequencing and pacing
    2. Workload distribution
    3. Assignment balance and timing
    
    For each recommendation, explain WHY this change would benefit students and instructors.
    """
    
    # Get recommendations from AI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in curriculum design and instructional planning who provides practical advice for improving course syllabi."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        
        recommendations = response.choices[0].message.content.strip()
        return recommendations
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"

def create_dependency_matrix(topics):
    """Create a UI for defining topic dependencies"""
    st.write("For each topic, select which other topics are prerequisites:")
    
    # Create dictionary to store dependencies
    if "dependency_dict" not in st.session_state:
        st.session_state.dependency_dict = {topic: [] for topic in topics}
    
    # Show topic dependencies
    for i, topic in enumerate(topics):
        # Can't select itself or topics that come after it as prerequisites
        options = [t for j, t in enumerate(topics) if j != i]
        
        selected = st.multiselect(
            f"Prerequisites for: **{topic}**",
            options=options,
            default=st.session_state.dependency_dict.get(topic, [])
        )
        
        st.session_state.dependency_dict[topic] = selected
    
    # Convert to matrix form
    dependency_matrix = np.zeros((len(topics), len(topics)))
    
    for i, topic in enumerate(topics):
        for prereq in st.session_state.dependency_dict[topic]:
            j = topics.index(prereq)
            dependency_matrix[i, j] = 1
    
    return dependency_matrix

def optimize_topic_sequence(topics, dependency_matrix):
    """Generate an optimized topic sequence based on dependencies"""
    # Create a directed graph from the dependency matrix
    G = nx.DiGraph()
    
    # Add nodes
    for i, topic in enumerate(topics):
        G.add_node(i, name=topic)
    
    # Add edges
    for i in range(len(topics)):
        for j in range(len(topics)):
            if dependency_matrix[i, j] == 1:
                G.add_edge(j, i)  # j is a prerequisite for i
    
    # Check for cycles
    try:
        cycles = list(nx.simple_cycles(G))
        if cycles:
            st.warning(f"⚠️ Circular dependencies detected: {cycles}")
            # Break the cycle by removing the least important edge
            for cycle in cycles:
                # Remove the first edge of each cycle
                if len(cycle) > 1:
                    G.remove_edge(cycle[0], cycle[1])
    except:
        pass
    
    # Perform topological sort to get optimal sequence
    try:
        sorted_indices = list(nx.topological_sort(G))
        optimized_sequence = [topics[i] for i in sorted_indices]
        return optimized_sequence, G
    except nx.NetworkXUnfeasible:
        st.error("Could not create a valid sequence due to cyclic dependencies")
        return topics, G  # Return original order if sort fails

def visualize_dependency_graph(graph, topics):
    """Visualize the topic dependency graph"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Get positions for nodes
    pos = nx.spring_layout(graph, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=700, node_color='lightblue', alpha=0.8)
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowsize=15, width=1.5, alpha=0.7)
    
    # Draw labels
    labels = {i: topics[i] for i in range(len(topics))}
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, font_weight='bold')
    
    plt.title("Topic Dependency Graph")
    plt.axis('off')
    plt.tight_layout()
    
    return fig

def get_sequence_explanation(original_sequence, optimized_sequence):
    """Get AI explanation for the optimized sequence"""
    prompt = f"""
    Compare the original topic sequence with the optimized sequence and explain the reasoning behind the changes:
    
    Original Sequence:
    {original_sequence}
    
    Optimized Sequence:
    {optimized_sequence}
    
    Please explain:
    1. What key changes were made and why
    2. How the new sequence improves logical flow of learning
    3. How this might benefit student understanding
    
    Keep your explanation clear and concise, focusing on the pedagogical benefits.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in curriculum design who explains topic sequencing rationales."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=500
        )
        
        explanation = response.choices[0].message.content.strip()
        return explanation
    except Exception as e:
        return f"Error generating explanation: {str(e)}"

def visualize_assignment_timeline(assignments, semester_start, semester_end):
    """Visualize assignments on a timeline"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Create a list of assignment categories
    categories = list(set(a.get("type", "Other") for a in assignments))
    colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))
    category_colors = {cat: colors[i] for i, cat in enumerate(categories)}
    
    # Create x-axis (dates)
    days = (semester_end_dt - semester_start_dt).days
    dates = [semester_start_dt + timedelta(days=d) for d in range(days)]
    
    # Plot assignments
    for i, assignment in enumerate(assignments):
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        assignment_type = assignment.get("type", "Other")
        weight = assignment.get("weight", 0)
        name = assignment.get("name", f"Assignment {i+1}")
        
        # Convert to datetime if needed and calculate position on timeline
        due_date_dt = ensure_datetime(due_date)
        position = (due_date_dt - semester_start_dt).days
            
        if 0 <= position <= days:
            # Plot point with size based on weight
            point_size = max(50, weight * 10) if weight > 0 else 50
            ax.scatter(position, i, s=point_size, color=category_colors[assignment_type], 
                     alpha=0.7, edgecolors='black', zorder=2)
            
            # Add label
            ax.annotate(name, 
                      xy=(position, i), 
                      xytext=(5, 0),
                      textcoords="offset points",
                      va='center')
    
    # Set y-axis
    ax.set_yticks([])  # Hide y-axis ticks
    
    # Set x-axis
    week_ticks = list(range(0, days, 7))
    week_labels = [f"Week {i//7 + 1}" for i in week_ticks]
    ax.set_xticks(week_ticks)
    ax.set_xticklabels(week_labels, rotation=45, ha='right')
    ax.set_xlim(-5, days + 5)
    
    # Add grid
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Add legend for assignment types
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor=color, markersize=10, label=cat)
                     for cat, color in category_colors.items()]
    ax.legend(handles=legend_elements, title="Assignment Types", loc='upper right')
    
    # Labels and title
    ax.set_title('Assignment Timeline')
    ax.set_xlabel('Semester Timeline')
    
    plt.tight_layout()
    return fig

def visualize_workload_heatmap(assignments, semester_start, semester_end):
    """Create a heatmap of weekly workload"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Calculate total weeks
    total_weeks = (semester_end_dt - semester_start_dt).days // 7 + 1
    
    # Create data for each week and assignment type
    categories = list(set(a.get("type", "Other") for a in assignments))
    weekly_workload = np.zeros((len(categories), total_weeks))
    
    # Populate data
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        assignment_type = assignment.get("type", "Other")
        hours = assignment.get("estimated_hours", 3)
        
        # Convert to datetime and calculate week index
        due_date_dt = ensure_datetime(due_date)
        week_idx = min((due_date_dt - semester_start_dt).days // 7, total_weeks - 1)
            
        # Update workload for that week and category
        cat_idx = categories.index(assignment_type)
        weekly_workload[cat_idx, week_idx] += hours
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot heatmap
    im = ax.imshow(weekly_workload, cmap='YlOrRd')
    
    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Estimated Hours", rotation=-90, va="bottom")
    
    # Set ticks and labels
    ax.set_xticks(np.arange(total_weeks))
    ax.set_xticklabels([f"Week {i+1}" for i in range(total_weeks)])
    ax.set_yticks(np.arange(len(categories)))
    ax.set_yticklabels(categories)
    
    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Annotate cells with values
    for i in range(len(categories)):
        for j in range(total_weeks):
            if weekly_workload[i, j] > 0:
                text = ax.text(j, i, f"{weekly_workload[i, j]:.1f}",
                             ha="center", va="center", color="black" if weekly_workload[i, j] < 8 else "white")
    
    # Title and labels
    ax.set_title("Weekly Workload by Assignment Type")
    ax.set_xlabel("Semester Timeline")
    
    fig.tight_layout()
    return fig

def analyze_workload(assignments, semester_start, semester_end):
    """Analyze workload distribution and provide statistics"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Calculate total weeks
    total_weeks = (semester_end_dt - semester_start_dt).days // 7 + 1
    
    # Create weekly workload array
    weekly_workload = [0] * total_weeks
    
    # Populate data
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        hours = assignment.get("estimated_hours", 3)
        
        # Convert to datetime and calculate week index
        due_date_dt = ensure_datetime(due_date)
        week_idx = min((due_date_dt - semester_start_dt).days // 7, total_weeks - 1)
            
        # Update workload for that week
        weekly_workload[week_idx] += hours
    
    # Calculate statistics
    stats = {
        "avg_weekly_hours": sum(weekly_workload) / total_weeks,
        "max_weekly_hours": max(weekly_workload) if weekly_workload else 0,
        "min_weekly_hours": min(weekly_workload) if weekly_workload else 0,
        "std_dev": np.std(weekly_workload),
        "total_hours": sum(weekly_workload),
        "weeks_above_avg": sum(1 for w in weekly_workload if w > sum(weekly_workload) / total_weeks),
        "weekly_data": weekly_workload
    }
    
    return stats

def optimize_workload(assignments, semester_start, semester_end):
    """Optimize workload distribution across the semester"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Copy assignments to avoid modifying the original
    optimized = assignments.copy()
    
    # Get current workload stats
    current_stats = analyze_workload(optimized, semester_start_dt, semester_end_dt)
    
    # Get total weeks
    total_weeks = (semester_end_dt - semester_start_dt).days // 7 + 1
    
    # Create optimization algorithm
    
    # Step 1: Identify weeks with high workload
    weekly_data = current_stats["weekly_data"]
    avg_workload = current_stats["avg_weekly_hours"]
    high_load_weeks = [i for i, load in enumerate(weekly_data) if load > avg_workload * 1.5]
    
    # Step 2: Identify weeks with low workload that can accept more assignments
    low_load_weeks = [i for i, load in enumerate(weekly_data) if load < avg_workload * 0.8]
    
    # Step 3: Move assignments from high load weeks to low load weeks when possible
    if high_load_weeks and low_load_weeks:
        # Sort assignments by estimated hours (largest first)
        sorted_assignments = sorted(
            [(i, a) for i, a in enumerate(optimized) if isinstance(a.get("due_date"), date) or isinstance(a.get("due_date"), datetime)],
            key=lambda x: x[1].get("estimated_hours", 3),
            reverse=True
        )
        
        for idx, assignment in sorted_assignments:
            due_date = assignment.get("due_date")
            if not due_date:
                continue
                
            # Convert to datetime
            due_date_dt = ensure_datetime(due_date)
            current_week = (due_date_dt - semester_start_dt).days // 7
            
            # If this assignment is due in a high load week
            if current_week in high_load_weeks:
                hours = assignment.get("estimated_hours", 3)
                assignment_type = assignment.get("type", "Other")
                
                # Find appropriate low load week
                # 1. Prefer weeks after prerequisites but before the current due date
                # 2. If not possible, find a week shortly after the current due date
                
                # Find valid low load weeks
                valid_low_weeks = [w for w in low_load_weeks if w < current_week]
                
                if not valid_low_weeks:
                    # If no valid weeks before, look for weeks after
                    valid_low_weeks = [w for w in low_load_weeks if w > current_week]
                
                if valid_low_weeks:
                    # Choose the week that would make workload most balanced
                    target_week = min(valid_low_weeks, 
                                      key=lambda w: abs((weekly_data[w] + hours) - avg_workload))
                    
                    # Update the assignment due date
                    new_date = semester_start_dt + timedelta(days=target_week * 7 + 3)  # Middle of week
                    optimized[idx]["due_date"] = new_date
                    
                    # Update weekly workload data
                    weekly_data[current_week] -= hours
                    weekly_data[target_week] += hours
                    
                    # Update high/low load weeks
                    if weekly_data[current_week] <= avg_workload * 1.5 and current_week in high_load_weeks:
                        high_load_weeks.remove(current_week)
                    if weekly_data[target_week] >= avg_workload * 0.8 and target_week in low_load_weeks:
                        low_load_weeks.remove(target_week)
    
    return optimized

def identify_assignment_changes(original, optimized):
    """Identify the changes made to assignment schedule"""
    changes = []
    
    for i, (orig, opt) in enumerate(zip(original, optimized)):
        orig_date = orig.get("due_date")
        opt_date = opt.get("due_date")
        
        if orig_date and opt_date and orig_date != opt_date:
            # Convert dates to datetime objects
            orig_date_dt = ensure_datetime(orig_date)
            opt_date_dt = ensure_datetime(opt_date)
            semester_start_dt = ensure_datetime(st.session_state.semester_start)
            
            # Calculate week numbers
            orig_week = (orig_date_dt - semester_start_dt).days // 7 + 1
            opt_week = (opt_date_dt - semester_start_dt).days // 7 + 1
            
            changes.append(
                f"Move '{orig.get('name')}' from Week {orig_week} ({orig_date_dt.strftime('%b %d')}) "
                f"to Week {opt_week} ({opt_date_dt.strftime('%b %d')})"
            )
    
    return changes

def get_holidays(country, year):
    """Get holidays for a specific country and year"""
    try:
        country_holidays = holidays.country_holidays(country, years=year)
        return country_holidays
    except:
        # Fallback to US holidays if country not available
        return holidays.US(years=year)

def visualize_semester_calendar(semester_start, semester_end, assignments, topics, holiday_calendar, course_metadata):
    """Visualize semester calendar with assignments, topics, and holidays"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Calculate semester weeks
    days = (semester_end_dt - semester_start_dt).days
    weeks = days // 7 + 1
    
    # Create calendar grid (weeks x days)
    calendar_grid = np.zeros((weeks, 7))
    
    # Days of week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Fill in holidays
    for d in range(days):
        current_date = semester_start_dt + timedelta(days=d)
        week_idx = d // 7
        day_idx = current_date.weekday()
        
        # Check if it's a holiday
        if current_date in holiday_calendar:
            calendar_grid[week_idx, day_idx] = 1
    
    # Mark class days based on metadata
    # Assume classes are held on weekdays (0-4 = Monday-Friday)
    meetings_per_week = course_metadata["meetings_per_week"]
    
    if meetings_per_week == 1:
        class_days = [0]  # Monday
    elif meetings_per_week == 2:
        class_days = [0, 2]  # Monday, Wednesday
    elif meetings_per_week == 3:
        class_days = [0, 2, 4]  # Monday, Wednesday, Friday
    else:
        class_days = list(range(meetings_per_week))  # First n days of week
    
    # Add class days to calendar
    for week in range(weeks):
        for day in class_days:
            if day < 7:
                if calendar_grid[week, day] != 1:  # Not a holiday
                    calendar_grid[week, day] = 2  # Class day
    
    # Add assignments to calendar
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        # Convert to datetime and calculate position
        due_date_dt = ensure_datetime(due_date)
        week_idx = (due_date_dt - semester_start_dt).days // 7
        day_idx = due_date_dt.weekday()
        
        if 0 <= week_idx < weeks and 0 <= day_idx < 7:
            calendar_grid[week_idx, day_idx] = 3  # Assignment due
    
    # Create heatmap
    cmap = plt.cm.colors.ListedColormap(['white', 'red', 'lightblue', 'orange'])
    bounds = [0, 0.5, 1.5, 2.5, 3.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
    
    # Plot calendar
    im = ax.imshow(calendar_grid, cmap=cmap, norm=norm)
    
    # Add grid
    ax.grid(which='both', color='black', linestyle='-', linewidth=0.5)
    
    # Set ticks
    ax.set_xticks(np.arange(len(days_of_week)))
    ax.set_yticks(np.arange(weeks))
    
    # Set labels
    ax.set_xticklabels(days_of_week)
    week_labels = [f"Week {w+1}" for w in range(weeks)]
    ax.set_yticklabels(week_labels)
    
    # Add specific dates to week labels
    for week in range(weeks):
        week_start = semester_start_dt + timedelta(days=week*7)
        week_text = f"{week_labels[week]}\n{week_start.strftime('%b %d')}"
        ax.text(-0.8, week, week_text, va='center')
    
    # Create legend
    legend_elements = [
        plt.Rectangle((0,0), 1, 1, facecolor='white', edgecolor='black', label='Regular Day'),
        plt.Rectangle((0,0), 1, 1, facecolor='red', edgecolor='black', label='Holiday'),
        plt.Rectangle((0,0), 1, 1, facecolor='lightblue', edgecolor='black', label='Class Day'),
        plt.Rectangle((0,0), 1, 1, facecolor='orange', edgecolor='black', label='Assignment Due')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Add assignment annotations
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        # Convert to datetime and calculate position
        due_date_dt = ensure_datetime(due_date)
        week_idx = (due_date_dt - semester_start_dt).days // 7
        day_idx = due_date_dt.weekday()
        
        if 0 <= week_idx < weeks and 0 <= day_idx < 7:
            ax.text(day_idx, week_idx, assignment.get("name", ""),
                  ha='center', va='center', fontsize=8, color='black',
                  bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Title
    course_name = course_metadata.get("course_name", "Course")
    course_code = course_metadata.get("course_code", "")
    plt.title(f"{course_code} {course_name} - Semester Calendar")
    
    plt.tight_layout()
    return fig

def identify_scheduling_conflicts(semester_start, semester_end, assignments, holiday_calendar):
    """Identify potential scheduling conflicts"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    conflicts = []
    
    # Check for assignments due on holidays
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        # Convert to datetime
        due_date_dt = ensure_datetime(due_date)
        
        if due_date_dt in holiday_calendar:
            holiday_name = holiday_calendar[due_date_dt]
            conflicts.append(
                f"Assignment '{assignment.get('name')}' is due on a holiday: {due_date_dt.strftime('%b %d')} ({holiday_name})"
            )
    
    # Check for assignments due on weekends
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        # Convert to datetime
        due_date_dt = ensure_datetime(due_date)
        
        if due_date_dt.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][due_date_dt.weekday()]
            conflicts.append(
                f"Assignment '{assignment.get('name')}' is due on a weekend: {due_date_dt.strftime('%b %d')} ({day_name})"
            )
    
    # Check for multiple major assignments due in same week
    weeks_with_assignments = {}
    major_types = ["Exam", "Project", "Paper"]
    
    for assignment in assignments:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        assignment_type = assignment.get("type", "")
        
        # Convert to datetime
        due_date_dt = ensure_datetime(due_date)
        
        if assignment_type in major_types:
            week_idx = (due_date_dt - semester_start_dt).days // 7
            if week_idx not in weeks_with_assignments:
                weeks_with_assignments[week_idx] = []
            weeks_with_assignments[week_idx].append(assignment.get("name", ""))
    
    for week, assignments_list in weeks_with_assignments.items():
        if len(assignments_list) > 1:
            week_start = semester_start_dt + timedelta(days=week*7)
            conflicts.append(
                f"Multiple major assignments due in Week {week+1} ({week_start.strftime('%b %d')}): {', '.join(assignments_list)}"
            )
    
    # Check for periods with high assignment density
    assignment_dates = [ensure_datetime(a.get("due_date")) for a in assignments if a.get("due_date")]
    date_counts = {}
    
    for date in assignment_dates:
        week_idx = (date - semester_start_dt).days // 7
        if week_idx not in date_counts:
            date_counts[week_idx] = 0
        date_counts[week_idx] += 1
    
    for week, count in date_counts.items():
        if count > 3:
            week_start = semester_start_dt + timedelta(days=week*7)
            conflicts.append(
                f"High assignment density in Week {week+1} ({week_start.strftime('%b %d')}): {count} assignments due"
            )
    
    return conflicts

def generate_optimized_syllabus(topics, assignments, semester_start, semester_end, course_metadata, holiday_calendar):
    """Generate a fully optimized syllabus combining all optimization features"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Step 1: Optimize topic sequence
    if "dependency_dict" in st.session_state and topics:
        # Create dependency matrix from stored data
        dependency_matrix = np.zeros((len(topics), len(topics)))
        for i, topic in enumerate(topics):
            for prereq in st.session_state.dependency_dict.get(topic, []):
                if prereq in topics:
                    j = topics.index(prereq)
                    dependency_matrix[i, j] = 1
        
        # Run sequence optimization
        optimized_topics, _ = optimize_topic_sequence(topics, dependency_matrix)
    else:
        optimized_topics = topics
    
    # Step 2: Optimize workload distribution
    optimized_assignments = optimize_workload(assignments, semester_start_dt, semester_end_dt)
    
    # Step 3: Allocate topics to specific weeks
    # Account for holidays and create a schedule of class meetings
    
    # Get class days
    meetings_per_week = course_metadata["meetings_per_week"]
    
    if meetings_per_week == 1:
        class_days = [0]  # Monday
    elif meetings_per_week == 2:
        class_days = [0, 2]  # Monday, Wednesday
    elif meetings_per_week == 3:
        class_days = [0, 2, 4]  # Monday, Wednesday, Friday
    else:
        class_days = list(range(meetings_per_week))  # First n days of week
    
    # Calculate total class sessions (accounting for holidays)
    class_sessions = []
    current_date = semester_start_dt
    
    while current_date <= semester_end_dt:
        if current_date.weekday() in class_days and current_date not in holiday_calendar:
            class_sessions.append(current_date)
        current_date += timedelta(days=1)
    
    # Allocate topics to class sessions
    topic_schedule = []
    topics_per_session = max(1, len(optimized_topics) // len(class_sessions)) if class_sessions else 1
    
    for i, session_date in enumerate(class_sessions):
        start_idx = i * topics_per_session
        end_idx = min(start_idx + topics_per_session, len(optimized_topics))
        
        session_topics = optimized_topics[start_idx:end_idx] if start_idx < len(optimized_topics) else []
        
        if session_topics:
            topic_schedule.append({
                "date": session_date,
                "week": (session_date - semester_start_dt).days // 7 + 1,
                "topics": session_topics
            })
    
    # Create complete schedule with both topics and assignments
    complete_schedule = {
        "course_info": course_metadata,
        "semester_start": semester_start_dt,
        "semester_end": semester_end_dt,
        "topics": topic_schedule,
        "assignments": optimized_assignments
    }
    
    return complete_schedule

def visualize_optimized_schedule(schedule, semester_start, semester_end, holiday_calendar):
    """Visualize the optimized schedule"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Calculate semester weeks
    days = (semester_end_dt - semester_start_dt).days
    weeks = days // 7 + 1
    
    # Create calendar grid (weeks x days)
    calendar_grid = np.zeros((weeks, 7))
    
    # Days of week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Fill in holidays
    for d in range(days):
        current_date = semester_start_dt + timedelta(days=d)
        week_idx = d // 7
        day_idx = current_date.weekday()
        
        # Check if it's a holiday
        if current_date in holiday_calendar:
            calendar_grid[week_idx, day_idx] = 1
    
    # Fill in class sessions with topics
    for session in schedule["topics"]:
        date = ensure_datetime(session["date"])
        week_idx = (date - semester_start_dt).days // 7
        day_idx = date.weekday()
        
        if 0 <= week_idx < weeks and 0 <= day_idx < 7:
            calendar_grid[week_idx, day_idx] = 2  # Class with topics
    
    # Fill in assignments
    for assignment in schedule["assignments"]:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        due_date_dt = ensure_datetime(due_date)
        week_idx = (due_date_dt - semester_start_dt).days // 7
        day_idx = due_date_dt.weekday()
        
        if 0 <= week_idx < weeks and 0 <= day_idx < 7:
            calendar_grid[week_idx, day_idx] = 3  # Assignment due
    
    # Create heatmap
    cmap = plt.cm.colors.ListedColormap(['white', 'red', 'lightblue', 'orange'])
    bounds = [0, 0.5, 1.5, 2.5, 3.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
    
    # Plot calendar
    im = ax.imshow(calendar_grid, cmap=cmap, norm=norm)
    
    # Add grid
    ax.grid(which='both', color='black', linestyle='-', linewidth=0.5)
    
    # Set ticks
    ax.set_xticks(np.arange(len(days_of_week)))
    ax.set_yticks(np.arange(weeks))
    
    # Set labels
    ax.set_xticklabels(days_of_week)
    week_labels = [f"Week {w+1}" for w in range(weeks)]
    ax.set_yticklabels(week_labels)
    
    # Add specific dates to week labels
    for week in range(weeks):
        week_start = semester_start_dt + timedelta(days=week*7)
        week_text = f"{week_labels[week]}\n{week_start.strftime('%b %d')}"
        ax.text(-0.8, week, week_text, va='center')
    
    # Create legend
    legend_elements = [
        plt.Rectangle((0,0), 1, 1, facecolor='white', edgecolor='black', label='Regular Day'),
        plt.Rectangle((0,0), 1, 1, facecolor='red', edgecolor='black', label='Holiday'),
        plt.Rectangle((0,0), 1, 1, facecolor='lightblue', edgecolor='black', label='Class with Topics'),
        plt.Rectangle((0,0), 1, 1, facecolor='orange', edgecolor='black', label='Assignment Due')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Annotate class sessions with topics
    for session in schedule["topics"]:
        date = ensure_datetime(session["date"])
        week_idx = (date - semester_start_dt).days // 7
        day_idx = date.weekday()
        topics_text = ", ".join(session["topics"])
        
        if 0 <= week_idx < weeks and 0 <= day_idx < 7:
            # Truncate if too long
            if len(topics_text) > 30:
                topics_text = topics_text[:27] + "..."
                
            ax.text(day_idx, week_idx, topics_text,
                  ha='center', va='center', fontsize=7, color='black',
                  bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))
    
    # Annotate assignments
    for assignment in schedule["assignments"]:
        due_date = assignment.get("due_date")
        if not due_date:
            continue
            
        due_date_dt = ensure_datetime(due_date)
        week_idx = (due_date_dt - semester_start_dt).days // 7
        day_idx = due_date_dt.weekday()
        
        if 0 <= week_idx < weeks and 0 <= day_idx < 7:
            # Get assignment name and truncate if needed
            name = assignment.get("name", "")
            if len(name) > 20:
                name = name[:17] + "..."
                
            # Position text slightly below center to avoid overlapping with topics
            ax.text(day_idx, week_idx + 0.3, name,
                  ha='center', va='center', fontsize=7, color='black', weight='bold',
                  bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.9))
    
    # Title
    course_name = schedule["course_info"].get("course_name", "Course")
    course_code = schedule["course_info"].get("course_code", "")
    plt.title(f"{course_code} {course_name} - Optimized Schedule")
    
    plt.tight_layout()
    return fig

def generate_syllabus_document(schedule, course_metadata, semester_start, semester_end):
    """Generate a text version of the optimized syllabus"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Format course information
    course_code = course_metadata.get("course_code", "")
    course_name = course_metadata.get("course_name", "")
    credit_hours = course_metadata.get("credit_hours", 3)
    
    # Start building the syllabus document
    syllabus = f"""
# {course_code}: {course_name}
## {semester_start_dt.strftime('%B %Y')} to {semester_end_dt.strftime('%B %Y')}

**Credit Hours:** {credit_hours}

## Course Description
This is an automatically optimized syllabus for {course_code}: {course_name}.

## Learning Objectives
By the end of this course, students will be able to:
1. Understand key concepts in {course_name}
2. Apply theoretical knowledge to practical problems
3. Analyze and evaluate approaches in the field

## Course Schedule

"""
    
    # Add weekly schedule
    current_week = 0
    for session in schedule["topics"]:
        week = session["week"]
        session_date = ensure_datetime(session["date"])
        
        if week != current_week:
            current_week = week
            end_date = session_date + timedelta(days=6)
            syllabus += f"\n### Week {week}: {session_date.strftime('%B %d')} - {end_date.strftime('%B %d')}\n"
        
        syllabus += f"- **{session_date.strftime('%A, %B %d')}**: {', '.join(session['topics'])}\n"
    
    # Add assignments section
    syllabus += "\n## Assignments\n\n"
    
    # Group assignments by type
    assignment_types = {}
    for assignment in schedule["assignments"]:
        assignment_type = assignment.get("type", "Other")
        if assignment_type not in assignment_types:
            assignment_types[assignment_type] = []
        assignment_types[assignment_type].append(assignment)
    
    # Add each type of assignment
    for assignment_type, assignments_list in assignment_types.items():
        syllabus += f"### {assignment_type}s\n\n"
        for assignment in sorted(assignments_list, key=lambda x: ensure_datetime(x.get("due_date", semester_start))):
            name = assignment.get("name", "")
            due_date = assignment.get("due_date")
            weight = assignment.get("weight", 0)
            
            syllabus += f"- **{name}** ({weight}%)"
            if due_date:
                due_date_dt = ensure_datetime(due_date)
                syllabus += f" - Due: {due_date_dt.strftime('%A, %B %d')}"
            syllabus += "\n"
    
    # Add grading section
    syllabus += "\n## Grading\n\n"
    
    # Calculate total weight by type
    type_weights = {}
    for assignment in schedule["assignments"]:
        assignment_type = assignment.get("type", "Other")
        weight = assignment.get("weight", 0)
        type_weights[assignment_type] = type_weights.get(assignment_type, 0) + weight
    
    # Add weight distribution
    syllabus += "| Assignment Type | Percentage of Final Grade |\n"
    syllabus += "|----------------|---------------------------|\n"
    for assignment_type, weight in type_weights.items():
        syllabus += f"| {assignment_type}s | {weight}% |\n"
    
    # Add standard policies
    syllabus += """
## Course Policies

### Attendance
Regular attendance is expected and will contribute to your learning experience and success in this course.

### Late Assignments
Late assignments will be penalized at 10% per day late, up to a maximum of 3 days. After 3 days, assignments will not be accepted without prior arrangement.

### Academic Integrity
Academic integrity is fundamental to the activities and principles of a university. All members of the academic community must be confident that each person's work has been responsibly and honorably acquired, developed, and presented. Any effort to gain an advantage not given to all students is dishonest whether or not the effort is successful.
"""
    
    return syllabus

def generate_syllabus_docx(schedule, course_metadata, semester_start, semester_end):
    """Generate a downloadable DOCX version of the optimized syllabus"""
    # Ensure datetime objects for calculation
    semester_start_dt = ensure_datetime(semester_start)
    semester_end_dt = ensure_datetime(semester_end)
    
    # Create a new document
    doc = docx.Document()
    
    # Add title
    course_code = course_metadata.get("course_code", "")
    course_name = course_metadata.get("course_name", "")
    doc.add_heading(f"{course_code}: {course_name}", 0)
    
    # Add course info
    doc.add_heading(f"{semester_start_dt.strftime('%B %Y')} to {semester_end_dt.strftime('%B %Y')}", 1)
    doc.add_paragraph(f"Credit Hours: {course_metadata.get('credit_hours', 3)}")
    
    # Add course description
    doc.add_heading("Course Description", 1)
    doc.add_paragraph(f"This is an automatically optimized syllabus for {course_code}: {course_name}.")
    
    # Add learning objectives
    doc.add_heading("Learning Objectives", 1)
    objectives = doc.add_paragraph()
    objectives.add_run("By the end of this course, students will be able to:").bold = True
    objectives_list = doc.add_paragraph(style='List Bullet')
    objectives_list.add_run(f"Understand key concepts in {course_name}")
    objectives_list = doc.add_paragraph(style='List Bullet')
    objectives_list.add_run("Apply theoretical knowledge to practical problems")
    objectives_list = doc.add_paragraph(style='List Bullet')
    objectives_list.add_run("Analyze and evaluate approaches in the field")
    
    # Add course schedule
    doc.add_heading("Course Schedule", 1)
    
    current_week = 0
    for session in schedule["topics"]:
        week = session["week"]
        session_date = ensure_datetime(session["date"])
        
        if week != current_week:
            current_week = week
            end_date = session_date + timedelta(days=6)
            doc.add_heading(f"Week {week}: {session_date.strftime('%B %d')} - {end_date.strftime('%B %d')}", 2)
        
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{session_date.strftime('%A, %B %d')}: ").bold = True
        p.add_run(f"{', '.join(session['topics'])}")
    
    # Add assignments section
    doc.add_heading("Assignments", 1)
    
    # Group assignments by type
    assignment_types = {}
    for assignment in schedule["assignments"]:
        assignment_type = assignment.get("type", "Other")
        if assignment_type not in assignment_types:
            assignment_types[assignment_type] = []
        assignment_types[assignment_type].append(assignment)
    
    # Add each type of assignment
    for assignment_type, assignments_list in assignment_types.items():
        doc.add_heading(f"{assignment_type}s", 2)
        for assignment in sorted(assignments_list, key=lambda x: ensure_datetime(x.get("due_date", semester_start))):
            name = assignment.get("name", "")
            due_date = assignment.get("due_date")
            weight = assignment.get("weight", 0)
            
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(f"{name} ({weight}%)").bold = True
            if due_date:
                due_date_dt = ensure_datetime(due_date)
                p.add_run(f" - Due: {due_date_dt.strftime('%A, %B %d')}")
    
    # Add grading section
    doc.add_heading("Grading", 1)
    
    # Calculate total weight by type
    type_weights = {}
    for assignment in schedule["assignments"]:
        assignment_type = assignment.get("type", "Other")
        weight = assignment.get("weight", 0)
        type_weights[assignment_type] = type_weights.get(assignment_type, 0) + weight
    
    # Add weight distribution table
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    
    # Add header row
    header_cells = table.rows[0].cells
    header_cells[0].text = "Assignment Type"
    header_cells[1].text = "Percentage of Final Grade"
    
    # Add data rows
    for assignment_type, weight in type_weights.items():
        row_cells = table.add_row().cells
        row_cells[0].text = f"{assignment_type}s"
        row_cells[1].text = f"{weight}%"
    
    # Add standard policies
    doc.add_heading("Course Policies", 1)
    
    doc.add_heading("Attendance", 2)
    doc.add_paragraph("Regular attendance is expected and will contribute to your learning experience and success in this course.")
    
    doc.add_heading("Late Assignments", 2)
    doc.add_paragraph("Late assignments will be penalized at 10% per day late, up to a maximum of 3 days. After 3 days, assignments will not be accepted without prior arrangement.")
    
    doc.add_heading("Academic Integrity", 2)
    doc.add_paragraph("Academic integrity is fundamental to the activities and principles of a university. All members of the academic community must be confident that each person's work has been responsibly and honorably acquired, developed, and presented. Any effort to gain an advantage not given to all students is dishonest whether or not the effort is successful.")
    
    # Save to a BytesIO object
    docx_buffer = BytesIO()
    doc.save(docx_buffer)
    docx_buffer.seek(0)
    
    return docx_buffer

# Add function to main.py to integrate this functionality
def integrate_syllabus_optimization_with_app():
    """Integrate syllabus optimization functionality with the main app"""
    display_syllabus_optimization()

# Execute the main function if this file is run directly
if __name__ == "__main__":
    # Set up page config
    st.set_page_config(
        page_title="Syllabus Optimization Engine",
        page_icon="🗓️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Run the app
    display_syllabus_optimization()
