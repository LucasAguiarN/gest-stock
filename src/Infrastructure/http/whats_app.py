from twilio.rest import Client
import os

class WhatsAppService:

    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")

        if not self.account_sid or not self.auth_token:
            raise ValueError("Credenciais do Twilio não encontradas")

        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to, message):
        try:
            message = self.client.messages.create(
                body=message,
                from_='whatsapp:+14155238886',  # número sandbox Twilio
                to=f'whatsapp:{to}'
            )
            print("Mensagem enviada! SID:", message.sid)
        except Exception as e:
            print("Erro ao enviar WhatsApp:", e)