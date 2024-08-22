# local parser
import aiohttp
import asyncio
from config.db import database

BASE_URL = 'https://api.github.com'
URL_TOP_100 = '/search/repositories?q=stars:>1&sort=stars&order=desc&per_page=100'



async def fetch_repo_data(session):
    result = []
    async with session.get(BASE_URL + URL_TOP_100) as response:
        data = await response.json()
    for position, repo in enumerate(data['items'], start=1):
        full_name = repo['full_name']
        owner = repo.get("owner")['login']
        position_cur = position
        position_prev = position
        stars = repo['stargazers_count']
        watchers = repo['watchers_count']
        forks = repo['forks_count']
        open_issues = repo['open_issues_count']
        language = repo.get('language')
        result.append(
            {
                "repo": full_name,
                "owner": owner,
                "position_cur": position_cur,
                "position_prev": position_prev,
                "stars": stars,
                "watchers": watchers,
                "forks": forks,
                "open_issues": open_issues,
                "language": language
            }
        )
    return result


async def update_db_with_repo_data(repo_data):
    query = """
        INSERT INTO repo (repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language)
        VALUES (:repo, :owner, :position_cur, :position_prev, :stars, :watchers, :forks, :open_issues, :language)
        ON CONFLICT (repo) DO UPDATE SET
        position_cur = excluded.position_cur,
        position_prev = repo.position_cur,
        stars = excluded.stars,
        watchers = excluded.watchers,
        forks = excluded.forks,
        open_issues = excluded.open_issues,
        language = excluded.language
        """
    await database.execute(query, repo_data)


async def main():
    await database.connect()
    async with aiohttp.ClientSession() as session:

        data = await fetch_repo_data(session)
        for repo_data in data:
            await update_db_with_repo_data(repo_data)
    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
