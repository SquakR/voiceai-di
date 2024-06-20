from typing import Annotated

from fastapi import Depends, FastAPI

from .container import Container
from .use_cases import SumUseCaseProtocol

app = FastAPI()


@app.get('/sum')
async def root(
    a: int, sum_use_case: Annotated[SumUseCaseProtocol, Depends(Container.sum_use_case)]
):
    return await sum_use_case(a)
