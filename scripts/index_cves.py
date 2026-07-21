"""Script to index processed CVEs into ChromaDB."""

import json
from pathlib import Path
from typing import Any, Dict, List

from app.retrieval.embeddings import get_embedding_model
from app.retrieval.vector_store import get_vector_store

BATCH_SIZE: int = 100


def main() -> None:
    """Load processed CVEs and index them into ChromaDB in batches."""
    processed_file = Path("storage/datasets/processed/processed_cves.json")
    if not processed_file.exists():
        print(f"Error: {processed_file} not found.")
        return

    with processed_file.open("r", encoding="utf-8") as f:
        cves: List[Dict[str, Any]] = json.load(f)

    model = get_embedding_model()
    collection = get_vector_store()

    # Clear existing collection contents to avoid duplicate ID errors
    existing_data = collection.get(include=[])
    existing_ids = existing_data.get("ids", [])
    if existing_ids:
        for i in range(0, len(existing_ids), BATCH_SIZE):
            collection.delete(ids=existing_ids[i:i + BATCH_SIZE])

    indexed_count: int = 0

    batch_ids: List[str] = []
    batch_descriptions: List[str] = []
    batch_metadatas: List[Dict[str, Any]] = []

    print(f"Indexing {len(cves)} CVEs...")

    for cve in cves:
        cve_id = cve.get("id")
        description = cve.get("description")

        if not cve_id or not description:
            continue

        metadata: Dict[str, Any] = {}
        if cve.get("published") is not None:
            metadata["published"] = str(cve.get("published"))
        if cve.get("last_modified") is not None:
            metadata["last_modified"] = str(cve.get("last_modified"))
        if cve.get("cvss_score") is not None:
            metadata["cvss_score"] = float(cve.get("cvss_score"))

        batch_ids.append(cve_id)
        batch_descriptions.append(description)
        batch_metadatas.append(metadata)

        if len(batch_ids) >= BATCH_SIZE:
            # Generate embeddings in a single batch
            batch_embeddings = model.encode(batch_descriptions).tolist()

            collection.add(
                ids=batch_ids,
                documents=batch_descriptions,
                embeddings=batch_embeddings,
                metadatas=batch_metadatas
            )
            indexed_count += len(batch_ids)

            batch_ids.clear()
            batch_descriptions.clear()
            batch_metadatas.clear()

    # Process remaining items in the last batch
    if batch_ids:
        batch_embeddings = model.encode(batch_descriptions).tolist()
        collection.add(
            ids=batch_ids,
            documents=batch_descriptions,
            embeddings=batch_embeddings,
            metadatas=batch_metadatas
        )
        indexed_count += len(batch_ids)

    print(f"Number of indexed CVEs: {indexed_count}")
    print(f"Collection name: {collection.name}")


if __name__ == "__main__":
    main()
