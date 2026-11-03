import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime, timedelta

# Function to integrate CMS with the main app
def integrate_cms_with_app():
    """Integrate enhanced content management system with the application"""
    st.title("📚 Enhanced Content Management System")
    
    # Create tabs for different sections
    tabs = st.tabs(["Exam Preparation", "Personal Content Management"])
    
    # Section 1: Exam Preparation Portal
    with tabs[0]:
        st.header("🎓 Exam Preparation Portal")
        
        # Select exam category
        exam_category = st.selectbox(
            "Select Exam Category",
            ["Engineering Entrance", "Medical Entrance", "Civil Services", "Management Entrance", 
             "Research & Higher Education", "Banking & Insurance", "Defense Services", "State Services", "Other"]
        )
        
        # Show specific exams based on category
        if exam_category == "Engineering Entrance":
            exam_options = ["JEE Main", "JEE Advanced", "GATE", "BITSAT", "VITEEE", "MET", "SRMJEEE", "COMEDK", "WBJEE"]
        elif exam_category == "Medical Entrance":
            exam_options = ["NEET UG", "NEET PG", "AIIMS", "JIPMER", "PGIMER", "INI CET", "AIAPGET"]
        elif exam_category == "Civil Services":
            exam_options = ["UPSC CSE", "UPSC ESE", "UPSC CDS", "UPSC NDA", "UPSC CAPF"]
        elif exam_category == "Management Entrance":
            exam_options = ["CAT", "XAT", "SNAP", "NMAT", "MAT", "CMAT", "GMAT", "IIFT"]
        elif exam_category == "Research & Higher Education":
            exam_options = ["UGC NET", "CSIR NET", "JEST", "TIFR", "NBHM", "JGEEBILS"]
        elif exam_category == "Banking & Insurance":
            exam_options = ["SBI PO", "IBPS PO", "RBI Grade B", "NABARD", "LIC AAO", "SEBI Grade A"]
        elif exam_category == "Defense Services":
            exam_options = ["NDA", "CDS", "AFCAT", "Indian Navy B.Tech", "Indian Army Technical Entry"]
        elif exam_category == "State Services":
            exam_options = ["State PSC", "State Engineering Services", "State Teacher Eligibility", "State Police Services"]
        else:
            exam_options = ["Other"]
        
        # Select specific exam
        exam_type = st.selectbox("Select Specific Exam", exam_options)
        
        # Get exam details and display appropriate content
        stream_or_subject = None
        
        # Handle specific exam configurations
        if exam_type == "GATE":
            stream_or_subject = st.selectbox(
                "Select GATE Stream",
                ["Computer Science (CS)", "Electronics & Communication (EC)", 
                 "Electrical Engineering (EE)", "Mechanical Engineering (ME)",
                 "Civil Engineering (CE)", "Chemical Engineering (CH)",
                 "Instrumentation Engineering (IN)", "Biotechnology (BT)"]
            )
        elif exam_type in ["JEE Main", "JEE Advanced"]:
            stream_or_subject = st.selectbox(
                "Select Subject",
                ["Physics", "Chemistry", "Mathematics", "All Subjects"]
            )
        elif exam_type in ["NEET UG", "AIIMS"]:
            stream_or_subject = st.selectbox(
                "Select Subject",
                ["Physics", "Chemistry", "Biology", "All Subjects"]
            )
        elif exam_type in ["CAT", "XAT", "SNAP"]:
            stream_or_subject = st.selectbox(
                "Select Section",
                ["Quantitative Ability", "Verbal Ability", "Data Interpretation", "Logical Reasoning", "All Sections"]
            )
        elif exam_type in ["UPSC CSE"]:
            stream_or_subject = st.selectbox(
                "Select Phase/Subject",
                ["Prelims - GS", "Prelims - CSAT", "Mains - GS", "Mains - Optional", "Interview Preparation"]
            )
            if stream_or_subject == "Mains - Optional":
                stream_or_subject = st.selectbox(
                    "Select Optional Subject",
                    ["History", "Geography", "Political Science", "Public Administration", 
                     "Sociology", "Philosophy", "Psychology", "Economics", "Mathematics", "Physics", "Others"]
                )
        elif exam_type in ["UGC NET", "CSIR NET"]:
            stream_or_subject = st.selectbox(
                "Select Subject",
                ["Computer Science", "Economics", "English", "Life Sciences", "Physical Sciences", 
                 "Mathematical Sciences", "Chemical Sciences", "Commerce", "Others"]
            )
        
        # Display exam content organization
        if exam_type:
            title_text = f"{exam_type}"
            if stream_or_subject:
                title_text += f" - {stream_or_subject}"
            
            st.subheader(f"{title_text} Preparation Resources")
            
            # Create expandable sections for different resource types
            with st.expander("📋 Syllabus", expanded=True):
                display_exam_syllabus(exam_type, stream_or_subject)
            
            with st.expander("📚 Study Materials"):
                display_exam_study_materials(exam_type, stream_or_subject)
            
            with st.expander("📝 Previous Year Question Papers"):
                display_exam_previous_papers(exam_type, stream_or_subject)
                
            with st.expander("📊 Topic-wise Weightage Analysis"):
                display_exam_topic_weightage(exam_type, stream_or_subject)
                
            with st.expander("🎯 Mock Tests"):
                display_exam_mock_tests(exam_type, stream_or_subject)
                
            with st.expander("📝 Personalized Study Plan"):
                generate_personalized_study_plan(exam_type, stream_or_subject)
                
            with st.expander("👥 Find Study Partners"):
                find_study_partners(exam_type, stream_or_subject)
                
            with st.expander("🧠 AI-Powered Doubt Solving"):
                solve_doubts_with_ai(exam_type, stream_or_subject)
    
    # Section 2: Personal Content Management
    with tabs[1]:
        st.header("📁 Personal Content Management")
        
        # Create sidebar for navigation within this section
        content_category = st.selectbox(
            "Select Content Category",
            ["My Courses", "Notes", "Videos", "Books & PDFs", "Flashcards", "My Progress"]
        )
        
        if content_category == "My Courses":
            display_personal_courses()
        
        elif content_category == "Notes":
            manage_personal_notes()
            
        elif content_category == "Videos":
            manage_personal_videos()
            
        elif content_category == "Books & PDFs":
            manage_personal_books()
            
        elif content_category == "Flashcards":
            manage_personal_flashcards()
            
        elif content_category == "My Progress":
            display_personal_progress()

# AI content generation function (placeholder to work with existing API in assessment5.py)
def ai_generate_content(prompt, max_tokens=500, temperature=0.7):
    """Generate content using OpenAI API"""
    try:
        import openai
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert educational assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback to placeholder text if API call fails
        return f"AI-generated content based on: {prompt[:50]}...\n\nThis is placeholder content. In a production environment, this would use the OpenAI API to generate a response based on your prompt."

# -------------------- General Exam Preparation Functions --------------------

def display_exam_syllabus(exam_type, stream_or_subject):
    """Display syllabus for selected exam and stream/subject"""
    
    # GATE Syllabus
    if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
        st.markdown("""
        ### GATE Computer Science Engineering Syllabus
        
        #### Section 1: Engineering Mathematics
        - Discrete Mathematics
        - Linear Algebra
        - Calculus
        - Probability
        
        #### Section 2: Digital Logic
        - Boolean algebra
        - Combinational and sequential circuits
        - Minimization
        
        #### Section 3: Computer Organization and Architecture
        - Machine instructions and addressing modes
        - ALU, data‐path and control unit
        - Memory hierarchy
        
        #### Section 4: Programming and Data Structures
        - Programming in C
        - Recursion
        - Arrays, stacks, queues, linked lists, trees, binary search trees, graphs
        
        #### Section 5: Algorithms
        - Searching, sorting, hashing
        - Asymptotic analysis (best, worst, average cases)
        - Algorithm design techniques
        
        #### Section 6: Theory of Computation
        - Regular languages and finite automata
        - Context-free languages and push-down automata
        - Turing machines and undecidability
        
        #### Section 7: Compiler Design
        - Lexical analysis, parsing, syntax-directed translation
        - Runtime environments
        
        #### Section 8: Operating System
        - Processes, threads, inter‐process communication, concurrency
        - CPU scheduling, memory management, file systems
        
        #### Section 9: Databases
        - ER‐model, relational model
        - Transaction management, concurrency control
        
        #### Section 10: Computer Networks
        - ISO/OSI stack, LAN technologies
        - Flow and error control techniques, routing algorithms
        """)
    
    # JEE Main/Advanced Syllabus
    elif exam_type in ["JEE Main", "JEE Advanced"]:
        if stream_or_subject == "Physics":
            st.markdown("""
            ### JEE Physics Syllabus
            
            #### Class 11
            - Physical world and measurement
            - Kinematics
            - Laws of Motion
            - Work, Energy and Power
            - Motion of System of Particles and Rigid Body
            - Gravitation
            - Properties of Bulk Matter
            - Thermodynamics
            - Behaviour of Perfect Gas and Kinetic Theory
            - Oscillations and Waves
            
            #### Class 12
            - Electrostatics
            - Current Electricity
            - Magnetic Effects of Current and Magnetism
            - Electromagnetic Induction and Alternating Currents
            - Electromagnetic Waves
            - Optics
            - Dual Nature of Matter and Radiation
            - Atoms and Nuclei
            - Electronic Devices
            """)
        elif stream_or_subject == "Chemistry":
            st.markdown("""
            ### JEE Chemistry Syllabus
            
            #### Physical Chemistry
            - Some Basic Concepts of Chemistry
            - States of Matter
            - Atomic Structure
            - Chemical Bonding and Molecular Structure
            - Chemical Thermodynamics
            - Solutions
            - Equilibrium
            - Redox Reactions
            - Electrochemistry
            - Chemical Kinetics
            - Surface Chemistry
            
            #### Organic Chemistry
            - Purification and Characterisation of Organic Compounds
            - Some Basic Principles of Organic Chemistry
            - Hydrocarbons
            - Organic Compounds Containing Halogens
            - Organic Compounds Containing Oxygen
            - Organic Compounds Containing Nitrogen
            - Polymers
            - Biomolecules
            - Chemistry in Everyday Life
            
            #### Inorganic Chemistry
            - Classification of Elements and Periodicity in Properties
            - General Principles and Processes of Isolation of Elements
            - Hydrogen
            - s-Block Elements
            - p-Block Elements
            - d and f Block Elements
            - Coordination Compounds
            - Environmental Chemistry
            """)
        elif stream_or_subject == "Mathematics":
            st.markdown("""
            ### JEE Mathematics Syllabus
            
            #### Algebra
            - Complex Numbers and Quadratic Equations
            - Matrices and Determinants
            - Sets, Relations and Functions
            - Mathematical Induction
            - Permutations and Combinations
            - Binomial Theorem and its Applications
            - Sequences and Series
            
            #### Trigonometry
            - Trigonometric Functions
            - Trigonometric Equations
            - Inverse Trigonometric Functions
            - Heights and Distances
            
            #### Analytical Geometry
            - Cartesian System of Rectangular Coordinates
            - Straight Lines
            - Circles
            - Conic Sections
            
            #### Differential Calculus
            - Limits and Continuity
            - Differentiation
            - Applications of Derivatives
            
            #### Integral Calculus
            - Integration
            - Definite Integrals
            - Applications of the Integrals
            - Differential Equations
            
            #### Vectors and 3-D Geometry
            - Vectors
            - Three-dimensional Geometry
            
            #### Statistics and Probability
            - Statistics
            - Probability
            """)
    
    # UPSC CSE Syllabus
    elif exam_type == "UPSC CSE":
        if stream_or_subject == "Prelims - GS":
            st.markdown("""
            ### UPSC CSE Prelims - General Studies Syllabus
            
            #### Current Affairs
            - Current events of national and international importance
            
            #### History of India
            - Indian culture will cover the salient aspects of Art Forms, literature and Architecture from ancient to modern times
            - Modern Indian history from about the middle of the eighteenth century until the present
            - The Freedom Struggle - its various stages and important contributors/contributions from different parts of the country
            
            #### Geography
            - Physical, Social, Economic geography of India and the World
            
            #### Indian Polity and Governance
            - Constitution, Political System, Panchayati Raj, Public Policy, Rights Issues, etc
            
            #### Economic and Social Development
            - Sustainable Development, Poverty, Inclusion, Demographics, Social Sector Initiatives, etc
            
            #### General Science
            - General issues on Environmental ecology, Bio-diversity and Climate Change
            """)
        elif stream_or_subject == "Prelims - CSAT":
            st.markdown("""
            ### UPSC CSE Prelims - CSAT Syllabus
            
            #### Comprehension
            - Interpersonal skills including communication skills
            - Logical reasoning and analytical ability
            
            #### Decision Making and Problem Solving
            - General mental ability
            - Basic numeracy (numbers and their relations, orders of magnitude, etc.)
            - Data interpretation (charts, graphs, tables, data sufficiency etc.)
            """)
    
    # NEET UG Syllabus
    elif exam_type == "NEET UG":
        if stream_or_subject == "Biology":
            st.markdown("""
            ### NEET Biology Syllabus
            
            #### Class 11
            - Diversity in Living World
            - Structural Organization in Animals and Plants
            - Cell Structure and Function
            - Plant Physiology
            - Human Physiology
            
            #### Class 12
            - Reproduction
            - Genetics and Evolution
            - Biology and Human Welfare
            - Biotechnology and its Applications
            - Ecology and Environment
            """)
    
    # CAT Syllabus
    elif exam_type == "CAT":
        if stream_or_subject == "Quantitative Ability":
            st.markdown("""
            ### CAT Quantitative Ability Syllabus
            
            #### Arithmetic
            - Number Systems
            - LCM and HCF
            - Percentages
            - Profit, Loss, and Discount
            - Interest (Simple and Compound)
            - Speed, Time, and Distance
            - Time and Work
            - Averages
            - Ratio and Proportion
            - Mixtures and Alligations
            
            #### Algebra
            - Linear Equations
            - Quadratic Equations
            - Inequalities
            - Logarithm
            - Sequences and Series
            - Functions
            - Set Theory
            
            #### Geometry
            - Lines and Angles
            - Triangles
            - Circles
            - Quadrilaterals
            - Coordinate Geometry
            - Mensuration
            
            #### Other Topics
            - Permutation and Combination
            - Probability
            - Trigonometry
            """)
    
    else:
        st.info(f"Syllabus for {exam_type} {stream_or_subject if stream_or_subject else ''} will be available soon.")
        
        # Option to request syllabus via AI
        if st.button("Generate AI Syllabus Overview"):
            with st.spinner(f"Generating syllabus overview for {exam_type}..."):
                ai_syllabus = ai_generate_content(
                    f"Create a detailed syllabus outline for {exam_type} {stream_or_subject if stream_or_subject else ''}. Organize it by main sections and include subsections with key topics."
                )
                st.markdown(ai_syllabus)
                st.download_button(
                    label=f"Download {exam_type} Syllabus",
                    data=ai_syllabus,
                    file_name=f"{exam_type.replace(' ', '_')}_Syllabus.txt"
                )

def display_exam_study_materials(exam_type, stream_or_subject):
    """Display study materials for selected exam and stream/subject"""
    
    st.write(f"### Recommended Study Materials for {exam_type} {stream_or_subject if stream_or_subject else ''}")
    
    # Create a general function for displaying study materials
    def show_study_materials(materials):
        # Convert to DataFrame for better display
        import pandas as pd
        materials_df = pd.DataFrame(materials)
        st.dataframe(materials_df)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_type = st.multiselect("Filter by Type", list(set([m["type"] for m in materials])))
        with col2:
            min_rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0, 0.1)
        
        # Apply filters
        filtered_materials = materials
        if filter_type:
            filtered_materials = [m for m in filtered_materials if m["type"] in filter_type]
        filtered_materials = [m for m in filtered_materials if m["rating"] >= min_rating]
        
        # Display filtered results
        if filtered_materials:
            st.write("### Filtered Results")
            st.dataframe(pd.DataFrame(filtered_materials))
        else:
            st.info("No materials match your filters.")
    
    # Define materials based on exam
    if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
        materials = [
            {"title": "Made Easy Gate CSE Notes", "type": "Notes", "rating": 4.5},
            {"title": "Data Structures and Algorithms by Cormen", "type": "Book", "rating": 4.8},
            {"title": "Operating System Concepts by Galvin", "type": "Book", "rating": 4.7},
            {"title": "Database System Concepts by Korth", "type": "Book", "rating": 4.6},
            {"title": "Computer Networks by Tanenbaum", "type": "Book", "rating": 4.5},
            {"title": "Theory of Computation by Ullman", "type": "Book", "rating": 4.4},
            {"title": "GATE CSE Video Lectures by Ravindrababu Ravula", "type": "Video", "rating": 4.6},
            {"title": "GATE Overflow Question Bank", "type": "Question Bank", "rating": 4.9},
        ]
        show_study_materials(materials)
    
    # JEE Main/Advanced Materials
    elif exam_type in ["JEE Main", "JEE Advanced"]:
        if stream_or_subject == "Physics":
            materials = [
                {"title": "Concepts of Physics by H.C. Verma (Vol 1 & 2)", "type": "Book", "rating": 4.9},
                {"title": "Problems in General Physics by I.E. Irodov", "type": "Book", "rating": 4.7},
                {"title": "Fundamentals of Physics by Halliday, Resnick & Walker", "type": "Book", "rating": 4.8},
                {"title": "Physics for JEE by DC Pandey", "type": "Book", "rating": 4.5},
                {"title": "Physics Formula Handbook", "type": "Notes", "rating": 4.6},
                {"title": "Physics Video Lectures by Etoos", "type": "Video", "rating": 4.7},
                {"title": "Physics Solved Problems Workbook", "type": "Practice Book", "rating": 4.4}
            ]
            show_study_materials(materials)
        elif stream_or_subject == "Chemistry":
            materials = [
                {"title": "NCERT Chemistry Textbooks (Class 11 & 12)", "type": "Book", "rating": 4.7},
                {"title": "Organic Chemistry by Morrison & Boyd", "type": "Book", "rating": 4.8},
                {"title": "Modern Approach to Chemical Calculations by R.C. Mukherjee", "type": "Book", "rating": 4.9},
                {"title": "Concise Inorganic Chemistry by J.D. Lee", "type": "Book", "rating": 4.6},
                {"title": "Chemistry Formula & Reaction Handbook", "type": "Notes", "rating": 4.5},
                {"title": "Chemistry Video Lectures by Vedantu", "type": "Video", "rating": 4.4},
                {"title": "Chemistry Master Problem Package", "type": "Practice Book", "rating": 4.3}
            ]
            show_study_materials(materials)
    
    # UPSC CSE Materials
    elif exam_type == "UPSC CSE":
        materials = [
            {"title": "Indian Polity by M. Laxmikanth", "type": "Book", "rating": 4.8},
            {"title": "Indian Economy by Ramesh Singh", "type": "Book", "rating": 4.6},
            {"title": "India's Ancient Past by R.S. Sharma", "type": "Book", "rating": 4.7},
            {"title": "Certificate Physical and Human Geography by G C Leong", "type": "Book", "rating": 4.5},
            {"title": "Ethics, Integrity & Aptitude by G Subba Rao & P N Roy Chowdhury", "type": "Book", "rating": 4.4},
            {"title": "UPSC Syllabus-wise Compiled Current Affairs", "type": "Notes", "rating": 4.9},
            {"title": "UPSC Complete Video Lecture Series by Unacademy", "type": "Video", "rating": 4.7},
            {"title": "Vision IAS Mains Test Series", "type": "Practice Tests", "rating": 4.8}
        ]
        show_study_materials(materials)
    
    # NEET UG Materials
    elif exam_type == "NEET UG":
        if stream_or_subject == "Biology":
            materials = [
                {"title": "NCERT Biology (Class 11 & 12)", "type": "Book", "rating": 4.9},
                {"title": "Trueman's Biology (Vol 1 & 2)", "type": "Book", "rating": 4.7},
                {"title": "Objective Biology by Dinesh", "type": "Book", "rating": 4.6},
                {"title": "MTG NEET Guide Biology", "type": "Guide", "rating": 4.8},
                {"title": "Biology Video Lectures by Allen", "type": "Video", "rating": 4.7},
                {"title": "Biology Diagrams & Illustrations Handbook", "type": "Notes", "rating": 4.5},
                {"title": "30 Days Biology Crash Course", "type": "Course", "rating": 4.4}
            ]
            show_study_materials(materials)
    
    # CAT Materials
    elif exam_type == "CAT":
        materials = [
            {"title": "How to Prepare for Quantitative Aptitude for CAT by Arun Sharma", "type": "Book", "rating": 4.8},
            {"title": "Logical Reasoning and Data Interpretation for CAT by Nishit Sinha", "type": "Book", "rating": 4.7},
            {"title": "Verbal Ability and Reading Comprehension for CAT by Arun Sharma", "type": "Book", "rating": 4.6},
            {"title": "Time MBA CAT Prep Material", "type": "Notes", "rating": 4.5},
            {"title": "IMS CAT Complete Course", "type": "Course", "rating": 4.7},
            {"title": "CAT Previous Year Papers Compilation", "type": "Question Bank", "rating": 4.9},
            {"title": "MBA Guru CAT Mock Tests", "type": "Practice Tests", "rating": 4.8}
        ]
        show_study_materials(materials)
    
    else:
        st.info(f"Study materials for {exam_type} {stream_or_subject if stream_or_subject else ''} are being updated.")
        
        # AI-generated study guide option
        if st.button("Generate AI Study Guide"):
            if not stream_or_subject:
                stream_or_subject = st.text_input("Enter specific subject/topic:")
                
            if stream_or_subject:
                with st.spinner(f"Generating AI study guide for {exam_type} - {stream_or_subject}..."):
                    study_guide = ai_generate_content(
                        f"Create a concise study guide for {stream_or_subject} for {exam_type} preparation. Include recommended books, key concepts to focus on, and study strategies."
                    )
                    st.markdown(study_guide)
                    st.download_button(
                        label=f"Download {exam_type} Study Guide",
                        data=study_guide,
                        file_name=f"{exam_type.replace(' ', '_')}_{stream_or_subject.replace(' ', '_')}_Study_Guide.txt"
                    )

def display_exam_previous_papers(exam_type, stream_or_subject):
    """Display previous year papers for selected exam and stream/subject"""
    
    st.write(f"### Previous Year {exam_type} Question Papers")
    
    # Define years based on exam type
    if exam_type in ["GATE", "JEE Main", "JEE Advanced", "NEET UG", "CAT", "UPSC CSE"]:
        years = ["2023", "2022", "2021", "2020", "2019"]
    else:
        years = ["2023", "2022", "2021"]
    
    selected_years = st.multiselect("Select years", years, default=years[:3])
    
    if selected_years:
        for year in selected_years:
            # FIX: Using a normal container instead of a nested expander
            st.write(f"#### {exam_type} {year} {stream_or_subject if stream_or_subject else ''}")
            st.write(f"Question Paper and Solutions for {exam_type} {year}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label=f"Download Question Paper ({year})",
                    data=f"Sample content for {exam_type} {year} question paper",
                    file_name=f"{exam_type.replace(' ', '_')}_{year}_Question.pdf"
                )
            with col2:
                st.download_button(
                    label=f"Download Solutions ({year})",
                    data=f"Sample content for {exam_type} {year} solutions",
                    file_name=f"{exam_type.replace(' ', '_')}_{year}_Solutions.pdf"
                )
            
            # Add AI analysis option
            if st.button(f"Get AI Analysis of {year} Paper", key=f"ai_analysis_{year}"):
                with st.spinner(f"Analyzing {exam_type} {year} paper..."):
                    analysis = ai_generate_content(
                        f"Provide a detailed analysis of the {exam_type} {year} paper for {stream_or_subject if stream_or_subject else 'all subjects'}. Include difficulty level, topic distribution, comparison with previous years, and key insights for future aspirants."
                    )
                    st.markdown(analysis)
            
            # Add a divider between years
            st.markdown("---")
    else:
        st.info("Please select at least one year to view question papers.")
        
    # Generate topic-wise papers
    st.subheader("Topic-wise Question Papers")
    
    # Define topics based on exam and stream
    if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
        topics = ["Digital Logic", "Computer Organization", "Programming & DS", 
                "Algorithms", "Theory of Computation", "Compiler Design",
                "Operating Systems", "Databases", "Computer Networks"]
    elif exam_type in ["JEE Main", "JEE Advanced"] and stream_or_subject == "Physics":
        topics = ["Mechanics", "Thermodynamics", "Electrostatics", "Magnetism", 
                "Optics", "Modern Physics", "Waves", "Fluid Mechanics"]
    elif exam_type == "UPSC CSE":
        topics = ["Indian Polity", "Geography", "Economy", "History", 
                "International Relations", "Environment", "Science & Technology"]
    else:
        topics = ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
    
    selected_topic = st.selectbox("Select Topic for Focused Practice", topics)
    
    if st.button(f"Generate {selected_topic} Questions"):
        with st.spinner(f"Generating {selected_topic} questions for {exam_type}..."):
            topic_questions = ai_generate_content(
                f"Create 5 previous year style questions on {selected_topic} for {exam_type} {stream_or_subject if stream_or_subject else ''}. For each question, provide the question, options if applicable, and detailed solution."
            )
            st.markdown(topic_questions)
            st.download_button(
                label=f"Download {selected_topic} Questions",
                data=topic_questions,
                file_name=f"{exam_type.replace(' ', '_')}_{selected_topic.replace(' ', '_')}_Questions.txt"
            )

def display_exam_topic_weightage(exam_type, stream_or_subject):
    """Display topic-wise weightage analysis for exams"""
    
    st.write(f"### Topic-wise Weightage Analysis for {exam_type} {stream_or_subject if stream_or_subject else ''}")
    
    # Define topics and weightages based on exam type
    topics = []
    weightages = []
    
    if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
        topics = ["Engineering Mathematics", "Digital Logic", "Computer Organization", 
                "Programming & DS", "Algorithms", "Theory of Computation", 
                "Compiler Design", "Operating Systems","Compiler Design", "Operating Systems", "Databases", "Computer Networks"]
        weightages = [12, 8, 10, 15, 10, 8, 7, 10, 10, 10]
    
    elif exam_type in ["JEE Main", "JEE Advanced"]:
        if stream_or_subject == "Physics":
            topics = ["Mechanics", "Thermodynamics", "Electrostatics", "Current Electricity", 
                    "Magnetism", "Optics", "Modern Physics", "Waves", "SHM & Elasticity"]
            weightages = [20, 12, 15, 10, 12, 10, 8, 8, 5]
        elif stream_or_subject == "Chemistry":
            topics = ["Physical Chemistry", "Organic Chemistry", "Inorganic Chemistry"]
            weightages = [40, 30, 30]
        elif stream_or_subject == "Mathematics":
            topics = ["Calculus", "Algebra", "Coordinate Geometry", "Vectors & 3D", 
                    "Trigonometry", "Probability & Statistics"]
            weightages = [25, 30, 20, 10, 10, 5]
    
    elif exam_type == "UPSC CSE" and stream_or_subject == "Prelims - GS":
        topics = ["History", "Geography", "Polity", "Economy", "Environment", 
                "Science & Tech", "Current Affairs", "Art & Culture"]
        weightages = [15, 15, 20, 15, 10, 10, 10, 5]
    
    elif exam_type == "NEET UG" and stream_or_subject == "Biology":
        topics = ["Human Physiology", "Plant Physiology", "Genetics", "Cell Biology", 
                "Ecology", "Biotechnology", "Zoology", "Botany", "Evolution"]
        weightages = [20, 15, 15, 10, 10, 5, 15, 5, 5]
    
    elif exam_type == "CAT":
        topics = ["Quantitative Ability", "Verbal Ability", "Data Interpretation", "Logical Reasoning"]
        weightages = [35, 25, 20, 20]
    
    else:
        # Generate random data for demonstration
        topics = [f"Topic {i+1}" for i in range(8)]
        weightages = [random.randint(5, 25) for _ in range(8)]
        # Normalize to 100%
        total = sum(weightages)
        weightages = [int(w * 100 / total) for w in weightages]
    
    # Visualize weightage distribution
    import matplotlib.pyplot as plt
    import numpy as np
    
    if topics and weightages:
        # Horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        y_pos = np.arange(len(topics))
        ax.barh(y_pos, weightages)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(topics)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Weightage (%)')
        ax.set_title(f'{exam_type} Topic Weightage')
        
        # Add percentage labels to each bar
        for i, v in enumerate(weightages):
            ax.text(v + 0.5, i, str(v) + "%", color='blue', va='center')
            
        plt.tight_layout()
        st.pyplot(fig)
        
        # Pie chart
        fig2, ax2 = plt.subplots(figsize=(10, 10))
        ax2.pie(weightages, labels=topics, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(f'{exam_type} Topic Distribution')
        st.pyplot(fig2)
        
        # Topic prioritization
        st.subheader("Topic Prioritization Strategy")
        st.write("Based on weightage analysis, here's how you should prioritize your preparation:")
        
        for topic, weight in sorted(zip(topics, weightages), key=lambda x: x[1], reverse=True):
            importance = "High" if weight > 15 else "Medium" if weight > 8 else "Low"
            if importance == "High":
                st.markdown(f"**{topic}**: {weight}% - ⭐⭐⭐ {importance} Priority")
            elif importance == "Medium":
                st.markdown(f"**{topic}**: {weight}% - ⭐⭐ {importance} Priority")
            else:
                st.markdown(f"**{topic}**: {weight}% - ⭐ {importance} Priority")
    else:
        st.info(f"Weightage analysis for {exam_type} {stream_or_subject if stream_or_subject else ''} is being updated.")
        
        if st.button("Generate AI Weightage Analysis"):
            with st.spinner(f"Generating analysis for {exam_type}..."):
                analysis = ai_generate_content(
                    f"Provide a detailed topic-wise weightage analysis for {exam_type} {stream_or_subject if stream_or_subject else ''}. Include percentage weightage of each topic based on past trends, topics that should be prioritized, and preparation strategy based on this analysis."
                )
                st.markdown(analysis)

def display_exam_mock_tests(exam_type, stream_or_subject):
    """Display mock tests for the selected exam"""
    
    st.write(f"### {exam_type} Mock Tests {stream_or_subject if stream_or_subject else ''}")
    
    # Mock test configuration
    test_types = []
    
    if exam_type in ["GATE", "JEE Advanced", "NEET UG", "UPSC CSE"]:
        test_types = [
            {"name": "Full-length Mock Test 1", "duration": "3 hours", "questions": 100, "marks": 100},
            {"name": "Full-length Mock Test 2", "duration": "3 hours", "questions": 100, "marks": 100},
            {"name": "Subject-wise Test", "duration": "1 hour", "questions": 30, "marks": 30},
            {"name": "Topic-wise Test", "duration": "30 minutes", "questions": 15, "marks": 15},
            {"name": "Previous Year Paper Simulation", "duration": "3 hours", "questions": 100, "marks": 100}
        ]
    elif exam_type in ["JEE Main", "CAT"]:
        test_types = [
            {"name": "Full-length Mock Test 1", "duration": "3 hours", "questions": 90, "marks": 300},
            {"name": "Full-length Mock Test 2", "duration": "3 hours", "questions": 90, "marks": 300},
            {"name": "Physics Sectional Test", "duration": "1 hour", "questions": 30, "marks": 100},
            {"name": "Chemistry Sectional Test", "duration": "1 hour", "questions": 30, "marks": 100},
            {"name": "Mathematics Sectional Test", "duration": "1 hour", "questions": 30, "marks": 100}
        ]
    else:
        test_types = [
            {"name": "Full Mock Test", "duration": "2 hours", "questions": 50, "marks": 100},
            {"name": "Sectional Test", "duration": "1 hour", "questions": 25, "marks": 50},
            {"name": "Speed Test", "duration": "30 minutes", "questions": 15, "marks": 30}
        ]
    
    # Display mock test options
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_test_type = st.selectbox(
            "Select Test Type",
            [test["name"] for test in test_types]
        )
    
    with col2:
        # Find selected test details
        selected_test = next((test for test in test_types if test["name"] == selected_test_type), None)
        if selected_test:
            st.write(f"Duration: {selected_test['duration']}")
            st.write(f"Questions: {selected_test['questions']}")
            st.write(f"Marks: {selected_test['marks']}")
    
    # Display test start button
    if st.button("Start Test"):
        st.success(f"Starting {selected_test_type} for {exam_type} {stream_or_subject if stream_or_subject else ''}...")
        st.info("This is a placeholder. In the actual implementation, this would launch the test interface.")
    
    # Custom test creation option
    st.subheader("Create Custom Test")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        custom_duration = st.slider("Duration (minutes)", 15, 180, 60, 15)
    with col2:
        custom_questions = st.slider("Number of Questions", 5, 100, 20, 5)
    with col3:
        difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard", "Mixed"])
    
    # Topic selection for custom test
    if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
        topics = ["Digital Logic", "Computer Organization", "Programming & DS", 
                "Algorithms", "Theory of Computation", "Operating Systems", "Databases", "Computer Networks"]
    elif exam_type in ["JEE Main", "JEE Advanced"]:
        topics = ["Mechanics", "Thermodynamics", "Electromagnetism", "Optics", "Modern Physics"]
    else:
        topics = ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
    
    selected_topics = st.multiselect("Select Topics", topics, default=topics[:2])
    
    if st.button("Create & Start Custom Test"):
        if selected_topics:
            st.success(f"Creating custom {difficulty} test with {custom_questions} questions on {', '.join(selected_topics)} for {custom_duration} minutes...")
            st.info("This is a placeholder. In the actual implementation, this would generate and launch a custom test.")
        else:
            st.warning("Please select at least one topic for your custom test.")
    
    # Test performance analytics
    st.subheader("Your Test Performance Analytics")
    
    # Sample data for demonstration
    import pandas as pd
    
    # Sample test results for demonstration
    if "mock_test_results" not in st.session_state:
        st.session_state.mock_test_results = [
            {"date": "2023-10-15", "test_name": "Full Mock Test 1", "score": 65, "total": 100, "percentile": 78},
            {"date": "2023-10-22", "test_name": "Sectional Test", "score": 42, "total": 50, "percentile": 82},
            {"date": "2023-10-29", "test_name": "Full Mock Test 2", "score": 72, "total": 100, "percentile": 85},
            {"date": "2023-11-05", "test_name": "Speed Test", "score": 24, "total": 30, "percentile": 90},
            {"date": "2023-11-12", "test_name": "Full Mock Test 3", "score": 78, "total": 100, "percentile": 88}
        ]
    
    results_df = pd.DataFrame(st.session_state.mock_test_results)
    
    if not results_df.empty:
        # Convert to datetime for plotting
        results_df['date'] = pd.to_datetime(results_df['date'])
        results_df['percentage'] = (results_df['score'] / results_df['total'] * 100).round(1)
        
        # Display results table
        st.dataframe(results_df[['date', 'test_name', 'score', 'total', 'percentage', 'percentile']])
        
        # Plot performance trend
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # Score percentage trend
        ax1.plot(results_df['date'], results_df['percentage'], marker='o', linestyle='-', linewidth=2)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Score (%)')
        ax1.set_title('Mock Test Score Trend')
        ax1.grid(True)
        
        # Percentile trend
        ax2.plot(results_df['date'], results_df['percentile'], marker='s', linestyle='-', color='orange', linewidth=2)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Percentile')
        ax2.set_title('Percentile Trend')
        ax2.grid(True)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Performance insights
        st.subheader("Performance Insights")
        
        # Calculate metrics
        avg_score = results_df['percentage'].mean()
        max_score = results_df['percentage'].max()
        trend = results_df['percentage'].iloc[-1] - results_df['percentage'].iloc[0]
        
        # Display metrics and insights
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col2:
            st.metric("Highest Score", f"{max_score:.1f}%")
        with col3:
            st.metric("Score Trend", f"{trend:+.1f}%", delta_color="normal" if trend >= 0 else "inverse")
        
        # AI-generated insights
        if st.button("Generate Performance Analysis"):
            with st.spinner("Analyzing your test performance..."):
                results_text = "\n".join([
                    f"Test: {row['test_name']}, Date: {row['date']}, Score: {row['score']}/{row['total']} ({row['percentage']}%), Percentile: {row['percentile']}"
                    for _, row in results_df.iterrows()
                ])
                
                insights = ai_generate_content(
                    f"""Analyze the following test results for {exam_type} preparation and provide insights, strengths, weaknesses, and recommendations for improvement:
                    
                    {results_text}
                    
                    Provide specific, actionable advice on how to improve scores. Be encouraging but realistic."""
                )
                st.markdown(insights)
    else:
        st.info("No test results available yet. Take a mock test to see your performance analytics.")

def generate_personalized_study_plan(exam_type, stream_or_subject):
    """Generate personalized study plan based on user input"""
    
    st.write(f"### Generate Your Personalized {exam_type} Study Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exam_date = st.date_input("When is your exam date?")
        study_hours_per_day = st.slider("How many hours can you study per day?", 1, 12, 4)
        
    with col2:
        current_preparation = st.selectbox(
            "What is your current preparation level?",
            ["Just starting", "Completed basics", "Midway through syllabus", "Advanced preparation"]
        )
        
        # Define strong subjects based on exam type
        if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
            subject_options = ["Engineering Mathematics", "Digital Logic", "Computer Organization", 
                             "Programming & DS", "Algorithms", "Theory of Computation", 
                             "Compiler Design", "Operating Systems", "Databases", "Computer Networks"]
        elif exam_type in ["JEE Main", "JEE Advanced"]:
            subject_options = ["Physics Mechanics", "Physics Electromagnetism", "Physics Optics", 
                             "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry",
                             "Algebra", "Calculus", "Coordinate Geometry", "Trigonometry"]
        elif exam_type == "UPSC CSE":
            subject_options = ["History", "Geography", "Polity", "Economy", 
                             "International Relations", "Environment", "Science & Technology"]
        else:
            subject_options = ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"]
        
        strong_subjects = st.multiselect(
            "Select your stronger subjects/topics",
            subject_options
        )
    
    # Additional preferences
    st.subheader("Additional Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        preferred_time = st.multiselect(
            "When do you prefer to study?",
            ["Early morning (4-8 AM)", "Morning (8-12 PM)", "Afternoon (12-4 PM)", 
             "Evening (4-8 PM)", "Night (8-12 AM)", "Late night (12-4 AM)"]
        )
        
        revision_style = st.selectbox(
            "Your preferred revision style",
            ["Daily short revisions", "Weekly in-depth revisions", "Monthly comprehensive revisions", "Mixed approach"]
        )
    
    with col2:
        learning_style = st.multiselect(
            "Your learning style preferences",
            ["Reading textbooks", "Video lectures", "Practice problems", "Group discussions", 
             "Teaching concepts to others", "Flashcards", "Mind maps"]
        )
        
        mock_test_frequency = st.selectbox(
            "Preferred mock test frequency",
            ["Daily", "Twice a week", "Weekly", "Biweekly", "Monthly"]
        )
    
    if st.button("Generate Personalized Study Plan"):
        with st.spinner(f"Generating your personalized {exam_type} study plan..."):
            import datetime
            days_left = (exam_date - datetime.date.today()).days
            
            if days_left > 0:
                total_study_hours = days_left * study_hours_per_day
                
                weak_subjects = [subj for subj in subject_options if subj not in strong_subjects]
                
                study_plan = ai_generate_content(
                    f"""Create a personalized {days_left}-day study plan for {exam_type} {stream_or_subject if stream_or_subject else ''} with the following details:
                    - Exam in {days_left} days
                    - {study_hours_per_day} hours of study per day
                    - Current level: {current_preparation}
                    - Stronger subjects/topics: {', '.join(strong_subjects) if strong_subjects else 'None specified'}
                    - Weaker subjects/topics: {', '.join(weak_subjects) if weak_subjects else 'None specified'}
                    - Preferred study times: {', '.join(preferred_time) if preferred_time else 'Not specified'}
                    - Learning style preferences: {', '.join(learning_style) if learning_style else 'Not specified'}
                    - Revision style: {revision_style}
                    - Mock test frequency: {mock_test_frequency}
                    
                    Create a detailed plan that includes:
                    1. Week-by-week schedule with specific daily objectives
                    2. Topic prioritization based on weightage and personal strengths/weaknesses
                    3. Recommended resources for each topic
                    4. Revision schedule and strategy
                    5. Mock test strategy with specific dates
                    6. Short-term and long-term milestones
                    7. Daily study routine template
                    
                    Make the plan realistic, actionable, and motivating.
                    """
                )
                
                st.markdown(study_plan)
                st.download_button(
                    label="📥 Download Study Plan",
                    data=study_plan,
                    file_name=f"{exam_type.replace(' ', '_')}_Study_Plan.txt"
                )
            else:
                st.error("Please select a future date for your exam.")

def find_study_partners(exam_type, stream_or_subject):
    """Find study partners preparing for the same exam"""
    
    st.write(f"### Find Study Partners for {exam_type}")
    
    # Create profile
    st.subheader("Your Study Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name")
        location = st.text_input("Your City/Town")
        
    with col2:
        prep_level = st.select_slider(
            "Preparation Level",
            options=["Beginner", "Intermediate", "Advanced"]
        )
        
        study_mode = st.multiselect(
            "Preferred Study Mode",
            ["In-person", "Online video calls", "Discussion forum", "Problem-solving sessions"]
        )
    
    # Study schedule & topics
    study_schedule = st.multiselect(
        "Your Study Schedule",
        ["Weekday mornings", "Weekday afternoons", "Weekday evenings", 
         "Weekend mornings", "Weekend afternoons", "Weekend evenings"]
    )
    
    # Topics for collaboration
    if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
        topic_options = ["Algorithms", "Operating Systems", "Databases", "Computer Networks", 
                       "Theory of Computation", "Compiler Design", "Digital Logic"]
    elif exam_type in ["JEE Main", "JEE Advanced"]:
        topic_options = ["Physics Mechanics", "Electromagnetism", "Thermodynamics", 
                       "Organic Chemistry", "Inorganic Chemistry", "Calculus", "Algebra"]
    elif exam_type == "UPSC CSE":
        topic_options = ["Indian Polity", "Economy", "History", "Geography", 
                       "International Relations", "Environment", "Science & Technology"]
    else:
        topic_options = ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
    
    collaboration_topics = st.multiselect(
        "Topics you want to collaborate on",
        topic_options
    )
    
    # Bio
    bio = st.text_area(
        "Brief introduction and what you're looking for in study partners", 
        max_chars=300
    )
    
    # Create or update profile
    if st.button("Update Study Partner Profile"):
        if name and location:
            st.success(f"✅ Profile updated for {name}!")
            st.info("In the actual app, your profile would now be visible to other students preparing for the same exam.")
        else:
            st.warning("Please provide at least your name and location.")
    
    # Find partners
    st.subheader("Find Study Partners")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_location = st.text_input("Filter by location")
    with col2:
        filter_level = st.selectbox(
            "Filter by level",
            ["Any", "Beginner", "Intermediate", "Advanced"]
        )
    with col3:
        filter_mode = st.selectbox(
            "Filter by mode",
            ["Any", "In-person", "Online"]
        )
    
    # Mock data for study partners
    if "study_partners" not in st.session_state:
        st.session_state.study_partners = [
            {
                "name": "Arjun Sharma", 
                "location": "Mumbai", 
                "level": "Intermediate",
                "mode": ["In-person", "Online video calls"],
                "schedule": ["Weekday evenings", "Weekend mornings"],
                "topics": ["Algorithms", "Operating Systems"] if exam_type == "GATE" else ["Physics Mechanics", "Calculus"],
                "bio": "Engineering student preparing for GATE CS. Strong in algorithms, looking to collaborate on OS concepts."
            },
            {
                "name": "Priya Patel", 
                "location": "Delhi", 
                "level": "Advanced",
                "mode": ["Online video calls", "Problem-solving sessions"],
                "schedule": ["Weekday mornings", "Weekend evenings"],
                "topics": ["Databases", "Computer Networks"] if exam_type == "GATE" else ["Organic Chemistry", "Thermodynamics"],
                "bio": "Working professional with 2 years experience. Can help with databases and seeking help with networks."
            },
            {
                "name": "Mohammed Khan", 
                "location": "Bangalore", 
                "level": "Beginner",
                "mode": ["In-person", "Discussion forum"],
                "schedule": ["Weekend afternoons", "Weekend evenings"],
                "topics": ["Digital Logic", "Theory of Computation"] if exam_type == "GATE" else ["Inorganic Chemistry", "Algebra"],
                "bio": "Just started preparation. Looking for study group to understand fundamental concepts better."
            }
        ]
    
    # Filter partners
    filtered_partners = st.session_state.study_partners
    if filter_location:
        filtered_partners = [p for p in filtered_partners if filter_location.lower() in p["location"].lower()]
    if filter_level != "Any":
        filtered_partners = [p for p in filtered_partners if p["level"] == filter_level]
    if filter_mode != "Any":
        filtered_partners = [p for p in filtered_partners if filter_mode in " ".join(p["mode"])]
    
    # Display partners
    if filtered_partners:
        for i, partner in enumerate(filtered_partners):
            # Use a container instead of an expander to display partner info
            st.markdown(f"### 👤 {partner['name']} - {partner['location']} ({partner['level']})")
            
            # Display partner information
            st.write(f"**Bio:** {partner['bio']}")
            st.write(f"**Study Mode:** {', '.join(partner['mode'])}")
            st.write(f"**Schedule:** {', '.join(partner['schedule'])}")
            st.write(f"**Topics:** {', '.join(partner['topics'])}")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Connect", key=f"connect_{i}"):
                    st.success(f"Connection request sent to {partner['name']}!")
            
            with col2:
                # Message functionality
                message_text = st.text_input(f"Message to {partner['name']}", key=f"msg_input_{i}")
                if st.button("Send Message", key=f"send_msg_{i}"):
                    if message_text:
                        st.success(f"Message sent to {partner['name']}!")
                    else:
                        st.warning("Please enter a message before sending.")
            
            # Add a separator between partners
            st.markdown("---")
    else:
        st.info("No study partners found with the current filters.")
    
    # Create study group
    st.subheader("Create a Study Group")
    group_name = st.text_input("Group Name")
    group_description = st.text_area("Group Description", max_chars=200)
    group_size = st.number_input("Maximum Group Size", min_value=2, max_value=10, value=5)
    
    if st.button("Create Group"):
        if group_name and group_description:
            st.success(f"Study group '{group_name}' created successfully!")
            st.info("In the actual app, others would be able to find and join your group.")
        else:
            st.warning("Please provide a group name and description.")
def solve_doubts_with_ai(exam_type, stream_or_subject):
    """AI-powered doubt solving feature"""
    
    st.write(f"### AI Doubt Solver for {exam_type} {stream_or_subject if stream_or_subject else ''}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        doubt_text = st.text_area("Enter your doubt or question", height=100)
    
    with col2:
        doubt_type = st.selectbox(
            "Question Type",
            ["Conceptual", "Numerical", "Application", "Previous Year", "General"]
        )
        
        detail_level = st.select_slider(
            "Detail Level",
            options=["Basic", "Intermediate", "Detailed"]
        )
    
    # Optional file upload for relevant images/diagrams
    uploaded_file = st.file_uploader("Upload relevant image/diagram (optional)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", width=400)
    
    if st.button("Get Solution") and doubt_text:
        with st.spinner("Solving your doubt..."):
            # Customize prompt based on exam and detail level
            detail_modifier = {
                "Basic": "Provide a simple, concise explanation suitable for beginners",
                "Intermediate": "Provide a balanced explanation with some technical details",
                "Detailed": "Provide an in-depth explanation with technical details, formulas, and step-by-step workings"
            }
            
            solution = ai_generate_content(
                f"""Solve the following {doubt_type.lower()} doubt related to {exam_type} {stream_or_subject if stream_or_subject else ''}:
                
                {doubt_text}
                
                {detail_modifier[detail_level]}. Include relevant formulas, diagrams (described in text), and examples where appropriate.
                If this is a numerical problem, show all steps clearly.
                Also provide 1-2 similar practice questions at the end.
                """
            )
            
            st.subheader("📝 Solution to Your Doubt")
            st.markdown(solution)
            
            # Rate solution
            st.write("Was this solution helpful?")
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("👍 Yes"):
                    st.success("Thanks for your feedback!")
            with col2:
                if st.button("👎 No"):
                    improvement = st.text_area("How can we improve?")
                    if st.button("Submit Feedback"):
                        st.success("Thanks for your feedback!")
    
    # Recent/common doubts section
    st.subheader("Common Doubts & FAQs")
    
    # Sample common doubts based on exam type
    common_doubts = []
    
    if exam_type == "GATE" and stream_or_subject == "Computer Science (CS)":
        common_doubts = [
            "How to approach time complexity analysis in algorithms?",
            "Difference between process and thread in operating systems?",
            "How to solve recurrence relations in algorithm analysis?",
            "Normalization in database management systems?",
            "Key differences between TCP and UDP protocols?"
        ]
    elif exam_type in ["JEE Main", "JEE Advanced"]:
        common_doubts = [
            "How to approach rotational mechanics problems?",
            "Tips for solving complex organic chemistry reactions?",
            "Methods to solve differential equations in JEE?",
            "Common mistakes in electromagnetism problems?",
            "How to approach coordinate geometry problems effectively?"
        ]
    elif exam_type == "UPSC CSE":
        common_doubts = [
            "How to make effective notes for UPSC preparation?",
            "Approach to tackle current affairs for prelims?",
            "Strategy for answer writing in mains examination?",
            "How to integrate standard books with current issues?",
            "Tips for geography mapping practice?"
        ]
    else:
        common_doubts = [
            "Study strategies for this exam?",
            "How to manage time during the exam?",
            "Best resources for preparation?",
            "How to improve accuracy in the exam?",
            "Strategy for last month preparation?"
        ]
    
    # Display common doubts
    selected_doubt = st.selectbox("Browse Common Doubts", common_doubts)
    
    if st.button("Show Answer"):
        with st.spinner("Generating answer..."):
            common_answer = ai_generate_content(
                f"Provide a detailed answer to this frequently asked question for {exam_type} preparation: {selected_doubt}"
            )
            st.markdown(common_answer)

# -------------------- Personal Content Management Functions --------------------

def manage_personal_books():
    """Manage personal books and PDFs collection"""
    st.subheader("My Books & PDFs")
    
    if "user_books" not in st.session_state:
        # Initialize with sample books
        st.session_state.user_books = [
            {"title": "Introduction to Algorithms", "author": "Cormen et al.", "type": "Textbook", "notes": "Great reference for algorithm analysis", "file": None},
            {"title": "Deep Learning", "author": "Goodfellow et al.", "type": "Textbook", "notes": "Comprehensive coverage of neural networks", "file": None}
        ]
    
    books = st.session_state.user_books
    
    # Add new book/PDF
    with st.expander("➕ Add New Book or PDF"):
        new_title = st.text_input("Title")
        new_author = st.text_input("Author(s)")
        new_type = st.selectbox(
            "Type",
            ["Textbook", "Research Paper", "Notes", "Article", "Other"]
        )
        new_notes = st.text_area("Your Notes", height=100)
        new_file = st.file_uploader("Upload PDF (optional)", type=["pdf"])
        
        if st.button("Add Book") and new_title:
            books.append({
                "title": new_title, 
                "author": new_author, 
                "type": new_type, 
                "notes": new_notes,
                "file": new_file.name if new_file else None
            })
            st.success(f"Book '{new_title}' added successfully!")
            st.rerun()
    
    # Display books
    for i, book in enumerate(books):
        with st.expander(f"📕 {book['title']} - {book['author']} ({book['type']})"):
            st.write(f"**Notes:** {book['notes']}")
            
            if book['file']:
                st.write(f"**File:** {book['file']}")
                st.download_button(
                    label="Download PDF",
                    data=book['file'],
                    file_name=book['file']
                )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Edit", key=f"edit_book_{i}"):
                    st.session_state.edit_book_index = i
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_book_{i}"):
                    books.pop(i)
                    st.success("Book removed from collection")
                    st.rerun()
    
    # Edit book modal
    if "edit_book_index" in st.session_state:
        i = st.session_state.edit_book_index
        if i < len(books):
            st.subheader(f"Edit Book: {books[i]['title']}")
            
            books[i]['title'] = st.text_input("Title", books[i]['title'], key="edit_book_title")
            books[i]['author'] = st.text_input("Author(s)", books[i]['author'], key="edit_book_author")
            books[i]['type'] = st.selectbox(
                "Type",
                ["Textbook", "Research Paper", "Notes", "Article", "Other"],
                index=["Textbook", "Research Paper", "Notes", "Article", "Other"].index(books[i]['type']),
                key="edit_book_type"
            )
            books[i]['notes'] = st.text_area("Your Notes", books[i]['notes'], height=100, key="edit_book_notes")
            new_file = st.file_uploader("Replace PDF (optional)", type=["pdf"], key="edit_book_file")
            
            if new_file:
                books[i]['file'] = new_file.name
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes", key="save_book_changes"):
                    st.success("Book updated successfully!")
                    del st.session_state.edit_book_index
                    st.rerun()
            with col2:
                if st.button("Cancel", key="cancel_book_edit"):
                    del st.session_state.edit_book_index
                    st.rerun()
    
    # Book recommendation
    st.subheader("📚 Book Recommendations")
    recommendation_topic = st.text_input("Enter a topic for book recommendations")
    
    if st.button("Get Recommendations") and recommendation_topic:
        with st.spinner(f"Finding book recommendations for {recommendation_topic}..."):
            recommendations = ai_generate_content(
                f"""Recommend 5 top books or resources on the topic of {recommendation_topic}.
                
                For each book, provide:
                1. Title
                2. Author(s)
                3. Brief description (1-2 sentences)
                4. Difficulty level (Beginner, Intermediate, Advanced)
                5. Why it's valuable for this topic
                
                Format your response with clear headings for each book and numbered points within.
                """
            )
            st.markdown(recommendations)
            
            # Add recommended books option
            if st.button("Add these to my collection"):
                st.info("In a full implementation, this would parse the recommendations and add them to your collection.")

def manage_personal_videos():
    """Manage personal video collection"""
    st.subheader("My Video Collection")
    
    if "user_videos" not in st.session_state:
        # Initialize with sample videos
        st.session_state.user_videos = [
            {"title": "Introduction to Algorithms", "url": "https://www.youtube.com/watch?v=example1", "notes": "Good explanation of sorting algorithms", "category": "Computer Science"},
            {"title": "Neural Networks Explained", "url": "https://www.youtube.com/watch?v=example2", "notes": "Covers backpropagation in detail", "category": "AI/ML"}
        ]
    
    videos = st.session_state.user_videos
    
    # Add new video
    with st.expander("➕ Add New Video"):
        new_title = st.text_input("Video Title")
        new_url = st.text_input("Video URL (YouTube, Vimeo, etc.)")
        new_category = st.selectbox(
            "Category",
            ["Computer Science", "AI/ML", "Mathematics", "Electronics", "General", "Other"]
        )
        new_notes = st.text_area("Your Notes", height=100)
        
        if st.button("Add Video") and new_title and new_url:
            videos.append({
                "title": new_title, 
                "url": new_url, 
                "notes": new_notes, 
                "category": new_category
            })
            st.success(f"Video '{new_title}' added successfully!")
            st.rerun()
    
    # Filter videos
    all_categories = list(set([v["category"] for v in videos]))
    filter_category = st.multiselect("Filter by category", all_categories)
    
    # Apply filter
    filtered_videos = videos
    if filter_category:
        filtered_videos = [v for v in videos if v["category"] in filter_category]
    
    # Display videos
    for i, video in enumerate(filtered_videos):
        with st.expander(f"🎬 {video['title']} ({video['category']})"):
            st.write(f"**URL:** [{video['url']}]({video['url']})")
            
            # Embed video if from YouTube
            if "youtube.com" in video['url'] or "youtu.be" in video['url']:
                st.video(video['url'])
            
            st.write("**Your Notes:**")
            st.write(video['notes'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Edit", key=f"edit_video_{i}"):
                    st.session_state.edit_video_index = i
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"delete_video_{i}"):
                    videos.remove(video)  # Remove the specific video object
                    st.success("Video removed from collection")
                    st.rerun()
    
    # Edit video modal
    if "edit_video_index" in st.session_state:
        i = st.session_state.edit_video_index
        if i < len(videos):
            st.subheader(f"Edit Video: {videos[i]['title']}")
            
            videos[i]['title'] = st.text_input("Video Title", videos[i]['title'], key="edit_video_title")
            videos[i]['url'] = st.text_input("Video URL", videos[i]['url'], key="edit_video_url")
            videos[i]['category'] = st.selectbox(
                "Category",
                ["Computer Science", "AI/ML", "Mathematics", "Electronics", "General", "Other"],
                index=["Computer Science", "AI/ML", "Mathematics", "Electronics", "General", "Other"].index(videos[i]['category']) 
                    if videos[i]['category'] in ["Computer Science", "AI/ML", "Mathematics", "Electronics", "General", "Other"] else 0,
                key="edit_video_category"
            )
            videos[i]['notes'] = st.text_area("Your Notes", videos[i]['notes'], height=100, key="edit_video_notes")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes", key="save_video_changes"):
                    st.success("Video updated successfully!")
                    del st.session_state.edit_video_index
                    st.rerun()
            with col2:
                if st.button("Cancel", key="cancel_video_edit"):
                    del st.session_state.edit_video_index
                    st.rerun()
    
    # Video search feature
    st.subheader("🔍 Video Search")
    search_query = st.text_input("Search for videos")
    
    if search_query:
        search_results = [v for v in videos if search_query.lower() in v["title"].lower() or search_query.lower() in v["notes"].lower()]
        
        if search_results:
            st.write(f"**{len(search_results)} results found:**")
            
            for i, video in enumerate(search_results):
                st.write(f"**{i+1}. [{video['title']}]({video['url']})** ({video['category']})")
        else:
            st.info("No videos found matching your search.")
    
    # Video recommendations
    st.subheader("🎥 Recommended Educational Videos")
    
    recommendation_topic = st.text_input("Enter a topic for video recommendations")
    
    if st.button("Find Videos") and recommendation_topic:
        with st.spinner(f"Searching for videos on {recommendation_topic}..."):
            st.info("In a full implementation, this would connect to YouTube API to find educational videos on your topic.")
            
            # Simulate API response with AI-generated recommendations
            video_recommendations = ai_generate_content(
                f"""Recommend 5 educational videos that might exist on YouTube about {recommendation_topic}.
                
                For each video, provide:
                1. A realistic title
                2. A fictional creator/channel name
                3. A brief description of what the video would cover
                4. Why it would be valuable for learning this topic
                
                Format as a list with clear headings for each video.
                """
            )
            st.markdown(video_recommendations)

def manage_personal_notes():
    """Manage personal notes"""
    st.subheader("My Notes Collection")
    
    # Initialize notes in session state if not present
    if "user_notes" not in st.session_state:
        st.session_state.user_notes = [
            {"title": "Data Structures: Trees & Graphs", "content": "Sample note content about trees and graphs...", "tag": "Computer Science"},
            {"title": "Neural Networks Architecture", "content": "Sample note about neural network architectures...", "tag": "AI/ML"}
        ]
    
    notes = st.session_state.user_notes
    
    # Create tabs for different note views
    note_tabs = st.tabs(["Browse Notes", "Create Note", "AI Note Generator"])
    
    # TAB 1: Browse Notes
    with note_tabs[0]:
        # Filter options
        all_tags = sorted(list(set([note["tag"] for note in notes])))
        selected_tags = st.multiselect("Filter by tags", all_tags)
        search_term = st.text_input("Search in notes")
        
        # Apply filters
        filtered_notes = notes
        if selected_tags:
            filtered_notes = [note for note in filtered_notes if note["tag"] in selected_tags]
        if search_term:
            filtered_notes = [note for note in filtered_notes if search_term.lower() in note["title"].lower() or 
                             search_term.lower() in note["content"].lower()]
        
        # Sort options
        sort_by = st.selectbox("Sort by", ["Title (A-Z)", "Title (Z-A)", "Tag"])
        
        if sort_by == "Title (A-Z)":
            filtered_notes = sorted(filtered_notes, key=lambda x: x["title"])
        elif sort_by == "Title (Z-A)":
            filtered_notes = sorted(filtered_notes, key=lambda x: x["title"], reverse=True)
        elif sort_by == "Tag":
            filtered_notes = sorted(filtered_notes, key=lambda x: x["tag"])
        
        # Display notes
        for i, note in enumerate(filtered_notes):
            with st.expander(f"📝 {note['title']} ({note['tag']})"):
                st.markdown(note['content'])
                
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                with col1:
                    if st.button("Edit", key=f"edit_note_{i}"):
                        st.session_state.edit_note_index = i
                        st.session_state.edit_note = note
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"delete_note_{i}"):
                        notes.remove(note)
                        st.success("Note deleted")
                        st.rerun()
                with col3:
                    st.download_button(
                        label="Download",
                        data=note['content'],
                        file_name=f"{note['title'].replace(' ', '_')}.txt"
                    )
                with col4:
                    if st.button("Summarize", key=f"summarize_note_{i}"):
                        with st.spinner("Generating summary..."):
                            summary = ai_generate_content(
                                f"Summarize the following note in 3-5 bullet points:\n\n{note['content']}"
                            )
                            st.info("Summary:")
                            st.markdown(summary)
    
    # TAB 2: Create Note
    with note_tabs[1]:
        new_title = st.text_input("Note Title")
        
        # Rich text editor options
        text_format = st.radio("Text Format", ["Plain Text", "Markdown"], horizontal=True)
        
        if text_format == "Plain Text":
            new_content = st.text_area("Note Content", height=300)
        else:
            st.write("Markdown Editor (you can use markdown syntax)")
            new_content = st.text_area("Note Content", height=300, placeholder="# Heading\n\n**Bold text**\n\n- Bullet point\n\n```python\nprint('Code block')\n```")
            if new_content:
                st.write("Preview:")
                st.markdown(new_content)
        
        new_tag = st.selectbox(
            "Tag",
            ["Computer Science", "AI/ML", "Mathematics", "Physics", "Chemistry", "Biology", 
             "History", "Geography", "Economics", "General", "Other"]
        )
        
        if st.button("Save Note") and new_title and new_content:
            notes.append({"title": new_title, "content": new_content, "tag": new_tag})
            st.success(f"Note '{new_title}' saved successfully!")
            st.rerun()
    
    # TAB 3: AI Note Generator
    with note_tabs[2]:
        st.write("Let AI help you generate organized notes on any topic")
        
        ai_topic = st.text_input("Enter a topic for AI-generated notes")
        
        col1, col2 = st.columns(2)
        with col1:
            detail_level = st.select_slider(
                "Detail Level",
                options=["Basic", "Intermediate", "Comprehensive"]
            )
        with col2:
            format_style = st.selectbox(
                "Format Style",
                ["Comprehensive Notes", "Study Guide", "Summary Points", "Question & Answer", "Concept Map"]
            )
        
        if st.button("Generate Notes") and ai_topic:
            with st.spinner(f"Generating notes about {ai_topic}..."):
                # Customize prompt based on format and detail
                detail_modifier = {
                    "Basic": "concise and simple",
                    "Intermediate": "moderately detailed with key concepts",
                    "Comprehensive": "in-depth with comprehensive explanations"
                }
                
                format_instructions = {
                    "Comprehensive Notes": "Create comprehensive organized notes with headings, subheadings, and bullet points",
                    "Study Guide": "Create a study guide with clear sections, key concepts, definitions, and example problems",
                    "Summary Points": "Create concise summary points organized by key concepts",
                    "Question & Answer": "Create a set of important questions and detailed answers on the topic",
                    "Concept Map": "Create a textual representation of a concept map showing key concepts and their relationships"
                }
                
                ai_content = ai_generate_content(
                    f"""Create {detail_modifier[detail_level]} notes on the topic of {ai_topic}.
                    
                    {format_instructions[format_style]}.
                    
                    Include relevant terminology, key concepts, and examples.
                    Use markdown formatting with appropriate headings, lists, and emphasis.
                    """
                )
                
                # Display the generated notes
                st.subheader(f"AI-Generated Notes: {ai_topic}")
                st.markdown(ai_content)
                
                # Options to save or modify
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save to My Notes"):
                        notes.append({
                            "title": f"{ai_topic} ({format_style})", 
                            "content": ai_content, 
                            "tag": "AI-Generated"
                        })
                        st.success(f"Notes on '{ai_topic}' saved to your collection!")
                        st.rerun()
                with col2:
                    if st.button("Modify Before Saving"):
                        modified_content = st.text_area("Edit Notes", value=ai_content, height=400)
                        modified_title = st.text_input("Edit Title", value=f"{ai_topic} ({format_style})")
                        modified_tag = st.selectbox(
                            "Tag",
                            ["Computer Science", "AI/ML", "Mathematics", "Physics", "Chemistry", "Biology", 
                             "History", "Geography", "Economics", "General", "AI-Generated", "Other"]
                        )
                        
                        if st.button("Save Modified Notes"):
                            notes.append({
                                "title": modified_title, 
                                "content": modified_content, 
                                "tag": modified_tag
                            })
                            st.success(f"Modified notes on '{modified_title}' saved successfully!")
                            st.rerun()
                            # Edit note modal
    if "edit_note_index" in st.session_state and "edit_note" in st.session_state:
        i = st.session_state.edit_note_index
        note = st.session_state.edit_note
        
        st.subheader(f"Edit Note: {note['title']}")
        
        note['title'] = st.text_input("Note Title", note['title'], key="edit_note_title")
        
        # Determine if content is markdown
        is_markdown = any([
            note['content'].startswith('#'),
            '**' in note['content'],
            '*' in note['content'],
            '```' in note['content'],
            '- ' in note['content'],
            '1. ' in note['content']
        ])
        
        format_option = st.radio(
            "Text Format", 
            ["Plain Text", "Markdown"], 
            index=1 if is_markdown else 0,
            horizontal=True,
            key="edit_note_format"
        )
        
        note['content'] = st.text_area("Note Content", note['content'], height=300, key="edit_note_content")
        
        if format_option == "Markdown" and note['content']:
            st.write("Preview:")
            st.markdown(note['content'])
        
        note['tag'] = st.selectbox(
            "Tag",
            ["Computer Science", "AI/ML", "Mathematics", "Physics", "Chemistry", "Biology", 
             "History", "Geography", "Economics", "General", "AI-Generated", "Other"],
            index=["Computer Science", "AI/ML", "Mathematics", "Physics", "Chemistry", "Biology", 
                   "History", "Geography", "Economics", "General", "AI-Generated", "Other"].index(note['tag']) 
                  if note['tag'] in ["Computer Science", "AI/ML", "Mathematics", "Physics", "Chemistry", "Biology", 
                                    "History", "Geography", "Economics", "General", "AI-Generated", "Other"] else 0,
            key="edit_note_tag"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Changes", key="save_note_changes"):
                # Update the actual note in the list
                for idx, original_note in enumerate(notes):
                    if idx == i:
                        original_note.update(note)
                        break
                
                st.success("Note updated successfully!")
                del st.session_state.edit_note_index
                del st.session_state.edit_note
                st.rerun()
        with col2:
            if st.button("Cancel", key="cancel_note_edit"):
                del st.session_state.edit_note_index
                del st.session_state.edit_note
                st.rerun()

def display_personal_courses():
    """Display and manage personal courses"""
    st.subheader("My Course Collection")
    
    # Display existing courses
    if "user_courses" not in st.session_state:
        # Initialize with sample courses
        st.session_state.user_courses = [
            {"title": "Advanced Data Structures", "category": "Computer Science", "progress": 65, "materials": [], "notes": ""},
            {"title": "Machine Learning Fundamentals", "category": "AI/ML", "progress": 30, "materials": [], "notes": ""},
            {"title": "Computer Networks", "category": "Computer Science", "progress": 80, "materials": [], "notes": ""}
        ]
    
    courses = st.session_state.user_courses
    
    # Create tabs for different views
    course_tabs = st.tabs(["View Courses", "Add/Edit Course", "Course Analytics"])
    
    # TAB 1: View Courses
    with course_tabs[0]:
        # Filter courses
        all_categories = sorted(list(set([course["category"] for course in courses])))
        filter_category = st.multiselect("Filter by category", all_categories)
        
        # Apply filter
        filtered_courses = courses
        if filter_category:
            filtered_courses = [c for c in courses if c["category"] in filter_category]
        
        # Sort options
        sort_by = st.selectbox("Sort by", ["Title (A-Z)", "Progress (High to Low)", "Progress (Low to High)"])
        
        if sort_by == "Title (A-Z)":
            filtered_courses = sorted(filtered_courses, key=lambda x: x["title"])
        elif sort_by == "Progress (High to Low)":
            filtered_courses = sorted(filtered_courses, key=lambda x: x["progress"], reverse=True)
        elif sort_by == "Progress (Low to High)":
            filtered_courses = sorted(filtered_courses, key=lambda x: x["progress"])
        
        # Display courses
        for i, course in enumerate(filtered_courses):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{course['title']}** ({course['category']})")
                st.progress(course['progress'] / 100)
                st.write(f"{course['progress']}% complete")
            
            with col2:
                if st.button("View Details", key=f"view_{i}"):
                    st.session_state.view_course_index = i
                    st.rerun()
            
            with col3:
                if st.button("Delete", key=f"delete_course_{i}"):
                    courses.remove(course)
                    st.success("Course deleted")
                    st.rerun()
            
            st.divider()
    
    # TAB 2: Add/Edit Course
    with course_tabs[1]:
        if "edit_course_index" in st.session_state:
            # Edit existing course
            i = st.session_state.edit_course_index
            st.subheader(f"Edit Course: {courses[i]['title']}")
            
            courses[i]['title'] = st.text_input("Course Title", courses[i]['title'])
            courses[i]['category'] = st.selectbox(
                "Category",
                ["Computer Science", "AI/ML", "Web Development", "Mobile Development", 
                 "Mathematics", "Electronics", "Others"],
                index=["Computer Science", "AI/ML", "Web Development", "Mobile Development", 
                       "Mathematics", "Electronics", "Others"].index(courses[i]['category']) 
                      if courses[i]['category'] in ["Computer Science", "AI/ML", "Web Development", 
                                                   "Mobile Development", "Mathematics", "Electronics", "Others"] else 0
            )
            courses[i]['progress'] = st.slider("Progress", 0, 100, courses[i]['progress'])
            courses[i]['notes'] = st.text_area("Course Notes", courses[i]['notes'] if 'notes' in courses[i] else "")
            
            # Course materials
            st.subheader("Course Materials")
            if 'materials' not in courses[i]:
                courses[i]['materials'] = []
            
            for j, material in enumerate(courses[i]['materials']):
                with st.expander(f"Material {j+1}: {material['title']}"):
                    material['title'] = st.text_input("Title", material['title'], key=f"mat_title_{j}")
                    material['type'] = st.selectbox(
                        "Type",
                        ["Video", "Document", "Quiz", "Assignment", "Link"],
                        index=["Video", "Document", "Quiz", "Assignment", "Link"].index(material['type']) 
                              if material['type'] in ["Video", "Document", "Quiz", "Assignment", "Link"] else 0,
                        key=f"mat_type_{j}"
                    )
                    material['url'] = st.text_input("URL/Path", material['url'], key=f"mat_url_{j}")
                    material['completed'] = st.checkbox("Completed", material['completed'] if 'completed' in material else False, key=f"mat_completed_{j}")
                    
                    if st.button("Remove Material", key=f"remove_mat_{j}"):
                        courses[i]['materials'].pop(j)
                        st.rerun()
            
            # Add new material
            with st.expander("Add New Material"):
                new_mat_title = st.text_input("Title", key="new_mat_title")
                new_mat_type = st.selectbox(
                    "Type",
                    ["Video", "Document", "Quiz", "Assignment", "Link"],
                    key="new_mat_type"
                )
                new_mat_url = st.text_input("URL/Path", key="new_mat_url")
                new_mat_completed = st.checkbox("Completed", key="new_mat_completed")
                
                if st.button("Add Material") and new_mat_title:
                    courses[i]['materials'].append({
                        "title": new_mat_title,
                        "type": new_mat_type,
                        "url": new_mat_url,
                        "completed": new_mat_completed
                    })
                    st.success("Material added!")
                    st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Changes"):
                    st.success("Course updated successfully!")
                    del st.session_state.edit_course_index
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    del st.session_state.edit_course_index
                    st.rerun()
        else:
            # Add new course
            st.subheader("Add New Course")
            
            new_title = st.text_input("Course Title")
            new_category = st.selectbox(
                "Category",
                ["Computer Science", "AI/ML", "Web Development", "Mobile Development", 
                 "Mathematics", "Electronics", "Others"]
            )
            new_progress = st.slider("Initial Progress", 0, 100, 0)
            new_notes = st.text_area("Course Notes")
            
            if st.button("Add Course") and new_title:
                courses.append({
                    "title": new_title,
                    "category": new_category,
                    "progress": new_progress,
                    "materials": [],
                    "notes": new_notes
                })
                st.success(f"Added new course: {new_title}")
                st.rerun()
    
    # TAB 3: Course Analytics
    with course_tabs[2]:
        if courses:
            st.subheader("Course Progress Overview")
            
            # Calculate statistics
            total_courses = len(courses)
            completed_courses = sum(1 for c in courses if c["progress"] == 100)
            in_progress_courses = sum(1 for c in courses if 0 < c["progress"] < 100)
            not_started_courses = sum(1 for c in courses if c["progress"] == 0)
            
            # Display statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Courses", total_courses)
            with col2:
                st.metric("Completed", completed_courses)
            with col3:
                st.metric("In Progress", in_progress_courses)
            
            # Progress by category
            st.subheader("Progress by Category")
            
            # Group by category and calculate average progress
            category_progress = {}
            for course in courses:
                cat = course["category"]
                if cat not in category_progress:
                    category_progress[cat] = []
                category_progress[cat].append(course["progress"])
            
            # Calculate average for each category
            category_avg = {cat: sum(progs)/len(progs) for cat, progs in category_progress.items()}
            
            # Create progress bars for each category
            for cat, avg in category_avg.items():
                st.write(f"**{cat}**")
                st.progress(avg / 100)
                st.write(f"Average progress: {avg:.1f}%")
            
            # Course completion timeline projection
            st.subheader("Completion Timeline Projection")
            
            # For simplicity, assume 10% progress takes 1 week on average
            weeks_per_10_percent = 1
            
            # Calculate estimated weeks to completion for each in-progress course
            for course in [c for c in courses if c["progress"] < 100]:
                remaining_progress = 100 - course["progress"]
                estimated_weeks = (remaining_progress / 10) * weeks_per_10_percent
                
                st.write(f"**{course['title']}**: {course['progress']}% complete")
                
                if estimated_weeks < 1:
                    st.write(f"Estimated completion: Less than 1 week")
                elif estimated_weeks == 1:
                    st.write(f"Estimated completion: About 1 week")
                else:
                    st.write(f"Estimated completion: About {estimated_weeks:.1f} weeks")
        else:
            st.info("No courses available for analysis. Add some courses to see analytics.")
    
    # View course details
    if "view_course_index" in st.session_state:
        i = st.session_state.view_course_index
        course = courses[i]
        
        st.header(f"Course: {course['title']}")
        st.subheader(f"Category: {course['category']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Progress", f"{course['progress']}%")
        with col2:
            if st.button("Edit Course"):
                st.session_state.edit_course_index = i
                del st.session_state.view_course_index
                st.rerun()
        with col3:
            if st.button("Update Progress"):
                new_progress = st.slider("Course Progress", 0, 100, course['progress'])
                if st.button("Save New Progress"):
                    course['progress'] = new_progress
                    st.success("Progress updated!")
                    st.rerun()
        
        # Display notes
        st.subheader("Course Notes")
        if 'notes' in course and course['notes']:
            st.write(course['notes'])
        else:
            st.info("No notes available for this course.")
        
        # Display materials
        st.subheader("Course Materials")
        if 'materials' in course and course['materials']:
            for material in course['materials']:
                with st.container():  # Use container instead of expander to avoid nesting
                    st.markdown(f"**{material['title']} ({material['type']})**")
                    st.write(f"URL/Path: {material['url']}")
                    st.write(f"Status: {'✅ Completed' if material.get('completed', False) else '⏳ In Progress'}")
                    
                    if material['type'] == "Video" and ("youtube.com" in material['url'] or "youtu.be" in material['url']):
                        st.video(material['url'])
                    elif material['type'] == "Link":
                        st.markdown(f"[Open Link]({material['url']})")
                    
                    st.markdown("---")  # Add a divider between materials
        else:
            st.info("No materials available for this course.")
        
        # Add material button
        if st.button("Add Material to This Course"):
            st.session_state.adding_material_to_course = i
            st.rerun()
            
        # Material form appears when the button is clicked
        if hasattr(st.session_state, 'adding_material_to_course') and st.session_state.adding_material_to_course == i:
            st.subheader("Add New Material")
            if 'materials' not in course:
                course['materials'] = []
                
            material_title = st.text_input("Material Title")
            material_type = st.selectbox("Material Type", ["Video", "Document", "Quiz", "Assignment", "Link"])
            material_url = st.text_input("URL/Path")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Material") and material_title:
                    course['materials'].append({
                        "title": material_title,
                        "type": material_type,
                        "url": material_url,
                        "completed": False
                    })
                    del st.session_state.adding_material_to_course
                    st.success("Material added successfully!")
                    st.rerun()
            with col2:
                if st.button("Cancel Adding Material"):
                    del st.session_state.adding_material_to_course
                    st.rerun()
        
        # Back button
        if st.button("Back to Course List"):
            del st.session_state.view_course_index
            st.rerun()

def manage_personal_flashcards():
    """Manage personal flashcards for spaced repetition learning"""
    
    st.subheader("My Flashcards")
    
    if "user_flashcards" not in st.session_state:
        # Initialize with sample flashcards
        st.session_state.user_flashcards = {
            "Computer Science": [
                {"front": "What is a binary search tree?", "back": "A binary tree data structure where each node has at most two children, with all nodes in the left subtree having values less than the node, and all nodes in the right subtree having values greater than the node."},
                {"front": "What is the time complexity of quicksort?", "back": "Average case: O(n log n), Worst case: O(n²)"}
            ],
            "Mathematics": [
                {"front": "What is the derivative of e^x?", "back": "e^x"},
                {"front": "What is the integral of 1/x?", "back": "ln|x| + C"}
            ]
        }
    
    # Create new deck
    with st.expander("➕ Create New Deck"):
        new_deck_name = st.text_input("Deck Name")
        if st.button("Create Deck") and new_deck_name:
            if new_deck_name not in st.session_state.user_flashcards:
                st.session_state.user_flashcards[new_deck_name] = []
                st.success(f"Deck '{new_deck_name}' created successfully!")
                st.rerun()
            else:
                st.error("A deck with this name already exists.")
    
    # Select deck
    available_decks = list(st.session_state.user_flashcards.keys())
    if available_decks:
        selected_deck = st.selectbox("Select Deck", available_decks)
        
        # Add card to selected deck
        with st.expander("➕ Add New Card"):
            col1, col2 = st.columns(2)
            with col1:
                card_front = st.text_area("Front (Question)", height=100)
            with col2:
                card_back = st.text_area("Back (Answer)", height=100)
            
            if st.button("Add Card") and card_front and card_back:
                st.session_state.user_flashcards[selected_deck].append({"front": card_front, "back": card_back})
                st.success("Card added successfully!")
                st.rerun()
        
        # Display and manage cards
        st.subheader(f"Cards in {selected_deck}")
        
        if len(st.session_state.user_flashcards[selected_deck]) > 0:
            for i, card in enumerate(st.session_state.user_flashcards[selected_deck]):
                with st.container():  # Use container instead of expander
                    st.markdown(f"**Card {i+1}**: {card['front'][:50]}...")
                    
                    # Create a toggle for showing answer
                    if st.checkbox(f"Show Answer #{i+1}", key=f"show_answer_{i}"):
                        st.write("**Answer:**")
                        st.write(card['back'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Edit", key=f"edit_card_{i}"):
                            st.session_state.edit_card_index = i
                            st.session_state.edit_card_deck = selected_deck
                            st.rerun()
                    with col2:
                        if st.button("Delete", key=f"delete_card_{i}"):
                            st.session_state.user_flashcards[selected_deck].pop(i)
                            st.success("Card deleted successfully!")
                            st.rerun()
                    
                    st.markdown("---")  # Add a divider
            
            # Practice deck button
            if st.button("Practice This Deck"):
                st.session_state.practice_deck = selected_deck
                st.session_state.practice_index = 0
                st.session_state.show_answer = False
                st.rerun()
        else:
            st.info("This deck has no cards. Add some cards to get started!")
        
        # Deck management options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Rename Deck"):
                new_name = st.text_input("New Deck Name")
                if st.button("Save New Name") and new_name:
                    if new_name not in st.session_state.user_flashcards:
                        st.session_state.user_flashcards[new_name] = st.session_state.user_flashcards[selected_deck]
                        del st.session_state.user_flashcards[selected_deck]
                        st.success(f"Deck renamed to '{new_name}'")
                        st.rerun()
                    else:
                        st.error("A deck with this name already exists.")
        with col2:
            if st.button("Delete Deck"):
                if st.button("Confirm Delete"):
                    del st.session_state.user_flashcards[selected_deck]
                    st.success(f"Deck '{selected_deck}' deleted successfully!")
                    st.rerun()
        
        # AI-Generated Flashcards
        with st.container():  # Use container instead of expander
            st.subheader("🤖 Generate AI Flashcards")
            topic = st.text_input("Enter Topic for Flashcards")
            num_cards = st.slider("Number of Cards to Generate", 5, 20, 10)
            
            if st.button("Generate Flashcards") and topic:
                with st.spinner(f"Generating {num_cards} flashcards on {topic}..."):
                    ai_content = ai_generate_content(
                        f"""Generate {num_cards} flashcards on the topic of {topic}. 
                        Each flashcard should have a clear question on the front and a concise, informative answer on the back.
                        Format your response as a JSON array of objects, each with 'front' and 'back' fields."""
                    )
                    
                    try:
                        # This is a mock parsing since we don't actually have JSON in our ai_generate_content function
                        # In a real implementation, you would parse the JSON response
                        # For demonstration, we'll create some sample cards
                        cards = [
                            {"front": f"Question {i+1} about {topic}", "back": f"Answer {i+1} about {topic}"}
                            for i in range(num_cards)
                        ]
                        
                        # Add generated cards to the deck
                        for card in cards:
                            if 'front' in card and 'back' in card:
                                st.session_state.user_flashcards[selected_deck].append(card)
                        
                        st.success(f"Successfully generated and added {len(cards)} flashcards on {topic}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating flashcards: {str(e)}")
    else:
        st.info("No flashcard decks found. Create a new deck to get started!")
    
    # Card practice mode
    if "practice_deck" in st.session_state:
        deck = st.session_state.practice_deck
        cards = st.session_state.user_flashcards[deck]
        
        if cards:
            st.header(f"Practicing: {deck}")
            
            idx = st.session_state.practice_index
            card = cards[idx]
            
            # Display card front
            st.subheader("Question:")
            st.write(card['front'])
            
            # Toggle answer visibility
            if st.button("Show Answer" if not st.session_state.show_answer else "Hide Answer"):
                st.session_state.show_answer = not st.session_state.show_answer
            
            if st.session_state.show_answer:
                st.subheader("Answer:")
                st.write(card['back'])
                
                # Self-assessment buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("😔 Didn't Know"):
                        # In a real implementation, you would adjust the spaced repetition algorithm here
                        st.session_state.practice_index = (idx + 1) % len(cards)
                        st.session_state.show_answer = False
                        st.rerun()
                with col2:
                    if st.button("😐 Sort of Knew"):
                        st.session_state.practice_index = (idx + 1) % len(cards)
                        st.session_state.show_answer = False
                        st.rerun()
                with col3:
                    if st.button("😊 Knew It Well"):
                        st.session_state.practice_index = (idx + 1) % len(cards)
                        st.session_state.show_answer = False
                        st.rerun()
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Previous Card"):
                    st.session_state.practice_index = (idx - 1) % len(cards)
                    st.session_state.show_answer = False
                    st.rerun()
            with col2:
                if st.button("Next Card ➡️"):
                    st.session_state.practice_index = (idx + 1) % len(cards)
                    st.session_state.show_answer = False
                    st.rerun()
            
            # Exit practice mode
            if st.button("Exit Practice Mode"):
                del st.session_state.practice_deck
                del st.session_state.practice_index
                del st.session_state.show_answer
                st.rerun()
            
            # Show progress
            st.progress((idx + 1) / len(cards))
            st.caption(f"Card {idx + 1} of {len(cards)}")
def display_personal_progress():
    """Display personal learning progress and analytics"""
    
    st.subheader("My Learning Progress")
    
    # Sample learning data for demonstration
    if "learning_progress" not in st.session_state:
        # Initial data
        import datetime
        
        today = datetime.date.today()
        
        st.session_state.learning_progress = {
            "study_sessions": [
                {"date": (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d"), "minutes": 120, "topic": "Algorithms", "productivity": 7},
                {"date": (today - datetime.timedelta(days=28)).strftime("%Y-%m-%d"), "minutes": 90, "topic": "Operating Systems", "productivity": 8},
                {"date": (today - datetime.timedelta(days=25)).strftime("%Y-%m-%d"), "minutes": 150, "topic": "Databases", "productivity": 6},
                {"date": (today - datetime.timedelta(days=21)).strftime("%Y-%m-%d"), "minutes": 180, "topic": "Computer Networks", "productivity": 9},
                {"date": (today - datetime.timedelta(days=18)).strftime("%Y-%m-%d"), "minutes": 120, "topic": "Algorithms", "productivity": 8},
                {"date": (today - datetime.timedelta(days=15)).strftime("%Y-%m-%d"), "minutes": 90, "topic": "Operating Systems", "productivity": 7},
                {"date": (today - datetime.timedelta(days=12)).strftime("%Y-%m-%d"), "minutes": 150, "topic": "Databases", "productivity": 8},
                {"date": (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d"), "minutes": 180, "topic": "Computer Networks", "productivity": 9},
                {"date": (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), "minutes": 200, "topic": "Algorithms", "productivity": 9},
                {"date": (today - datetime.timedelta(days=5)).strftime("%Y-%m-%d"), "minutes": 120, "topic": "Operating Systems", "productivity": 8},
                {"date": (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d"), "minutes": 90, "topic": "Databases", "productivity": 7},
                {"date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"), "minutes": 150, "topic": "Computer Networks", "productivity": 8}
            ],
            "quiz_results": [
                {"date": (today - datetime.timedelta(days=29)).strftime("%Y-%m-%d"), "topic": "Algorithms", "score": 65, "total": 100},
                {"date": (today - datetime.timedelta(days=22)).strftime("%Y-%m-%d"), "topic": "Operating Systems", "score": 72, "total": 100},
                {"date": (today - datetime.timedelta(days=15)).strftime("%Y-%m-%d"), "topic": "Databases", "score": 68, "total": 100},
                {"date": (today - datetime.timedelta(days=8)).strftime("%Y-%m-%d"), "topic": "Computer Networks", "score": 75, "total": 100},
                {"date": (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d"), "topic": "Algorithms", "score": 82, "total": 100}
            ],
            "topic_proficiency": {
                "Algorithms": 82,
                "Operating Systems": 75,
                "Databases": 68,
                "Computer Networks": 78,
                "Theory of Computation": 60,
                "Compiler Design": 50,
                "Digital Logic": 65
            }
        }
    
    # Add session form
    with st.container():  # Use container instead of expander
        st.subheader("➕ Log Study Session")
        col1, col2, col3 = st.columns(3)
        with col1:
            session_date = st.date_input("Date")
        with col2:
            session_minutes = st.number_input("Minutes Studied", min_value=5, max_value=600, value=60, step=5)
        with col3:
            session_topic = st.selectbox("Topic", list(st.session_state.learning_progress["topic_proficiency"].keys()))
        
        session_productivity = st.slider("Productivity Rating (1-10)", 1, 10, 7)
        session_notes = st.text_area("Session Notes", height=100)
        
        if st.button("Save Session"):
            st.session_state.learning_progress["study_sessions"].append({
                "date": session_date.strftime("%Y-%m-%d"),
                "minutes": session_minutes,
                "topic": session_topic,
                "productivity": session_productivity
            })
            st.success("Study session logged successfully!")
            st.rerun()
    
    # Add quiz/test result form
    with st.container():  # Use container instead of expander
        st.subheader("➕ Log Quiz/Test Result")
        col1, col2, col3 = st.columns(3)
        with col1:
            quiz_date = st.date_input("Date", key="quiz_date")
        with col2:
            quiz_topic = st.selectbox("Topic", list(st.session_state.learning_progress["topic_proficiency"].keys()), key="quiz_topic")
        with col3:
            quiz_type = st.selectbox("Type", ["Quiz", "Mock Test", "Practice Test"])
        
        col1, col2 = st.columns(2)
        with col1:
            quiz_score = st.number_input("Score", min_value=0, max_value=100, value=70)
        with col2:
            quiz_total = st.number_input("Total Possible", min_value=1, max_value=100, value=100)
        
        if st.button("Save Result"):
            st.session_state.learning_progress["quiz_results"].append({
                "date": quiz_date.strftime("%Y-%m-%d"),
                "topic": quiz_topic,
                "score": quiz_score,
                "total": quiz_total
            })
            
            # Update topic proficiency (simple calculation, in a real app this would be more sophisticated)
            current_prof = st.session_state.learning_progress["topic_proficiency"][quiz_topic]
            new_prof = int(current_prof * 0.7 + (quiz_score/quiz_total * 100) * 0.3)  # Weighted average
            st.session_state.learning_progress["topic_proficiency"][quiz_topic] = new_prof
            
            st.success(f"Quiz result saved! Your {quiz_topic} proficiency is now {new_prof}%")
            st.rerun()
    
    # Display learning analytics
    
    # 1. Study time summary
    st.subheader("📊 Study Time Analytics")
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Convert sessions to DataFrame
    sessions_df = pd.DataFrame(st.session_state.learning_progress["study_sessions"])
    sessions_df["date"] = pd.to_datetime(sessions_df["date"])
    
    # Time studied by topic
    topic_time = sessions_df.groupby("topic")["minutes"].sum().reset_index()
    topic_time["hours"] = topic_time["minutes"] / 60
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(topic_time["topic"], topic_time["hours"])
    
    # Add data labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.1f}h', ha='center', va='bottom')
    
    plt.title("Total Study Hours by Topic")
    plt.xlabel("Topic")
    plt.ylabel("Hours")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    
    # Study time per day (last 30 days)
    st.subheader("📈 Daily Study Time (Last 30 Days)")
    
    # Group by date and calculate total minutes per day
    last_30_days = pd.DataFrame(sessions_df[sessions_df["date"] >= pd.Timestamp.now() - pd.Timedelta(days=30)])
    daily_time = last_30_days.groupby(last_30_days["date"].dt.date)["minutes"].sum().reset_index()
    
    # Add missing dates with 0 minutes
    date_range = pd.date_range(end=pd.Timestamp.now(), periods=30).date
    full_dates = pd.DataFrame({"date": date_range})
    daily_time = full_dates.merge(daily_time, on="date", how="left").fillna(0)
    
    # Plot daily study time
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_time["date"], daily_time["minutes"] / 60, marker='o', linestyle='-', linewidth=2)
    
    # Add a 7-day moving average
    daily_time["hours"] = daily_time["minutes"] / 60
    daily_time["rolling_avg"] = daily_time["hours"].rolling(window=7, min_periods=1).mean()
    ax.plot(daily_time["date"], daily_time["rolling_avg"], linestyle='--', color='red', label='7-day Avg')
    
    # Calculate total and average
    total_hours = daily_time["hours"].sum()
    avg_hours = daily_time["hours"].mean()
    
    # Add summary text to the plot
    ax.text(0.02, 0.95, f"Total: {total_hours:.1f} hours\nDaily Avg: {avg_hours:.1f} hours", 
            transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.title("Daily Study Hours (Last 30 Days)")
    plt.xlabel("Date")
    plt.ylabel("Hours")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)
    
    # 2. Topic proficiency radar chart
    st.subheader("🎯 Topic Proficiency")
    
    # Get topic proficiencies
    topics = list(st.session_state.learning_progress["topic_proficiency"].keys())
    proficiencies = list(st.session_state.learning_progress["topic_proficiency"].values())
    
    # Create radar chart
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar=True)
    
    # Compute angle for each topic
    angles = np.linspace(0, 2*np.pi, len(topics), endpoint=False).tolist()
    # Make the plot circular by appending the first value to the end
    angles += angles[:1]
    proficiencies += proficiencies[:1]
    topics += topics[:1]
    
    # Plot and fill
    ax.plot(angles, proficiencies, linewidth=2)
    ax.fill(angles, proficiencies, alpha=0.25)
    
    # Set labels and limits
    ax.set_thetagrids(np.degrees(angles[:-1]), topics[:-1])
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"])
    ax.grid(True)
    
    plt.title("Topic Proficiency Radar", size=15, y=1.1)
    st.pyplot(fig)
    
    # 3. Quiz performance trends
    st.subheader("📝 Quiz Performance Trends")
    
    # Convert quiz results to DataFrame
    quiz_df = pd.DataFrame(st.session_state.learning_progress["quiz_results"])
    quiz_df["date"] = pd.to_datetime(quiz_df["date"])
    quiz_df["percentage"] = (quiz_df["score"] / quiz_df["total"] * 100).round(1)
    
    # Group by topic
    topic_quiz_results = quiz_df.groupby(["topic", "date"])["percentage"].mean().reset_index()
    
    # Plot quiz scores by topic over time
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot each topic with a different color
    for topic in topic_quiz_results["topic"].unique():
        topic_data = topic_quiz_results[topic_quiz_results["topic"] == topic]
        ax.plot(topic_data["date"], topic_data["percentage"], marker='o', linestyle='-', label=topic)
    
    plt.title("Quiz Performance by Topic")
    plt.xlabel("Date")
    plt.ylabel("Score (%)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc="best")
    plt.ylim(0, 100)
    plt.tight_layout()
    st.pyplot(fig)
    
    # 4. Productivity correlation
    st.subheader("⚡ Productivity Analysis")
    
    # Calculate correlation between study session duration and productivity
    corr = sessions_df["minutes"].corr(sessions_df["productivity"])
    
    # Scatter plot of session duration vs productivity
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sessions_df["minutes"], sessions_df["productivity"], alpha=0.7)
    
    # Add trend line
    z = np.polyfit(sessions_df["minutes"], sessions_df["productivity"], 1)
    p = np.poly1d(z)
    ax.plot(sessions_df["minutes"], p(sessions_df["minutes"]), "r--", alpha=0.7)
    
    # Add correlation info
    ax.text(0.05, 0.95, f"Correlation: {corr:.2f}", transform=ax.transAxes, 
            fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.title("Study Session Duration vs. Productivity")
    plt.xlabel("Session Duration (minutes)")
    plt.ylabel("Productivity Rating (1-10)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)
    
    # 5. Topic recommendation
    st.subheader("🔍 Recommendations")
    
    # Find the weakest topics (lowest proficiency)
    topic_proficiency = st.session_state.learning_progress["topic_proficiency"]
    sorted_topics = sorted(topic_proficiency.items(), key=lambda x: x[1])
    
    # Recommend focusing on the weakest topics
    st.write("Based on your proficiency levels, consider focusing on these topics:")
    
    for topic, prof in sorted_topics[:3]:
        if prof < 70:
            st.warning(f"⚠️ **{topic}**: Current proficiency is only {prof}%. This needs immediate attention.")
        else:
            st.info(f"ℹ️ **{topic}**: Current proficiency is {prof}%. This could use some improvement.")
    
    # Calculate optimal study time allocation
    total_study_time = 10  # Example: 10 hours per week
    total_proficiency = sum([100 - prof for _, prof in sorted_topics])  # Invert proficiency
    
    if total_proficiency > 0:
        st.write(f"### Recommended Weekly Study Plan (Based on {total_study_time} hours/week)")
        
        allocation_data = []
        for topic, prof in sorted_topics:
            # Allocate more time to weaker topics
            inverse_prof = 100 - prof
            allocation_percent = inverse_prof / total_proficiency
            hours = round(total_study_time * allocation_percent, 1)
            allocation_data.append({"Topic": topic, "Proficiency": prof, "Hours": hours})
        
        # Create allocation DataFrame
        allocation_df = pd.DataFrame(allocation_data)
        
        # Display as a table
        st.dataframe(allocation_df, hide_index=True)
        
        # Create pie chart of recommended time allocation
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(allocation_df["Hours"], labels=allocation_df["Topic"], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Recommended Study Time Allocation')
        st.pyplot(fig)
    
    # Generate personalized AI insights
    if st.button("Generate AI Learning Insights"):
        with st.spinner("Analyzing your learning data..."):
            # Prepare data for AI analysis
            sessions_summary = ', '.join([f"{row['topic']}: {row['minutes']} minutes (productivity: {row['productivity']}/10)" 
                                        for _, row in sessions_df.tail(5).iterrows()])
            
            quiz_summary = ', '.join([f"{row['topic']}: {row['percentage']}%" 
                                     for _, row in quiz_df.tail(5).iterrows()])
            
            proficiency_summary = ', '.join([f"{topic}: {prof}%" for topic, prof in topic_proficiency.items()])
            
            insights = ai_generate_content(
                f"""Analyze this learning data and provide personalized insights and recommendations:
                
                Recent study sessions: {sessions_summary}
                
                Recent quiz results: {quiz_summary}
                
                Current topic proficiencies: {proficiency_summary}
                
                Please provide:
                1. Key observations about learning patterns
                2. Specific recommendations to improve weakest areas
                3. Study strategy optimization suggestions
                4. Time management advice based on productivity patterns
                5. Next steps for continued progress
                
                Format your response in clear sections with bullet points where appropriate.
                """
            )
            st.markdown(insights)
