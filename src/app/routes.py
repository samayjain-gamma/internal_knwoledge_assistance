from fastapi import APIRouter, Depends

from src.app.deps import get_graph

router = APIRouter()


@router.post("/chat")
async def chat(graph=Depends(get_graph)):

    result = graph.invoke({})

    return result.get("generated_answer")
