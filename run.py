from hinge import Hinge
import time


def run():

    hinge = Hinge()
    feed = hinge.get_feed()

    arr = []

    for i in feed:
        arr.append(i['subjectId'])

    subjects = str(arr).strip('[]').replace(' ', '').replace("'", '')

    profiles = hinge.get_profile(subjects)
    print(f"Found {len(profiles)} profiles")

    for i in profiles:

        print(f"Liking {i['profile']['firstName']}")

        subject = {
            'id': i['identityId'],
            'url': i['profile']['mainPhoto']['url'],
            'box': i['profile']['mainPhoto']['boundingBox'],
        }

        swipe = hinge.swipe(subject)
        print(swipe)

        time.sleep(10)

    return run()


if __name__ == "__main__":
    run()
