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
        # the golden set
        test = pd.DataFrame({'user': test_users,
                             'test_item': test_items,
                             'test_score': test_scores})
        print(test)
        print()
        # because we are using all the items for the metrics we need to make sure the full data don't have
        # the test items with its own score.
        #temp = pd.DataFrame({'user': neg_users,
        #                     'test_item': neg_items,
        #                     'test_score': neg_scores})
        #temp['key1'] = 1
        #test['key2'] = 1
        #temp = pd.merge(temp, test, on=['user', 'test_item'], how='left')
        #temp = temp[~(temp.key2 == temp.key1)]
        #temp = temp.drop(['test_score_y','key1', 'key2'], axis=1)
        #temp.rename(columns={'test_score_x': 'test_score'}, inplace=True)
        #full = pd.concat([temp, test])
        #full = full.drop(['key2'], axis=1)
        # the full set
        #full.rename(columns={"test_item": "item", "test_score": "score"}, inplace=True)
        full = pd.DataFrame({'user': neg_users,
                            'item': neg_items,
                            'score': neg_scores})
        print(full)
        print()
        full = pd.merge(full, test, on=['user'], how='left')
        print(full)
        print()
        # test = pd.merge(test, full, on=['user'], how='left')
        # rank the items according to the scores for each user
        full['rank'] = full.groupby('user')['score'].rank(method='first', ascending=False)
        print(full)
        print()
        test['rank'] = test.groupby('user')['test_score'].rank(method='first', ascending=False)
        full.sort_values(['user', 'rank'], inplace=True)
        print(full)
        print()
        test.sort_values(['user', 'rank'], inplace=True)
        self._subjects = full

    def cal_hit_ratio(self):
        # Hit Ratio @ top_K
        full, top_k = self._subjects, self._top_k
        top_k = full[full['rank'] <= top_k]
        test_in_top_k = top_k[top_k['test_item'] == top_k['item']]  # golden items hit in the top_K items
        return len(test_in_top_k) * 1.0 / full['user'].nunique()

    def cal_mrr(self):
        # MRR @ top_K
        rec_rank = 0
        full, top_k = self._subjects, self._top_k
        top_k = full[full['rank'] <= top_k]
        test_in_top_k = top_k[top_k['test_item'] == top_k['item']]
        for rate in test_in_top_k['rank']:
            rec_rank += (1 / rate)
        return rec_rank / full['user'].nunique()

    def cal_mpr(self):
        # MPR
        rec_percent = 0
        full = self._subjects
        test = full[full['test_item'] == full['item']]
        for rate in test['rank']:
            rec_percent += (rate / test['rank'].max())
        return 1 - (rec_percent / full['user'].nunique())

    def cal_ndcg(self):
        full, top_k = self._subjects, self._top_k
        top_k = full[full['rank'] <= top_k]
        test_in_top_k =top_k[top_k['test_item'] == top_k['item']]
        test_in_top_k['ndcg'] = test_in_top_k['rank'].apply(lambda x: math.log(2) / math.log(1 + x)) # the rank starts from 1
        return test_in_top_k['ndcg'].sum() * 1.0 / full['user'].nunique()
