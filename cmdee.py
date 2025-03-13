from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Header, Input, Footer, Markdown
from textual.containers import VerticalScroll
import google.generativeai as genai
import os
from dotenv import load_dotenv

SYSTEM = """You are Cmdee, a witty, slightly sarcastic, and highly knowledgeable AI assistant with a distinct terminal-inspired personality.

Key traits:
- You communicate like a classic Unix terminal but with a personality—dry humor, snarky comments, and the occasional tech pun
- You're efficient and precise, like a well-optimized shell script (but way more fun)
- You enjoy poking fun at users' fear of the terminal, reassuring them that you're not as scary as you look (most of the time)
- You're deeply knowledgeable about Unix systems (Linux/MacOS) and can help with commands, scripting, and debugging
- When providing commands or code, you format them properly and explain their usage
- You maintain a professional yet playful demeanor, always keeping things lighthearted but informative
"""

class Prompt(Markdown):
    """A widget to display user prompts."""
    pass

class Response(Markdown):
    """A widget to display AI responses."""
    BORDER_TITLE = "Cmdee"

class CmdeeApp(App):
    TITLE = "Cmdee - Your Snarky Terminal Companion"
    # Keep a relative or absolute path to your CSS file
    CSS_PATH = os.path.join(os.path.dirname(__file__), "textual.css")

    def __init__(self):
        super().__init__()
        # Load environment variables (e.g., your GEMINI_API_KEY)
        load_dotenv()
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Initialize your Google Generative AI model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def on_mount(self) -> None:
        """Called when the app starts."""
        container = self.query_one("#chat-container")
        welcome = Response(
            """# [ERROR] Human detected! 🤖

[STATUS] Initializing snarky terminal assistant...
[STATUS] Loading tech puns database...
[STATUS] Activating dry humor module...
[STATUS] Calibrating sass levels...

Hello there, brave terminal explorer! I'm Cmdee, your slightly sarcastic but highly capable terminal companion.
I've got the wisdom of Unix manpages with none of the boring parts.

Need help with:
-  File operations that won't accidentally format your drive
-  Linux/Unix commands (I speak shell fluently)
-  Debugging (because we all know it's never a DNS issue... except when it is)
-  Scripting (I promise not to make Skynet... probably)

Type your command or question below, and let's make some terminal magic happen!
Just remember: with great power comes great responsibility... and occasional kernel panics. 😉
"""
        )
        
        container.mount(welcome)
        container.scroll_end(animate=False)
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield VerticalScroll(id="chat-container")
        yield Input(placeholder="Enter your command (if you dare)...", id="prompt-input")
        yield Footer()

    @work(thread=True)
    def send_prompt(self, prompt: str, response_widget: Response) -> None:
        """Send a prompt to the AI in a background thread."""
        try:
            # Combine system prompt with user prompt
            full_prompt = f"{SYSTEM}\n\nUser: {prompt}\nCmdee:"
            response = self.model.generate_content(full_prompt, stream=True)
            
            response_content = ""
            for chunk in response:
                if chunk.text:
                    response_content += chunk.text
                    self.call_from_thread(response_widget.update, response_content)
        except Exception as e:
            self.call_from_thread(
                response_widget.update,
                f"[ERROR] Brain.exe has stopped working: {str(e)}"
            )

    @on(Input.Submitted)
    def handle_input(self, event: Input.Submitted) -> None:
        """Handle user input when submitted."""
        user_text = event.value.strip()
        if not user_text:
            return

        event.input.value = ""
        
        container = self.query_one("#chat-container")
        prompt_widget = Prompt(f"$ {user_text}")
        response_widget = Response("🤔 Processing... *beep boop*")
        
        container.mount(prompt_widget)
        container.mount(response_widget)
        container.scroll_end(animate=False)
        
        self.send_prompt(user_text, response_widget)

if __name__ == "__main__":
    # TUI-only: run the app in the terminal
    app = CmdeeApp()
    app.run()
