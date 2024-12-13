import uuid
from typing import List, Optional
import logging

from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


logger = logging.getLogger(__name__)

class VectorInput(BaseModel):
    vector: List[float]
    payload: dict

class VectorDBClient():
    def __init__(
        self, 
        url: str, 
        collection_name: str,
        vector_size: Optional[int],
    ):
        self.client = QdrantClient(url=url)

        self.collection_name = collection_name
        if not self.client.collection_exists(collection_name=collection_name):
            if not self.create_collection(collection_name, vector_size): 
                raise ValueError("Error creating collection")
            
    def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance: Distance = Distance.COSINE
    ) -> bool:
        '''
        Create a new collection.

        Parameters:
            collection_name: str
            vector_size: int
            distance: Distance = Distance.COSINE
        '''
        return self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )

    def delete_vector(self, vector_id: uuid.UUID | str):
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
        top_k: int = 5, 
        with_payload: bool = True
    ) -> List:
        '''
        Search for vectors similar to one provided.

        Parameters:
            vector: List[float]
            top_k: int = 5
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
        vector_id: uuid.UUID | str, 
        top_k: int, 
        with_payload: bool = True
    ) -> List:
        '''
        Search for a vector by id.

        Parameters:
            vector_id: UUID | str
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

    def upsert_vector(self, vector_input: VectorInput):
        '''
        Insert or update a vector.

        Parameters:
            vector: VectorInput
        '''
        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=[
                PointStruct(
                    id = uuid.uuid4(),
                    payload = vector_input.payload,
                    vector = vector_input.vector
                )
            ]
        )

    # TODO: Create batch upsert method
    def upsert_vectors(self, vectors: List[VectorInput]):
        '''
        Insert or update a vector.

        Parameters:
            vectors: List[VectorInput]
        '''
        points_list = []
        for i in vectors:
            points_list.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    payload=i.payload,
                    vector=i.vector
                )
            )
        
        return self.client.upsert(
            collection_name = self.collection_name,
            wait = True,
            points = points_list
        )
