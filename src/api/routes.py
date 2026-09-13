from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.concurrency import run_in_threadpool
from src.api.schemas import AskRequest, AskResponse
from src.services.qa_service import answer_question, stream_answer_question

router = APIRouter(prefix="/api/v1", tags=["RAG Q&A"])


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    try:
        result = await run_in_threadpool(
            answer_question, query=req.question, top_k=req.top_k
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask/stream")
def ask_stream(req: AskRequest):
    token_generator = stream_answer_question(query=req.question, top_k=req.top_k)
    return StreamingResponse(token_generator, media_type="text/event-stream")
