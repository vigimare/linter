import io

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException, UploadFile

from linter import Linter  # type: ignore
from linter.exceptions import LinterSuccess  # type: ignore

app = FastAPI()
api_router = APIRouter(prefix="/api/v1")

linter = Linter()


@api_router.get("/health")
async def health():
    return {"status": "ok"}


@api_router.post("/validate-file")
async def validate(file: UploadFile):
    try:
        contents = await file.read()
        text_io = io.StringIO(contents.decode("utf-8"))
        result = linter.validate(text_io)
        if isinstance(result, LinterSuccess):
            return {"status": str(result)}
        else:
            raise HTTPException(status_code=400, detail=str(result).replace("\n", ""))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
