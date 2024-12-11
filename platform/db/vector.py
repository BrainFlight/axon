import uuid
from uuid import UUID
from typing import List
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct


logger = logging.getLogger(__name__)

class VectorDBClient():
    def __init__(self, url: str, collection_name: str):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        if not self.client.collection_exists(collection_name=collection_name):
            if not self.create_collection(collection_name): 
                raise ValueError("Error creating collection")
            
    def create_collection(
        self,
        collection_name: str,
        vectors_config: VectorParams
    ) -> bool:
        '''
        Create a new collection.

        Parameters:
            collection_name: str
            vectors_config: VectorParams (optional)
        '''
        return self.client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config,
        )

    def delete_vector(self, vector_id: UUID | str):
        '''
        Delete a vector based on id.

        Parameters:
            vector_id: UUID | str
        '''
        self.client.delete(
            collection_name=self.collection_name,
            vector_id=str(vector_id),
        )

    def search_vectors(
        self, 
        vector: List[float], 
        top_k: int, 
        with_payload: bool = True
    ) -> List:
        '''
        Search for vectors similar to one provided.

        Parameters:
            vector: List[float]
            top_k: int
            with_payload: bool = True
        '''
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            with_payload=with_payload,
            with_vectors=True,
            limit=top_k
        )

        logger.info(search_result)
        #return search_result.points #, search_result.payload
    
    def search_vector_by_id(
        self, 
        vector_id: UUID | str, 
        top_k: int, 
        with_payload: bool = True
    ) -> List:
        '''
        Search for a vector by id.

        Parameters:
            vector_id: int
            top_k: int
            with_payload: bool = True
        '''
        return self.client.search_by_id(
            collection_name=self.collection_name,
            vector_id=vector_id,
            with_payload=with_payload,
            with_vectors=True,
            limit=top_k,
        )

    def upsert_vector(self, vector: List[float], payload: dict):
        '''
        Insert or update a vector.

        Parameters:
            vector: List[float]
            payload: dict
        '''
        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    payload=payload,
                    vector=[i/388 for i in range(384)] # vector
                )
            ]
        )

    # TODO: Create batch upsert method
