from app.retrieval.embeddings import get_embedding_model

model = get_embedding_model()

print(type(model))
print(model)