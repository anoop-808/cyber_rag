from app.ingestion.loader import load_json_dataset

data = load_json_dataset(
    "storage/datasets/raw/nvd_cves.json"
)

print(type(data))

if isinstance(data, dict):
    print("Keys:")
    print(data.keys())