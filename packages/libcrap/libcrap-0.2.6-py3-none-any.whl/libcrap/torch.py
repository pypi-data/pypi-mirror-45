from typing import Union

import torch

def inverse_sigmoid(x: torch.Tensor) -> torch.Tensor:
    """Inverse of the sigmoid function, i.e., for any x,
    inverse_sigmoid(torch.sigmoid(x)) approximately equals x."""
    return torch.log(x / (torch.tensor(1.0, device=x.device) - x))
