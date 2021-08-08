import torch
from neumf import NeuMF

def resume_checkpoint(model, model_dir, device_id):
    state_dict = torch.load(model_dir,
                            map_location=lambda storage, loc: storage.cuda(device=device_id))  # ensure all storage are on gpu
    model.load_state_dict(state_dict)

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
                'pretrain_mf': 'movielens_checkpoints/{}'.format('movielens_gmf_movielens_Epoch49_HR0.0272_NDCG0.0501.model'),
                'pretrain_mlp': 'movielens_checkpoints/{}'.format('movielens_mlp_movielens_Epoch49_HR0.0354_NDCG0.0652.model'),
                'pretrain_neumf': 'movielens_checkpoints/{}'.format('movielens_neumf_movielens_Epoch7_HR0.0319_NDCG0.0503.model'),
                'model_dir':'movielens_checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }

config = neumf_config
neumf_model = NeuMF(config)
if config['use_cuda'] is True:
    neumf_model.cuda()
resume_checkpoint(neumf_model, model_dir=config['pretrain_neumf'], device_id=config['device_id'])

embedding_user_neumf = torch.nn.Embedding(num_embeddings=5765, embedding_dim=8)
embedding_item_neumf = torch.nn.Embedding(num_embeddings=1865, embedding_dim=8)

embedding_user_neumf.weight.data = neumf_model.embedding_user.weight.data
embedding_item_neumf.weight.data = neumf_model.embedding_item.weight.data

vector = torch.mul(embedding_user_neumf, embedding_item_neumf)

print(vector)