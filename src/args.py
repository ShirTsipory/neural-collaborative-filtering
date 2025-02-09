##################################################################################################################
# movielens config
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
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_movielens',
              'num_epoch': 50,
              'batch_size': 256,
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
              'pretrain_mf': 'checkpoints/{}'.format('movielens_gmf_movielens_Epoch49_HR0.0272_NDCG0.0501.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

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
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }
##################################################################################################################
##################################################################################################################
# amazon beauty config
gmf_config = {'alias': 'gmf_amazonbeauty',
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
              'num_users': 18150,
              'num_items': 13570,
              'latent_dim': 8,
              'num_negative': 4,
              'l2_regularization': 0, # 0.01
              'use_cuda': True,
              'device_id': 0,
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_amazonbeauty',
              'num_epoch': 50,
              'batch_size': 256,  # 1024,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 18150,
              'num_items': 13570,
              'latent_dim': 8,
              'num_negative': 4,
              'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
              'l2_regularization': 0.0000001,  # MLP model is sensitive to hyper params
              'use_cuda': True,
              'device_id': 0,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('gmf_amazonbeauty_Epoch49_HR0.0045_NDCG0.0084.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_amazonbeauty',
                'num_epoch': 50,
                'batch_size': 1024,
                'optimizer': 'adam',
                'adam_lr': 1e-3,
                'num_users': 18150,
                'num_items': 13570,
                'latent_dim_mf': 8,
                'latent_dim_mlp': 8,
                'num_negative': 4,
                'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
                'l2_regularization': 0.01,
                'use_cuda': True,
                'device_id': 0,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('gmf_amazonbeauty_Epoch49_HR0.0045_NDCG0.0084.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('mlp_amazonbeauty_Epoch25_HR0.0099_NDCG0.0187.model'),
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }
##################################################################################################################
##################################################################################################################
# GoodBooks config
gmf_config = {'alias': 'gmf_goodbooks',
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
              'num_users': 18645,
              'num_items': 9851,
              'latent_dim': 8,
              'num_negative': 4,
              'l2_regularization': 0, # 0.01
              'use_cuda': True,
              'device_id': 0,
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_goodbooks',
              'num_epoch': 50,
              'batch_size': 256,  # 1024,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 18645,
              'num_items': 9851,
              'latent_dim': 8,
              'num_negative': 4,
              'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
              'l2_regularization': 0.0000001,  # MLP model is sensitive to hyper params
              'use_cuda': True,
              'device_id': 0,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('gmf_goodbooks_Epoch47_HR0.0032_NDCG0.0072.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_goodbooks',
                'num_epoch': 50,
                'batch_size': 1024,
                'optimizer': 'adam',
                'adam_lr': 1e-3,
                'num_users': 18645,
                'num_items': 9851,
                'latent_dim_mf': 8,
                'latent_dim_mlp': 8,
                'num_negative': 4,
                'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
                'l2_regularization': 0.01,
                'use_cuda': True,
                'device_id': 0,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('gmf_goodbooks_Epoch47_HR0.0032_NDCG0.0072.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('mlp_goodbooks_Epoch47_HR0.0198_NDCG0.0363.model'),
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }
##################################################################################################################
##################################################################################################################
# Netflix config
gmf_config = {'alias': 'gmf_netflix',
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
              'num_users': 10677,
              'num_items': 2121,
              'latent_dim': 8,
              'num_negative': 4,
              'l2_regularization': 0, # 0.01
              'use_cuda': True,
              'device_id': 0,
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_netflix',
              'num_epoch': 50,
              'batch_size': 256,  # 1024,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 10677,
              'num_items': 2121,
              'latent_dim': 8,
              'num_negative': 4,
              'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
              'l2_regularization': 0.0000001,  # MLP model is sensitive to hyper params
              'use_cuda': True,
              'device_id': 0,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('gmf_netflix_Epoch49_HR0.0645_NDCG0.0929.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_netflix',
                'num_epoch': 50,
                'batch_size': 1024,
                'optimizer': 'adam',
                'adam_lr': 1e-3,
                'num_users': 10677,
                'num_items': 2121,
                'latent_dim_mf': 8,
                'latent_dim_mlp': 8,
                'num_negative': 4,
                'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
                'l2_regularization': 0.01,
                'use_cuda': True,
                'device_id': 0,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('gmf_netflix_Epoch49_HR0.0645_NDCG0.0929.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('mlp_netflix_Epoch37_HR0.0968_NDCG0.1293.model'),
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}_try2.model'
                }
##################################################################################################################
##################################################################################################################
# moviesdat config
gmf_config = {'alias': 'gmf_moviesdat',
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
              'num_users': 11142,
              'num_items': 2949,
              'latent_dim': 8,
              'num_negative': 4,
              'l2_regularization': 0, # 0.01
              'use_cuda': True,
              'device_id': 3,
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_moviesdat',
              'num_epoch': 50,
              'batch_size': 256,  # 1024,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 11142,
              'num_items': 2949,
              'latent_dim': 8,
              'num_negative': 4,
              'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
              'l2_regularization': 0.0000001,  # MLP model is sensitive to hyper params
              'use_cuda': True,
              'device_id': 3,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('gmf_moviesdat_Epoch45_HR0.0066_NDCG0.0125.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_moviesdat',
                'num_epoch': 50,
                'batch_size': 1024,
                'optimizer': 'adam',
                'adam_lr': 1e-3,
                'num_users': 11142,
                'num_items': 2949,
                'latent_dim_mf': 8,
                'latent_dim_mlp': 8,
                'num_negative': 4,
                'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
                'l2_regularization': 0.01,
                'use_cuda': True,
                'device_id': 3,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('gmf_moviesdat_Epoch45_HR0.0066_NDCG0.0125.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('mlp_moviesdat_Epoch25_HR0.0066_NDCG0.0122.model'),
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }
##################################################################################################################
##################################################################################################################
# yahoo_all config
gmf_config = {'alias': 'gmf_yahoo',
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
              'num_users': 19151,
              'num_items': 17711,
              'latent_dim': 8,
              'num_negative': 4,
              'l2_regularization': 0, # 0.01
              'use_cuda': True,
              'device_id': 3,
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_yahoo',
              'num_epoch': 50,
              'batch_size': 256,  # 1024,
              'optimizer': 'adam',
              'adam_lr': 1e-3,
              'num_users': 19151,
              'num_items': 17711,
              'latent_dim': 8,
              'num_negative': 4,
              'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
              'l2_regularization': 0.0000001,  # MLP model is sensitive to hyper params
              'use_cuda': True,
              'device_id': 3,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('gmf_yahoo_Epoch38_HR0.0429_NDCG0.0777.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_yahoo',
                'num_epoch': 50,
                'batch_size': 1024,
                'optimizer': 'adam',
                'adam_lr': 1e-3,
                'num_users': 19151,
                'num_items': 17711,
                'latent_dim_mf': 8,
                'latent_dim_mlp': 8,
                'num_negative': 4,
                'layers': [16,64,32,16,8],  # layers[0] is the concat of latent user vector & latent item vector
                'l2_regularization': 0.01,
                'use_cuda': True,
                'device_id': 3,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('gmf_yahoo_Epoch38_HR0.0429_NDCG0.0777.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('mlp_yahoo_Epoch49_HR0.0406_NDCG0.0752.model'),
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }
##################################################################################################################
##################################################################################################################
# amazonbooks config
gmf_config = {'alias': 'gmf_amazonbooks',
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
              'device_id': 1,
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

mlp_config = {'alias': 'mlp_amazonbooks',
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
              'device_id': 1,
              'pretrain': True,
              'pretrain_mf': 'checkpoints/{}'.format('gmf_amazonbooks_Epoch49_HR0.0254_NDCG0.0471.model'),
              'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'}

neumf_config = {'alias': 'neumf_amazonbooks',
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
                'device_id': 1,
                'pretrain': True,
                'pretrain_mf': 'checkpoints/{}'.format('gmf_amazonbooks_Epoch49_HR0.0254_NDCG0.0471.model'),
                'pretrain_mlp': 'checkpoints/{}'.format('mlp_amazonbooks_Epoch47_HR0.0455_NDCG0.0852.model'),
                'model_dir':'checkpoints/{}_Epoch{}_HR{:.4f}_NDCG{:.4f}.model'
                }
##################################################################################################################
