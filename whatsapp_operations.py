from whatsapp_api_client_python import API



class WhatsAppAPI:
    def __init__(self, api_key=None, instance_id=None):
        self.instance_id = instance_id
        self.api_key = api_key
        self.initiated_api = API.GreenAPI(
            self.instance_id, self.api_key
        )


    def __repr__(self):
        return f"{__class__.__name__}({self.api_key}, {self.instance_id})"
    

    def send_message(self, message: str, destination: str):
        _ = self.initiated_api.sending.sendMessage(
            f"{destination}@c.us", f"{message}"
        )


    