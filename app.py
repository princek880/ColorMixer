import streamlit as st
import numpy as np
from PIL import Image
from scipy.optimize import nnls

st.title("Color Mixing Proportion Finder")

st.write("Upload three base color images:")

# Upload 3 base images
col1_img = st.file_uploader("Upload Base Color 1", type=["png", "jpg", "jpeg"])
col2_img = st.file_uploader("Upload Base Color 2", type=["png", "jpg", "jpeg"])
col3_img = st.file_uploader("Upload Base Color 3", type=["png", "jpg", "jpeg"])

base_colors = []

for img_file in [col1_img, col2_img, col3_img]:
    if img_file:
        img = Image.open(img_file).convert("RGB")
        arr = np.array(img)
        avg_color = arr.mean(axis=(0, 1))  # Average RGB values
        base_colors.append(avg_color)

if len(base_colors) == 3:
    st.write("Base RGB values:")
    for i, col in enumerate(base_colors, 1):
        st.write(f"Color {i}: {col.astype(int)}")

    # Upload target image
    target_img_file = st.file_uploader("Upload Target Color Image", type=["png", "jpg", "jpeg"])

    if target_img_file:
        target_img = Image.open(target_img_file).convert("RGB")
        target_arr = np.array(target_img)
        target_color = target_arr.mean(axis=(0, 1))
        st.write(f"Target RGB: {target_color.astype(int)}")

        # Solve proportions using non-negative least squares
        A = np.array(base_colors).T  # 3x3 matrix
        b = target_color

        coeffs, _ = nnls(A, b)
        coeffs = coeffs / coeffs.sum() if coeffs.sum() > 0 else coeffs

        st.write("Proportions:")
        st.write({f"Color {i+1}": float(coeffs[i]) for i in range(3)})
