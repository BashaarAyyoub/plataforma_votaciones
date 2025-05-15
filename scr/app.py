import argparse
from src.controllers.cli_controller import CLIController
from src.controllers.ui_controller import UIController
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService
from src.ui.gradio_app import lanzar_ui
from src.config import cargar_config

def main():
    config = cargar_config()
    poll_service = PollService()
    user_service = UserService()
    nft_service = NFTService()
    chatbot_service = ChatbotService(poll_service)

    parser = argparse.ArgumentParser()
    parser.add_argument("--ui", action="store_true", help="Lanzar interfaz Gradio")
    args = parser.parse_args()

    if args.ui:
        ui_controller = UIController(poll_service, user_service, nft_service, chatbot_service)
        app = lanzar_ui(ui_controller)
        app.launch(server_port=config.get("puerto", 7860))
    else:
        controller = CLIController(poll_service, user_service, nft_service)
        print("💻 Modo CLI. Escribe comandos ('exit' para salir).")
        while True:
            cmd = input(">>> ")
            if cmd.strip() in ("exit", "salir"):
                break
            controller.ejecutar_comando(cmd)

if __name__ == "__main__":
    main()
