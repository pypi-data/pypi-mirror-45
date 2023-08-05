import json
from pathlib import Path

import jsonschema
import torch.nn
import torch.optim
import torch_model_loader

from .configs import OptimizerConfig
from .group_parameters import group_parameters
from .group_rule import GroupRule

# register common optimizers
torch_model_loader.register(torch.optim.SGD, tag='optimizer')
torch_model_loader.register(torch.optim.Adam, tag='optimizer')
torch_model_loader.register(torch.optim.RMSprop, tag='optimizer')

with open(str(Path(__file__).parent / 'schema' / 'optimizer_config.json')) as f:
    schema = json.load(f)


def optimizer_factory(model: torch.nn.Module, config: dict = None) -> torch.optim.Optimizer:
    jsonschema.validate(config or {}, schema)
    config = OptimizerConfig(config)

    rules = list(map(GroupRule.factory, config.rules))
    param_groups = group_parameters(model=model, rules=rules)

    params = []
    for param_group, rule in zip(param_groups, rules):
        if rule.refuse_if_match is False:
            kwargs = {'weight_decay': rule.weight_decay} if rule.weight_decay is not None else {}
            params.append({
                'params': param_group,
                **kwargs
            })

    optimizer_class: torch.optim.Optimizer = torch_model_loader.load(config.type, tag='optimizer')
    return optimizer_class(params=params, lr=config.lr, **config.kwargs)
