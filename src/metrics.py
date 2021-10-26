import math
import pandas as pd


class MetronAtK(object):
    def __init__(self, top_k):
        self._top_k = top_k
        self._subjects = None  # Subjects which we ran evaluation on

    @property
    def top_k(self):
        return self._top_k

    @top_k.setter
    def top_k(self, top_k):
        self._top_k = top_k

    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, subjects):
        """
        args:
            subjects: list, [test_users, test_items, test_scores, negative users, negative items, negative scores]
        """
        assert isinstance(subjects, list)
        test_users, test_items, test_scores = subjects[0], subjects[1], subjects[2]
        neg_users, neg_items, neg_scores = subjects[3], subjects[4], subjects[5]
        epoch_id = subjects[6]
        # The golden set
        test = pd.DataFrame({'user': test_users,
                             'test_item': test_items,
                             'test_score': test_scores})
        # The full set
        full = pd.DataFrame({'user': neg_users,
                            'item': neg_items,
                            'score': neg_scores})
        full = pd.merge(full, test, on=['user'], how='left', copy=False)
        # rank the items according to the scores for each user
        full['rank'] = full.groupby('user')['score'].rank(method='first', ascending=False)
        full.sort_values(['user', 'rank'], inplace=True)
        self._subjects = full
        test_only = full[full['test_item'] == full['item']]
        test_only.to_csv(r'./csvs/amazonbooks_csv/test_scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)
        # full.to_csv(r'./csvs/amazonbooks_csv/full_scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)

        # full.to_csv(r'./csvs/movielens_csv/scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)
        # full.to_csv(r'./csvs/netflix_csv/scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)
        # full.to_csv(r'./csvs/moviesdat_csv/scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)
        # test_only.to_csv(r'./csvs/yahoo_csv/scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)
        # full.to_csv(r'./csvs/amazonbeauty_csv/scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)
        # full.to_csv(r'./csvs/goodbooks_csv/scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)
        # full.to_csv(r'./csvs/amazonbooks_csv/scores_epoch_' + str(epoch_id) + '.csv', encoding='utf-8', index=False)

    def cal_hit_ratio(self):
        # Hit Ratio @ top_K
        full, top_ks = self._subjects, self._top_k
        hr = []
        for k in top_ks:
            top_k = full[full['rank'] <= k]
            test_in_top_k = top_k[top_k['test_item'] == top_k['item']]  # golden items hit in the top_K items
            hr.append(len(test_in_top_k) * 1.0 / full['user'].nunique())
        return hr

    def cal_mrr(self):
        # MRR @ top_K
        full, top_ks = self._subjects, self._top_k
        mrr = []
        for k in top_ks:
            rec_rank = 0
            top_k = full[full['rank'] <= k]
            test_in_top_k = top_k[top_k['test_item'] == top_k['item']]
            for rate in test_in_top_k['rank']:
                rec_rank += (1 / rate + 1)
            mrr.append(rec_rank / full['user'].nunique())
        return mrr

    def cal_mpr(self):
        # MPR
        rec_percent = 0
        full = self._subjects
        test = full[full['test_item'] == full['item']]
        for rate in test['rank']:
            rec_percent += (rate / test['rank'].max())
        return 1 - (rec_percent / full['user'].nunique())

    def cal_ndcg(self):
        full, top_ks = self._subjects, self._top_k
        ndcg = []
        for k in top_ks:
            top_k = full[full['rank'] <= k]
            test_in_top_k =top_k[top_k['test_item'] == top_k['item']]
            test_in_top_k['ndcg'] = test_in_top_k['rank'].apply(lambda x: math.log(2) / math.log(1 + x)) # the rank starts from 1
            ndcg.append(test_in_top_k['ndcg'].sum() * 1.0 / full['user'].nunique())
        return ndcg