import cv2
import numpy as np

from scipy.interpolate import UnivariateSpline

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
        filtered = cv2.GaussianBlur(image, (35, 35), 0)

    elif action == 'BINARY':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    elif action == 'INVERT':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)

    elif action == 'CARTOONISED':
        num_iter = 5
        for _ in range(num_iter):
            image = cv2.bilateralFilter(image, d=9, sigmaColor=9, sigmaSpace=7)

        img_rgb = image

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

    elif action == 'SHARPEN':
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        filtered = cv2.filter2D(image, -1, kernel)

    elif action == 'SEPIA':
        kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
        filtered = cv2.filter2D(image, -1, kernel)

    elif action == 'EMBOSS':
        kernel = np.array([[0,-1,-1],
                            [1,0,-1],
                            [1,1,0]])
        filtered = cv2.filter2D(image, -1, kernel)

    elif action == "WARM":
        def spreadLookupTable(x, y):
            spline = UnivariateSpline(x, y)
            return spline(range(256))
    
        increaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        red_channel, green_channel, blue_channel = cv2.split(image)
        red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        filtered = cv2.merge((red_channel, green_channel, blue_channel))

    elif action == 'COOL':
        def spreadLookupTable(x, y):
            spline = UnivariateSpline(x, y)
            return spline(range(256))

        increaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 80, 160, 256])
        decreaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 50, 100, 256])
        red_channel, green_channel, blue_channel = cv2.split(image)
        red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
        filtered = cv2.merge((red_channel, green_channel, blue_channel))

    elif action == 'SKETCH':
        sk_gray, sk_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
        filtered = sk_gray

    elif action == 'HDR':
        hdr = cv2.detailEnhance(image, sigma_s=12, sigma_r=0.15)
        filtered = hdr

    return filtered
