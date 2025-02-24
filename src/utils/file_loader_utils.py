import os
import streamlit as st

def save_uploaded_files(uploaded_files, target_dir):
    """Save uploaded files to the target directory and return their paths."""
    os.makedirs(target_dir, exist_ok=True)
    saved_paths = []
    for file in uploaded_files:
        file_path = os.path.join(target_dir, file.name)
        try:
            with open(file_path, "wb") as f:
                f.write(file.read())
            st.success(f"File '{file.name}' saved successfully at {file_path}.")
            saved_paths.append(file_path)
        except Exception as e:
            st.error(f"Error saving file '{file.name}': {e}")
    return saved_paths


def cleanup_files(file_paths):
    """Remove files from disk based on their paths."""
    for file_path in file_paths:
        try:
            os.remove(file_path)
            st.info(f"Removed file: {file_path}")
        except Exception as e:
            st.error(f"Error removing file {file_path}: {e}")