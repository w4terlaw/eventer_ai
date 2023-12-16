from datetime import datetime

import requests

from config import Config
from core import get_session
from core.database.models import Category, City, Event, Organization

session = get_session()

organizations_ids: dict[int, int] = dict()


def parse():
    cities = get_cities()

    # categories = get_categories()

    for city in cities:
        exclude_ids = []
        count = first_count = \
            requests.get(Config.TIMEPAD_API_URL.format(params=generate_params(city.name, exclude_ids))).json()["count"]
        while first_count - count <= 100 and count != 0:
            request = requests.get(Config.TIMEPAD_API_URL.format(params=generate_params(city.name, exclude_ids)))
            response = request.json()
            count = response["count"]
            events = response["list"]

            for event_data in events:
                organization_id = create_organization(event_data["organization"])

                event = Event(
                    title=event_data["title"],
                    street=event_data["address"]["street"],
                    maxPrice=event_data["maxPrice"],
                    startDate=event_data["startDate"] and datetime.fromisoformat(event_data["startDate"]),
                    endDate=event_data["endDate"] and datetime.fromisoformat(event_data["endDate"]),
                    rating=event_data["rating"],
                    category_id=event_data["categories"][0],
                    organization_id=organization_id,
                    city_id=city.id
                )

                event.save(session)
                exclude_ids.append(event_data["id"])


def create_organization(data: dict) -> int:
    o_id = organizations_ids.get(data["id"])
    if o_id is None:
        organization = Organization(
            name=data["name"],
            logo=data["logo"],
            phone=data["contact_phone"].replace('-', '').replace('(', '').replace(')', '').replace(' ', ''),
        )
        organization.save(session)
        o_id = organizations_ids[data["id"]] = organization.id
    return o_id


def generate_params(city_name: str, exclude_ids: list[int]):
    params = f"?city={city_name}"
    for event_id in exclude_ids:
        params += f"&excludeIds[]={event_id}"
    return params


def get_categories() -> list[tuple[int]]:
    return session.query(Category.id).all()


def get_cities() -> list[City]:
    return session.query(City).all()


if __name__ == '__main__':
    parse()
