from collections import defaultdict

import pandas as pd
from surprise import Dataset, SVD, Reader

from core import get_session
from core.database.models import UserEvent, Event

session = get_session()


def get_top_n(predictions, n=10, threshold=4):
    user_est_true = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        user_est_true[uid].append((iid, est))
    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        user_est_true[uid] = user_ratings[:n]
        n_rel = sum((int(true_r) >= threshold) for (_, true_r) in user_ratings)
        n_rec_k = sum((int(est) >= threshold) for (est, _) in user_ratings[:n])
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (int(est) >= threshold))
            for (est, true_r) in user_ratings[:n]
        )
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0

        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0

    return precisions, recalls, user_est_true


def main():
    user_event = session.query(UserEvent).all()
    user_ids = [event.user_id for event in user_event]
    event_ids = [event.event_id for event in user_event]
    ratings = [event.rating for event in user_event]

    reader = Reader(rating_scale=(1, 5))

    data = Dataset.load_from_df(pd.DataFrame({'user_id': user_ids, 'event_id': event_ids, 'rating': ratings}), reader)

    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    precisions, recalls, top_n = get_top_n(predictions, n=10)

    avg_precision = sum(prec for prec in precisions.values()) / len(precisions)
    avg_recall = sum(rec for rec in recalls.values()) / len(recalls)

    print(f'Average Precision: {avg_precision:.4f}')
    print(f'Average Recall: {avg_recall:.4f}')

    print("\nTop Recommendations:")
    for event_id, _ in top_n[1]:
        event_title = session.query(Event).filter_by(id=event_id).one_or_none().title
        print(f"Event ID: {event_id}, Title: {event_title}")


if __name__ == '__main__':
    main()
