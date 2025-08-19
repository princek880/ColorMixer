import streamlit as st
import numpy as np
from PIL import Image
from scipy.optimize import nnls

st.title("Flexible Color Mixer App")

st.markdown("""
This app computes non-negative proportions of up to **5 base colors** that best approximate a target color.  
You can either **upload images** or **manually enter RGB values** for the base and target colors.  
At least **3 base colors** are required.
""")

# --- Function to get average RGB from image ---
def get_average_rgb(uploaded_file):
    if uploaded_file is None:
        return None
    image = Image.open(uploaded_file).convert("RGB")
    arr = np.array(image)
    avg = arr.reshape(-1, 3).mean(axis=0)
    return avg.astype(int)

# --- Input mode selection ---
mode = st.radio("Select input mode", ["Upload Images", "Enter RGB Values"])

base_rgbs = []
target_rgb = None

if mode == "Upload Images":
    st.header("Upload Base Color Images (up to 5)")
    base_uploads = []
    for i in range(5):
        file = st.file_uploader(f"Upload Base Color {i+1}", type=["png","jpg","jpeg"])
        base_uploads.append(file)
    base_rgbs = [get_average_rgb(f) for f in base_uploads if f is not None]

    st.header("Upload Target Color Image")
    target_upload = st.file_uploader("Upload Target Color", type=["png","jpg","jpeg"])
    if target_upload:
        target_rgb = get_average_rgb(target_upload)

else:  # Enter RGB Values
    st.header("Enter Base RGB Values (up to 5, min 3)")
    for i in range(5):
        r = st.number_input(f"Base Color {i+1} - R", min_value=0, max_value=255, value=0, key=f"r{i}")
        g = st.number_input(f"Base Color {i+1} - G", min_value=0, max_value=255, value=0, key=f"g{i}")
        b = st.number_input(f"Base Color {i+1} - B", min_value=0, max_value=255, value=0, key=f"b{i}")
        if (r,g,b) != (0,0,0):  # avoid dummy all-zero entries
            base_rgbs.append([r,g,b])

    st.header("Enter Target RGB Value")
    tr = st.number_input("Target - R", min_value=0, max_value=255, value=0, key="tr")
    tg = st.number_input("Target - G", min_value=0, max_value=255, value=0, key="tg")
    tb = st.number_input("Target - B", min_value=0, max_value=255, value=0, key="tb")
    target_rgb = [tr, tg, tb]

# --- Compute proportions ---
if st.button("Compute Proportions"):
    if target_rgb is None:
        st.error("Provide a target color (image or RGB values).")
    elif len(base_rgbs) < 3:
        st.error("Provide at least 3 base colors.")
    else:
        A = np.array(base_rgbs).T  # shape (3, n_colors)
        b = np.array(target_rgb)

        coeffs, _ = nnls(A, b)

        if coeffs.sum() == 0:
            st.warning("No valid non-negative solution found.")
        else:
            proportions = coeffs / coeffs.sum()
            st.subheader("Results")
            for i, p in enumerate(proportions):
                st.write(f"Base Color {i+1}: {p:.3f}")
            st.write("Proportions sum:", proportions.sum())
