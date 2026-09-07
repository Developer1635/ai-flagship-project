import os
from huggingface_hub import hf_hub_download

def install_best_local_model():
    repo_id = "bartowski/Qwen2.5-7B-Instruct-GGUF"
    filename = "Qwen2.5-7B-Instruct-Q4_K_M.gguf"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    target_path = os.path.join(models_dir, filename)
    
    if os.path.exists(target_path):
        print(f"[System]: Model is already installed at: {target_path}")
        return target_path

    print(f"[System]: Starting native Python installation for {filename}...")
    print("[System]: Downloading from Hugging Face (~4.68 GB). Please wait...")

    downloaded_file_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=models_dir,
        local_dir_use_symlinks=False
    )
    
    print(f"[System]: Installation successful! Model saved to: {downloaded_file_path}")
    return downloaded_file_path

if __name__ == "__main__":
    install_best_local_model()
