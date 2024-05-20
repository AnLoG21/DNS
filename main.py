# from fastapi import FastAPI
# import uvicorn
# from fastapi.routing import APIRouter
# from sqlalchemy import Column, Boolean, String
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base
# import settings
# from sqlalchemy.dialects.postgresql import UUID
# import uuid
# import re
# from fastapi import HTTPException
# from pydantic import BaseModel
# from pydantic import EmailStr
# from pydantic import validator
#
# from api.handlers import user_router
#
# app = FastAPI(title="Ekelmende")
#
#
#
#
#
#
#
#
#
#
#
# main_api_router = APIRouter()
# main_api_router.include_router(user_router, prefix="/user", tags=["user"])
# app.include_router(main_api_router)
#
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
#
