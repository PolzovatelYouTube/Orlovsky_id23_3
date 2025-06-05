import requests
import base64
import json
from PIL import Image
import io
#import matplotlib.pyplot as plt

# URL вашего API
BASE_URL = "http://127.0.0.1:8000/api"

# Регистрация пользователя
def register_user(email, password):
    response = requests.post(
        f"{BASE_URL}/sign-up/", 
        json={"email": email, "password": password}
    )
    return response.json()

# Вход в систему
def login_user(email, password):
    response = requests.post(
        f"{BASE_URL}/login/", 
        json={"email": email, "password": password}
    )
    return response.json()

# Бинаризация изображения
def binarize_image(image_path, token, algorithm="otsu"):
    # Чтение и кодирование изображения в base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Отправка запроса на бинаризацию
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/binary_image", 
        headers=headers,
        json={"image": base64_image, "algorithm": algorithm}
    )
    
    # Декодирование результата
    result = response.json()
    binary_image_base64 = result.get("binarized_image")
    
    # Преобразование base64 обратно в изображение
    binary_image_data = base64.b64decode(binary_image_base64)
    binary_image = Image.open(io.BytesIO(binary_image_data))
    
    return binary_image

# Пример использования
if __name__ == "__main__":
    # Замените на свои данные
    email = "test2@mail.ru"
    password = "test2@"
    image_path = "testo.jpg"
    
    # Регистрация пользователя
    # user_data = register_user(email, password)
    # print("Регистрация:", user_data)
    
    # Или вход, если пользователь уже зарегистрирован
    user_data = login_user(email, password)
    print("Вход:", user_data)
    
    # Получение токена
    token = user_data.get("token")
    
    # Бинаризация изображения
    binary_image = binarize_image(image_path, token)
'''
    # Отображение результата
    plt.figure(figsize=(10, 5))
    
    # Исходное изображение
    plt.subplot(1, 2, 1)
    original_image = Image.open(image_path)
    plt.imshow(original_image)
    plt.title("Исходное изображение")
    
    # Бинаризованное изображение
    plt.subplot(1, 2, 2)
    plt.imshow(binary_image, cmap='gray')
    plt.title("Бинаризованное изображение")
    
    plt.tight_layout()
    plt.show()
'''