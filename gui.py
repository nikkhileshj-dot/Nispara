import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("NISPARA AI")
app.geometry("700x500")

title = ctk.CTkLabel(
    app,
    text="🤖 NISPARA",
    font=("Arial", 30, "bold")
)
title.pack(pady=20)

status = ctk.CTkLabel(
    app,
    text="Status: Ready",
    font=("Arial", 18)
)
status.pack(pady=10)

chat = ctk.CTkTextbox(app, width=650, height=300)
chat.pack(pady=20)

app.mainloop()