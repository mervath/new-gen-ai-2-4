from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
import json
import time
from io import BytesIO

def initialize_methodology_state():
    """Initialize session state variables for research methodology guidance"""
    if "active_methodology_tab" not in st.session_state:
        st.session_state.active_methodology_tab = "Overview"
    
    if "research_question" not in st.session_state:
        st.session_state.research_question = ""
    
    if "research_hypothesis" not in st.session_state:
        st.session_state.research_hypothesis = ""
    
    if "research_design" not in st.session_state:
        st.session_state.research_design = ""
    
    if "methodology_type" not in st.session_state:
        st.session_state.methodology_type = "Quantitative"
    
    if "sample_size_recommendation" not in st.session_state:
        st.session_state.sample_size_recommendation = ""
        
    if "methodology_templates" not in st.session_state:
        st.session_state.methodology_templates = {
            "Quantitative": {
                "Experimental": "Experimental research establishes cause and effect by manipulating variables and observing outcomes.",
                "Correlational": "Correlational research examines relationships between variables without manipulation.",
                "Survey": "Survey research collects data through questionnaires or interviews from a sample population.",
                "Observational": "Observational research involves systematic observation of behavior or phenomena."
            },
            "Qualitative": {
                "Phenomenological": "Phenomenological research explores lived experiences of participants.",
                "Ethnographic": "Ethnographic research studies cultural groups in their natural setting over an extended period.",
                "Grounded Theory": "Grounded theory develops theories based on systematic analysis of data.",
                "Case Study": "Case study research investigates a phenomenon within its real-life context."
            },
            "Mixed Methods": {
                "Sequential Explanatory": "Collect and analyze quantitative data first, then qualitative data to explain results.",
                "Sequential Exploratory": "Collect and analyze qualitative data first, then quantitative data to test or generalize findings.",
                "Convergent Parallel": "Collect and analyze quantitative and qualitative data concurrently, then compare or combine results.",
                "Embedded": "Either qualitative or quantitative data is embedded within the other approach."
            }
        }

def get_methodology_recommendation(research_question, methodology_type):
    """Generate methodology recommendations using AI"""
    
    prompt = f"""
    Generate a research methodology recommendation for the following research question:
    "{research_question}"
    
    Focusing on {methodology_type} research methods.
    
    Provide:
    1. Recommended research design
    2. Data collection methods
    3. Sampling strategy and recommended sample size
    4. Data analysis techniques
    5. Potential methodological limitations
    6. Ethical considerations
    
    Format your response as a JSON with these exact keys:
    - "research_design"
    - "data_collection"
    - "sampling"
    - "sample_size"
    - "data_analysis"
    - "limitations"
    - "ethics"
    
    The JSON must be properly formatted.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a research methodology specialist providing structured guidance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON if it's wrapped in code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        methodology_data = json.loads(response_text)
        return methodology_data
    
    except Exception as e:
        st.error(f"Error generating methodology recommendation: {str(e)}")
        # Provide fallback data
        return {
            "research_design": "Unable to generate recommendation. Please check your API key or try again later.",
            "data_collection": "",
            "sampling": "",
            "sample_size": "30-100 participants (typical range)",
            "data_analysis": "",
            "limitations": "",
            "ethics": "Ensure informed consent, confidentiality, and ethical approvals are in place."
        }

def generate_sample_size_calculation(methodology_type, design_type, effect_size, power, alpha):
    """Generate sample size calculation and explanation"""
    
    prompt = f"""
    Calculate the recommended sample size for a {methodology_type} research study with:
    - Research design: {design_type}
    - Expected effect size: {effect_size}
    - Desired statistical power: {power}
    - Significance level (alpha): {alpha}
    
    Provide:
    1. The calculated sample size
    2. The formula used for calculation
    3. Explanation of the calculation
    4. Recommendations for minimum and optimal sample sizes
    
    Format your response as a JSON with these exact keys:
    - "calculated_sample_size"
    - "formula"
    - "explanation"
    - "min_recommendation"
    - "optimal_recommendation"
    
    The JSON must be properly formatted.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a research methodology specialist providing sample size calculations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Extract JSON if it's wrapped in code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        calculation_data = json.loads(response_text)
        return calculation_data
    
    except Exception as e:
        st.error(f"Error generating sample size calculation: {str(e)}")
        # Provide fallback data
        return {
            "calculated_sample_size": "Unable to calculate. Please check your API key or try again later.",
            "formula": "n = (Z²σ²)/E²",
            "explanation": "Sample size calculation typically depends on effect size, power, and significance level.",
            "min_recommendation": "30 participants (minimum for statistical analysis)",
            "optimal_recommendation": "100+ participants for better statistical power"
        }

def generate_methodology_section(research_question, methodology_type, research_design):
    """Generate a draft methodology section for a research paper"""
    
    prompt = f"""
    Generate a draft methodology section for a research paper with:
    - Research question: "{research_question}"
    - Methodology type: {methodology_type}
    - Research design: {research_design}
    
    The methodology section should include:
    1. Research approach and design justification
    2. Sampling methodology
    3. Data collection procedures
    4. Data analysis techniques
    5. Validity and reliability considerations
    6. Ethical considerations
    
    Write this as a complete academic methodology section ready for inclusion in a research paper. Use formal academic language and proper structure.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a research methodology specialist writing academic methodology sections."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )
        
        methodology_section = response.choices[0].message.content.strip()
        return methodology_section
    
    except Exception as e:
        st.error(f"Error generating methodology section: {str(e)}")
        return "Unable to generate methodology section. Please check your API key or try again later."

def display_methodology_guidance():
    """Main function to display research methodology guidance interface"""
    
    # Initialize session state
    initialize_methodology_state()
    
    st.title("🧪 Research Methodology Guidance")
    
    # Navigation tabs
    methodology_tabs = [
        "Overview",
        "Research Design",
        "Sample Size Calculator",
        "Methodology Templates",
        "Draft Generator"
    ]
    
    selected_tab = st.radio("Research Methodology Tools", methodology_tabs, horizontal=True)
    st.session_state.active_methodology_tab = selected_tab
    
    st.markdown("---")
    
    # Tab 1: Methodology Overview
    if st.session_state.active_methodology_tab == "Overview":
        st.subheader("Overview of Research Methodologies")
        
        # Visual representation of methodology types
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### Quantitative
            - 📊 Numerical data
            - 📏 Measurable variables
            - 🔍 Testing hypotheses
            - 📈 Statistical analysis
            """)
            
        with col2:
            st.markdown("""
            ### Qualitative
            - 💬 Textual/verbal data
            - 🧠 Understanding experiences
            - 🌍 Contextual interpretation
            - 📝 Thematic analysis
            """)
            
        with col3:
            st.markdown("""
            ### Mixed Methods
            - 🔄 Integration of approaches
            - 🧩 Complex research problems
            - 📊 Triangulation of data
            - 🔬 Comprehensive insights
            """)
        
        # Methodology decision flowchart
        st.subheader("Methodology Selection Guide")
        st.markdown("""
        Use this decision tree to help select an appropriate methodology:
        
        1. **Research Question Type**
            - Testing relationships/hypotheses → Quantitative
            - Understanding meanings/experiences → Qualitative
            - Complex questions requiring multiple approaches → Mixed Methods
            
        2. **Available Data**
            - Primarily numerical/measurable → Quantitative
            - Primarily textual/observational → Qualitative
            - Both types equally important → Mixed Methods
            
        3. **Research Objective**
            - Generalization to populations → Quantitative
            - In-depth understanding of phenomena → Qualitative
            - Both breadth and depth → Mixed Methods
        """)
        
        # Research paradigms explanation
        with st.expander("Research Paradigms Explained"):
            st.markdown("""
            ### Key Research Paradigms
            
            **Positivism**
            - Objective reality exists independent of the researcher
            - Knowledge can be measured and observed
            - Typically associated with quantitative methods
            
            **Interpretivism**
            - Reality is subjective and socially constructed
            - Knowledge is interpreted through meaning-making
            - Typically associated with qualitative methods
            
            **Pragmatism**
            - Reality is what is useful or practical
            - Knowledge is derived from practical outcomes
            - Compatible with mixed methods approaches
            
            **Critical Theory**
            - Reality is shaped by social, political factors
            - Knowledge serves to challenge power structures
            - Can use various methodological approaches
            """)
        
        # Common research methods comparison
        with st.expander("Common Research Methods Comparison"):
            methods_data = {
                "Method": ["Experiments", "Surveys", "Interviews", "Focus Groups", "Case Studies", "Ethnography", "Action Research"],
                "Type": ["Quantitative", "Quant/Qual", "Qualitative", "Qualitative", "Qualitative", "Qualitative", "Mixed"],
                "When to Use": [
                    "Testing cause-effect relationships",
                    "Collecting data from large samples",
                    "In-depth individual perspectives",
                    "Group dynamics & collective opinions",
                    "Detailed analysis of specific instances",
                    "Cultural & social context understanding",
                    "Implementing & evaluating change"
                ],
                "Strengths": [
                    "High internal validity",
                    "Large sample sizes",
                    "Rich, detailed data",
                    "Group interaction insights",
                    "Contextual understanding",
                    "Real-world observations",
                    "Practical application"
                ],
                "Limitations": [
                    "Artificial settings",
                    "Surface-level data",
                    "Time-intensive",
                    "Dominant voices bias",
                    "Limited generalizability",
                    "Time-consuming",
                    "Researcher bias risks"
                ]
            }
            
            methods_df = pd.DataFrame(methods_data)
            st.dataframe(methods_df, use_container_width=True)
    
    # Tab 2: Research Design Advisor
    elif st.session_state.active_methodology_tab == "Research Design":
        st.subheader("Research Design Advisor")
        
        st.markdown("""
        The research design is the overall strategy chosen to integrate the different components 
        of your study in a coherent and logical way. Let's build your research design step-by-step.
        """)
        
        # Input fields for research design
        st.session_state.research_question = st.text_area(
            "Research Question",
            st.session_state.research_question,
            placeholder="e.g., What is the effect of X on Y?",
            help="A clear, specific, and answerable question that guides your research"
        )
        
        st.session_state.research_hypothesis = st.text_area(
            "Research Hypothesis (if applicable)",
            st.session_state.research_hypothesis,
            placeholder="e.g., X has a positive effect on Y",
            help="A testable statement predicting the relationship between variables"
        )
        
        # Methodology selection
        methodology_options = ["Quantitative", "Qualitative", "Mixed Methods"]
        methodology_type = st.selectbox(
            "Select Primary Methodology Type",
            methodology_options,
            index=methodology_options.index(st.session_state.methodology_type)
        )
        st.session_state.methodology_type = methodology_type
        
        # Show specific design options based on methodology type
        if methodology_type == "Quantitative":
            design_options = ["Experimental", "Correlational", "Survey", "Observational"]
        elif methodology_type == "Qualitative":
            design_options = ["Phenomenological", "Ethnographic", "Grounded Theory", "Case Study"]
        else:  # Mixed Methods
            design_options = ["Sequential Explanatory", "Sequential Exploratory", "Convergent Parallel", "Embedded"]
        
        research_design = st.selectbox(
            "Select Research Design",
            design_options,
            help="The specific approach for conducting your research"
        )
        st.session_state.research_design = research_design
        
        # Get AI recommendation for methodology
        if st.button("Get Methodology Recommendations"):
            if st.session_state.research_question:
                with st.spinner("Generating methodology recommendations..."):
                    methodology_data = get_methodology_recommendation(
                        st.session_state.research_question,
                        st.session_state.methodology_type
                    )
                    
                    # Display recommendation in a structured format
                    st.success("✅ Methodology recommendations generated!")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### Recommended Research Design")
                        st.markdown(methodology_data["research_design"])
                        
                        st.markdown("### Data Collection Methods")
                        st.markdown(methodology_data["data_collection"])
                        
                        st.markdown("### Sampling Strategy")
                        st.markdown(methodology_data["sampling"])
                    
                    with col2:
                        st.markdown("### Data Analysis Techniques")
                        st.markdown(methodology_data["data_analysis"])
                        
                        st.markdown("### Methodological Limitations")
                        st.markdown(methodology_data["limitations"])
                        
                        st.markdown("### Ethical Considerations")
                        st.markdown(methodology_data["ethics"])
                    
                    # Recommended sample size
                    st.markdown("### Recommended Sample Size")
                    st.info(f"🔢 {methodology_data['sample_size']}")
                    
                    # Add download option for the methodology recommendations
                    methodology_text = f"""
                    # Methodology Recommendations for Research Question:
                    "{st.session_state.research_question}"
                    
                    ## Research Design
                    {methodology_data["research_design"]}
                    
                    ## Data Collection Methods
                    {methodology_data["data_collection"]}
                    
                    ## Sampling Strategy
                    {methodology_data["sampling"]}
                    
                    ## Recommended Sample Size
                    {methodology_data["sample_size"]}
                    
                    ## Data Analysis Techniques
                    {methodology_data["data_analysis"]}
                    
                    ## Methodological Limitations
                    {methodology_data["limitations"]}
                    
                    ## Ethical Considerations
                    {methodology_data["ethics"]}
                    """
                    
                    st.download_button(
                        label="📥 Download Methodology Recommendations",
                        data=methodology_text,
                        file_name="methodology_recommendations.txt",
                        mime="text/plain"
                    )
            else:
                st.warning("Please enter a research question first.")
    
    # Tab 3: Sample Size Calculator
    elif st.session_state.active_methodology_tab == "Sample Size Calculator":
        st.subheader("Sample Size Calculator")
        
        st.markdown("""
        Determining an appropriate sample size is crucial for research validity and statistical power.
        This calculator helps estimate sample size requirements based on your research parameters.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Research parameters
            methodology_type = st.selectbox(
                "Research Methodology",
                ["Quantitative", "Qualitative", "Mixed Methods"],
                index=0,
                help="The primary methodological approach of your study"
            )
            
            # Show different design options based on methodology
            if methodology_type == "Quantitative":
                design_options = ["Experimental", "Correlational", "Survey", "Observational"]
            elif methodology_type == "Qualitative":
                design_options = ["Phenomenological", "Ethnographic", "Grounded Theory", "Case Study"]
            else:  # Mixed Methods
                design_options = ["Sequential Explanatory", "Sequential Exploratory", "Convergent Parallel", "Embedded"]
            
            design_type = st.selectbox(
                "Research Design",
                design_options,
                help="The specific structure of your research"
            )
            
            if methodology_type == "Quantitative":
                effect_size = st.select_slider(
                    "Expected Effect Size",
                    options=["Small (0.2)", "Medium (0.5)", "Large (0.8)"],
                    value="Medium (0.5)",
                    help="The expected magnitude of the relationship or difference"
                )
                
                power = st.slider(
                    "Desired Statistical Power",
                    min_value=0.7,
                    max_value=0.99,
                    value=0.8,
                    step=0.05,
                    format="%.2f",
                    help="The probability of detecting an effect if it exists (typically 0.8 or higher)"
                )
                
                alpha = st.select_slider(
                    "Significance Level (α)",
                    options=["0.10", "0.05", "0.01"],
                    value="0.05",
                    help="The probability of rejecting the null hypothesis when it is true (Type I error)"
                )
            else:
                # For qualitative, use simpler parameters
                effect_size = "N/A"
                power = 0.8
                alpha = "0.05"
                
                st.info("Note: Classical sample size calculations are less applicable to qualitative research, which focuses on depth rather than statistical power.")
                
                participant_range = st.slider(
                    "Expected Number of Participants",
                    min_value=5,
                    max_value=50,
                    value=(10, 20),
                    help="Typical range for qualitative studies"
                )
        
        with col2:
            st.markdown("### Sample Size Guidelines")
            
            if methodology_type == "Quantitative":
                st.markdown("""
                **General Quantitative Guidelines:**
                - Experimental studies: 30+ per group
                - Correlational studies: 50+ participants
                - Survey research: 100+ participants
                - Factor analysis: 5-10 participants per variable
                
                **Statistical Power:**
                - 0.8 is standard (80% chance of detecting effect)
                - Higher power requires larger samples
                
                **Effect Size:**
                - Small effects require larger samples
                - Large effects can be detected with smaller samples
                """)
            elif methodology_type == "Qualitative":
                st.markdown("""
                **Qualitative Sample Size Guidelines:**
                - Phenomenological: 5-25 participants
                - Ethnographic: 30-50 participants
                - Grounded Theory: 20-30 participants
                - Case Study: 1-10 cases
                
                **Saturation Principle:**
                Sampling until no new themes or information emerges is the primary guiding principle in qualitative research.
                
                **Factors Affecting Sample Size:**
                - Study scope and complexity
                - Data quality and richness
                - Participant homogeneity
                """)
            else:  # Mixed Methods
                st.markdown("""
                **Mixed Methods Considerations:**
                - Quantitative component follows statistical guidelines
                - Qualitative component follows saturation principles
                - Sequential designs may adjust second phase based on first phase results
                - Convergent designs need sufficient sample for both approaches
                
                **Integration Strategy:**
                Consider how quantitative and qualitative data will be integrated when determining sample sizes.
                """)
        
        # Sample size calculation button
        if st.button("Calculate Recommended Sample Size"):
            with st.spinner("Calculating sample size recommendation..."):
                calculation_data = generate_sample_size_calculation(
                    methodology_type,
                    design_type,
                    effect_size,
                    power,
                    alpha
                )
                
                # Display results with visual elements
                st.success("✅ Sample size calculation complete!")
                
                st.markdown("### Calculation Results")
                
                # Highlight the calculated sample size
                st.markdown(f"""
                <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #4361ee;">
                    <h3 style="margin-top: 0;">Recommended Sample Size</h3>
                    <p style="font-size: 24px; font-weight: bold;">{calculation_data["calculated_sample_size"]}</p>
                    <p><strong>Formula used:</strong> {calculation_data["formula"]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional recommendations
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Minimum Sample Size")
                    st.info(f"🔢 {calculation_data['min_recommendation']}")
                
                with col2:
                    st.markdown("### Optimal Sample Size")
                    st.info(f"🔢 {calculation_data['optimal_recommendation']}")
                
                # Explanation
                st.markdown("### Explanation")
                st.markdown(calculation_data["explanation"])
                
                # Visualization of sample size and power
                if methodology_type == "Quantitative":
                    st.subheader("Sample Size vs. Statistical Power")
                    
                    # Create sample visualization
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    # Example curve showing relationship between sample size and power
                    # This is a simplified visualization
                    sample_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                    
                    # Power curves for different effect sizes
                    power_small = [0.2, 0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 0.7, 0.72, 0.75]
                    power_medium = [0.4, 0.55, 0.65, 0.75, 0.8, 0.85, 0.88, 0.9, 0.92, 0.94]
                    power_large = [0.6, 0.75, 0.85, 0.9, 0.93, 0.95, 0.96, 0.97, 0.98, 0.99]
                    
                    ax.plot(sample_sizes, power_small, label="Small effect size (0.2)", marker='o')
                    ax.plot(sample_sizes, power_medium, label="Medium effect size (0.5)", marker='s')
                    ax.plot(sample_sizes, power_large, label="Large effect size (0.8)", marker='^')
                    
                    # Add line for conventional 0.8 power threshold
                    ax.axhline(y=0.8, color='r', linestyle='--', alpha=0.7)
                    ax.text(101, 0.81, "0.8 Power Threshold", fontsize=10, color='r')
                    
                    ax.set_xlabel("Sample Size (n)")
                    ax.set_ylabel("Statistical Power (1-β)")
                    ax.set_title("Relationship Between Sample Size and Statistical Power")
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    
                    st.pyplot(fig)
    
    # Tab 4: Methodology Templates
    elif st.session_state.active_methodology_tab == "Methodology Templates":
        st.subheader("Research Methodology Templates")
        
        st.markdown("""
        Browse methodology templates for different research approaches. These templates provide
        structured frameworks that you can adapt for your specific research context.
        """)
        
        # Select methodology type
        methodology_type = st.selectbox(
            "Select Methodology Type",
            ["Quantitative", "Qualitative", "Mixed Methods"]
        )
        
        # Display templates for the selected methodology
        templates = st.session_state.methodology_templates[methodology_type]
        
        for method, description in templates.items():
            with st.expander(f"{method} Methodology"):
                st.markdown(f"### {method}")
                st.markdown(description)
                
                # Generate detailed template
                if st.button(f"Generate Detailed {method} Template", key=f"btn_{method}"):
                    with st.spinner(f"Generating {method} template..."):
                        prompt = f"""
                        Create a detailed research methodology template for a {methodology_type} study using {method} approach.
                        
                        Include the following sections:
                        1. Research Design Overview
                        2. Participants/Sampling
                        3. Data Collection Procedures
                        4. Instruments/Measures
                        5. Data Analysis
                        6. Validity/Reliability Considerations
                        7. Ethical Considerations
                        
                        Format as a structured template that a researcher could adapt to their specific study.
                        """
                        
                        try:
                            response = openai.ChatCompletion.create(
                                model="gpt-4",
                                messages=[
                                    {"role": "system", "content": "You are a research methodology specialist creating structured templates."},
                                    {"role": "user", "content": prompt}
                                ],
                                temperature=0.7,
                                max_tokens=1000
                            )
                            
                            template_text = response.choices[0].message.content.strip()
                            st.markdown(template_text)
                            
                            # Add download button for the template
                            st.download_button(
                                label="📥 Download Template",
                                data=template_text,
                                file_name=f"{method}_methodology_template.txt",
                                mime="text/plain"
                            )
                            
                        except Exception as e:
                            st.error(f"Error generating template: {str(e)}")
                            # Provide fallback content for the template
                            st.markdown("""
                            # Sample Methodology Template
                            
                            ## 1. Research Design Overview
                            [Describe the overall design and approach]
                            
                            ## 2. Participants/Sampling
                            [Describe the target population, sampling method, and sample characteristics]
                            
                            ## 3. Data Collection Procedures
                            [Detail the step-by-step procedures for collecting data]
                            
                            ## 4. Instruments/Measures
                            [Describe the tools, instruments, and measures used]
                            
                            ## 5. Data Analysis
                            [Explain the analytical approach and techniques]
                            
                            ## 6. Validity/Reliability Considerations
                            [Address how validity and reliability will be ensured]
                            
                            ## 7. Ethical Considerations
                            [Detail ethical procedures, approvals, and protections]
                            """)
        
        # Methodology comparison chart
        st.subheader("Methodology Comparison")
        
        # Create comparison data for various methodologies
        comparison_data = {
            "Criteria": [
                "Research Questions",
                "Data Type",
                "Sample Size",
                "Analysis Approach",
                "Validity Focus",
                "Generalizability",
                "Researcher Role"
            ],
            "Quantitative": [
                "Relationship, difference, prediction",
                "Numerical",
                "Large (30+)",
                "Statistical",
                "Internal, external, construct",
                "High, if properly sampled",
                "Objective, detached"
            ],
            "Qualitative": [
                "Understanding, meaning, process",
                "Textual, observational",
                "Small (5-30)",
                "Thematic, interpretive",
                "Trustworthiness, authenticity",
                "Transferability to similar contexts",
                "Involved, interpretive"
            ],
            "Mixed Methods": [
                "Complex, multi-faceted",
                "Numerical and textual",
                "Varies by component",
                "Integrated, multi-method",
                "Multiple validities",
                "Context-dependent",
                "Adaptive, flexible"
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
    
    # Tab 5: Draft Generator
    elif st.session_state.active_methodology_tab == "Draft Generator":
        st.subheader("Methodology Section Draft Generator")
        
        st.markdown("""
        Generate a complete methodology section draft for your research paper or proposal.
        This tool creates a structured academic methodology section based on your inputs.
        """)
        
        # Input fields for the generator
        research_question = st.text_area(
            "Research Question",
            placeholder="e.g., What is the effect of X on Y?",
            help="The main question your research aims to answer"
        )
        
        methodology_options = ["Quantitative", "Qualitative", "Mixed Methods"]
        methodology_type = st.selectbox(
            "Methodology Type",
            methodology_options,
            help="The overall methodological approach for your research"
        )
        
        # Show specific design options based on methodology type
        if methodology_type == "Quantitative":
            design_options = ["Experimental", "Correlational", "Survey", "Observational"]
        elif methodology_type == "Qualitative":
            design_options = ["Phenomenological", "Ethnographic", "Grounded Theory", "Case Study"]
        else:  # Mixed Methods
            design_options = ["Sequential Explanatory", "Sequential Exploratory", "Convergent Parallel", "Embedded"]
        
        research_design = st.selectbox(
            "Research Design",
            design_options,
            help="The specific structure of your research"
        )
        
        population = st.text_input(
            "Target Population",
            placeholder="e.g., Undergraduate students aged 18-25",
            help="The population from which you will draw your sample"
        )
        
        sample_strategy = st.selectbox(
            "Sampling Strategy",
            ["Random Sampling", "Stratified Sampling", "Convenience Sampling", 
             "Purposive Sampling", "Cluster Sampling", "Snowball Sampling"],
            help="The approach used to select participants for your study"
        )
        
        # Generate draft button
        if st.button("Generate Methodology Section Draft"):
            if research_question:
                with st.spinner("Generating methodology section draft..."):
                    methodology_draft = generate_methodology_section(
                        research_question, 
                        methodology_type, 
                        research_design
                    )
                    
                    st.success("✅ Methodology section draft generated!")
                    
                    # Display the methodology draft
                    st.markdown("### Methodology Section Draft")
                    st.markdown(methodology_draft)
                    
                    # Add download button for the methodology draft
                    st.download_button(
                        label="📥 Download Methodology Draft",
                        data=methodology_draft,
                        file_name="methodology_section_draft.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
                    # Add editing options
                    st.subheader("Edit or Refine Your Draft")
                    st.write("Use the feedback below to guide your revisions:")
                    
                    # Provide checklist for methodology sections
                    methodology_checklist = {
                        "Research Design": "✓ Clearly described and justified",
                        "Sampling": "✓ Target population and sampling strategy defined",
                        "Data Collection": "✓ Procedures and instruments outlined",
                        "Data Analysis": "✓ Analytical approach specified",
                        "Validity/Reliability": "✓ Quality assurance measures addressed",
                        "Ethics": "✓ Ethical considerations included"
                    }
                    
                    for section, status in methodology_checklist.items():
                        st.write(f"{status} - {section}")
                    
                    # Option to refine with specific instructions
                    refine_instructions = st.text_area(
                        "Enter specific revision instructions (optional)",
                        placeholder="e.g., Add more detail about the sampling procedure"
                    )
                    
                    if refine_instructions and st.button("Refine Draft"):
                        with st.spinner("Refining methodology draft..."):
                            refine_prompt = f"""
                            Refine the following methodology section based on these instructions: 
                            "{refine_instructions}"
                            
                            Original methodology section:
                            {methodology_draft}
                            """
                            
                            try:
                                response = openai.ChatCompletion.create(
                                    model="gpt-4",
                                    messages=[
                                        {"role": "system", "content": "You are a research methodology specialist refining academic methodology sections."},
                                        {"role": "user", "content": refine_prompt}
                                    ],
                                    temperature=0.7,
                                    max_tokens=1200
                                )
                                
                                refined_draft = response.choices[0].message.content.strip()
                                st.success("✅ Methodology draft refined!")
                                
                                # Display the refined methodology draft
                                st.markdown("### Refined Methodology Section")
                                st.markdown(refined_draft)
                                
                                # Add download button for the refined methodology draft
                                st.download_button(
                                    label="📥 Download Refined Draft",
                                    data=refined_draft,
                                    file_name="refined_methodology_section.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                                
                            except Exception as e:
                                st.error(f"Error refining draft: {str(e)}")
            else:
                st.warning("Please enter a research question first.")

# For testing the module independently
if __name__ == "__main__":
    # Set API key (for testing)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Display the interface
    display_methodology_guidance()
