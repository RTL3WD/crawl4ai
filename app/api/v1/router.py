from fastapi import APIRouter
from app.api.v1.endpoints import extraction, docs, cache, multi, human_docs, basic, content

router = APIRouter()
router.include_router(basic.router, prefix="/crawl", tags=["crawl"])
router.include_router(content.router, prefix="/crawl", tags=["crawl"])
router.include_router(extraction.router, prefix="/crawl", tags=["crawl"])
router.include_router(docs.router, tags=["documentation"])
router.include_router(cache.router, prefix="/crawl", tags=["crawl"])
router.include_router(multi.router, prefix="/crawl", tags=["crawl"])
router.include_router(human_docs.router, tags=["documentation"]) 