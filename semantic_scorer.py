from sentence_transformers import SentenceTransformer, util
import torch

class SemanticScore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"device: {self.device}")

    def sorting_links(self, links, target):
        target_embed=self.model.encode(target, convert_to_tensor=True,device=self.device)
        link_embedd=self.model.encode(links,convert_to_tensor=True,device=self.device)
        scores=util.cos_sim(target_embed,link_embedd)
        scored_links = []
        for i in range(len(links)):
            score = scores[i].item() # .item() automatically moves single value to CPU
            scored_links.append((links[i], score))
            
        scored_links.sort(key=lambda x: x[1], reverse=True)
        return scored_links
    
