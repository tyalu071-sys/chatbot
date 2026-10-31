import tkinter as tk
from tkinter import scrolledtext
from ollama import chat
import threading

# AI conversation instructions
chat_history = [
    {
        "role": "system",
        "content": (
            "You are Yalini GPT, a friendly AI assistant. "
            "Give simple answers using easy English. "
            "Keep answers short, usually 5 to 6 lines. "
            "Use short sentences and clear explanations. "
            "Avoid unnecessary details and long lists. "
            "Do not use Markdown symbols like ** or ##. "
            "Explain technical topics in a beginner-friendly way."
        )
    }
]


# Send user message
def send_message(event=None):
    message = message_box.get().strip()

    if not message:
        return

    message_box.delete(0, tk.END)

    chat_display.config(state="normal")
    chat_display.insert(tk.END, "You: " + message + "\n\n")
    chat_display.config(state="disabled")
    chat_display.see(tk.END)

    if message.lower() == "bye":
        chat_display.config(state="normal")
        chat_display.insert(
            tk.END,
            "Yalini GPT: Goodbye! Have a nice day.\n\n"
        )
        chat_display.config(state="disabled")
        chat_display.see(tk.END)
        return

    chat_history.append({
        "role": "user",
        "content": message
    })

    send_button.config(state="disabled", text="Thinking...")

    threading.Thread(
        target=get_ai_response,
        daemon=True
    ).start()


# Get answer from local AI
def get_ai_response():
    try:
        response = chat(
            model="llama3.2:1b",
            messages=chat_history
        )

        answer = response.message.content.strip()

        chat_history.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as error:
        print("Error:", error)
        answer = (
            "Sorry, I couldn't connect to the AI. "
            "Please check whether Ollama is running."
        )

    root.after(0, display_response, answer)


# Display AI answer
def display_response(answer):
    chat_display.config(state="normal")

    chat_display.insert(
        tk.END,
        "Yalini GPT: " + answer + "\n\n"
    )

    chat_display.see(tk.END)
    chat_display.config(state="disabled")

    send_button.config(state="normal", text="Send")
    message_box.focus_set()


# Main application window
root = tk.Tk()
root.title("Yalini GPT")
root.geometry("650x600")
root.configure(bg="#EAF0FF")


# Title
title_label = tk.Label(
    root,
    text="Yalini GPT",
    font=("Arial", 22, "bold"),
    bg="#EAF0FF",
    fg="#3155C6"
)
title_label.pack(pady=(15, 5))


# Description
description_label = tk.Label(
    root,
    text="Your friendly AI assistant — ask me anything!",
    font=("Arial", 11),
    bg="#EAF0FF",
    fg="#333333"
)
description_label.pack(pady=(0, 12))


# Chat display
chat_display = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 11),
    bg="white",
    fg="#222222",
    state="disabled"
)
chat_display.pack(
    padx=15,
    pady=10,
    fill=tk.BOTH,
    expand=True
)


# Welcome message
chat_display.config(state="normal")
chat_display.insert(
    tk.END,
    "Yalini GPT: Hi! Welcome to Yalini GPT.\n"
    "I am your AI assistant. Ask me anything!\n\n"
)
chat_display.config(state="disabled")


# Input frame
input_frame = tk.Frame(
    root,
    bg="#EAF0FF"
)
input_frame.pack(
    fill=tk.X,
    padx=15,
    pady=(5, 15)
)


# Message box
message_box = tk.Entry(
    input_frame,
    font=("Arial", 12)
)
message_box.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    ipady=8,
    padx=(0, 10)
)


# Send button
send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    bg="#3155C6",
    fg="white",
    command=send_message
)
send_button.pack(
    side=tk.LEFT,
    ipadx=10,
    ipady=5
)


# Press Enter to send
message_box.bind(
    "<Return>",
    send_message
)

message_box.focus_set()


# Run application
root.mainloop()