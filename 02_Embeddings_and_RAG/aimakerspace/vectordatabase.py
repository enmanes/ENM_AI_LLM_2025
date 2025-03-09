import numpy as np
from collections import defaultdict
from typing import List, Tuple, Callable
from aimakerspace.openai_utils.embedding import EmbeddingModel
import asyncio
<<<<<<< HEAD
import time
=======
>>>>>>> 1b963e52d261b1851b7c8927b6607b7fc9ab2f54


def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)


class VectorDatabase:
    def __init__(self, embedding_model: EmbeddingModel = None):
        self.vectors = defaultdict(np.array)
        self.embedding_model = embedding_model or EmbeddingModel()
<<<<<<< HEAD
        #ENM added following line
        #self.batch_size = batch_size
=======
>>>>>>> 1b963e52d261b1851b7c8927b6607b7fc9ab2f54

    def insert(self, key: str, vector: np.array) -> None:
        self.vectors[key] = vector

    def search(
        self,
        query_vector: np.array,
        k: int,
        distance_measure: Callable = cosine_similarity,
    ) -> List[Tuple[str, float]]:
        scores = [
            (key, distance_measure(query_vector, vector))
            for key, vector in self.vectors.items()
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:k]

    def search_by_text(
        self,
        query_text: str,
        k: int,
        distance_measure: Callable = cosine_similarity,
        return_as_text: bool = False,
    ) -> List[Tuple[str, float]]:
        query_vector = self.embedding_model.get_embedding(query_text)
        results = self.search(query_vector, k, distance_measure)
        return [result[0] for result in results] if return_as_text else results

    def retrieve_from_key(self, key: str) -> np.array:
        return self.vectors.get(key, None)

    async def abuild_from_list(self, list_of_text: List[str]) -> "VectorDatabase":
        embeddings = await self.embedding_model.async_get_embeddings(list_of_text)
        for text, embedding in zip(list_of_text, embeddings):
            self.insert(text, np.array(embedding))
        return self
<<<<<<< HEAD
    # SYNC VERSION ADDED BY ENM - ADDED THE FOLLOWING BLOCK OF CODE TO MAKE THE CODE WORK WITH THE ASSIGNMENT
    def build_from_list(self, list_of_text: List[str]) -> "VectorDatabase":
        embeddings = self.embedding_model.get_embeddings(list_of_text)
        for text, embedding in zip(list_of_text, embeddings):
            self.insert(text, np.array(embedding))
        return self
    
    #def build_from_list(self, list_of_text: List[str]) -> "VectorDatabase":
        # Process documents in batches
     #   for i in range(0, len(list_of_text), self.batch_size):
      ##      batch = list_of_text[i:i + self.batch_size]
       #     embeddings = self.embedding_model.get_embeddings(batch)
            
       #     for text, embedding in zip(batch, embeddings):
       #         self.insert(text, np.array(embedding))
            
            # Add a small delay between batches to respect rate limits
       #     time.sleep(1)

        #return self
=======
>>>>>>> 1b963e52d261b1851b7c8927b6607b7fc9ab2f54


if __name__ == "__main__":
    list_of_text = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]
<<<<<<< HEAD
# ENM COMMENTED THE ASYNC METHOD BELOW AND ADDED THE SYNC METHOD
    #vector_db = VectorDatabase()
    #vector_db = asyncio.run(vector_db.abuild_from_list(list_of_text))
    #k = 2

# ENM ADDED THE FOLLOWING BLOCK OF CODE TO MAKE THE CODE WORK WITH THE ASSIGNMENT- SYNC VERSION
# LIKELY WANT TO USE THE ASYNC VERSION TO PROCESS FASTER
    vector_db = VectorDatabase() 
    BATCH_SIZE = 20  # Adjust this based on your rate limits
    for i in range(0, len(list_of_text), BATCH_SIZE):
        batch = list_of_text[i:i + BATCH_SIZE]
        vector_db = vector_db.build_from_list(batch)
        # Add a small delay between batches to respect rate limits
        time.sleep(1) 
    k=2 # ENM ADDED NOT SURE IF THIS IS NEEDED
=======

    vector_db = VectorDatabase()
    vector_db = asyncio.run(vector_db.abuild_from_list(list_of_text))
    k = 2
>>>>>>> 1b963e52d261b1851b7c8927b6607b7fc9ab2f54

    searched_vector = vector_db.search_by_text("I think fruit is awesome!", k=k)
    print(f"Closest {k} vector(s):", searched_vector)

    retrieved_vector = vector_db.retrieve_from_key(
        "I like to eat broccoli and bananas."
    )
    print("Retrieved vector:", retrieved_vector)

    relevant_texts = vector_db.search_by_text(
        "I think fruit is awesome!", k=k, return_as_text=True
    )
    print(f"Closest {k} text(s):", relevant_texts)
