import requests
import time
import base64
from PIL import Image
from io import BytesIO

API_URL = "http://127.0.0.1:8000/api"

def login_user(email, password):
    response = requests.post(
        f"{API_URL}/login/",
        json={"email": email, "password": password}
    )
    response.raise_for_status()
    return response.json()["token"]

def start_binarization(image_path, token):
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    response = requests.post(
        f"{API_URL}/binary_image",
        json={"image": image_data, "algorithm": "otsu"},
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()["task_id"]

def get_task_status(task_id, token):
    response = requests.get(
        f"{API_URL}/tasks/status/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()

def main():
    email = "a@a.a"
    password = "a"
    image_path = "testo.jpg"

    token = login_user(email, password)
    print("Logged in, token received.")

    task_id = start_binarization(image_path, token)
    print(f"Started binarization task with id: {task_id}")

    while True:
        status = get_task_status(task_id, token)
        progress = status.get("progress", 0)
        state = status.get("state", "")
        print(f"Task status: {state}, progress: {progress}%")
        if state == "SUCCESS":
            binarized_image_b64 = status["result"]["binarized_image"]
            image_data = base64.b64decode(binarized_image_b64)
            image = Image.open(BytesIO(image_data))
            image.show()
            print("Binarization completed and image displayed.")
            break
        elif state == "FAILURE":
            print(f"Task failed with error: {status.get('error')}")
            break
        time.sleep(1)

if __name__ == "__main__":
    main()
