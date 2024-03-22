import tkinter as tk
from client.gui import Frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RED NEURONAL")
    root.iconbitmap("img/Gmvfi.ico")
    root.resizable(True, True)

    app = Frame(root=root)
    app.mainloop()