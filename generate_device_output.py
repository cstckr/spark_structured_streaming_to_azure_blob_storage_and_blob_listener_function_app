import numpy as np
from PIL import Image
import uuid
import time
import random
import os


def generate_device_output():
    try:
        os.mkdir("./device_output")
    except FileExistsError:
        print("Folder already available")
    
    count = 1
    while True:
        time.sleep(random.randint(10, 15))
        img = Image.fromarray(
            np.random.randint(255, size=(32, 32), dtype=np.uint8))
        filename = uuid.uuid4()
        img.save(f"./device_output/{filename}.png")
        print("Count:", count, ", filename:", filename, 
              ", pixel_count count:", np.sum(img))
        count += 1


generate_device_output()
