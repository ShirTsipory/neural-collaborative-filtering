import pandas as pd
import numpy as np
import os
from gmf import GMFEngine
from mlp import MLPEngine
from neumf import NeuMFEngine
from data import SampleGenerator

# os.environ['CUDA_VISIBLE_DEVICES'] = "1"


gmf_config = {'alias': 'gmf_movielens',
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
              'num_users': 5765,
              'num_items': 1865,
              'latent_dim': 8,
              'num_negative': 4,
              'l2_regularization': 0, # 0.01
              'use_cuda': True,
              'device_id': 0,
              'model_dir':'checkpoints/movielens_{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_movielens',
              'num_epoch': 50,
              'batch_size': 1024,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 5765,
              'num_items': 1865,
              'latent_dim': 8,
              'num_negative': 4,
              'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
              'l2_regularization': 0.0000001,  # MLP model is sensitive to hyper params
              'use_cuda': True,
              'device_id': 0,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('movielens_gmf_factor8neg4_movielens_Epoch26_HR0.4158_NDCG0.5995.model'),
              'model_dir':'checkpoints/movielens_{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_movielens',
                'num_epoch': 50,
                'batch_size': 1024,
                'optimizer': 'adam',
                'adam_lr': 1e-3,
                'num_users': 5765,
                'num_items': 1865,
                'latent_dim_mf': 8,
                'latent_dim_mlp': 8,
                'num_negative': 4,
                'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
                'l2_regularization': 0.01,
                'use_cuda': True,
                'device_id': 0,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('movielens_gmf_factor8neg4_movielens_Epoch26_HR0.4158_NDCG0.5995.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('movielens_mlp_factor8neg4_pretrain_movielens_Epoch41_HR0.4477_NDCG0.6280.model'),
                'model_dir':'checkpoints/movielens_{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }


# Load Data
ml1m_dir = 'data/movielens_corpus.csv'
# ml1m_dir = 'data/amazonbeauty/amazonbeauty_corpus.csv'
# ml1m_dir = 'data/goodbooks/goodbooks_corpus.csv'
# ml1m_rating = pd.read_csv(ml1m_dir, sep='::', header=None, names=['uid', 'mid', 'rating', 'timestamp'],  engine='python')
ml1m_rating = pd.read_csv(ml1m_dir, sep=',', header=None, names=['uid', 'mid', 'rating', 'timestamp'],  engine='python')
# Reindex
user_id = ml1m_rating[['uid']].drop_duplicates().reindex()
user_id['userId'] = np.arange(len(user_id))
ml1m_rating = pd.merge(ml1m_rating, user_id, on=['uid'], how='left')
item_id = ml1m_rating[['mid']].drop_duplicates()
item_id['itemId'] = np.arange(len(item_id))
ml1m_rating = pd.merge(ml1m_rating, item_id, on=['mid'], how='left')
ml1m_rating = ml1m_rating[['userId', 'itemId', 'rating', 'timestamp']]
print('Range of userId is [{}, {}]'.format(ml1m_rating.userId.min(), ml1m_rating.userId.max()))
print('Range of itemId is [{}, {}]'.format(ml1m_rating.itemId.min(), ml1m_rating.itemId.max()))
# DataLoader for training
sample_generator = SampleGenerator(ratings=ml1m_rating)
evaluate_data = sample_generator.evaluate_data
# Specify the exact model
config = gmf_config
engine = GMFEngine(config)
# config = mlp_config
# engine = MLPEngine(config)
# config = neumf_config
# engine = NeuMFEngine(config)
for epoch in range(config['num_epoch']):
    print('Epoch {} starts !'.format(epoch))
    print('-' * 80)
    train_loader = sample_generator.instance_a_train_loader(config['num_negative'], config['batch_size'])
    engine.train_an_epoch(train_loader, epoch_id=epoch)
    hit_ratio1, hit_ratio2, hit_ratio3, mrr1, mrr2, mrr3, mpr, ndcg1, ndcg2, ndcg3 = engine.evaluate(evaluate_data, epoch_id=epoch)
    engine.save(config['alias'], epoch, hit_ratio1, hit_ratio2, hit_ratio3, mrr1, mrr2, mrr3, mpr, ndcg1, ndcg2, ndcg3)
