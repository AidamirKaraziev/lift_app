import logging
# from fastapi import APIRouter, Depends, Header, Request, UploadFile, File, Query
from fastapi import APIRouter

router = APIRouter()


@router.get("/test-2/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    logging.info('Running...')
