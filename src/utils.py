import numpy as np
from PIL import Image

def compute_cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return float(dot_product / (norm_v1 * norm_v2 + 1e-8))

def generate_differential_heatmap(img1, img2, image_size=224):
    arr1 = np.array(img1.resize((image_size, image_size)), dtype=np.float32)
    arr2 = np.array(img2.resize((image_size, image_size)), dtype=np.float32)
    diff = np.mean(np.abs(arr1 - arr2), axis=2)
    diff = (diff - diff.min()) / (diff.max() - diff.min() + 1e-8)
    return diff