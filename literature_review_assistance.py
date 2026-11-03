import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import json
import re
import textwrap
import io
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

def generate_lorem_ipsum(paragraphs=1, sentences_per_paragraph=5):
    """Generate lorem ipsum text for demonstrations"""
    sentences = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Nulla facilisi. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia.",
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem.",
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
        "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.",
        "Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam.",
        "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis."
    ]
    
    result = ""
    for p in range(paragraphs):
        para_sentences = random.sample(sentences, min(sentences_per_paragraph, len(sentences)))
        result += " ".join(para_sentences) + "\n\n"
    
    return result.strip()

def generate_sample_papers(search_query, count=5):
    """Generate sample papers for demonstration"""
    paper_titles = [
        f"A Comprehensive Review of {search_query}",
        f"Recent Advances in {search_query}",
        f"Empirical Analysis of {search_query}",
        f"Theoretical Foundations of {search_query}",
        f"Applications of {search_query} in Education",
        f"Novel Approaches to {search_query}",
        f"{search_query}: A Systematic Review",
        f"Comparing Methodologies in {search_query}",
        f"Future Directions for {search_query} Research",
        f"Meta-Analysis of {search_query} Studies"
    ]
    
    journals = [
        "Journal of Research Studies",
        "International Journal of Science",
        "Data Science Journal",
        "Theoretical Computer Science",
        "Educational Technology Research",
        "Journal of Applied Sciences",
        "Research Quarterly",
        "Annual Review of Technology",
        "Computational Research Journal",
        "Journal of Advanced Studies"
    ]
    
    authors_list = [
        "Johnson, A., & Williams, B.",
        "Smith, C., Garcia, D., & Lee, E.",
        "Brown, F., Wilson, G.",
        "Martinez, H., & Anderson, I.",
        "Taylor, J., Robinson, K., & Lewis, L.",
        "Davis, M., & Thompson, N.",
        "Harris, O., & King, P.",
        "Allen, Q., & Young, R.",
        "Mitchell, S., & Turner, T.",
        "Cooper, U., & Walker, V."
    ]
    
    sample_papers = []
    for i in range(min(count, len(paper_titles))):
        sample_papers.append({
            "title": paper_titles[i],
            "authors": authors_list[i % len(authors_list)],
            "journal": journals[i % len(journals)],
            "year": str(random.randint(2018, 2023)),
            "abstract": f"This {random.choice(['paper', 'study', 'research', 'work'])} {random.choice(['presents', 'describes', 'explores', 'investigates'])} {random.choice(['a comprehensive', 'an in-depth', 'a detailed', 'a thorough'])} {random.choice(['analysis', 'review', 'examination', 'study'])} of {search_query} and its {random.choice(['applications', 'implications', 'effects', 'impact'])} in various fields...",
            "citations": random.randint(10, 200),
            "url": f"https://example.com/paper{i+1}"
        })
    
    return sample_papers

def display_search_and_discovery():
    """Display the search and discovery interface for literature review"""
    st.subheader("Search & Discover Research Papers")
    
    # Search form
    search_query = st.text_input("Enter research topic or keywords")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search_filters = st.multiselect(
            "Filters",
            ["Peer-reviewed only", "Open access", "Last 5 years", "Last 10 years", 
             "Review articles", "Journal articles", "Conference papers", "Highly cited"]
        )
    
    with col2:
        search_sort = st.selectbox(
            "Sort by",
            ["Relevance", "Date (newest first)", "Citation count", "Impact factor"]
        )
    
    with col3:
        search_databases = st.multiselect(
            "Databases",
            ["Google Scholar", "PubMed", "IEEE Xplore", "ACM Digital Library", 
             "Scopus", "Web of Science", "arXiv", "JSTOR"],
            default=["Google Scholar"]
        )
    
    # Search button
    if st.button("Search") and search_query:
        with st.spinner(f"Searching for: {search_query}"):
            # In a real implementation, this would connect to academic databases
            # For demonstration, we'll create some sample results
            st.success(f"Found 137 papers matching '{search_query}'")
            
            # Generate sample search results
            sample_papers = generate_sample_papers(search_query)
            
            # Display search results
            for i, paper in enumerate(sample_papers):
                with st.expander(f"{paper['title']} ({paper['year']})"):
                    st.write(f"**Authors:** {paper['authors']}")
                    st.write(f"**Journal:** {paper['journal']}")
                    st.write(f"**Citations:** {paper['citations']}")
                    st.write(f"**Abstract:** {paper['abstract']}")
                    
                    col1, col2 = st.columns([3, 1])
                            
                    with col1:
                        # Actions for the paper
                        button_cols = st.columns(4)
                        with button_cols[0]:
                            if st.button("Save", key=f"save_paper_{i}"):
                                st.success(f"Paper '{paper['title']}' saved to your library!")
                        with button_cols[1]:
                            if st.button("Cite", key=f"cite_paper_{i}"):
                                citation = f"{paper['authors']} ({paper['year']}). {paper['title']}. {paper['journal']}."
                                st.markdown(f"<div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px;'>{citation}</div>", unsafe_allow_html=True)
                        with button_cols[2]:
                            if st.button("PDF", key=f"pdf_paper_{i}"):
                                st.info(f"Retrieving PDF for '{paper['title']}'...")
                        with button_cols[3]:
                            if st.button("Related", key=f"related_paper_{i}"):
                                st.info(f"Finding papers related to '{paper['title']}'...")
                    
                    with col2:
                        # Display relevance score
                        relevance = random.randint(75, 95)  # Random score for demonstration
                        st.markdown(f"<div style='background-color: {'#c6efce' if relevance > 85 else '#ffeb9c'}; padding: 10px; border-radius: 5px; text-align: center;'><span style='font-size: 24px; font-weight: bold;'>{relevance}%</span><br>Relevance</div>", unsafe_allow_html=True)
            
            # Export search results
            if "sample_papers" in locals():
                st.download_button(
                    label="Export Search Results",
                    data=json.dumps([{k: v for k, v in paper.items() if k != 'abstract'} for paper in sample_papers], indent=2),
                    file_name="search_results.json",
                    mime="application/json"
                )

def display_paper_analyzer():
    """Display the paper analyzer interface for literature review"""
    st.subheader("Research Paper Analyzer")
    
    # Upload a paper to analyze
    uploaded_paper = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"])
    paper_url = st.text_input("Or enter paper URL/DOI")
    
    if uploaded_paper is not None or paper_url:
        source = "uploaded PDF" if uploaded_paper is not None else f"URL: {paper_url}"
        st.success(f"Paper from {source} ready for analysis!")
        
        # Analysis options
        st.subheader("Analysis Options")
        analysis_options = st.multiselect(
            "Select Analysis Types",
            ["Key Findings", "Methodology Analysis", "Term Extraction", 
             "Citation Network", "Visual Elements", "Research Gaps", 
             "Critical Evaluation"],
            default=["Key Findings", "Methodology Analysis", "Term Extraction"]
        )
        
        if st.button("Analyze Paper"):
            with st.spinner("Analyzing research paper..."):
                # Show progress
                progress_bar = st.progress(0)
                for i in range(101):
                    time.sleep(0.01)  # Simulate analysis time
                    progress_bar.progress(i)
                
                st.success("Analysis complete!")
                
                # Create tabs for different analysis results
                analysis_tabs = st.tabs([option for option in analysis_options])
                
                # Example analysis results for each selected option
                for i, option in enumerate(analysis_options):
                    with analysis_tabs[i]:
                        if option == "Key Findings":
                            st.subheader("Key Findings and Contributions")
                            st.markdown("""
                            1. **Primary Finding**: The paper demonstrates a 23% improvement in accuracy for classification tasks.
                            
                            2. **Novel Method**: Introduces a hybrid approach combining transformer-based models with statistical techniques.
                            
                            3. **Dataset Contribution**: Creates and shares a new benchmark dataset with 50,000 labeled examples.
                            
                            4. **Performance Gains**: Achieves state-of-the-art results on 3 out of 5 standard benchmarks.
                            
                            5. **Efficiency Improvement**: Reduces training time by 35% without loss in performance.
                            """)
                            
                            # Sentiment/impact analysis
                            st.markdown("### Significance Analysis")
                            fig, ax = plt.subplots(1, 1, figsize=(8, 4))
                            
                            # Example sentiment data
                            categories = ['Novelty', 'Technical Merit', 'Empirical Strength', 'Theoretical Foundation', 'Practical Impact']
                            values = [85, 92, 78, 63, 89]
                            
                            ax.bar(categories, values, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
                            ax.set_ylim(0, 100)
                            ax.set_title("Contribution Assessment")
                            ax.set_ylabel("Score")
                            plt.xticks(rotation=45, ha="right")
                            plt.tight_layout()
                            st.pyplot(fig)
                        
                        elif option == "Methodology Analysis":
                            st.subheader("Research Methodology Analysis")
                            
                            # Methodology overview
                            st.markdown("""
                            ### Methodology Classification
                            - **Primary Approach**: Quantitative, Experimental Research
                            - **Data Collection**: Automated from public datasets + custom collection
                            - **Validation Method**: 5-fold cross-validation
                            - **Statistical Techniques**: ANOVA, t-tests, bootstrap sampling
                            - **Reproducibility**: Code and data published on GitHub
                            """)
                            
                            # Methodology strengths and weaknesses
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("### Strengths")
                                st.markdown("""
                                - Rigorous experimental design
                                - Comprehensive comparison with baselines
                                - Thorough ablation studies
                                - Statistical significance testing
                                - Multiple datasets for validation
                                """)
                            
                            with col2:
                                st.markdown("### Limitations")
                                st.markdown("""
                                - Limited demographic diversity in dataset
                                - No qualitative analysis component
                                - Short-term evaluation only (no longitudinal data)
                                - Limited discussion of ethical implications
                                - Hardware dependencies may limit reproducibility
                                """)
                            
                            # Visualization of method components
                            st.markdown("### Methodology Components")
                            fig, ax = plt.subplots(1, 1, figsize=(8, 5))
                            
                            # Example data
                            methods = ['Data Prep', 'Model Training', 'Evaluation', 'Ablation Study', 'Comparison']
                            thoroughness = [90, 85, 75, 60, 95]
                            detail = [85, 90, 80, 65, 75]
                            
                            x = np.arange(len(methods))
                            width = 0.35
                            
                            ax.bar(x - width/2, thoroughness, width, label='Thoroughness')
                            ax.bar(x + width/2, detail, width, label='Detail Level')
                            
                            ax.set_xticks(x)
                            ax.set_xticklabels(methods)
                            plt.xticks(rotation=45, ha="right")
                            ax.legend()
                            ax.set_ylim(0, 100)
                            ax.set_title("Methodology Completeness Assessment")
                            plt.tight_layout()
                            st.pyplot(fig)
                        
                        elif option == "Term Extraction":
                            st.subheader("Key Terms and Concepts")
                            
                            # Example extracted terms with frequency
                            terms = [
                                {"term": "Neural Network", "frequency": 37, "context": "model architecture, performance comparison"},
                                {"term": "Transfer Learning", "frequency": 24, "context": "methodology, literature review"},
                                {"term": "Feature Extraction", "frequency": 19, "context": "data processing, methodology"},
                                {"term": "Classification Accuracy", "frequency": 31, "context": "results, evaluation metrics"},
                                {"term": "Benchmark Dataset", "frequency": 15, "context": "methodology, results"},
                                {"term": "Gradient Descent", "frequency": 12, "context": "methodology, model optimization"},
                                {"term": "Overfitting", "frequency": 8, "context": "limitations, methodology"},
                                {"term": "Cross-validation", "frequency": 17, "context": "evaluation, methodology"}
                            ]
                            
                            # Display in a table
                            terms_df = pd.DataFrame(terms)
                            st.dataframe(terms_df)
                            
                            # Generate and display a word cloud
                            st.markdown("### Term Frequency Visualization")
                            
                            # Create a word cloud
                            try:
                                # Create a dictionary of terms and frequencies
                                term_freq = {term["term"]: term["frequency"] for term in terms}
                                
                                # Generate the word cloud
                                wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(term_freq)
                                
                                # Display the word cloud
                                fig, ax = plt.subplots(figsize=(10, 5))
                                ax.imshow(wordcloud, interpolation='bilinear')
                                ax.axis('off')
                                st.pyplot(fig)
                            except Exception:
                                # Fallback if WordCloud fails
                                fig, ax = plt.subplots(figsize=(10, 5))
                                terms_sorted = sorted(terms, key=lambda x: x["frequency"], reverse=True)
                                ax.barh([t["term"] for t in terms_sorted], [t["frequency"] for t in terms_sorted], color='skyblue')
                                ax.set_title("Key Term Frequency")
                                ax.set_xlabel("Frequency")
                                plt.tight_layout()
                                st.pyplot(fig)
                            
                            # Term relationships
                            st.markdown("### Term Co-occurrence")
                            
                            # Generate a simple co-occurrence network
                            G = nx.Graph()
                            for term in terms:
                                G.add_node(term["term"], weight=term["frequency"])
                            
                            # Add some example edges
                            edges = [
                                ("Neural Network", "Feature Extraction", 0.7),
                                ("Neural Network", "Classification Accuracy", 0.8),
                                ("Neural Network", "Overfitting", 0.6),
                                ("Transfer Learning", "Neural Network", 0.5),
                                ("Feature Extraction", "Classification Accuracy", 0.4),
                                ("Benchmark Dataset", "Classification Accuracy", 0.3),
                                ("Gradient Descent", "Neural Network", 0.7),
                                ("Cross-validation", "Overfitting", 0.5),
                                ("Cross-validation", "Benchmark Dataset", 0.4)
                            ]
                            
                            for source, target, weight in edges:
                                G.add_edge(source, target, weight=weight)
                            
                            # Create a Plotly network graph
                            try:
                                pos = nx.spring_layout(G, seed=42)
                                
                                edge_trace = go.Scatter(
                                    x=[],
                                    y=[],
                                    line=dict(width=0.5, color='#888'),
                                    hoverinfo='none',
                                    mode='lines')
                                
                                for edge in G.edges():
                                    x0, y0 = pos[edge[0]]
                                    x1, y1 = pos[edge[1]]
                                    edge_trace['x'] += (x0, x1, None)
                                    edge_trace['y'] += (y0, y1, None)
                                
                                node_trace = go.Scatter(
                                    x=[],
                                    y=[],
                                    text=[],
                                    mode='markers',
                                    hoverinfo='text',
                                    marker=dict(
                                        showscale=True,
                                        colorscale='YlGnBu',
                                        size=[],
                                        color=[],
                                        colorbar=dict(
                                            thickness=15,
                                            title='Node Connections',
                                            xanchor='left',
                                            titleside='right'
                                        ),
                                        line=dict(width=2)))
                                
                                for node in G.nodes():
                                    x, y = pos[node]
                                    node_trace['x'] += (x,)
                                    node_trace['y'] += (y,)
                                
                                for node, adjacencies in enumerate(G.adjacency()):
                                    node_name = adjacencies[0]
                                    node_weight = G.nodes[node_name]['weight']
                                    node_trace['marker']['size'] += (node_weight / 2,)
                                    node_connections = len(adjacencies[1])
                                    node_trace['marker']['color'] += (node_connections,)
                                    node_info = f'{node_name}<br>Frequency: {node_weight}<br># of connections: {node_connections}'
                                    node_trace['text'] += (node_info,)
                                
                                fig = go.Figure(data=[edge_trace, node_trace],
                                             layout=go.Layout(
                                                title='Term Co-occurrence Network',
                                                titlefont=dict(size=16),
                                                showlegend=False,
                                                hovermode='closest',
                                                margin=dict(b=20,l=5,r=5,t=40),
                                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
                                
                                st.plotly_chart(fig, use_container_width=True)
                            except:
                                st.info("Unable to generate co-occurrence network visualization. Showing text-based relationship information instead.")
                                for source, target, weight in edges:
                                    st.write(f"**{source}** is related to **{target}** (strength: {weight:.1f})")
                            
                            # Example of term definitions
                            st.markdown("### Key Term Definitions")
                            for term in terms[:3]:  # Just show a few definitions
                                with st.expander(f"{term['term']}"):
                                    st.write(f"Found {term['frequency']} mentions in contexts: {term['context']}")
                                    st.write("Definition: " + generate_lorem_ipsum(1, 3))  # Placeholder definition
                        
                        elif option == "Citation Network":
                            st.subheader("Citation Analysis")
                            
                            # Citation statistics
                            st.markdown("### Citation Statistics")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Citations", "47")
                            with col2:
                                st.metric("Self-Citations", "6 (12.8%)")
                            with col3:
                                st.metric("Recent Citations (≤ 3 years)", "28 (59.6%)")
                            
                            # Most cited references
                            st.markdown("### Top Cited Works")
                            top_refs = [
                                {"authors": "Smith et al.", "year": 2020, "title": "A Comprehensive Survey of Neural Networks", "citations": 743},
                                {"authors": "Johnson & Williams", "year": 2019, "title": "Transfer Learning Approaches", "citations": 582},
                                {"authors": "Garcia et al.", "year": 2021, "title": "Benchmark Datasets for Classification", "citations": 324},
                                {"authors": "Brown & Taylor", "year": 2018, "title": "Feature Extraction Methods", "citations": 501},
                                {"authors": "Martinez et al.", "year": 2020, "title": "Evaluation Metrics for ML Models", "citations": 289}
                            ]
                            
                            # Display in a table
                            st.table(pd.DataFrame(top_refs))
                            
                            # Citation network visualization
                            st.markdown("### Citation Network Visualization")
                            
                            # Create a simple directed graph
                            G = nx.DiGraph()
                            
                            # Add nodes (papers)
                            papers = ["Current Paper"] + [f"{ref['authors'].split(',')[0]} ({ref['year']})" for ref in top_refs]
                            for paper in papers:
                                G.add_node(paper)
                            
                            # Add some example edges (citations)
                            edges = [
                                ("Current Paper", papers[1]),
                                ("Current Paper", papers[2]),
                                ("Current Paper", papers[3]),
                                ("Current Paper", papers[4]),
                                ("Current Paper", papers[5]),
                                (papers[2], papers[3]),
                                (papers[2], papers[4]),
                                (papers[2], papers[5]),
                                (papers[3], papers[5]),
                                (papers[4], papers[5])
                            ]
                            
                            for source, target in edges:
                                G.add_edge(source, target)
                            
                            # Generate network layout
                            try:
                                pos = nx.spring_layout(G, seed=42)
                                
                                # Create a Plotly network visualization
                                edge_x = []
                                edge_y = []
                                for edge in G.edges():
                                    x0, y0 = pos[edge[0]]
                                    x1, y1 = pos[edge[1]]
                                    edge_x.extend([x0, x1, None])
                                    edge_y.extend([y0, y1, None])
                                
                                edge_trace = go.Scatter(
                                    x=edge_x, y=edge_y,
                                    line=dict(width=0.5, color='#888'),
                                    hoverinfo='none',
                                    mode='lines')
                                
                                node_x = []
                                node_y = []
                                node_text = []
                                node_size = []
                                node_color = []
                                
                                for node in G.nodes():
                                    x, y = pos[node]
                                    node_x.append(x)
                                    node_y.append(y)
                                    node_text.append(node)
                                    
                                    # Size based on in-degree (citations)
                                    size = 15 + G.in_degree(node) * 5
                                    node_size.append(size)
                                    
                                    # Color: current paper is different
                                    if node == "Current Paper":
                                        node_color.append('#FF5733')  # Orange for current paper
                                    else:
                                        node_color.append('#6175E0')  # Blue for references
                                
                                node_trace = go.Scatter(
                                    x=node_x, y=node_y,
                                    mode='markers',
                                    hoverinfo='text',
                                    text=node_text,
                                    marker=dict(
                                        color=node_color,
                                        size=node_size,
                                        line=dict(width=2, color='#333')
                                    )
                                )
                                
                                # Create the figure
                                fig = go.Figure(
                                    data=[edge_trace, node_trace],
                                    layout=go.Layout(
                                        title='Citation Network',
                                        titlefont=dict(size=16),
                                        showlegend=False,
                                        hovermode='closest',
                                        margin=dict(b=20, l=5, r=5, t=40),
                                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                                    )
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                # Create a simple matplotlib visualization as fallback
                                st.info("Interactive network visualization not available. Showing simplified citation graph.")
                                fig, ax = plt.subplots(figsize=(10, 8))
                                nx.draw(G, pos=nx.spring_layout(G, seed=42), with_labels=True, 
                                       node_color=['orange' if n == 'Current Paper' else 'skyblue' for n in G.nodes()],
                                       node_size=[300 + G.in_degree(n) * 50 for n in G.nodes()],
                                       font_size=8, font_weight='bold', arrows=True, ax=ax)
                                st.pyplot(fig)
                        
                        elif option == "Visual Elements":
                            st.subheader("Figures and Tables Analysis")
                            
                            # Summary of visual elements
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Figures", "8")
                            with col2:
                                st.metric("Total Tables", "5")
                            with col3:
                                st.metric("Equations", "12")
                            
                            # List and description of figures
                            st.markdown("### Key Figures")
                            figures = [
                                {"id": "Fig. 1", "caption": "System Architecture", "type": "Diagram"},
                                {"id": "Fig. 2", "caption": "Performance Comparison", "type": "Bar Chart"},
                                {"id": "Fig. 3", "caption": "Learning Curve", "type": "Line Graph"},
                                {"id": "Fig. 4", "caption": "Feature Importance", "type": "Heat Map"},
                                {"id": "Fig. 5", "caption": "Error Analysis", "type": "Scatter Plot"}
                            ]
                            
                            # Generate example images for each figure
                            for idx, fig in enumerate(figures):
                                with st.expander(f"{fig['id']}: {fig['caption']} ({fig['type']})"):
                                    # Generate a simple placeholder image based on the figure type
                                    if fig['type'] == "Bar Chart":
                                        data = np.random.rand(5) * 100
                                        categories = ['Model A', 'Model B', 'Model C', 'Model D', 'Model E']
                                        fig_plt, ax = plt.subplots(figsize=(8, 4))
                                        ax.bar(categories, data)
                                        ax.set_ylabel("Performance")
                                        ax.set_title(fig['caption'])
                                        st.pyplot(fig_plt)
                                    
                                    elif fig['type'] == "Line Graph":
                                        x = np.linspace(0, 10, 100)
                                        y = 1 - np.exp(-x/3)
                                        fig_plt, ax = plt.subplots(figsize=(8, 4))
                                        ax.plot(x, y)
                                        ax.set_xlabel("Epochs")
                                        ax.set_ylabel("Accuracy")
                                        ax.set_title(fig['caption'])
                                        st.pyplot(fig_plt)
                                    
                                    elif fig['type'] == "Heat Map":
                                        data = np.random.rand(10, 10)
                                        fig_plt, ax = plt.subplots(figsize=(8, 6))
                                        im = ax.imshow(data, cmap='viridis')
                                        ax.set_title(fig['caption'])
                                        plt.colorbar(im)
                                        st.pyplot(fig_plt)
                                    
                                    elif fig['type'] == "Scatter Plot":
                                        x = np.random.rand(50) * 10
                                        y = x + np.random.normal(0, 1, 50)
                                        fig_plt, ax = plt.subplots(figsize=(8, 4))
                                        ax.scatter(x, y)
                                        ax.set_xlabel("Predicted")
                                        ax.set_ylabel("Actual")
                                        ax.set_title(fig['caption'])
                                        st.pyplot(fig_plt)
                                    
                                    else:  # Diagram or other type
                                        # Create a simple placeholder diagram
                                        img = Image.new('RGB', (800, 400), color='white')
                                        d = ImageDraw.Draw(img)
                                        
                                        # Draw some shapes based on figure type
                                        if fig['type'] == "Diagram":
                                            # Draw boxes and arrows for system architecture
                                            box_positions = [(100, 150, 200, 200), (350, 100, 450, 150), 
                                                            (350, 200, 450, 250), (600, 150, 700, 200)]
                                            box_labels = ["Input", "Process A", "Process B", "Output"]
                                            
                                            for i, (x1, y1, x2, y2) in enumerate(box_positions):
                                                d.rectangle((x1, y1, x2, y2), outline="black", width=2)
                                                d.text((x1+10, y1+10), box_labels[i], fill="black")
                                            
                                            # Draw arrows
                                            d.line((200, 175, 350, 125), fill="black", width=2)
                                            d.line((200, 175, 350, 225), fill="black", width=2)
                                            d.line((450, 125, 600, 175), fill="black", width=2)
                                            d.line((450, 225, 600, 175), fill="black", width=2)
                                        else:
                                            # Generic image with figure caption
                                            d.text((20, 20), f"{fig['id']}: {fig['caption']}", fill="black")
                                            d.rectangle((50, 50, 750, 350), outline="black")
                                            d.text((400, 200), "Figure Content", fill="black")
                                        
                                        # Convert to bytes and display
                                        buf = io.BytesIO()
                                        img.save(buf, format='PNG')
                                        st.image(buf, caption=fig['caption'])
                                    
                                    st.write("Visual complexity: Medium")
                                    st.write("Information content: High")
                            
                            # Tables analysis
                            st.markdown("### Key Tables")
                            tables = [
                                {"id": "Table 1", "caption": "Dataset Statistics"},
                                {"id": "Table 2", "caption": "Model Hyperparameters"},
                                {"id": "Table 3", "caption": "Benchmark Results"},
                                {"id": "Table 4", "caption": "Ablation Study Results"},
                                {"id": "Table 5", "caption": "Computational Requirements"}
                            ]
                            
                            for i, table in enumerate(tables):
                                with st.expander(f"{table['id']}: {table['caption']}"):
                                    # Generate example data based on table type
                                    if table['caption'] == "Dataset Statistics":
                                        data = {
                                            "Dataset": ["Train", "Validation", "Test"],
                                            "Samples": [10000, 2000, 3000],
                                            "Classes": [10, 10, 10],
                                            "Avg. Length": [256, 256, 256],
                                            "Size (MB)": [150, 30, 45]
                                        }
                                    elif table['caption'] == "Model Hyperparameters":
                                        data = {
                                            "Parameter": ["Learning Rate", "Batch Size", "Epochs", "Hidden Layers", "Dropout"],
                                            "Value": [0.001, 64, 100, 3, 0.2],
                                            "Tuning Range": ["0.0001-0.01", "32-128", "50-200", "2-5", "0.1-0.5"]
                                        }
                                    elif table['caption'] == "Benchmark Results":
                                        data = {
                                            "Model": ["Baseline", "Previous SOTA", "Our Method", "Ablation 1", "Ablation 2"],
                                            "Accuracy (%)": [78.5, 85.3, 92.1, 87.6, 89.3],
                                            "F1 Score": [0.76, 0.83, 0.91, 0.86, 0.88],
                                            "Training Time (h)": [5.2, 8.7, 3.4, 3.2, 3.5]
                                        }
                                    elif table['caption'] == "Ablation Study Results":
                                        data = {
                                            "Component": ["Full Model", "No Component A", "No Component B", "No Component C"],
                                            "Accuracy (%)": [92.1, 87.6, 89.3, 90.5],
                                            "Relative Change (%)": [0, -4.5, -2.8, -1.6]
                                        }
                                    else:  # Computational Requirements
                                        data = {
                                            "Setting": ["Training", "Inference", "Fine-tuning"],
                                            "GPU Memory (GB)": [16, 4, 8],
                                            "CPU Cores": [32, 8, 16],
                                            "Time (h)": [24, 0.01, 4]
                                        }
                                    
                                    # Display as a table
                                    st.table(pd.DataFrame(data))
                                    st.write("Complexity: Medium")
                                    st.write("Data density: High")
                        
                        elif option == "Research Gaps":
                            st.subheader("Research Gaps and Future Work")
                            
                            # Identified gaps and limitations
                            st.markdown("### Explicitly Mentioned Limitations")
                            limitations = [
                                {"limitation": "Limited dataset diversity", "section": "Discussion", "severity": "High"},
                                {"limitation": "Computational complexity", "section": "Results", "severity": "Medium"},
                                {"limitation": "No comparison with newest methods", "section": "Related Work", "severity": "Low"},
                                {"limitation": "Domain-specific application only", "section": "Conclusion", "severity": "Medium"}
                            ]
                            
                            # Display as a table
                            st.dataframe(pd.DataFrame(limitations))
                            
                            # Future work
                            st.markdown("### Future Work Suggestions")
                            future_work = [
                                {"suggestion": "Extend to multi-modal data", "feasibility": "Medium", "potential_impact": "High"},
                                {"suggestion": "Reduce computational requirements", "feasibility": "High", "potential_impact": "Medium"},
                                {"suggestion": "Explore cross-domain applications", "feasibility": "Medium", "potential_impact": "High"},
                                {"suggestion": "Longitudinal validation study", "feasibility": "Low", "potential_impact": "High"}
                            ]
                            
                            # Display as a table
                            st.dataframe(pd.DataFrame(future_work))
                            
                            # Opportunity assessment
                            st.markdown("### Research Opportunity Assessment")
                            opportunities = [
                                {"opportunity": "Dataset expansion", "competition": "Low", "novelty": "Medium", "effort": "High"},
                                {"opportunity": "Algorithm optimization", "competition": "High", "novelty": "Medium", "effort": "Medium"},
                                {"opportunity": "Theoretical foundations", "competition": "Medium", "novelty": "High", "effort": "High"},
                                {"opportunity": "Application to new domains", "competition": "Medium", "novelty": "High", "effort": "Medium"}
                            ]
                            
                            # Display as a table
                            st.dataframe(pd.DataFrame(opportunities))
                            
                            # Visualize research gaps
                            st.markdown("### Gap Analysis Visualization")
                            
                            # Create a bubble chart of research gaps
                            try:
                                # Prepare data for bubble chart
                                gap_data = pd.DataFrame({
                                    "Gap": ["Dataset Diversity", "Computational Efficiency", "Theoretical Foundation", 
                                           "Cross-domain Application", "Evaluation Methods"],
                                    "Current_Coverage": [30, 60, 45, 25, 70],  # 0-100 scale
                                    "Importance": [90, 75, 80, 65, 50],  # 0-100 scale
                                    "Difficulty": [60, 40, 85, 50, 45]  # 0-100 scale
                                })
                                
                                # Create bubble chart with Plotly
                                fig = px.scatter(
                                    gap_data, 
                                    x="Current_Coverage", 
                                    y="Importance",
                                    size="Difficulty",
                                    color="Gap",
                                    hover_name="Gap",
                                    size_max=60,
                                    labels={
                                        "Current_Coverage": "Current Coverage (%)",
                                        "Importance": "Research Importance (%)",
                                        "Difficulty": "Implementation Difficulty"
                                    },
                                    title="Research Gap Analysis"
                                )
                                
                                # Add quadrant lines
                                fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(color="Gray", width=1, dash="dash"))
                                fig.add_shape(type="line", x0=0, y0=50, x1=100, y1=50, line=dict(color="Gray", width=1, dash="dash"))
                                
                                # Add quadrant labels
                                fig.add_annotation(x=25, y=75, text="High Priority Gaps", showarrow=False, font=dict(size=14))
                                fig.add_annotation(x=75, y=75, text="Important but Covered", showarrow=False, font=dict(size=14))
                                fig.add_annotation(x=25, y=25, text="Low Priority", showarrow=False, font=dict(size=14))
                                fig.add_annotation(x=75, y=25, text="Well Covered", showarrow=False, font=dict(size=14))
                                
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception:
                                # Fallback to simpler matplotlib visualization
                                fig, ax = plt.subplots(figsize=(10, 8))
                                
                                # Example data for opportunity map
                                opportunities = [
                                    {"name": "Dataset Diversity", "x": 0.3, "y": 0.9, "size": 300},
                                    {"name": "Computational Efficiency", "x": 0.6, "y": 0.75, "size": 200},
                                    {"name": "Theoretical Foundation", "x": 0.45, "y": 0.8, "size": 350},
                                    {"name": "Cross-domain Application", "x": 0.25, "y": 0.65, "size": 250},
                                    {"name": "Evaluation Methods", "x": 0.7, "y": 0.5, "size": 150}
                                ]
                                
                                # Plot opportunities
                                for opp in opportunities:
                                    ax.scatter(opp["x"], opp["y"], s=opp["size"], alpha=0.7)
                                    ax.annotate(opp["name"], (opp["x"], opp["y"]), 
                                              xytext=(5, 5), textcoords="offset points")
                                
                                # Add quadrant lines
                                ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
                                ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
                                
                                # Add labels
                                ax.set_xlabel("Current Coverage")
                                ax.set_ylabel("Research Importance")
                                ax.set_title("Research Gap Analysis")
                                
                                # Add quadrant labels
                                ax.text(0.25, 0.75, "High Priority Gaps", ha='center', va='center', fontsize=12)
                                ax.text(0.75, 0.75, "Important but Covered", ha='center', va='center', fontsize=12)
                                ax.text(0.25, 0.25, "Low Priority", ha='center', va='center', fontsize=12)
                                ax.text(0.75, 0.25, "Well Covered", ha='center', va='center', fontsize=12)
                                
                                st.pyplot(fig)
                        
                        elif option == "Critical Evaluation":
                            st.subheader("Critical Evaluation")
                            
                            # Strengths and weaknesses
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("### Strengths")
                                st.markdown("""
                                - Novel approach with significant performance gains
                                - Comprehensive experimentation
                                - Clear presentation of results
                                - Strong theoretical foundation
                                - Reproducible research (code available)
                                """)
                            
                            with col2:
                                st.markdown("### Weaknesses")
                                st.markdown("""
                                - Limited dataset diversity
                                - Some methodological details missing
                                - Alternative explanations not fully explored
                                - Limited discussion of broader implications
                                - High computational requirements
                                """)
                            
                            # Overall assessment
                            st.markdown("### Quality Assessment")
                            
                            # Quality metrics
                            quality_metrics = {
                                "Originality": 85,
                                "Methodology": 78,
                                "Clarity": 90,
                                "Significance": 82,
                                "Technical Soundness": 88,
                                "Presentation": 75,
                                "Literature Coverage": 70
                            }
                            
                            # Create radar chart for quality assessment
                            categories = list(quality_metrics.keys())
                            values = list(quality_metrics.values())
                            
                            # Add the first value at the end to close the polygon
                            categories = categories + [categories[0]]
                            values = values + [values[0]]
                            
                            # Convert to radians and calculate coordinates
                            N = len(categories) - 1
                            angles = [n / float(N) * 2 * np.pi for n in range(N)]
                            angles += angles[:1]  # Close the loop
                            
                            # Create radar chart
                            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
                            
                            # Draw the polygon and fill it
                            ax.plot(angles, [v/100 for v in values], linewidth=1, linestyle='solid')
                            ax.fill(angles, [v/100 for v in values], alpha=0.1)
                            
                            # Set categories as labels
                            ax.set_xticks(angles[:-1])
                            ax.set_xticklabels(categories[:-1])
                            
                            # Draw axis lines for each category
                            ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
                            ax.set_yticklabels(['20', '40', '60', '80', '100'])
                            ax.set_ylim(0, 1)
                            
                            plt.title("Paper Quality Assessment")
                            st.pyplot(fig)
                            
                            # Overall recommendation
                            st.markdown("### Overall Recommendation")
                            st.info("This paper represents a valuable contribution to the field, with strong technical merit and clear presentation. Despite some limitations in dataset diversity and methodological details, the novel approach and significant performance improvements make this paper worth studying and building upon.")
                
                # Export options
                export_format = st.selectbox("Export Analysis As", ["PDF Report", "Markdown", "Word Document", "HTML"])
                st.download_button(
                    label=f"Export Analysis as {export_format}",
                    data="Sample paper analysis report content...",
                    file_name=f"paper_analysis.{'pdf' if export_format == 'PDF Report' else 'md' if export_format == 'Markdown' else 'docx' if export_format == 'Word Document' else 'html'}",
                    mime="text/plain"
                )

def display_literature_map():
    """Display the literature map interface for literature review"""
    st.subheader("Literature Map")
    
    # Input for literature map
    map_topic = st.text_input("Enter research topic for literature mapping")
    
    col1, col2 = st.columns(2)
    with col1:
        map_depth = st.slider("Search Depth", 1, 5, 2, help="How many levels of citations to follow")
    with col2:
        max_papers = st.slider("Maximum Papers", 10, 100, 50, help="Maximum number of papers to include")
    
    map_options = st.multiselect(
        "Map Options",
        ["Include citation counts", "Show publication years", "Group by subtopics", 
         "Highlight seminal papers", "Show author networks"],
        default=["Include citation counts", "Show publication years"]
    )
    
    # Create map button
    if st.button("Generate Literature Map") and map_topic:
        with st.spinner(f"Mapping literature for '{map_topic}'..."):
            # In a real implementation, this would generate an actual literature map
            # For demonstration, we'll create a sample visualization
            
            # Sample papers for the knowledge graph
            sample_nodes = [
                {"id": 1, "title": f"Foundations of {map_topic}", "year": 2010, "citations": 1245, "authors": "Smith, A."},
                {"id": 2, "title": f"Advanced {map_topic} Techniques", "year": 2015, "citations": 823, "authors": "Johnson, B."},
                {"id": 3, "title": f"Empirical Studies in {map_topic}", "year": 2017, "citations": 412, "authors": "Williams, C."},
                {"id": 4, "title": f"A Survey of {map_topic}", "year": 2013, "citations": 967, "authors": "Brown, D."},
                {"id": 5, "title": f"{map_topic} in Education", "year": 2018, "citations": 285, "authors": "Garcia, E."},
                {"id": 6, "title": f"Theoretical Aspects of {map_topic}", "year": 2012, "citations": 743, "authors": "Miller, F."},
                {"id": 7, "title": f"Practical Applications of {map_topic}", "year": 2019, "citations": 156, "authors": "Davis, G."},
                {"id": 8, "title": f"Emerging Trends in {map_topic}", "year": 2021, "citations": 87, "authors": "Wilson, H."},
                {"id": 9, "title": f"{map_topic} Methodologies", "year": 2016, "citations": 352, "authors": "Martinez, I."},
                {"id": 10, "title": f"Future Directions for {map_topic}", "year": 2022, "citations": 43, "authors": "Anderson, J."}
            ]
            
            # Sample edges for the knowledge graph
            sample_edges = [
                {"source": 1, "target": 2},
                {"source": 1, "target": 6},
                {"source": 2, "target": 3},
                {"source": 2, "target": 7},
                {"source": 3, "target": 5},
                {"source": 4, "target": 2},
                {"source": 4, "target": 6},
                {"source": 4, "target": 9},
                {"source": 6, "target": 8},
                {"source": 7, "target": 8},
                {"source": 7, "target": 10},
                {"source": 9, "target": 3},
                {"source": 9, "target": 7}
            ]
            
            try:
                # Create network visualization using Plotly
                G = nx.DiGraph()
                
                # Add nodes with attributes
                for node in sample_nodes:
                    G.add_node(node["id"], 
                              title=node["title"],
                              year=node["year"],
                              citations=node["citations"],
                              authors=node["authors"])
                
                # Add edges
                for edge in sample_edges:
                    G.add_edge(edge["source"], edge["target"])
                
                # Calculate positions using a layout algorithm
                pos = nx.spring_layout(G, seed=42)
                
                # Create edge traces
                edge_trace = go.Scatter(
                    x=[],
                    y=[],
                    line=dict(width=0.5, color='#888'),
                    hoverinfo='none',
                    mode='lines')
                
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_trace['x'] += (x0, x1, None)
                    edge_trace['y'] += (y0, y1, None)
                
                # Create node traces
                node_trace = go.Scatter(
                    x=[],
                    y=[],
                    text=[],
                    mode='markers',
                    hoverinfo='text',
                    marker=dict(
                        showscale=True,
                        colorscale='YlGnBu',
                        size=[],
                        color=[],
                        colorbar=dict(
                            thickness=15,
                            title='Citations',
                            xanchor='left',
                            titleside='right'
                        ),
                        line=dict(width=2)))
                
                # Add node positions and attributes
                for node in G.nodes():
                    x, y = pos[node]
                    node_trace['x'] += (x,)
                    node_trace['y'] += (y,)
                    
                    # Node size based on citations
                    citations = G.nodes[node]['citations']
                    node_size = 10 + (citations / 50)  # Scale node size
                    node_trace['marker']['size'] += (node_size,)
                    node_trace['marker']['color'] += (citations,)
                    
                    # Node hover text
                    hover_text = f"ID: {node}<br>Title: {G.nodes[node]['title']}<br>"
                    hover_text += f"Year: {G.nodes[node]['year']}<br>"
                    hover_text += f"Citations: {G.nodes[node]['citations']}<br>"
                    hover_text += f"Authors: {G.nodes[node]['authors']}"
                    node_trace['text'] += (hover_text,)
                
                # Create the figure
                fig = go.Figure(data=[edge_trace, node_trace],
                             layout=go.Layout(
                                title=f'Literature Map for "{map_topic}"',
                                titlefont=dict(size=16),
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20, l=5, r=5, t=40),
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                height=600,
                                annotations=[
                                    dict(
                                        text="Network shows citation relationships between papers",
                                        showarrow=False,
                                        xref="paper", yref="paper",
                                        x=0.005, y=-0.002
                                    )
                                ]
                            ))
                
                st.plotly_chart(fig, use_container_width=True)
            
            except Exception:
                # Fallback if plotly visualization fails
                st.info("Interactive network visualization not available. Displaying alternative view.")
                
                # Display nodes (papers) in a table
                st.subheader("Papers in Literature Map")
                nodes_df = pd.DataFrame(sample_nodes)
                st.dataframe(nodes_df[["id", "title", "year", "citations", "authors"]])
                
                # Display a simple visualization of paper relationships
                st.subheader("Research Evolution Timeline")
                
                # Create a timeline visualization
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Plot papers on timeline
                for node in sample_nodes:
                    ax.scatter(node["year"], node["citations"] / 100, s=node["citations"] / 10, alpha=0.7)
                    ax.text(node["year"], node["citations"] / 100 + 0.5, f"Paper {node['id']}", fontsize=9)
                
                ax.set_xlabel("Publication Year")
                ax.set_ylabel("Impact (Citations / 100)")
                ax.set_title(f"Research Evolution: {map_topic}")
                ax.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
                st.pyplot(fig)
            
            # Subtopic analysis
            st.subheader("Subtopic Distribution")
            
            # Sample subtopics
            subtopics = ["Theory", "Applications", "Methods", "Education", "Reviews"]
            subtopic_counts = [28, 35, 42, 15, 10]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(subtopic_counts, labels=subtopics, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title(f"Subtopic Distribution in {map_topic} Research")
            st.pyplot(fig)
            
            # Export options
            st.subheader("Export Options")
            export_format = st.selectbox("Export Format", ["PNG Image", "SVG", "PDF", "Interactive HTML"])
            
            if st.button("Export Literature Map"):
                st.success(f"Literature map exported as {export_format}!")

def display_gap_analysis():
    """Display the gap analysis interface for literature review"""
    st.subheader("Research Gap Analysis")
    
    # Input for research gap analysis
    gap_topic = st.text_input("Enter research topic or field")
    
    gap_options = st.multiselect(
        "Analysis Types",
        ["Methodological gaps", "Theoretical gaps", "Application gaps", 
         "Population/context gaps", "Technological gaps", "Chronological gaps"],
        default=["Methodological gaps", "Application gaps"]
    )
    
    # Additional parameters
    col1, col2 = st.columns(2)
    with col1:
        time_range = st.slider("Time Range (Years)", 1, 20, 5, help="Consider papers published in the last X years")
    with col2:
        min_citations = st.slider("Minimum Citations", 0, 100, 10, help="Minimum citations for papers to include")
    
    # Run analysis button
    if st.button("Run Gap Analysis") and gap_topic:
        with st.spinner(f"Analyzing research gaps in '{gap_topic}'..."):
            # In a real implementation, this would perform actual gap analysis
            # For demonstration, we'll create sample results
            
            # Sample gap analysis results
            st.success("Gap analysis completed!")
            
            # Overall summary
            st.markdown(f"### Research Gap Analysis Summary for: {gap_topic}")
            st.info("This analysis reviewed 137 papers published in the last 5 years with at least 10 citations. Several significant research gaps were identified across methodological, application, and theoretical dimensions.")
            
            # Create tabs for different gap types
            gap_tabs = st.tabs([option.split(" ")[0] for option in gap_options])
            
            # Generate content for each tab
            for i, option in enumerate(gap_options):
                with gap_tabs[i]:
                    if option == "Methodological gaps":
                        st.markdown("### Methodological Gaps")
                        st.markdown("""
                        1. **Lack of Longitudinal Studies**: 
                           - Most research uses cross-sectional data
                           - Only 7% of papers employed longitudinal methods
                           - Opportunity for tracking long-term effects and developments
                        
                        2. **Limited Mixed-Method Approaches**:
                           - 82% of studies are purely quantitative
                           - Only 12% incorporate mixed methods
                           - Qualitative insights could complement quantitative findings
                        
                        3. **Sample Size and Diversity Issues**:
                           - Median sample size is relatively small (n=143)
                           - Geographic concentration in North America and Europe (76%)
                           - Limited diversity in participant demographics
                        
                        4. **Validation and Replication Gaps**:
                           - Few replication studies (3% of sample)
                           - Limited cross-validation across different contexts
                           - Need for more robust validation frameworks
                        """)
                        
                        # Visualization of methods distribution
                        methods = ["Quantitative", "Qualitative", "Mixed Methods", "Theoretical", "Meta-Analysis"]
                        percentages = [82, 6, 12, 8, 2]  # Percentages sum > 100% due to some papers using multiple methods
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.bar(methods, percentages)
                        ax.set_ylabel("Percentage of Papers")
                        ax.set_title("Research Methodology Distribution")
                        plt.xticks(rotation=45, ha="right")
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    elif option == "Theoretical gaps":
                        st.markdown("### Theoretical Gaps")
                        st.markdown("""
                        1. **Fragmented Theoretical Frameworks**:
                           - Multiple competing frameworks with limited integration
                           - Lack of comprehensive unified theories
                           - Opportunity for theoretical synthesis work
                        
                        2. **Limited Explanatory Power**:
                           - Current theories explain variance in outcomes (average R² = 0.34)
                           - Significant unexplained variance in most models
                           - Need for more robust theoretical foundations
                        
                        3. **Weak Theory-Practice Connection**:
                           - 63% of theories lack clear practical applications
                           - Practitioners report difficulty applying theoretical concepts
                           - Opportunity for translational research
                        
                        4. **Under-theorized Mechanisms**:
                           - Focus on correlations rather than causal mechanisms
                           - Limited theoretical work on underlying processes
                           - Need for more mechanism-focused theoretical development
                        """)
                        
                        # Visualization of theoretical gaps
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        # Example data for radar chart
                        categories = ['Framework Integration', 'Explanatory Power', 
                                     'Practice Connection', 'Mechanism Clarity', 
                                     'Predictive Ability']
                        
                        # Current coverage (0-100 scale)
                        values = [35, 45, 30, 25, 50]
                        
                        # Add the first value at the end to close the polygon
                        categories = categories + [categories[0]]
                        values = values + [values[0]]
                        
                        # Convert to radians and calculate coordinates
                        N = len(categories) - 1
                        angles = [n / float(N) * 2 * np.pi for n in range(N)]
                        angles += angles[:1]  # Close the loop
                        
                        # Create radar chart
                        ax = plt.subplot(polar=True)
                        ax.fill(angles, [v/100 for v in values], 'b', alpha=0.1)
                        ax.plot(angles, [v/100 for v in values], 'o-', linewidth=2)
                        ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
                        ax.set_ylim(0, 1)
                        ax.grid(True)
                        ax.set_title("Theoretical Coverage Assessment")
                        
                        st.pyplot(fig)
                        
                        # Priority areas
                        st.markdown("### Priority Areas for Theoretical Development")
                        priorities = [
                            {"area": "Causal Mechanism Models", "gap_size": "High", "field_interest": "High", "difficulty": "Medium"},
                            {"area": "Unified Framework Creation", "gap_size": "High", "field_interest": "Medium", "difficulty": "High"},
                            {"area": "Theory-Practice Translation", "gap_size": "Medium", "field_interest": "High", "difficulty": "Low"},
                            {"area": "Predictive Modeling Theory", "gap_size": "Medium", "field_interest": "Medium", "difficulty": "Medium"}
                        ]
                        
                        st.dataframe(pd.DataFrame(priorities))
                    
                    elif option == "Application gaps":
                        st.markdown("### Application Gaps")
                        st.markdown("""
                        1. **Limited Cross-Domain Applications**:
                           - 67% of applications focused on 3 primary domains
                           - Limited exploration in emerging fields
                           - Potential for cross-pollination of techniques
                        
                        2. **Practical Implementation Gaps**:
                           - 73% of papers focus on theoretical aspects or lab settings
                           - Only 18% address real-world implementation challenges
                           - Need for more industry collaboration and field studies
                        
                        3. **Scale and Generalizability Issues**:
                           - Most applications demonstrated at small scale only
                           - Limited evidence for generalizability across contexts
                           - Opportunity for large-scale validation studies
                        
                        4. **User and Stakeholder Engagement**:
                           - Limited involvement of end-users in application design
                           - Few studies incorporate stakeholder perspectives
                           - Need for more participatory and co-design approaches
                        """)
                        
                        # Visualization of application domains
                        domains = ["Healthcare", "Finance", "Education", "Manufacturing", "Social Media", "Others"]
                        applications = [32, 28, 18, 9, 7, 6]
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.bar(domains, applications, color='skyblue')
                        ax.set_ylabel("Percentage of Applications")
                        ax.set_title("Application Domain Distribution")
                        plt.xticks(rotation=45, ha="right")
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Application-theory gap visualization
                        st.markdown("### Application-Theory Gap")
                        
                        # Create a simple 2D visualization of the gap
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        # Example data showing the gap between theoretical work and applications
                        categories = ["Foundational\nTheory", "Methodological\nDevelopment", "Algorithmic\nAdvances", "Prototype\nSystems", "Real-world\nDeployments"]
                        theory_values = [85, 72, 68, 45, 23]
                        application_values = [15, 27, 44, 38, 17]
                        
                        x = np.arange(len(categories))
                        width = 0.35
                        
                        ax.bar(x - width/2, theory_values, width, label='Theoretical Work')
                        ax.bar(x + width/2, application_values, width, label='Applied Work')
                        
                        # Add gap visualization
                        for i in range(len(categories)):
                            gap = theory_values[i] - application_values[i]
                            if gap > 20:  # Only highlight significant gaps
                                ax.annotate(f"Gap: {gap}%", 
                                          xy=(i, (theory_values[i] + application_values[i])/2),
                                          xytext=(i + 0.5, (theory_values[i] + application_values[i])/2),
                                          arrowprops=dict(arrowstyle="->", color="red"))
                        
                        ax.set_ylabel("Percentage of Research")
                        ax.set_title("Theory-Application Gap")
                        ax.set_xticks(x)
                        ax.set_xticklabels(categories)
                        ax.legend()
                        plt.xticks(rotation=45, ha="right")
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    elif option == "Population/context gaps":
                        st.markdown("### Population and Context Gaps")
                        st.markdown("""
                        1. **Geographic Concentration**:
                           - 68% of studies from North America and Europe
                           - Only 8% from Africa and South America combined
                           - Need for more globally representative research
                        
                        2. **Demographic Limitations**:
                           - Overrepresentation of WEIRD populations
                           - Limited inclusion of diverse age groups and socioeconomic statuses
                           - Opportunity for more diverse and representative sampling
                        
                        3. **Contextual Constraints**:
                           - 72% of studies in academic or laboratory settings
                           - Limited research in naturalistic environments
                           - Need for more context-sensitive approaches
                        
                        4. **Access and Equity Issues**:
                           - Limited research addressing marginalized populations
                           - Few studies examining accessibility challenges
                           - Opportunity for equity-focused research
                        """)
                        
                        # Geographic distribution visualization
                        regions = ["North America", "Europe", "East Asia", "South Asia", "Middle East", "Africa", "South America", "Oceania"]
                        percentages = [42, 26, 13, 6, 5, 4, 3, 1]
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.pie(percentages, labels=regions, autopct='%1.1f%%', startangle=90)
                        ax.axis('equal')
                        plt.title("Geographic Distribution of Research")
                        st.pyplot(fig)
                        
                        # Context gap visualization
                        st.markdown("### Context Coverage Analysis")
                        
                        # Create a heatmap of context coverage
                        contexts = ["Academic", "Industry", "Healthcare", "Education", "Government", "Community"]
                        demographics = ["Children", "Young Adults", "Adults", "Seniors", "Diverse SES", "Special Needs"]
                        
                        # Sample data: coverage percentage for each context-demographic combination
                        coverage_data = np.array([
                            [65, 72, 45, 18, 22, 15],
                            [12, 58, 67, 9, 13, 8],
                            [28, 15, 42, 48, 23, 32],
                            [52, 38, 22, 13, 18, 25],
                            [8, 12, 24, 18, 15, 7],
                            [5, 8, 12, 10, 25, 18]
                        ])
                        
                        fig, ax = plt.subplots(figsize=(10, 8))
                        im = ax.imshow(coverage_data, cmap="YlGnBu")
                        
                        # Show all ticks and label them
                        ax.set_xticks(np.arange(len(demographics)))
                        ax.set_yticks(np.arange(len(contexts)))
                        ax.set_xticklabels(demographics)
                        ax.set_yticklabels(contexts)
                        
                        # Rotate the tick labels and set their alignment
                        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
                        
                        # Loop over data dimensions and create text annotations
                        for i in range(len(contexts)):
                            for j in range(len(demographics)):
                                text = ax.text(j, i, coverage_data[i, j],
                                             ha="center", va="center", color="black" if coverage_data[i, j] > 50 else "white")
                        
                        ax.set_title("Research Coverage by Context and Demographics (%)")
                        fig.tight_layout()
                        plt.colorbar(im)
                        st.pyplot(fig)
                    
                    elif option == "Technological gaps":
                        st.markdown("### Technological Gaps")
                        st.markdown("""
                        1. **Scalability Limitations**:
                           - 64% of technologies demonstrated only at small scale
                           - Computational resource constraints for larger implementations
                           - Need for more efficient and scalable approaches
                        
                        2. **Integration Challenges**:
                           - Limited integration with existing systems and infrastructures
                           - Few studies address technical debt and legacy system issues
                           - Opportunity for more interoperable solutions
                        
                        3. **Implementation Barriers**:
                           - Significant gap between prototype and production systems
                           - Limited addressing of real-world deployment challenges
                           - Need for more implementation science research
                        
                        4. **Emerging Technology Adoption**:
                           - Slow adoption of cutting-edge technologies in key applications
                           - Limited exploration of new hardware capabilities
                           - Opportunity to leverage emerging computational paradigms
                        """)
                        
                        # Technology readiness visualization
                        st.markdown("### Technology Readiness Assessment")
                        
                        # Technology Readiness Levels
                        trl_levels = ["Basic Research", "Applied Research", "Proof of Concept", "Lab Validation",
                                    "Simulated Environment", "Real Environment", "System Prototype", 
                                    "System Complete", "System Proven"]
                        
                        # Percentage of papers at each TRL level
                        trl_percentages = [22, 35, 18, 12, 5, 4, 2, 1, 1]
                        
                        fig, ax = plt.subplots(figsize=(12, 6))
                        
                        # Create stacked bars to show the progression
                        cumulative = 0
                        for i, (level, pct) in enumerate(zip(trl_levels, trl_percentages)):
                            ax.bar(1, pct, bottom=cumulative, label=level, 
                                  color=plt.cm.viridis(i/len(trl_levels)))
                            
                            # Add percentage labels
                            if pct > 3:  # Only label bars that are large enough
                                ax.text(1, cumulative + pct/2, f"{pct}%", ha='center', va='center')
                            
                            cumulative += pct
                        
                        ax.set_ylim(0, 100)
                        ax.set_ylabel("Percentage of Research")
                        ax.set_xticks([])
                        ax.set_title("Technology Readiness Level Distribution")
                        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Technology gap analysis
                        st.markdown("### Technology Gap Analysis")
                        
                        # Create a radar chart showing gaps across different technology areas
                        tech_areas = ["Data Processing", "User Interfaces", "Security & Privacy", 
                                     "Infrastructure", "Integration", "Deployment"]
                        
                        # Current capabilities vs needs (0-100 scale)
                        current_capabilities = [75, 60, 45, 50, 35, 30]
                        market_needs = [85, 75, 90, 70, 80, 75]
                        
                        # Calculate gaps
                        gaps = [n - c for c, n in zip(current_capabilities, market_needs)]
                        
                        # Create bar chart of gaps
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        bars = ax.bar(tech_areas, gaps, color=['#ff9999' if g > 30 else '#66b3ff' for g in gaps])
                        
                        ax.set_ylabel("Technology Gap (Need - Current)")
                        ax.set_title("Technology Gap Analysis")
                        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
                        
                        # Add labels on top of bars
                        for bar in bars:
                            height = bar.get_height()
                            ax.annotate(f"{height}",
                                      xy=(bar.get_x() + bar.get_width() / 2, height),
                                      xytext=(0, 3),  # 3 points vertical offset
                                      textcoords="offset points",
                                      ha='center', va='bottom')
                        
                        plt.xticks(rotation=45, ha="right")
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    elif option == "Chronological gaps":
                        st.markdown("### Chronological and Temporal Gaps")
                        st.markdown("""
                        1. **Short-term Focus**:
                           - 78% of studies have timeframes less than 1 year
                           - Limited longitudinal research (only 7% > 3 years)
                           - Need for more long-term impact studies
                        
                        2. **Historical Context Limitations**:
                           - Limited historical perspective in current research
                           - Few studies tracing evolution of concepts over time
                           - Opportunity for more historical analysis
                        
                        3. **Trend Prediction Gaps**:
                           - Focus on current applications rather than future directions
                           - Limited forecasting and trend analysis
                           - Need for more forward-looking research
                        
                        4. **Temporal Dynamics**:
                           - Limited understanding of how phenomena change over time
                           - Few studies addressing seasonality or temporal patterns
                           - Opportunity for time-series and temporal dynamics research
                        """)
                        
                        # Research timeframe visualization
                        timeframes = ["< 1 month", "1-6 months", "6-12 months", "1-3 years", "> 3 years"]
                        percentages = [15, 35, 28, 15, 7]
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.bar(timeframes, percentages, color='lightgreen')
                        ax.set_ylabel("Percentage of Studies")
                        ax.set_title("Research Timeframe Distribution")
                        plt.xticks(rotation=0)
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Publication trend visualization
                        st.markdown("### Publication Trends Over Time")
                        
                        # Create time-series data showing publication trends
                        years = list(range(2013, 2024))
                        publications = [12, 18, 25, 35, 42, 58, 72, 85, 92, 98, 105]
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.plot(years, publications, marker='o', linestyle='-', linewidth=2)
                        
                        # Add trend line
                        z = np.polyfit(range(len(years)), publications, 1)
                        p = np.poly1d(z)
                        ax.plot(years, p(range(len(years))), "r--", alpha=0.8, label="Trend")
                        
                        # Highlight gap between expected and actual for most recent years
                        expected_2022 = p(9)  # 2022 is index 9
                        expected_2023 = p(10)  # 2023 is index 10
                        
                        ax.scatter([2022, 2023], [expected_2022, expected_2023], color='red', s=50, alpha=0.5)
                        ax.plot([2022, 2022], [publications[9], expected_2022], 'r:', alpha=0.7)
                        ax.plot([2023, 2023], [publications[10], expected_2023], 'r:', alpha=0.7)
                        
                        ax.annotate(f"Gap: {int(expected_2022 - publications[9])}", 
                                   xy=(2022, (publications[9] + expected_2022)/2),
                                   xytext=(2020.5, (publications[9] + expected_2022)/2),
                                   arrowprops=dict(arrowstyle="->", color="red"))
                        
                        ax.set_xlabel("Year")
                        ax.set_ylabel("Number of Publications")
                        ax.set_title("Publication Trends in the Field")
                        ax.grid(True, linestyle='--', alpha=0.7)
                        plt.tight_layout()
                        st.pyplot(fig)
            
            # Additional visualizations
            st.subheader("Gap Priority Matrix")
            
            try:
                # Create a priority matrix with Plotly
                gap_areas = ["Methodological", "Theoretical", "Application", "Population", "Technological", "Chronological"]
                research_impact = [75, 65, 85, 70, 80, 55]  # Potential impact on the field (0-100)
                gap_size = [60, 50, 70, 80, 65, 45]  # Size of the gap (0-100)
                difficulty = [50, 70, 40, 30, 65, 55]  # Implementation difficulty (0-100)
                
                # Create bubble chart with Plotly
                fig = px.scatter(
                    x=gap_size, 
                    y=research_impact, 
                    size=[100-d for d in difficulty],  # Inverse of difficulty (larger bubble = easier to implement)
                    color=gap_areas,
                    labels={
                        "x": "Gap Size",
                        "y": "Potential Research Impact",
                        "size": "Ease of Implementation"
                    },
                    title="Research Gap Priority Matrix",
                    hover_name=gap_areas,
                    size_max=60
                )
                
                # Add quadrant lines
                fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=100, line=dict(color="Gray", width=1, dash="dash"))
                fig.add_shape(type="line", x0=0, y0=50, x1=100, y1=50, line=dict(color="Gray", width=1, dash="dash"))
                
                # Add quadrant labels
                fig.add_annotation(x=75, y=75, text="HIGH PRIORITY", showarrow=False, font=dict(size=14, color="red"))
                fig.add_annotation(x=25, y=75, text="MODERATE PRIORITY", showarrow=False, font=dict(size=12))
                fig.add_annotation(x=75, y=25, text="MODERATE PRIORITY", showarrow=False, font=dict(size=12))
                fig.add_annotation(x=25, y=25, text="LOW PRIORITY", showarrow=False, font=dict(size=12))
                
                # Update layout
                fig.update_layout(
                    xaxis=dict(range=[0, 100]),
                    yaxis=dict(range=[0, 100])
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                # Fallback to matplotlib
                fig, ax = plt.subplots(figsize=(10, 8))
                
                # Size is proportional to ease of implementation (inverse of difficulty)
                sizes = [(100 - d) * 5 for d in difficulty]
                
                scatter = ax.scatter(gap_size, research_impact, s=sizes, alpha=0.6,
                                  c=range(len(gap_areas)), cmap='viridis')
                
                # Add labels for each point
                for i, area in enumerate(gap_areas):
                    ax.annotate(area, (gap_size[i]+2, research_impact[i]),
                               xytext=(5, 0), textcoords='offset points')
                
                # Add quadrant lines
                ax.axhline(y=50, color='gray', linestyle='--', alpha=0.3)
                ax.axvline(x=50, color='gray', linestyle='--', alpha=0.3)
                
                # Add quadrant labels
                ax.text(75, 75, "HIGH PRIORITY", ha='center', va='center', fontsize=12, color='red')
                ax.text(25, 75, "MODERATE PRIORITY", ha='center', va='center', fontsize=10)
                ax.text(75, 25, "MODERATE PRIORITY", ha='center', va='center', fontsize=10)
                ax.text(25, 25, "LOW PRIORITY", ha='center', va='center', fontsize=10)
                
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 100)
                ax.set_xlabel("Gap Size")
                ax.set_ylabel("Potential Research Impact")
                ax.set_title("Research Gap Priority Matrix")
                
                # Add legend for size
                handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6,
                                                        num=4, func=lambda s: (s/5))
                legend = ax.legend(handles, ["Hard", "Moderate", "Easy", "Very Easy"],
                                 loc="upper right", title="Implementation Difficulty")
                
                plt.tight_layout()
                st.pyplot(fig)
            
            # Recommendations
            st.subheader("Key Research Recommendations")
            
            recommendations = [
                {
                    "gap_area": "Application", 
                    "recommendation": "Develop practical implementations in underserved domains", 
                    "priority": "High"
                },
                {
                    "gap_area": "Population",
                    "recommendation": "Conduct studies with more diverse and representative populations",
                    "priority": "High"
                },
                {
                    "gap_area": "Methodological",
                    "recommendation": "Implement more longitudinal studies to track long-term impacts",
                    "priority": "High"
                },
                {
                    "gap_area": "Technological",
                    "recommendation": "Address scalability issues for large-scale implementations",
                    "priority": "Medium"
                },
                {
                    "gap_area": "Theoretical",
                    "recommendation": "Develop integrated frameworks that unify existing approaches",
                    "priority": "Medium"
                }
            ]
            
            # Display as a table with styled priority
            st.dataframe(pd.DataFrame(recommendations).style.applymap(
                lambda x: 'background-color: #ffcccc' if x == 'High' else 'background-color: #ffffcc' if x == 'Medium' else '',
                subset=['priority']
            ))
            
            # Export options
            export_format = st.selectbox("Export Gap Analysis As", ["PDF Report", "Markdown", "Word Document", "Excel"])
            st.download_button(
                label=f"Export Gap Analysis as {export_format}",
                data="Sample gap analysis report content...",
                file_name=f"gap_analysis.{'pdf' if export_format == 'PDF Report' else 'md' if export_format == 'Markdown' else 'docx' if export_format == 'Word Document' else 'xlsx'}",
                mime="text/plain"
            )

def display_review_generator():
    """Display the review generator interface for literature review"""
    st.subheader("Literature Review Generator")
    
    # Input options for the review
    review_topic = st.text_input("Enter literature review topic")
    
    col1, col2 = st.columns(2)
    with col1:
        review_type = st.selectbox(
            "Review Type",
            ["Narrative Review", "Systematic Review", "Meta-analysis", "Scoping Review", "Critical Review"]
        )
    
    with col2:
        time_period = st.selectbox(
            "Time Period",
            ["Last 5 years", "Last 10 years", "Last 20 years", "All time"]
        )
    
    # Advanced options
    with st.expander("Advanced Options"):
        st.markdown("### Structure and Content Options")
        
        # Sections to include
        sections = st.multiselect(
            "Sections to include",
            ["Introduction", "Methods", "Theoretical Background", "Chronological Development", 
             "Thematic Analysis", "Critical Evaluation", "Research Gaps", "Future Directions", 
             "Practical Implications", "Conclusion", "References"],
            default=["Introduction", "Methods", "Thematic Analysis", "Research Gaps", "Conclusion", "References"]
        )
        
        # Review style
        col1, col2 = st.columns(2)
        with col1:
            academic_level = st.select_slider(
                "Academic Level",
                options=["Undergraduate", "Graduate", "Doctoral", "Expert"],
                value="Graduate"
            )
        
        with col2:
            citation_style = st.selectbox(
                "Citation Style",
                ["APA", "MLA", "Chicago", "Harvard", "IEEE", "Vancouver"]
            )
        
        # Sources
        min_sources = st.slider("Minimum number of sources", 5, 100, 20)
        
        # Focus areas
        focus_areas = st.text_area("Specific focus areas (one per line)", 
                                  "Current trends\nMethodological approaches\nKey findings")
    
    # Generate review button
    if st.button("Generate Literature Review") and review_topic:
        with st.spinner(f"Generating {review_type} on {review_topic}..."):
            # In a real implementation, this would generate an actual literature review
            # For demonstration, we'll create a sample review structure
            
            # Show progress
            progress_bar = st.progress(0)
            for i in range(101):
                time.sleep(0.02)  # Simulate generation time
                progress_bar.progress(i)
            
            st.success("Literature review generated successfully!")
            
            # Display the review structure
            st.subheader(f"{review_type}: {review_topic}")
            
            # Mock review content based on selected sections
            if "Introduction" in sections:
                st.markdown("### 1. Introduction")
                st.markdown(f"""
                This literature review examines the field of {review_topic} over {time_period}. 
                The review synthesizes findings from {min_sources}+ sources to provide a comprehensive 
                overview of the current state of knowledge, methodological approaches, and research gaps.
                
                The field of {review_topic} has evolved significantly in recent years, with growing interest 
                in {focus_areas.split('\n')[0].lower() if focus_areas else 'various aspects'}. This review aims to 
                categorize and analyze the existing literature to identify patterns, trends, and areas 
                for future research.
                """)
            
            if "Methods" in sections:
                st.markdown("### 2. Methodology")
                st.markdown(f"""
                This {review_type.lower()} followed a structured approach to literature identification, 
                selection, and analysis. The search was conducted using major databases including:
                
                - Web of Science
                - Scopus
                - ProQuest
                - IEEE Xplore
                - ACM Digital Library
                
                Search terms included: "{review_topic}", "{review_topic} approaches", "{review_topic} applications", 
                and related terminology. The time period was restricted to {time_period.lower()}, and only 
                peer-reviewed English-language publications were included.
                
                The initial search yielded 273 results, which was narrowed to 87 after removing duplicates 
                and applying exclusion criteria. These were further refined to {min_sources} core sources 
                after quality assessment and relevance screening.
                """)
            
            if "Theoretical Background" in sections:
                st.markdown("### 3. Theoretical Background")
                st.markdown(f"""
                The theoretical underpinnings of {review_topic} draw from multiple disciplines, including 
                computer science, cognitive psychology, and information systems. Major theoretical frameworks 
                include:
                
                1. **Computational Theory**: Focusing on algorithmic approaches and computational efficiency
                2. **Information Processing Models**: Addressing how information is processed and transformed
                3. **User Interaction Frameworks**: Examining human-system interactions and usability concerns
                
                These theoretical foundations provide the conceptual basis for research developments in the field, 
                though significant theoretical integration remains an opportunity for future work.
                """)
            
            if "Chronological Development" in sections:
                st.markdown("### 4. Chronological Development")
                
                # Create a timeline visualization
                years = [2010, 2012, 2015, 2017, 2019, 2021, 2023]
                milestones = [
                    "Foundation papers published",
                    "First standardized frameworks",
                    "Major methodological advances",
                    "Industry adoption begins",
                    "Scale and performance breakthroughs",
                    "Integration with other technologies",
                    "Current state-of-the-art approaches"
                ]
                
                fig, ax = plt.subplots(figsize=(12, 5))
                
                # Plot the timeline
                ax.scatter(years, [1]*len(years), s=100, color='skyblue', zorder=2)
                ax.plot(years, [1]*len(years), color='gray', linestyle='-', linewidth=2, zorder=1)
                
                # Add milestone labels
                for i, (year, milestone) in enumerate(zip(years, milestones)):
                    ax.annotate(milestone, (year, 1),
                               xytext=(0, 10 if i % 2 == 0 else -30),
                               textcoords='offset points',
                               ha='center', va='center',
                               bbox=dict(boxstyle='round,pad=0.5', fc='skyblue' if i % 2 == 0 else 'lightgreen', alpha=0.7),
                               arrowprops=dict(arrowstyle='->', color='gray'))
                
                # Customize the plot
                ax.set_yticks([])
                ax.set_xticks(years)
                ax.set_xticklabels(years)
                ax.set_title(f"Chronological Development of {review_topic}")
                plt.tight_layout()
                st.pyplot(fig)
                
                st.markdown(f"""
                The field of {review_topic} has evolved through several distinct phases. Early work 
                (2010-2012) focused on establishing fundamental concepts and frameworks. The middle period 
                (2015-2019) saw significant methodological refinements and the beginning of practical 
                applications. The most recent period (2021-present) has been characterized by integration 
                with other technologies and dramatic improvements in scale and performance.
                """)
            
            if "Thematic Analysis" in sections:
                st.markdown("### 5. Thematic Analysis")
                st.markdown(f"""
                Analysis of the literature reveals several predominant themes in {review_topic} research:
                """)
                
                # Generate themes based on focus areas or default themes
                themes = focus_areas.strip().split('\n') if focus_areas.strip() else [
                    "Algorithmic Approaches", "Application Domains", "Performance Evaluation"
                ]
                
                # Display themes with expandable content
                for i, theme in enumerate(themes):
                    with st.expander(f"5.{i+1} {theme}"):
                        st.markdown(f"""
                        Research on {theme.lower()} in the context of {review_topic} has produced significant 
                        insights. Smith et al. (2021) found that {generate_lorem_ipsum(1, 3)}
                        
                        Supporting this view, Johnson and Williams (2019) demonstrated that {generate_lorem_ipsum(1, 2)}
                        However, contrasting results from Garcia et al. (2022) suggest that {generate_lorem_ipsum(1, 3)}
                        
                        A synthesis of these findings indicates that {generate_lorem_ipsum(1, 2)}
                        """)
                
                # Create a theme distribution visualization
                theme_counts = [random.randint(8, 25) for _ in themes]
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(themes, theme_counts, color='lightgreen')
                ax.set_ylabel("Number of Publications")
                ax.set_title("Publication Distribution by Theme")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
            
            if "Critical Evaluation" in sections:
                st.markdown("### 6. Critical Evaluation")
                st.markdown(f"""
                The current body of literature on {review_topic} exhibits both strengths and limitations 
                that should be addressed in future research.
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Strengths")
                    st.markdown("""
                    - Strong empirical evidence for core concepts
                    - Methodological innovations and rigor
                    - Growing practical applications
                    - Interdisciplinary perspectives
                    - Reproducible research practices
                    """)
                
                with col2:
                    st.markdown("#### Limitations")
                    st.markdown("""
                    - Geographic and demographic concentration
                    - Limited long-term studies
                    - Methodological homogeneity
                    - Publication bias toward positive results
                    - Gaps between theory and application
                    """)
                
                # Quality assessment visualization
                st.markdown("#### Quality Assessment of the Literature")
                
                # Example metrics for assessment
                quality_metrics = {
                    "Methodological Rigor": 72,
                    "Reporting Quality": 68,
                    "Statistical Analysis": 65,
                    "Sample Representativeness": 43,
                    "Theoretical Grounding": 78,
                    "Generalizability": 55
                }
                
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.bar(quality_metrics.keys(), quality_metrics.values(), color='skyblue')
                ax.set_ylabel("Average Score (0-100)")
                ax.set_title("Quality Assessment of Literature")
                ax.set_ylim(0, 100)
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
            
            if "Research Gaps" in sections:
                st.markdown("### 7. Research Gaps")
                st.markdown(f"""
                Despite the growing body of literature on {review_topic}, several significant gaps remain:
                
                1. **Methodological Gaps**:
                   - Limited use of longitudinal and mixed-methods approaches
                   - Lack of standardized measurement and evaluation frameworks
                   - Insufficient replication studies
                
                2. **Theoretical Gaps**:
                   - Fragmented theoretical frameworks with limited integration
                   - Underdeveloped explanatory mechanisms for observed phenomena
                   - Weak connections between theory and practical applications
                
                3. **Application Gaps**:
                   - Limited research in domains such as healthcare, education, and public services
                   - Few studies addressing implementation challenges and barriers
                   - Insufficient consideration of ethical and societal implications
                
                4. **Contextual and Demographic Gaps**:
                   - Geographic concentration of research in North America and Europe
                   - Limited diversity in study populations and contexts
                   - Few studies examining cultural and socioeconomic factors
                """)
                
                # Gap visualization
                st.markdown("#### Gap Analysis Visualization")
                
                # Create a simple gap analysis
                gap_types = ["Methodological", "Theoretical", "Application", "Contextual"]
                coverage = [35, 45, 25, 20]  # Percentage of literature addressing each gap
                
                fig, ax = plt.subplots(figsize=(10, 5))
                
                # Create bars for coverage with transparency
                ax.bar(gap_types, coverage, color='royalblue', alpha=0.6, label="Current Coverage")
                
                # Create bars for gaps (100 - coverage)
                ax.bar(gap_types, [100 - c for c in coverage], bottom=coverage, color='salmon', alpha=0.6, label="Gap")
                
                ax.set_ylabel("Percentage")
                ax.set_title("Research Coverage and Gaps")
                ax.set_ylim(0, 100)
                ax.legend()
                
                # Add text labels
                for i, (c, g) in enumerate(zip(coverage, [100 - c for c in coverage])):
                    ax.text(i, c/2, f"{c}%", ha='center', va='center')
                    ax.text(i, c + g/2, f"{g}%", ha='center', va='center')
                
                plt.tight_layout()
                st.pyplot(fig)
            
            if "Future Directions" in sections:
                st.markdown("### 8. Future Directions")
                st.markdown(f"""
                Based on the identified research gaps, several promising directions for future research emerge:
                
                1. **Methodological Advancements**:
                   - Development of standardized evaluation frameworks
                   - Integration of qualitative and quantitative approaches
                   - Longitudinal studies to track development and impact over time
                
                2. **Theoretical Development**:
                   - Creation of integrative theoretical frameworks
                   - Investigation of underlying mechanisms and processes
                   - Theory-building to explain contextual variations
                
                3. **Application Expansion**:
                   - Exploration of applications in underserved domains
                   - Research on implementation and adoption challenges
                   - Investigation of transferability across contexts
                
                4. **Diversification of Contexts and Populations**:
                   - Research in diverse geographic and cultural settings
                   - Studies with varied demographic populations
                   - Examination of socioeconomic and contextual factors
                
                5. **Ethical and Societal Implications**:
                   - Investigation of unintended consequences
                   - Development of ethical guidelines and frameworks
                   - Research on equity and accessibility considerations
                """)
                
                # Create a research roadmap visualization
                st.markdown("#### Research Roadmap")
                
                # Create a simple roadmap timeline
                phases = ["Short-term\n(1-2 years)", "Medium-term\n(3-5 years)", "Long-term\n(5+ years)"]
                
                # Example priorities for each phase
                priorities = [
                    ["Standardized metrics", "Replication studies", "Tool development"],
                    ["Theoretical integration", "Cross-domain applications", "Longitudinal studies"],
                    ["Comprehensive frameworks", "Societal impact assessment", "Global implementation"]
                ]
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Create the roadmap
                for i, phase in enumerate(phases):
                    # Draw phase box
                    ax.add_patch(plt.Rectangle((i, 0), 0.8, 1, fill=True, color=f'C{i}', alpha=0.3))
                    ax.text(i + 0.4, 1.1, phase, ha='center', va='center', fontweight='bold')
                    
                    # Add priorities
                    for j, priority in enumerate(priorities[i]):
                        y_pos = 0.8 - j * 0.3
                        ax.text(i + 0.4, y_pos, priority, ha='center', va='center', 
                               bbox=dict(boxstyle='round,pad=0.3', facecolor=f'C{i}', alpha=0.2))
                
                # Connect phases with arrows
                ax.arrow(0.8, 0.5, 0.2, 0, head_width=0.05, head_length=0.05, fc='black', ec='black')
                ax.arrow(1.8, 0.5, 0.2, 0, head_width=0.05, head_length=0.05, fc='black', ec='black')
                
                # Customize plot
                ax.set_xlim(-0.2, 3)
                ax.set_ylim(-0.1, 1.3)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(f"Research Roadmap for {review_topic}")
                ax.axis('off')
                
                st.pyplot(fig)
            
            if "Practical Implications" in sections:
                st.markdown("### 9. Practical Implications")
                st.markdown(f"""
                The findings of this literature review have several practical implications for researchers, 
                practitioners, and policymakers in the field of {review_topic}:
                
                1. **For Researchers**:
                   - Priority areas for future investigation have been identified
                   - Methodological recommendations for more robust studies
                   - Opportunities for interdisciplinary collaboration
                
                2. **For Practitioners**:
                   - Evidence-based guidelines for implementation
                   - Identification of common challenges and potential solutions
                   - Frameworks for evaluation and assessment
                
                3. **For Policymakers**:
                   - Evidence to inform policy development
                   - Identification of areas requiring regulatory attention
                   - Insights into potential societal impacts
                """)
                
                # Create a stakeholder impact visualization
                stakeholders = ["Researchers", "Practitioners", "Policymakers", "End Users", "Society"]
                impact_levels = [85, 70, 60, 90, 65]  # Impact relevance for each stakeholder group
                
                fig, ax = plt.subplots(figsize=(10, 5))
                bars = ax.bar(stakeholders, impact_levels, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
                
                # Add value labels on top of bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{int(height)}%',
                           ha='center', va='bottom')
                
                ax.set_ylabel("Relevance (%)")
                ax.set_title("Relevance of Findings to Stakeholders")
                ax.set_ylim(0, 100)
                plt.tight_layout()
                st.pyplot(fig)
            
            if "Conclusion" in sections:
                st.markdown("### 10. Conclusion")
                st.markdown(f"""
                This {review_type.lower()} has synthesized the current state of knowledge on {review_topic}, 
                examining {min_sources}+ sources published over {time_period.lower()}. The analysis reveals 
                a field with substantial growth and evolution, yet with significant opportunities for further 
                development.
                
                Key findings include the emergence of {themes[0].lower() if themes else 'several major themes'}, 
                the development of increasingly sophisticated methodological approaches, and the expansion 
                of applications across domains. However, important gaps remain in terms of {gap_types[0].lower() if 'gap_types' in locals() else 'methodological diversity'}, 
                theoretical integration, and contextual diversity.
                
                Future research should prioritize addressing these gaps through methodological innovation, 
                theoretical development, expansion of application contexts, and increased attention to 
                ethical and societal implications. Such efforts will contribute to a more robust, 
                comprehensive, and impactful body of knowledge on {review_topic}.
                """)
            
            if "References" in sections:
                st.markdown("### 11. References")
                
                # Generate mock references in the selected citation style
                if citation_style == "APA":
                    st.markdown("""
                    Smith, J. A., & Johnson, B. C. (2021). Advances in theoretical approaches to artificial intelligence. *Journal of AI Research, 15*(2), 123-145.
                    
                    Williams, D. E., Garcia, F. G., & Martinez, H. I. (2020). Empirical evaluation of machine learning algorithms. *Computational Intelligence Review, 8*(3), 234-256.
                    
                    Brown, K. L., & Davis, M. N. (2022). Applications of deep learning in healthcare. *Medical AI Journal, 5*(1), 67-89.
                    
                    Anderson, O. P., Taylor, Q. R., & Wilson, S. T. (2019). A systematic review of natural language processing techniques. *Language Technology, 12*(4), 345-367.
                    
                    Lee, U. V., & Robinson, W. X. (2023). Ethical considerations in autonomous systems. *AI Ethics Review, 7*(2), 156-178.
                    """)
                elif citation_style == "MLA":
                    st.markdown("""
                    Smith, Jonathan A., and Barbara C. Johnson. "Advances in Theoretical Approaches to Artificial Intelligence." *Journal of AI Research*, vol. 15, no. 2, 2021, pp. 123-145.
                    
                    Williams, David E., et al. "Empirical Evaluation of Machine Learning Algorithms." *Computational Intelligence Review*, vol. 8, no. 3, 2020, pp. 234-256.
                    
                    Brown, Kevin L., and Melissa N. Davis. "Applications of Deep Learning in Healthcare." *Medical AI Journal*, vol. 5, no. 1, 2022, pp. 67-89.
                    
                    Anderson, Oliver P., et al. "A Systematic Review of Natural Language Processing Techniques." *Language Technology*, vol. 12, no. 4, 2019, pp. 345-367.
                    
                    Lee, Uma V., and William X. Robinson. "Ethical Considerations in Autonomous Systems." *AI Ethics Review*, vol. 7, no. 2, 2023, pp. 156-178.
                    """)
                else:  # Default to IEEE
                    st.markdown("""
                    [1] J. A. Smith and B. C. Johnson, "Advances in theoretical approaches to artificial intelligence," *Journal of AI Research*, vol. 15, no. 2, pp. 123-145, 2021.
                    
                    [2] D. E. Williams, F. G. Garcia, and H. I. Martinez, "Empirical evaluation of machine learning algorithms," *Computational Intelligence Review*, vol. 8, no. 3, pp. 234-256, 2020.
                    
                    [3] K. L. Brown and M. N. Davis, "Applications of deep learning in healthcare," *Medical AI Journal*, vol. 5, no. 1, pp. 67-89, 2022.
                    
                    [4] O. P. Anderson, Q. R. Taylor, and S. T. Wilson, "A systematic review of natural language processing techniques," *Language Technology*, vol. 12, no. 4, pp. 345-367, 2019.
                    
                    [5] U. V. Lee and W. X. Robinson, "Ethical considerations in autonomous systems," *AI Ethics Review*, vol. 7, no. 2, pp. 156-178, 2023.
                    """)
            
            # Export the review
            st.subheader("Export Options")
            
            export_format = st.selectbox("Export Format", ["PDF", "Word Document", "Markdown", "LaTeX"])
            include_figures = st.checkbox("Include figures and visualizations", value=True)
            
            if st.button("Download Literature Review"):
                st.success(f"Literature review successfully exported as {export_format}!")
                st.download_button(
                    label=f"Download {export_format} File",
                    data=f"Sample literature review on {review_topic}...",
                    file_name=f"literature_review_{review_topic.replace(' ', '_').lower()}.{'pdf' if export_format == 'PDF' else 'docx' if export_format == 'Word Document' else 'md' if export_format == 'Markdown' else 'tex'}",
                    mime="text/plain"
                )

def display_literature_review_assistant():
    """Display literature review assistant tools"""
    st.header("📖 Literature Review Assistant")
    
    # Create tabs for different literature review features
    lit_review_tabs = st.tabs([
        "Search & Discovery",
        "Paper Analyzer",
        "Literature Map",
        "Gap Analysis",
        "Review Generator"
    ])
    
    # Tab 1: Search & Discovery
    with lit_review_tabs[0]:
        display_search_and_discovery()
    
    # Tab 2: Paper Analyzer
    with lit_review_tabs[1]:
        display_paper_analyzer()
    
    # Tab 3: Literature Map
    with lit_review_tabs[2]:
        display_literature_map()
    
    # Tab 4: Gap Analysis
    with lit_review_tabs[3]:
        display_gap_analysis()
    
    # Tab 5: Review Generator
    with lit_review_tabs[4]:
        display_review_generator()

# Main function to be called from the research_tools_integration.py
def main():
    display_literature_review_assistant()

if __name__ == "__main__":
    main()
