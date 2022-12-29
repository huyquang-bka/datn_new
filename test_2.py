import os
from PIL import Image
from tqdm import tqdm

path = ""
path_images = path + "/images"
path_labels = path + "/text_c10_copy"

images = []
texts = []
for folder in os.listdir(path_labels):
    print(folder)
    for fn in tqdm(os.listdir(os.path.join(path_labels, folder))):
        name = os.path.splitext(fn)[0]
        image = Image.open(os.path.join(path_images, folder, name + ".jpg"))
        image = image.resize((256, 256))
        with open(os.path.join(path_labels, folder, fn), "r") as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                texts.append(line.strip())
                images.append(image)
        