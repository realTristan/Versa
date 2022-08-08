import requests

class DiscordWebhooks:
    @staticmethod
    def send(url: str, title: str="d", description: str="d", footer: str="e", thumbnail="", files=None):
        session: requests.Session = requests.Session()
        
        # // Send Embed
        session.post(url, json={
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
            session.post(url, files=files)
