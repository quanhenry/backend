import os
import logging
from anthropic import Anthropic

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hàm call_claude_api như bạn đã cung cấp
def call_claude_api(prompt, api_key, model="claude-3-5-sonnet-20240620"):
    client = Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=model,
            max_tokens=8000,
            temperature=0.2,
            system="Bạn là một chuyên gia lập trình full-stack. Nhiệm vụ của bạn là tạo mã cho các thành phần của một ứng dụng web.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        logging.error(f"Lỗi khi gọi API Claude: {str(e)}")
        return None

def generate_project_structure(base_path, api_key):
    project_structure = {
        "backend": {
            "src": {
                "config": ["database.js", "env.js"],
                "controllers": ["authController.js", "userController.js"],
                "middleware": ["auth.js", "errorHandler.js"],
                "models": ["User.js"],
                "routes": ["authRoutes.js", "userRoutes.js"],
                "services": ["emailService.js"],
                "utils": ["logger.js", "validators.js"],
                "app.js": None
            },
            "tests": {
                "unit": {},
                "integration": {}
            },
            ".env": None,
            ".gitignore": None,
            "package.json": None
        },
        "frontend": {
            "public": ["index.html", "favicon.ico", "manifest.json"],
            "src": {
                "components": {
                    "auth": ["Login.js", "Register.js"],
                    "common": ["Header.js", "Footer.js"],
                    "user": ["Profile.js"]
                },
                "context": ["AuthContext.js"],
                "hooks": ["useAuth.js"],
                "pages": ["Home.js", "Login.js", "Register.js"],
                "services": ["api.js", "authService.js"],
                "styles": ["global.css", "variables.css"],
                "utils": ["helpers.js"],
                "App.js": None,
                "App.css": None,
                "index.js": None,
                "setupTests.js": None
            },
            ".env": None,
            ".gitignore": None,
            "package.json": None
        },
        ".gitignore": None,
        "README.md": None
    }

    def create_structure(current_path, structure):
        for key, value in structure.items():
            path = os.path.join(current_path, key)
            if isinstance(value, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, value)
            elif isinstance(value, list):
                os.makedirs(path, exist_ok=True)
                for item in value:
                    file_path = os.path.join(path, item)
                    create_or_update_file(file_path)
            elif value is None:
                create_or_update_file(path)

    def create_or_update_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_content = file.read()
            if is_code_correct(file_path, existing_content):
                logging.info(f"File {file_path} is correct, no changes needed.")
                return
            else:
                logging.info(f"Updating file {file_path}")
        else:
            logging.info(f"Creating new file {file_path}")
        
        new_content = generate_code(file_path)
        if new_content:
            with open(file_path, 'w') as file:
                file.write(new_content)
        else:
            logging.error(f"Failed to generate content for {file_path}")

    def is_code_correct(file_path, existing_content):
        prompt = f"Kiểm tra xem mã sau đây cho file {os.path.basename(file_path)} có chính xác và đầy đủ không? Nếu không, giải thích tại sao:\n\n{existing_content}"
        response = call_claude_api(prompt, api_key)
        return response and "đúng" in response.lower() and "chính xác" in response.lower()

    def generate_code(file_path):
        file_name = os.path.basename(file_path)
        prompt = f"Tạo mã phù hợp cho file {file_name} trong một ứng dụng JavaScript full-stack. Chỉ cung cấp mã, không cần giải thích."
        return call_claude_api(prompt, api_key)

    create_structure(base_path, project_structure)

# Sử dụng hàm
api_key = ""  # Thay thế bằng API key thực của bạn
generate_project_structure("/Users/kieuphuchuy/Documents/full-stack/ai-code-generator", api_key)