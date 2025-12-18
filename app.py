import streamlit as st
import time
from wikilink import WikiConnector
from semantic_scorer import SemanticScore

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="WikiLink AI Pathfinder")

st.title("WikiLink AI Pathfinder")
st.markdown("Enter two Wikipedia pages, and watch the AI find the path between them using Semantic Search.")

# 2. LOAD RESOURCES (Cached so it doesn't reload the AI model every time)
@st.cache_resource
def load_tools():
    return WikiConnector(), SemanticScore()

with st.spinner("Loading AI Model..."):
    connector, scorer = load_tools()

# 3. SIDEBAR INPUTS
with st.sidebar:
    st.header("Settings")
    start_page = st.text_input("Start Page", value="Elon Musk")
    target_page = st.text_input("Target Page", value="Mars")
    max_steps = st.slider("Max Steps", min_value=5, max_value=50, value=20)
    start_btn = st.button("Start Search", type="primary")

# 4. MAIN LOGIC
if start_btn:
    if not start_page or not target_page:
        st.error("Please enter both a start and target page.")
    else:
        # Initialize Variables
        path = [start_page]
        visited = {start_page.lower()}
        current_page = start_page
        
        # Create a container for the live updates
        status_container = st.status(f"Searching path from {start_page} to {target_page}...", expanded=True)
        
        found = False
        
        # THE SEARCH LOOP
        for step in range(1, max_steps + 1):
            status_container.write(f"Step {step}: On page '{current_page}'")
            
            # Check Victory
            if current_page.lower() == target_page.lower():
                found = True
                status_container.update(label="Target Found!", state="complete", expanded=False)
                break
            
            # Fetch Links
            links = connector.get_links(current_page)
            if not links:
                status_container.write("Dead end. No links found.")
                status_container.update(state="error")
                break
            
            # Filter Links
            candidates = [l for l in links if l.lower() not in visited and not l.isdigit()]
            
            if not candidates:
                status_container.write("Dead end. All links visited.")
                status_container.update(state="error")
                break
                
            # AI Analysis
            status_container.write(f"AI analyzing {len(candidates)} links...")
            ranked_links = scorer.sorting_links(candidates, target_page)
            
            # Choose Best
            best_link, score = ranked_links[0]
            status_container.write(f"Selected: '{best_link}' (Score: {score:.4f})")
            
            # Move
            current_page = best_link
            visited.add(current_page.lower())
            path.append(current_page)
            time.sleep(0.5) 

        # 5. FINAL RESULTS
        if found:
            st.success(f"VICTORY! Path found in {len(path)-1} steps.")
            
            st.markdown("### The Path:")
            path_str = " -> ".join([f"**{p}**" for p in path])
            st.info(path_str)
        else:
            st.warning("Max steps reached or path not found.")
            st.write("Path taken so far:", path)