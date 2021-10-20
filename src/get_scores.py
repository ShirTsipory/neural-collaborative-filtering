import csv
import os
from random import randrange
import datetime
import time
import pandas as pd
import numpy as np

def mrr_k(preds_df, k):
    preds_df['rr_k'] = 1 / preds_df['rank']
    preds_df.loc[preds_df['rank'] > k, 'rr_k'] = 0
    return preds_df.loc[preds_df['rank'] > 0, 'rr_k'].mean()

def hr_k(preds_df, k):
    preds_df['hit'] = 0
    preds_df.loc[preds_df['rank'] <= k, 'hit'] = 1
    return preds_df['hit'].mean()

def mpr(preds_df, num_all_items):
    return 1 - (preds_df['rank'] / num_all_items).mean()

def ndcg_k(preds_df, k):
    preds_df['ndcg_k'] = 1 / np.log2(1 + preds_df['rank'])
    preds_df.loc[preds_df['rank'] > k, 'ndcg_k'] = 0
    return preds_df['ndcg_k'].mean()

# names=['user', 'item', 'rating', 'timestamp'],
#                        dtype={'user': int, 'item': int, 'rating': float, 'timestamp': float},
#                        engine='python'

# taking out only the test items but I need to reindex them back.

#test_items = test['test_item'].values
#print(test_items)
#print(len(test_items))
#items_set = set(test_items)
#trained = pd.read_csv('movilens_csv/scores_epoch_27.csv', sep=',')
#print(trained)
#test_partly = test[['user', 'item']]
#print(test_partly)
#full = pd.merge(test_partly, trained, on=['user', 'item'], how='left')
#print(full)
# selecting rows based on condition
#result = trained.loc[~trained['item'].isin(items_set)]
#print(result)
#for index, row in trained.iterrows():
#    if row['item'] in items_set:

# full = pd.merge(index_data, test, on=['user', 'item'], how='left')

####################################################################################################################
trained_data = pd.read_csv('csvs/movilens_csv/scores_epoch_0.csv', sep=',')
# trained_data = pd.read_csv('csvs/netflix_csv/scores_epoch_0.csv', sep=',')
# trained_data = pd.read_csv('csvs/yahoo_csv/scores_epoch_16.csv', sep=',')

# trained_data = pd.read_csv('csvs/amazonbeauty_csv/scores_epoch_3.csv', sep=',')
# trained_data = pd.read_csv('csvs/amazonbooks_csv/scores_epoch_0.csv', sep=',')
# trained_data = pd.read_csv('csvs/goodbooks_csv/scores_epoch_0.csv', sep=',')
# trained_data = pd.read_csv('csvs/moviesdat_csv/scores_epoch_20.csv', sep=',')

items_list = []
for idx, line in trained_data.iterrows():
    items_list.append(line['item'])
items_list = list(set(items_list))
num_all_items = len(items_list)
print("num_all_items")
print(num_all_items)
print()
test = trained_data[trained_data['test_item'] == trained_data['item']]
# print(test)
test_check = test[['user', 'item', 'rank']]

print("hr@5")
print(hr_k(test_check, 5))
print("hr@10")
print(hr_k(test_check, 10))
print("hr@20")
print(hr_k(test_check, 20))
print()
print("mrr@5")
print(mrr_k(test_check, 5))
print("mrr@10")
print(mrr_k(test_check, 10))
print("mrr@20")
print(mrr_k(test_check, 20))
print()
print("ndcg@5")
print(ndcg_k(test_check, 5))
print("ndcg@10")
print(ndcg_k(test_check, 10))
print("ndcg@20")
print(ndcg_k(test_check, 20))
print()
print("mpr")
print(mpr(test_check, num_all_items))
print()

# take test check data and create it that the user and item ids will be as in index data.

index_data = pd.read_csv('csvs/movilens_csv/new_index_movielens.csv', sep=',')
# index_data = pd.read_csv('csvs/netflix_csv/new_index_netflix.csv', sep=',')
# index_data = pd.read_csv('csvs/yahoo_csv/new_index_yahoo.csv', sep=',')

# index_data = pd.read_csv('csvs/amazonbeauty_csv/new_index_amazonbeauty.csv', sep=',')
# index_data = pd.read_csv('csvs/amazonbooks_csv/new_index_amazonbooks.csv', sep=',')
# index_data = pd.read_csv('csvs/goodbooks_csv/new_index_goodbooks.csv', sep=',')
# index_data = pd.read_csv('csvs/moviesdat_csv/new_index_moviesdat.csv', sep=',')

# print(index_data)
user_dict = {}
item_dict = {}
for idx, line in index_data.iterrows():
    if line['userId'] not in user_dict.keys():  # user
        user_dict[line['userId']] = line['uid']
    if line['itemId'] not in user_dict.keys():  # item
        user_dict[line['itemId']] = line['mid']

#for idx, line in test_check.iterrows():
#    line['user'] = user_dict[line['user']]
#    line['item'] = user_dict[line['item']]


# with open('ncf_netflix_scores.csv', 'w', newline='') as w_file:
# with open('ncf_yahoo_scores.csv', 'w', newline='') as w_file:


# with open('ncf_amazonbeauty_scores.csv', 'w', newline='') as w_file:
# with open('ncf_amazonbooks_scores.csv', 'w', newline='') as w_file:
# with open('ncf_goodbooks_scores.csv', 'w', newline='') as w_file:
# with open('ncf_moviesdat_scores.csv', 'w', newline='') as w_file:
with open('ncf_movielens_scores.csv', 'w', newline='') as w_file:
    writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
    writer.writerow(['user', 'item', 'score', 'rank'])
    for idx, line in test.iterrows():
        user = user_dict[line['user']]
        item = user_dict[line['item']]
        score = line['score']
        rank = line['rank']
        writer.writerow([user, item, score, rank])