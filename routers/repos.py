from datetime import datetime
from typing import List

from fastapi import APIRouter
from schemas.repos import Repo, ReposActivity
from services.repos_service import get_top_100_repos, get_activity, get_active_from_db

router = APIRouter(prefix="/api/repos", tags=["repos"])


@router.get("/top100", response_model=List[Repo])
async def get_top100():
    results = await get_top_100_repos()
    return [Repo(**repo) for repo in results]


@router.get("/{owner}/{repo}/activity")
async def get_repo_activity(repo: str, owner: str,
                            since: datetime = None, until: datetime = None) -> List[ReposActivity]:
    repos_data = await get_active_from_db(repo, owner, since, until)
    return [ReposActivity(**repos) for repos in repos_data]

