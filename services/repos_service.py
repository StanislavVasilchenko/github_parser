import aiohttp

from config.db import database
from services.parser import BASE_URL
from datetime import datetime


async def get_top_100_repos():
    """Выбор из БД топ 100 репозиториев по кол-ву коммитов"""
    query = """
    SELECT * FROM repo
    ORDER BY stars DESC, id ASC
    LIMIT 100
    """
    results = await database.fetch_all(query=query)
    return results


async def get_activity(owner, repos, since, until):
    """Парсер активности репозитория"""
    URL_ACTIVITY = BASE_URL + f"/repos/{owner}/{repos}/commits"
    if since is not None and until is not None:
        URL_ACTIVITY = BASE_URL + (f"/repos/{owner}/{repos}/commits"
                                   f"?since={since}&until={until}")
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_ACTIVITY) as response:
            data = await response.json()
    for repo in data:
        owner = owner
        repo_name = repos
        date = datetime.fromisoformat(repo["commit"]["author"]["date"].replace('Z', '+00:00'))
        author = repo["commit"]["author"]["name"]
        query = """
        INSERT INTO activity (repo_name, owner, date, author)
        VALUES (:repo_name, :owner, :date, :author)"""
        data = {"repo_name": repo_name, "owner": owner, "date": date, "author": author}
        await database.execute(query=query, values=data)


async def get_active_from_db(repo_name, owner, since, until):
    query = """
    SELECT date, COUNT(*) as commits, array_agg(distinct(author)) as author
    FROM activity
    WHERE repo_name = :repo_name AND owner = :owner  AND date BETWEEN :since AND :until
    GROUP BY date
    ORDER BY date;"""

    res = await database.fetch_all(query=query, values={"repo_name": repo_name, "owner": owner,
                                                        "since": since, "until": until})

    return res
