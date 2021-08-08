import codecs
import csv
import os
from random import randrange
import datetime
import time
import pandas as pd
import numpy as np


def create_final_corpus_all(file_out, data_dir, min_usr_len, max_usr_len, fin_usr_len, min_items_cnt, max_items_cnt):
    print(data_dir)
    raw_data = pd.read_csv(data_dir, sep=',',
                           names=['user', 'item', 'rating', 'timestamp'],
                           dtype={'user': int, 'item': int, 'rating': float, 'timestamp': float},
                           engine='python')

    sample_row = raw_data.iloc[0, :]
    if pd.isna(sample_row.rating):
        raw_data.rating = np.ones(len(raw_data))
    if pd.isna(sample_row.timestamp):
        raw_data.timestamp = np.ones(len(raw_data))

    # user item id map
    raw_num_users = len(pd.unique(raw_data.user))
    raw_num_items = len(pd.unique(raw_data.item))

    print('# raw users: %d' % (raw_num_users))
    print('# raw items: %d' % (raw_num_items))

    # Filter positive threshold
    raw_data = raw_data[raw_data['rating'] > 4.0]

    # Filter users
    num_items_by_user = raw_data.groupby('user', as_index=False).size()
    num_items_by_user = num_items_by_user.set_index('user')
    user_filter_idx = raw_data['user'].isin(
        num_items_by_user.index[(num_items_by_user['size'] > min_usr_len)
                                & (num_items_by_user['size'] < max_usr_len)])
    raw_data = raw_data[user_filter_idx]

    # Filter items
    num_users_by_item = raw_data.groupby('item', as_index=False).size()
    num_users_by_item = num_users_by_item.set_index('item')
    item_filter_idx = raw_data['item'].isin(
        num_users_by_item.index[(num_users_by_item['size'] > min_items_cnt)
                                & (num_users_by_item['size'] < max_items_cnt)])
    raw_data = raw_data[item_filter_idx]
    num_users_by_item = raw_data.groupby('item', as_index=False).size()
    num_users_by_item = num_users_by_item.set_index('item')

    # Filter users
    num_items_by_user = raw_data.groupby('user', as_index=False).size()
    num_items_by_user = num_items_by_user.set_index('user')
    user_filter_idx = raw_data['user'].isin(
        num_items_by_user.index[(num_items_by_user['size'] >= fin_usr_len)
                                & (num_items_by_user['size'] <= max_usr_len)])
    raw_data = raw_data[user_filter_idx]
    num_items_by_user = raw_data.groupby('user', as_index=False).size()
    num_items_by_user = num_items_by_user.set_index('user')
    print(raw_data.shape[0])

    num_users = len(pd.unique(raw_data.user))
    num_items = len(pd.unique(raw_data.item))
    print('# user after filter (min %d user len): %d' % (min_usr_len, num_users))
    print('# items after filter (min %d items cnt): %d' % (min_items_cnt, num_items))

    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for idx, line in raw_data.iterrows():
            user = line['user']
            item = line['item']
            rating = line['rating']
            date = line['timestamp']
            writer.writerow([user, item, rating, date])


def create_movielens_corpus(min_usr_len, max_usr_len, fin_usr_len, min_items_cnt, max_items_cnt):  # MovieLens: https://grouplens.org/datasets/movielens/
    file_out = './data/movielens_corpus.csv'  # The file of the output, the ready corpus
    data_dir = './data/movielens'  # The directory of the files.
    for file in sorted(os.listdir(data_dir)):
        print(file)
        os.path.join(data_dir, file)
        raw_data = pd.read_csv(os.path.join(data_dir, file), sep='::',
                                   names=['user', 'item', 'rating', 'timestamp'],
                                   dtype={'user': int, 'item': int, 'rating': float, 'timestamp': float},
                                   engine='python')

        sample_row = raw_data.iloc[0, :]
        if pd.isna(sample_row.rating):
            raw_data.rating = np.ones(len(raw_data))
        if pd.isna(sample_row.timestamp):
            raw_data.timestamp = np.ones(len(raw_data))

        # user item id map
        raw_num_users = len(pd.unique(raw_data.user))
        raw_num_items = len(pd.unique(raw_data.item))

        print('# raw users: %d' % (raw_num_users))
        print('# raw items: %d' % (raw_num_items))

        # Filter positive threshold
        raw_data = raw_data[raw_data['rating'] > 4.0]

        # Filter users
        num_items_by_user = raw_data.groupby('user', as_index=False).size()
        num_items_by_user = num_items_by_user.set_index('user')
        user_filter_idx = raw_data['user'].isin(
            num_items_by_user.index[(num_items_by_user['size'] > min_usr_len)
                                    & (num_items_by_user['size'] < max_usr_len)])
        raw_data = raw_data[user_filter_idx]

        # Filter items
        num_users_by_item = raw_data.groupby('item', as_index=False).size()
        num_users_by_item = num_users_by_item.set_index('item')
        item_filter_idx = raw_data['item'].isin(
            num_users_by_item.index[(num_users_by_item['size'] > min_items_cnt)
                                    & (num_users_by_item['size'] < max_items_cnt)])
        raw_data = raw_data[item_filter_idx]
        num_users_by_item = raw_data.groupby('item', as_index=False).size()
        num_users_by_item = num_users_by_item.set_index('item')

        # Filter users
        num_items_by_user = raw_data.groupby('user', as_index=False).size()
        num_items_by_user = num_items_by_user.set_index('user')
        user_filter_idx = raw_data['user'].isin(
            num_items_by_user.index[(num_items_by_user['size'] >= fin_usr_len)
                                    & (num_items_by_user['size'] <= max_usr_len)])
        raw_data = raw_data[user_filter_idx]
        num_items_by_user = raw_data.groupby('user', as_index=False).size()
        num_items_by_user = num_items_by_user.set_index('user')
        print(raw_data.shape[0])

        num_users = len(pd.unique(raw_data.user))
        num_items = len(pd.unique(raw_data.item))
        print('# user after filter (min %d user len): %d' % (min_usr_len, num_users))
        print('# items after filter (min %d items cnt): %d' % (min_items_cnt, num_items))

        with open(file_out, 'w', newline='') as w_file:
            writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
            for idx, line in raw_data.iterrows():
                user = line['user']
                item = line['item']
                rating = line['rating']
                date = line['timestamp']
                writer.writerow([user, item, rating, date])


"""
def create_movielens_corpus(min_usr_len, max_usr_len, min_items_cnt, max_items_cnt):  # MovieLens: https://grouplens.org/datasets/movielens/
    file_out = './data/movielens_corpus.csv'  # The file of the output, the ready corpus
    data_dir = './data/movielens'  # The directory of the files.
    users_amount = {}
    users_set = set()
    items_amount = {}
    items_set = set()
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    line = line.split('::')
                    user = line[0]
                    if user not in users_set:
                        users_set.add(user)
                        users_amount[user] = 1
                    else:
                        users_amount[user] += 1
                    cus_id = line[1]
                    if cus_id not in items_set:
                        items_set.add(cus_id)
                        items_amount[cus_id] = 1
                    else:
                        items_amount[cus_id] += 1
            sorted_users = sorted(users_amount.items(), key=lambda x: x[1], reverse=True)
            sorted_items = sorted(items_amount.items(), key=lambda x: x[1], reverse=True)
            sorted_users = [user[0] for user in sorted_users if user[1] >= min_usr_len and user[1] <= max_usr_len]
            sorted_items = [item[0] for item in sorted_items if item[1] >= min_items_cnt and item[1] <= max_items_cnt]
            sorted_users = set(sorted_users)
            sorted_items = set(sorted_items)
            print("Users amount")
            print(len(sorted_users))
            print("items amount")
            print(len(sorted_items))
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    line = line.split('::')
                    user = line[0]
                    if user not in sorted_users:
                        continue
                    cus_id = line[1]
                    if cus_id not in sorted_items:
                        continue
                    rating = line[2]
                    date = line[3][:-1]
                    writer.writerow([user, cus_id, rating, date])
"""

def create_netflix_corpus():  # https://www.kaggle.com/netflix-inc/netflix-prize-data
    file_out = './data/netflix_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/netflix'  # The directory of the files.
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    if ',' not in line:
                        user = int(line.split(':')[0])
                    else:
                        cus_id, rating, date = line.split(',')
                        date = date[:-1]
                        date = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
                        writer.writerow([str(user), str(cus_id), str(rating), str(date)])


def create_moviesdat_corpus():  # https://www.kaggle.com/rounakbanik/the-movies-dataset
    file_out = './data/moviesdat_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/moviesdat'  # The directory of the files.
    count = 0
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    if count < 1:
                        count += 1
                    elif count >= 1:
                        line = line.split(',')
                        user = line[0]
                        cus_id = line[1]
                        rating = line[2]
                        date = line[3][:-1]
                        writer.writerow([user, cus_id, rating, date])


def create_yahoo_corpus():  # https://webscope.sandbox.yahoo.com/catalog.php?datatype=c&did=48
    # We create a random timestamp.
    file_out = './data/yahoo_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/yahoo'  # The directory of the files.
    start_date = datetime.date(2000, 1, 1)
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    line = line.split('|')
                    if len(line) != 1:
                        user = line[0]
                    elif len(line) == 1:
                        line = line[0].split('\t')
                        cus_id = line[0]
                        rating = line[1]
                        random_number_of_days = randrange(10000)
                        random_date = str(start_date + datetime.timedelta(days=random_number_of_days))
                        date = time.mktime(datetime.datetime.strptime(random_date, "%Y-%m-%d").timetuple())
                        writer.writerow([user, cus_id, rating, int(date)])


def create_goodbooks_corpus():  # https://www.kaggle.com/zygmunt/goodbooks-10k
    # The data is sorted by time so we create a timestamp accordingly.
    file_out = './data/goodbooks_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/goodbooks'  # The directory of the files.
    count = 0
    last_cus = '0'
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    if count < 1:
                        count += 1
                    elif count >= 1:
                        line = line.split(',')
                        user = line[1]
                        cus_id = line[0]
                        rating = line[2][:-1]
                        if last_cus != cus_id:
                            last_cus = cus_id
                            start_date = datetime.date(2000, 1, 1)
                            date_time = start_date
                        else:
                            date_time = date_time + datetime.timedelta(days=1)
                        date = time.mktime(datetime.datetime.strptime(str(date_time), "%Y-%m-%d").timetuple())
                        writer.writerow([user, cus_id, rating, int(date)])


def create_booksrec_corpus():  # https://www.kaggle.com/arashnic/book-recommendation-dataset
    # We create a random timestamp.
    # Because the item id isn't int, we make sure to pass every id to an int id.
    file_out = './data/booksrec_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/booksrec'  # The directory of the files.
    count = 0
    start_date = datetime.date(2000, 1, 1)
    id_to_num = {}
    id_counter = 1
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU', encoding="utf8") as r_file:
                for line in r_file:
                    if count < 1:
                        count += 1
                    elif count >= 1:
                        line = line.split(',')
                        user = line[0]
                        if line[1] not in id_to_num.keys():
                            id_to_num[line[1]] = id_counter
                            id_counter += 1
                        cus_id = id_to_num[line[1]]
                        rating = line[2][:-1]
                        random_number_of_days = randrange(10000)
                        random_date = str(start_date + datetime.timedelta(days=random_number_of_days))
                        date = time.mktime(datetime.datetime.strptime(random_date, "%Y-%m-%d").timetuple())
                        writer.writerow([user, cus_id, rating, int(date)])


def create_animerec_corpus():  # https://www.kaggle.com/CooperUnion/anime-recommendations-database
    # We create a random timestamp.
    file_out = './data/animerec_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/animerec'  # The directory of the files.
    count = 0
    start_date = datetime.date(2000, 1, 1)
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    if count < 1:
                        count += 1
                    elif count >= 1:
                        line = line.split(',')
                        user = line[0]
                        cus_id = line[1]
                        rating = line[2][:-1]
                        random_number_of_days = randrange(10000)
                        random_date = str(start_date + datetime.timedelta(days=random_number_of_days))
                        date = time.mktime(datetime.datetime.strptime(random_date, "%Y-%m-%d").timetuple())
                        writer.writerow([user, cus_id, rating, int(date)])


def create_animerec20_corpus():  # https://www.kaggle.com/hernan4444/anime-recommendation-database-2020
    # We create a random timestamp.
    file_out = './data/animerec20_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/animerec20'  # The directory of the files.
    count = 0
    start_date = datetime.date(2000, 1, 1)
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    if count < 1:
                        count += 1
                    elif count >= 1:
                        line = line.split(',')
                        user = line[0]
                        cus_id = line[1]
                        rating = line[2][:-1]
                        random_number_of_days = randrange(10000)
                        random_date = str(start_date + datetime.timedelta(days=random_number_of_days))
                        date = time.mktime(datetime.datetime.strptime(random_date, "%Y-%m-%d").timetuple())
                        writer.writerow([user, cus_id, rating, int(date)])


def create_amazonbeauty_corpus():  # https://www.kaggle.com/skillsmuggler/amazon-ratings
    # We create a random timestamp.
    # Because the item id isn't int, we make sure to pass every id to an int id.
    file_out = './data/amazonbeauty_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/amazonbeauty'  # The directory of the files.
    count = 0
    user_to_num = {}
    user_counter = 1
    id_to_num = {}
    id_counter = 1
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU', encoding="utf8") as r_file:
                for line in r_file:
                    if count < 1:
                        count += 1
                    elif count >= 1:
                        line = line.split(',')
                        if line[0] not in user_to_num.keys():
                            user_to_num[line[0]] = user_counter
                            user_counter += 1
                        user = user_to_num[line[0]]
                        if line[1] not in id_to_num.keys():
                            id_to_num[line[1]] = id_counter
                            id_counter += 1
                        cus_id = id_to_num[line[1]]
                        rating = line[2][:-1]
                        date = line[3][:-1]
                        writer.writerow([user, cus_id, rating, date])


def create_amazonbooks_corpus():  # https://www.kaggle.com/skillsmuggler/amazon-ratings
    # We create a random timestamp.
    # Because the item id isn't int, we make sure to pass every id to an int id.
    file_out = './data/amazonbooks_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/amazonbooks'  # The directory of the files.
    count = 0
    user_to_num = {}
    user_counter = 1
    id_to_num = {}
    id_counter = 1
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU', encoding="utf8") as r_file:
                for line in r_file:
                    if count < 1:
                        count += 1
                    elif count >= 1:
                        line = line.split(',')
                        if line[0] not in user_to_num.keys():
                            user_to_num[line[0]] = user_counter
                            user_counter += 1
                        user = user_to_num[line[0]]
                        if line[1] not in id_to_num.keys():
                            id_to_num[line[1]] = id_counter
                            id_counter += 1
                        cus_id = id_to_num[line[1]]
                        rating = line[2][:-1]
                        date = line[3][:-1]
                        writer.writerow([user, cus_id, rating, date])


def create_yahoo_all_corpus():  # https://webscope.sandbox.yahoo.com/catalog.php?datatype=c&did=48
    file_out = './data/yahoo_all_corpus_temp.csv'  # The file of the output, the ready corpus
    data_dir = './data/yahoo_all'  # The directory of the files.
    user_counter = 0
    item_counter = 0
    item_set = set()
    items_amount = {}
    line_counter = 0
    last_user = ''
    start_date = datetime.date(2000, 1, 1)
    with open(file_out, 'w', newline='') as w_file:
        writer = csv.writer(w_file, delimiter=',', quotechar='"', escapechar='\n', quoting=csv.QUOTE_NONE)
        for file in sorted(os.listdir(data_dir)):
            print(file)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                for line in r_file:
                    if user_counter >= 20000:
                        break
                    line = line.split('|')
                    if len(line) != 1:
                        user = line[0]
                        user_counter += 1
                    elif len(line) == 1:
                        line = line[0].split('\t')
                        cus_id = line[0]
                        if cus_id not in item_set:
                            item_set.add(cus_id)
                            items_amount[cus_id] = 1
                            item_counter += 1
                        else:
                            items_amount[cus_id] += 1
                        line_counter += 1
                        if (line_counter % 500000) == 0:
                            print(line_counter)
            user_counter = 0
            line_counter = 0
            top_items = sorted(items_amount.items(), key=lambda x: x[1], reverse=True)[:30000]
            top_items = [item[0] for item in top_items]
            top_items = set(top_items)
            with codecs.open(os.path.join(data_dir, file), 'rU') as r_file:
                print("staring with the file")
                for line in r_file:
                    if user_counter >= 20000:
                        break
                    line = line.split('|')
                    if len(line) != 1:
                        user = line[0]
                        user_counter += 1
                    elif len(line) == 1:
                        line = line[0].split('\t')
                        cus_id = line[0]
                        if cus_id not in top_items:
                            continue
                        rating = float(line[1])/20
                        if last_user != user:
                            last_user = user
                            date_time = start_date
                        else:
                            date_time = date_time + datetime.timedelta(days=1)
                        date = time.mktime(datetime.datetime.strptime(str(date_time), "%Y-%m-%d").timetuple())
                        writer.writerow([user, cus_id, rating, int(date)])
                        line_counter += 1
                        if (line_counter % 500000) == 0:
                            print(line_counter)
    print("user_counter")
    print(user_counter)
    print()
    print("item_counter")
    print(item_counter)
    print()
    print("line_counter")
    print(line_counter)



def main():
    ##### create_movielens_corpus(min_usr_len=1, max_usr_len=1000, fin_usr_len=4, min_items_cnt=10, max_items_cnt=10000)
    #create_netflix_corpus()
    create_final_corpus_all('./data/netflix_corpus.csv', './data/netflix_corpus_temp.csv', min_usr_len=3,
                            max_usr_len=1000, fin_usr_len=4, min_items_cnt=100, max_items_cnt=130000)
    ##### create_moviesdat_corpus()
    ##### create_final_corpus_all('./data/moviesdat_corpus.csv', './data/moviesdat_corpus_temp.csv',min_usr_len=100, max_usr_len=1000, fin_usr_len=4, min_items_cnt=100, max_items_cnt=100000)
    ##### create_yahoo_all_corpus()
    ##### create_final_corpus_all('./data/yahoo_all_corpus.csv', './data/yahoo_all_corpus_temp.csv', min_usr_len=2, max_usr_len=1000, fin_usr_len=4, min_items_cnt=10, max_items_cnt=100000)
    ##### create_goodbooks_corpus()
    ##### create_final_corpus_all('./data/goodbooks_corpus.csv', './data/goodbooks_corpus_temp.csv', min_usr_len=2, max_usr_len=1000, fin_usr_len=4, min_items_cnt=5, max_items_cnt=10000)
    # create_booksrec_corpus()
    #create_final_corpus_all('./data/booksrec_corpus.csv', './data/booksrec_corpus_temp.csv', min_usr_len=2, max_usr_len=1000, fin_usr_len=4, min_items_cnt=5, max_items_cnt=10000)
    # create_animerec_corpus()
    #create_final_corpus_all('./data/animerec_corpus.csv', './data/animerec_corpus_temp.csv', min_usr_len=2, max_usr_len=1000, fin_usr_len=4, min_items_cnt=10, max_items_cnt=100000)
    # create_animerec20_corpus()
    #create_final_corpus_all('./data/animerec20_corpus.csv', './data/animerec20_corpus_temp.csv', min_usr_len=2, max_usr_len=1000, fin_usr_len=4, min_items_cnt=15, max_items_cnt=100000)
    ##### create_amazonbeauty_corpus()
    ##### create_final_corpus_all('./data/amazonbeauty_corpus.csv', './data/amazonbeauty_corpus_temp.csv', min_usr_len=2,
    #####                        max_usr_len=1000, fin_usr_len=4, min_items_cnt=5, max_items_cnt=50000)
    ##### create_amazonbooks_corpus()
    ##### create_final_corpus_all('./data/amazonbooks_corpus.csv', './data/amazonbooks_corpus_temp.csv', min_usr_len=10,
    #####                        max_usr_len=1000, fin_usr_len=4, min_items_cnt=100, max_items_cnt=10000)



if __name__ == '__main__':
    main()
