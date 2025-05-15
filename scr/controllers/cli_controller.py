import shlex
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService

class CLIController:
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.usuario_actual = None

    def ejecutar_comando(self, linea: str):
        try:
            partes = shlex.split(linea)
            comando = partes[0]

            if comando == "registro":
                self.usuario_actual = self.user_service.register(partes[1], partes[2])
                print("✅ Registro exitoso")

            elif comando == "login":
                self.usuario_actual = self.user_service.login(partes[1], partes[2])
                print("🔐 Login exitoso")

            elif comando == "crear_encuesta":
                pregunta = partes[1]
                opciones = partes[2].split(",")
                duracion = int(partes[3])
                tipo = partes[4]
                poll_id = self.poll_service.create_poll(pregunta, opciones, duracion, tipo)
                print(f"📊 Encuesta creada con ID: {poll_id}")

            elif comando == "listar_encuestas":
                for poll in self.poll_service.listar_encuestas():
                    estado = "✅ Activa" if poll.esta_activa() else "❌ Cerrada"
                    print(f"- {poll.id}: {poll.pregunta} ({estado})")

            elif comando == "votar":
                poll_id = partes[1]
                opciones = partes[2].split(",")
                self.poll_service.vote(poll_id, self.usuario_actual.username, opciones)
                print("🗳️ Voto registrado")

            elif comando == "cerrar_encuesta":
                poll_id = partes[1]
                self.poll_service.close_poll(poll_id)
                print("🔒 Encuesta cerrada")

            elif comando == "ver_resultados":
                poll_id = partes[1]
                resultados = self.poll_service.get_final_results(poll_id)
                print("📈 Resultados:")
                for op, count in resultados.items():
                    print(f"  - {op}: {count} votos")

            elif comando == "mis_tokens":
                tokens = self.nft_service.obtener_tokens_usuario(self.usuario_actual.username)
                for t in tokens:
                    print(f"🪙 {t.token_id} - {t.option} en {t.poll_id} (emitido {t.issued_at})")

            elif comando == "transferir_token":
                token_id = partes[1]
                nuevo_owner = partes[2]
                self.nft_service.transferir_token(token_id, self.usuario_actual.username, nuevo_owner)
                print("🔁 Token transferido")

            else:
                print("❓ Comando no reconocido")

        except Exception as e:
            print(f"⚠️ Error: {str(e)}")
