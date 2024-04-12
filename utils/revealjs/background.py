class Background:
    def generate_html(self):
        raise NotImplementedError


class ColorBackground(Background):
    def __init__(self, color):
        self.color = color

    def generate_html(self):
        return f' data-background-color="{self.color}"'


class ImageBackground(Background):
    def __init__(self, image_url, size=None):
        self.image_url = image_url
        self.size = size

    def generate_html(self):
        size_str = f' data-background-size="{self.size}"' if self.size else ""
        return f' data-background="{self.image_url}"{size_str}'


class VideoBackground(Background):
    def __init__(self, video_url):
        self.video_url = video_url

    def generate_html(self):
        return f' data-background-video="{self.video_url}"'


class BackgroundFactory:
    @staticmethod
    def create_background(bg_type, value, **kwargs):
        if bg_type == "color":
            return ColorBackground(value)
        elif bg_type == "image":
            return ImageBackground(value, **kwargs)
        elif bg_type == "video":
            return VideoBackground(value)
        else:
            raise ValueError(f"Unsupported background type: {bg_type}")
