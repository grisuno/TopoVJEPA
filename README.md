# Topo V-JEPA: Quaternion-Enhanced Video World Model

A quaternion-enhanced Video Joint-Embedding Predictive Architecture with
continuous spectral autoencoders, Fourier-domain topology, and a 2D torus
latent space for world model learning.

## Architecture

- **Quaternion algebra** for spatiotemporal representations (Hamilton product)
- **Complex spectral kernels** with real (conservative) / imaginary (dissipative) dynamics in Fourier domain
- **2D Torus brain** replacing standard FFN: 4 angular x 2 radial = 8 nodes, fully periodic
- **V-JEPA asymmetric masking**: encoder sees ~10% visible patches, predictor predicts ~75% of masked
- **Phase diagram tracking**: delta, kappa, T_eff, alpha, Berry phase, GOE/GUE statistics
- **GQA attention** with Rotary Position Embeddings
- **Topological MoE** with load-balancing auxiliary loss

## Requirements

- Python 3.10+
- PyTorch 2.0+
- NumPy
- torchcodec or torchvision with PyAV (for UCF101 video decoding)

## Quick Start

```bash
# Run tests
python model.py --test

# Run UCF101 dataset tests
python -m pytest tests/test_ucf101_dataset.py -v

# Train micro scale (2.4M params, 128x128 video)
python model.py --mode train --scale micro --epochs 10 --batch_size 4

# Train small scale (88M params, 224x224 video)
python model.py --mode train --scale small --epochs 100

# Train with custom batch size
python model.py --mode train --scale micro --epochs 5 --batch_size 2

# Train with workers to activate MoE
python model.py --mode train --scale small --epochs 1 --batch_size 16 --num_workers 8

# Fine-tune on UCF101 (videos must be pre-downloaded)
python model.py --mode train --scale micro --data_mode ucf101 --epochs 20 --batch_size 8

# Fine-tune with custom UCF101 settings
python model.py --mode train --scale micro --data_mode ucf101 --epochs 20 --batch_size 8

# Generate
python model.py --mode generate --scale small --epochs 1 --backbone checkpoints_vjepa_q/latest.safetensors  

# Run inference (saves .pt with tensors)                                                                                                                                                      
python model.py --mode infer --scale small --resume checkpoints_vjepa_q_generator/decoder_latest.safetensors --output /tmp/my_video.pt

# Convert .pt to MP4 videos
python model.py --mode visualize --input /tmp/my_video.pt --output /tmp/generated.mp4
```

## Example

https://github.com/user-attachments/assets/b3be4788-fb91-4488-abe7-6dd2f5716aa5

## Scale Presets

| Scale | D_MODEL | Heads | Layers | Params | Image Size | Frames |
|-------|---------|-------|--------|--------|------------|--------|
| micro | 128     | 4     | 4      | 2.4M   | 128x128    | 8      |
| small | 384     | 6     | 12     | 88M    | 224x224    | 16     |
| medium| 768     | 12    | 24     | ~350M  | 224x224    | 16     |

## Dataset

### Synthetic MovingShapes (default)

Generates synthetic **MovingShapes** videos on-the-fly:
- Coloured geometric shapes (circles, squares) with bounce physics
- Multiple objects with occlusion
- Configurable canvas size and object count
- Zero bytes disk usage
- 10,000 unique samples per seed

No external data download required. Optionally load `.mp4`/`.avi` files via `--video_dir`.

### UCF101 Fine-Tuning (data_mode=ucf101)

Real human action videos from the UCF101 dataset (101 action classes).

**Setup:**
1. Download UCF101 videos from https://www.crcv.ucf.edu/data/UCF101/UCF101.rar
2. Extract into `./data/ucf101/UCF101/` preserving subdirectory structure
3. Annotations are auto-downloaded, or manually place them from https://www.crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-RecognitionTask.zip

**Key parameters (in model.py VJEPAQConfig):**
| Parameter | Default | Description |
|-----------|---------|-------------|
| `DATA_MODE` | `'synthetic'` | Set to `'ucf101'` to use UCF101 dataset |
| `UCF101_ROOT` | `'./data/ucf101'` | Root directory for UCF101 data |
| `UCF101_OUTPUT_SIZE` | `(64, 64)` | Target frame size (H, W) for resize |
| `UCF101_RESIZE` | `True` | Enable/disable frame resizing |
| `UCF101_FRAMES_PER_CLIP` | `16` | Frames per clip |
| `UCF101_DOWNLOAD_ANNOTATIONS` | `False` | Auto-download annotation files |
| `UCF101_SPLIT_INDEX` | `1` | Train/test split fold (1-3) |

**CLI usage:**
```bash
python model.py --mode train --scale micro --data_mode ucf101 --epochs 20
```

For fine-tuning a pre-trained backbone at 64x64 resolution:
```bash
python model.py --mode train --scale micro --data_mode ucf101 --epochs 20 --backbone /path/to/backbone.safetensors
```

## Testing

```bash
# Run all model tests
python model.py --test

# Run UCF101 dataset tests
python -m pytest tests/test_ucf101_dataset.py -v

# Run specific test class
python model.py --test TestUCF101Config

# Run specific test method
python model.py --test TestVideoPatchEmbedding.test_forward_shape_matches_config
```

## Configuration

All hyperparameters in `VJEPAQConfig` dataclass (model.py:54). No hardcoded
values or magic numbers exist outside this class. Override any field:

```python
config = VJEPAQConfig(
    D_MODEL=256,
    N_HEADS=8,
    NUM_FRAMES=32,
    TORUS_SOFT_ASSIGN_TEMPERATURE=0.5,
)
```

UCF101 dataset has its own `UCF101Config` dataclass (src/ucf101_dataset.py:60).

## Module Structure

```
.
├── model.py                    # VJEPAQ model + trainers + synthetic data
├── src/
│   ├── __init__.py
│   └── ucf101_dataset.py       # UCF101 dataset contract
├── spec/
│   └── ucf101_dataset.md       # BDD specification
├── tests/
│   └── test_ucf101_dataset.py  # UCF101 test suite
└── ...
```

## License

AGPL v3. Gris Iscomeback.
