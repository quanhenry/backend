import os
import json
import logging
from anthropic import Anthropic
from dotenv import load_dotenv

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load biến môi trường từ file .env
load_dotenv()

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

def generate_code_with_claude(prompt, file_path, api_key):
    full_prompt = f"""
    Hãy tạo mã cho: {prompt}
    Chỉ trả về mã dưới dạng chuỗi JSON, không cần giải thích thêm.
    Ví dụ: {{"code": "function example() {{ console.log('Hello, World!'); }}"}}
    """
    response = call_claude_api(full_prompt, api_key)
    if response:
        try:
            code_dict = json.loads(response, strict=False)
            generated_code = code_dict['code']
            
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Lưu mã vào file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            
            logging.info(f"Mã đã được tạo và lưu vào {file_path}")
            return f"Mã đã được tạo và lưu vào {file_path}"
        except json.JSONDecodeError as e:
            logging.error(f"Lỗi: Không thể phân tích chuỗi JSON từ phản hồi API: {str(e)}")
            logging.error(f"Phản hồi gốc: {response}")
        except KeyError:
            logging.error(f"Lỗi: Không tìm thấy khóa 'code' trong phản hồi JSON: {response}")
    return None

def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logging.error("API key không được tìm thấy. Hãy đảm bảo bạn đã set biến môi trường ANTHROPIC_API_KEY.")
        return

    backend_path = "/Users/kieuphuchuy/Documents/full-stack/ai-code-generator/backend"
    frontend_path = "/Users/kieuphuchuy/Documents/full-stack/ai-code-generator/frontend"

    # Tạo model User
    user_model_prompt = "Tạo một Mongoose User model với các trường: username, email, và password. Bao gồm cả hashing password."
    user_model_path = os.path.join(backend_path, "src", "models", "User.js")
    generate_code_with_claude(user_model_prompt, user_model_path, api_key)

    # Tạo auth controller
    auth_controller_prompt = "Tạo một Express.js auth controller với các hàm đăng ký và đăng nhập. Sử dụng JWT cho xác thực."
    auth_controller_path = os.path.join(backend_path, "src", "controllers", "authController.js")
    generate_code_with_claude(auth_controller_prompt, auth_controller_path, api_key)

    # Tạo React Login component
    login_component_prompt = "Tạo một React functional component cho form đăng nhập. Sử dụng hooks và axios cho API calls."
    login_component_path = os.path.join(frontend_path, "src", "components", "Login.js")
    generate_code_with_claude(login_component_prompt, login_component_path, api_key)

    logging.info("Hoàn thành tạo mã cho tất cả các thành phần.")

if __name__ == "__main__":
    main()