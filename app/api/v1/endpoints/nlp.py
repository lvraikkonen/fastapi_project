import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.schemas.query import QueryRequest, QueryResponse
from app.services.nlp import process_nlp_query_with_db
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_PATH")

router = APIRouter()


@router.post("/nlp_query", response_model=QueryResponse)
def nlp_query_endpoint(request: QueryRequest, db: AsyncSession = Depends(get_db_session)):
    try:
        result = process_nlp_query_with_db(request.query, DATABASE_URL)
        logger.info(f"get the result: {result}")
        return QueryResponse(result=result)
    except Exception as e:
        logger.error(f"Error in NLP query endpoint: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
