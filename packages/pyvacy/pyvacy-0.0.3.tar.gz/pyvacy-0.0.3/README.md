<div align="center">
    <img src="assets/logo.png" width="150px"><br>
    <h1>PyVacy: Privacy Algorithms for PyTorch</h1>
</div>

PyVacy provides custom PyTorch opimizers for conducting deep learning in a differentially private manner. Basically <a href="https://github.com/tensorflow/privacy">TensorFlow Privacy</a>, but for PyTorch.

## Getting Started

```bash
pip install pyvacy
```

## Example Usage

```python
import torch

from pyvacy import optim
from pyvacy.analysis import moments_accountant

model = torch.nn.Sequential(...)

optimizer = optim.DPSGD(
    l2_norm_clip=...,
    noise_multiplier=...,
    batch_size=...,
    lr=...,
    momentum=...,
)

epsilon = moments_accountant.epsilon(
    N=...,
    batch_size=...
    noise_multiplier=...,
    epochs=...,
    delta=...,
)

for epoch in range(epochs):
    # do training as usual...
```

## Tutorials

```python
python tutorials/mnist.py

Training procedure achieves (3.0, 0.00001)-DP
[Epoch 1/60] [Batch 0/235] [Loss: 2.321049]
[Epoch 1/60] [Batch 10/235] [Loss: 0.952795]
[Epoch 1/60] [Batch 20/235] [Loss: 1.040896]
...
```
