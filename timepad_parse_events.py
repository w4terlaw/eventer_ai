import asyncio
from datetime import datetime

import aiohttp

from config import Config
from core import get_session
from core.database.models import Category, City, Event, Organization

session = get_session()

organizations_ids: dict[int, int] = dict()


async def parse_city(city):
    exclude_ids = []
    count = await get_event_count(city, exclude_ids)
    # first_count = count
    try:
        while count != 0:
            events, count = await get_events(city, exclude_ids)
            for event_data in events:
                organization_id = await create_organization(event_data["organization"])

                event = Event(
                    title=event_data["title"],
                    street=event_data["address"]["street"],
                    maxPrice=event_data["maxPrice"],
                    startDate=event_data["startDate"] and datetime.fromisoformat(event_data["startDate"]),
                    endDate=event_data["endDate"] and datetime.fromisoformat(event_data["endDate"]),
                    rating=event_data["rating"],
                    category_id=event_data["categories"][0],
                    organization_id=organization_id,
                    city_id=city.id,
                )

                event.save(session)
                exclude_ids.append(event_data["id"])
            print(count)
    except Exception as e:
        print(e)


async def get_event_count(city, exclude_ids):
    async with aiohttp.ClientSession() as session:
        response = await session.get(Config.TIMEPAD_API_URL.format(params=generate_params(city.name, exclude_ids)))
        data = await response.json()
        return data["count"]


async def get_events(city, exclude_ids):
    async with aiohttp.ClientSession() as session:
        response = await session.get(Config.TIMEPAD_API_URL.format(params=generate_params(city.name, exclude_ids)))
        data = await response.json()
        return data["list"], data['count']


async def create_organization(data):
    o_id = organizations_ids.get(data["id"])
    if o_id is None:
        organization = Organization(
            name=data["name"],
            logo=data["logo"],
            phone=data["contact_phone"].replace("-", "").replace("(", "").replace(")", "").replace(" ", ""),
        )
        organization.save(session)
        o_id = organizations_ids[data["id"]] = organization.id
    return o_id


def generate_params(city_name, exclude_ids):
    params = f"?city={city_name}"
    for event_id in exclude_ids:
        params += f"&excludeIds[]={event_id}"
    return params


def get_categories():
    return session.query(Category.id).all()


def get_cities():
    return session.query(City).all()


async def main():
    cities = get_cities()
    tasks = [parse_city(city) for city in cities]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
