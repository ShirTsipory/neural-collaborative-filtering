import pandas as pd
import numpy as np
import os
from gmf import GMFEngine
from mlp import MLPEngine
from neumf import NeuMFEngine
from data import SampleGenerator
# os.environ['CUDA_VISIBLE_DEVICES'] = '0, 3'

gmf_config = {'alias': 'gmf_amazonbooks_new',
              'num_epoch': 50,
              'batch_size': 1024,
              # 'optimizer': 'sgd',
              # 'sgd_lr': 1e-3,
              # 'sgd_momentum': 0.9,
              # 'optimizer': 'rmsprop',
              # 'rmsprop_lr': 1e-3,
              # 'rmsprop_alpha': 0.99,
              # 'rmsprop_momentum': 0,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 31202,
              'num_items': 2111,
              'latent_dim': 8,
              'num_negative': 4,
              'l2_regularization': 0, # 0.01
              'use_cuda': True,
              'device_id': 2,
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_amazonbooks_new',
              'num_epoch': 50,
              'batch_size': 256,  # 1024,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 31202,
              'num_items': 2111,
              'latent_dim': 8,
              'num_negative': 4,
              'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
              'l2_regularization': 0.0000001,  # MLP model is sensitive to hyper params
              'use_cuda': True,
              'device_id': 2,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('gmf_amazonbooks_new_Epoch49_HR0.0241_NDCG0.0482.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_amazonbooks_new',
                'num_epoch': 50,
                'batch_size': 1024,
                'optimizer': 'adam',
                'adam_lr': 1e-3,
                'num_users': 31202,
                'num_items': 2111,
                'latent_dim_mf': 8,
                'latent_dim_mlp': 8,
                'num_negative': 4,
                'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
                'l2_regularization': 0.01,
                'use_cuda': True,
                'device_id': 2,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('gmf_amazonbooks_new_Epoch49_HR0.0241_NDCG0.0482.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('mlp_amazonbooks_new_Epoch46_HR0.0466_NDCG0.0874.model'),
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }

# Load Data
# ml1m_dir = 'data/movielens_corpus.csv'
# ml1m_dir = 'data/netflix_corpus.csv'
# ml1m_dir = 'data/moviesdat_corpus.csv'
# ml1m_dir = 'data/yahoo_all_corpus.csv'
# ml1m_dir = 'data/amazonbeauty_corpus.csv'
# ml1m_dir = 'data/goodbooks_corpus.csv'
# ml1m_dir = 'data/amazonbooks_corpus.csv'
ml1m_dir = 'data/ratings_amazon_books_new.csv'
ml1m_rating = pd.read_csv(ml1m_dir, sep=',', header=None, names=['uid', 'mid', 'rating', 'timestamp'],  engine='python')
# Reindex
user_id = ml1m_rating[['uid']].drop_duplicates().reindex()
user_id['userId'] = np.arange(len(user_id))
ml1m_rating = pd.merge(ml1m_rating, user_id, on=['uid'], how='left')
item_id = ml1m_rating[['mid']].drop_duplicates()
item_id['itemId'] = np.arange(len(item_id))
ml1m_rating = pd.merge(ml1m_rating, item_id, on=['mid'], how='left')
# ml1m_rating.to_csv(r'./csvs/movielens_csv/new_index_movielens.csv', encoding='utf-8', index=False)
# ml1m_rating.to_csv(r'./csvs/netflix_csv/new_index_netflix.csv', encoding='utf-8', index=False)
# ml1m_rating.to_csv(r'./csvs/moviesdat_csv/new_index_moviesdat.csv', encoding='utf-8', index=False)
# ml1m_rating.to_csv(r'./csvs/yahoo_csv/new_index_yahoo.csv', encoding='utf-8', index=False)
# ml1m_rating.to_csv(r'./csvs/amazonbeauty_csv/new_index_amazonbeauty.csv', encoding='utf-8', index=False)
# ml1m_rating.to_csv(r'./csvs/goodbooks_csv/new_index_goodbooks.csv', encoding='utf-8', index=False)
# ml1m_rating.to_csv(r'./csvs/amazonbooks_csv/new_index_amazonbooks.csv', encoding='utf-8', index=False)
ml1m_rating.to_csv(r'./csvs/amazonbooks_csv/new_index_amazonbooks_new.csv', encoding='utf-8', index=False)
ml1m_rating = ml1m_rating[['userId', 'itemId', 'rating', 'timestamp']]
print('Range of userId is [{}, {}]'.format(ml1m_rating.userId.min(), ml1m_rating.userId.max()))
print('Range of itemId is [{}, {}]'.format(ml1m_rating.itemId.min(), ml1m_rating.itemId.max()))
# DataLoader for training
sample_generator = SampleGenerator(ratings=ml1m_rating)
evaluate_data = sample_generator.evaluate_data
# Specify the exact model
# config = gmf_config
# engine = GMFEngine(config)
# config = mlp_config
# engine = MLPEngine(config)
config = neumf_config
engine = NeuMFEngine(config)
for epoch in range(config['num_epoch']):
    print('Epoch {} starts !'.format(epoch))
    print('-' * 80)
    train_loader = sample_generator.instance_a_train_loader(config['num_negative'], config['batch_size'])
    engine.train_an_epoch(train_loader, epoch_id=epoch)
    hit_ratio1, hit_ratio2, hit_ratio3, mrr1, mrr2, mrr3, mpr, ndcg1, ndcg2, ndcg3 = engine.evaluate(evaluate_data, epoch_id=epoch)
    engine.save(config['alias'], epoch, hit_ratio1, hit_ratio2, hit_ratio3, mrr1, mrr2, mrr3, mpr, ndcg1, ndcg2, ndcg3)
