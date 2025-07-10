
import gradio as gr
from backend_gpt import generate_response

def handle_input(user_input):
    return generate_response(user_input)

iface = gr.Interface(fn=handle_input, inputs="text", outputs="text")
iface.launch()
