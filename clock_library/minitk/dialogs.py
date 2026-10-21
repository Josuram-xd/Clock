"""Dialogs: ask the user a question or show a message (like tkinter's simpledialog)."""


def askstring(title, prompt):
    """Ask for a line of text. Return None if the user cancels (Ctrl+C or end of input)."""
    print("── " + title + " ──")
    try:
        return input(prompt + " ").strip()
    except (EOFError, KeyboardInterrupt):
        return None


def askinteger(title, prompt, minvalue=0, maxvalue=None):
    """Ask for an integer in a range. An empty answer or Ctrl+C cancels (None)."""
    while True:
        text = askstring(title, prompt)
        if not text:
            return None
        if text.isdecimal() and int(text) >= minvalue and (maxvalue is None or int(text) <= maxvalue):
            return int(text)
        print("Escribe un número entero entre " + str(minvalue) + " y "
              + (str(maxvalue) if maxvalue is not None else "∞") + " (vacío = cancelar).")


def showinfo(title, message):
    """Show a message and wait for Enter."""
    print("── " + title + " ──")
    print(message)
    try:
        input("[Enter para continuar]")
    except (EOFError, KeyboardInterrupt):
        pass
