# Architecture

## Internal Dependencies

- `app.py` -> `model.py`
- `model.py` -> `src/quaternion_ops.py`
- `model.py` -> `src/ucf101_dataset.py`
- `tests/test_ucf101_dataset.py` -> `src/ucf101_dataset.py`

## External Imports

- `model.py` -> PIL, argparse, collections, dataclasses, json, logging, math, numpy, os, pathlib, safetensors.torch, signal, subprocess, sys, tempfile, time, torch, torch.nn, torch.nn.functional, torch.utils.checkpoint, typing, unittest, wandb
- `src/quaternion_ops.py` -> torch, torch.nn
- `src/ucf101_dataset.py` -> collections, dataclasses, logging, pathlib, shutil, ssl, subprocess, torch, torch.nn.functional, torch.utils.data, torchcodec.decoders, torchvision.io, typing, urllib.error, urllib.request, zipfile
- `tests/test_ucf101_dataset.py` -> os, pathlib, shutil, tempfile, torch, torchcodec.encoders, torchvision.io, typing, unittest
