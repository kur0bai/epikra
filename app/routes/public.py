from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from app.functions import Functions

router = APIRouter()

@router.get("/public/qr")
def public_qr(content: str):
    try:
        functions = Functions()
        qr = functions.generate(content)
        return Response(content=qr.getvalue(), media_type="image/png")
    except Exception as ex:
        return {"error": f'Something went wrong: {ex}'}
