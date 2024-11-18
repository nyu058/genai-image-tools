from tools.base import ImageAi

class LogoAiTool(ImageAi):

    prompt_template = "A {logo_style} logo of {subject} with a white background. The theme color should be {theme_color}. {add_req}"
    model = "dall-e-3"
