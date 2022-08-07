import requests

class DiscordWebhooks:
    @staticmethod
    def generate_data(title: str, desc: str, foot: str, thumb: str):
        return {
            "embeds": [
                {
                    "title": title,
                    "description": desc,
                    "footer": {"text": foot},
                    "thumbnail": {
                        "url": thumb
                    },
                    "color": 16711758
                }
            ]
        }
    
    @staticmethod
    def send(url: str, title: str="d", description: str="d", footer: str="e", thumbnail="", files=None):
        requests.post(url, json=DiscordWebhooks.generate_data(title=title, desc=description, foot=footer, thumb=thumbnail))
        if files is not None:
            requests.post(url, files=files)
