from core.database import get_session
from core.database.models import User

session = get_session()


def main():
    users = session.query(User).all()

    for user in users:
        print(f"User: {user.last_name} {user.first_name} {user.middle_name}")
        for category in user.categories:
            print(f"\tCategory: {category.name}")
            for event in category.events:
                print(f"\t\tEvent: {event.title}")
                print(f"\t\tOrganization: {event.organization}")
                print(f"\t\tDate: {event.startDate} - {event.endDate}")
                print("\t\t-------------------------")
        print("\n")


if __name__ == "__main__":
    main()
