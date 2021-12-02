import cv2
import numpy as np

def get_filtered_image(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    filtered = None
    if action == 'NO_FILTER':
        filtered = image
    elif action == 'COLORIZED':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif action == 'BLURRED':
        width, height = img.shape[:2]
        if width > 500:
            k = (50, 50)
        elif width > 200 and width <=500:
            k = (25,25)
        else:
            k = (10,10)
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    elif action == 'BINARY':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif action == 'INVERT':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)
    elif action == 'CARTOONISED':
        img_small = cv2.pyrDown(image)

        num_iter = 5
        for _ in range(num_iter):
            img_small = cv2.bilateralFilter(img_small, d=9, sigmaColor=9, sigmaSpace=7)

        img_rgb = cv2.pyrUp(img_small)

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)

        img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2)

        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)

        filtered = cv2.bitwise_and(image, img_edge)
    elif action == 'WATER-ART':
        # resizing the image
        # Interpolation is cubic for best results
        image_resized = cv2.resize(image, None, fx=0.5, fy=0.5)

        # removing impurities from image
        image_cleared = cv2.medianBlur(image_resized, 3)
        image_cleared = cv2.medianBlur(image_cleared, 3)
        image_cleared = cv2.medianBlur(image_cleared, 3)

        image_cleared = cv2.edgePreservingFilter(image_cleared, sigma_s=5)

        # Bilateral Image filtering
        image_filtered = cv2.bilateralFilter(image_cleared, 3, 10, 5)

        for i in range(2):
            image_filtered = cv2.bilateralFilter(image_filtered, 3, 20, 10)

        for i in range(3):
            image_filtered = cv2.bilateralFilter(image_filtered, 5, 30, 10)

        # Sharpening the image using addWeighted()
        gaussian_mask = cv2.GaussianBlur(image_filtered, (7, 7), 2)
        image_sharp = cv2.addWeighted(image_filtered, 1.5, gaussian_mask, -0.5, 0)
        image_sharp = cv2.addWeighted(image_sharp, 1.4, gaussian_mask, -0.2, 10)

        filtered = image_sharp
    return filtered
