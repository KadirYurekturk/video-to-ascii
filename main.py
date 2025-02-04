import cv2
import numpy as np
import os
import time

def clamp(x, mn, mx):
    return max(mn, min(x, mx))

def adjust_brightness_contrast(img, brightness, contrast):
    # Hesaplanan kontrast katsayısı
    factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
    adjusted = factor * (img - 128) + 128 + brightness
    return np.clip(adjusted, 0, 255)

def floyd_steinberg_dithering(image, n_levels):
    h, w = image.shape
    img = image.copy().astype(np.float32)
    for y in range(h):
        for x in range(w):
            oldpixel = img[y, x]
            newpixel = round(oldpixel / 255 * (n_levels - 1)) * (255 / (n_levels - 1))
            img[y, x] = newpixel
            error = oldpixel - newpixel
            if x + 1 < w:
                img[y, x+1] += error * 7/16
            if x - 1 >= 0 and y + 1 < h:
                img[y+1, x-1] += error * 3/16
            if y + 1 < h:
                img[y+1, x] += error * 5/16
            if x + 1 < w and y + 1 < h:
                img[y+1, x+1] += error * 1/16
    return np.clip(img, 0, 255)

# Detaylı karakter seti (detailed)
detailed_gradient = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."

def frame_to_ascii(frame, output_width=149, brightness=100, contrast=28, invert=False, dithering=True):
    h, w, _ = frame.shape
    font_aspect_ratio = 0.55
    output_height = int((h / w) * output_width * font_aspect_ratio)
    # Yeniden boyutlandırma
    resized = cv2.resize(frame, (output_width, output_height))
    # Gri tonlara çevirme
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY).astype(np.float32)
    if invert:
        gray = 255 - gray
    gray = adjust_brightness_contrast(gray, brightness, contrast)
    if dithering:
        gray = floyd_steinberg_dithering(gray, len(detailed_gradient))
    ascii_art = ""
    n_levels = len(detailed_gradient)
    for i in range(output_height):
        line = ""
        for j in range(output_width):
            pixel = gray[i, j]
            idx = int(round((pixel / 255) * (n_levels - 1)))
            idx = min(max(idx, 0), n_levels - 1)
            line += detailed_gradient[idx]
        ascii_art += line + "\n"
    return ascii_art

def main():
    cap = cv2.VideoCapture(0)  # Varsayılan kamerayı kullanır
    if not cap.isOpened():
        print("Kamera açılamadı.")
        return
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            art = frame_to_ascii(frame,
                                 output_width=149,
                                 brightness=100,
                                 contrast=28,
                                 invert=False,
                                 dithering=True)
            os.system('cls' if os.name == 'nt' else 'clear')
            # Matrix tarzı yeşil yazı efekti için ANSI escape kodları kullanılır.
            print("\033[32m" + art + "\033[0m")
            time.sleep(0.05)  # Yaklaşık 20 FPS
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()

if __name__ == '__main__':
    main()
