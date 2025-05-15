import gradio as gr

def lanzar_ui(ui_controller):
    def votar_interface(poll_id, username, opciones):
        try:
            ui_controller.votar_ui(poll_id, username, opciones.split(","))
            return "✅ Voto registrado"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def mostrar_encuestas():
        encuestas = ui_controller.obtener_encuestas_activas()
        if not encuestas:
            return "No hay encuestas activas"
        res = ""
        for e in encuestas:
            res += f"{e.id}: {e.pregunta} -> {', '.join(e.opciones)}\n"
        return res

    def chatbot_fn(username, mensaje):
        return ui_controller.chatbot_response(username, mensaje)

    def ver_tokens(username):
        tokens = ui_controller.obtener_tokens_usuario(username)
        return "\n".join([f"{t.token_id} - {t.option} en {t.poll_id}" for t in tokens]) or "Sin tokens"

    with gr.Blocks() as demo:
        gr.Markdown("# 🎥 Encuestas Interactivas para Streamers")

        with gr.Tab("📊 Votar"):
            user = gr.Textbox(label="Usuario")
            poll_id = gr.Textbox(label="ID de Encuesta")
            opciones = gr.Textbox(label="Opciones (separadas por coma)")
            votar_btn = gr.Button("Votar")
            resultado = gr.Textbox(label="Resultado")
            encuestas = gr.Textbox(label="Encuestas Activas", interactive=False)
            mostrar_btn = gr.Button("Actualizar Encuestas")

            votar_btn.click(votar_interface, inputs=[poll_id, user, opciones], outputs=resultado)
            mostrar_btn.click(mostrar_encuestas, outputs=encuestas)

        with gr.Tab("🤖 Chatbot"):
            user_chat = gr.Textbox(label="Usuario")
            entrada = gr.Textbox(label="Mensaje")
            salida = gr.Textbox(label="Respuesta")
            enviar = gr.Button("Enviar")
            enviar.click(chatbot_fn, inputs=[user_chat, entrada], outputs=salida)

        with gr.Tab("🪙 Mis Tokens"):
            user_token = gr.Textbox(label="Usuario")
            tokens_output = gr.Textbox(label="Tokens", lines=10)
            ver_btn = gr.Button("Ver Tokens")
            ver_btn.click(ver_tokens, inputs=user_token, outputs=tokens_output)

    return demo
