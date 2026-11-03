from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import time
import io
import openai
from io import BytesIO
import base64

def initialize_data_analysis_state():
    """Initialize session state variables for data analysis tools"""
    if "active_analysis_tab" not in st.session_state:
        st.session_state.active_analysis_tab = "Data Explorer"
        
    if "uploaded_data" not in st.session_state:
        st.session_state.uploaded_data = None
        
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
        
    if "visualization_config" not in st.session_state:
        st.session_state.visualization_config = {}
        
    if "selected_columns" not in st.session_state:
        st.session_state.selected_columns = []
        
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []

def load_dataset(file):
    """Load dataset from uploaded file"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        elif file.name.endswith('.json'):
            df = pd.read_json(file)
        elif file.name.endswith('.tsv'):
            df = pd.read_csv(file, sep='\t')
        else:
            st.error("Unsupported file format. Please upload a CSV, Excel, JSON, or TSV file.")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None

def get_data_summary(df):
    """Generate a comprehensive summary of the dataset"""
    summary = {}
    
    # Basic info
    summary["shape"] = df.shape
    summary["columns"] = list(df.columns)
    summary["dtypes"] = {col: str(dtype) for col, dtype in df.dtypes.items()}
    
    # Missing values
    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    summary["missing_values"] = {col: {
        "count": int(count),
        "percentage": float(round(percentage, 2))
    } for col, count, percentage in zip(missing_values.index, missing_values, missing_percentage)}
    
    # Numeric columns summary
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    summary["numeric_summary"] = {}
    
    if len(numeric_cols) > 0:
        numeric_stats = df[numeric_cols].describe().transpose()
        for col in numeric_cols:
            if col in numeric_stats.index:
                summary["numeric_summary"][col] = {
                    "min": float(numeric_stats.loc[col, 'min']),
                    "max": float(numeric_stats.loc[col, 'max']),
                    "mean": float(numeric_stats.loc[col, 'mean']),
                    "median": float(df[col].median()),
                    "std": float(numeric_stats.loc[col, 'std']),
                    "skewness": float(df[col].skew()),
                    "kurtosis": float(df[col].kurtosis())
                }
    
    # Categorical columns summary
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    summary["categorical_summary"] = {}
    
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        if len(value_counts) <= 50:  # Only include if there aren't too many categories
            summary["categorical_summary"][col] = {
                "unique_values": int(df[col].nunique()),
                "top_categories": {
                    str(value): int(count) 
                    for value, count in value_counts.head(10).items()
                }
            }
        else:
            summary["categorical_summary"][col] = {
                "unique_values": int(df[col].nunique()),
                "note": "Too many categories to display"
            }
    
    # Correlations (for numeric data)
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr().round(2)
        # Convert to dictionary with only the upper triangle
        correlations = {}
        for i, col1 in enumerate(corr_matrix.columns):
            for j, col2 in enumerate(corr_matrix.columns):
                if i < j:  # Upper triangle only
                    corr_value = corr_matrix.iloc[i, j]
                    if not pd.isna(corr_value):
                        correlations[f"{col1}__{col2}"] = float(corr_value)
        
        summary["correlations"] = correlations
    
    return summary

def generate_ai_insights(df, question=None):
    """Generate AI-powered insights about the dataset"""
    
    # Get basic summary
    data_summary = get_data_summary(df)
    
    # Sample of the data (first 5 rows)
    sample_data = df.head(5).to_dict(orient='records')
    
    # Create prompt for GPT
    if question:
        prompt = f"""
        Analyze this dataset to answer the following question: '{question}'
        
        Dataset summary: {json.dumps(data_summary)}
        
        Sample data: {json.dumps(sample_data)}
        
        Provide:
        1. A direct answer to the question
        2. Key findings from the data related to the question
        3. Any notable patterns or trends
        4. Limitations in the analysis
        
        Keep your analysis concise and data-focused.
        """
    else:
        prompt = f"""
        Generate insights about this dataset:
        
        Dataset summary: {json.dumps(data_summary)}
        
        Sample data: {json.dumps(sample_data)}
        
        Provide:
        1. Key observations about the dataset structure
        2. Notable patterns or trends in the data
        3. Potential research questions this dataset could answer
        4. Suggested analyses or visualizations that might be revealing
        5. Data quality issues or limitations
        
        Focus on the most important insights. Be concise and specific.
        """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data scientist providing insights on research datasets."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )
        
        insights = response.choices[0].message.content.strip()
        return insights
    
    except Exception as e:
        st.error(f"Error generating insights: {str(e)}")
        return "Unable to generate insights. Please check your API key or try again later."

def plot_correlation_heatmap(df):
    """Create a correlation heatmap for numeric columns"""
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) < 2:
        return None, "Not enough numeric columns for correlation analysis"
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    plt.title("Correlation Matrix")
    
    return fig, None

def plot_distribution(df, column):
    """Create a distribution plot for a numeric column"""
    if df[column].dtype not in ['int64', 'float64']:
        return None, f"Column '{column}' is not numeric"
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Add histogram with KDE
    sns.histplot(df[column].dropna(), kde=True, ax=ax)
    
    # Add mean and median lines
    mean_val = df[column].mean()
    median_val = df[column].median()
    
    ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
    ax.axvline(median_val, color='green', linestyle='-.', label=f'Median: {median_val:.2f}')
    
    plt.title(f"Distribution of {column}")
    plt.legend()
    
    return fig, None

def plot_categorical(df, column, top_n=10):
    """Create a bar plot for a categorical column"""
    if df[column].dtype in ['int64', 'float64']:
        return None, f"Column '{column}' is numeric, not categorical"
    
    # Get value counts and limit to top N categories
    value_counts = df[column].value_counts().nlargest(top_n)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
    plt.title(f"Top {len(value_counts)} Categories in {column}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig, None

def plot_scatter(df, x_col, y_col, hue_col=None):
    """Create a scatter plot between two numeric columns"""
    if df[x_col].dtype not in ['int64', 'float64'] or df[y_col].dtype not in ['int64', 'float64']:
        return None, "Both columns must be numeric for a scatter plot"
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if hue_col and hue_col in df.columns:
        if df[hue_col].nunique() <= 10:  # Only use hue if there aren't too many categories
            sns.scatterplot(x=x_col, y=y_col, hue=hue_col, data=df, ax=ax)
        else:
            sns.scatterplot(x=x_col, y=y_col, data=df, ax=ax)
            return fig, "Too many categories in hue column, showing scatter plot without hue"
    else:
        sns.scatterplot(x=x_col, y=y_col, data=df, ax=ax)
    
    # Add regression line
    sns.regplot(x=x_col, y=y_col, data=df, scatter=False, ax=ax, line_kws={"color": "red"})
    
    # Calculate correlation
    correlation = df[[x_col, y_col]].corr().iloc[0, 1]
    plt.title(f"Scatter Plot: {x_col} vs {y_col} (r = {correlation:.2f})")
    
    return fig, None

def plot_time_series(df, date_col, value_col):
    """Create a time series plot"""
    # Check if date column exists and is in datetime format
    if date_col not in df.columns:
        return None, f"Column '{date_col}' does not exist"
    
    # Convert to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        try:
            df = df.copy()
            df[date_col] = pd.to_datetime(df[date_col])
        except:
            return None, f"Column '{date_col}' could not be converted to datetime format"
    
    # Check if value column is numeric
    if df[value_col].dtype not in ['int64', 'float64']:
        return None, f"Column '{value_col}' is not numeric"
    
    # Sort by date
    df_sorted = df.sort_values(by=date_col)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=date_col, y=value_col, data=df_sorted, marker='o', ax=ax)
    plt.title(f"Time Series: {value_col} over {date_col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig, None

def display_data_analysis_tools():
    """Main function to display data analysis tools interface"""
    
    # Initialize session state
    initialize_data_analysis_state()
    
    st.title("📊 Data Analysis Tools & Visualization")
    
    # Navigation tabs
    analysis_tabs = [
        "Data Explorer",
        "Statistical Analysis",
        "Visualization Studio",
        "AI Insights",
        "Code Generator"
    ]
    
    selected_tab = st.radio("Data Analysis Tools", analysis_tabs, horizontal=True)
    st.session_state.active_analysis_tab = selected_tab
    
    st.markdown("---")
    
    # File uploader for all tabs
    uploaded_file = st.file_uploader("Upload data file", type=["csv", "xlsx", "xls", "json", "tsv"])
    
    # Load the data
    df = None
    if uploaded_file:
        if st.session_state.uploaded_data is None or uploaded_file.name != st.session_state.uploaded_data_name:
            with st.spinner("Loading data..."):
                df = load_dataset(uploaded_file)
                if df is not None:
                    st.session_state.uploaded_data = df
                    st.session_state.uploaded_data_name = uploaded_file.name
                    st.success(f"Data loaded successfully: {df.shape[0]} rows and {df.shape[1]} columns")
        else:
            df = st.session_state.uploaded_data
            st.success(f"Using previously loaded data: {df.shape[0]} rows and {df.shape[1]} columns")
    else:
        df = st.session_state.uploaded_data
    
    # If no data is loaded, display example options
    if df is None:
        st.info("Please upload a data file or select one of the example datasets below.")
        
        example_choice = st.radio(
            "Select an example dataset:",
            ["None", "Iris Flower Dataset", "Titanic Survival Dataset", "Boston Housing Dataset"]
        )
        
        if example_choice == "Iris Flower Dataset":
            df = sns.load_dataset("iris")
            st.session_state.uploaded_data = df
            st.session_state.uploaded_data_name = "iris.csv"
            st.success(f"Iris dataset loaded: {df.shape[0]} rows and {df.shape[1]} columns")
        elif example_choice == "Titanic Survival Dataset":
            df = sns.load_dataset("titanic")
            st.session_state.uploaded_data = df
            st.session_state.uploaded_data_name = "titanic.csv"
            st.success(f"Titanic dataset loaded: {df.shape[0]} rows and {df.shape[1]} columns")
        elif example_choice == "Boston Housing Dataset":
            # Create a simplified Boston Housing dataset (since the original is deprecated)
            np.random.seed(42)
            n = 506  # Same as original Boston dataset
            X = np.random.randn(n, 4)
            y = 25 + 5 * X[:, 0] + 2 * X[:, 1] - 4 * X[:, 2] + 0.5 * X[:, 3] + np.random.randn(n) * 2
            
            boston = pd.DataFrame({
                'CRIM': np.abs(X[:, 0]),  # Crime rate
                'RM': np.abs(X[:, 1]) * 3 + 4,  # Average rooms
                'AGE': np.abs(X[:, 2]) * 50 + 50,  # Age of homes
                'DIS': np.abs(X[:, 3]) * 2 + 1,  # Distance to employment centers
                'PRICE': y  # House prices
            })
            
            df = boston
            st.session_state.uploaded_data = df
            st.session_state.uploaded_data_name = "boston.csv"
            st.success(f"Boston housing dataset loaded: {df.shape[0]} rows and {df.shape[1]} columns")
    
    # If data is available, show tab content
    if df is not None:
        # Tab 1: Data Explorer
        if st.session_state.active_analysis_tab == "Data Explorer":
            st.header("Data Explorer")
            
            # Create tabs for different views
            explorer_tabs = st.tabs(["Preview", "Summary", "Structure", "Missing Values", "Search"])
            
            # Tab 1: Data Preview
            with explorer_tabs[0]:
                st.subheader("Data Preview")
                
                # Show the first n rows
                n_rows = st.slider("Number of rows to display", 5, 100, 10)
                st.dataframe(df.head(n_rows))
                
                # Show column selector
                all_columns = df.columns.tolist()
                selected_cols = st.multiselect("Select columns to display", all_columns, default=all_columns[:5])
                
                if selected_cols:
                    st.dataframe(df[selected_cols].head(n_rows))
                
                # Add download option
                csv_buffer = BytesIO()
                df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                st.download_button(
                    label="Download CSV",
                    data=csv_buffer,
                    file_name="dataset.csv",
                    mime="text/csv"
                )
            
            # Tab 2: Data Summary
            with explorer_tabs[1]:
                st.subheader("Data Summary")
                
                # Display descriptive statistics
                st.write("### Descriptive Statistics")
                st.dataframe(df.describe().round(2))
                
                # Summary for categorical variables
                cat_cols = df.select_dtypes(include=['object', 'category']).columns
                if not cat_cols.empty:
                    st.write("### Categorical Variables")
                    
                    for col in cat_cols:
                        with st.expander(f"{col} - {df[col].nunique()} unique values"):
                            value_counts = df[col].value_counts()
                            st.dataframe(pd.DataFrame({
                                'Value': value_counts.index,
                                'Count': value_counts.values,
                                'Percentage': (value_counts.values / len(df) * 100).round(2)
                            }))
            
            # Tab 3: Data Structure
            with explorer_tabs[2]:
                st.subheader("Data Structure")
                
                # Display column info
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.astype(str),
                    'Non-Null Count': df.count(),
                    'Null Count': df.isnull().sum(),
                    'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2),
                    'Unique Values': [df[col].nunique() for col in df.columns]
                })
                
                st.dataframe(col_info)
                
                # Display memory usage
                st.write("### Memory Usage")
                memory_usage = df.memory_usage(deep=True)
                total_memory = memory_usage.sum()
                
                st.write(f"Total memory usage: {total_memory / 1024**2:.2f} MB")
                
                # Memory usage by column
                memory_by_col = pd.DataFrame({
                    'Column': memory_usage.index,
                    'Memory (KB)': (memory_usage.values / 1024).round(2),
                    'Percentage': (memory_usage.values / total_memory * 100).round(2)
                })
                
                st.dataframe(memory_by_col.sort_values("Memory (KB)", ascending=False))
            
            # Tab 4: Missing Values
            with explorer_tabs[3]:
                st.subheader("Missing Values Analysis")
                
                # Missing values summary
                missing_values = df.isnull().sum()
                missing_percentage = (missing_values / len(df) * 100).round(2)
                
                missing_df = pd.DataFrame({
                    'Column': missing_values.index,
                    'Missing Count': missing_values.values,
                    'Missing Percentage': missing_percentage.values
                })
                
                missing_df = missing_df.sort_values("Missing Count", ascending=False)
                st.dataframe(missing_df)
                
                # Visualize missing values
                if missing_df["Missing Count"].sum() > 0:
                    st.write("### Missing Values Visualization")
                    
                    # Create a heatmap of missing values
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.heatmap(df.isnull(), cmap='viridis', yticklabels=False, cbar=False, ax=ax)
                    plt.title("Missing Values Heatmap")
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Handling missing values options
                    st.write("### Handle Missing Values")
                    missing_col = st.selectbox("Select column with missing values", 
                                              missing_df[missing_df["Missing Count"] > 0]["Column"].tolist())
                    
                    if missing_col:
                        handling_method = st.radio(
                            "Select handling method",
                            ["Drop rows", "Fill with mean/mode", "Fill with median", "Fill with custom value"]
                        )
                        
                        if st.button("Apply"):
                            df_cleaned = df.copy()
                            
                            if handling_method == "Drop rows":
                                df_cleaned = df_cleaned.dropna(subset=[missing_col])
                                st.success(f"Dropped {len(df) - len(df_cleaned)} rows with missing values in {missing_col}")
                            
                            elif handling_method == "Fill with mean/mode":
                                if df[missing_col].dtype in ['int64', 'float64']:
                                    fill_value = df[missing_col].mean()
                                    df_cleaned[missing_col] = df_cleaned[missing_col].fillna(fill_value)
                                    st.success(f"Filled missing values in {missing_col} with mean ({fill_value:.2f})")
                                else:
                                    fill_value = df[missing_col].mode()[0]
                                    df_cleaned[missing_col] = df_cleaned[missing_col].fillna(fill_value)
                                    st.success(f"Filled missing values in {missing_col} with mode ({fill_value})")
                            
                            elif handling_method == "Fill with median":
                                if df[missing_col].dtype in ['int64', 'float64']:
                                    fill_value = df[missing_col].median()
                                    df_cleaned[missing_col] = df_cleaned[missing_col].fillna(fill_value)
                                    st.success(f"Filled missing values in {missing_col} with median ({fill_value:.2f})")
                                else:
                                    st.error("Median can only be used with numeric columns")
                            
                            elif handling_method == "Fill with custom value":
                                custom_value = st.text_input("Enter custom value")
                                if custom_value:
                                    df_cleaned[missing_col] = df_cleaned[missing_col].fillna(custom_value)
                                    st.success(f"Filled missing values in {missing_col} with '{custom_value}'")
                            
                            # Update the dataframe
                            st.session_state.uploaded_data = df_cleaned
                            st.dataframe(df_cleaned.head())
                else:
                    st.success("No missing values in the dataset!")
            
            # Tab 5: Search
            with explorer_tabs[4]:
                st.subheader("Search Data")
                
                # Select column to search
                search_col = st.selectbox("Select column to search", df.columns)
                search_term = st.text_input("Enter search term")
                
                if search_term and search_col:
                    # Handle different data types for searching
                    if df[search_col].dtype in ['int64', 'float64']:
                        try:
                            search_term_numeric = float(search_term)
                            results = df[df[search_col] == search_term_numeric]
                        except ValueError:
                            st.error("Please enter a valid number for numeric column")
                            results = pd.DataFrame()
                    else:
                        # Case-insensitive text search
                        results = df[df[search_col].astype(str).str.contains(search_term, case=False, na=False)]
                    
                    st.write(f"Found {len(results)} matching rows:")
                    st.dataframe(results)
        
        # Tab 2: Statistical Analysis
        elif st.session_state.active_analysis_tab == "Statistical Analysis":
            st.header("Statistical Analysis")
            
            stats_tabs = st.tabs(["Basic Stats", "Correlation Analysis", "Group Analysis", "Hypothesis Testing"])
            
            # Tab 1: Basic Statistics
            with stats_tabs[0]:
                st.subheader("Basic Statistical Analysis")
                
                # Select columns for analysis
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                
                if numeric_cols:
                    st.write("### Numeric Variable Statistics")
                    selected_num_cols = st.multiselect("Select numeric columns", numeric_cols, default=numeric_cols[:min(3, len(numeric_cols))])
                    
                    if selected_num_cols:
                        # Display basic statistics
                        stats_df = df[selected_num_cols].describe().T
                        
                        # Add additional statistics
                        stats_df['median'] = df[selected_num_cols].median()
                        stats_df['skewness'] = df[selected_num_cols].skew()
                        stats_df['kurtosis'] = df[selected_num_cols].kurtosis()
                        stats_df['missing'] = df[selected_num_cols].isnull().sum()
                        stats_df['missing_pct'] = (df[selected_num_cols].isnull().sum() / len(df) * 100).round(2)
                        
                        st.dataframe(stats_df)
                        
                        # Plot distributions
                        st.write("### Distributions")
                        plot_type = st.radio(
                            "Select plot type",
                            ["Histogram", "Box Plot", "Violin Plot", "KDE"]
                        )
                        
                        fig, axes = plt.subplots(1, len(selected_num_cols), figsize=(5*len(selected_num_cols), 5))
                        if len(selected_num_cols) == 1:
                            axes = [axes]
                            
                        for i, col in enumerate(selected_num_cols):
                            if plot_type == "Histogram":
                                sns.histplot(df[col].dropna(), kde=True, ax=axes[i])
                            elif plot_type == "Box Plot":
                                sns.boxplot(y=df[col].dropna(), ax=axes[i])
                            elif plot_type == "Violin Plot":
                                sns.violinplot(y=df[col].dropna(), ax=axes[i])
                            else:  # KDE
                                sns.kdeplot(df[col].dropna(), fill=True, ax=axes[i])
                            
                            axes[i].set_title(col)
                            
                        plt.tight_layout()
                        st.pyplot(fig)
                
                if categorical_cols:
                    st.write("### Categorical Variable Statistics")
                    selected_cat_cols = st.multiselect("Select categorical columns", categorical_cols, default=categorical_cols[:min(2, len(categorical_cols))])
                    
                    if selected_cat_cols:
                        for col in selected_cat_cols:
                            with st.expander(f"{col} - {df[col].nunique()} unique values"):
                                value_counts = df[col].value_counts()
                                value_pcts = (df[col].value_counts(normalize=True) * 100).round(2)
                                
                                cat_stats = pd.DataFrame({
                                    'Value': value_counts.index,
                                    'Count': value_counts.values,
                                    'Percentage': value_pcts.values
                                }).reset_index(drop=True)
                                
                                st.dataframe(cat_stats)
                                
                                # Bar chart for categorical variable
                                fig, ax = plt.subplots(figsize=(10, 5))
                                sns.barplot(x=value_counts.index[:10], y=value_counts.values[:10], ax=ax)
                                plt.title(f"Top 10 Categories in {col}")
                                plt.xticks(rotation=45)
                                plt.tight_layout()
                                st.pyplot(fig)
            
            # Tab 2: Correlation Analysis
            with stats_tabs[1]:
                st.subheader("Correlation Analysis")
                
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                
                if len(numeric_cols) < 2:
                    st.warning("Need at least 2 numeric columns for correlation analysis.")
                else:
                    # Select columns for correlation
                    selected_corr_cols = st.multiselect(
                        "Select columns for correlation analysis", 
                        numeric_cols, 
                        default=numeric_cols[:min(5, len(numeric_cols))]
                    )
                    
                    if len(selected_corr_cols) >= 2:
                        corr_method = st.radio(
                            "Correlation method",
                            ["Pearson", "Spearman", "Kendall"],
                            horizontal=True
                        )
                        
                        # Calculate correlation
                        corr_matrix = df[selected_corr_cols].corr(method=corr_method.lower())
                        
                        # Display correlation matrix
                        st.write("### Correlation Matrix")
                        st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm'))
                        
                        # Correlation heatmap
                        fig, ax = plt.subplots(figsize=(10, 8))
                        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
                        sns.heatmap(
                            corr_matrix, 
                            mask=mask, 
                            annot=True, 
                            fmt=".2f", 
                            cmap='coolwarm', 
                            linewidths=0.5, 
                            ax=ax
                        )
                        plt.title(f"{corr_method} Correlation Matrix")
                        st.pyplot(fig)
                        
                        # Pairplot (if not too many columns)
                        if len(selected_corr_cols) <= 5:
                            if st.checkbox("Show Pairplot"):
                                with st.spinner("Generating pairplot..."):
                                    fig = sns.pairplot(df[selected_corr_cols].dropna())
                                    st.pyplot(fig)
                        
                        # Correlation insights
                        st.write("### Correlation Insights")
                        
                        # Find strongest correlations
                        corr_pairs = []
                        for i in range(len(selected_corr_cols)):
                            for j in range(i+1, len(selected_corr_cols)):
                                corr_value = corr_matrix.iloc[i, j]
                                corr_pairs.append((
                                    selected_corr_cols[i], 
                                    selected_corr_cols[j], 
                                    corr_value, 
                                    abs(corr_value)
                                ))
                        
                        # Sort by absolute correlation
                        corr_pairs.sort(key=lambda x: x[3], reverse=True)
                        
                        # Display top correlations
                        top_corr_df = pd.DataFrame(
                            [(x, y, z) for x, y, z, _ in corr_pairs], 
                            columns=["Variable 1", "Variable 2", "Correlation"]
                        )
                        
                        st.dataframe(top_corr_df)
                        
                        # Plot top correlation
                        if corr_pairs:
                            top_var1, top_var2, top_corr, _ = corr_pairs[0]
                            
                            fig, ax = plt.subplots(figsize=(10, 6))
                            scatter = sns.scatterplot(x=top_var1, y=top_var2, data=df, ax=ax)
                            sns.regplot(x=top_var1, y=top_var2, data=df, scatter=False, ax=ax, line_kws={"color": "red"})
                            
                            plt.title(f"Strongest Correlation: {top_var1} vs {top_var2} (r = {top_corr:.2f})")
                            st.pyplot(fig)
            
            # Tab 3: Group Analysis
            with stats_tabs[2]:
                st.subheader("Group Analysis")
                
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                
                if not categorical_cols or not numeric_cols:
                    st.warning("Group analysis requires both categorical and numeric columns.")
                else:
                    # Select grouping column
                    group_col = st.selectbox("Select column to group by", categorical_cols)
                    
                    # Check if too many groups
                    num_groups = df[group_col].nunique()
                    if num_groups > 20:
                        st.warning(f"Selected column has {num_groups} groups. Consider using a column with fewer groups.")
                    
                    # Select columns to analyze
                    analysis_cols = st.multiselect(
                        "Select columns to analyze", 
                        numeric_cols,
                        default=numeric_cols[:min(3, len(numeric_cols))]
                    )
                    
                    if group_col and analysis_cols:
                        # Aggregation functions
                        agg_funcs = st.multiselect(
                            "Select aggregation functions",
                            ["Mean", "Median", "Sum", "Min", "Max", "Count", "Std. Dev"],
                            default=["Mean", "Median"]
                        )
                        
                        agg_func_map = {
                            "Mean": "mean",
                            "Median": "median",
                            "Sum": "sum",
                            "Min": "min",
                            "Max": "max",
                            "Count": "count",
                            "Std. Dev": "std"
                        }
                        
                        selected_aggs = {func: agg_func_map[func] for func in agg_funcs}
                        
                        if selected_aggs:
                            # Generate group statistics
                            group_stats = df.groupby(group_col)[analysis_cols].agg(list(selected_aggs.values()))
                            
                            # Flatten multi-index columns
                            group_stats.columns = [f"{col}_{agg}" for col, agg in 
                                                 zip(group_stats.columns.get_level_values(0),
                                                    group_stats.columns.get_level_values(1))]
                            
                            st.write("### Group Statistics")
                            st.dataframe(group_stats)
                            
                            # Visualization of group stats
                            st.write("### Group Comparison")
                            
                            plot_type = st.radio(
                                "Select plot type",
                                ["Bar Plot", "Box Plot", "Violin Plot"],
                                horizontal=True
                            )
                            
                            # Select column for visualization
                            viz_col = st.selectbox("Select column to visualize", analysis_cols)
                            
                            if viz_col:
                                if plot_type == "Bar Plot":
                                    fig, ax = plt.subplots(figsize=(12, 6))
                                    sns.barplot(x=group_col, y=viz_col, data=df, ax=ax)
                                    plt.title(f"Mean {viz_col} by {group_col}")
                                    plt.xticks(rotation=45)
                                    plt.tight_layout()
                                    st.pyplot(fig)
                                
                                elif plot_type == "Box Plot":
                                    fig, ax = plt.subplots(figsize=(12, 6))
                                    sns.boxplot(x=group_col, y=viz_col, data=df, ax=ax)
                                    plt.title(f"Distribution of {viz_col} by {group_col}")
                                    plt.xticks(rotation=45)
                                    plt.tight_layout()
                                    st.pyplot(fig)
                                
                                else:  # Violin Plot
                                    fig, ax = plt.subplots(figsize=(12, 6))
                                    sns.violinplot(x=group_col, y=viz_col, data=df, ax=ax)
                                    plt.title(f"Distribution of {viz_col} by {group_col}")
                                    plt.xticks(rotation=45)
                                    plt.tight_layout()
                                    st.pyplot(fig)
            
            # Tab 4: Hypothesis Testing
            with stats_tabs[3]:
                st.subheader("Hypothesis Testing")
                
                st.write("""
                Hypothesis testing allows you to determine if there are statistically significant 
                differences or relationships in your data.
                """)
                
                test_type = st.selectbox(
                    "Select test type",
                    ["T-Test (Two Groups)", "ANOVA (Multiple Groups)", "Chi-Square (Categorical)", "Correlation Test"]
                )
                
                try:
                    from scipy import stats
                    
                    if test_type == "T-Test (Two Groups)":
                        st.write("""
                        The t-test compares the means of two groups to determine if they are 
                        significantly different from each other.
                        """)
                        
                        # Select group and numeric columns
                        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                        
                        if not categorical_cols or not numeric_cols:
                            st.warning("T-test requires both categorical and numeric columns.")
                        else:
                            group_col = st.selectbox("Select column with groups", categorical_cols)
                            value_col = st.selectbox("Select numeric column to compare", numeric_cols)
                            
                            # Check if column has exactly 2 groups
                            groups = df[group_col].dropna().unique()
                            
                            if len(groups) < 2:
                                st.warning(f"Column '{group_col}' has less than 2 groups.")
                            elif len(groups) > 2:
                                st.warning(f"Column '{group_col}' has {len(groups)} groups. T-test requires exactly 2 groups.")
                                st.write("Select which two groups to compare:")
                                group1 = st.selectbox("Group 1", groups, index=0)
                                group2 = st.selectbox("Group 2", groups, index=min(1, len(groups)-1))
                                
                                # Filter data for selected groups
                                group1_data = df[df[group_col] == group1][value_col].dropna()
                                group2_data = df[df[group_col] == group2][value_col].dropna()
                                
                                if len(group1_data) < 2 or len(group2_data) < 2:
                                    st.warning("One or both groups have insufficient data for t-test (need at least 2 values per group).")
                                else:
                                    # Run t-test
                                    t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=False)
                                    
                                    st.write("### T-Test Results")
                                    st.write(f"**Groups compared:** {group1} vs {group2}")
                                    st.write(f"**Variable tested:** {value_col}")
                                    st.write(f"**t-statistic:** {t_stat:.4f}")
                                    st.write(f"**p-value:** {p_value:.4f}")
                                    
                                    # Interpretation
                                    alpha = 0.05
                                    if p_value < alpha:
                                        st.success(f"**Result:** Statistically significant difference (p < {alpha})")
                                        st.write(f"We reject the null hypothesis. There is a significant difference in {value_col} between {group1} and {group2}.")
                                    else:
                                        st.info(f"**Result:** No statistically significant difference (p >= {alpha})")
                                        st.write(f"We fail to reject the null hypothesis. There is no significant difference in {value_col} between {group1} and {group2}.")
                                    
                                    # Visualization
                                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                                    
                                    # Box plot
                                    sns.boxplot(x=group_col, y=value_col, data=df[df[group_col].isin([group1, group2])], ax=ax1)
                                    ax1.set_title(f"Box Plot: {value_col} by Group")
                                    
                                    # Means with error bars
                                    group_means = [group1_data.mean(), group2_data.mean()]
                                    group_errors = [group1_data.sem(), group2_data.sem()]
                                    
                                    ax2.bar([0, 1], group_means, yerr=group_errors, capsize=10, alpha=0.7)
                                    ax2.set_xticks([0, 1])
                                    ax2.set_xticklabels([group1, group2])
                                    ax2.set_title(f"Mean {value_col} with Standard Error")
                                    
                                    plt.tight_layout()
                                    st.pyplot(fig)
                            else:
                                # If exactly 2 groups
                                group1, group2 = groups
                                
                                # Filter data for the two groups
                                group1_data = df[df[group_col] == group1][value_col].dropna()
                                group2_data = df[df[group_col] == group2][value_col].dropna()
                                
                                if len(group1_data) < 2 or len(group2_data) < 2:
                                    st.warning("One or both groups have insufficient data for t-test (need at least 2 values per group).")
                                else:
                                    # Run t-test
                                    t_stat, p_value = stats.ttest_ind(group1_data, group2_data, equal_var=False)
                                    
                                    st.write("### T-Test Results")
                                    st.write(f"**Groups compared:** {group1} vs {group2}")
                                    st.write(f"**Variable tested:** {value_col}")
                                    st.write(f"**t-statistic:** {t_stat:.4f}")
                                    st.write(f"**p-value:** {p_value:.4f}")
                                    
                                    # Interpretation
                                    alpha = 0.05
                                    if p_value < alpha:
                                        st.success(f"**Result:** Statistically significant difference (p < {alpha})")
                                        st.write(f"We reject the null hypothesis. There is a significant difference in {value_col} between {group1} and {group2}.")
                                    else:
                                        st.info(f"**Result:** No statistically significant difference (p >= {alpha})")
                                        st.write(f"We fail to reject the null hypothesis. There is no significant difference in {value_col} between {group1} and {group2}.")
                                    
                                    # Visualization
                                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                                    
                                    # Box plot
                                    sns.boxplot(x=group_col, y=value_col, data=df, ax=ax1)
                                    ax1.set_title(f"Box Plot: {value_col} by Group")
                                    
                                    # Means with error bars
                                    group_means = [group1_data.mean(), group2_data.mean()]
                                    group_errors = [group1_data.sem(), group2_data.sem()]
                                    
                                    ax2.bar([0, 1], group_means, yerr=group_errors, capsize=10, alpha=0.7)
                                    ax2.set_xticks([0, 1])
                                    ax2.set_xticklabels([group1, group2])
                                    ax2.set_title(f"Mean {value_col} with Standard Error")
                                    
                                    plt.tight_layout()
                                    st.pyplot(fig)
                    
                    elif test_type == "ANOVA (Multiple Groups)":
                        st.write("""
                        ANOVA (Analysis of Variance) tests if there are significant differences between 
                        the means of three or more groups.
                        """)
                        
                        # Select group and numeric columns
                        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                        
                        if not categorical_cols or not numeric_cols:
                            st.warning("ANOVA requires both categorical and numeric columns.")
                        else:
                            group_col = st.selectbox("Select column with groups", categorical_cols, key="anova_group")
                            value_col = st.selectbox("Select numeric column to compare", numeric_cols, key="anova_value")
                            
                            # Check if column has at least 3 groups
                            groups = df[group_col].dropna().unique()
                            
                            if len(groups) < 3:
                                st.warning(f"Column '{group_col}' has {len(groups)} groups. ANOVA is typically used for 3+ groups.")
                                st.write("Consider using a t-test instead.")
                            else:
                                # Run ANOVA
                                group_data = [df[df[group_col] == group][value_col].dropna() for group in groups]
                                
                                # Check if all groups have data
                                if any(len(data) < 2 for data in group_data):
                                    st.warning("One or more groups have insufficient data for ANOVA (need at least 2 values per group).")
                                else:
                                    f_stat, p_value = stats.f_oneway(*group_data)
                                    
                                    st.write("### ANOVA Results")
                                    st.write(f"**Groups compared:** {', '.join(map(str, groups))}")
                                    st.write(f"**Variable tested:** {value_col}")
                                    st.write(f"**F-statistic:** {f_stat:.4f}")
                                    st.write(f"**p-value:** {p_value:.4f}")
                                    
                                    # Interpretation
                                    alpha = 0.05
                                    if p_value < alpha:
                                        st.success(f"**Result:** Statistically significant difference between groups (p < {alpha})")
                                        st.write(f"We reject the null hypothesis. There are significant differences in {value_col} between at least some of the groups.")
                                        
                                        # Post-hoc test
                                        st.write("### Post-hoc Test (Tukey's HSD)")
                                        st.write("Running post-hoc tests to determine which specific groups differ...")
                                        
                                        from statsmodels.stats.multicomp import pairwise_tukeyhsd
                                        
                                        # Prepare data for Tukey's test
                                        data = []
                                        groups_list = []
                                        
                                        for group in groups:
                                            group_values = df[df[group_col] == group][value_col].dropna()
                                            data.extend(group_values)
                                            groups_list.extend([str(group)] * len(group_values))
                                        
                                        # Run Tukey's test
                                        tukey = pairwise_tukeyhsd(data, groups_list, alpha=0.05)
                                        
                                        # Display results
                                        tukey_results = pd.DataFrame(
                                            data=np.c_[tukey.groupsunique[tukey.pairindices], 
                                                      tukey.meandiffs, tukey.confint, tukey.reject], 
                                            columns=['group1', 'group2', 'mean_diff', 'lower', 'upper', 'reject']
                                        )
                                        
                                        st.dataframe(tukey_results)
                                        
                                    else:
                                        st.info(f"**Result:** No statistically significant differences between groups (p >= {alpha})")
                                        st.write(f"We fail to reject the null hypothesis. There are no significant differences in {value_col} among the groups.")
                                    
                                    # Visualization
                                    fig, ax = plt.subplots(figsize=(12, 6))
                                    
                                    # Box plot
                                    sns.boxplot(x=group_col, y=value_col, data=df, ax=ax)
                                    ax.set_title(f"Box Plot: {value_col} by Group")
                                    plt.xticks(rotation=45)
                                    plt.tight_layout()
                                    
                                    st.pyplot(fig)
                    
                    elif test_type == "Chi-Square (Categorical)":
                        st.write("""
                        The Chi-Square test determines if there is a significant association between 
                        two categorical variables.
                        """)
                        
                        # Select two categorical columns
                        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                        
                        if len(categorical_cols) < 2:
                            st.warning("Chi-Square test requires at least two categorical columns.")
                        else:
                            cat_col1 = st.selectbox("Select first categorical column", categorical_cols, index=0)
                            cat_col2 = st.selectbox("Select second categorical column", categorical_cols, index=min(1, len(categorical_cols)-1))
                            
                            if cat_col1 == cat_col2:
                                st.warning("Please select two different columns.")
                            else:
                                # Create contingency table
                                contingency_table = pd.crosstab(df[cat_col1], df[cat_col2])
                                
                                st.write("### Contingency Table")
                                st.dataframe(contingency_table)
                                
                                # Run Chi-Square test
                                chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                                
                                st.write("### Chi-Square Test Results")
                                st.write(f"**Variables tested:** {cat_col1} vs {cat_col2}")
                                st.write(f"**Chi-Square statistic:** {chi2:.4f}")
                                st.write(f"**Degrees of freedom:** {dof}")
                                st.write(f"**p-value:** {p_value:.4f}")
                                
                                # Interpretation
                                alpha = 0.05
                                if p_value < alpha:
                                    st.success(f"**Result:** Statistically significant association (p < {alpha})")
                                    st.write(f"We reject the null hypothesis. There is a significant association between {cat_col1} and {cat_col2}.")
                                else:
                                    st.info(f"**Result:** No statistically significant association (p >= {alpha})")
                                    st.write(f"We fail to reject the null hypothesis. There is no significant association between {cat_col1} and {cat_col2}.")
                                
                                # Visualization
                                st.write("### Visualization")
                                
                                # Stacked bar chart
                                fig, ax = plt.subplots(figsize=(12, 6))
                                contingency_table_pct = contingency_table.div(contingency_table.sum(axis=1), axis=0)
                                contingency_table_pct.plot(kind='bar', stacked=True, ax=ax)
                                ax.set_title(f"Stacked Bar Chart: {cat_col1} vs {cat_col2}")
                                ax.set_ylabel("Percentage")
                                plt.legend(title=cat_col2)
                                plt.tight_layout()
                                
                                st.pyplot(fig)
                    
                    elif test_type == "Correlation Test":
                        st.write("""
                        The correlation test determines if there is a statistically significant 
                        correlation between two numeric variables.
                        """)
                        
                        # Select two numeric columns
                        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                        
                        if len(numeric_cols) < 2:
                            st.warning("Correlation test requires at least two numeric columns.")
                        else:
                            num_col1 = st.selectbox("Select first numeric column", numeric_cols, index=0)
                            num_col2 = st.selectbox("Select second numeric column", numeric_cols, index=min(1, len(numeric_cols)-1))
                            
                            corr_method = st.radio(
                                "Correlation method",
                                ["Pearson", "Spearman"],
                                horizontal=True
                            )
                            
                            if num_col1 == num_col2:
                                st.warning("Please select two different columns.")
                            else:
                                # Drop rows with NaN in either column
                                valid_data = df[[num_col1, num_col2]].dropna()
                                
                                if len(valid_data) < 3:
                                    st.warning("Insufficient data for correlation test (need at least 3 valid pairs).")
                                else:
                                    # Run correlation test
                                    if corr_method == "Pearson":
                                        corr, p_value = stats.pearsonr(valid_data[num_col1], valid_data[num_col2])
                                    else:  # Spearman
                                        corr, p_value = stats.spearmanr(valid_data[num_col1], valid_data[num_col2])
                                    
                                    st.write("### Correlation Test Results")
                                    st.write(f"**Variables tested:** {num_col1} vs {num_col2}")
                                    st.write(f"**Correlation method:** {corr_method}")
                                    st.write(f"**Correlation coefficient:** {corr:.4f}")
                                    st.write(f"**p-value:** {p_value:.4f}")
                                    
                                    # Interpretation
                                    alpha = 0.05
                                    if p_value < alpha:
                                        st.success(f"**Result:** Statistically significant correlation (p < {alpha})")
                                        
                                        if corr > 0:
                                            direction = "positive"
                                        else:
                                            direction = "negative"
                                            
                                        if abs(corr) > 0.7:
                                            strength = "strong"
                                        elif abs(corr) > 0.3:
                                            strength = "moderate"
                                        else:
                                            strength = "weak"
                                            
                                        st.write(f"There is a statistically significant {strength} {direction} correlation between {num_col1} and {num_col2}.")
                                    else:
                                        st.info(f"**Result:** No statistically significant correlation (p >= {alpha})")
                                        st.write(f"We fail to reject the null hypothesis. There is no significant correlation between {num_col1} and {num_col2}.")
                                    
                                    # Visualization
                                    fig, ax = plt.subplots(figsize=(10, 6))
                                    
                                    # Scatter plot with regression line
                                    sns.scatterplot(x=num_col1, y=num_col2, data=df, ax=ax)
                                    sns.regplot(x=num_col1, y=num_col2, data=df, scatter=False, ax=ax, line_kws={"color": "red"})
                                    
                                    ax.set_title(f"Scatter Plot: {num_col1} vs {num_col2} (r = {corr:.2f})")
                                    
                                    st.pyplot(fig)
                except ImportError:
                    st.error("The SciPy package is required for hypothesis testing. Please install it to use this feature.")
        
        # Tab 3: Visualization Studio
        elif st.session_state.active_analysis_tab == "Visualization Studio":
            st.header("Visualization Studio")
            
            # Visualization selection
            viz_type = st.selectbox(
                "Select Visualization Type",
                [
                    "Scatter Plot", "Line Chart", "Bar Chart", "Histogram", 
                    "Box Plot", "Violin Plot", "Heatmap", "Pair Plot", "Distribution Plot"
                ]
            )
            
            # Column selection based on visualization type
            if viz_type in ["Scatter Plot"]:
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                
                if len(numeric_cols) < 2:
                    st.warning("Need at least 2 numeric columns for a scatter plot.")
                else:
                    x_col = st.selectbox("X-axis", numeric_cols, index=0)
                    y_col = st.selectbox("Y-axis", numeric_cols, index=min(1, len(numeric_cols)-1))
                    
                    # Optional color grouping
                    color_options = ["None"] + df.columns.tolist()
                    color_col = st.selectbox("Color by (optional)", color_options)
                    
                    if color_col == "None":
                        color_col = None
                    
                    # Optional size variable
                    size_options = ["None"] + numeric_cols
                    size_col = st.selectbox("Size by (optional)", size_options)
                    
                    if size_col == "None":
                        size_col = None
                    
                    # Create visualization
                    if st.button("Generate Scatter Plot"):
                        st.write(f"### Scatter Plot: {x_col} vs {y_col}")
                        
                        # Create plot
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        if color_col and size_col:
                            scatter = sns.scatterplot(
                                x=x_col, y=y_col, hue=color_col, size=size_col, 
                                sizes=(20, 200), alpha=0.7, data=df, ax=ax
                            )
                        elif color_col:
                            scatter = sns.scatterplot(
                                x=x_col, y=y_col, hue=color_col, 
                                alpha=0.7, data=df, ax=ax
                            )
                        elif size_col:
                            scatter = sns.scatterplot(
                                x=x_col, y=y_col, size=size_col, 
                                sizes=(20, 200), alpha=0.7, data=df, ax=ax
                            )
                        else:
                            scatter = sns.scatterplot(
                                x=x_col, y=y_col, alpha=0.7, data=df, ax=ax
                            )
                        
                        # Add regression line
                        add_regression = st.checkbox("Add regression line")
                        if add_regression:
                            sns.regplot(
                                x=x_col, y=y_col, data=df, scatter=False, 
                                ax=ax, line_kws={"color": "red"}
                            )
                            
                            # Calculate correlation
                            correlation = df[[x_col, y_col]].corr().iloc[0, 1]
                            plt.title(f"Scatter Plot: {x_col} vs {y_col} (r = {correlation:.2f})")
                        else:
                            plt.title(f"Scatter Plot: {x_col} vs {y_col}")
                        
                        # Display plot
                        st.pyplot(fig)
            
            elif viz_type in ["Line Chart"]:
                # Column selection
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                all_cols = df.columns.tolist()
                
                # Check for datetime columns
                datetime_cols = []
                for col in all_cols:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        datetime_cols.append(col)
                    else:
                        try:
                            # Try to convert to datetime
                            pd.to_datetime(df[col])
                            datetime_cols.append(col)
                        except:
                            pass
                
                if not datetime_cols and not numeric_cols:
                    st.warning("Need at least one datetime or numeric column for x-axis and one numeric column for y-axis.")
                else:
                    # X-axis can be datetime or numeric
                    x_options = datetime_cols + numeric_cols
                    x_col = st.selectbox("X-axis", x_options, index=0)
                    
                    # Y-axis must be numeric
                    y_col = st.selectbox("Y-axis", numeric_cols, index=min(1, len(numeric_cols)-1))
                    
                    # Optional grouping
                    group_options = ["None"] + [col for col in all_cols if col not in [x_col, y_col]]
                    group_col = st.selectbox("Group by (optional)", group_options)
                    
                    if group_col == "None":
                        group_col = None
                    
                    # Create visualization
                    if st.button("Generate Line Chart"):
                        st.write(f"### Line Chart: {y_col} over {x_col}")
                        
                        # Convert to datetime if needed
                        if x_col in datetime_cols and not pd.api.types.is_datetime64_any_dtype(df[x_col]):
                            try:
                                df = df.copy()
                                df[x_col] = pd.to_datetime(df[x_col])
                            except:
                                st.error(f"Failed to convert {x_col} to datetime.")
                                return
                        
                        # Sort by x-axis
                        df_sorted = df.sort_values(by=x_col)
                        
                        # Create plot
                        fig, ax = plt.subplots(figsize=(12, 6))
                        
                        if group_col:
                            for group, group_df in df_sorted.groupby(group_col):
                                ax.plot(group_df[x_col], group_df[y_col], marker='o', linestyle='-', label=str(group))
                            ax.legend(title=group_col)
                        else:
                            ax.plot(df_sorted[x_col], df_sorted[y_col], marker='o', linestyle='-')
                        
                        plt.title(f"Line Chart: {y_col} over {x_col}")
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        
                        # Display plot
                        st.pyplot(fig)
            
            elif viz_type in ["Bar Chart"]:
                all_cols = df.columns.tolist()
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                
                # Options for bar chart
                chart_subtype = st.radio(
                    "Bar Chart Type",
                    ["Simple (one variable)", "Grouped", "Stacked"],
                    horizontal=True
                )
                
                if chart_subtype == "Simple (one variable)":
                    # Single variable bar chart
                    x_col = st.selectbox("Category (X-axis)", all_cols, index=0)
                    
                    # For the y-axis, allow count or a numeric column
                    y_options = ["Count"] + numeric_cols
                    y_col = st.selectbox("Value (Y-axis)", y_options)
                    
                    # Sorting options
                    sort_options = ["None", "Ascending", "Descending"]
                    sort_by = st.selectbox("Sort bars", sort_options)
                    
                    # Limit for large categories
                    n_categories = df[x_col].nunique()
                    if n_categories > 10:
                        limit = st.slider("Limit to top N categories", 5, 30, 10)
                    else:
                        limit = n_categories
                    
                    # Create visualization
                    if st.button("Generate Bar Chart"):
                        st.write(f"### Bar Chart: {x_col}")
                        
                        # Prepare data
                        if y_col == "Count":
                            # Count plot
                            value_counts = df[x_col].value_counts()
                            
                            # Apply sorting
                            if sort_by == "Ascending":
                                value_counts = value_counts.sort_values()
                            elif sort_by == "Descending":
                                value_counts = value_counts.sort_values(ascending=False)
                            
                            # Limit categories
                            if len(value_counts) > limit:
                                value_counts = value_counts.head(limit)
                            
                            # Create plot
                            fig, ax = plt.subplots(figsize=(12, 6))
                            value_counts.plot(kind="bar", ax=ax)
                            plt.title(f"Bar Chart: Count of {x_col}")
                            plt.xlabel(x_col)
                            plt.ylabel("Count")
                            
                        else:
                            # Regular bar chart with numeric y-axis
                            # Group by x column and calculate mean of y column
                            group_data = df.groupby(x_col)[y_col].mean().reset_index()
                            
                            # Apply sorting
                            if sort_by == "Ascending":
                                group_data = group_data.sort_values(by=y_col)
                            elif sort_by == "Descending":
                                group_data = group_data.sort_values(by=y_col, ascending=False)
                            
                            # Limit categories
                            if len(group_data) > limit:
                                group_data = group_data.head(limit)
                            
                            # Create plot
                            fig, ax = plt.subplots(figsize=(12, 6))
                            sns.barplot(x=x_col, y=y_col, data=group_data, ax=ax)
                            plt.title(f"Bar Chart: Average {y_col} by {x_col}")
                        
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        
                        # Display plot
                        st.pyplot(fig)
                
                elif chart_subtype == "Grouped":
                    # Grouped bar chart needs:
                    # - Main category (x)
                    # - Grouping category (hue)
                    # - Value (y)
                    
                    categorical_cols = [col for col in all_cols if df[col].nunique() < 30]
                    
                    if len(categorical_cols) < 2:
                        st.warning("Need at least 2 categorical columns with fewer than 30 categories each for a grouped bar chart.")
                    else:
                        x_col = st.selectbox("Main Category (X-axis)", categorical_cols, index=0)
                        
                        # Filter out the x_col for the hue selection
                        hue_options = [col for col in categorical_cols if col != x_col]
                        hue_col = st.selectbox("Group By", hue_options, index=0)
                        
                        # For the y-axis, allow count or a numeric column
                        y_options = ["Count"] + numeric_cols
                        y_col = st.selectbox("Value (Y-axis)", y_options)
                        
                        # Create visualization
                        if st.button("Generate Grouped Bar Chart"):
                            st.write(f"### Grouped Bar Chart: {x_col} grouped by {hue_col}")
                            
                            # Create plot
                            fig, ax = plt.subplots(figsize=(14, 7))
                            
                            if y_col == "Count":
                                # Count plot with grouping
                                sns.countplot(x=x_col, hue=hue_col, data=df, ax=ax)
                                plt.title(f"Grouped Bar Chart: Count of {x_col} by {hue_col}")
                                plt.ylabel("Count")
                            else:
                                # Regular bar chart with numeric y-axis
                                sns.barplot(x=x_col, y=y_col, hue=hue_col, data=df, ax=ax)
                                plt.title(f"Grouped Bar Chart: {y_col} by {x_col} and {hue_col}")
                            
                            plt.xticks(rotation=45)
                            plt.legend(title=hue_col)
                            plt.tight_layout()
                            
                            # Display plot
                            st.pyplot(fig)
                
                else:  # Stacked bar chart
                    categorical_cols = [col for col in all_cols if df[col].nunique() < 30]
                    
                    if len(categorical_cols) < 2:
                        st.warning("Need at least 2 categorical columns with fewer than 30 categories each for a stacked bar chart.")
                    else:
                        x_col = st.selectbox("Main Category (X-axis)", categorical_cols, index=0)
                        
                        # Filter out the x_col for the stack selection
                        stack_options = [col for col in categorical_cols if col != x_col]
                        stack_col = st.selectbox("Stack By", stack_options, index=0)
                        
                        # Create visualization
                        if st.button("Generate Stacked Bar Chart"):
                            st.write(f"### Stacked Bar Chart: {x_col} stacked by {stack_col}")
                            
                            # Create contingency table
                            contingency = pd.crosstab(df[x_col], df[stack_col])
                            
                            # Create plot
                            fig, ax = plt.subplots(figsize=(14, 7))
                            contingency.plot(kind='bar', stacked=True, ax=ax)
                            
                            plt.title(f"Stacked Bar Chart: {x_col} by {stack_col}")
                            plt.ylabel("Count")
                            plt.xticks(rotation=45)
                            plt.legend(title=stack_col)
                            plt.tight_layout()
                            
                            # Display plot
                            st.pyplot(fig)
            
            elif viz_type in ["Histogram", "Distribution Plot"]:
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                
                if not numeric_cols:
                    st.warning("Need at least one numeric column for a histogram.")
                else:
                    col = st.selectbox("Select column", numeric_cols, index=0)
                    
                    # Histogram options
                    bins = st.slider("Number of bins", 5, 100, 20)
                    kde = st.checkbox("Show KDE", value=True)
                    
                    # Create visualization
                    if st.button(f"Generate {viz_type}"):
                        st.write(f"### {viz_type}: {col}")
                        
                        # Create plot
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        sns.histplot(df[col].dropna(), bins=bins, kde=kde, ax=ax)
                        
                        # Add mean and median lines
                        mean_val = df[col].mean()
                        median_val = df[col].median()
                        
                        ax.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
                        ax.axvline(median_val, color='green', linestyle='-.', label=f'Median: {median_val:.2f}')
                        
                        plt.title(f"{viz_type}: {col}")
                        plt.legend()
                        
                        # Display plot
                        st.pyplot(fig)
                        
                        # Display statistics
                        st.write("### Distribution Statistics")
                        stats = df[col].describe()
                        
                        # Add additional statistics
                        stats_df = pd.DataFrame({
                            'Statistic': stats.index,
                            'Value': stats.values
                        })
                        
                        # Add skewness and kurtosis
                        extra_stats = pd.DataFrame({
                            'Statistic': ['skewness', 'kurtosis'],
                            'Value': [df[col].skew(), df[col].kurtosis()]
                        })
                        
                        stats_df = pd.concat([stats_df, extra_stats])
                        
                        st.dataframe(stats_df)
            
            elif viz_type in ["Box Plot", "Violin Plot"]:
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                categorical_cols = [col for col in df.columns if col not in numeric_cols]
                
                if not numeric_cols:
                    st.warning(f"Need at least one numeric column for a {viz_type}.")
                else:
                    y_col = st.selectbox("Numeric column (Y-axis)", numeric_cols, index=0)
                    
                    # Optional x-axis grouping
                    x_options = ["None"] + categorical_cols
                    x_col = st.selectbox("Group by (X-axis, optional)", x_options)
                    
                    if x_col == "None":
                        x_col = None
                    
                    # Optional hue
                    hue_options = ["None"] + [col for col in categorical_cols if col != x_col]
                    hue_col = st.selectbox("Color by (optional)", hue_options)
                    
                    if hue_col == "None":
                        hue_col = None
                    
                    # Create visualization
                    if st.button(f"Generate {viz_type}"):
                        st.write(f"### {viz_type}: {y_col}")
                        
                        # Create plot
                        fig, ax = plt.subplots(figsize=(12, 6))
                        
                        if viz_type == "Box Plot":
                            if x_col and hue_col:
                                sns.boxplot(x=x_col, y=y_col, hue=hue_col, data=df, ax=ax)
                            elif x_col:
                                sns.boxplot(x=x_col, y=y_col, data=df, ax=ax)
                            else:
                                sns.boxplot(y=y_col, data=df, ax=ax)
                        else:  # Violin Plot
                            if x_col and hue_col:
                                sns.violinplot(x=x_col, y=y_col, hue=hue_col, data=df, ax=ax)
                            elif x_col:
                                sns.violinplot(x=x_col, y=y_col, data=df, ax=ax)
                            else:
                                sns.violinplot(y=y_col, data=df, ax=ax)
                        
                        title = f"{viz_type}: {y_col}"
                        if x_col:
                            title += f" by {x_col}"
                        if hue_col:
                            title += f" and {hue_col}"
                            
                        plt.title(title)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        
                        # Display plot
                        st.pyplot(fig)
            
            elif viz_type == "Heatmap":
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                
                if len(numeric_cols) < 2:
                    st.warning("Need at least 2 numeric columns for a heatmap.")
                else:
                    # Select columns for correlation
                    selected_cols = st.multiselect(
                        "Select columns for correlation heatmap", 
                        numeric_cols, 
                        default=numeric_cols[:min(5, len(numeric_cols))]
                    )
                    
                    # Correlation method
                    corr_method = st.radio(
                        "Correlation method",
                        ["Pearson", "Spearman", "Kendall"],
                        horizontal=True
                    )
                    
                    if len(selected_cols) >= 2:
                        # Create visualization
                        if st.button("Generate Heatmap"):
                            st.write(f"### Correlation Heatmap")
                            
                            # Calculate correlation
                            corr_matrix = df[selected_cols].corr(method=corr_method.lower())
                            
                            # Create plot
                            fig, ax = plt.subplots(figsize=(10, 8))
                            sns.heatmap(
                                corr_matrix, 
                                annot=True, 
                                fmt=".2f", 
                                cmap='coolwarm', 
                                linewidths=0.5, 
                                ax=ax
                            )
                            plt.title(f"{corr_method} Correlation Heatmap")
                            
                            # Display plot
                            st.pyplot(fig)
                    else:
                        st.warning("Please select at least 2 columns for the heatmap.")
            
            elif viz_type == "Pair Plot":
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
                
                if len(numeric_cols) < 2:
                    st.warning("Need at least 2 numeric columns for a pair plot.")
                else:
                    # Select columns
                    selected_cols = st.multiselect(
                        "Select columns for pair plot", 
                        numeric_cols, 
                        default=numeric_cols[:min(4, len(numeric_cols))]
                    )
                    
                    # Optional hue
                    hue_options = ["None"] + df.columns.tolist()
                    hue_col = st.selectbox("Color by (optional)", hue_options)
                    
                    if hue_col == "None":
                        hue_col = None
                    
                    if len(selected_cols) >= 2:
                        # Create visualization
                        if st.button("Generate Pair Plot"):
                            st.write(f"### Pair Plot")
                            
                            # Warning for large datasets
                            if len(df) > 1000:
                                st.warning("Large dataset detected. Pair plot may take a while to generate.")
                            
                            # Create plot
                            with st.spinner("Generating pair plot..."):
                                if hue_col:
                                    # Limit hue categories if too many
                                    if df[hue_col].nunique() > 5:
                                        st.warning(f"The column '{hue_col}' has {df[hue_col].nunique()} unique values. Limiting to top 5.")
                                        top_categories = df[hue_col].value_counts().nlargest(5).index
                                        plot_df = df[df[hue_col].isin(top_categories)]
                                    else:
                                        plot_df = df
                                    
                                    g = sns.pairplot(
                                        plot_df, 
                                        vars=selected_cols, 
                                        hue=hue_col,
                                        plot_kws={"alpha": 0.5}
                                    )
                                else:
                                    g = sns.pairplot(
                                        df, 
                                        vars=selected_cols,
                                        plot_kws={"alpha": 0.5}
                                    )
                                
                                # Display plot
                                st.pyplot(g)
                    else:
                        st.warning("Please select at least 2 columns for the pair plot.")
        
        # Tab 4: AI Insights
        elif st.session_state.active_analysis_tab == "AI Insights":
            st.header("AI-Powered Data Insights")
            
            st.write("""
            This tool uses AI to generate insights about your data. You can ask specific
            questions or get general observations about patterns and trends.
            """)
            
            # AI insights options
            insight_type = st.radio(
                "Type of insight",
                ["General Data Insights", "Answer Specific Question"],
                horizontal=True
            )
            
            if insight_type == "General Data Insights":
                if st.button("Generate Insights"):
                    with st.spinner("Analyzing data and generating insights..."):
                        insights = generate_ai_insights(df)
                        
                        st.success("✅ Insights generated!")
                        st.markdown("### Key Insights")
                        st.markdown(insights)
                        
                        # Add to analysis history
                        if "analysis_history" in st.session_state:
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.analysis_history.append({
                                "type": "General Insights",
                                "timestamp": timestamp,
                                "content": insights
                            })
            else:
                # Ask specific question
                question = st.text_area(
                    "Ask a question about your data",
                    placeholder="e.g., What are the main factors affecting sales?"
                )
                
                if st.button("Get Answer") and question:
                    with st.spinner("Analyzing data to answer your question..."):
                        answer = generate_ai_insights(df, question)
                        
                        st.success("✅ Analysis complete!")
                        st.markdown(f"### Answer to: {question}")
                        st.markdown(answer)
                        
                        # Add to analysis history
                        if "analysis_history" in st.session_state:
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.analysis_history.append({
                                "type": "Question",
                                "question": question,
                                "timestamp": timestamp,
                                "content": answer
                            })
            
            # History section
            if "analysis_history" in st.session_state and st.session_state.analysis_history:
                st.markdown("---")
                st.subheader("Analysis History")
                
                for i, item in enumerate(reversed(st.session_state.analysis_history)):
                    with st.expander(f"{item['timestamp']} - {item['type']}"):
                        if "question" in item:
                            st.markdown(f"**Question:** {item['question']}")
                        st.markdown(item["content"])
        
        # Tab 5: Code Generator
        elif st.session_state.active_analysis_tab == "Code Generator":
            st.header("Analysis Code Generator")
            
            st.write("""
            Generate Python code for various data analysis tasks. You can use this code
            in your own projects or modify it to suit your specific needs.
            """)
            
            # Code generator options
            code_task = st.selectbox(
                "Select analysis task",
                [
                    "Basic EDA (Exploratory Data Analysis)",
                    "Feature Engineering",
                    "Visualization",
                    "Statistical Analysis",
                    "Machine Learning Model",
                    "Custom Analysis"
                ]
            )
            
            if code_task == "Custom Analysis":
                custom_task = st.text_area(
                    "Describe your analysis task",
                    placeholder="e.g., Generate a correlation heatmap and identify the top 3 features correlated with the target variable"
                )
            
            # Generate code
            if st.button("Generate Code"):
                with st.spinner("Generating code..."):
                    try:
                        # Create prompt for OpenAI
                        if code_task == "Custom Analysis":
                            if not custom_task:
                                st.warning("Please describe your custom analysis task.")
                                return
                            
                            task_description = custom_task
                        else:
                            task_description = code_task
                        
                        # Get column types and first few rows
                        column_info = {}
                        for col in df.columns:
                            column_info[col] = str(df[col].dtype)
                        
                        # Sample data (first 5 rows)
                        sample_data = df.head(5).to_dict(orient='records')
                        
                        prompt = f"""
                        Generate Python code for {task_description} on a dataset with the following columns:
                        
                        Column information:
                        {json.dumps(column_info, indent=2)}
                        
                        Sample data:
                        {json.dumps(sample_data, indent=2)}
                        
                        The code should be well-commented, easy to understand, and use best practices.
                        Use pandas, numpy, matplotlib, seaborn, scipy, and scikit-learn as needed.
                        The dataframe is already loaded as 'df'.
                        """
                        
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a data scientist creating Python code for data analysis tasks."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.4,
                            max_tokens=1000
                        )
                        
                        generated_code = response.choices[0].message.content.strip()
                        
                        # Extract code if wrapped in ```python blocks
                        if "```python" in generated_code:
                            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
                        elif "```" in generated_code:
                            generated_code = generated_code.split("```")[1].split("```")[0].strip()
                        
                        st.success("✅ Code generated successfully!")
                        
                        # Display code
                        st.subheader("Generated Python Code")
                        st.code(generated_code, language="python")
                        
                        # Copy to clipboard button
                        copy_button = """
                        <textarea id="code-text" style="position: absolute; left: -9999px;">{}</textarea>
                        <button onclick="copyCode()">Copy Code</button>

                        <script>
                        function copyCode() {{
                            var copyText = document.getElementById("code-text");
                            copyText.select();
                            document.execCommand("copy");
                            alert("Code copied to clipboard!");
                        }}
                        </script>
                        """.format(generated_code)

                        st.markdown(copy_button, unsafe_allow_html=True)

                        
                        # Download as .py file
                        st.download_button(
                            label="Download as .py file",
                            data=generated_code,
                            file_name="analysis_code.py",
                            mime="text/plain"
                        )
                        
                        # Option to execute code (with caution)
                        if st.checkbox("Execute code (preview only)"):
                            st.warning("⚠️ This is a preview feature. Code execution could potentially modify your data.")
                            
                            # Display code with the option to edit
                            edited_code = st.text_area("Edit code before execution", generated_code, height=300)
                            
                            if st.button("Run Code"):
                                try:
                                    # Create locals dict with the dataframe
                                    locals_dict = {"df": df}
                                    
                                    # Capture output
                                    from io import StringIO
                                    import sys
                                    
                                    # Redirect stdout to capture print statements
                                    old_stdout = sys.stdout
                                    sys.stdout = mystdout = StringIO()
                                    
                                    # Execute the code
                                    exec(edited_code, globals(), locals_dict)
                                    
                                    # Get the captured output
                                    sys.stdout = old_stdout
                                    output = mystdout.getvalue()
                                    
                                    # Display results
                                    st.subheader("Code Execution Results")
                                    
                                    # Display any print outputs
                                    if output.strip():
                                        st.text("Print Output:")
                                        st.text(output)
                                    
                                    # Check for figures
                                    import matplotlib.pyplot as plt
                                    if plt.get_fignums():
                                        st.text("Figures:")
                                        for i in plt.get_fignums():
                                            fig = plt.figure(i)
                                            st.pyplot(fig)
                                    
                                    # Check for dataframes in local variables
                                    for var_name, var_value in locals_dict.items():
                                        if isinstance(var_value, pd.DataFrame) and var_name != "df":
                                            st.text(f"DataFrame: {var_name}")
                                            st.dataframe(var_value.head())
                                    
                                except Exception as e:
                                    st.error(f"Error executing code: {str(e)}")
                        
                    except Exception as e:
                        st.error(f"Error generating code: {str(e)}")
                        st.info("You can try a different task or provide more details about your analysis goal.")

# For testing the module independently
if __name__ == "__main__":
    # Set API key (for testing)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Display the interface
    display_data_analysis_tools()
