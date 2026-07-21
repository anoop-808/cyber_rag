from app.retrieval.vector_store import get_vector_store

collection = get_vector_store()

print(type(collection))
print(collection.name)