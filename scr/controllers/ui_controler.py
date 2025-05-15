class UIController:
    def __init__(self, poll_service, user_service, nft_service, chatbot_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service

    def votar_ui(self, poll_id, username, opciones):
        return self.poll_service.vote(poll_id, username, opciones)

    def obtener_encuestas_activas(self):
        return self.poll_service.encuestas_activas()

    def obtener_tokens_usuario(self, username):
        return self.nft_service.obtener_tokens_usuario(username)

    def chatbot_response(self, username, mensaje):
        return self.chatbot_service.responder(username, mensaje)
