## Satellite Image Land-Use Classifier & Temporal Change Detector

A production-grade, modular computer vision system built using PyTorch, Torchvision, Streamlit, and OpenCV to classify satellite imagery into land-use categories and track structural environmental variations over time.

The system leverages deep transfer learning for robust categorical representation alongside embedding-based distance metrics to detect macro-temporal landscape modifications without requiring dense pixel-level ground truth segmentation masks. The architecture is fully optimized for GPU acceleration, executing dynamically with absolute dependency sandboxing on local environments.

## Features

-Geospatial Block Partitioning: Implements a robust Spatial Block Split data pipeline to process continuous geographical flight tracks, completely eliminating spatial autocorrelation and downstream validation data leakage
-Multi-Phase Optimization Floor: Establishes a highly efficient 3-layer Convolutional Neural Network baseline trained from scratch to act as a project-wide performance floor.
-Two-Phase Fine-Tuning Engine: Implements a targeted transfer learning strategy using a pre-trained ResNet-18 backbone—freezing early layers before fine-tuning the deep convolutional layers with a $10\times$ reduced learning rate.
-Embedding-Based Change Detector: Strips away the categorical classification layer to output high-fidelity 512-dimensional vector representations, applying pair-wise Cosine Similarity matrices and optimized ROC threshold cutoffs to identify landscape anomalies.
-Interactive Geo-Dashboard: Deploys a beautiful, responsive Single Page Application UI via Streamlit that supports multi-temporal dual image uploads, real-time category inference, and spatial difference heatmap masks.

## Project Preview
#Interactive Geo-Dashboard Interface
A self-contained geospatial interface for uploading multi-temporal tracking tiles, reviewing category predictions, calculating vector distance indices, and rendering dynamic landscape variation heatmaps.


#Directory Structure
satellite_change_detection/
│
├── models/
│   └── baseline_cnn_checkpoint.pt     # Serialized PyTorch baseline weights (.pt)
│   └── resnet18_eurosat_finetuned.pt  # Serialized fine-tuned ResNet-18 weights (.pt)
├── notebooks/
│   ├── 01_data_pipeline.ipynb         # Spatial block partitioning split pipeline
│   ├── 02_baseline_cnn.ipynb          # Baseline 3-layer scratch CNN training
│   ├── 03_transfer_learning.ipynb     # Two-phase ResNet-18 fine-tuning routine
│   └── 04_change_detection.ipynb      # Embedding extraction and ROC cutoff tuning
├── src/
│   ├── __init__.py                    # Python namespace package declaration
│   ├── dataset.py                     # Spatial dataset classes & patch loaders
│   ├── models.py                      # Baseline CNN & Embedding Extractor networks
│   └── utils.py                       # Cosine similarity engines & heatmap processors
├── app.py                             # Interactive user Streamlit Geo-Dashboard
└── requirements.txt                   # Project environment dependencies manifest


## Tech Stack



## Deep Learning & Detection Architecture
The complete image land-use categorization and change detection system is built around a unified mathematical extraction engine.

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


##Quick Start & Installation (Step-by-Step)

Follow these steps to set up and execute the project locally on Windows:

#1. Open Terminal and Navigate to Project Folder

Open PowerShell or Command Prompt and enter your working directory path:

cd D:\Celebal\satellite-change-detection

#2. Create the Virtual Environment
Initialize a clean, isolated virtual python execution environment:

python -m venv venv

#3. Activate the Virtual Environment
Activate the environment structure to sandbox code dependencies.
-PowerShell:
venv\Scripts\Activate.ps1

-Command Prompt:
venv\Scripts\activate.bat

#4. Install Dependencies
Install all necessary deep learning and visualization dependencies. Setting num_workers=0 inside the data loaders avoids multi-threading deadlocks common on Windows architectures:

python -m pip install -r requirements.txt

#5. Execute Training Notebooks

Open your VS Code workspace editor, access the notebooks/ folder, and execute the files sequentially (01 through 04). This creates the partitioned dataset streams, evaluates the scratch CNN floor, runs the two-phase fine-tuning model, and saves the optimized network checkpoint into the models/ folder.


#6. Launch the Local Geo-Dashboard App

Run the local production web dashboard instance by executing the following terminal command:

The application will launch immediately inside your default web browser tracking interface at http://localhost:8501.

##API & Processing Reference

#Modular Data Handling (src/dataset.py)


-load_eurosat_spatial_splits(data_dir, train_ratio, val_ratio): Iterates across alphabetically sorted continuous image folders to extract geographic tracking lists, entirely preventing spatial autocorrelation leakage.
-SpatialEuroSATDataset(file_list, transform): Custom PyTorch dataset structure to apply geometric variations and color jitters to imagery during training.


#Neural Networks (src/models.py)
-FastBaselineCNN(num_classes): Lightweight 3-layer baseline CNN utilizing adaptive global downsampling to minimize the network parameter size.
-SpatialEmbeddingExtractor(checkpoint_path, device): Reconfigures the fine-tuned ResNet-18 model by converting the final linear layer into an Identity block to generate clean 512-dimensional feature maps



#Geoprocessing Math (src/utils.py)
-Compute_cosine_similarity(v1, v2): Evaluates the mathematical cosine vector distance between two latent arrays to track ground transformations.
-generate_differential_heatmap(img1, img2): Maps absolute pixel-level color variance across multi-temporal frames, producing a normalized 2D change heatmap.

##Future Enhancements
-Multi-Spectral Ingestion Support: Upgrade the data pipeline to support 13-band Sentinel-2 multi-spectral image bands, using near-infrared (NIR) data to track crop transformations regardless of seasonal lighting changes.
-Grad-CAM Saliency Overlay: Integrate Grad-CAM tracking directly into the dashboard interface to map and display the exact pixel clusters that drove each land-use prediction.
-Multi-Threshold Toggle Engine: Incorporate high-precision, balanced, and high-recall cutoff switches into the app sidebar, allowing users to dynamically adjust change detection sensitivity.
-Latent Space Embedding Maps: Project 512-dimensional land-use features into lower 2D coordinates using t-SNE or UMAP to generate side-by-side cluster visualizations for data drift verification.








