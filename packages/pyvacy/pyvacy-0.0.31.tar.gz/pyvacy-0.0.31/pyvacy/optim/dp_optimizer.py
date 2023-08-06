import torch
from torch.optim import Optimizer
from torch.nn.utils.clip_grad import clip_grad_norm_
from torch.distributions.normal import Normal
from torch.optim import SGD, Adam, Adagrad, RMSprop

def make_optimizer_class(cls):

    class DPOptimizerClass(cls):

        def __init__(self, l2_norm_clip, noise_multiplier, batch_size, *args, **kwargs):
            """
            Args:
                l2_norm_clip (float): An upper bound on the 2-norm of the gradient w.r.t. the model parameters
                noise_multiplier (float): The ratio between the clipping parameter and the std of noise applied
                batch_size (int): Number of examples per batch
            """
            self.l2_norm_clip = l2_norm_clip
            self.noise = Normal(0.0, noise_multiplier * l2_norm_clip / (batch_size ** 0.5))
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            super(DPOptimizerClass, self).__init__(*args, **kwargs)

        def step(self, closure=None):
            # Calculate total gradient
            total_norm = 0
            for group in self.param_groups:
                for p in filter(lambda p: p.grad is not None, group['params']):
                    param_norm = p.grad.data.norm(2.)
                    total_norm += param_norm.item() ** 2.
                total_norm = total_norm ** (1. / 2.)

            # Calculate clipping coefficient, apply if nontrivial
            clip_coef = self.l2_norm_clip / (total_norm + 1e-6)
            if clip_coef < 1:
                for group in self.param_groups:
                    for p in filter(lambda p: p.grad is not None, group['params']):
                            p.grad.data.mul_(clip_coef)

            # Inject noise
            for group in self.param_groups:
                for p in filter(lambda p: p.grad is not None, group['params']):
                    p.grad.data.add_(self.noise.sample(p.grad.data.size()).to(self.device))

            super(DPOptimizerClass, self).step(closure)

    return DPOptimizerClass

DPAdam = make_optimizer_class(Adam)
DPAdagrad = make_optimizer_class(Adagrad)
DPSGD = make_optimizer_class(SGD)
DPRMSprop = make_optimizer_class(RMSprop)

