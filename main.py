# main.py
import tkinter as tk
from tkinter import Text
import openai
import tkinter.messagebox
from config import openai_api_key  # import the API key from config.py

root = tk.Tk()
root.title("Alex")
root.geometry("800x600")
root.configure(bg='#000000')

chat_frame = tk.Frame(root, bg='#0A0A0A')
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_area = Text(chat_frame, bg='#0A0A0A', fg='#9BC53D', font=("Ubuntu", 12))
chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(chat_frame, command=chat_area.yview, bg='#0A0A0A')
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_area['yscrollcommand'] = scrollbar.set

# Prevent the user from typing in the conversation box
chat_area.config(state=tk.DISABLED)

input_frame = tk.Frame(root, bg='#0A0A0A')
input_frame.pack(padx=10, pady=10, fill=tk.X)

user_input = tk.Entry(input_frame, bg='#0A0A0A', fg='#9BC53D', font=("Ubuntu", 12))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)

# Set focus to the input box
user_input.focus()

# The chat history is a list of dictionaries, where each dictionary has two keys: "role" and "content".
chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

def clear_chat():
    chat_area.delete('1.0', tk.END)

def send_message(event=None):
    message = user_input.get().strip()  # get the user's input and strip whitespace

    if not message:
        tk.messagebox.showwarning("Warning", "Message cannot be empty.")
        return

    user_input.delete(0, tk.END)  # clear the input box

    chat_area.insert(tk.END, "User: " + message + "\n")  # add the user's message to the chat area

    chat_history.append({"role": "user", "content": message})  # add the user's message to the chat history


    try:
        openai.api_key = openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history
        )
    except Exception as e:
        chat_area.insert(tk.END, "Alex: " + "I'm sorry, I encountered an error: " + str(e) + "\n")
        return

    response_content = response['choices'][0]['message']['content']
    chat_area.insert(tk.END, "Alex: " + response_content + "\n")  # add the response to the chat area
    chat_history.append({"role": "assistant", "content": response_content})  # add the AI's response to the chat history
    chat_area.yview(tk.END)  # automatically scroll to the end of the chat

clear_button = tk.Button(input_frame, text="Clear Chat", bg='#323031', fg='#8BCD51', command=clear_chat, font=("Ubuntu", 12), relief='groove')
clear_button.pack(side=tk.RIGHT, ipadx=5, ipady=5)

send_button = tk.Button(input_frame, text="Send", bg='#323031', fg='#8BCD51', command=send_message, font=("Ubuntu", 12), relief='groove')
send_button.pack(side=tk.RIGHT, ipadx=5, ipady=5)

root.bind("<Return>", send_message)

root.mainloop()
