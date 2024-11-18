from tools.base import ImageAi

class StandardImageAiTool(ImageAi):
    prompt_template = "{prompt}"
    model = "dall-e-3"
    