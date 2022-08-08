import requests

class DiscordWebhooks:
    @staticmethod
    def send(url: str, title: str="d", description: str="d", footer: str="e", thumbnail="", files=None):
        # // Send Embed
        requests.post(url, json={
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "footer": {"text": footer},
                    "thumbnail": {
                        "url": thumbnail
                    },
                    "color": 16711758
                }
            ]
        })
        # // Send files
        if files is not None:
            requests.post(url, files=files)
