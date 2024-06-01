import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from ownLang import Interpreter

class SimpleIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple IDE")
        self.file_path = None

        self.create_widgets()
        self.interpreter = Interpreter()

    def create_widgets(self):
        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        menubar.add_cascade(label="Run", menu=run_menu)

        # Create a text editor
        self.text_editor = ScrolledText(self.root, wrap=tk.WORD, undo=True)
        self.text_editor.pack(fill=tk.BOTH, expand=1)

        # Create an output console
        self.console = ScrolledText(self.root, height=10, wrap=tk.WORD, state=tk.DISABLED, bg="black", fg="white")
        self.console.pack(fill=tk.X, expand=False)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".grah",
                                                    filetypes=[("Grah Files", "*.grah"), ("All Files", "*.*")])
        if not self.file_path:
            return
        with open(self.file_path, "r") as file:
            code = file.read()
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, code)

    def save_file(self):
        if not self.file_path:
            self.save_as_file()
        else:
            with open(self.file_path, "w") as file:
                code = self.text_editor.get(1.0, tk.END)
                file.write(code)

    def save_as_file(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".grah",
                                                      filetypes=[("Grah Files", "*.grah"), ("All Files", "*.*")])
        if not self.file_path:
            return
        self.save_file()

    def run_code(self):
        code = self.text_editor.get(1.0, tk.END)
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)

        # Redirect print to the console
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        try:
            self.interpreter.interpret(code)
            self.console.insert(tk.END, redirected_output.getvalue())
        except Exception as e:
            self.console.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            sys.stdout = old_stdout
            self.console.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    ide = SimpleIDE(root)
    root.mainloop()
