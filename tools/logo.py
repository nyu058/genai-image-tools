from tools.base import AiTool
import shutil
import os
from functools import lru_cache

from openai import OpenAI

class LogoAiTool(AiTool):

    prompt_template = "A {logo_style} logo of {subject} with a white background. {add_req}"
    model = "dall-e-3"
    
    def generate_image(self, **kwargs):
        prompt = self.prompt_template.format(**kwargs)
        client = OpenAI(api_key=self.openai_api_key)
        image_response = client.images.generate(
            model=self.model,
            prompt=prompt,
            quality="standard",
            n=1
        )
        
        return image_response.data[0].url
    
