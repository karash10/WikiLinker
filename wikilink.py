import requests 

class WikiConnector:
    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php" #setting the api endpoint for the wikipedia
        self.session = requests.Session() #creates a session for making requests with the api 
        self.session.headers.update({
            "User-Agent": "SmartWikiConnector/1.0 (contact: yourname@example.com)" 
        })
        
    def get_links(self, title):
        link=[]
        
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "links",      # Get links on the page
            "pllimit": "max",     # Max 500 per request
            "plnamespace": 0,     # Only fetch Articles (ignore Talk pages)
            "redirects": 1        # Auto-resolves the case of the word 
        }
        
        while True:
            response = self.session.get(url=self.url, params=params)
            data=response.json()
            pages = data.get("query", {}).get("pages", {})
            page_id = next(iter(pages))
            
            if "links" in pages[page_id]:
                batch = [link['title'] for link in pages[page_id]['links']]
                link.extend(batch)
                print(".", end="", flush=True)
                
            if 'continue' in data:
                    # Update params with the token for the next batch
                    params.update(data['continue'])
            else:
                break
            
        return link
        
if __name__ == "__main__":
    connector = WikiConnector()
    title = "Artificial intelligence"
    links = connector.get_links(title)
    print(f"\nLinks found on the page '{title}':")
    if links:
        print(links[:10])