import time
from wikilink import WikiConnector
from semantic_scorer import SemanticScore

def start_smart_search(start_page, target_page):
    # 1. Initialize tools
    print("Initializing systems...")
    connector = WikiConnector()
    scorer = SemanticScore()
    
    # 2. Setup game variables
    path = [start_page]
    visited = set()
    visited.add(start_page.lower()) 
    
    current_page = start_page
    print(f"\nMission: Go from '{start_page}' to '{target_page}'\n")

    # 3. The Search Loop (Max 20 steps)
    for step in range(1, 21):
        print(f"Step {step}: On page '{current_page}'")
        
        # CHECK: Did we win?
        if current_page.lower() == target_page.lower():
            print(f"\nTarget reached in {step} steps.")
            print(f"Path: {' -> '.join(path)}")
            return path

        # A. Fetch links 
        links = connector.get_links(current_page)
        
        if not links:
            print("Dead end. No links found on this page.")
            break
            
        # Filter: Remove visited pages and generic numeric links
        candidates = []
        for link in links:
            if link.lower() not in visited and not link.isdigit():
                candidates.append(link)
        
        if not candidates:
            print("Dead end. All links on this page have been visited.")
            break

        # B. AI Brain: Sort links 
        print(f"Analyzing {len(candidates)} links...", end=" ")
        ranked_links = scorer.sorting_links(candidates, target_page)
        print("Done.")

        # C. Choose the best link
        best_link, score = ranked_links[0]
        
        print(f"Selected: '{best_link}' (Score: {score:.4f})")
        print("-" * 40)

        # D. Move to next page
        current_page = best_link
        visited.add(current_page.lower())
        path.append(current_page)
        
        # Optional: Sleep to be polite to Wikipedia
        time.sleep(1)

    print("\nMax steps reached or dead end.")
    return path

if __name__ == "__main__":
    start = "Elon Musk"
    target = "Mars"
    
    start_smart_search(start, target)