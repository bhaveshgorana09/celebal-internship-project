## Satellite Image Land-Use Classifier & Temporal Change Detector

A production-grade, modular computer vision system built using PyTorch, Torchvision, Streamlit, and OpenCV to classify satellite imagery into land-use categories and track structural environmental variations over time.

The system leverages deep transfer learning for robust categorical representation alongside embedding-based distance metrics to detect macro-temporal landscape modifications without requiring dense pixel-level ground truth segmentation masks. The architecture is fully optimized for GPU acceleration, executing dynamically with absolute dependency sandboxing on local environments.

---

## Features

-Geospatial Block Partitioning: Implements a robust Spatial Block Split data pipeline to process continuous geographical flight tracks, completely eliminating spatial autocorrelation and downstream validation data leakage
-Multi-Phase Optimization Floor: Establishes a highly efficient 3-layer Convolutional Neural Network baseline trained from scratch to act as a project-wide performance floor.
-Two-Phase Fine-Tuning Engine: Implements a targeted transfer learning strategy using a pre-trained ResNet-18 backbone—freezing early layers before fine-tuning the deep convolutional layers with a $10\times$ reduced learning rate.
-Embedding-Based Change Detector: Strips away the categorical classification layer to output high-fidelity 512-dimensional vector representations, applying pair-wise Cosine Similarity matrices and optimized ROC threshold cutoffs to identify landscape anomalies.
-Interactive Geo-Dashboard: Deploys a beautiful, responsive Single Page Application UI via Streamlit that supports multi-temporal dual image uploads, real-time category inference, and spatial difference heatmap masks.

---

## 🖼️ Project Previews & Visual Analytics

### 1. Geo-Dashboard Application Interface
The central data orchestration platform interface built with Streamlit, managing dynamic data frames, operational parameter sliders, and parallel deep-learning pipelines locally.

<img src="assets/Dashboard Platform.png" alt="Geo-Dashboard Interface" width="100%" />

---

### 2. Multi-Temporal Target Frame Ingestion
Sample input pairing showing a standard operational ingestion pipeline where time period $T_1$ (Before) and time period $T_2$ (After) frames are structured through identical geographical bounds.

<img src="assets/T1 and T2 Frame.png" alt="Multi-Temporal Target Frames" width="100%" />

---

### 4. Steady-State Baseline Verification
Analytical sample demonstrating system state consistency when input tracks remain structurally invariant across temporal monitoring checkpoints.

<img src="assets/No change in Image.png" alt="No Change Baseline Verification" width="100%" />

---

### 3. Structural Land-Use Modification Diagnostics
Comparative visual analysis when mismatched or transformed categories are detected. The engine maps the spatial differential and highlights precise environmental variations using a structural deviation heatmap layer.

#### A. Different Image Inputs (Mismatched Categories)
<img src="assets/Different Image T1 and T2.png" alt="Different Image Input Verification" width="100%" />

#### B. Resulting Anomaly Heatmap Output (Change Detected)
<img src="assets/Change in Heatmap.png" alt="Structural Change Deviation Heatmap" width="100%" />





---

## Directory Structure

```text
satellite_change_detection/
│
├── models/
│   └── baseline_cnn_checkpoint.pt     # Serialized PyTorch baseline weights (.pt)
│   └── resnet18_eurosat_finetuned.pt  # Serialized fine-tuned ResNet-18 weights (.pt)
├── notebooks/
│   ├── Main.ipynb                     # Step 1 to 4 (Module)
├── src/
│   ├── __init__.py                    # Python namespace package declaration
│   ├── dataset.py                     # Spatial dataset classes & patch loaders
│   ├── models.py                      # Baseline CNN & Embedding Extractor networks
│   └── utils.py                       # Cosine similarity engines & heatmap processors
├── app.py                             # Interactive user Streamlit Geo-Dashboard
└── requirements.txt                   # Project environment dependencies manifest
```

---

## Tech Stack

| Technology | Purpose |
|:---|:---|
| **PyTorch** | Open-source machine learning framework for deep learning, tensor operations, and computer vision tasks. |
| **Torchvision** | Provides datasets, image transformations, data augmentation, and pre-trained computer vision models. |
| **Streamlit** | Fast Python framework for building interactive web-based machine learning dashboards and applications. |
| **NumPy & Pandas** | Efficient numerical computing, data manipulation, preprocessing, and dataset management. |
| **Matplotlib & Seaborn** | Data visualization libraries used for plotting training metrics, confusion matrices, and performance analysis. |
| **Pillow (PIL)** | Image processing library for loading, resizing, converting, and manipulating image files. |

---

## Deep Learning & Detection Architecture

The complete image land-use categorization and change detection system is built around a unified mathematical extraction engine.
```text
[Time Frame T1 Tile]                  [Time Frame T2 Tile]
           │                                     │
           ▼                                     ▼
┌──────────────────────┐              ┌──────────────────────┐
│  ResNet-18 Backbone  │              │  ResNet-18 Backbone  │
│  (Weights: EuroSAT)  │              │  (Weights: EuroSAT)  │
└──────────┬───────────┘              └──────────┬───────────┘
           │                                     │
           │ (Strips Classification Head)        │ (Strips Classification Head)
           ▼                                     ▼
┌──────────────────────┐              ┌──────────────────────┐
│ 512-D Latent Vector  │              │ 512-D Latent Vector  │
│    Embedding (v1)    │              │    Embedding (v2)    │
└──────────┬───────────┘              └──────────┬───────────┘
           │                                     │
           └──────────────────┬──────────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │    Cosine Similarity Unit    │
               │   v1 ∙ v2 / (||v1|| ||v2||)  │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │   Anomaly Threshold Engine   │
               │ Is Similarity < Cutoff (0.885)│
               └──────────────┬───────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
   [🔴 CHANGE DETECTED]               [🟢 SYSTEM STABLE]
(Generates Jet Deviation Mask)       (Invariance Verified)
```

---

## Quick Start & Installation (Step-by-Step)

Follow these steps to set up and execute the project locally on Windows:

### 1. Open Terminal and Navigate to Project Folder
Open PowerShell or Command Prompt and enter your working directory path:
```powershell
cd D:\Celebal\satellite-change-detection
```

### 2. Create the Virtual Environment
Initialize a clean, isolated virtual python execution environment:
```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment
Activate the environment structure to sandbox code dependencies.
```powershell   
venv\Scripts\Activate.ps1
``` 

```Command Prompt 
venv\Scripts\activate.bat 
```


### 4. Install Dependencies
Install all necessary deep learning and visualization dependencies. Setting num_workers=0 inside the data loaders avoids multi-threading deadlocks common on Windows architectures:

```powershell 
python -m pip install -r requirements.txt
```  

### 5. Execute Training Notebooks
Open your VS Code workspace editor, access the notebooks/ folder, and execute the files sequentially (01 through 04). This creates the partitioned dataset streams, evaluates the scratch CNN floor, runs the two-phase fine-tuning model, and saves the optimized network checkpoint into the models/ folder[cite: 1].

### 6. Launch the Local Geo-Dashboard App
Run the local production web dashboard instance by executing the following terminal command:

```powershell 
streamlit run app.py
```
The application will launch immediately inside your default web browser tracking interface at http://localhost:8501[cite: 1].

---

## Running the Application

1. Open your web browser and navigate to http://localhost:8501.
Interactive Geo-Dashboard UI: Open your web browser and visit http://localhost:8501 (or the network URL provided in your terminal). This opens the single-page web interface where you can select detection thresholds, upload temporal image pairs, and view instant tracking diagnostics.

2. Upload Multi-Temporal Satellite Images: Use the file upload buttons to select two satellite images captured at different time frames (T1 and T2). Ensure that the images are of the same geographical region for accurate change detection.
Local Vector Diagnostics: The application interface allows you to benchmark classification changes, dynamically shift operating precision toggles, and actively generate multi-spectral disparity heatmaps in real-time.

---

## Verification & Testing

To execute automated unit and integration tests across the modular architecture (covering spatial dataloaders, model weight dimension states, embedding extraction vector verification, and mathematical cosine calculation boundaries):

```powershell 
python -m pytest test_main.py -v
```
 
---

## References

### Modular Data Handling (src/dataset.py)

1. [EuroSAT Dataset](load_eurosat_spatial_splits(data_dir, train_ratio, val_ratio): Iterates across alphabetically sorted continuous image folders to extract geographic tracking lists, entirely preventing spatial autocorrelation leakage)

2. SpatialEuroSATDataset(file_list, transform): Custom PyTorch dataset structure to apply geometric variations and color jitters to imagery during training[cite: 1].

### Model Architecture (src/models.py)

1. BaselineCNN: A 3-layer convolutional neural network trained from scratch to establish a performance floor for land-use classification tasks.
2. ResNet-18 Fine-Tuning: A pre-trained ResNet-18 model adapted for the EuroSAT dataset, with early layers frozen and deep convolutional layers fine-tuned for improved classification accuracy.
3. Embedding Extraction: The classification head is removed to output 512-dimensional latent vector embeddings for change detection.
4. Cosine Similarity Calculation: Computes the cosine similarity between embeddings from two time frames to quantify landscape changes. 
5. Anomaly Thresholding: Applies a predefined threshold to the cosine similarity score to determine if significant changes have occurred between the two time frames.   
6. Heatmap Generation: Generates visual heatmaps to represent areas of change based on the cosine similarity scores.

### Geoprocessing Math (src/utils.py)

1. Cosine Similarity Function: Implements the mathematical formula for cosine similarity between two vectors.
2. Heatmap Generation Function: Creates heatmaps based on the cosine similarity scores to visualize areas of change in the satellite images.
3. Thresholding Function: Applies a threshold to the cosine similarity scores to classify areas as changed or unchanged.
4. Visualization Utilities: Functions for plotting and visualizing the results, including heatmaps and classification outputs.
5. Performance Metrics: Functions to calculate and display performance metrics such as accuracy, precision, recall, and F1-score for the classification tasks.
6. Data Augmentation Utilities: Functions to apply data augmentation techniques such as rotation, flipping, and color jittering to the satellite images during training.
7. Model Saving and Loading Utilities: Functions to save and load model weights, including the baseline CNN and fine-tuned ResNet-18 models.
8. Logging and Debugging Utilities: Functions to log training progress, model performance, and any errors encountered during execution for easier debugging and analysis.
9. compute_cosine_similarity(v1, v2): Evaluates the mathematical cosine vector distance between two latent arrays to track ground transformations.
10. generate_heatmap(similarity_matrix): Generates a heatmap visualization based on the cosine similarity matrix to highlight areas of change between two time frames.

---

## Future Enhancements

1. **Multi-Temporal Analysis**: Extend the system to handle more than two time frames, allowing for continuous monitoring of land-use changes over extended periods.
2. **Integration with GIS Platforms**: Enable direct integration with Geographic Information System (GIS) platforms for enhanced spatial analysis and visualization.
3. **Real-Time Change Detection**: Implement real-time processing capabilities to analyze satellite imagery as it is received, providing immediate insights into land-use changes.
4. **Advanced Anomaly Detection**: Incorporate more sophisticated anomaly detection algorithms, such as clustering or deep learning-based approaches, to improve the accuracy of change detection.
5. **User Authentication and Data Management**: Add user authentication features and data management capabilities to allow multiple users to securely upload and analyze their own satellite imagery datasets.
6. **Cloud Deployment**: Deploy the application on cloud platforms to enable remote access and scalability for larger datasets and multiple users.
7. **Enhanced Visualization Tools**: Develop additional visualization tools, such as 3D terrain models and interactive maps, to provide more comprehensive insights into land-use changes.
8. **Automated Reporting**: Implement automated reporting features that generate summaries and visualizations of detected changes for stakeholders and decision-makers.
9. **Support for Additional Satellite Datasets**: Expand the system to support a wider range of satellite imagery datasets, including higher resolution and multi-spectral images, to improve classification and change detection capabilities.
