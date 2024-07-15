import os
import requests
import jax
import jax.numpy as jnp
import numpy as np
from flax import linen as nn
from PIL import Image

# Define a simplified VGG-like model using Flax
class SimpleVGG(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.Conv(features=64, kernel_size=(3, 3), padding='SAME')(x)
        x = nn.relu(x)
        x = nn.Conv(features=64, kernel_size=(3, 3), padding='SAME')(x)
        x = nn.relu(x)
        x = nn.max_pool(x, window_shape=(2, 2), strides=(2, 2))
        
        x = nn.Conv(features=128, kernel_size=(3, 3), padding='SAME')(x)
        x = nn.relu(x)
        x = nn.Conv(features=128, kernel_size=(3, 3), padding='SAME')(x)
        x = nn.relu(x)
        x = nn.max_pool(x, window_shape=(2, 2), strides=(2, 2))
        
        x = nn.Conv(features=256, kernel_size=(3, 3), padding='SAME')(x)
        x = nn.relu(x)
        x = nn.Conv(features=256, kernel_size=(3, 3), padding='SAME')(x)
        x = nn.relu(x)
        x = nn.Conv(features=256, kernel_size=(3, 3), padding='SAME')(x)
        x = nn.relu(x)
        x = nn.max_pool(x, window_shape=(2, 2), strides=(2, 2))
        
        x = x.reshape((x.shape[0], -1))  # Flatten the array
        x = nn.Dense(features=4096)(x)
        x = nn.relu(x)
        x = nn.Dense(features=4096)(x)
        x = nn.relu(x)
        x = nn.Dense(features=1000)(x)
        
        return x

# Initialize the model
model = SimpleVGG()
rng = jax.random.PRNGKey(0)
variables = model.init(rng, jnp.ones((1, 224, 224, 3)))

# Function to preprocess the image
def preprocess_image(img_path):
    img = Image.open(img_path).convert('RGB')
    img = img.resize((224, 224))
    img_data = np.array(img) / 255.0
    img_data = np.expand_dims(img_data, axis=0)
    return jnp.array(img_data)

# Feature extraction function
def extract_features(img_path):
    img_data = preprocess_image(img_path)
    features = model.apply(variables, img_data)
    return features.flatten()

# Function to compute cosine similarity
def cosine_similarity(feature1, feature2):
    dot_product = jnp.dot(feature1, feature2)
    norm1 = jnp.linalg.norm(feature1)
    norm2 = jnp.linalg.norm(feature2)
    return dot_product / (norm1 * norm2)

# Define the directory for product images
product_images_dir = '/Users/shiwangikumari/Desktop/flask/fashion_app/product_images'

# Create the directory if it does not exist
os.makedirs(product_images_dir, exist_ok=True)

# List of image URLs to download (example URLs, replace with actual URLs)

image_urls = [
    'https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Mi%27kmaq_porcupine_quill_purse_%2840412695490%29.jpg/800px-Mi%27kmaq_porcupine_quill_purse_%2840412695490%29.jpg',
    'https://5.imimg.com/data5/CO/XW/MY-44197581/ladies-stylish-purse.jpg',
    'https://image.made-in-china.com/202f0j00NpFUJEqykucK/New-Designer-PU-Leather-Ladies-Handbags-Bags-with-Factory-Price-Shell-Bag.jpg',
]
# Download and save images to the directory
for i, url in enumerate(image_urls):
    response = requests.get(url)
    image_path = os.path.join(product_images_dir, f'product{i+1}.jpg')
    with open(image_path, 'wb') as f:
        f.write(response.content)

# Get a list of all image file paths in the directory
product_images = [os.path.join(product_images_dir, filename) for filename in os.listdir(product_images_dir) if filename.endswith('.jpg')]

# Extract features for all product images
product_features = [extract_features(img) for img in product_images]

# Function to find similar products
def find_similar_products(query_img_path, product_images, product_features, top_k=5):
    query_features = extract_features(query_img_path)
    similarities = [cosine_similarity(query_features, pf) for pf in product_features]
    sorted_indices = jnp.argsort(similarities)[::-1]  # Sort by similarity, descending
    return [product_images[i] for i in sorted_indices[:top_k]]

# Example usage
query_img_path = '/Users/shiwangikumari/Desktop/flask/fashion_app/product_images/query_image.jpg'
similar_products = find_similar_products(query_img_path, product_images, product_features)
print("Similar products:", similar_products)