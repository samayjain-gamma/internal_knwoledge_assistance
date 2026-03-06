from fastapi import APIRouter, Depends

from src.app.deps import get_graph

router = APIRouter()


@router.post("/chat")
async def chat(request: str, graph=Depends(get_graph)):

    result = graph.invoke({})
