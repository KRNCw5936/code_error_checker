import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import tempfile

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Error Checker")
        self.root.geometry("800x600")  # Memperbesar jendela aplikasi

        # Frame untuk judul
        title_frame = tk.Frame(root)
        title_frame.pack(pady=10, fill=tk.X)

        # Label untuk judul
        title_label = tk.Label(title_frame, text="Code Error Checker", font=("Arial", 18, "bold"))
        title_label.pack()

        # Frame untuk dropdown dan tombol
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)

        # Dropdown untuk memilih bahasa pemrograman
        self.languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++']
        self.selected_language = tk.StringVar(value=self.languages[0])

        language_label = tk.Label(top_frame, text="Select Language:")
        language_label.pack(side=tk.LEFT, padx=10)

        self.language_dropdown = ttk.Combobox(top_frame, textvariable=self.selected_language, values=self.languages)
        self.language_dropdown.pack(side=tk.LEFT, padx=10)

        # Tombol untuk mengecek error
        self.check_button = tk.Button(top_frame, text="Check Error", command=self.check_code)
        self.check_button.pack(side=tk.LEFT, padx=10)

        # Frame untuk textbox dan output
        middle_frame = tk.Frame(root)
        middle_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Textbox untuk memasukkan kode
        self.textbox = scrolledtext.ScrolledText(middle_frame, width=100, height=20, wrap=tk.WORD)
        self.textbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Area untuk output hasil error
        self.output_box = tk.Text(middle_frame, width=60, height=20, wrap=tk.WORD, state=tk.NORMAL)
        self.output_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Configure tag for error text
        self.output_box.tag_configure("error", foreground="red")

    def check_code(self):
        code = self.textbox.get("1.0", tk.END)
        language = self.selected_language.get()

        # Temporary file untuk menyimpan kode sementara
        with tempfile.NamedTemporaryFile(suffix=self.get_file_extension(language), delete=False) as temp_file:
            temp_file.write(code.encode())
            temp_file.flush()

            try:
                # Cek error berdasarkan bahasa yang dipilih
                if language == 'Python':
                    self.run_python(temp_file.name)
                elif language == 'Java':
                    self.run_java(temp_file.name)
                elif language == 'JavaScript':
                    self.run_javascript(temp_file.name)
                elif language == 'C#':
                    self.run_csharp(temp_file.name)
                elif language == 'C++':
                    self.run_cpp(temp_file.name)
            except Exception as e:
                self.display_output(f"Error: {str(e)}")

    def get_file_extension(self, language):
        """Mengembalikan ekstensi file berdasarkan bahasa."""
        extensions = {
            'Python': '.py',
            'Java': '.java',
            'JavaScript': '.js',
            'C#': '.cs',
            'C++': '.cpp'
        }
        return extensions.get(language, '.txt')

    def run_python(self, file_path):
        result = subprocess.run(['python3', '-m', 'py_compile', file_path], capture_output=True, text=True)
        self.display_output(result.stderr if result.returncode != 0 else "No syntax errors found!")

    def run_java(self, file_path):
        result = subprocess.run(['javac', file_path], capture_output=True, text=True)
        self.display_output(result.stderr if result.returncode != 0 else "No syntax errors found!")

    def run_javascript(self, file_path):
        result = subprocess.run(['node', '--check', file_path], capture_output=True, text=True)
        self.display_output(result.stderr if result.returncode != 0 else "No syntax errors found!")

    def run_csharp(self, file_path):
        result = subprocess.run(['mcs', file_path], capture_output=True, text=True)
        self.display_output(result.stderr if result.returncode != 0 else "No syntax errors found!")

    def run_cpp(self, file_path):
        result = subprocess.run(['g++', '-fsyntax-only', file_path], capture_output=True, text=True)
        self.display_output(result.stderr if result.returncode != 0 else "No syntax errors found!")

    def display_output(self, message):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete(1.0, tk.END)
        
        # Highlight errors in red
        lines = message.splitlines()
        for line in lines:
            if 'error' in line.lower():  # Simple check to colorize lines containing "error"
                self.output_box.insert(tk.END, line + "\n", "error")
            else:
                self.output_box.insert(tk.END, line + "\n")
        
        self.output_box.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditor(root)
    root.mainloop()