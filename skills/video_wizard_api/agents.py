
import json
import logging
import g4f
import asyncio
from typing import List, Dict

class StyleIdeationAgent:
    def __init__(self):
        self.model = "openai" # g4f alias
        self.provider = g4f.Provider.PollinationsAI # or others, but Pollinations is usually fast for text too

    async def brainstorm_concepts(self, niche: str, theme: str) -> List[Dict]:
        """
        Agent 1: Creative Director.
        Generates visual concepts based on niche and theme.
        """
        system_prompt = (
            f"You are a world-class Creative Director for video production. "
            f"Client Profile: Niche='{niche}', Theme='{theme}'. "
            "Task: Create 3 distinct, high-quality visual style concepts for their video marketing. "
            "Output strictly valid JSON list of objects with keys: 'concept_id', 'visual_prompt' (detailed, for AI image gen), 'rationale'."
        )
        
        try:
            response = await g4f.ChatCompletion.create_async(
                model=self.model,
                provider=self.provider,
                messages=[{"role": "user", "content": system_prompt}],
            )
            
            text = str(response)
            # Attempt to clean JSON if wrapped in markdown
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            data = json.loads(text)
            return data
        except Exception as e:
            logging.error(f"Ideation Agent failed: {e}")
            # Fallback to smart defaults if LLM fails
            return [
                {
                    "concept_id": "minimalist",
                    "visual_prompt": f"minimalist clean design for {niche}, {theme} colors, high key lighting, white background, professional photography, 8k",
                    "rationale": "Clean and professional look."
                },
                {
                    "concept_id": "energetic",
                    "visual_prompt": f"dynamic action shot for {niche}, {theme} aesthetic, motion blur, vibrant colors, dramatic lighting, cinematic",
                    "rationale": "High energy to grab attention."
                },
                {
                    "concept_id": "lifestyle",
                    "visual_prompt": f"lifestyle photography of people using {niche} products, warm lighting, natural bokeh, authentic emotion, {theme} vibe",
                    "rationale": "Connects emotionally with customers."
                }
            ]

class StyleCuratorAgent:
    def __init__(self):
        self.model = "openai"
        self.provider = g4f.Provider.PollinationsAI

    async def describe_result(self, visual_prompt: str) -> Dict:
        """
        Agent 2: Curator/Analyst.
        Generates Title and Description based on the specific visual prompt used.
        Simulates 'seeing' the result by knowing exactly what was asked for.
        """
        system_prompt = (
            f"You are a curator analyzing a generated image. "
            f"The image was generated with this prompt: '{visual_prompt}'. "
            "Task: Write a short, catchy Title (max 3 words) and a Description (max 1 sentence) that accurately describes this visual style. "
            "The description MUST match the visual elements mentioned in the prompt (lighting, colors, mood). "
            "Output strictly valid JSON object with keys: 'title', 'description'."
        )

        try:
            response = await g4f.ChatCompletion.create_async(
                model=self.model,
                provider=self.provider,
                messages=[{"role": "user", "content": system_prompt}],
            )
            
            text = str(response)
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            data = json.loads(text)
            return data
        except Exception as e:
            logging.error(f"Curator Agent failed: {e}")
            # Fallback based on simple keyword extraction
            return {
                "title": "Style Concept",
                "description": f"A visual style based on {visual_prompt[:20]}..."
            }

# Orchestrator
async def run_style_agent_pipeline(niche: str, theme: str):
    ideator = StyleIdeationAgent()
    curator = StyleCuratorAgent()
    
    # 1. Ideation
    concepts = await ideator.brainstorm_concepts(niche, theme)
    
    results = []
    for concept in concepts:
        # 2. Refine (Simulated Analysis)
        # We generate the description based on the prompt to ensure alignment
        curation = await curator.describe_result(concept['visual_prompt'])
        
        # 3. Construct Result
        results.append({
            "style_name": curation.get('title', 'Unknown Style'),
            "description": curation.get('description', concept.get('rationale')),
            "prompt": concept['visual_prompt'],
            "source": "AI Agent"
        })
        
    return results
