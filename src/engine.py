import torch
from torch.autograd import Variable
from tensorboardX import SummaryWriter

from utils import save_checkpoint, use_optimizer
from metrics import MetronAtK


class Engine(object):
    """Meta Engine for training & evaluating NCF model

    Note: Subclass should implement self.model !
    """

    def __init__(self, config):
        self.config = config  # model configuration
        self._metron = MetronAtK(top_k=[5, 10, 20])
        self._writer = SummaryWriter(log_dir='runs/{}'.format(config['alias']))  # tensorboard writer
        self._writer.add_text('config', str(config), 0)
        self.opt = use_optimizer(self.model, config)
        # explicit feedback
        # self.crit = torch.nn.MSELoss()
        # implicit feedback
        self.crit = torch.nn.BCELoss()

    def train_single_batch(self, users, items, ratings):
        assert hasattr(self, 'model'), 'Please specify the exact model !'
        if self.config['use_cuda'] is True:
            users, items, ratings = users.cuda(), items.cuda(), ratings.cuda()
        self.opt.zero_grad()
        ratings_pred = self.model(users, items)
        loss = self.crit(ratings_pred.view(-1), ratings)
        loss.backward()
        self.opt.step()
        loss = loss.item()
        return loss

    def train_an_epoch(self, train_loader, epoch_id):
        assert hasattr(self, 'model'), 'Please specify the exact model !'
        self.model.train()
        total_loss = 0
        for batch_id, batch in enumerate(train_loader):
            assert isinstance(batch[0], torch.LongTensor)
            user, item, rating = batch[0], batch[1], batch[2]
            rating = rating.float()
            loss = self.train_single_batch(user, item, rating)
            print('[Training Epoch {}] Batch {}, Loss {}'.format(epoch_id, batch_id, loss))
            total_loss += loss
        self._writer.add_scalar('model/loss', total_loss, epoch_id)

    def evaluate(self, evaluate_data, epoch_id):
        assert hasattr(self, 'model'), 'Please specify the exact model !'
        self.model.eval()
        with torch.no_grad():
            test_users, test_items = evaluate_data[0], evaluate_data[1]
            negative_users, negative_items = evaluate_data[2], evaluate_data[3]
            if self.config['use_cuda'] is True:
                test_users = test_users.cuda()
                test_items = test_items.cuda()
                negative_users = negative_users.cuda()
                negative_items = negative_items.cuda()
            test_scores = self.model(test_users, test_items)
            #negative_scores = self.model(negative_users, negative_items)
            batches = 25
            batch_size = int(len(negative_users) / batches)
            neg_users = torch.split(negative_users, batch_size)
            neg_items = torch.split(negative_items, batch_size)
            negative_scores = self.model(neg_users[0], neg_items[0])
            for part in range(1, len(neg_users)):
                neg_scores = self.model(neg_users[part], neg_items[part])
                negative_scores = torch.cat((negative_scores, neg_scores))
            if self.config['use_cuda'] is True:
                test_users = test_users.cpu()
                test_items = test_items.cpu()
                test_scores = test_scores.cpu()
                negative_users = negative_users.cpu()
                negative_items = negative_items.cpu()
                negative_scores = negative_scores.cpu()
            self._metron.subjects = [test_users.data.view(-1).tolist(),
                                 test_items.data.view(-1).tolist(),
                                 test_scores.data.view(-1).tolist(),
                                 negative_users.data.view(-1).tolist(),
                                 negative_items.data.view(-1).tolist(),
                                 negative_scores.data.view(-1).tolist(), epoch_id]
        mpr = self._metron.cal_mpr()
        hit_ratio, mrr, ndcg = self._metron.cal_hit_ratio(), self._metron.cal_mrr(), self._metron.cal_ndcg()
        hit_ratio1, hit_ratio2, hit_ratio3 = hit_ratio
        mrr1, mrr2, mrr3 = mrr
        ndcg1, ndcg2, ndcg3 = ndcg
        self._writer.add_scalar('performance/HR@5', hit_ratio1, epoch_id)
        self._writer.add_scalar('performance/HR@10', hit_ratio2, epoch_id)
        self._writer.add_scalar('performance/HR@20', hit_ratio3, epoch_id)
        self._writer.add_scalar('performance/MRR@5', mrr1, epoch_id)
        self._writer.add_scalar('performance/MRR@10', mrr2, epoch_id)
        self._writer.add_scalar('performance/MRR@20', mrr3, epoch_id)
        self._writer.add_scalar('performance/MPR', mpr, epoch_id)
        self._writer.add_scalar('performance/NDCG@5', ndcg1, epoch_id)
        self._writer.add_scalar('performance/NDCG@10', ndcg2, epoch_id)
        self._writer.add_scalar('performance/NDCG@20', ndcg3, epoch_id)
        print('[Evluating Epoch {}] HR = {:.4f}, MRR = {:.4f}, MPR = {:.4f}, NDCG = {:.4f}'.format(epoch_id, hit_ratio2, mrr2, mpr, ndcg2))
        return hit_ratio1,hit_ratio2,hit_ratio3, mrr1, mrr2, mrr3, mpr, ndcg1, ndcg2, ndcg3

    def save(self, alias, epoch_id, hit_ratio1,hit_ratio2,hit_ratio3, mrr1, mrr2, mrr3, mpr, ndcg1, ndcg2, ndcg3):
        assert hasattr(self, 'model'), 'Please specify the exact model !'
        model_dir = self.config['model_dir'].format(alias, epoch_id, hit_ratio1,hit_ratio2,hit_ratio3, mrr1, mrr2, mrr3, mpr, ndcg1, ndcg2, ndcg3)
        save_checkpoint(self.model, model_dir)