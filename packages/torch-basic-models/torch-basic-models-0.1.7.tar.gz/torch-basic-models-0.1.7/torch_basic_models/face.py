import json
import math
from pathlib import Path

import box
import jsonschema
import torch
import torch.nn as nn

from .configs import ArcFaceConfig


def l2_norm(x, axis=1):
    norm = torch.norm(x, 2, axis, True)
    output = torch.div(x, norm)
    return output


@box.register(tag='model')
class ArcFace(nn.Module):
    """
    ArcFace loss for face recognition
    refer to https://github.com/TreB1eN/InsightFace_Pytorch/blob/master/model.py#L242
    """
    with open(str(Path(__file__).parent / 'schema' / 'arc_face_config.json')) as f:
        schema = json.load(f)

    def __init__(self, config: ArcFaceConfig):
        super().__init__()
        self.num_classes = config.num_classes
        self.kernel = nn.Parameter(torch.Tensor(config.feature_dim, config.num_classes))
        # initial kernel
        self.kernel.data.uniform_(-1, 1).renorm_(2, 1, 1e-5).mul_(1e5)
        self.m = config.m  # the margin value, default is 0.5
        self.s = config.s  # scalar value default is 64, see normface https://arxiv.org/abs/1704.06369
        self.cos_m = math.cos(config.m)
        self.sin_m = math.sin(config.m)
        self.mm = self.sin_m * config.m  # issue 1
        self.threshold = math.cos(math.pi - config.m)

    def forward(self, feature: torch.Tensor, label: torch.Tensor):
        # weights norm
        batch_size = feature.size(0)
        kernel_norm = l2_norm(self.kernel, axis=0)
        # cos(theta+m)
        cos_theta = torch.mm(feature, kernel_norm)
        cos_theta = cos_theta.clamp(-1, 1)  # for numerical stability
        cos_theta_2: torch.Tensor = torch.pow(cos_theta, 2)
        sin_theta_2: torch.Tensor = cos_theta_2.neg().add(1)
        sin_theta = torch.sqrt(sin_theta_2)
        cos_theta_m = (cos_theta * self.cos_m - sin_theta * self.sin_m)
        # this condition controls the theta+m should in range [0, pi]
        #      0<=theta+m<=pi
        #     -m<=theta<=pi-m
        cond_v = cos_theta - self.threshold
        cond_mask = cond_v <= 0
        keep_val = (cos_theta - self.mm)  # when theta not in [0,pi], use cosface instead
        cos_theta_m[cond_mask] = keep_val[cond_mask]
        output = cos_theta * 1.0  # a little bit hacky way to prevent in_place operation on cos_theta
        idx_ = torch.arange(0, batch_size, dtype=torch.long)
        output[idx_, label] = cos_theta_m[idx_, label]
        output *= self.s  # scale up in order to make softmax work, first introduced in normface
        return output

    @classmethod
    def factory(cls, config: dict):
        jsonschema.validate(config or {}, cls.schema)
        return cls(config=ArcFaceConfig(values=config))
