from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(embedding1, embedding2):
    score = cosine_similarity([embedding1], [embedding2])[0][0]
    return round(float(score) * 100, 2)