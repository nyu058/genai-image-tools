from tools.base import AiTool

from openai import OpenAI

class ImageAiTool(AiTool):

    model = "dall-e-3"
    
    def generate_image(self, quality, prompt):
        client = OpenAI(api_key=self.openai_api_key)
        image_response = client.images.generate(
            model=self.model,
            prompt=prompt,
            quality=quality,
            n=1
        )
        
        return image_response.data[0].url
    
