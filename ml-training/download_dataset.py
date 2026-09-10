from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="PINGEcosystem/sss-crab-pot-detection-ds",
    repo_type="dataset",
    local_dir="./dataset"
)

print("Download complete!")