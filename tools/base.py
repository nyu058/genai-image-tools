import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class ImageAi:

    prompt_template = ""
    model = ""

    def __init__(self) -> None:
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    def generate_image(self, quality="standard", **kwargs):
        prompt = self.prompt_template.format(**kwargs)
        client = OpenAI(api_key=self.openai_api_key)
        image_response = client.images.generate(
            model=self.model,
            prompt=prompt,
            quality=quality,
            n=1
        )
        
        return image_response.data[0].url