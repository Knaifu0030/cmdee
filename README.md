# Cmdee - Your Terminal Companion

Cmdee is a witty, terminal-inspired AI assistant built with Textual and Google's Gemini AI. It provides helpful command-line guidance with a dash of personality!

## Features
- Interactive TUI (Terminal User Interface)
- Powered by Google's Gemini AI
- Helpful command-line assistance with a fun personality
- Web-compatible interface
- ![cmdee1](https://github.com/user-attachments/assets/b40b2311-eac7-457a-844a-dc7c41060749)
- ![cmdee2](https://github.com/user-attachments/assets/ff0cd139-85a0-4a51-b502-8b0b719039c1)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Knaifu0030/cmdee.git
cd cmdee
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
   - Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

Run locally:
```bash
python cmdee.py
```

Run as a web app:
```bash
textual-serve cmdee.py
```

## Contributing

Feel free to open issues or submit pull requests! 
