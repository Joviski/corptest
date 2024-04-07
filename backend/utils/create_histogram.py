import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import BytesIO

def create_color_histogram(image):
    # Read the image
    image_np = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    # Prepare the histogram plot
    for i, color in enumerate(['r', 'g', 'b']):
        hist = cv2.calcHist([image_rgb], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    plt.title('Color Histogram')
    plt.xlabel('Bin')
    plt.ylabel('Frequency')

    # Save the plot as an image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()  # Close the plot to free memory
    buffer.seek(0)

    # Convert the buffer to a NumPy array
    image_data = np.frombuffer(buffer.getvalue(), dtype=np.uint8)

    # Read the image data as an image
    histogram_image = cv2.imdecode(image_data, 1)
    _, buffer = cv2.imencode('.png', histogram_image)

    # Convert buffer to byte stream
    byte_stream = buffer.tobytes()

    return byte_stream