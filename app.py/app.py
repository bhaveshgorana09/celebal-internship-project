import os
import streamlit as st
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import rasterio

# =====================================================================
# 1. CORE APPLICATIVE LAYOUT & INTERFACE PARAMETERS
# =====================================================================
st.set_page_config(
    layout="wide", 
    page_title="GeoAI Temporal Analytics Pro", 
    page_icon="🌐",
    initial_sidebar_state="expanded"
)

# Advanced UI Custom Glassmorphism CSS for Modern Look
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 12px; border: 1px solid #1e293b; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    div[data-testid="stMetricDelta"] > div { font-weight: bold !important; }
    .stAlert { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

IMAGE_SIZE = 224
CLASS_NAMES = [
    'AnnualCrop', 'Forest', 'HerbaceousVegetation', 'Highway', 
    'Industrial', 'Pasture', 'PermanentCrop', 'Residential', 
    'River', 'SeaLake'
]

DEFAULT_THRESHOLD = 0.885 

# =====================================================================
# 2. FILE HANDLING HELPER (SATELLITE .TIF & STANDARD IMAGE SUPPORT)
# =====================================================================
def load_satellite_image(uploaded_file):
    """
    Safely reads standard images (PNG, JPG) and geospatial TIFF (.tif) files,
    converting them into a standard RGB PIL Image format for PyTorch inference.
    """
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0)
    
    if uploaded_file.name.lower().endswith(('.tif', '.tiff')):
        try:
            with rasterio.open(uploaded_file) as src:
                if src.count >= 3:
                    arr = src.read([1, 2, 3])
                    arr = np.transpose(arr, (1, 2, 0))
                else:
                    arr = src.read(1)
                    arr = np.stack([arr, arr, arr], axis=-1)
                
                if arr.max() > 255:
                    arr = ((arr - arr.min()) / (arr.max() - arr.min()) * 255).astype(np.uint8)
                else:
                    arr = arr.astype(np.uint8)
                
                return Image.fromarray(arr)
        except Exception as e:
            st.error(f"Error decoding GeoTIFF matrix framework: {str(e)}")
            return None
    else:
        return Image.open(uploaded_file).convert('RGB')

# =====================================================================
# 3. RUNTIME INFERENCE ENGINE INITIALIZATION
# =====================================================================
@st.cache_resource
def load_production_vision_models():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    checkpoint_path = os.path.join("models", "resnet18_eurosat_finetuned.pt")
    
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Missing fine-tuned checkpoint matrix: {checkpoint_path}. Run Step 3 first.")
        
    classifier_model = models.resnet18()
    classifier_model.fc = nn.Linear(classifier_model.fc.in_features, 10)
    classifier_model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    classifier_model.eval()
    classifier_model.to(device)
    
    extractor_model = models.resnet18()
    extractor_model.fc = nn.Linear(extractor_model.fc.in_features, 10)
    extractor_model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    extractor_model.fc = nn.Identity()  
    extractor_model.eval()
    extractor_model.to(device)
    
    return classifier_model, extractor_model, device

try:
    classifier, extractor, active_device = load_production_vision_models()
    engine_status = f"ℹ️ Compute Status: Active on **{str(active_device).upper()}** Core"
except Exception as e:
    st.error(f"System Error: Application Initialization Failure: {str(e)}")
    st.stop()

eval_transforms = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# =====================================================================
# 4. ANALYTICAL PROCESSING FUNCTIONS
# =====================================================================
def infer_land_use(image, model, transform_pipeline, target_device):
    tensor = transform_pipeline(image).unsqueeze(0).to(target_device)
    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.nn.functional.softmax(logits, dim=1)[0]
    
    confidence, class_idx = torch.max(probabilities, dim=0)
    return CLASS_NAMES[class_idx.item()], confidence.item()

def extract_latent_embeddings(image, model, transform_pipeline, target_device):
    tensor = transform_pipeline(image).unsqueeze(0).to(target_device)
    with torch.no_grad():
        embedding = model(tensor).cpu().numpy().flatten()
    return embedding

def generate_differential_heatmap(img1, img2):
    arr1 = np.array(img1.resize((IMAGE_SIZE, IMAGE_SIZE)), dtype=np.float32)
    arr2 = np.array(img2.resize((IMAGE_SIZE, IMAGE_SIZE)), dtype=np.float32)
    diff = np.mean(np.abs(arr1 - arr2), axis=2)
    diff = (diff - diff.min()) / (diff.max() - diff.min() + 1e-8)
    return diff

# =====================================================================
# 5. STREAMLIT APPLICATION FRONTEND ORCHESTRATION
# =====================================================================
st.title("🌐 GeoAI Temporal Analytics & Change Detection Platform")
st.caption(f"{engine_status} | Enterprise Dashboard v2.5")
st.markdown("---")

# --- ADVANCED SIDEBAR CONTROLS ---
st.sidebar.image("https://img.icons8.com/nolan/64/earth-planets.png", width=50)
st.sidebar.title("Control Center")
st.sidebar.markdown("---")

# Feature 1: Similarity Slider
sim_threshold = st.sidebar.slider(
    "Similarity Cutoff Threshold", 
    min_value=0.50, max_value=1.00, 
    value=DEFAULT_THRESHOLD, step=0.005,
    help="Pairs falling below this setting trigger an alert for environmental shifts."
)

st.sidebar.markdown("### ⚙️ Image Optimization")
# Feature 2: Interactive Brightness Controller
brightness_factor = st.sidebar.slider(
    "Live Image Brightness", 
    min_value=0.5, max_value=2.0, 
    value=1.0, step=0.1,
    help="Adjust visibility for dark satellite tiles."
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📋 Operating Profiles:
* **High Precision Mode**: Cutoff ~ `0.950`
* **Balanced Mode (Optimal)**: Cutoff ~ `0.885`
* **High Recall Mode**: Cutoff ~ `0.800`
""")

# Compact Upload Layout
upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    st.markdown("##### ⏱️ Baseline Frame (T1)")
    uploaded_file_t1 = st.file_uploader("Upload T1", type=["png", "jpg", "jpeg", "tif", "tiff"], key="t1_uploader", label_visibility="collapsed")

with upload_col2:
    st.markdown("##### ⏱️ Monitoring Frame (T2)")
    uploaded_file_t2 = st.file_uploader("Upload T2", type=["png", "jpg", "jpeg", "tif", "tiff"], key="t2_uploader", label_visibility="collapsed")

image_t1, image_t2 = None, None

# Centered Compact Grid for Images
if uploaded_file_t1 or uploaded_file_t2:
    img_disp_col1, img_disp_col2, _ = st.columns([1.5, 1.5, 2])
    
    with img_disp_col1:
        if uploaded_file_t1:
            raw_image_t1 = load_satellite_image(uploaded_file_t1)
            if raw_image_t1:
                # Apply live brightness adjustment
                enhancer = ImageEnhance.Brightness(raw_image_t1)
                image_t1 = enhancer.enhance(brightness_factor)
                st.image(image_t1, width=280, caption="T1 Baseline View")

    with img_disp_col2:
        if uploaded_file_t2:
            raw_image_t2 = load_satellite_image(uploaded_file_t2)
            if raw_image_t2:
                # Apply live brightness adjustment
                enhancer = ImageEnhance.Brightness(raw_image_t2)
                image_t2 = enhancer.enhance(brightness_factor)
                st.image(image_t2, width=280, caption="T2 Analysis View")

# Deep Learning Inference Execution
if image_t1 and image_t2:
    st.markdown("---")
    st.subheader("📊 Analytical Summary")
    
    with st.spinner("Analyzing structural arrays across spatial layers..."):
        class_t1, conf_t1 = infer_land_use(image_t1, classifier, eval_transforms, active_device)
        class_t2, conf_t2 = infer_land_use(image_t2, classifier, eval_transforms, active_device)
        
        emb_t1 = extract_latent_embeddings(image_t1, extractor, eval_transforms, active_device)
        emb_t2 = extract_latent_embeddings(image_t2, extractor, eval_transforms, active_device)
        
        similarity_score = float(np.dot(emb_t1, emb_t2) / (np.linalg.norm(emb_t1) * np.linalg.norm(emb_t2) + 1e-8))
        change_detected = similarity_score < sim_threshold

    # Clean Responsive Metrics Cards
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="T1 Land-Use Classification", value=class_t1, delta=f"{conf_t1*100:.1f}% Confidence")
    with m_col2:
        st.metric(label="T2 Land-Use Classification", value=class_t2, delta=f"{conf_t2*100:.1f}% Confidence")
    with m_col3:
        status_label = "Anomaly Detected" if change_detected else "Terrain Stable"
        st.metric(
            label="Cosine Vector Alignment", 
            value=f"{similarity_score:.4f}", 
            delta=status_label, 
            delta_color="inverse" if change_detected else "normal"
        )
        
    # Spatial Mapping & Telemetry Grid (Compact View)
    st.markdown("---")
    h_col1, h_col2 = st.columns([1.5, 2.5])
    
    with h_col1:
        st.markdown("### 🔍 System Diagnostics")
        if change_detected:
            st.error("Anomaly Alert: Significant land cover modification or architectural shift verified between target intervals.")
        else:
            st.success("Verification Confirmed: Optimal vector covariance. No structural divergence detected.")
            
        st.markdown(f"""
        **Telemetry Specifications:**
        * **Vector Alignment Score:** `{similarity_score:.4f}`
        * **Target Trigger Limit:** `{sim_threshold:.4f}`
        * **Divergence Margin:** `{abs(similarity_score - sim_threshold):.4f}`
        """)
        
    with h_col2:
        st.markdown("### 🗺️ Spatial Deviation Heatmap")
        heatmap_mask = generate_differential_heatmap(image_t1, image_t2)
        
        # Downsized Matplotlib Plot for modern fit
        fig, ax = plt.subplots(figsize=(5, 3))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        
        im = ax.imshow(heatmap_mask, cmap='inferno')
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cb.set_label("Deviation Scale", color="white", fontsize=8)
        cb.ax.yaxis.label.set_color('white')
        cb.ax.tick_params(labelsize=7, colors='white')
        
        ax.axis('off')
        
        st.pyplot(fig, bbox_inches='tight', transparent=True)
        plt.close(fig)
else:
    st.markdown("---")
    st.info("System Ready: Awaiting PNG, JPG, or GeoTIFF tracking sequences. Please upload both matrices to initialize diagnostics.")