# Color Mixer App

A simple [Streamlit](https://streamlit.io) web app to experiment with digital color mixing.  
You upload three base color images, the app extracts their average RGB values, and then you upload a target color image.  
It computes the non-negative proportions of the three base colors needed to approximate the target color using non-negative least squares (NNLS).

## Features
- Upload three base color images (JPEG/PNG).
- Upload a target color image.
- Automatic extraction of average RGB values.
- Non-negative least squares solver ensures all mixing coefficients are >= 0.
- Proportions normalized to sum to 1.

## Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/<your-username>/color-mixer-app.git
cd color-mixer-app

# Using conda
conda create -n colormixer python=3.11
conda activate colormixer
conda install -c conda-forge streamlit numpy pillow scipy

# or with pip
pip install streamlit numpy pillow scipy
