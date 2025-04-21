import tkinter as tk
import subprocess
import os

ollama_path = r"C:\Users\rifra\AppData\Local\Programs\Ollama"
if ollama_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + ollama_path


class LLMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project LLM Assistant")

        # 🌑 Dark mode colors
        bg_color = "#1e1e1e"
        fg_color = "#d4d4d4"
        entry_bg = "#2d2d2d"
        button_bg = "#3a3a3a"
        highlight_color = "#007acc"

        self.root.configure(bg=bg_color)
        # Add this just before self.prompt_entry
        self.context_path_entry = tk.Entry(
            root, width=100, bg=entry_bg, fg=fg_color, insertbackground=fg_color
        )
        self.context_path_entry.insert(
            0, "Enter file or folder path for context..."
        )
        self.context_path_entry.pack(pady=(10, 0))

        self.prompt_entry = tk.Entry(
            root, width=100, bg=entry_bg, fg=fg_color, insertbackground=fg_color
        )
        self.prompt_entry.pack(pady=10)

        self.ask_button = tk.Button(
            root,
            text="Ask LLM",
            command=self.ask_llm,
            bg=button_bg,
            fg=fg_color,
            activebackground=highlight_color,
            activeforeground="white",
        )
        self.ask_button.pack(pady=5)

        self.output_text = tk.Text(
            root,
            wrap="word",
            height=25,
            width=100,
            bg=entry_bg,
            fg=fg_color,
            insertbackground=fg_color,
        )
        self.output_text.pack(pady=10)

        # Optionally: set a default project directory to help later with context
        self.project_root = os.path.abspath(".")

    def ask_llm(self):
        prompt = self.prompt_entry.get()
        context_path = self.context_path_entry.get().strip()

        if not prompt.strip():
            return

        self.output_text.insert(tk.END, f"\n>> You: {prompt}\n")

        # Build context string
        context_string = ""
        if os.path.exists(context_path):
            try:
                if os.path.isfile(context_path):
                    with open(
                        context_path, "r", encoding="utf-8", errors="ignore"
                    ) as f:
                        file_content = f.read()
                    context_string = f"Here is the content of the file `{os.path.basename(context_path)}`:\n\n{file_content}\n\n"
                elif os.path.isdir(context_path):
                    files = os.listdir(context_path)
                    context_string = (
                        f"The folder `{os.path.basename(context_path)}` contains:\n"
                        + "\n".join(files)
                        + "\n\n"
                    )
            except Exception as e:
                context_string = f"⚠️ Could not read context: {e}\n\n"

        # Final prompt to send to LLM
        full_prompt = (
            context_string
            + f"You are a helpful coding assistant. Here is my question:\n{prompt}"
        )

        try:
            command = [
                r"C:\Users\rifra\AppData\Local\Programs\Ollama\ollama.exe",
                "run",
                "deepseek-coder",
            ]

            result = subprocess.run(
                command,
                input=full_prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=600,
                check=True,
            )
            answer = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            answer = f"❌ Ollama failed:\n{e.stderr or str(e)}"
        except subprocess.TimeoutExpired:
            answer = "⚠️ Model timed out."

        self.output_text.insert(tk.END, f"{answer}\n")
        self.output_text.see(tk.END)


# Run the GUI
if __name__ == "__main__":

    root = tk.Tk()
    app = LLMApp(root)
    root.mainloop()
