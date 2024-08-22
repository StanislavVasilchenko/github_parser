from typing import List
from pydantic import BaseModel
from datetime import datetime


class Repo(BaseModel):
    id: int
    repo: str
    owner: str
    position_cur: int
    position_prev: int
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str | None


class ReposActivity(BaseModel):
    date: datetime
    commits: int
    author: List[str]
