import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import time
from datetime import datetime

def display_citation_management():
    """Display and manage citation management tools"""
    st.header("📚 Citation Management")
    
    # Create tabs for different citation management features
    citation_tabs = st.tabs([
        "Citation Generator",
        "Bibliography Manager",
        "Reference Library",
        "Import/Export"
    ])
    
    # Tab 1: Citation Generator
    with citation_tabs[0]:
        st.subheader("Generate Citations")
        
        # Source type selection
        source_type = st.selectbox(
            "Select Source Type",
            ["Journal Article", "Book", "Book Chapter", "Conference Paper", 
             "Website", "Thesis/Dissertation", "Report", "Newspaper Article"]
        )
        
        # Citation style selection
        citation_style = st.selectbox(
            "Select Citation Style",
            ["APA 7th Edition", "MLA 9th Edition", "Chicago 17th Edition", 
             "Harvard", "IEEE", "Vancouver", "AMA"]
        )
        
        # Display appropriate input fields based on source type
        if source_type == "Journal Article":
            col1, col2 = st.columns(2)
            with col1:
                authors = st.text_input("Authors (separate by comma)")
                title = st.text_input("Article Title")
                journal = st.text_input("Journal Name")
                
            with col2:
                year = st.text_input("Publication Year")
                volume = st.text_input("Volume")
                issue = st.text_input("Issue")
                pages = st.text_input("Pages (e.g., 123-145)")
                doi = st.text_input("DOI (optional)")
        
        elif source_type == "Book":
            col1, col2 = st.columns(2)
            with col1:
                authors = st.text_input("Authors/Editors (separate by comma)")
                title = st.text_input("Book Title")
                
            with col2:
                year = st.text_input("Publication Year")
                publisher = st.text_input("Publisher")
                place = st.text_input("Place of Publication")
                edition = st.text_input("Edition (optional)")
                
        elif source_type == "Website":
            col1, col2 = st.columns(2)
            with col1:
                authors = st.text_input("Authors/Organization (if known)")
                title = st.text_input("Page Title")
                website = st.text_input("Website Name")
                
            with col2:
                year = st.text_input("Year Published/Updated")
                url = st.text_input("URL")
                accessed = st.date_input("Date Accessed")
        
        # Generate citation button
        if st.button("Generate Citation"):
            with st.spinner("Generating citation..."):
                # This is a simplified demonstration
                if source_type == "Journal Article":
                    if citation_style == "APA 7th Edition":
                        citation = f"{authors} ({year}). {title}. <i>{journal}, {volume}({issue})</i>, {pages}."
                    elif citation_style == "MLA 9th Edition":
                        citation = f"{authors}. \"{title}.\" <i>{journal}</i>, vol. {volume}, no. {issue}, {year}, pp. {pages}."
                    else:
                        citation = f"{authors}. {title}. {journal}. {year};{volume}({issue}):{pages}."
                
                elif source_type == "Book":
                    if citation_style == "APA 7th Edition":
                        citation = f"{authors} ({year}). <i>{title}</i>{' (' + edition + ' ed.)' if edition else ''}. {publisher}."
                    elif citation_style == "MLA 9th Edition":
                        citation = f"{authors}. <i>{title}</i>{', ' + edition + ' ed.' if edition else ''}. {publisher}, {year}."
                    else:
                        citation = f"{authors}. <i>{title}</i>. {place}: {publisher}; {year}."
                
                elif source_type == "Website":
                    if citation_style == "APA 7th Edition":
                        citation = f"{authors} ({year}). {title}. <i>{website}</i>. {url}"
                    elif citation_style == "MLA 9th Edition":
                        citation = f"{authors}. \"{title}.\" <i>{website}</i>, {year}, {url}. Accessed {accessed.strftime('%d %b. %Y')}."
                    else:
                        citation = f"{authors}. {title} [Internet]. {website}; {year} [cited {accessed.strftime('%Y %b %d')}]. Available from: {url}"
                
                st.markdown("<div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px;'>" + citation + "</div>", unsafe_allow_html=True)
                
                # Buttons to copy or save the citation
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Copy to Clipboard"):
                        st.success("Citation copied to clipboard!")
                with col2:
                    if st.button("Add to Bibliography"):
                        st.success("Citation added to your bibliography!")
    
    # Tab 2: Bibliography Manager
    with citation_tabs[1]:
        st.subheader("Manage Your Bibliography")
        
        # Sample bibliography for demonstration
        if "bibliography" not in st.session_state:
            st.session_state.bibliography = [
                {
                    "id": "smith2020",
                    "type": "Journal Article",
                    "authors": "Smith, J., & Johnson, B.",
                    "year": "2020",
                    "title": "Advances in Educational Technology",
                    "journal": "Journal of Educational Research",
                    "volume": "45",
                    "issue": "3",
                    "pages": "123-145",
                    "doi": "10.1234/jer.2020.123",
                    "tags": ["education", "technology"]
                },
                {
                    "id": "brown2019",
                    "type": "Book",
                    "authors": "Brown, M.",
                    "year": "2019",
                    "title": "Research Methods in Education",
                    "publisher": "Academic Press",
                    "place": "New York",
                    "edition": "3rd",
                    "tags": ["research", "methods", "education"]
                }
            ]
        
        # Filter bibliography
        filter_tags = st.multiselect(
            "Filter by Tags",
            list(set([tag for item in st.session_state.bibliography for tag in item.get("tags", [])]))
        )
        
        # Apply filters
        filtered_bibliography = st.session_state.bibliography
        if filter_tags:
            filtered_bibliography = [
                item for item in filtered_bibliography 
                if any(tag in item.get("tags", []) for tag in filter_tags)
            ]
        
        # Display bibliography
        for i, item in enumerate(filtered_bibliography):
            with st.expander(f"{item['authors']} ({item['year']}) - {item['title']}"):
                # Display all fields
                for key, value in item.items():
                    if key != "id" and key != "tags":
                        st.write(f"**{key.capitalize()}:** {value}")
                
                # Tags
                if "tags" in item:
                    st.write("**Tags:** " + ", ".join(item["tags"]))
                
                # Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Edit", key=f"edit_{i}"):
                        st.session_state.editing_reference = i
                
                with col2:
                    if st.button("Delete", key=f"delete_{i}"):
                        st.session_state.bibliography.remove(item)
                        st.rerun()
                
                with col3:
                    citation_style = st.selectbox(
                        "Citation Style", 
                        ["APA", "MLA", "Chicago"],
                        key=f"style_{i}"
                    )
                    
                    if st.button("Generate Citation", key=f"cite_{i}"):
                        # Generate citation based on style and reference type
                        if item["type"] == "Journal Article":
                            if citation_style == "APA":
                                citation = f"{item['authors']} ({item['year']}). {item['title']}. <i>{item['journal']}, {item['volume']}({item['issue']})</i>, {item['pages']}."
                            elif citation_style == "MLA":
                                citation = f"{item['authors']}. \"{item['title']}.\" <i>{item['journal']}</i>, vol. {item['volume']}, no. {item['issue']}, {item['year']}, pp. {item['pages']}."
                            else:
                                citation = f"{item['authors']}. {item['title']}. {item['journal']}. {item['year']};{item['volume']}({item['issue']}):{item['pages']}."
                        
                        elif item["type"] == "Book":
                            if citation_style == "APA":
                                citation = f"{item['authors']} ({item['year']}). <i>{item['title']}</i>{' (' + item.get('edition', '') + ' ed.)' if 'edition' in item else ''}. {item['publisher']}."
                            elif citation_style == "MLA":
                                citation = f"{item['authors']}. <i>{item['title']}</i>{', ' + item.get('edition', '') + ' ed.' if 'edition' in item else ''}. {item['publisher']}, {item['year']}."
                            else:
                                citation = f"{item['authors']}. <i>{item['title']}</i>. {item.get('place', '')}: {item['publisher']}; {item['year']}."
                        
                        st.markdown("<div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px;'>" + citation + "</div>", unsafe_allow_html=True)
        
        # Add new reference
        st.subheader("Add New Reference")
        
        reference_type = st.selectbox(
            "Reference Type",
            ["Journal Article", "Book", "Book Chapter", "Conference Paper", 
             "Website", "Thesis/Dissertation", "Report", "Newspaper Article"]
        )
        
        # ID and tags for all types
        reference_id = st.text_input("Reference ID (e.g., smith2020)")
        reference_tags = st.text_input("Tags (comma separated)")
        
        # Display fields based on reference type
        if reference_type == "Journal Article":
            col1, col2 = st.columns(2)
            with col1:
                authors = st.text_input("Authors (separate by comma)", key="new_authors")
                title = st.text_input("Article Title", key="new_title")
                journal = st.text_input("Journal Name", key="new_journal")
                
            with col2:
                year = st.text_input("Publication Year", key="new_year")
                volume = st.text_input("Volume", key="new_volume")
                issue = st.text_input("Issue", key="new_issue")
                pages = st.text_input("Pages", key="new_pages")
                doi = st.text_input("DOI (optional)", key="new_doi")
            
            if st.button("Add Reference"):
                if reference_id and authors and title and journal and year:
                    new_reference = {
                        "id": reference_id,
                        "type": reference_type,
                        "authors": authors,
                        "year": year,
                        "title": title,
                        "journal": journal,
                        "volume": volume,
                        "issue": issue,
                        "pages": pages,
                        "doi": doi,
                        "tags": [tag.strip() for tag in reference_tags.split(",")] if reference_tags else []
                    }
                    
                    st.session_state.bibliography.append(new_reference)
                    st.success("Reference added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
        
        # Export bibliography options
        st.subheader("Export Bibliography")
        export_format = st.selectbox(
            "Export Format",
            ["BibTeX", "RIS", "CSV", "EndNote XML", "Plain Text"]
        )
        
        export_style = st.selectbox(
            "Citation Style",
            ["APA 7th Edition", "MLA 9th Edition", "Chicago 17th Edition", 
             "Harvard", "IEEE", "Vancouver", "AMA"]
        )
        
        if st.button("Export Bibliography"):
            # In a real implementation, this would generate the actual file
            # For demonstration, we'll show a preview
            if export_format == "BibTeX":
                export_text = "@article{smith2020,\n  author = {Smith, J. and Johnson, B.},\n  title = {Advances in Educational Technology},\n  journal = {Journal of Educational Research},\n  year = {2020},\n  volume = {45},\n  number = {3},\n  pages = {123--145}\n}\n\n@book{brown2019,\n  author = {Brown, M.},\n  title = {Research Methods in Education},\n  publisher = {Academic Press},\n  year = {2019},\n  edition = {3},\n  address = {New York}\n}"
            elif export_format == "CSV":
                export_text = "ID,Type,Authors,Year,Title,Journal,Volume,Issue,Pages,DOI\nsmith2020,Journal Article,\"Smith, J., & Johnson, B.\",2020,Advances in Educational Technology,Journal of Educational Research,45,3,123-145,10.1234/jer.2020.123\nbrown2019,Book,\"Brown, M.\",2019,Research Methods in Education,Academic Press,,,,"
            else:
                export_text = "Bibliography in " + export_format + " format..."
            
            st.text_area("Preview", export_text, height=200)
            st.download_button(
                label="Download Bibliography",
                data=export_text,
                file_name=f"bibliography.{export_format.lower()}",
                mime="text/plain"
            )
    
    # Tab 3: Reference Library
    with citation_tabs[2]:
        st.subheader("Reference Library")
        
        # Sample library for demonstration
        if "reference_library" not in st.session_state:
            st.session_state.reference_library = [
                {
                    "id": "smith2020paper",
                    "title": "Advances in Educational Technology",
                    "authors": "Smith, J., & Johnson, B.",
                    "year": "2020",
                    "file": "sample_paper.pdf",
                    "tags": ["education", "technology", "research"],
                    "notes": "Excellent literature review section. Key points on pages 5-7."
                },
                {
                    "id": "brown2019book",
                    "title": "Research Methods in Education",
                    "authors": "Brown, M.",
                    "year": "2019",
                    "file": "research_methods.pdf",
                    "tags": ["research", "methods", "education"],
                    "notes": "Good reference for experimental design (Chapter 4)."
                }
            ]
        
        # Search and filter options
        st.markdown("### Search Your Library")
        search_query = st.text_input("Search")
        
        # Tags filter
        all_tags = sorted(list(set([tag for item in st.session_state.reference_library for tag in item.get("tags", [])])))
        filter_tags = st.multiselect("Filter by Tags", all_tags)
        
        # Apply search and filters
        filtered_library = st.session_state.reference_library
        if search_query:
            filtered_library = [
                item for item in filtered_library 
                if search_query.lower() in item["title"].lower() or 
                   search_query.lower() in item["authors"].lower() or
                   search_query.lower() in item.get("notes", "").lower()
            ]
        
        if filter_tags:
            filtered_library = [
                item for item in filtered_library 
                if any(tag in item.get("tags", []) for tag in filter_tags)
            ]
        
        # Display library items
        for i, item in enumerate(filtered_library):
            with st.expander(f"{item['title']} ({item['year']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Authors:** {item['authors']}")
                    st.write(f"**Year:** {item['year']}")
                    st.write(f"**File:** {item['file']}")
                    st.write(f"**Tags:** {', '.join(item.get('tags', []))}")
                    
                    if "notes" in item and item["notes"]:
                        st.write("**Notes:**")
                        st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 5px;'>{item['notes']}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.button("📄 View", key=f"view_{i}")
                    st.button("📝 Edit", key=f"edit_ref_{i}")
                    st.button("🗑️ Delete", key=f"delete_ref_{i}")
                    st.button("📎 Cite", key=f"cite_ref_{i}")
        
        # Upload new reference
        st.subheader("Add to Library")
        
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        
        if uploaded_file is not None:
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            
            # Extract metadata if possible
            st.info("Extracting metadata from PDF...")
            
            # For demonstration, we'll use placeholder data
            extracted_title = "Extracted Title: " + uploaded_file.name.replace(".pdf", "")
            extracted_authors = "John Smith, Jane Doe"
            extracted_year = "2023"
            
            st.write(f"Extracted Title: {extracted_title}")
            st.write(f"Extracted Authors: {extracted_authors}")
            st.write(f"Extracted Year: {extracted_year}")
            
            # Form for additional metadata
            st.subheader("Edit Metadata")
            
            ref_title = st.text_input("Title", value=extracted_title)
            ref_authors = st.text_input("Authors", value=extracted_authors)
            ref_year = st.text_input("Year", value=extracted_year)
            ref_tags = st.text_input("Tags (comma separated)")
            ref_notes = st.text_area("Notes")
            
            if st.button("Add to Library"):
                # In a real implementation, this would save the PDF and metadata
                new_ref = {
                    "id": ref_title.lower().replace(" ", "_") + ref_year,
                    "title": ref_title,
                    "authors": ref_authors,
                    "year": ref_year,
                    "file": uploaded_file.name,
                    "tags": [tag.strip() for tag in ref_tags.split(",")] if ref_tags else [],
                    "notes": ref_notes
                }
                
                st.session_state.reference_library.append(new_ref)
                st.success("Reference added to library!")
                st.rerun()
    
    # Tab 4: Import/Export
    with citation_tabs[3]:
        st.subheader("Import & Export Citations")
        
        # Import options
        st.markdown("### Import Citations")
        
        import_format = st.selectbox(
            "Import Format",
            ["BibTeX", "RIS", "EndNote XML", "CSV", "Zotero", "Mendeley"]
        )
        
        import_file = st.file_uploader(f"Upload {import_format} File", type=["bib", "ris", "xml", "csv"])
        
        if import_file is not None:
            st.success(f"File '{import_file.name}' uploaded successfully!")
            
            if st.button("Import Citations"):
                # In a real implementation, this would parse and import the citations
                st.info(f"Importing citations from {import_file.name}...")
                time.sleep(1)  # Simulate processing
                st.success("Citations imported successfully!")
        
        # Export options
        st.markdown("### Export Citations")
        
        export_format = st.selectbox(
            "Export Format",
            ["BibTeX", "RIS", "EndNote XML", "CSV", "Zotero", "Mendeley"]
        )
        
        export_style = st.selectbox(
            "Citation Style",
            ["APA 7th Edition", "MLA 9th Edition", "Chicago 17th Edition", 
             "Harvard", "IEEE", "Vancouver", "AMA"],
            key="export_style"
        )
        
        if st.button("Export All Citations"):
            # In a real implementation, this would generate the file in the selected format
            st.info(f"Exporting citations in {export_format} format...")
            time.sleep(1)  # Simulate processing
            
            # Create some example content
            if export_format == "BibTeX":
                export_data = "@article{smith2020,\n  author = {Smith, J. and Johnson, B.},\n  title = {Advances in Educational Technology},\n  journal = {Journal of Educational Research},\n  year = {2020},\n  volume = {45},\n  number = {3},\n  pages = {123--145}\n}\n\n@book{brown2019,\n  author = {Brown, M.},\n  title = {Research Methods in Education},\n  publisher = {Academic Press},\n  year = {2019},\n  edition = {3},\n  address = {New York}\n}"
                file_extension = "bib"
            elif export_format == "CSV":
                export_data = "ID,Type,Authors,Year,Title,Journal,Volume,Issue,Pages,DOI\nsmith2020,Journal Article,\"Smith, J., & Johnson, B.\",2020,Advances in Educational Technology,Journal of Educational Research,45,3,123-145,10.1234/jer.2020.123\nbrown2019,Book,\"Brown, M.\",2019,Research Methods in Education,Academic Press,,,,"
                file_extension = "csv"
            else:
                export_data = f"Sample {export_format} export data"
                file_extension = "txt"
            
            st.download_button(
                label=f"Download {export_format} File",
                data=export_data,
                file_name=f"citations.{file_extension}",
                mime="text/plain"
            )
        
        # Integration options
        st.markdown("### Integrate with Reference Managers")
        
        integration_options = ["Zotero", "Mendeley", "EndNote", "RefWorks", "Citavi"]
        selected_integration = st.selectbox("Select Reference Manager", integration_options)
        
        if st.button(f"Connect to {selected_integration}"):
            # In a real implementation, this would connect to the selected reference manager
            st.info(f"Connecting to {selected_integration}...")
            time.sleep(1)  # Simulate connection
            st.success(f"Connected to {selected_integration}!")
            
            # Display placeholder for sync options
            st.write(f"### {selected_integration} Sync Options")
            st.checkbox("Two-way sync")
            st.checkbox("Import only")
            st.checkbox("Export only")
            
            if st.button("Sync Now"):
                st.info("Synchronizing citations...")
                sync_progress = st.progress(0)
                for i in range(101):
                    time.sleep(0.01)  # Simulate sync process
                    sync_progress.progress(i)
                st.success("Synchronization complete!")
