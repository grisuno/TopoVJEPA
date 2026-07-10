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

## Quick Start

```bash
# Run tests
python model.py --test

# Train micro scale (2.4M params, 128x128 video)
python model.py --mode train --scale micro --epochs 10 --batch_size 4

# Train small scale (88M params, 224x224 video)
python model.py --mode train --scale small --epochs 100

# Train with custom batch size
python model.py --mode train --scale micro --epochs 5 --batch_size 2

# Train with workers to activate MoE
python model.py --mode train --scale small --epochs 1 --batch_size 16 --num_workers 8

# Generate
python model.py --mode generate --scale small --epochs 1 --backbone checkpoints_vjepa_q/latest.safetensors  

# Run inference (saves .pt with tensors)                                                                                                                                                      
python model.py --mode infer --scale small --resume checkpoints_vjepa_q_generator/decoder_latest.safetensors --output /tmp/my_video.pt

# Convert .pt to MP4 videos
python model.py --mode visualize --input /tmp/my_video.pt --output /tmp/generated.mp4


```

## Scale Presets

| Scale | D_MODEL | Heads | Layers | Params | Image Size | Frames |
|-------|---------|-------|--------|--------|------------|--------|
| micro | 128     | 4     | 4      | 2.4M   | 128x128    | 8      |
| small | 384     | 6     | 12     | 88M    | 224x224    | 16     |
| medium| 768     | 12    | 24     | ~350M  | 224x224    | 16     |

## Dataset

Generates synthetic **MovingShapes** videos on-the-fly:
- Coloured geometric shapes (circles, squares) with bounce physics
- Multiple objects with occlusion
- Configurable canvas size and object count
- Zero bytes disk usage
- 10,000 unique samples per seed

No external data download required. Optionally load `.mp4`/`.avi` files via `--video_dir`.

## Testing

```bash
# Run all tests
python model.py --test

# Run specific test class
python model.py --test TestQuaternionOps

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


## License

AGPL v3. Gris Iscomeback.
