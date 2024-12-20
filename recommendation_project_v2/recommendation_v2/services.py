import pandas as pd
from recommendation_v2.models import Purchase

from sentence_transformers import SentenceTransformer, util
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')



def generate_product_embeddings():
    products = Product.objects.all()
    descriptions = [p.description for p in products]
    embeddings = model.encode(descriptions, convert_to_tensor=True)
    return products, embeddings

def recommend_products_for_user(user, purchase_history, product_embeddings):
    user_history = purchase_history.loc[user, :]
    purchased_products = user_history[user_history > 0].index.tolist()

    recommended = []
    for product in purchased_products:
        product_idx = purchase_history.columns.get_loc(product)
        similarity_scores = cosine_similarity(
            [product_embeddings[product_idx]],
            product_embeddings
        )
        similar_products = sorted(
            enumerate(similarity_scores[0]),
            key=lambda x: x[1],
            reverse=True
        )
        recommended.extend([product_embeddings[i] for i, _ in similar_products[:5]])

    return list(set(recommended))
