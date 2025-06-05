import base64
import io
import numpy as np
from PIL import Image

def decode_base64_image(base64_str):
    """Декодирует base64-строку в объект изображения."""
    img_data = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_data))
    return img

def encode_base64_image(image):
    """Кодирует изображение в base64-строку."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def convert_to_grayscale(image):
    """Преобразует изображение в оттенки серого с помощью PILLOW."""
    return image.convert('L')

def calculate_histogram(image_array):
    """Вычисляет гистограмму для изображения в оттенках серого."""
    histogram = np.zeros(256, dtype=int)
    height, width = image_array.shape
    
    for y in range(height):
        for x in range(width):
            pixel_value = image_array[y, x]
            histogram[pixel_value] += 1
            
    return histogram

def otsu_threshold(image_array):
    """
    Реализация алгоритма Отсу для нахождения порогового значения.
    
    Алгоритм Отсу выбирает такой порог, что дисперсия между классами максимальна.
    """
    # Расчет гистограммы
    histogram = calculate_histogram(image_array)
    
    # Общее количество пикселей
    total_pixels = np.sum(histogram)
    
    # Инициализация переменных
    sum_total = 0
    for i in range(256):
        sum_total += i * histogram[i]
    
    # Поиск оптимального порога
    max_variance = 0
    optimal_threshold = 0
    sum_background = 0
    weight_background = 0
    
    for threshold in range(256):
        # Вес фона (пиксели ниже порога)
        weight_background += histogram[threshold]
        if weight_background == 0:
            continue
        
        # Вес объекта (пиксели выше порога)
        weight_object = total_pixels - weight_background
        if weight_object == 0:
            break
        
        # Сумма значений пикселей фона
        sum_background += threshold * histogram[threshold]
        
        # Средние значения для фона и объекта
        mean_background = sum_background / weight_background
        mean_object = (sum_total - sum_background) / weight_object
        
        # Расчет межклассовой дисперсии
        variance = weight_background * weight_object * (mean_background - mean_object) ** 2
        
        # Обновление оптимального порога
        if variance > max_variance:
            max_variance = variance
            optimal_threshold = threshold
    
    return optimal_threshold

def apply_threshold(image_array, threshold):
    """Применяет пороговое значение к изображению."""
    binary_image = np.zeros_like(image_array)
    binary_image[image_array > threshold] = 255
    return binary_image

def binarize_image(base64_image, algorithm="otsu"):
    """
    Бинаризация изображения с использованием выбранного алгоритма.
    
    Параметры:
    - base64_image: строка изображения в формате base64
    - algorithm: строка с названием алгоритма бинаризации ("otsu" по умолчанию)
    
    Возвращает:
    - строку с бинаризованным изображением в формате base64
    """
    # Декодирование изображения из base64
    image = decode_base64_image(base64_image)
    
    # Преобразование в оттенки серого
    gray_image = convert_to_grayscale(image)
    
    # Преобразование в массив numpy для обработки
    image_array = np.array(gray_image)
    
    # Выбор и применение алгоритма бинаризации
    if algorithm.lower() == "otsu":
        # Нахождение порога методом Отсу
        threshold = otsu_threshold(image_array)
        # Применение порога
        binary_array = apply_threshold(image_array, threshold)
    else:
        raise ValueError(f"Алгоритм {algorithm} не реализован")
    
    # Преобразование обратно в объект PIL Image
    binary_image = Image.fromarray(binary_array.astype('uint8'))
    
    # Кодирование результата в base64
    result_base64 = encode_base64_image(binary_image)
    
    return result_base64