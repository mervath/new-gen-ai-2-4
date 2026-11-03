from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import openai
import json
from datetime import datetime
import fitz  # PyMuPDF for PDFs
import docx  # For Word document handling
import ast  # For checking Python syntax
import io  # For handling uploaded files
import sqlite3
import os
from io import BytesIO
import xgboost as xgb
import numpy as np
import cv2
import time
from PIL import Image, ImageDraw
from PIL import Image, ImageDraw
from io import BytesIO
# Add this near your other imports
from ai_tutor_helper import setup_ai_tutor, display_ai_tutor_page
from content_management_system import integrate_cms_with_app
from research_tools_integration import integrate_cms_with_app
from syllabus_optimization import display_syllabus_optimization, integrate_syllabus_optimization_with_app
# STEP 1: Add these new imports near the top of your file, with your other imports
# Add them after your existing imports like numpy, PIL, etc.
# Add this function to create improved icon navigation

def create_improved_icon_sidebar():
    """
    Create an improved sidebar with clickable icons that directly trigger functionality
    """
    st.sidebar.header("Navigation")
    
    # Define menu items with icons, labels, and keys
    # In create_improved_icon_sidebar() function:
    # In create_improved_icon_sidebar() function:
    menu_items = [
        {"icon": "📊", "label": "Dashboard", "key": "dashboard"},
        {"icon": "👨‍🏫", "label": "AI Tutor", "key": "ai_tutor"},
        {"icon": "📝", "label": "AI Exam", "key": "ai_exam"},
        {"icon": "👤", "label": "AI Student Info", "key": "ai_student_info"},
        {"icon": "🔍", "label": "AI Search", "key": "ai_search"},
        {"icon": "📈", "label": "AI Assessment", "key": "ai_assessment"},
        {"icon": "🎯", "label": "Learning Analytics", "key": "learning_analytics"},  # This was missing
        {"icon": "🔬", "label": "Research Tools", "key": "research_tools"},  # NEW ITEM
        {"icon": "📚", "label": "Content Management", "key": "content_management"},
        {"icon": "🔌", "label": "Integrations", "key": "integrations"}
    ]

    
    # Create a 4-column layout for the icons
    cols = st.sidebar.columns(4)
    
    # Arrange icons in the grid
    for i, item in enumerate(menu_items):
        col_idx = i % 4  # Determine which column to place the icon
        
        # Create a clickable button with the icon and label
        with cols[col_idx]:
            # Create a container for better styling
            with st.container():
                # Button with icon
                if st.button(
                    item["icon"], 
                    key=f"nav_{item['key']}",
                    help=item["label"],
                    use_container_width=True
                ):
                    # Update session state to reflect the selected category
                    st.session_state.selected_category = item["label"]
                    st.rerun()
                
                # Display label below icon
                st.markdown(
                    f"<div style='text-align: center; font-size: 0.8rem; margin-top: -15px;'>{item['label']}</div>", 
                    unsafe_allow_html=True
                )
    
    # Return the current selection (default to Dashboard if none selected)
    return st.session_state.get("selected_category", "Dashboard")


# Alternative implementation using CSS for better styling
def create_stylish_icon_sidebar():
    """
    Create a stylish sidebar with better-looking icons and direct functionality
    """
    st.sidebar.header("Navigation")
    
    # Add custom CSS for better styling
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: transparent;
        border: none;
        font-size: 24px;
        display: flex;
        justify-content: center;
        padding: 10px 0;
        width: 100%;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: rgba(0, 0, 0, 0.05);
        transform: scale(1.1);
        transition: transform 0.2s ease;
    }
    .selected-button {
        background-color: #1E90FF !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .icon-label {
        text-align: center;
        font-size: 0.7rem;
        margin-top: -15px;
        font-weight: normal;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Define menu items with icons, labels, and keys
    menu_items = [
        {"icon": "📊", "label": "Dashboard", "key": "dashboard"},
        {"icon": "👨‍🏫", "label": "AI Tutor", "key": "ai_tutor"},
        {"icon": "📝", "label": "AI Exam", "key": "ai_exam"},
        {"icon": "👤", "label": "AI Student Info", "key": "ai_student_info"},
        {"icon": "🔍", "label": "AI Search", "key": "ai_search"},
        {"icon": "📈", "label": "AI Assessment", "key": "ai_assessment"},
        {"icon": "📚", "label": "Content Management", "key": "content_management"},
        {"icon": "🔌", "label": "Integrations", "key": "integrations"}
    ]
    
    # Create a 4-column layout
    cols = st.sidebar.columns(4)
    
    # Loop through menu items and create icon buttons
    for i, item in enumerate(menu_items):
        col_idx = i % 4
        
        with cols[col_idx]:
            # Check if this item is selected
            is_selected = st.session_state.get("selected_category") == item["label"]
            
            # Create a container for the icon and label
            with st.container():
                # Button with icon
                if st.button(
                    item["icon"], 
                    key=f"styled_nav_{item['key']}",
                    help=item["label"]
                ):
                    st.session_state.selected_category = item["label"]
                    st.rerun()
                
                # Display label below icon
                st.markdown(
                    f"<div class='icon-label'>{item['label']}</div>", 
                    unsafe_allow_html=True
                )
    
    # Apply highlighting to the selected button using JavaScript
    if "selected_category" in st.session_state:
        selected = st.session_state["selected_category"]
        for item in menu_items:
            if item["label"] == selected:
                # Find the button for this item and add the selected class
                st.markdown(f"""
                <script>
                    document.querySelector('button[key="styled_nav_{item['key']}"]').classList.add('selected-button');
                </script>
                """, unsafe_allow_html=True)
    
    # Return the current selection
    return st.session_state.get("selected_category", "Dashboard")


# Function to use modern SVG or Font Awesome icons
def create_modern_icon_sidebar():
    """
    Create a modern sidebar with professional icons that directly trigger functionality
    """
    st.sidebar.header("Navigation")
    
    # CSS for modern styling
    st.markdown("""
    <style>
    .icon-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }
    .icon-button {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: transparent;
        border: none;
        cursor: pointer;
        padding: 10px 5px;
        border-radius: 10px;
    }
    .icon-button:hover {
        background-color: #f0f0f0;
    }
    .icon-button.selected {
        background-color: #e6f3ff;
    }
    .icon-image {
        width: 32px;
        height: 32px;
        margin-bottom: 5px;
    }
    .icon-label {
        font-size: 0.7rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Define menu items with modern icons
    menu_items = [
        {"label": "Dashboard", "key": "dashboard", "icon": "📊"},
        {"label": "AI Tutor", "key": "ai_tutor", "icon": "👨‍🏫"},
        {"label": "AI Exam", "key": "ai_exam", "icon": "📝"},
        {"label": "AI Student Info", "key": "ai_student_info", "icon": "👤"},
        {"label": "AI Search", "key": "ai_search", "icon": "🔍"},
        {"label": "AI Assessment", "key": "ai_assessment", "icon": "📈"},
        {"label": "Content Management", "key": "content_management", "icon": "📚"},
        {"label": "Integrations", "key": "integrations", "icon": "🔌"}
    ]
    
    # Create grid container for icons
    html_buttons = "<div class='icon-grid'>"
    
    # Generate HTML for each icon button
    for item in menu_items:
        # Determine if this item is selected
        selected_class = " selected" if st.session_state.get("selected_category") == item["label"] else ""
        
        # Create button HTML
        html_buttons += f"""
        <button class="icon-button{selected_class}" onclick="selectCategory('{item['label']}', '{item['key']}')">
            <div class="icon-image">{item['icon']}</div>
            <div class="icon-label">{item['label']}</div>
        </button>
        """
    
    # Close grid container
    html_buttons += "</div>"
    
    # Add JavaScript for selection handling
    selection_script = """
    <script>
    function selectCategory(category, key) {
        // Use Streamlit's setComponentValue to update a session variable
        // This requires the Streamlit Component API
        const data = {
            category: category,
            key: key
        };
        
        // Store data locally in case we need to refresh
        localStorage.setItem('selectedCategory', JSON.stringify(data));
        
        // Force page reload to apply the selection
        window.location.reload();
    }
    </script>
    """
    
    # Render the icon grid
    st.sidebar.markdown(html_buttons + selection_script, unsafe_allow_html=True)
    
    # Below the visual icons, add hidden buttons for actual functionality
    col1, col2, col3, col4 = st.sidebar.columns(4)
    cols = [col1, col2, col3, col4]
    
    # Create actual Streamlit buttons but keep them very small/hidden
    for i, item in enumerate(menu_items):
        col_idx = i % 4
        with cols[col_idx]:
            # Create a tiny button
            if st.button(".", key=f"hidden_btn_{item['key']}", help=item["label"]):
                st.session_state.selected_category = item["label"]
                st.rerun()
    
    # Add a way to detect selection from localStorage
    st.markdown("""
    <script>
    // Check if there's a stored selection
    const storedData = localStorage.getItem('selectedCategory');
    if (storedData) {
        const data = JSON.parse(storedData);
        // Find the hidden button and click it
        document.querySelector(`button[key="hidden_btn_${data.key}"]`).click();
        // Clear storage to prevent loops
        localStorage.removeItem('selectedCategory');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Return the current selection
    return st.session_state.get("selected_category", "Dashboard")

# Initialize session state function stays the same
def initialize_session_state():
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Dashboard"
def get_page_from_category(category):
    """Map the selected category to the appropriate page"""
    
    if category == "Dashboard":
        return "📊 Dashboard"
    
    elif category == "AI Tutor":
        # AI Tutor is directly accessible - just display the AI Tutor page
        display_ai_tutor_page(students_data)
        return None  # Set page to None to prevent other pages from displaying
    
    elif category == "AI Exam":
        # Exam submenu
        exam_options = ["📝 Take Quiz", "📚 Quiz History", "📝 Live OMR Test"]
        exam = st.sidebar.selectbox("Select Exam Type", exam_options)
        return exam
    
    elif category == "AI Student Info":
        # Student info submenu
        student_info_options = ["📄 AI-Based LOR Generator", "📈 ML Performance Tracking & Prediction"]
        student_info = st.sidebar.selectbox("Select Student Tool", student_info_options)
        return student_info
    
    elif category == "AI Search":
        # Search submenu
        search_options = ["📖 AI-Powered Storytelling", "🔍 AI Peer Assessment", "🧠 AI-Powered Hints"]
        search = st.sidebar.selectbox("Select Search Tool", search_options)
        return search
    
    elif category == "AI Assessment":
        # Assessment submenu
        assessment_options = [
            "🔍 Plagiarism/Reasoning Finder",
            "📂 Code Evaluation & Plagiarism Check",
            "📝 NLP Answer Evaluation",
            "📝 OMR MCQ Grading",
            "🔒 AI Proctoring & Integrity Checks",
            "📅 Syllabus Optimization Engine",
            "📝 AI Paper Setter"  # Add this new option
            ]
        assessment = st.sidebar.selectbox("Select Assessment Tool", assessment_options)
        return assessment
    
    elif category == "Content Management":
        # Display the content management system
        integrate_cms_with_app()
        return None  # Set page to None to prevent other pages from displaying
    
    elif category == "Learning Analytics":
        display_ai_learning_analytics()
        return None

    elif category == "Research Tools":
        # Research Tools submenu
        research_tools_options = [
            "📚 Citation Management",
            "📖 Literature Review Assistant",
            "🧪 Research Methodology",
            "📊 Data Analysis Tools",
            "🔍 Academic Integrity"
        ]
        research_tool = st.sidebar.selectbox("Select Research Tool", research_tools_options)
        return research_tool
    
    elif category == "Integrations":
        # Display the integrations page
        st.title("🔌 Third-Party Integrations")
        
        tabs = st.tabs(["LMS", "Cloud Storage", "Calendar"])
        
        with tabs[0]:
            st.header("Learning Management System (LMS) Integration")
            
            lms_type = st.selectbox("Select LMS", ["Canvas", "Moodle", "Blackboard", "Google Classroom"])
            st.text_input("API Key", type="password")
            st.text_input("API URL")
            st.checkbox("Enable Auto-Sync")
            
            if st.button("Save LMS Settings"):
                st.success(f"{lms_type} integration settings saved!")
        
        with tabs[1]:
            st.header("Cloud Storage Integration")
            
            storage_type = st.selectbox("Select Storage Provider", ["Google Drive", "OneDrive", "Dropbox", "AWS S3"])
            st.text_input("Access Key/Token", type="password")
            st.text_input("Secret Key (if applicable)", type="password")
            st.text_input("Default Folder Path", "/assignments")
            
            uploaded_file = st.file_uploader("Test Upload", type=["pdf", "docx", "pptx"])
            if uploaded_file and st.button("Upload to Cloud"):
                st.success(f"File uploaded to {storage_type}!")
        
        with tabs[2]:
            st.header("Calendar Integration")
            
            calendar_type = st.selectbox("Select Calendar", ["Google Calendar", "Outlook Calendar", "Apple Calendar"])
            st.text_input("Calendar ID")
            st.text_input("API Key", type="password", key="cal_key")
            sync_types = st.multiselect("Sync Event Types", ["Assignments", "Exams", "Class Schedule", "Office Hours"])
            
            if st.button("Save Calendar Settings"):
                st.success(f"{calendar_type} integration settings saved!")
        
        return None  # Set page to None to prevent other pages from displaying
    
    # Default return if no category matches
    return None

# USAGE IN MAIN CODE:
# Initialize session state
# initialize_session_state()
# 
# # Set up the app title
# st.title("🚀 Generative AI-Based Students Assessment System")
# 
# # Create the improved icon-based sidebar for navigation - CHOOSE ONE:
# main_category = create_improved_icon_sidebar()  # Basic improved version
# # OR
# main_category = create_stylish_icon_sidebar()   # More stylish version
# # OR
# main_category = create_modern_icon_sidebar()    # Modern version with custom styling
# 
# # Get the page to display based on the selected category 
# page = get_page_from_category(main_category)

# For Live OMR Test webcam functionality
try:
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
    import av
    import threading
    import queue
except ImportError:
    pass

# Uncomment and install these if needed
# !pip install opencv-python face_recognition xgboost scikit-learn streamlit_webrtc pillow av streamlit_webrtc

try:
    import cv2  # for Computer Vision (OMR, Face/Eye detection, etc.)
except ImportError:
    pass

try:
    import face_recognition  # for facial recognition
except ImportError:
    pass

try:
    import xgboost as xgb  # for XGBoost-based predictions
except ImportError:
    pass

try:
    from sklearn.ensemble import RandomForestClassifier
except ImportError:
    pass

# ---------------- SET YOUR OPENAI API KEY HERE ----------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect('student_quiz_history.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        topic TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    return conn

def save_quiz_result(student_id, student_name, topic, score, total_questions):
    conn = init_db()
    c = conn.cursor()
    c.execute('''
    INSERT INTO quiz_results (student_id, student_name, topic, score, total_questions, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, student_name, topic, score, total_questions, datetime.now()))
    conn.commit()
    conn.close()

def get_student_quiz_history(student_id=None):
    conn = init_db()
    c = conn.cursor()
    if student_id:
        c.execute('''
        SELECT student_id, student_name, topic, score, total_questions, timestamp
        FROM quiz_results
        WHERE student_id = ?
        ORDER BY timestamp DESC
        ''', (student_id,))
    else:
        c.execute('''
        SELECT student_id, student_name, topic, score, total_questions, timestamp
        FROM quiz_results
        ORDER BY timestamp DESC
        ''')
    results = c.fetchall()
    conn.close()
    if results:
        return pd.DataFrame(results, columns=['student_id', 'student_name', 'topic', 'score', 'total_questions', 'timestamp'])
    return pd.DataFrame()

def extract_text_from_docx(uploaded_file):
    """Extract text from a .docx file"""
    try:
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_pdf(uploaded_file):
    """Extract text from a .pdf file."""
    try:
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def check_python_syntax(code):
    """Check for syntax errors in uploaded Python code."""
    try:
        ast.parse(code)
        return None  # No syntax errors
    except SyntaxError as e:
        return f"Syntax Error: {e}"

# ---------------- LIVE OMR TEST FUNCTIONS ----------------
# Video processor for proctoring during the test
# Video processor for proctoring during the test
# Enhanced Video Processor for AI Proctoring
class EnhancedVideoProcessor(VideoTransformerBase):
    def __init__(self):
        # Face and eye detection using Haar cascades
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # State tracking
        self.frame_count = 0
        self.last_warning_time = time.time() - 10  # Initialize to allow immediate warnings
        self.face_detected = False
        self.eyes_detected = False
        self.multiple_faces = False
        self.looking_away_duration = 0
        self.suspicious_movements = 0
        
        # Audio monitoring
        self.audio_threshold = 0.1
        self.last_audio_warning_time = time.time() - 10
        self.noise_detection_window = []
        
        # Warning management
        self.should_warn = False
        self.warning_message = ""
        self.warning_type = None
        
        # Debug and analytics
        self.debug_info = {
            "frames_processed": 0,
            "face_detections": 0,
            "eye_detections": 0,
            "warnings_triggered": 0,
            "audio_warnings": 0,
            "multi_face_warnings": 0
        }
        
        # Movement detection
        self.prev_frame = None
        self.movement_threshold = 0.05
        self.movement_detection_counter = 0
        
    def detect_suspicious_movement(self, current_frame):
        """Detect rapid or unusual movements in the frame"""
        if self.prev_frame is None:
            self.prev_frame = current_frame
            return False
        
        # Calculate frame difference
        frame_diff = cv2.absdiff(current_frame, self.prev_frame)
        gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        _, thresh_diff = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
        
        # Calculate movement percentage
        movement_percentage = np.sum(thresh_diff) / (thresh_diff.shape[0] * thresh_diff.shape[1] * 255)
        
        # Update previous frame
        self.prev_frame = current_frame
        
        # Check if movement exceeds threshold
        if movement_percentage > self.movement_threshold:
            self.movement_detection_counter += 1
            # Only trigger warning if we have detected excessive movement for several frames
            if self.movement_detection_counter > 5:
                return True
        else:
            self.movement_detection_counter = max(0, self.movement_detection_counter - 1)
            
        return False

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1
        self.debug_info["frames_processed"] += 1
        
        # Process every frame for better responsiveness
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # More sensitive face detection
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.05,
            minNeighbors=3,
            minSize=(20, 20),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Update face detection state
        prev_face_detected = self.face_detected
        self.face_detected = len(faces) > 0
        
        # Check for multiple faces - potential cheating
        self.multiple_faces = len(faces) > 1
        
        if self.face_detected:
            self.debug_info["face_detections"] += 1
        
        current_time = time.time()

        # Check for suspicious movements
        suspicious_movement = self.detect_suspicious_movement(img)
        if suspicious_movement and (current_time - self.last_warning_time) > 3:
            self.last_warning_time = current_time
            self.should_warn = True
            self.warning_type = "movement"
            self.warning_message = "⚠️ Warning: Excessive movement detected. Please remain still during the test."
            if "warnings_count" in st.session_state:
                st.session_state.warnings_count += 1

        # If multiple faces detected - possible cheating
        if self.multiple_faces and (current_time - self.last_warning_time) > 3:
            self.last_warning_time = current_time
            self.debug_info["multi_face_warnings"] += 1
            self.should_warn = True
            self.warning_type = "multiple_faces"
            self.warning_message = "⚠️ Warning: Multiple faces detected. Only you should be visible during the test."
            if "warnings_count" in st.session_state:
                st.session_state.warnings_count += 1

        # If face is detected
        if self.face_detected:
            # Update Streamlit session state if it exists
            if "last_detection_time" in st.session_state:
                st.session_state.last_detection_time = current_time
            if "looking_away_start" in st.session_state:
                st.session_state.looking_away_start = None

            # Draw rectangle around faces and check for eyes
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                
                # More sensitive eye detection
                eyes = self.eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.05,
                    minNeighbors=2,
                    minSize=(5, 5)
                )
                
                prev_eyes_detected = self.eyes_detected
                self.eyes_detected = len(eyes) > 0
                
                if self.eyes_detected:
                    self.debug_info["eye_detections"] += 1
                
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                
                # If eyes not detected, trigger warning
                if not self.eyes_detected and (current_time - self.last_warning_time) > 2:
                    self.last_warning_time = current_time
                    self.debug_info["warnings_triggered"] += 1
                    
                    # Set direct warning flag
                    self.should_warn = True
                    self.warning_type = "eyes"
                    self.warning_message = "⚠️ Warning: Eyes not detected. Please look at the screen."
                    
                    # Update session state
                    if "warnings_count" in st.session_state:
                        st.session_state.warnings_count += 1
        else:
            # Face not detected - update looking away time
            if "looking_away_start" in st.session_state:
                if st.session_state.looking_away_start is None:
                    st.session_state.looking_away_start = current_time
                # Reduced time threshold for warning (1.5 seconds)
                elif (current_time - st.session_state.looking_away_start) > 1.5 and (current_time - self.last_warning_time) > 2:
                    self.last_warning_time = current_time
                    self.debug_info["warnings_triggered"] += 1
                    
                    # Set direct warning flag
                    self.should_warn = True
                    self.warning_type = "face"
                    self.warning_message = "⚠️ Warning: Face not detected. Please stay in front of the camera."
                    
                    # Update session state
                    if "warnings_count" in st.session_state:
                        st.session_state.warnings_count += 1

        # Check if warnings threshold reached - terminate test
        if "warnings_count" in st.session_state and "test_in_progress" in st.session_state:
            if st.session_state.warnings_count >= 3 and st.session_state.test_in_progress:
                st.session_state.test_in_progress = False
                st.session_state.test_terminated = True
                st.session_state.termination_reason = "Multiple violations of test integrity rules"

        # Add status information to the frame
        status_text = "Status: Face Detected ✓" if self.face_detected else "Status: Face Not Detected ✗"
        cv2.putText(img, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                   (0, 255, 0) if self.face_detected else (0, 0, 255), 2)
        
        eye_status = "Eyes Detected ✓" if self.eyes_detected else "Eyes Not Detected ✗"
        cv2.putText(img, eye_status, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                   (0, 255, 0) if self.eyes_detected else (0, 0, 255), 2)
        
        # Add warning count
        if "warnings_count" in st.session_state:
            warning_color = (0, 255, 0)  # Green for 0 warnings
            if st.session_state.warnings_count == 1:
                warning_color = (0, 255, 255)  # Yellow for 1 warning
            elif st.session_state.warnings_count == 2:
                warning_color = (0, 165, 255)  # Orange for 2 warnings
            elif st.session_state.warnings_count >= 3:
                warning_color = (0, 0, 255)    # Red for 3+ warnings
                
            warnings_text = f"Warnings: {st.session_state.warnings_count}/3"
            cv2.putText(img, warnings_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, warning_color, 2)
        
        # Add debug info
        debug_text = f"Processed: {self.debug_info['frames_processed']} | Warnings: {self.debug_info['warnings_triggered']}"
        cv2.putText(img, debug_text, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return img

    def recv(self, frame):
        # Process video
        if frame.format.name == "video":
            img = self.transform(frame)
            
            # Direct warning mechanism
            if self.should_warn:
                # Apply warning to session state
                if "latest_warning" in st.session_state:
                    st.session_state.latest_warning = self.warning_message
                if "latest_warning_time" in st.session_state:
                    st.session_state.latest_warning_time = time.time()
                if "latest_warning_type" in st.session_state:
                    st.session_state.latest_warning_type = self.warning_type
                    
                self.should_warn = False  # Reset flag
            
            return av.VideoFrame.from_ndarray(img, format="bgr24")
        
        # Process audio
        elif frame.format.name == "audio":
            sound = frame.to_ndarray()
            sound_level = np.abs(sound).max()
            self.noise_detection_window.append(sound_level)
            
            # Keep a rolling window of sound levels
            if len(self.noise_detection_window) > 20:
                self.noise_detection_window.pop(0)
            
            # Check for sustained high audio levels - possible talking
            if len(self.noise_detection_window) > 5:
                current_time = time.time()
                average_level = np.mean(self.noise_detection_window)
                
                if average_level > self.audio_threshold and current_time - self.last_audio_warning_time > 5:
                    self.last_audio_warning_time = current_time
                    self.debug_info["audio_warnings"] += 1
                    
                    if "warnings_count" in st.session_state:
                        st.session_state.warnings_count += 1
                        
                    # Update session state with audio warning
                    if "latest_warning" in st.session_state:
                        st.session_state.latest_warning = "⚠️ Warning: High audio levels detected. Please remain quiet during the test."
                    if "latest_warning_time" in st.session_state:
                        st.session_state.latest_warning_time = time.time()
                    if "latest_warning_type" in st.session_state:
                        st.session_state.latest_warning_type = "audio"
            
            return frame
        
        return frame
# Function to initialize proctoring session state
def init_proctoring_state():
    """Initialize all session state variables needed for proctoring"""
    if "warnings_count" not in st.session_state:
        st.session_state.warnings_count = 0
    if "looking_away_start" not in st.session_state:
        st.session_state.looking_away_start = None
    if "last_detection_time" not in st.session_state:
        st.session_state.last_detection_time = time.time()
    if "latest_warning" not in st.session_state:
        st.session_state.latest_warning = None
    if "latest_warning_time" not in st.session_state:
        st.session_state.latest_warning_time = None
    if "latest_warning_type" not in st.session_state:
        st.session_state.latest_warning_type = None
    if "test_terminated" not in st.session_state:
        st.session_state.test_terminated = False
    if "termination_reason" not in st.session_state:
        st.session_state.termination_reason = None

# Function to display and manage proctoring warnings
def display_proctoring_warnings():
    """Display proctoring warnings and handle test termination"""
    # Create container for warnings
    warning_container = st.empty()
    
    # Display current warning if it exists and is recent (within last 10 seconds)
    current_time = time.time()
    if (st.session_state.latest_warning_time is not None and 
            current_time - st.session_state.latest_warning_time < 10):
        
        warning_type = st.session_state.latest_warning_type
        warning_message = st.session_state.latest_warning
        
        if warning_type == "multiple_faces":
            warning_container.error(warning_message)
        else:
            warning_container.warning(warning_message)
            
        # Also display warning in sidebar for higher visibility
        with st.sidebar:
            if warning_type == "multiple_faces":
                st.error(warning_message)
            else:
                st.warning(warning_message)
    
    # Display warning count prominently
    current_warnings = st.session_state.warnings_count
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if current_warnings > 0:
            st.markdown(f"### ⚠️ Current warnings: {current_warnings}/3")
        else:
            st.markdown(f"### Current warnings: {current_warnings}/3")
    
    with col2:
        if st.button("Reset Warnings"):
            st.session_state.warnings_count = 0
            st.session_state.latest_warning = None
            st.session_state.latest_warning_time = None
            st.session_state.latest_warning_type = None
            st.rerun()
    
    # Use a progress bar to visualize warnings with color coding
    if current_warnings == 0:
        st.progress(current_warnings/3, "Good standing")
    elif current_warnings == 1:
        st.warning("First warning issued")
        st.progress(current_warnings/3)
    elif current_warnings == 2:
        st.warning("⚠️⚠️ Second warning issued! One more warning will terminate the test.")
        st.progress(current_warnings/3)
    elif current_warnings >= 3:
        st.error("❌ Maximum warnings reached")
        st.progress(1.0)
    
    # Handle test termination if too many warnings
    if st.session_state.test_terminated:
        st.error(f"❌ Test terminated: {st.session_state.termination_reason}")
        if st.button("Return to Test Setup"):
            st.session_state.test_in_progress = False
            st.session_state.test_completed = False
            st.session_state.test_terminated = False
            st.session_state.warnings_count = 0
            st.rerun()
# Function to generate questions using OpenAI's API
def generate_questions(topic, num_questions):
    """Generate multiple choice questions on the given topic using ChatGPT API"""
    prompt = f"""Generate a multiple-choice quiz with {num_questions} questions on the topic '{topic}'. 
    Each question should have 4 options labeled A, B, C, D and indicate the correct answer. 
    Format your response as a JSON array of objects with these exact keys:
    - "question": the question text
    - "options": an array of 4 strings representing the options
    - "correct": the correct answer (A, B, C, or D)
    - "explanation": brief explanation of the correct answer
    
    The JSON must be valid and properly formatted."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates quiz questions. Return valid JSON only with no other text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON if it's wrapped in code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        questions_data = json.loads(response_text)
        return questions_data
    
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        st.write("Response received:", response_text if 'response_text' in locals() else "No response")
        return None
# Function to create an interactive OMR sheet
def create_omr_sheet(num_questions, current_answers=None):
    """Create an interactive OMR sheet with the given number of questions"""
    if current_answers is None:
        current_answers = [None] * num_questions
        
    # Create a new image
    width, height = 600, 100 + (num_questions * 50)
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw title
    draw.text((width//2 - 80, 20), "OMR ANSWER SHEET", fill='black')
    draw.line([(50, 50), (width-50, 50)], fill='black', width=2)
    
    # Draw question numbers and option bubbles
    for i in range(num_questions):
        y_pos = 80 + (i * 50)
        # Question number
        draw.text((30, y_pos+5), f"{i+1}.", fill='black')
        
        # Option bubbles
        options = ['A', 'B', 'C', 'D']
        for j, option in enumerate(options):
            x_pos = 80 + (j * 100)
            # Draw option label
            draw.text((x_pos-5, y_pos-15), option, fill='black')
            
            # Draw circle
            radius = 15
            if current_answers[i] == option:
                # Filled circle if selected
                draw.ellipse((x_pos-radius, y_pos-radius, x_pos+radius, y_pos+radius), outline='black', fill='black')
            else:
                # Empty circle if not selected
                draw.ellipse((x_pos-radius, y_pos-radius, x_pos+radius, y_pos+radius), outline='black')
    
    # Convert to bytes for displaying in Streamlit
    buf = BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    
    return byte_im
# Function to evaluate the test and provide feedback
def evaluate_test(questions, student_answers):
    """Evaluate the test and get feedback using ChatGPT"""
    correct_answers = [q["correct"] for q in questions]
    score = sum(1 for i in range(len(correct_answers)) if student_answers[i] == correct_answers[i])
    
    feedback_prompt = f"""Evaluate the following test results:
    
    Questions and correct answers:
    """
    
    for idx, q in enumerate(questions, start=1):
        feedback_prompt += f"Q{idx}: {q['question']}\n"
        feedback_prompt += f"Options: A: {q['options'][0]}, B: {q['options'][1]}, C: {q['options'][2]}, D: {q['options'][3]}\n"
        feedback_prompt += f"Correct Answer: {q['correct']}\n"
        feedback_prompt += f"Student's Answer: {student_answers[idx-1] if idx-1 < len(student_answers) else 'Not answered'}\n\n"
    
    feedback_prompt += f"""
    Student scored {score} out of {len(questions)}.
    
    Please provide:
    1. Overall assessment of the student's performance
    2. Specific feedback on incorrect answers
    3. Areas for improvement
    4. Study recommendations
    
    Use a supportive and constructive tone.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that provides educational feedback and assessment."},
                {"role": "user", "content": feedback_prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        
        feedback = response.choices[0].message.content.strip()
        return {
            "score": score,
            "total": len(questions),
            "percentage": round((score / len(questions)) * 100, 1),
            "feedback": feedback
        }
    except Exception as e:
        st.error(f"Error generating feedback: {str(e)}")
        return {
            "score": score,
            "total": len(questions),
            "percentage": round((score / len(questions)) * 100, 1),
            "feedback": "Error generating detailed feedback."
        }
# Add this function to generate questions from uploaded file content
def generate_questions_from_file(file_content, num_questions):
    """Generate multiple choice questions based on uploaded file content using ChatGPT API"""
    prompt = f"""Based on the following document content, generate a multiple-choice quiz with {num_questions} questions. 
    Each question should have 4 options labeled A, B, C, D and indicate the correct answer. 
    Format your response as a JSON array of objects with these exact keys:
    - "question": the question text
    - "options": an array of 4 strings representing the options
    - "correct": the correct answer (A, B, C, or D)
    - "explanation": brief explanation of the correct answer
    
    The JSON must be valid and properly formatted.
    
    Document Content:
    {file_content}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that generates quiz questions from documents. Return valid JSON only with no other text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON if it's wrapped in code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        questions_data = json.loads(response_text)
        return questions_data
    
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        st.write("Response received:", response_text if 'response_text' in locals() else "No response")
        return None

# Modify the display_live_omr_test function to include file upload
# Modify the display_live_omr_test function to better handle termination
def display_live_omr_test():
    # Add at the beginning of display_live_omr_test function
    st.title("📝 Interactive Live OMR Test with AI Proctoring")

    # Auto-refresh mechanism
    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = time.time()

    current_time = time.time()
    # Force a rerun every 3 seconds to check for new warnings
    if current_time - st.session_state.last_refresh_time > 3:
        st.session_state.last_refresh_time = current_time
        try:
            st.experimental_rerun()  # Use experimental_rerun for compatibility
        except:
            # Fallback to rerun if available
            if hasattr(st, 'rerun'):
                st.rerun()
   
    # Initialize proctoring state
    init_proctoring_state()
    
    # Create a placeholder for warnings
    warning_placeholder = st.empty()
    
    # Set up layout for test and proctoring
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📹 Proctoring Camera")
        
        # WebRTC configuration for proctoring with improved settings
        rtc_configuration = RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        )
        
        # Start webcam with enhanced processor and better configuration
        try:
            webrtc_ctx = webrtc_streamer(
                key="enhanced_proctoring",
                video_processor_factory=EnhancedVideoProcessor,
                rtc_configuration=rtc_configuration,
                media_stream_constraints={
                    "video": True,
                    "audio": True
                },
                async_processing=True,
                video_html_attrs={
                    "style": {"width": "100%", "height": "auto", "margin": "0 auto"},
                    "controls": False,
                    "autoPlay": True,
                },
            )
        except Exception as e:
            st.error(f"Error initializing webcam: {str(e)}")
            webrtc_ctx = None
        
        # Check if camera is connected before showing proctoring
        if webrtc_ctx and webrtc_ctx.state and webrtc_ctx.state.playing:
            # Display proctoring warnings and status
            display_proctoring_warnings()
            
            # Add a debug section only visible with a toggle
            with st.expander("Debug Information (Click to expand)"):
                st.write(f"Face detected: {getattr(webrtc_ctx.video_processor, 'face_detected', 'N/A') if webrtc_ctx and webrtc_ctx.video_processor else 'No webcam'}")
                st.write(f"Eyes detected: {getattr(webrtc_ctx.video_processor, 'eyes_detected', 'N/A') if webrtc_ctx and webrtc_ctx.video_processor else 'No webcam'}")
                st.write(f"Multiple faces: {getattr(webrtc_ctx.video_processor, 'multiple_faces', 'N/A') if webrtc_ctx and webrtc_ctx.video_processor else 'No webcam'}")
                st.write(f"Warning count: {st.session_state.warnings_count}")
                st.write(f"Latest warning: {st.session_state.latest_warning}")
                st.write(f"Warning time: {st.session_state.latest_warning_time}")
                st.write(f"Warning type: {st.session_state.latest_warning_type}")
            
                # Add a manual warning button for testing
                if st.button("Trigger Test Warning"):
                    st.session_state.warnings_count += 1
                    st.session_state.latest_warning = "This is a test warning"
                    st.session_state.latest_warning_time = time.time()
                    st.session_state.latest_warning_type = "test"
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
        else:
            st.warning("⚠️ Camera not connected. Please ensure your camera is working and you've granted browser permissions.")
            st.info("If you're having trouble connecting, try refreshing the page or using a different browser.")
            
            # Add alternative capture method
            if st.button("Use Alternative Camera Method"):
                st.session_state.use_alternative_camera = True
                try:
                    st.experimental_rerun()
                except:
                    if hasattr(st, 'rerun'):
                        st.rerun()
                
            if st.session_state.get("use_alternative_camera", False):
                st.success("Using alternative camera method")
                # Create a placeholder with simulated camera feed
                img = Image.new('RGB', (640, 480), color='white')
                draw = ImageDraw.Draw(img)
                draw.text((320, 240), "Camera Simulation Active", fill='black')
                st.image(img, channels="RGB", use_container_width=True)
                
                # Add test warning controls for the alternative mode
                if st.button("Simulate Warning"):
                    st.session_state.warnings_count = min(st.session_state.warnings_count + 1, 3)
                    st.session_state.latest_warning = "Simulated Warning"
                    st.session_state.latest_warning_time = time.time()
                    st.session_state.latest_warning_type = "test" 
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
        
        # Proctoring rules
        st.caption("📝 Proctoring Rules:")
        st.caption("1. Keep your face visible at all times")
        st.caption("2. Look at the screen (eyes must be visible)")
        st.caption("3. No other people in frame")
        st.caption("4. Remain quiet during the test")
        st.caption("5. Avoid excessive movement")
        st.caption("6. Three warnings will terminate and restart the test")
    
    # NEW HANDLING: Check for automatic restart countdown
    if "restart_countdown" in st.session_state:
        # If we're in restart countdown mode, just show the countdown and don't proceed with the rest of the function
        remaining = max(0, st.session_state.restart_countdown - int(time.time() - st.session_state.restart_time))
        if remaining <= 0:
            # If countdown is done, clear test termination status and restart
            st.session_state.test_terminated = False
            if "restart_countdown" in st.session_state:
                del st.session_state.restart_countdown
            if "restart_time" in st.session_state:
                del st.session_state.restart_time
            st.session_state.warnings_count = 0
            st.rerun()
        return  # Exit the function to avoid showing test content during countdown
        
    # If test is terminated, don't show test content
    if st.session_state.test_terminated:
        return
        
    # Step 1: Configure the test if not already in progress
    if not st.session_state.test_in_progress and not st.session_state.test_completed:
        with col2:
            st.header("Configure Your Test")
            
            # Student selection
            student_id = st.selectbox("Select your Student ID", list(students_data.keys()))
            st.write(f"Student Name: {students_data[student_id]['name']}")
            st.session_state.current_student_id = student_id
            st.session_state.current_student_name = students_data[student_id]["name"]
            
            # NEW: Add file upload for generating questions
            st.subheader("Upload Content for Questions")
            uploaded_file = st.file_uploader("Upload a file (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
            
            file_content = None
            if uploaded_file is not None:
                st.success(f"File uploaded: {uploaded_file.name}")
                
                # Extract text from different file types
                try:
                    if uploaded_file.name.endswith('.txt'):
                        file_content = uploaded_file.read().decode('utf-8')
                    elif uploaded_file.name.endswith('.pdf'):
                        file_content = extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.name.endswith('.docx'):
                        file_content = extract_text_from_docx(uploaded_file)
                    
                    # Show preview of extracted content
                    with st.expander("Content Preview"):
                        st.write(file_content[:500] + "..." if len(file_content) > 500 else file_content)
                except Exception as e:
                    st.error(f"Error extracting content from file: {str(e)}")
            
            # Allow backup topic entry if no file is uploaded
            if not file_content:
                test_topic = st.text_input("Enter test topic (if no file uploaded):", "Computer Science Fundamentals")
                st.session_state.current_test_topic = test_topic
            
            num_questions = st.number_input("Number of questions:", min_value=1, max_value=20, value=5)
            
            # Global secure OpenAI key setting
            openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable in production!
            
            # Add a camera check before starting the test
            st.subheader("Camera & Microphone Check")
            st.write("Please ensure your camera and microphone are working correctly.")
            
            # Check if webcam is active and running or we're using alternative mode
            camera_ready = (webrtc_ctx and webrtc_ctx.state and webrtc_ctx.state.playing) or st.session_state.get("use_alternative_camera", False)
            
            if camera_ready:
                st.success("✅ Camera and microphone are working!")
                
                # Start test button
                if st.button("Start Test"):
                    with st.spinner("Generating test questions..."):
                        if file_content:
                            # Generate questions from file content
                            questions = generate_questions_from_file(file_content, num_questions)
                        else:
                            # Fallback to topic-based question generation
                            questions = generate_questions(test_topic, num_questions)
                    
                    if questions:
                        st.session_state.live_omr_questions = questions
                        st.session_state.student_answers = [None] * len(questions)
                        st.session_state.current_question_index = 0
                        st.session_state.warnings_count = 0  # Reset warnings
                        st.session_state.test_in_progress = True
                        st.session_state.test_completed = False
                        st.session_state.test_terminated = False
                        try:
                            st.experimental_rerun()
                        except:
                            if hasattr(st, 'rerun'):
                                st.rerun()
                    else:
                        st.error("Failed to generate questions. Please try again.")
            else:
                st.error("⚠️ Camera access is required. Please allow camera access and try again.")
                
    # Step 2: Display the proctored test
    elif st.session_state.test_in_progress:
        with col2:
            st.header("🔍 OMR Test in Progress")
            
            if st.session_state.live_omr_questions:
                current_q = st.session_state.live_omr_questions[st.session_state.current_question_index]
                st.subheader(f"Question {st.session_state.current_question_index + 1} of {len(st.session_state.live_omr_questions)}")
                st.write(current_q["question"])
                
                # Display options
                for i, option in enumerate(['A', 'B', 'C', 'D']):
                    st.write(f"{option}: {current_q['options'][i]}")
            
            # Display interactive OMR sheet
            st.subheader("📑 Answer Sheet")
            st.caption("Select your answer below")
            
            # Create OMR sheet image
            omr_image = create_omr_sheet(len(st.session_state.live_omr_questions), st.session_state.student_answers)
            
            # Display the image
            omr_placeholder = st.empty()
            omr_placeholder.image(omr_image, use_container_width=True)
            
            # Handle test navigation and answers
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            
            with nav_col1:
                if st.button("⬅️ Previous") and st.session_state.current_question_index > 0:
                    st.session_state.current_question_index -= 1
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
            
            with nav_col2:
                # Allow selecting answer via buttons
                selected_option = st.selectbox(
                    "Select answer:", 
                    [None, 'A', 'B', 'C', 'D'], 
                    index=0 if st.session_state.student_answers[st.session_state.current_question_index] is None else 
                         ['A', 'B', 'C', 'D'].index(st.session_state.student_answers[st.session_state.current_question_index]) + 1
                )
                
                if selected_option:
                    st.session_state.student_answers[st.session_state.current_question_index] = selected_option
                    # Update the OMR sheet
                    omr_image = create_omr_sheet(len(st.session_state.live_omr_questions), st.session_state.student_answers)
                    omr_placeholder.image(omr_image, use_container_width=True)
            
            with nav_col3:
                if st.button("Next ➡️") and st.session_state.current_question_index < len(st.session_state.live_omr_questions) - 1:
                    st.session_state.current_question_index += 1
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
            
            # Submit button
            st.markdown("---")
            if st.button("📝 Submit Test", use_container_width=True):
                # Check if all questions have been answered
                if None in st.session_state.student_answers:
                    st.warning("Please answer all questions before submitting.")
                else:
                    st.session_state.test_in_progress = False
                    st.session_state.test_completed = True
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
    
    # Step 3: Show test results and feedback
    elif st.session_state.test_completed:
        with col2:
            st.header("📊 Test Results")
            
            # Display final OMR sheet
            st.subheader("Your Completed OMR Sheet")
            final_omr = create_omr_sheet(len(st.session_state.live_omr_questions), st.session_state.student_answers)
            st.image(final_omr, use_container_width=True)
            
            # Evaluate the test
            with st.spinner("Evaluating your test..."):
                evaluation = evaluate_test(st.session_state.live_omr_questions, st.session_state.student_answers)
            
            # Display score
            st.subheader(f"Your Score: {evaluation['score']}/{evaluation['total']} ({evaluation['percentage']}%)")
            
            # Display progress bar
            score_percent = evaluation['percentage'] / 100
            st.progress(score_percent)
            
            # Add celebrations for good scores
            if score_percent >= 0.8:
                st.balloons()
                st.success("🎉 Excellent job!")
            elif score_percent >= 0.6:
                st.success("👍 Good work!")
            else:
                st.info("📚 Keep practicing!")
            
            # Display detailed feedback
            with st.expander("Detailed Feedback", expanded=True):
                st.write(evaluation['feedback'])
            
            # Question-by-question review
            st.subheader("Question-by-Question Review")
            for i, question in enumerate(st.session_state.live_omr_questions):
                correct = st.session_state.student_answers[i] == question['correct']
                expander_title = f"Q{i+1}: {'✅ Correct' if correct else '❌ Incorrect'}"
                with st.expander(expander_title):
                    st.write(f"**Question:** {question['question']}")
                    st.write(f"**Your answer:** {st.session_state.student_answers[i]} - {question['options'][ord(st.session_state.student_answers[i]) - ord('A')]}")
                    st.write(f"**Correct answer:** {question['correct']} - {question['options'][ord(question['correct']) - ord('A')]}")
                    st.write(f"**Explanation:** {question['explanation']}")
            
            # Start a new test button
            if st.button("Start a New Test", use_container_width=True):
                st.session_state.test_in_progress = False
                st.session_state.test_completed = False
                st.session_state.test_terminated = False
                st.session_state.live_omr_questions = None
                st.session_state.student_answers = []
                st.session_state.current_question_index = 0
                st.session_state.warnings_count = 0
                try:
                    st.experimental_rerun()
                except:
                    if hasattr(st, 'rerun'):
                        st.rerun()
                    else:
                        st.error("Failed to generate questions. Please try again.")
            else:
                st.error("⚠️ Camera access is required. Please allow camera access and try again.")
                
    # Step 2: Display the proctored test
    elif st.session_state.test_in_progress:
        with col2:
            st.header("🔍 OMR Test in Progress")
            
            if st.session_state.live_omr_questions:
                current_q = st.session_state.live_omr_questions[st.session_state.current_question_index]
                st.subheader(f"Question {st.session_state.current_question_index + 1} of {len(st.session_state.live_omr_questions)}")
                st.write(current_q["question"])
                
                # Display options
                for i, option in enumerate(['A', 'B', 'C', 'D']):
                    st.write(f"{option}: {current_q['options'][i]}")
            
            # Display interactive OMR sheet
            st.subheader("📑 Answer Sheet")
            st.caption("Select your answer below")
            
            # Create OMR sheet image
            omr_image = create_omr_sheet(len(st.session_state.live_omr_questions), st.session_state.student_answers)
            
            # Display the image
            omr_placeholder = st.empty()
            omr_placeholder.image(omr_image, use_container_width=True)
            
            # Handle test navigation and answers
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            
            with nav_col1:
                if st.button("⬅️ Previous") and st.session_state.current_question_index > 0:
                    st.session_state.current_question_index -= 1
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
            
            with nav_col2:
                # Allow selecting answer via buttons
                selected_option = st.selectbox(
                    "Select answer:", 
                    [None, 'A', 'B', 'C', 'D'], 
                    index=0 if st.session_state.student_answers[st.session_state.current_question_index] is None else 
                         ['A', 'B', 'C', 'D'].index(st.session_state.student_answers[st.session_state.current_question_index]) + 1
                )
                
                if selected_option:
                    st.session_state.student_answers[st.session_state.current_question_index] = selected_option
                    # Update the OMR sheet
                    omr_image = create_omr_sheet(len(st.session_state.live_omr_questions), st.session_state.student_answers)
                    omr_placeholder.image(omr_image, use_container_width=True)
            
            with nav_col3:
                if st.button("Next ➡️") and st.session_state.current_question_index < len(st.session_state.live_omr_questions) - 1:
                    st.session_state.current_question_index += 1
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
            
            # Submit button
            st.markdown("---")
            if st.button("📝 Submit Test", use_container_width=True):
                # Check if all questions have been answered
                if None in st.session_state.student_answers:
                    st.warning("Please answer all questions before submitting.")
                else:
                    st.session_state.test_in_progress = False
                    st.session_state.test_completed = True
                    try:
                        st.experimental_rerun()
                    except:
                        if hasattr(st, 'rerun'):
                            st.rerun()
    
    # Step 3: Show test results and feedback
    elif st.session_state.test_completed:
        with col2:
            st.header("📊 Test Results")
            
            # Display final OMR sheet
            st.subheader("Your Completed OMR Sheet")
            final_omr = create_omr_sheet(len(st.session_state.live_omr_questions), st.session_state.student_answers)
            st.image(final_omr, use_container_width=True)
            
            # Evaluate the test
            with st.spinner("Evaluating your test..."):
                evaluation = evaluate_test(st.session_state.live_omr_questions, st.session_state.student_answers)
            
            # Display score
            st.subheader(f"Your Score: {evaluation['score']}/{evaluation['total']} ({evaluation['percentage']}%)")
            
            # Display progress bar
            score_percent = evaluation['percentage'] / 100
            st.progress(score_percent)
            
            # Add celebrations for good scores
            if score_percent >= 0.8:
                st.balloons()
                st.success("🎉 Excellent job!")
            elif score_percent >= 0.6:
                st.success("👍 Good work!")
            else:
                st.info("📚 Keep practicing!")
            
            # Display detailed feedback
            with st.expander("Detailed Feedback", expanded=True):
                st.write(evaluation['feedback'])
            
            # Question-by-question review
            st.subheader("Question-by-Question Review")
            for i, question in enumerate(st.session_state.live_omr_questions):
                correct = st.session_state.student_answers[i] == question['correct']
                expander_title = f"Q{i+1}: {'✅ Correct' if correct else '❌ Incorrect'}"
                with st.expander(expander_title):
                    st.write(f"**Question:** {question['question']}")
                    st.write(f"**Your answer:** {st.session_state.student_answers[i]} - {question['options'][ord(st.session_state.student_answers[i]) - ord('A')]}")
                    st.write(f"**Correct answer:** {question['correct']} - {question['options'][ord(question['correct']) - ord('A')]}")
                    st.write(f"**Explanation:** {question['explanation']}")
            
            # Start a new test button
            if st.button("Start a New Test", use_container_width=True):
                st.session_state.test_in_progress = False
                st.session_state.test_completed = False
                st.session_state.test_terminated = False
                st.session_state.live_omr_questions = None
                st.session_state.student_answers = []
                st.session_state.current_question_index = 0
                st.session_state.warnings_count = 0
                try:
                    st.experimental_rerun()
                except:
                    if hasattr(st, 'rerun'):
                        st.rerun()

def display_ai_learning_analytics():
    st.header("🎯 Advanced AI Learning Analytics & Optimization")
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Individual Analytics", 
        "Study Group Matcher", 
        "Class Insights",
        "Learning Path Prediction",
        "Cognitive Analysis"
    ])
    
    # Tab 1: Individual Analytics (Enhanced)
    with tab1:
        st.subheader("📊 Individual Performance Analytics")
        
        # Student selection
        student_id = st.selectbox("Select Student for Analysis", list(students_data.keys()), key="individual_student")
        student = students_data[student_id]
        
        # Create subtabs for detailed analysis
        subtab1, subtab2, subtab3 = st.tabs(["Performance Overview", "Skills Analysis", "Time Tracking"])
        
        # Performance Overview
        with subtab1:
            # Performance metrics
            prof_data = student.get("proficiency", {})
            if prof_data:
                # Create performance chart
                fig, ax = plt.subplots(figsize=(10, 6))
                
                for topic, levels in prof_data.items():
                    bloom_levels = sorted(levels.keys())
                    scores = [levels[l] for l in bloom_levels]
                    ax.plot(bloom_levels, scores, marker='o', label=topic)
                
                ax.set_xlabel("Bloom's Taxonomy Level")
                ax.set_ylabel("Proficiency Score")
                ax.set_title(f"Learning Progress - {student['name']}")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                
                # Calculate overall proficiency
                all_scores = []
                for topic, levels in prof_data.items():
                    all_scores.extend(levels.values())
                overall_score = sum(all_scores) / len(all_scores) if all_scores else 0
                
                # Display score with gauge
                st.subheader("Overall Proficiency")
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    progress_color = "green" if overall_score >= 0.7 else "orange" if overall_score >= 0.5 else "red"
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="margin: 0 auto; width: 150px; height: 150px; border-radius: 50%; background: conic-gradient({progress_color} {overall_score*360}deg, #f0f0f0 0deg); position: relative;">
                            <div style="position: absolute; top: 25px; left: 25px; width: 100px; height: 100px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold;">
                                {overall_score:.0%}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Get quiz history
            history_df = get_student_quiz_history(student_id)
            
            if not history_df.empty:
                # Performance trend over time
                st.subheader("Performance Trend")
                history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                history_df = history_df.sort_values('timestamp')
                
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(history_df['timestamp'], history_df['percentage'], marker='o', linestyle='-')
                ax.set_xlabel("Date")
                ax.set_ylabel("Score (%)")
                ax.set_title("Quiz Performance Over Time")
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                st.pyplot(fig)
        
        # Skills Analysis
        with subtab2:
            if 'history_df' in locals() and not history_df.empty:
                # Radar chart for skills
                st.subheader("Skills Radar")
                topic_performance = history_df.groupby('topic')['percentage'].mean()
                
                topics = list(topic_performance.index)
                scores = list(topic_performance.values)
                
                if topics:  # Only proceed if there are topics to analyze
                    # Add the first value again to close the circle
                    topics.append(topics[0])
                    scores.append(scores[0])
                    
                    # Convert to radians
                    angles = np.linspace(0, 2*np.pi, len(topics)-1, endpoint=False).tolist()
                    angles += angles[:1]  # Close the circle
                    
                    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
                    ax.plot(angles, [s/100 for s in scores], 'o-', linewidth=2)
                    ax.fill(angles, [s/100 for s in scores], alpha=0.25)
                    ax.set_thetagrids(np.degrees(angles[:-1]), topics[:-1])
                    ax.set_ylim(0, 1)
                    ax.set_title("Skills Assessment")
                    st.pyplot(fig)
                    
                    # Strengths and weaknesses analysis
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.success("💪 Strengths")
                        strengths = topic_performance[topic_performance >= 70].index.tolist()
                        for topic in strengths:
                            st.write(f"- {topic}: {topic_performance[topic]:.1f}%")
                    
                    with col2:
                        st.error("📚 Areas for Improvement")
                        weaknesses = topic_performance[topic_performance < 50].index.tolist()
                        for topic in weaknesses:
                            st.write(f"- {topic}: {topic_performance[topic]:.1f}%")
                            
                    # Skills gap analysis
                    st.subheader("Skills Gap Analysis")
                    
                    # Calculate ideal proficiency and current gap
                    ideal_score = 85  # Target score
                    gaps = {topic: max(0, ideal_score - score) for topic, score in topic_performance.items()}
                    
                    # Sort gaps by size (largest first)
                    sorted_gaps = dict(sorted(gaps.items(), key=lambda x: x[1], reverse=True))
                    
                    # Create gap chart
                    fig, ax = plt.subplots(figsize=(10, 5))
                    topics = list(sorted_gaps.keys())
                    gap_values = list(sorted_gaps.values())
                    
                    # Color bars based on gap size
                    colors = ['red' if gap > 30 else 'orange' if gap > 15 else 'green' for gap in gap_values]
                    
                    bars = ax.barh(topics, gap_values, color=colors)
                    ax.set_xlabel("Proficiency Gap (%)")
                    ax.set_title("Skills Gap Analysis")
                    ax.invert_yaxis()  # Display largest gap at the top
                    
                    # Add labels
                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center')
                    
                    st.pyplot(fig)
                else:
                    st.info("No topic data available for skills analysis.")
            else:
                st.info("No quiz history available for skills analysis.")
        
        # Time Tracking
        with subtab3:
            st.subheader("Learning Time Analysis")
            
            # Generate sample time tracking data (replace with real data when available)
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            hours_spent = [2.5, 1.0, 3.0, 2.0, 1.5, 4.0, 3.5]  # Sample data
            
            # Create time tracking chart
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.bar(days, hours_spent, color='skyblue')
            ax.set_xlabel("Day of Week")
            ax.set_ylabel("Hours Spent")
            ax.set_title("Weekly Study Pattern")
            
            # Add labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height}h', ha='center')
            
            st.pyplot(fig)
            
            # Study time statistics
            total_hours = sum(hours_spent)
            avg_daily = total_hours / 7
            most_productive = days[hours_spent.index(max(hours_spent))]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Weekly Hours", f"{total_hours}h")
            with col2:
                st.metric("Daily Average", f"{avg_daily:.1f}h")
            with col3:
                st.metric("Most Productive Day", most_productive)
        
        # AI Recommendations
        st.subheader("AI-Generated Learning Recommendations")
        if st.button("Generate Personalized Recommendations", key="individual_rec"):
            with st.spinner("Analyzing performance data..."):
                # Initialize local variables if they don't exist
                if 'history_df' not in locals():
                    history_df = pd.DataFrame()  # Empty DataFrame
                if 'strengths' not in locals():
                    strengths = []
                if 'weaknesses' not in locals():
                    weaknesses = []
                
                # Prepare data for AI analysis
                student_data = {
                    "name": student['name'],
                    "proficiency": student.get("proficiency", {}),
                    "quiz_history": history_df.to_dict() if not history_df.empty else None,
                    "strengths": strengths,
                    "weaknesses": weaknesses
                }
                
                prompt = f"""
                Analyze this student's performance data and provide personalized recommendations:
                
                Student Data: {json.dumps(student_data, indent=2)}
                
                Provide:
                1. Top 3 specific areas to focus on
                2. Recommended learning resources for each area
                3. Study strategies based on performance patterns
                4. Time management suggestions
                5. Learning milestones and goals (next 2 weeks)
                
                Format as actionable, encouraging advice.
                """
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an educational advisor providing personalized learning recommendations."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=800
                    )
                    
                    recommendations = response.choices[0].message.content.strip()
                    st.markdown(recommendations)
                    
                    # Add download button for recommendations
                    st.download_button(
                        label="📥 Download Recommendations",
                        data=recommendations,
                        file_name=f"{student['name']}_recommendations.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating recommendations: {str(e)}")
                    st.markdown("""
                    ### Personalized Learning Recommendations

                    #### 1. Areas to Focus On
                    - **Fuzzy Logic Fundamentals**: Strengthen your understanding of the core concepts
                    - **Data Science Applications**: Practice applying theoretical knowledge to real problems
                    - **Advanced Bloom's Taxonomy Skills**: Work on analysis and evaluation skills

                    #### 2. Recommended Learning Resources
                    - **For Fuzzy Logic**: "Fuzzy Logic with Engineering Applications" by Timothy J. Ross
                    - **For Data Science**: Kaggle competitions and DataCamp courses
                    - **For Advanced Skills**: Peer study groups and project-based learning activities

                    #### 3. Study Strategies
                    - Use visual learning tools like diagrams and mind maps
                    - Implement spaced repetition for better retention
                    - Try explaining concepts to others to solidify understanding

                    #### 4. Time Management
                    - Dedicate 2-3 focused hours per topic each week
                    - Break study sessions into 25-minute intervals with 5-minute breaks
                    - Review material on Saturdays when you appear most productive

                    #### 5. Learning Milestones
                    - Week 1: Complete foundational topics in both subjects
                    - Week 2: Successfully complete a small project applying your knowledge
                    """)
    
    # Tab 2: Study Group Matcher
    with tab2:
        st.subheader("🤝 AI-Powered Study Group Formation")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            group_size = st.slider("Group Size", 2, 5, 3)
            group_count = max(1, len(students_data) // group_size)
        
        with col2:
            matching_strategy = st.radio(
                "Matching Strategy",
                ["Complementary Skills", "Similar Proficiency", "Mixed Abilities"]
            )
        
        # Generate groups
        if st.button("Generate Optimal Study Groups", key="group_gen"):
            with st.spinner("Creating optimal study groups..."):
                # Generate groups using AI
                prompt = f"""
                Create {group_count} study groups from these students.
                Use the "{matching_strategy}" strategy with groups of {group_size} students.
                
                Students data: {json.dumps(students_data, indent=2)}
                
                Return JSON format:
                {{
                    "groups": [
                        {{
                            "group_name": "Group 1",
                            "members": ["SEEE001", "SEEE002"],
                            "focus_topics": ["Topic1", "Topic2"],
                            "study_plan": "Detailed study plan",
                            "rationale": "Why these students work well together",
                            "meeting_schedule": "Suggested meeting times"
                        }}
                    ]
                }}
                """
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You create optimal study groups based on student data."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    response_text = response.choices[0].message.content.strip()
                    if "```json" in response_text:
                        response_text = response_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in response_text:
                        response_text = response_text.split("```")[1].split("```")[0].strip()
                    
                    groups_data = json.loads(response_text)
                    
                    # Display groups
                    for i, group in enumerate(groups_data["groups"]):
                        with st.expander(f"📚 {group['group_name']}", expanded=True):
                            # Group header with student images (placeholder)
                            st.markdown(f"### {group['group_name']}")
                            member_cols = st.columns(len(group["members"]))
                            
                            for j, member_id in enumerate(group["members"]):
                                if member_id in students_data:
                                    with member_cols[j]:
                                        st.markdown(f"""
                                        <div style="text-align: center;">
                                            <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #4CAF50; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 20px;">
                                                {students_data[member_id]['name'][0]}
                                            </div>
                                            <p>{students_data[member_id]['name']}</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            # Group rationale
                            st.info(f"**Why this group works:** {group.get('rationale', 'Complementary skills and learning styles')}")
                            
                            # Group details
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("#### 🎯 Focus Topics")
                                for topic in group["focus_topics"]:
                                    st.markdown(f"- {topic}")
                                
                                st.markdown("#### 📅 Suggested Schedule")
                                st.markdown(group.get("meeting_schedule", "Weekly meetings on Monday and Thursday"))
                            
                            with col2:
                                st.markdown("#### 📝 Recommended Study Plan")
                                st.markdown(group["study_plan"])
                            
                            # Action buttons with error handling
                            if st.button("Create Study Room", key=f"room_{i}"):
                                try:
                                    # This would be where the actual room creation code goes
                                    st.success("Virtual study room created! (Placeholder functionality)")
                                except Exception as e:
                                    st.error(f"Error creating study room: {str(e)}")
                                    st.info("This is a placeholder feature. In a real deployment, this would create an actual virtual study room.")
                            
                            if st.button("Generate Study Materials", key=f"materials_{i}"):
                                with st.spinner("Generating study materials..."):
                                    # Generate sample study materials
                                    topic_prompt = f"Create a brief study guide for {', '.join(group['focus_topics'])}."
                                    try:
                                        materials_response = openai.ChatCompletion.create(
                                            model="gpt-4",
                                            messages=[
                                                {"role": "system", "content": "You create educational study materials."},
                                                {"role": "user", "content": topic_prompt}
                                            ],
                                            temperature=0.7,
                                            max_tokens=400
                                        )
                                        
                                        study_materials = materials_response.choices[0].message.content.strip()
                                        st.markdown(study_materials)
                                    except Exception as e:
                                        st.error(f"Error generating materials: {str(e)}")
                                        st.markdown("""
                                        # Sample Study Guide
                                        
                                        ## Key Concepts
                                        - Basic principles of Fuzzy Logic and Data Science
                                        - Important formulas and theories related to the topics
                                        - Practical applications and examples
                                        
                                        ## Study Approach
                                        - Begin with fundamental concepts
                                        - Practice with real-world examples
                                        - Use collaborative learning techniques
                                        
                                        ## Resources
                                        - Recommended textbooks and online courses
                                        - Practice problems and exercises
                                        - Interactive learning tools
                                        """)
                
                except Exception as e:
                    st.error(f"Error generating study groups: {str(e)}")
                    # Provide fallback content
                    st.markdown("### Sample Study Group")
                    
                    # Create placeholder group data
                    sample_group = {
                        "group_name": "Group 1",
                        "members": ["SEEE001", "SEEE002"],
                        "focus_topics": ["Fuzzy Logic", "Data Science"],
                        "study_plan": "Meet twice weekly to review concepts and practice problems. Focus on foundational understanding before advanced applications.",
                        "rationale": "Members have complementary skills with one strong in Fuzzy Logic and the other in Data Science.",
                        "meeting_schedule": "Mondays and Thursdays after class"
                    }
                    
                    with st.expander(f"📚 {sample_group['group_name']}", expanded=True):
                        # Display sample group
                        st.markdown(f"### {sample_group['group_name']}")
                        st.info(f"**Why this group works:** {sample_group['rationale']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### 🎯 Focus Topics")
                            for topic in sample_group["focus_topics"]:
                                st.markdown(f"- {topic}")
                            
                            st.markdown("#### 📅 Suggested Schedule")
                            st.markdown(sample_group["meeting_schedule"])
                        
                        with col2:
                            st.markdown("#### 📝 Recommended Study Plan")
                            st.markdown(sample_group["study_plan"])
                        
                        # Placeholder buttons
                        if st.button("Create Study Room", key="room_sample"):
                            st.success("Virtual study room created! (Placeholder functionality)")
                        
                        if st.button("Generate Study Materials", key="materials_sample"):
                            st.markdown("""
                            # Sample Study Guide
                            
                            ## Key Concepts
                            - Basic principles of Fuzzy Logic and Data Science
                            - Important formulas and theories related to the topics
                            - Practical applications and examples
                            
                            ## Study Approach
                            - Begin with fundamental concepts
                            - Practice with real-world examples
                            - Use collaborative learning techniques
                            
                            ## Resources
                            - Recommended textbooks and online courses
                            - Practice problems and exercises
                            - Interactive learning tools
                            """)
    
    # Tab 3: Class Insights
    with tab3:
        st.subheader("📈 Class-wide Analytics Dashboard")
        
        # Overall class performance
        all_scores = []
        topic_averages = {}
        
        for student_id in students_data:
            history_df = get_student_quiz_history(student_id)
            if not history_df.empty:
                all_scores.extend(history_df['percentage'].tolist())
                
                for topic in history_df['topic'].unique():
                    if topic not in topic_averages:
                        topic_averages[topic] = []
                    topic_averages[topic].extend(history_df[history_df['topic'] == topic]['percentage'].tolist())
        
        if all_scores:
            # Class statistics
            class_average = sum(all_scores) / len(all_scores)
            median_score = sorted(all_scores)[len(all_scores)//2]
            top_score = max(all_scores)
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Class Average", f"{class_average:.1f}%")
            with col2:
                st.metric("Median Score", f"{median_score:.1f}%")
            with col3:
                st.metric("Top Score", f"{top_score:.1f}%")
            with col4:
                st.metric("Total Assessments", len(all_scores))
            
            # Class distribution
            st.subheader("Grade Distribution")
            
            # Create histogram
            fig, ax = plt.subplots(figsize=(10, 5))
            
            bins = [0, 50, 60, 70, 80, 90, 100]
            bin_labels = ['F', 'D', 'C', 'B', 'A', 'A+']
            
            counts, edges, bars = ax.hist(all_scores, bins=bins, edgecolor='black')
            
            # Add annotations above bars
            for i in range(len(counts)):
                ax.text(edges[i] + (edges[i+1] - edges[i])/2, counts[i] + 0.1, 
                       f'{int(counts[i])}', ha='center')
                
                # Add grade labels
                ax.text(edges[i] + (edges[i+1] - edges[i])/2, -0.5, 
                       bin_labels[i], ha='center')
            
            ax.set_xlabel("Score Range")
            ax.set_ylabel("Number of Students")
            ax.set_title("Class Score Distribution")
            ax.set_xticks([])  # Remove x-ticks as we've added our own labels
            
            st.pyplot(fig)
            
            # Topic performance chart
            if topic_averages:
                st.subheader("Performance by Topic")
                
                fig, ax = plt.subplots(figsize=(10, 6))
                topics = list(topic_averages.keys())
                averages = [sum(scores)/len(scores) for scores in topic_averages.values()]
                
                # Sort by average score
                sorted_data = sorted(zip(topics, averages), key=lambda x: x[1])
                sorted_topics, sorted_averages = zip(*sorted_data)
                
                bars = ax.barh(sorted_topics, sorted_averages, 
                               color=['green' if avg >= 70 else 'orange' if avg >= 50 else 'red' for avg in sorted_averages])
                ax.set_xlabel("Average Score (%)")
                ax.set_title("Class Performance by Topic")
                
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center')
                
                st.pyplot(fig)
            
            # AI Class Insights
            if st.button("Generate Class Insights", key="class_insights"):
                with st.spinner("Analyzing class data..."):
                    class_data = {
                        "class_size": len(students_data),
                        "average_score": class_average,
                        "median_score": median_score,
                        "top_score": top_score,
                        "topic_averages": {topic: sum(scores)/len(scores) for topic, scores in topic_averages.items()},
                        "grade_distribution": {
                            "A+": sum(1 for score in all_scores if score >= 90),
                            "A": sum(1 for score in all_scores if 80 <= score < 90),
                            "B": sum(1 for score in all_scores if 70 <= score < 80),
                            "C": sum(1 for score in all_scores if 60 <= score < 70),
                            "D": sum(1 for score in all_scores if 50 <= score < 60),
                            "F": sum(1 for score in all_scores if score < 50)
                        }
                    }
                    
                    prompt = f"""
                    Analyze this class data and provide:
                    1. Overall class performance assessment
                    2. Topics that need more attention class-wide
                    3. Recommended class-wide interventions
                    4. Teaching strategies based on grade distribution
                    5. Suggested differentiation approaches for varied performance levels
                    
                    Class Data: {json.dumps(class_data, indent=2)}
                    """
                    
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are an educational analyst providing class-wide insights."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=800
                        )
                        
                        insights = response.choices[0].message.content.strip()
                        st.markdown(insights)
                        
                        # Add download button for insights
                        st.download_button(
                            label="📥 Download Class Insights",
                            data=insights,
                            file_name=f"class_insights.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"Error generating insights: {str(e)}")
                        # Provide fallback content
                        st.markdown("""
                        ## Class Performance Assessment

                        ### 1. Overall Performance
                        The class shows moderate performance with an average score in the C range. There's a wide distribution of grades, indicating varied mastery levels across the class.

                        ### 2. Topics Needing Attention
                        - Data Science applications need more reinforcement
                        - Fuzzy Logic fundamentals show inconsistent understanding

                        ### 3. Recommended Interventions
                        - Implement peer learning groups matching stronger and weaker students
                        - Develop supplementary materials for challenging topics
                        - Use formative assessments to identify misconceptions early

                        ### 4. Teaching Strategies
                        - Use scaffolded instruction to support struggling students
                        - Implement visual learning tools for abstract concepts
                        - Provide more real-world applications and examples

                        ### 5. Differentiation Approaches
                        - For high performers: Offer enrichment projects and advanced applications
                        - For middle performers: Reinforce concepts through varied practice
                        - For struggling students: Provide targeted support in small groups
                        """)
        else:
            st.info("No quiz data available for class analysis.")
    
    # Tab 4: Learning Path Prediction
    with tab4:
        st.subheader("🔮 Learning Path Prediction & Modeling")
        
        # Student selection
        student_id = st.selectbox("Select Student", list(students_data.keys()), key="prediction_student")
        student = students_data[student_id]
        
        col1, col2 = st.columns(2)
        with col1:
            prediction_weeks = st.slider("Prediction Timeframe (weeks)", 1, 12, 4)
        
        with col2:
            learning_intensity = st.select_slider(
                "Learning Intensity",
                options=["Low", "Medium", "High"],
                value="Medium"
            )
        
        # Generate learning path prediction
        if st.button("Predict Learning Path"):
            with st.spinner("Generating learning path prediction..."):
                # Get student's quiz history
                history_df = get_student_quiz_history(student_id)
                
                # Prepare data for AI analysis
                student_data = {
                    "name": student['name'],
                    "proficiency": student.get("proficiency", {}),
                    "quiz_history": history_df.to_dict() if not history_df.empty else None,
                    "prediction_weeks": prediction_weeks,
                    "learning_intensity": learning_intensity
                }
                
                prompt = f"""
                Predict the learning path for this student over the next {prediction_weeks} weeks.
                Assume {learning_intensity} intensity of study.
                
                Student Data: {json.dumps(student_data, indent=2)}
                
                Generate:
                1. Weekly proficiency predictions for each subject
                2. Expected milestones and achievements
                3. Potential challenges and bottlenecks
                4. Optimal learning sequence
                
                Return as JSON with this format:
                {{
                    "weekly_predictions": [
                        {{
                            "week": 1,
                            "proficiency": {{"Topic1": 0.75, "Topic2": 0.65}}
                        }}
                    ],
                    "milestones": ["Milestone 1", "Milestone 2"],
                    "challenges": ["Challenge 1", "Challenge 2"],
                    "learning_sequence": ["Step 1", "Step 2"]
                }}
                """
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You predict learning paths based on student data."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    response_text = response.choices[0].message.content.strip()
                    if "```json" in response_text:
                        response_text = response_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in response_text:
                        response_text = response_text.split("```")[1].split("```")[0].strip()
                    
                    prediction_data = json.loads(response_text)
                    
                    # Display proficiency prediction chart
                    st.subheader("Proficiency Prediction")
                    
                    # Prepare data for chart
                    weeks = [p["week"] for p in prediction_data["weekly_predictions"]]
                    topics = list(prediction_data["weekly_predictions"][0]["proficiency"].keys())
                    
                    # Create plot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    for topic in topics:
                        topic_scores = [p["proficiency"][topic] for p in prediction_data["weekly_predictions"]]
                        ax.plot(weeks, topic_scores, marker='o', label=topic)
                    
                    ax.set_xlabel("Week")
                    ax.set_ylabel("Predicted Proficiency")
                    ax.set_title(f"Proficiency Prediction - Next {prediction_weeks} Weeks")
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    
                    # Display milestones and challenges
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 🏆 Expected Milestones")
                        for i, milestone in enumerate(prediction_data["milestones"]):
                            st.markdown(f"{i+1}. {milestone}")
                    
                    with col2:
                        st.markdown("### 🧗 Potential Challenges")
                        for i, challenge in enumerate(prediction_data["challenges"]):
                            st.markdown(f"{i+1}. {challenge}")
                    
                    # Display learning sequence
                    st.markdown("### 🛣️ Optimal Learning Sequence")
                    
                    # Create a timeline visualization
                    sequence = prediction_data["learning_sequence"]
                    timeline_html = f"""
                    <div style="margin-top: 20px;">
                        <div style="display: flex; align-items: center;">
                    """
                    
                    for i, step in enumerate(sequence):
                        # Add connecting line for all but the first step
                        if i > 0:
                            timeline_html += f"""
                            <div style="height: 2px; flex-grow: 1; background-color: #4CAF50;"></div>
                            """
                        
                        # Add step bubble
                        timeline_html += f"""
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #4CAF50; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold;">{i+1}</div>
                        """
                    
                    timeline_html += """
                        </div>
                    """
                    
                    # Add step details below timeline
                    for i, step in enumerate(sequence):
                        timeline_html += f"""
                        <div style="margin-top: 10px; margin-bottom: 20px;">
                            <div style="font-weight: bold;">Step {i+1}</div>
                            <div>{step}</div>
                        </div>
                        """
                    
                    timeline_html += "</div>"
                    
                    st.markdown(timeline_html, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error generating learning path: {str(e)}")
                    # Provide fallback content
                    st.subheader("Sample Learning Path Prediction")
                    
                    # Create a sample prediction visualization
                    weeks = [1, 2, 3, 4]
                    
                    # Create plot with sample data for the student's topics
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    # Get topics from the student's proficiency data
                    topics = list(student.get("proficiency", {}).keys())
                    if not topics:  # Fallback if no proficiency data
                        topics = ["Fuzzy Logic", "Data Science"]
                    
                    # Generate sample predictions for each topic
                    for topic in topics:
                        # Generate slightly increasing values with some randomness
                        base = next(iter(student.get("proficiency", {}).get(topic, {6: 0.7}).values())) if student.get("proficiency", {}) else 0.6
                        topic_scores = [
                            base,
                            base + 0.05 + random.uniform(0, 0.02),
                            base + 0.10 + random.uniform(0, 0.02),
                            base + 0.15 + random.uniform(0, 0.02)
                        ]
                        ax.plot(weeks, topic_scores, marker='o', label=topic)
                    
                    ax.set_xlabel("Week")
                    ax.set_ylabel("Predicted Proficiency")
                    ax.set_title(f"Proficiency Prediction - Next {prediction_weeks} Weeks")
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    
                    # Display sample milestones and challenges
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 🏆 Expected Milestones")
                        st.markdown(f"1. Master fundamental concepts in {topics[0]}")
                        st.markdown(f"2. Complete practical exercises in {topics[0]}")
                        if len(topics) > 1:
                            st.markdown(f"3. Apply {topics[1]} knowledge to real problems")
                            st.markdown(f"4. Integrate {topics[0]} and {topics[1]} in a project")
                    
                    with col2:
                        st.markdown("### 🧗 Potential Challenges")
                        st.markdown(f"1. Understanding advanced {topics[0]} complexity")
                        st.markdown(f"2. Maintaining consistent study schedule")
                        if len(topics) > 1:
                            st.markdown(f"3. Balancing time between {topics[0]} and {topics[1]}")
                    
                    # Sample learning sequence
                    st.markdown("### 🛣️ Optimal Learning Sequence")
                    
                    # Create a timeline visualization with sample data
                    sequence = [
                        f"Build foundation in {topics[0]} basics", 
                        "Practice with examples and exercises",
                        "Tackle advanced concepts",
                        "Apply knowledge to real-world problems"
                    ]
                    
                    timeline_html = """
                    <div style="margin-top: 20px;">
                        <div style="display: flex; align-items: center;">
                    """
                    
                    for i, step in enumerate(sequence):
                        # Add connecting line for all but the first step
                        if i > 0:
                            timeline_html += """
                            <div style="height: 2px; flex-grow: 1; background-color: #4CAF50;"></div>
                            """
                        
                        # Add step bubble
                        timeline_html += f"""
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #4CAF50; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold;">{i+1}</div>
                        """
                    
                    timeline_html += """
                        </div>
                    """
                    
                    # Add step details below timeline
                    for i, step in enumerate(sequence):
                        timeline_html += f"""
                        <div style="margin-top: 10px; margin-bottom: 20px;">
                            <div style="font-weight: bold;">Step {i+1}</div>
                            <div>{step}</div>
                        </div>
                        """
                    
                    timeline_html += "</div>"
                    
                    st.markdown(timeline_html, unsafe_allow_html=True)
    
    # Tab 5: Cognitive Analysis
    with tab5:
        st.subheader("🧠 Cognitive Learning Style Analysis")
        
        # Student selection
        student_id = st.selectbox("Select Student", list(students_data.keys()), key="cognitive_student")
        student = students_data[student_id]
        
        # Generate cognitive analysis
        if st.button("Analyze Learning Style"):
            with st.spinner("Analyzing learning patterns..."):
                # Get student's quiz history
                history_df = get_student_quiz_history(student_id)
                
                # Prepare data for AI analysis
                student_data = {
                    "name": student['name'],
                    "proficiency": student.get("proficiency", {}),
                    "quiz_history": history_df.to_dict() if not history_df.empty else None
                }
                
                prompt = f"""
                Analyze this student's learning patterns and cognitive style:
                
                Student Data: {json.dumps(student_data, indent=2)}
                
                Provide:
                1. Learning style assessment (visual, auditory, kinesthetic, reading/writing)
                2. Cognitive strengths and weaknesses
                3. Memory and retention patterns
                4. Optimal content delivery approaches
                5. Recommended study environment
                
                Return as JSON with these exact fields:
                {{
                    "learning_style": {{
                        "visual": 65,
                        "auditory": 40,
                        "kinesthetic": 75,
                        "reading_writing": 50
                    }},
                    "cognitive_strengths": ["Strength 1", "Strength 2"],
                    "cognitive_challenges": ["Challenge 1", "Challenge 2"],
                    "memory_patterns": "Description of memory patterns...",
                    "delivery_approaches": ["Approach 1", "Approach 2"],
                    "study_environment": "Description of ideal study environment..."
                }}
                """
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You analyze learning styles and cognitive patterns."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    response_text = response.choices[0].message.content.strip()
                    if "```json" in response_text:
                        response_text = response_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in response_text:
                        response_text = response_text.split("```")[1].split("```")[0].strip()
                    
                    cognitive_data = json.loads(response_text)
                    
                    # Display learning style radar chart
                    st.subheader("Learning Style Profile")
                    
                    # Prepare data for radar chart
                    categories = ['Visual', 'Auditory', 'Kinesthetic', 'Reading/Writing']
                    values = [
                        cognitive_data["learning_style"]["visual"],
                        cognitive_data["learning_style"]["auditory"],
                        cognitive_data["learning_style"]["kinesthetic"],
                        cognitive_data["learning_style"]["reading_writing"]
                    ]
                    
                    # Close the polygon
                    categories = categories + [categories[0]]
                    values = values + [values[0]]
                    
                    # Convert to radians
                    angles = np.linspace(0, 2*np.pi, len(categories)-1, endpoint=False).tolist()
                    angles += angles[:1]  # Close the polygon
                    
                    # Create radar chart
                    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
                    ax.plot(angles, [v/100 for v in values], 'o-', linewidth=2)
                    ax.fill(angles, [v/100 for v in values], alpha=0.25)
                    ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
                    ax.set_ylim(0, 1)
                    ax.set_title("Learning Style Analysis")
                    st.pyplot(fig)
                    
                    # Display primary learning style
                    max_style = categories[values.index(max(values[:-1]))]  # Exclude the duplicated first element
                    
                    st.success(f"### Primary Learning Style: {max_style}")
                    st.info(f"This student shows a preference for {max_style.lower()} learning methods. Their learning profile shows how they process and retain information best.")
                    
                    # Display cognitive details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 💪 Cognitive Strengths")
                        for strength in cognitive_data["cognitive_strengths"]:
                            st.markdown(f"- {strength}")
                    
                    with col2:
                        st.markdown("### 🔍 Cognitive Challenges")
                        for challenge in cognitive_data["cognitive_challenges"]:
                            st.markdown(f"- {challenge}")
                    
                    # Memory patterns
                    st.markdown("### 🧠 Memory & Retention Patterns")
                    st.markdown(cognitive_data["memory_patterns"])
                    
                    # Recommended approaches
                    st.subheader("Personalized Learning Recommendations")
                    
                    # Create visually appealing cards for recommendations
                    st.markdown("#### 📚 Optimal Content Delivery")
                    
                    # Display approaches as cards
                    approaches_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">'
                    
                    for approach in cognitive_data["delivery_approaches"]:
                        approaches_html += f"""
                        <div style="flex: 1; min-width: 200px; padding: 15px; border-radius: 10px; background-color: #f0f8ff; border-left: 5px solid #4CAF50;">
                            {approach}
                        </div>
                        """
                    
                    approaches_html += '</div>'
                    st.markdown(approaches_html, unsafe_allow_html=True)
                    
                    # Ideal study environment
                    st.markdown("#### 🏡 Ideal Study Environment")
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 10px; background-color: #f5f5f5;">
                        {cognitive_data["study_environment"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add a personalized study plan based on cognitive analysis
                    if st.button("Generate Personalized Study Plan"):
                        with st.spinner("Creating personalized study plan..."):
                            plan_prompt = f"""
                            Create a personalized 2-week study plan for this student based on their cognitive analysis:
                            
                            Student: {student['name']}
                            Learning Style Profile: {json.dumps(cognitive_data["learning_style"])}
                            Primary Learning Style: {max_style}
                            Cognitive Strengths: {", ".join(cognitive_data["cognitive_strengths"])}
                            
                            The plan should leverage their {max_style} learning style and cognitive strengths.
                            Include specific activities, resources, and scheduling recommendations.
                            """
                            
                            try:
                                plan_response = openai.ChatCompletion.create(
                                    model="gpt-4",
                                    messages=[
                                        {"role": "system", "content": "You create personalized study plans based on cognitive analysis."},
                                        {"role": "user", "content": plan_prompt}
                                    ],
                                    temperature=0.7,
                                    max_tokens=800
                                )
                                
                                study_plan = plan_response.choices[0].message.content.strip()
                                st.markdown("### 📝 Personalized Study Plan")
                                st.markdown(study_plan)
                                
                                # Add download button for study plan
                                st.download_button(
                                    label="📥 Download Study Plan",
                                    data=study_plan,
                                    file_name=f"{student['name']}_cognitive_study_plan.txt",
                                    mime="text/plain"
                                )
                            except Exception as e:
                                st.error(f"Error generating study plan: {str(e)}")
                                # Provide fallback content
                                st.markdown("""
                                ### 📝 Personalized Study Plan

                                #### Week 1: Foundations
                                
                                **Monday:**
                                - Visual learning: Watch concept videos on topic (1 hour)
                                - Create mind maps of key concepts (30 min)
                                
                                **Tuesday:**
                                - Review mind maps (15 min)
                                - Practice problems with visual aids (45 min)
                                
                                **Wednesday:**
                                - Interactive tutorials or simulations (1 hour)
                                - Create visual flashcards for key terms (30 min)
                                
                                **Thursday:**
                                - Apply concepts to simple problems (45 min)
                                - Review and expand mind maps (30 min)
                                
                                **Friday:**
                                - Watch advanced concept videos (45 min)
                                - Self-quiz with flashcards (20 min)
                                
                                **Weekend:**
                                - Comprehensive review using all visual aids (1 hour)
                                - Rest and light review

                                #### Week 2: Application & Mastery
                                
                                **Monday:**
                                - Tackle complex problems with diagramming (1 hour)
                                - Review areas of difficulty (30 min)
                                
                                **Tuesday:**
                                - Create visual presentations on topics (1 hour)
                                - Share and explain to study partner (30 min)
                                
                                **Wednesday:**
                                - Work on practical project (1.5 hours)
                                
                                **Thursday:**
                                - Continue project work (1 hour)
                                - Review all visual materials (30 min)
                                
                                **Friday:**
                                - Complete self-assessment with visual aids (1 hour)
                                - Identify remaining gaps (30 min)
                                
                                **Weekend:**
                                - Final review and integration of all materials
                                - Prepare visual summary of what you've learned
                                """)
                    
                except Exception as e:
                    st.error(f"Error analyzing learning style: {str(e)}")
                    # Provide fallback content
                    st.subheader("Sample Learning Style Analysis")
                    
                    # Sample data based on the student's main subject
                    topic = list(student.get("proficiency", {"Visual Learning": {}}).keys())[0]
                    
                    # Create sample cognitive data
                    sample_data = {
                        "learning_style": {
                            "visual": 70,
                            "auditory": 45,
                            "kinesthetic": 60,
                            "reading_writing": 55
                        },
                        "cognitive_strengths": [
                            f"Strong visual processing of {topic} concepts",
                            "Good pattern recognition and connections between ideas",
                            "Effective learning through demonstrations and diagrams"
                        ],
                        "cognitive_challenges": [
                            "May struggle with purely verbal instructions",
                            "Needs to see concepts illustrated to fully grasp them",
                            "Can be distracted in text-heavy environments"
                        ],
                        "memory_patterns": f"This student demonstrates strong visual memory, retaining information best when presented with diagrams, charts, and other visual aids. They may benefit from creating mind maps and visual summaries of {topic} concepts.",
                        "delivery_approaches": [
                            "Use diagrams and flowcharts to explain complex concepts",
                            "Incorporate color-coding for categorizing information",
                            "Provide video demonstrations before practical exercises",
                            "Encourage creation of visual notes and mind maps"
                        ],
                        "study_environment": "An ideal study environment would be well-lit with minimal visual clutter. Having access to whiteboards or large paper for drawing out concepts would be beneficial. Digital tools for creating diagrams and mind maps are recommended. Reducing auditory distractions will help maintain focus on visual learning materials."
                    }
                    
                    # Display sample learning style radar chart
                    st.subheader("Learning Style Profile")
                    
                    # Prepare data for radar chart
                    categories = ['Visual', 'Auditory', 'Kinesthetic', 'Reading/Writing']
                    values = [
                        sample_data["learning_style"]["visual"],
                        sample_data["learning_style"]["auditory"],
                        sample_data["learning_style"]["kinesthetic"],
                        sample_data["learning_style"]["reading_writing"]
                    ]
                    
                    # Close the polygon
                    categories = categories + [categories[0]]
                    values = values + [values[0]]
                    
                    # Create radar chart
                    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
                    ax.plot(angles, [v/100 for v in values], 'o-', linewidth=2)
                    ax.fill(angles, [v/100 for v in values], alpha=0.25)
                    ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
                    ax.set_ylim(0, 1)
                    ax.set_title("Learning Style Analysis")
                    st.pyplot(fig)
                    
                    # Display primary learning style
                    st.success("### Primary Learning Style: Visual")
                    st.info("This student shows a preference for visual learning methods. Their learning profile shows how they process and retain information best through visual aids and representations.")
                    
                    # Display cognitive details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 💪 Cognitive Strengths")
                        for strength in sample_data["cognitive_strengths"]:
                            st.markdown(f"- {strength}")
                    
                    with col2:
                        st.markdown("### 🔍 Cognitive Challenges")
                        for challenge in sample_data["cognitive_challenges"]:
                            st.markdown(f"- {challenge}")
                    
                    # Memory patterns
                    st.markdown("### 🧠 Memory & Retention Patterns")
                    st.markdown(sample_data["memory_patterns"])
                    
                    # Recommended approaches
                    st.subheader("Personalized Learning Recommendations")
                    
                    # Create visually appealing cards for recommendations
                    st.markdown("#### 📚 Optimal Content Delivery")
                    
                    # Display approaches as cards
                    approaches_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">'
                    
                    for approach in sample_data["delivery_approaches"]:
                        approaches_html += f"""
                        <div style="flex: 1; min-width: 200px; padding: 15px; border-radius: 10px; background-color: #f0f8ff; border-left: 5px solid #4CAF50;">
                            {approach}
                        </div>
                        """
                    
                    approaches_html += '</div>'
                    st.markdown(approaches_html, unsafe_allow_html=True)
                    
                    # Ideal study environment
                    st.markdown("#### 🏡 Ideal Study Environment")
                    st.markdown(f"""
                    <div style="padding: 15px; border-radius: 10px; background-color: #f5f5f5;">
                        {sample_data["study_environment"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add a button for study plan
                    if st.button("Generate Personalized Study Plan"):
                        st.markdown("""
                        ### 📝 Personalized Study Plan

                        #### Week 1: Foundations
                        
                        **Monday:**
                        - Visual learning: Watch concept videos on topic (1 hour)
                        - Create mind maps of key concepts (30 min)
                        
                        **Tuesday:**
                        - Review mind maps (15 min)
                        - Practice problems with visual aids (45 min)
                        
                        **Wednesday:**
                        - Interactive tutorials or simulations (1 hour)
                        - Create visual flashcards for key terms (30 min)
                        
                        **Thursday:**
                        - Apply concepts to simple problems (45 min)
                        - Review and expand mind maps (30 min)
                        
                        **Friday:**
                        - Watch advanced concept videos (45 min)
                        - Self-quiz with flashcards (20 min)
                        
                        **Weekend:**
                        - Comprehensive review using all visual aids (1 hour)
                        - Rest and light review

                        #### Week 2: Application & Mastery
                        
                        **Monday:**
                        - Tackle complex problems with diagramming (1 hour)
                        - Review areas of difficulty (30 min)
                        
                        **Tuesday:**
                        - Create visual presentations on topics (1 hour)
                        - Share and explain to study partner (30 min)
                        
                        **Wednesday:**
                        - Work on practical project (1.5 hours)
                        
                        **Thursday:**
                        - Continue project work (1 hour)
                        - Review all visual materials (30 min)
                        
                        **Friday:**
                        - Complete self-assessment with visual aids (1 hour)
                        - Identify remaining gaps (30 min)
                        
                        **Weekend:**
                        - Final review and integration of all materials
                        - Prepare visual summary of what you've learned
                        """)
                        
                        # Add download button for study plan
                        sample_study_plan = """
                        # Personalized Study Plan for Visual Learner

                        ## Week 1: Foundations
                        
                        ### Monday:
                        - Visual learning: Watch concept videos on topic (1 hour)
                        - Create mind maps of key concepts (30 min)
                        
                        ### Tuesday:
                        - Review mind maps (15 min)
                        - Practice problems with visual aids (45 min)
                        
                        ### Wednesday:
                        - Interactive tutorials or simulations (1 hour)
                        - Create visual flashcards for key terms (30 min)
                        
                        ### Thursday:
                        - Apply concepts to simple problems (45 min)
                        - Review and expand mind maps (30 min)
                        
                        ### Friday:
                        - Watch advanced concept videos (45 min)
                        - Self-quiz with flashcards (20 min)
                        
                        ### Weekend:
                        - Comprehensive review using all visual aids (1 hour)
                        - Rest and light review

                        ## Week 2: Application & Mastery
                        
                        ### Monday:
                        - Tackle complex problems with diagramming (1 hour)
                        - Review areas of difficulty (30 min)
                        
                        ### Tuesday:
                        - Create visual presentations on topics (1 hour)
                        - Share and explain to study partner (30 min)
                        
                        ### Wednesday:
                        - Work on practical project (1.5 hours)
                        
                        ### Thursday:
                        - Continue project work (1 hour)
                        - Review all visual materials (30 min)
                        
                        ### Friday:
                        - Complete self-assessment with visual aids (1 hour)
                        - Identify remaining gaps (30 min)
                        
                        ### Weekend:
                        - Final review and integration of all materials
                        - Prepare visual summary of what you've learned
                        """
                        
                        st.download_button(
                            label="📥 Download Study Plan",
                            data=sample_study_plan,
                            file_name=f"{student['name']}_sample_study_plan.txt",
                            mime="text/plain"
                        )

def display_paper_setter():
    """Display the Paper Setter interface integrated from papersetter.py"""
    st.title("📝 SASTRA Exam Paper Setter")
    st.markdown("Set quality question papers automatically using AI.")

    # Upload study material
    study_file = st.file_uploader("📚 Upload Study Material (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
    syllabus_file = st.file_uploader("🗂️ Upload Syllabus (Optional)", type=["pdf", "txt", "docx"])

    # Paper pattern
    pattern = st.radio("📋 Choose Paper Pattern", (
        "Part A: 10 questions × 2 marks, Part B: 3 questions × 10 marks",
        "Part A: 5 questions × 10 marks"
    ))

    # Difficulty
    difficulty = st.selectbox("🎯 Select Difficulty Level", ["Easy", "Medium", "Hard", "Mixed"])

    # Additional Instructions
    instructions = st.text_area("🛠️ Additional Instructions (Optional)", 
                               placeholder="E.g., Include questions from all chapters, Bloom's taxonomy-based, etc.")

    # Generate button
    if st.button("Generate Question Paper"):
        if not study_file:
            st.error("Please upload study material.")
        else:
            with st.spinner("Generating question paper..."):
                study_text = extract_text(study_file)
                syllabus_text = extract_text(syllabus_file) if syllabus_file else ""
                result = generate_question_paper(study_text, syllabus_text, pattern, difficulty, instructions)

                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.success("✅ Question paper generated!")
                    st.download_button("📥 Download Question Paper", result, file_name="question_paper.txt")
                    st.text_area("📄 Preview", result, height=400)

# Add the extract_text function from papersetter.py
def extract_text(file):
    """Extract text from supported file types."""
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

# Add the generate_question_paper function from papersetter.py
def generate_question_paper(content, syllabus, pattern, difficulty, instructions):
    """Generate question paper using GPT."""
    prompt = f"""
You are an expert exam paper setter.

SET A QUESTION PAPER based on the given study material{'' if not syllabus else ' and syllabus'}.

### STUDY MATERIAL:
{content}

### SYLLABUS:
{syllabus if syllabus else 'Not Provided'}

### PAPER PATTERN:
{pattern}

### DIFFICULTY LEVEL:
{difficulty}

### ADDITIONAL INSTRUCTIONS:
{instructions}

Ensure questions are well-phrased, diverse, and aligned with the selected difficulty and pattern.
Clearly format Part A and Part B if both are present.
Return only the question paper.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    except openai.AuthenticationError:
        return "❌ Invalid API key. Please check your OpenAI API key."
    except Exception as e:
        return f"⚠️ An error occurred: {e}"
    

def display_all_research_tools():
    """Display all research tools in one dashboard"""
    from research_tools_integration import display_research_tools
    display_research_tools()


            # ---------------- SAMPLE STUDENT DATA ----------------
students_data = {
    "SEEE001": {"name": "Adhithya V", "proficiency": {"Fuzzy Logic": {1: 0.59, 2: 0.64, 3: 0.69, 4: 0.74, 5: 0.79, 6: 0.84}}},
    "SEEE002": {"name": "Akety Manjunath", "proficiency": {"Data Science": {1: 0.6, 2: 0.65, 3: 0.7, 4: 0.75, 5: 0.8, 6: 0.85}}},
    # ... (other student data omitted for brevity)
    "SEEE061": {"name": "Swaran V", "proficiency": {"AI Ethics": {1: 0.54, 2: 0.59, 3: 0.64, 4: 0.69, 5: 0.74, 6: 0.79}}}
}

# ---------------- SAMPLE QUESTIONS DATA ----------------
questions = [
    {"text": "What is the primary goal of supervised learning?", "options": [
        "To cluster data points without labels",
        "To learn patterns from labeled data to make predictions",
        "To reduce the dimensionality of data",
        "To generate new data samples"
    ], "correct": "To learn patterns from labeled data to make predictions"},
    {"text": "Which algorithm is used for classification?", "options": [
        "K-Means", "Decision Tree", "PCA", "Apriori"
    ], "correct": "Decision Tree"},
    {"text": "What does CNN stand for?", "options": [
        "Convolutional Neural Network", "Central Neural Network",
        "Computational Node Network", "Convolutional Node Network"
    ], "correct": "Convolutional Neural Network"},
    {"text": "Which technique helps reduce overfitting?", "options": [
        "Regularization", "Dropout", "Both 1 & 2", "None"
    ], "correct": "Both 1 & 2"}
]

# ---------------- SESSION STATE INIT ----------------
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 5
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "live_omr_questions" not in st.session_state:
    st.session_state.live_omr_questions = None
    
# Additional session states for enhanced OMR test
if "student_answers" not in st.session_state:
    st.session_state.student_answers = []
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "warnings_count" not in st.session_state:
    st.session_state.warnings_count = 0
if "test_in_progress" not in st.session_state:
    st.session_state.test_in_progress = False
if "test_completed" not in st.session_state:
    st.session_state.test_completed = False
if "last_detection_time" not in st.session_state:
    st.session_state.last_detection_time = time.time()
if "looking_away_start" not in st.session_state:
    st.session_state.looking_away_start = None
if "audio_detection_queue" not in st.session_state:
    st.session_state.audio_detection_queue = queue.Queue()
# New states for enhanced proctoring
if "latest_warning" not in st.session_state:
    st.session_state.latest_warning = None
if "latest_warning_time" not in st.session_state:
    st.session_state.latest_warning_time = None
if "latest_warning_type" not in st.session_state:
    st.session_state.latest_warning_type = None
if "test_terminated" not in st.session_state:
    st.session_state.test_terminated = False
if "termination_reason" not in st.session_state:
    st.session_state.termination_reason = None
# Initialize AI Tutor
setup_ai_tutor()

# Initialize database
init_db()

# ---------------- STREAMLIT UI LAYOUT ----------------
# ---------------- STREAMLIT UI LAYOUT ----------------
# Initialize session state
initialize_session_state()

# Set up the app title at the top
st.title("🚀 Generative AI-Based Students Assessment System")

# Create the improved icon-based sidebar for navigation
# Choose one of these options:
main_category = create_improved_icon_sidebar()  # Basic improved version
# OR
# main_category = create_stylish_icon_sidebar()   # More stylish version
# OR
# main_category = create_modern_icon_sidebar()    # Modern version with custom styling

# Get the page to display based on the selected category
page = get_page_from_category(main_category)

# The rest of your page content handling remains unchanged
# The rest of your code (page content display based on 'page' value) remains unchanged
# ---------------- PAGE: DASHBOARD ----------------
if page == "📊 Dashboard":
    st.header("📊 Class Performance Dashboard")
    
    # Select Student
    student_id = st.selectbox("Select a Student", list(students_data.keys()))
    student = students_data[student_id]
    st.subheader(f"Student: {student['name']}")
    
    # Proficiency Data
    prof_data = student["proficiency"]
    topics = list(prof_data.keys())
    bloom_levels = [1, 2, 3, 4, 5, 6]
    
    # Heatmap Data
    heatmap_data = pd.DataFrame(
        {topic: [prof_data[topic].get(level, 0.5) for level in bloom_levels] for topic in topics},
        index=[f"Level {lvl}" for lvl in bloom_levels]
    )
    
    st.subheader("📌 Bloom's Taxonomy Heatmap")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
    st.pyplot(fig)
    
    st.subheader("📈 Student Progress Over Time")
    dates = [datetime.now().replace(day=i) for i in range(1, 11)]
    scores = [random.uniform(0.4, 0.9) for _ in range(10)]
    plt.figure(figsize=(8, 5))
    plt.plot(dates, scores, marker='o', linestyle='-')
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Proficiency Score")
    plt.title("Student Progress")
    st.pyplot(plt)
# ---------------- PAGE: AI TUTOR ----------------
elif page == "👨‍🏫 AI Tutor":
    display_ai_tutor_page(students_data)
# ---------------- PAGE: AI-POWERED STORYTELLING ----------------
elif page == "📖 AI-Powered Storytelling":
    st.header("📖 AI-Powered Conversational Storytelling")
    user_topic = st.text_input("Enter a topic for the story (e.g., AI in Space, Lost Treasure, Cybersecurity):")
    if "story_conversation" not in st.session_state:
        st.session_state.story_conversation = []
    if st.button("Generate Story"):
        if user_topic.strip():
            prompt = (
                f"You are a friendly AI storyteller. Create a fun and engaging story based on the topic: '{user_topic}'. "
                f"Format the story like a chatbot conversation where an AI and a human character interact."
            )
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a storytelling AI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=400
            )
            story_text = response.choices[0].message.content.strip()
            st.session_state.story_conversation.append({"role": "AI Storyteller", "content": story_text})
    for message in st.session_state.story_conversation:
        if message["role"] == "AI Storyteller":
            st.markdown(f"**🤖 AI Storyteller:** {message['content']}")
    user_reply = st.text_input("Continue the story... (Optional)")
    if st.button("Continue"):
        if user_reply.strip():
            follow_up_prompt = (
                f"Continue the story based on the user's response: '{user_reply}'. "
                f"Keep the conversational tone between the AI storyteller and the characters."
            )
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a storytelling AI."},
                    {"role": "user", "content": follow_up_prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )
            follow_up_story = response.choices[0].message.content.strip()
            st.session_state.story_conversation.append({"role": "User", "content": user_reply})
            st.session_state.story_conversation.append({"role": "AI Storyteller", "content": follow_up_story})
            st.rerun()
# ---------------- PAGE: TAKE QUIZ ----------------
elif page == "📝 Take Quiz":
    st.header("📝 Adaptive Quiz")
    student_id = st.selectbox("Select your Student ID", list(students_data.keys()))
    st.write(f"Student Name: {students_data[student_id]['name']}")
    quiz_topic = st.selectbox(
        "Select a topic for your quiz:",
        ["Generative AI", "Machine Learning", "Reinforcement Learning", "Deep Learning", "Natural Language Processing", "Computer Vision"]
    )
    st.session_state.total_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)
    if not st.session_state.quiz_active:
        if st.button("Start Quiz"):
            st.session_state.quiz_active = True
            st.session_state.question_count = 0
            st.session_state.score = 0
            prompt = (
                f"Create a multiple-choice question about {quiz_topic} with 4 options and indicate the correct answer. "
                f"Format your response as JSON with fields: 'text', 'options' (array of 4), and 'correct'."
            )
            with st.spinner("Generating question..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI that generates educational quiz questions. Return valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=250
                )
                try:
                    response_text = response.choices[0].message.content.strip()
                    if "```json" in response_text:
                        response_text = response_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in response_text:
                        response_text = response_text.split("```")[1].split("```")[0].strip()
                    st.session_state.current_question = json.loads(response_text)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating question: {str(e)}")
                    st.write("Response received:", response.choices[0].message.content)
                    st.session_state.quiz_active = False
    if st.session_state.quiz_active and st.session_state.question_count < st.session_state.total_questions:
        q = st.session_state.current_question
        st.write(f"**Q{st.session_state.question_count+1}:** {q['text']}")
        answer = st.radio("Choose the correct answer:", q["options"], index=None)
        if st.button("Submit Answer"):
            if answer:
                if answer == q["correct"]:
                    st.success("✅ Correct Answer!")
                    st.session_state.score += 1
                else:
                    st.error("❌ Incorrect Answer!")
                    st.info(f"The correct answer was: {q['correct']}")
                st.session_state.question_count += 1
                if st.session_state.question_count < st.session_state.total_questions:
                    prompt = (
                        f"Create a multiple-choice question about {quiz_topic} with 4 options and indicate the correct answer. "
                        f"Format as JSON: 'text', 'options', 'correct'."
                    )
                    with st.spinner("Generating next question..."):
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are an AI that generates educational quiz questions. Return valid JSON only."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=250
                        )
                        try:
                            response_text = response.choices[0].message.content.strip()
                            if "```json" in response_text:
                                response_text = response_text.split("```json")[1].split("```")[0].strip()
                            elif "```" in response_text:
                                response_text = response_text.split("```")[1].split("```")[0].strip()
                            st.session_state.current_question = json.loads(response_text)
                        except Exception as e:
                            st.error(f"Error generating question: {str(e)}")
                            st.write("Response received:", response.choices[0].message.content)
                            st.session_state.current_question = {
                                "text": "What is a primary advantage of using neural networks?",
                                "options": [
                                    "They always require less data than other models",
                                    "They can automatically learn complex patterns from data",
                                    "They never overfit",
                                    "They always train quickly"
                                ],
                                "correct": "They can automatically learn complex patterns from data"
                            }
                st.rerun()
    elif st.session_state.quiz_active and st.session_state.question_count >= st.session_state.total_questions:
        st.success(f"Quiz Complete! Your Final Score: {st.session_state.score}/{st.session_state.total_questions}")
        save_quiz_result(
            student_id=student_id,
            student_name=students_data[student_id]["name"],
            topic=quiz_topic,
            score=st.session_state.score,
            total_questions=st.session_state.total_questions
        )
        score_percentage = (st.session_state.score / st.session_state.total_questions) * 100
        if score_percentage >= 80:
            st.balloons()
            st.write("🌟 Excellent! You have a strong understanding of this topic.")
        elif score_percentage >= 60:
            st.write("👍 Good job! You have a solid grasp of the basics.")
        else:
            st.write("📚 Keep learning! Consider reviewing this topic more thoroughly.")
        if st.button("Restart Quiz"):
            st.session_state.quiz_active = False
            st.rerun()

# ---------------- PAGE: QUIZ HISTORY ----------------
elif page == "📚 Quiz History":
    st.header("📚 Quiz History Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        view_option = st.radio("View", ["All Students", "Specific Student"])
    student_id = None
    if view_option == "Specific Student":
        with col2:
            student_id = st.selectbox("Select Student", list(students_data.keys()))
            st.write(f"Student: {students_data[student_id]['name']}")
    history_df = get_student_quiz_history(student_id)
    if not history_df.empty:
        history_df['percentage'] = (history_df['score'] / history_df['total_questions'] * 100).round(1)
        st.subheader("📋 Quiz Results")
        st.dataframe(history_df[['student_name', 'topic', 'score', 'total_questions', 'percentage', 'timestamp']])
        st.subheader("📊 Performance by Topic")
        topic_df = history_df.groupby('topic')[['percentage']].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='topic', y='percentage', data=topic_df, ax=ax)
        plt.title("Average Score by Topic")
        plt.ylabel("Average Score (%)")
        plt.xlabel("Topic")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        if student_id:
            st.subheader("📈 Performance Over Time")
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            history_df = history_df.sort_values('timestamp')
            plt.figure(figsize=(10, 6))
            plt.plot(history_df['timestamp'], history_df['percentage'], marker='o', linestyle='-')
            plt.title(f"Performance Over Time - {students_data[student_id]['name']}")
            plt.ylabel("Score (%)")
            plt.xlabel("Date")
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            st.pyplot(plt)
    else:
        st.info("No quiz history available. Take a quiz to see results here.")

# ---------------- PAGE: AI-POWERED HINTS ----------------
elif page == "🧠 AI-Powered Hints":
    st.header("🧠 Get AI-Powered Hints")
    question_text = st.text_area("Enter your question:")
    if st.button("Get Hint"):
        prompt = f"Provide a hint for the following question: {question_text}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant providing hints."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=100
        )
        hint = response.choices[0].message.content.strip()
        st.info(f"💡 Hint: {hint}")

# ---------------- PAGE: AI PEER ASSESSMENT ----------------
elif page == "🔍 AI Peer Assessment":
    st.header("🔍 AI-Powered Peer Assessment")
    student_submission = st.text_area("Paste student submission:")
    rubric = {"Concept Understanding": 10, "Implementation": 10, "Analysis": 10, "Clarity": 5, "Creativity": 5}
    if st.button("Generate Peer Review"):
        prompt = f"Assess the following submission using this rubric: {json.dumps(rubric)}\n\nSubmission: {student_submission}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI generating structured peer assessments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        review = response.choices[0].message.content.strip()
        st.success("✅ AI Peer Review Generated:")
        st.write(review)

# ---------------- PAGE: PLAGIARISM / REASONING FINDER ----------------
elif page == "🔍 Plagiarism/Reasoning Finder":
    st.header("🔍 Plagiarism/Reasoning Finder")
    uploaded_file = st.file_uploader("Upload student's document (.docx or .pdf)", type=["docx", "pdf"])
    student_submission = ""
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        if file_type == "docx":
            student_submission = extract_text_from_docx(uploaded_file)
        elif file_type == "pdf":
            student_submission = extract_text_from_pdf(uploaded_file)
        st.subheader("📄 Extracted Submission:")
        st.text_area("Extracted Text", student_submission, height=300)
    rubric = {"Concept Understanding": 10, "Implementation": 10, "Analysis": 10, "Clarity": 5, "Creativity": 5}
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Generate AI Assessment"):
            if student_submission.strip():
                prompt = (
                    f"Assess the following submission based on this rubric: {json.dumps(rubric)}\n\n"
                    f"Submission:\n{student_submission}"
                )
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI grading student assignments."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                review = response.choices[0].message.content.strip()
                st.success("✅ AI Feedback Generated:")
                st.write(review)
            else:
                st.warning("⚠️ Please upload a valid document.")
    with col2:
        if st.button("🔍 Check for Plagiarism"):
            if student_submission.strip():
                with st.spinner("Checking plagiarism..."):
                    plagiarism_prompt = (
                        f"Analyze the following document for plagiarism risk. "
                        f"Your response MUST include a clear plagiarism percentage in the first line with this exact format: "
                        f"'Plagiarism Risk: XX%' (where XX is a number between 0 and 100). "
                        f"Then provide your explanation below.\n\n"
                        f"Document:\n{student_submission}"
                    )
                    plagiarism_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an AI that checks for plagiarism in academic work. "
                                    "Always provide a clear plagiarism percentage in your first line."
                                )
                            },
                            {"role": "user", "content": plagiarism_prompt}
                        ],
                        temperature=0.3,
                        max_tokens=400
                    )
                    plagiarism_result = plagiarism_response.choices[0].message.content.strip()
                    try:
                        if "Plagiarism Risk:" in plagiarism_result:
                            first_line = plagiarism_result.split('\n')[0]
                            percentage_text = first_line.split('Plagiarism Risk:')[1].strip()
                            if '%' in percentage_text:
                                percentage = float(percentage_text.replace('%', '').strip())
                                st.subheader("Plagiarism Risk Score:")
                                st.progress(percentage / 100)
                                if percentage < 30:
                                    st.success(f"📊 Plagiarism Risk: {percentage}% (Low Risk)")
                                elif percentage < 60:
                                    st.warning(f"📊 Plagiarism Risk: {percentage}% (Medium Risk)")
                                else:
                                    st.error(f"📊 Plagiarism Risk: {percentage}% (High Risk)")
                    except Exception as e:
                        st.error(f"Error parsing plagiarism percentage: {str(e)}")
                    st.subheader("📝 Plagiarism Analysis:")
                    st.write(plagiarism_result)
            else:
                st.warning("⚠️ Please upload a valid document.")

# ---------------- PAGE: CODE EVALUATION & PLAGIARISM CHECK ----------------
elif page == "📂 Code Evaluation & Plagiarism Check":
    st.header("📂 Code Evaluation & Plagiarism Check")
    uploaded_code = st.file_uploader("Upload a Python (.py) file", type=["py"])
    if uploaded_code is not None:
        code_content = uploaded_code.getvalue().decode("utf-8")
        st.subheader("📜 Uploaded Code:")
        st.code(code_content, language="python")
        syntax_error = check_python_syntax(code_content)
        if syntax_error:
            st.error(syntax_error)
        else:
            st.success("✅ No syntax errors found!")
        if st.button("📊 Evaluate Code & Check Plagiarism"):
            with st.spinner("Analyzing Code..."):
                prompt = (
                    "Analyze the following Python program. Provide:\n"
                    "1. Correctness Score\n2. Efficiency Score\n3. Readability Score\n"
                    "4. Plagiarism Risk Score\n5. Suggestions for Improvement\n\n"
                    f"Code:\n{code_content}"
                )
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI that evaluates Python code."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=600
                )
                evaluation_result = response.choices[0].message.content.strip()
                st.success("✅ AI Evaluation Generated:")
                st.write(evaluation_result)
        if st.button("🔍 Check for Plagiarism"):
            with st.spinner("Checking plagiarism..."):
                plagiarism_prompt = (
                    f"Analyze the following Python code for plagiarism risk. "
                    f"Your response MUST include a clear plagiarism percentage in the first line with this exact format: "
                    f"'Plagiarism Risk: XX%' (where XX is 0-100). Then provide explanation below.\n\n"
                    f"Code:\n{code_content}"
                )
                plagiarism_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI that checks for plagiarism in Python code. "
                                "Always provide a clear plagiarism percentage in your first line."
                            )
                        },
                        {"role": "user", "content": plagiarism_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=400
                )
                plagiarism_result = plagiarism_response.choices[0].message.content.strip()
                try:
                    if "Plagiarism Risk:" in plagiarism_result:
                        first_line = plagiarism_result.split('\n')[0]
                        percentage_text = first_line.split('Plagiarism Risk:')[1].strip()
                        if '%' in percentage_text:
                            percentage = float(percentage_text.replace('%', '').strip())
                            st.subheader("Plagiarism Risk Score:")
                            st.progress(percentage / 100)
                            if percentage < 30:
                                st.success(f"📊 Plagiarism Risk: {percentage}% (Low Risk)")
                            elif percentage < 60:
                                st.warning(f"📊 Plagiarism Risk: {percentage}% (Medium Risk)")
                            else:
                                st.error(f"📊 Plagiarism Risk: {percentage}% (High Risk)")
                except Exception as e:
                    st.error(f"Error parsing plagiarism percentage: {str(e)}")
                st.subheader("📝 Plagiarism Analysis:")
                st.write(plagiarism_result)

# ---------------- PAGE: AI-BASED LOR GENERATOR ----------------
elif page == "📄 AI-Based LOR Generator":
    st.header("📄 AI-Powered Letter of Recommendation (LOR) Generator")
    student_id = st.selectbox("Select Student ID", list(students_data.keys()))
    student = students_data[student_id]
    st.subheader(
        f"Student: {student['name']} | {student.get('department', 'B.Tech. Robotics & AI')}, "
        f"{student.get('year', 'Third Year')}"
    )
    st.write(f"**CGPA:** {student.get('cgpa', 'Not Available')}")
    lor_purpose = st.radio("Purpose of LOR", ["Higher Studies", "Internship", "Job Application"])
    skills = st.text_area("Enter key skills (comma-separated)", "Machine Learning, Research, Leadership")
    achievements = st.text_area("Enter achievements (comma-separated)", "Won AI Hackathon, Published IEEE Paper")
    if st.button("Generate LOR"):
        with st.spinner("Generating Letter of Recommendation..."):
            prompt = f"""
            Write a professional Letter of Recommendation (LOR) for a student. 
            The student details are:
            - Name: {student['name']}
            - Department: {student.get('department', 'B.Tech. Robotics & AI, Third Year')}
            - CGPA: {student.get('cgpa', 'Not Available')}
            - Purpose: {lor_purpose if lor_purpose else "Not Provided"}
            - Skills: {skills if skills else "Not Provided"}
            - Achievements: {achievements if achievements else "Not Provided"}

            The LOR should be formal, structured, and highlight the student's strengths, 
            academic achievements, and suitability for {lor_purpose}.
            """
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI that writes professional letters of recommendation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            st.session_state.lor_text = response.choices[0].message.content.strip()
            st.success("✅ Letter of Recommendation Generated!")
            st.text_area("Generated LOR", st.session_state.lor_text, height=300)
    if "lor_text" in st.session_state:
        refine_prompt = st.text_area("🔄 Enter improvements to refine the LOR (optional)")
        if st.button("Refine LOR"):
            with st.spinner("Refining LOR..."):
                refine_request = f"Refine and improve the following LOR based on this feedback: {refine_prompt}\n\n{st.session_state.lor_text}"
                refined_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You refine and improve letters of recommendation based on feedback."},
                        {"role": "user", "content": refine_request}
                    ],
                    temperature=0.6,
                    max_tokens=400
                )
                st.session_state.lor_text = refined_response.choices[0].message.content.strip()
                st.success("✅ LOR Refined!")
                st.text_area("Refined LOR", st.session_state.lor_text, height=300)
        doc = docx.Document()
        doc.add_paragraph(st.session_state.lor_text)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        st.download_button(
            label="📥 Download LOR (Word)",
            data=buffer,
            file_name="LOR.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# ---------------- PAGE: NLP ANSWER EVALUATION ----------------
elif page == "📝 NLP Answer Evaluation":
    st.header("📝 NLP Answer Evaluation")
    question_prompt = st.text_area("Question/Prompt for the student:")
    student_answer = st.text_area("Student's Answer:")
    if st.button("Evaluate Answer"):
        if question_prompt.strip() and student_answer.strip():
            eval_prompt = (
                f"Evaluate the student's answer to the following question:\n\n"
                f"Question: {question_prompt}\n\n"
                f"Student Answer: {student_answer}\n\n"
                f"Provide a short evaluation of correctness, clarity, and completeness. Then provide a final grade (1-10)."
            )
            with st.spinner("Evaluating via GPT-4..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI specialized in NLP-based short-answer evaluation."},
                        {"role": "user", "content": eval_prompt}
                    ],
                    temperature=0.4,
                    max_tokens=250
                )
                evaluation = response.choices[0].message.content.strip()
            st.success("✅ Evaluation Complete:")
            st.write(evaluation)
        else:
            st.warning("Please provide both a question and a student answer.")

# ---------------- PAGE: OMR MCQ GRADING ----------------
elif page == "📝 OMR MCQ Grading":
    st.header("📝 Computer Vision-based OMR MCQ Grading")
    uploaded_omr = st.file_uploader("Upload a scanned OMR sheet (image)", type=["png", "jpg", "jpeg"])
    if uploaded_omr is not None:
        file_bytes = np.asarray(bytearray(uploaded_omr.read()), dtype=np.uint8)
        try:
            cv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            st.image(cv_image, caption="Uploaded OMR Sheet", use_container_width=True)
            if st.button("Process OMR"):
                st.info("Processing OMR... (placeholder)")
                # TODO: Add actual OMR detection logic (e.g., circle detection, etc.)
                st.success("OMR processing complete. Placeholder result: Score = 8/10.")
        except Exception as e:
            st.error(f"Error reading image: {str(e)}")
    else:
        st.info("Upload an OMR image to begin.")


    # ---------------- PAGE: LIVE OMR TEST ----------------
elif page == "📝 Live OMR Test":
    # Use the enhanced OMR test function
    display_live_omr_test()

# ---------------- PAGE: ML PERFORMANCE TRACKING & PREDICTION ----------------
elif page == "📈 ML Performance Tracking & Prediction":
    st.header("📈 ML Performance Tracking & Prediction")
    st.write("This page illustrates how to use ML (Random Forest/XGBoost) to predict future performance.")
    st.markdown(
        """
        **Steps (conceptual):**
        1. Collect student performance data over time (scores, quiz results, etc.).
        2. Prepare features (e.g., recent quiz scores, attendance, etc.).
        3. Train a model (RandomForest/XGBoost) to predict future exam performance.
        4. Provide early interventions if the predicted performance is below a threshold.
        """
    )
    if st.button("Train Sample Model"):
        st.info("Training placeholder RandomForest model on synthetic data...")
        try:
            from sklearn.datasets import make_classification
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score
            X, y = make_classification(n_samples=100, n_features=5, n_informative=3, random_state=42)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            rf = RandomForestClassifier(n_estimators=10, random_state=42)
            rf.fit(X_train, y_train)
            preds = rf.predict(X_test)
            acc = accuracy_score(y_test, preds)
            st.success(f"Sample RandomForest Accuracy: {acc*100:.2f}%")
        except Exception as e:
            st.error("Scikit-learn not installed or an error occurred:")
            st.error(str(e))
    st.write("Similarly, you could use XGBoost for performance prediction:")
    if st.button("Train XGBoost Model"):
        try:
            from sklearn.datasets import make_regression
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import r2_score
            X, y = make_regression(n_samples=100, n_features=5, n_informative=3, random_state=42)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = xgb.XGBRegressor(n_estimators=10, use_label_encoder=False)
            model.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='logloss')
            preds = model.predict(X_test)
            score = r2_score(y_test, preds)
            st.success(f"Sample XGBoost R2 Score: {score:.2f}")
        except Exception as e:
            st.error("XGBoost not installed or an error occurred:")
            st.error(str(e))
    st.info("Use the trained model to predict future performance and intervene early if needed.")

# ---------------- PAGE: AI PROCTORING & INTEGRITY CHECKS ----------------
elif page == "🔒 AI Proctoring & Integrity Checks":
    st.header("🔒 AI-Powered Proctoring & Integrity Checks")
    st.write("Below is a **conceptual** placeholder for real-time proctoring features.")
    st.markdown(
        """
        **Potential Approaches:**
        - **Facial Recognition**: Confirm the student's identity matches the ID photo.
        - **Eye-Tracking**: Check if eyes deviate from screen for suspicious durations.
        - **Behavior Analysis**: Detect multiple faces, unusual movements, etc.
        """
    )
    face_image = st.file_uploader("Upload a photo for face verification", type=["png", "jpg", "jpeg"])
    if face_image is not None:
        try:
            file_bytes = np.asarray(bytearray(face_image.read()), dtype=np.uint8)
            cv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            if cv_image is not None:
                st.image(cv_image, caption="Uploaded Face Image", use_container_width=True)
                if st.button("Run Face Recognition"):
                    st.info("Performing face recognition... (placeholder)")
                    st.success("Identity verified with high confidence. (Placeholder result)")
            else:
                st.error("Error: Could not decode the image. Please try a different file.")
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    st.write("For advanced proctoring (eye tracking, behavior analysis), you'd typically need a live camera feed.")
    st.write("Below is just a placeholder demonstration.")
    if st.button("Start Behavior Analysis"):
        st.info("Analyzing user behavior from webcam feed... (placeholder)")
        st.success("No suspicious behavior detected. (Placeholder)")
    st.warning("Note: Real-time proctoring requires additional setup (webcam access, advanced CV).")

# ------------------- PAGE: syllabus optimization ----------------------------

elif page == "📅 Syllabus Optimization Engine":
    display_syllabus_optimization()
    
# ---------------- PAGE: AI PAPER SETTER ----------------
elif page == "📝 AI Paper Setter":
    display_paper_setter()

#------------------- PAGE: research tools ---------------------------
# Handle Research Tools pages
elif page == "📚 Citation Management":
    from citation_management import display_citation_management
    display_citation_management()

elif page == "📖 Literature Review Assistant":
    from literature_review_assistance import display_literature_review_assistant
    display_literature_review_assistant()

elif page == "🧪 Research Methodology":
    from research_methodology_guidance import display_methodology_guidance
    display_methodology_guidance()

elif page == "📊 Data Analysis Tools":
    from data_analysis_tools import display_data_analysis_tools
    display_data_analysis_tools()

elif page == "🔍 Academic Integrity":
    from academic_integrity_checking import display_academic_integrity_tools
    display_academic_integrity_tools()
