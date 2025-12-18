from sentence_transformers import SentenceTransformer, util
import torch

class SemanticScore:
    def __init__(self):
        # Detect GPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f" Model on: {self.device.upper()}...")
        
        # Load the model (The "Old Way")
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)

    def sorting_links(self, links, target):
        if not links:
            return []

        # 1. Encode Target and Links
        target_embed = self.model.encode(target, convert_to_tensor=True, device=self.device)
        link_embedd = self.model.encode(links, convert_to_tensor=True, device=self.device)
        
        # 2. Calculate Similarity
        scores = util.cos_sim(target_embed, link_embedd)

        scored_links = []
        
        # 3. Extract scores
        for i in range(len(links)):
            score = scores[0][i].item() 
            scored_links.append((links[i], score))
            
        # 4. Sort
        scored_links.sort(key=lambda x: x[1], reverse=True)
        return scored_links

