# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM.
> No LLMs. No tokens. Pure static analysis. See more [here](https://github.com/grisuno/ReadMenator)

**Total Files Parsed:** 6 | **Total Symbols Extracted:** 243 | **Total Imports:** 73

## Structural Knowledge Map
```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray:5 5,color:#aaa;
    tests_test_ucf101_dataset_py["test_ucf101_dataset.py (py)"]
    class tests_test_ucf101_dataset_py mod;
    tests_test_ucf101_dataset_py__make_test_video["_make_test_video"]
    class tests_test_ucf101_dataset_py__make_test_video fn;
    tests_test_ucf101_dataset_py --> tests_test_ucf101_dataset_py__make_test_video
    tests_test_ucf101_dataset_py__make_annotation_files["_make_annotation_files"]
    class tests_test_ucf101_dataset_py__make_annotation_files fn;
    tests_test_ucf101_dataset_py --> tests_test_ucf101_dataset_py__make_annotation_files
    tests_test_ucf101_dataset_py_TestUCF101Config["TestUCF101Config"]
    class tests_test_ucf101_dataset_py_TestUCF101Config cls;
    tests_test_ucf101_dataset_py --> tests_test_ucf101_dataset_py_TestUCF101Config
    tests_test_ucf101_dataset_py_TestUCF101DatasetInit["TestUCF101DatasetInit"]
    class tests_test_ucf101_dataset_py_TestUCF101DatasetInit cls;
    tests_test_ucf101_dataset_py --> tests_test_ucf101_dataset_py_TestUCF101DatasetInit
    tests_test_ucf101_dataset_py_TestUCF101DatasetGetItem["TestUCF101DatasetGetItem"]
    class tests_test_ucf101_dataset_py_TestUCF101DatasetGetItem cls;
    tests_test_ucf101_dataset_py --> tests_test_ucf101_dataset_py_TestUCF101DatasetGetItem
    model_py["model.py (py)"]
    class model_py mod;
    model_py_VJEPAQConfig["VJEPAQConfig"]
    class model_py_VJEPAQConfig cls;
    model_py --> model_py_VJEPAQConfig
    model_py__setup_logger["_setup_logger"]
    class model_py__setup_logger fn;
    model_py --> model_py__setup_logger
    model_py__set_seed["_set_seed"]
    class model_py__set_seed fn;
    model_py --> model_py__set_seed
    model_py__count_parameters["_count_parameters"]
    class model_py__count_parameters fn;
    model_py --> model_py__count_parameters
    model_py_QuaternionOps["QuaternionOps"]
    class model_py_QuaternionOps cls;
    model_py --> model_py_QuaternionOps
    src_ucf101_dataset_py["ucf101_dataset.py (py)"]
    class src_ucf101_dataset_py mod;
    src_ucf101_dataset_py__detect_video_backend["_detect_video_backend"]
    class src_ucf101_dataset_py__detect_video_backend fn;
    src_ucf101_dataset_py --> src_ucf101_dataset_py__detect_video_backend
    src_ucf101_dataset_py_VideoBackendError["VideoBackendError"]
    class src_ucf101_dataset_py_VideoBackendError cls;
    src_ucf101_dataset_py --> src_ucf101_dataset_py_VideoBackendError
    src_ucf101_dataset_py_RarExtractError["RarExtractError"]
    class src_ucf101_dataset_py_RarExtractError cls;
    src_ucf101_dataset_py --> src_ucf101_dataset_py_RarExtractError
    src_ucf101_dataset_py_SecurityError["SecurityError"]
    class src_ucf101_dataset_py_SecurityError cls;
    src_ucf101_dataset_py --> src_ucf101_dataset_py_SecurityError
    src_ucf101_dataset_py_UCF101Config["UCF101Config"]
    class src_ucf101_dataset_py_UCF101Config cls;
    src_ucf101_dataset_py --> src_ucf101_dataset_py_UCF101Config
    app_py["app.py (py)"]
    class app_py mod;
    install_sh["install.sh (sh)"]
    class install_sh mod;
    src___init___py["__init__.py (py)"]
    class src___init___py mod;
    ext_model["model"]
    class ext_model ext;
    app_py -.->|imports| ext_model
    ext_argparse["argparse"]
    class ext_argparse ext;
    model_py -.->|imports| ext_argparse
    ext_json["json"]
    class ext_json ext;
    model_py -.->|imports| ext_json
    ext_logging["logging"]
    class ext_logging ext;
    model_py -.->|imports| ext_logging
    ext_math["math"]
    class ext_math ext;
    model_py -.->|imports| ext_math
    ext_sys["sys"]
    class ext_sys ext;
    model_py -.->|imports| ext_sys
    ext_time["time"]
    class ext_time ext;
    model_py -.->|imports| ext_time
    ext_unittest["unittest"]
    class ext_unittest ext;
    model_py -.->|imports| ext_unittest
    ext_collections["collections"]
    class ext_collections ext;
    model_py -.->|imports| ext_collections
    ext_dataclasses["dataclasses"]
    class ext_dataclasses ext;
    model_py -.->|imports| ext_dataclasses
    ext_pathlib["pathlib"]
    class ext_pathlib ext;
    model_py -.->|imports| ext_pathlib
    ext_typing["typing"]
    class ext_typing ext;
    model_py -.->|imports| ext_typing
    ext_numpy["numpy"]
    class ext_numpy ext;
    model_py -.->|imports| ext_numpy
    ext_torch["torch"]
    class ext_torch ext;
    model_py -.->|imports| ext_torch
    ext_torch_nn["torch.nn"]
    class ext_torch_nn ext;
    model_py -.->|imports| ext_torch_nn
    ext_safetensors_torch["safetensors.torch"]
    class ext_safetensors_torch ext;
    model_py -.->|imports| ext_safetensors_torch
    ext_torch_nn_functional["torch.nn.functional"]
    class ext_torch_nn_functional ext;
    model_py -.->|imports| ext_torch_nn_functional
    ext_torch_utils_checkpoint["torch.utils.checkpoint"]
    class ext_torch_utils_checkpoint ext;
    model_py -.->|imports| ext_torch_utils_checkpoint
    ext_subprocess["subprocess"]
    class ext_subprocess ext;
    model_py -.->|imports| ext_subprocess
    ext_tempfile["tempfile"]
    class ext_tempfile ext;
    model_py -.->|imports| ext_tempfile
    ext_os["os"]
    class ext_os ext;
    model_py -.->|imports| ext_os
    ext_PIL["PIL"]
    class ext_PIL ext;
    model_py -.->|imports| ext_PIL
    ext_src_ucf101_dataset["src.ucf101_dataset"]
    class ext_src_ucf101_dataset ext;
    model_py -.->|imports| ext_src_ucf101_dataset
    model_py -.->|imports| ext_sys
    src_ucf101_dataset_py -.->|imports| ext_logging
    ext_shutil["shutil"]
    class ext_shutil ext;
    src_ucf101_dataset_py -.->|imports| ext_shutil
    ext_ssl["ssl"]
    class ext_ssl ext;
    src_ucf101_dataset_py -.->|imports| ext_ssl
    src_ucf101_dataset_py -.->|imports| ext_subprocess
    ext_urllib_error["urllib.error"]
    class ext_urllib_error ext;
    src_ucf101_dataset_py -.->|imports| ext_urllib_error
    ext_urllib_request["urllib.request"]
    class ext_urllib_request ext;
    src_ucf101_dataset_py -.->|imports| ext_urllib_request
    ext_zipfile["zipfile"]
    class ext_zipfile ext;
    src_ucf101_dataset_py -.->|imports| ext_zipfile
    src_ucf101_dataset_py -.->|imports| ext_dataclasses
    src_ucf101_dataset_py -.->|imports| ext_pathlib
    src_ucf101_dataset_py -.->|imports| ext_typing
    src_ucf101_dataset_py -.->|imports| ext_torch
    src_ucf101_dataset_py -.->|imports| ext_torch_nn_functional
    ext_torch_utils_data["torch.utils.data"]
    class ext_torch_utils_data ext;
    src_ucf101_dataset_py -.->|imports| ext_torch_utils_data
    ext_torchcodec_decoders["torchcodec.decoders"]
    class ext_torchcodec_decoders ext;
    src_ucf101_dataset_py -.->|imports| ext_torchcodec_decoders
    ext_torchvision_io["torchvision.io"]
    class ext_torchvision_io ext;
    src_ucf101_dataset_py -.->|imports| ext_torchvision_io
    src_ucf101_dataset_py -.->|imports| ext_torchcodec_decoders
    src_ucf101_dataset_py -.->|imports| ext_torchvision_io
    tests_test_ucf101_dataset_py -.->|imports| ext_os
    tests_test_ucf101_dataset_py -.->|imports| ext_shutil
    tests_test_ucf101_dataset_py -.->|imports| ext_tempfile
    tests_test_ucf101_dataset_py -.->|imports| ext_unittest
    tests_test_ucf101_dataset_py -.->|imports| ext_pathlib
    tests_test_ucf101_dataset_py -.->|imports| ext_typing
    tests_test_ucf101_dataset_py -.->|imports| ext_torch
    ext_torchcodec_encoders["torchcodec.encoders"]
    class ext_torchcodec_encoders ext;
    tests_test_ucf101_dataset_py -.->|imports| ext_torchcodec_encoders
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_src_ucf101_dataset
    tests_test_ucf101_dataset_py -.->|imports| ext_torchvision_io
    tests_test_ucf101_dataset_py -.->|imports| ext_torchvision_io
```

---

## Architecture Reference

### PY (5 files)

#### `app.py`
**Path:** `app.py`

*No symbols extracted*

#### `model.py`
**Path:** `model.py`

**Classes:**
- `VJEPAQConfig` (line 46) `class VJEPAQConfig` - *Central configuration for V-JEPA-Q model and training.

All hyperparameters defined here. No hardcoded values or magic numbers
exist outside this class. Computed fields in __post_init__.*
- `QuaternionOps` (line 213) `class QuaternionOps` - *Pure quaternion operations. Convention: [w, x, y, z].

Includes exponential and logarithmic maps for the Lie group SU(2) / so(3).
The log map converts quaternion multiplication to vector addition in the
tangent space (Lie algebra). The exp map converts back.*
- `QuaternionLinear` (line 290) `class QuaternionLinear` - *Linear transform using quaternion Hamilton product.

Input and output dimensions must be multiples of 4. Weight is
factorised into four coupled subspaces via Hamilton product.*
- `ComplexSpectralLayer` (line 328) `class ComplexSpectralLayer` - *Spectral convolution with tuneable real/imaginary kernel ratio.

Operates in 2D Fourier domain: P(k) = W(k) * X(k) with channel mixing
via einsum. Real part: conservative dynamics. Imaginary part: dissipative.
Tracks GOE -> GUE transition via imaginary_ratio.*
- `QuaternionSpectralLayer` (line 404) `class QuaternionSpectralLayer` - *Full quaternion spectral convolution in Fourier domain.

Each quaternion component (w, x, y, z) gets a complex kernel.
Combined via Hamilton product in frequency space using Gauss's trick
(3 real MUL instead of 4 for complex multiply).*
- `SpatiotemporalSpectralAE` (line 487) `class SpatiotemporalSpectralAE` - *Two-level spectral autoencoder: temporal FFT + spatial quaternion spectral.*
- `VideoPatchEmbedding` (line 537) `class VideoPatchEmbedding` - *Convert video to quaternion-encoded patch embeddings with motion cues.

Extracts spatial patches and temporal derivative, then projects to
D_MODEL-dimensional quaternion space with position encodings.*
- `VJEPAMasker` (line 613) `class VJEPAMasker` - *Generate asymmetric encoder/predictor masks for V-JEPA training.*
- `RotaryEmbedding` (line 676) `class RotaryEmbedding` - *Rotary Position Embeddings (RoPE) for spatiotemporal attention.*
- `RMSNorm` (line 708) `class RMSNorm` - *Root Mean Square Layer Normalisation.*
- `SpatiotemporalAttention` (line 726) `class SpatiotemporalAttention` - *Grouped-Query Attention with RoPE for spatiotemporal sequences.*
- `QuaternionTorusBrain` (line 788) `class QuaternionTorusBrain` - *FFN replacement with quaternion-topological processing on a 2D torus.

Pipeline:
1. Token compression (no temporal FFT per token)
2. Project to torus coordinates (phi1, phi2)
3. Soft-assignment to 8 torus nodes (4 angular x 2 radial)
4. Lightweight channel mixer on torus grid
5. Message passing with Lie algebra (exp/log) quaternion product
6. Attention-weighted readout

The Lie algebra trick (TORUS_LIE_APPROX) replaces the Hamilton product
in message passing with log-space addition: exp(log(q1) + log(q2)).
This converts O(n^2) quaternion multiplications to O(n) element-wise adds.*
- `TopoMoE` (line 971) `class TopoMoE` - *Mixture of Experts with shared Topological Torus Brain.*
- `VJEPAQBlock` (line 1044) `class VJEPAQBlock` - *Transformer block with SpatiotemporalAttention + TopoMoE FFN.*
- `VJEPAQEncoder` (line 1082) `class VJEPAQEncoder` - *Video encoder with quaternion spectral processing.*
- `VJEPAQPredictor` (line 1134) `class VJEPAQPredictor` - *World model predictor: predicts masked patch representations.*
- `PhaseDiagramTracker` (line 1201) `class PhaseDiagramTracker` - *Tracks phase diagram metrics during world model training.

Metrics: delta, kappa, T_eff, alpha, Berry phase, Dyson beta.*
- `VJEPAQ` (line 1404) `class VJEPAQ` - *V-JEPA-Q: Quaternion-Enhanced Video Joint-Embedding Predictive Architecture.*
- `VJEPAQDecoder` (line 1498) `class VJEPAQDecoder` - *Decodes latent predictor tokens into pixel-space video frames.

Pipeline:
1. Linear projection from D_MODEL to PATCH_DIM (reconstructs image patches)
2. Rearrange token sequence into spatial-temporal pixel grid
3. 3D convolutions for temporal-spatial refinement
4. Sigmoid output for normalized pixel values [0, 1]*
- `VJEPAQVideoGenerator` (line 1599) `class VJEPAQVideoGenerator` - *Physically consistent video generator: frozen world model + pixel decoder.

Architecture:
- VJEPAQ backbone loaded from .safetensors (encoder + predictor, frozen)
- VJEPAQDecoder (trainable) converts torus latent states to pixels

Generation pipeline:
1. Context frames → frozen VideoPatchEmbedding + Encoder → visible latents
2. Frozen Predictor rolls out future states in torus latent space
3. Decoder converts predicted latent tokens to video frames*
- `VJEPAQGeneratorTrainer` (line 1689) `class VJEPAQGeneratorTrainer` - *Training loop for the video decoder.

Freezes the V-JEPA-Q backbone and only trains VJEPAQDecoder.
Loss = MSE + temporal gradient penalty for flicker-free video.*
- `MovingShapesDataset` (line 1851) `class MovingShapesDataset` - *Synthetic video dataset with moving geometric shapes (0 bytes on disk).

Generates videos with N coloured shapes (circles and squares) that
move at constant velocity and bounce off walls. Fully deterministic
given seed.*
- `VideoDataset` (line 1969) `class VideoDataset` - *Load video files from directory, falls back to MovingShapes.*
- `VJEPAQTrainer` (line 2012) `class VJEPAQTrainer` - *Training loop for V-JEPA-Q with AMP, gradient clipping, and phase tracking.*
- `TestVJEPAQDecoder` (line 2219) `class TestVJEPAQDecoder` - *Behaviour: decoder converts latent tokens to video frames.*
- `TestVJEPAQVideoGenerator` (line 2258) `class TestVJEPAQVideoGenerator` - *Behaviour: generator produces video from context frames.*
- `TestGeneratorTrainerIntegration` (line 2296) `class TestGeneratorTrainerIntegration` - *Behaviour: generator trainer can complete a step without error.*
- `TestQuaternionOps` (line 2343) `class TestQuaternionOps` - *Behaviour: Quaternion algebra must satisfy unit quaternion properties.*
- `TestQuaternionLinear` (line 2399) `class TestQuaternionLinear` - *Behaviour: QuaternionLinear must preserve quaternion structure.*
- `TestVideoPatchEmbedding` (line 2417) `class TestVideoPatchEmbedding` - *Critical: patch embedding shapes must match config (bug regression test).*
- `TestVJEPAMasker` (line 2445) `class TestVJEPAMasker` - *Behaviour: masks must be valid and consistent.*
- `TestVJEPAQModel` (line 2466) `class TestVJEPAQModel` - *Behaviour: full model forward pass produces valid losses.*
- `TestMovingShapesDataset` (line 2554) `class TestMovingShapesDataset` - *Behaviour: synthetic dataset produces valid video tensors.*
- `TestTrainerIntegration` (line 2589) `class TestTrainerIntegration` - *Behaviour: trainer can complete a training step without error.*
- `TestConfigValidation` (line 2630) `class TestConfigValidation` - *Behaviour: invalid configs must raise AssertionError.*

**Functions:**
- `_setup_logger` (line 186) `def _setup_logger(name, level)`
- `_set_seed` (line 197) `def _set_seed(seed, device)`
- `_count_parameters` (line 204) `def _count_parameters(module)`
- `_visualize_video` (line 2655) `def _visualize_video(input_path, output_path)` - *Load a .pt inference output and render it as .mp4 via ffmpeg.*
- `_create_dataloader` (line 2724) `def _create_dataloader(config)` - *Create dataset and DataLoader based on config.DATA_MODE.*
- `main` (line 2755) `def main()` - *Entry point: parse args, create config, build dataset, train or generate.*
- `__post_init__` (line 138) `def __post_init__(self)`
- `hamilton_product` (line 222) `def hamilton_product(q1, q2)`
- `normalize` (line 233) `def normalize(q, eps)`
- `conjugate` (line 237) `def conjugate(q)`
- `rotate_vector` (line 241) `def rotate_vector(v, q)`
- `log` (line 250) `def log(q, eps)` - *Logarithmic map from SU(2) to so(3) (tangent space).

Converts a unit quaternion q = [w, x, y, z] to a pure quaternion
v = [0, theta*u] where u is the unit axis and theta = arccos(w).
In the tangent space, quaternion multiplication becomes vector addition
(via BCH approximation: log(q1 * q2) approx log(q1) + log(q2)).*
- `exp` (line 266) `def exp(q, eps)` - *Exponential map from so(3) to SU(2).

Converts a pure quaternion v = [0, theta*u] back to a unit quaternion
q = [cos(theta), sin(theta)*u]. This is the inverse of log().*
- `lie_product` (line 278) `def lie_product(q1, q2, eps)` - *Approximate quaternion product via Lie algebra addition.

Instead of Hamilton product (O(n^2) cross terms), uses:
    q1 * q2 approx exp(log(q1) + log(q2))
which converts multiplication to element-wise addition in the
tangent space. Exact for commuting quaternions; BCH-approximate
for non-commuting.*
- `__init__` (line 297) `def __init__(self, in_features, out_features, bias)`
- `forward` (line 312) `def forward(self, x)`
- `__init__` (line 336) `def __init__(self, channels, grid_h, grid_w, imaginary_ratio, init_scale)`
- `set_imaginary_ratio` (line 360) `def set_imaginary_ratio(self, ratio)`
- `get_effective_imaginary_ratio` (line 367) `def get_effective_imaginary_ratio(self)`
- `get_spectral_operator` (line 376) `def get_spectral_operator(self)`
- `forward` (line 383) `def forward(self, x)`
- `__init__` (line 412) `def __init__(self, in_q, out_q, grid_h, grid_w, init_scale)`
- `_kernel` (line 439) `def _kernel(self, c)`
- `_gauss_contract` (line 443) `def _gauss_contract(W, X)`
- `forward` (line 453) `def forward(self, x)`
- `__init__` (line 490) `def __init__(self, config)`
- `_temporal_filter` (line 511) `def _temporal_filter(self, x, kr, ki)`
- `encode_temporal` (line 517) `def encode_temporal(self, x)`
- `decode_temporal` (line 521) `def decode_temporal(self, z)`
- `forward` (line 525) `def forward(self, x)`
- `__init__` (line 544) `def __init__(self, config)`
- `_compute_temporal_derivative` (line 562) `def _compute_temporal_derivative(video)`
- `forward` (line 567) `def forward(self, video)`
- `__init__` (line 616) `def __init__(self, config)`
- `_generate_block_mask` (line 621) `def _generate_block_mask(h, w, mask_ratio, block_size, device)`
- `generate_masks` (line 635) `def generate_masks(self, batch_size, device)`
- `__init__` (line 679) `def __init__(self, d_head, max_seq_len, base)`
- `_build_cache` (line 685) `def _build_cache(self, seq_len)`
- `_rotate_half` (line 692) `def _rotate_half(self, x)`
- `forward` (line 696) `def forward(self, q, k)`
- `__init__` (line 711) `def __init__(self, d_model, eps)`
- `forward` (line 716) `def forward(self, x)`
- `__init__` (line 729) `def __init__(self, d_model, n_heads, config)`
- `forward` (line 745) `def forward(self, x, mask, is_causal)`
- `__init__` (line 804) `def __init__(self, d_model, config)`
- `_build_torus_graph` (line 850) `def _build_torus_graph(self)` - *Build fully periodic 2D torus adjacency.*
- `_torus_soft_assign` (line 879) `def _torus_soft_assign(self, phi1, phi2)`
- `_message_passing` (line 894) `def _message_passing(self, node_feat)` - *Message passing with Lie algebra quaternion product.

When self.lie_approx is True, uses exp(log(q) + log(p)) instead of
Hamilton product q * p. This converts quaternion multiplication to
vector addition in so(3) tangent space via BCH approximation.*
- `forward` (line 926) `def forward(self, x)`
- `__init__` (line 974) `def __init__(self, d_model, config)`
- `_route` (line 994) `def _route(self, x)`
- `forward` (line 1021) `def forward(self, x)`
- `__init__` (line 1047) `def __init__(self, d_model, n_heads, config)`
- `_forward_impl` (line 1056) `def _forward_impl(self, x, mask)`
- `forward` (line 1067) `def forward(self, x, mask)`
- `__init__` (line 1085) `def __init__(self, config)`
- `forward` (line 1096) `def forward(self, video, mask)`
- `__init__` (line 1137) `def __init__(self, config)`
- `forward` (line 1156) `def forward(self, encoder_output, encoder_mask, predictor_mask)`
- `__init__` (line 1207) `def __init__(self, config)`
- `compute_delta` (line 1216) `def compute_delta(self, model)`
- `compute_kappa` (line 1224) `def compute_kappa(self, model, gradient_buffer, max_dim)`
- `compute_t_eff` (line 1242) `def compute_t_eff(self, gradient_buffer, lr)`
- `compute_alpha` (line 1252) `def compute_alpha(delta)`
- `compute_berry_phase` (line 1257) `def compute_berry_phase(self, model)`
- `_stack_spectral_kernels` (line 1293) `def _stack_spectral_kernels(self, model)`
- `compute_goe_gue_stats` (line 1318) `def compute_goe_gue_stats(self, model)`
- `snapshot` (line 1362) `def snapshot(self, model, step, gradient_buffer, lr)`
- `format_log` (line 1391) `def format_log(snap)`
- `__init__` (line 1407) `def __init__(self, config)`
- `forward` (line 1424) `def forward(self, video)`
- `get_phase_snapshot` (line 1487) `def get_phase_snapshot(self, step, lr)`
- `__init__` (line 1508) `def __init__(self, config)`
- `_apply_spatial_stack` (line 1537) `def _apply_spatial_stack(self, feat)`
- `forward` (line 1544) `def forward(self, tokens, frame_offsets)`
- `__init__` (line 1612) `def __init__(self, config)`
- `_freeze_backbone` (line 1622) `def _freeze_backbone(self)`
- `_make_gen_masks` (line 1628) `def _make_gen_masks(self, batch_size, device)`
- `forward` (line 1645) `def forward(self, video)`
- `__init__` (line 1696) `def __init__(self, config)`
- `_temporal_gradient_loss` (line 1729) `def _temporal_gradient_loss(self, generated, target)`
- `train_epoch` (line 1735) `def train_epoch(self, dataloader, epoch)`
- `save_checkpoint` (line 1821) `def save_checkpoint(self, epoch, metrics)`
- `load_checkpoint` (line 1837) `def load_checkpoint(self, path)`
- `__init__` (line 1861) `def __init__(self, config)`
- `__len__` (line 1872) `def __len__(self)`
- `_init_objects` (line 1875) `def _init_objects(self, rng)`
- `_render_frame` (line 1897) `def _render_frame(self, objects, grid_x, grid_y)`
- `_update_physics` (line 1922) `def _update_physics(self, objects)`
- `__getitem__` (line 1940) `def __getitem__(self, idx)`
- `__init__` (line 1972) `def __init__(self, video_dir, config)`
- `__len__` (line 1995) `def __len__(self)`
- `__getitem__` (line 1998) `def __getitem__(self, idx)`
- `__init__` (line 2015) `def __init__(self, config)`
- `_cosine_lr` (line 2053) `def _cosine_lr(self, step, total_steps)`
- `train_epoch` (line 2060) `def train_epoch(self, dataloader, epoch, total_steps)`
- `save_checkpoint` (line 2150) `def save_checkpoint(self, epoch, metrics, is_latest)`
- `load_checkpoint` (line 2169) `def load_checkpoint(self, path)`
- `setUp` (line 2222) `def setUp(self)`
- `test_decoder_output_shape` (line 2231) `def test_decoder_output_shape(self)`
- `test_decoder_pixel_range` (line 2239) `def test_decoder_pixel_range(self)`
- `test_decoder_gradient_flows` (line 2247) `def test_decoder_gradient_flows(self)`
- `setUp` (line 2261) `def setUp(self)`
- `test_generator_output_shape` (line 2275) `def test_generator_output_shape(self)`
- `test_generator_backbone_frozen` (line 2287) `def test_generator_backbone_frozen(self)`
- `setUp` (line 2299) `def setUp(self)`
- `test_train_one_step` (line 2322) `def test_train_one_step(self)`
- `test_decoder_parameters_update` (line 2332) `def test_decoder_parameters_update(self)`
- `setUp` (line 2346) `def setUp(self)`
- `test_hamilton_product_identity` (line 2350) `def test_hamilton_product_identity(self)`
- `test_hamilton_product_ij_equals_k` (line 2354) `def test_hamilton_product_ij_equals_k(self)`
- `test_normalize_unit` (line 2361) `def test_normalize_unit(self)`
- `test_conjugate_product_identity` (line 2366) `def test_conjugate_product_identity(self)`
- `test_rotate_vector_norm_preserving` (line 2373) `def test_rotate_vector_norm_preserving(self)`
- `test_log_exp_roundtrip` (line 2381) `def test_log_exp_roundtrip(self)`
- `test_lie_product_approximation` (line 2388) `def test_lie_product_approximation(self)`
- `test_output_divisible_by_4` (line 2402) `def test_output_divisible_by_4(self)`
- `test_gradient_flows` (line 2408) `def test_gradient_flows(self)`
- `setUp` (line 2420) `def setUp(self)`
- `test_forward_shape_matches_config` (line 2426) `def test_forward_shape_matches_config(self)`
- `test_temporal_derivative_handles_single_frame` (line 2436) `def test_temporal_derivative_handles_single_frame(self)`
- `setUp` (line 2448) `def setUp(self)`
- `test_mask_shapes` (line 2451) `def test_mask_shapes(self)`
- `test_predictor_mask_subset_of_encoder_mask` (line 2458) `def test_predictor_mask_subset_of_encoder_mask(self)`
- `setUp` (line 2469) `def setUp(self)`
- `test_forward_loss_scalar` (line 2476) `def test_forward_loss_scalar(self)`
- `test_encoder_output_shape` (line 2486) `def test_encoder_output_shape(self)`
- `test_predictor_output_shape` (line 2497) `def test_predictor_output_shape(self)`
- `test_torus_brain_forward` (line 2510) `def test_torus_brain_forward(self)`
- `test_quaternion_spectral_layer_forward` (line 2518) `def test_quaternion_spectral_layer_forward(self)`
- `test_complex_spectral_layer_forward` (line 2526) `def test_complex_spectral_layer_forward(self)`
- `test_moe_forward` (line 2532) `def test_moe_forward(self)`
- `test_attention_forward` (line 2539) `def test_attention_forward(self)`
- `test_block_forward` (line 2546) `def test_block_forward(self)`
- `setUp` (line 2557) `def setUp(self)`
- `test_output_shape` (line 2564) `def test_output_shape(self)`
- `test_pixel_range` (line 2570) `def test_pixel_range(self)`
- `test_deterministic` (line 2576) `def test_deterministic(self)`
- `test_different_indices_differ` (line 2582) `def test_different_indices_differ(self)`
- `setUp` (line 2592) `def setUp(self)`
- `test_train_one_step` (line 2610) `def test_train_one_step(self)`
- `test_train_multiple_steps` (line 2620) `def test_train_multiple_steps(self)`
- `test_bad_d_model_raises` (line 2633) `def test_bad_d_model_raises(self)`
- `test_bad_mask_ratio_raises` (line 2637) `def test_bad_mask_ratio_raises(self)`
- `test_bad_data_mode_raises` (line 2641) `def test_bad_data_mode_raises(self)`
- `test_micro_config_valid` (line 2645) `def test_micro_config_valid(self)`
- `to_frames` (line 2681) `def to_frames(t)` - *[T, C, H, W] float -> [T, H, W, C] uint8.*

#### `__init__.py`
**Path:** `src/__init__.py`

*No symbols extracted*

#### `ucf101_dataset.py`
**Path:** `src/ucf101_dataset.py`

**Classes:**
- `VideoBackendError` (line 60) `class VideoBackendError(RuntimeError)` - *Raised when no video decoding backend is available.*
- `RarExtractError` (line 64) `class RarExtractError(RuntimeError)` - *Raised when .rar extraction fails.*
- `SecurityError` (line 68) `class SecurityError(RuntimeError)` - *Raised when a security check fails (e.g. zip-slip).*
- `UCF101Config` (line 73) `class UCF101Config`
- `UCF101Dataset` (line 98) `class UCF101Dataset(Dataset)` - *PyTorch Dataset for UCF101 human actions.

Loads AVI video files from a local UCF101 directory structure,
parses train/test split annotations, extracts temporal clips,
and applies optional spatial resize.

Annotations are auto-downloaded by default (small ZIP, ~200 KB).
Videos can be auto-downloaded by setting download_videos=True
(6.5 GB RAR archive). If download_videos=False, videos must be
pre-downloaded from https://www.crcv.ucf.edu/data/UCF101/ and
extracted into {root}/UCF101/ preserving subdirectory structure.

__getitem__ returns:
    torch.Tensor: shape [T, C, H, W], float32, values in [0, 1]*

**Functions:**
- `_detect_video_backend` (line 41) `def _detect_video_backend()`
- `_download_url` (line 308) `def _download_url(url, dst_path, min_bytes)` - *Download a URL to a local path with SSL fallback and size check.

Uses wget if available (more robust for large files), otherwise
falls back to urllib with SSL-verified then SSL-unverified contexts.
If min_bytes > 0 and the existing file is smaller, it is re-downloaded.*
- `_extract_rar` (line 360) `def _extract_rar(rar_path, output_dir)` - *Extract a .rar archive using available system tools.*
- `create_ucf101_dataloader` (line 389) `def create_ucf101_dataloader(config)` - *Create a DataLoader for the UCF101 dataset.

The collate function stacks video tensors into [B, T, C, H, W]
batches, compatible with both VJEPAQTrainer and VJEPAQGeneratorTrainer.*
- `__post_init__` (line 87) `def __post_init__(self)`
- `__init__` (line 116) `def __init__(self, config)`
- `num_classes` (line 139) `def num_classes(self)`
- `num_samples` (line 143) `def num_samples(self)`
- `config` (line 147) `def config(self)`
- `_acquire_annotations` (line 150) `def _acquire_annotations(self)`
- `_normalize_video_dir` (line 181) `def _normalize_video_dir(self)`
- `_cleanup_video_dir` (line 187) `def _cleanup_video_dir(self)`
- `_download_and_extract_videos` (line 194) `def _download_and_extract_videos(self)`
- `_parse_split` (line 225) `def _parse_split(self)`
- `__len__` (line 255) `def __len__(self)`
- `__getitem__` (line 258) `def __getitem__(self, index)`
- `_read_video` (line 275) `def _read_video(self, path)`
- `_make_dummy` (line 300) `def _make_dummy(self)`
- `_collate_fn` (line 398) `def _collate_fn(batch)`

#### `test_ucf101_dataset.py`
**Path:** `tests/test_ucf101_dataset.py`

**Classes:**
- `TestUCF101Config` (line 69) `class TestUCF101Config` - *Behaviour: UCF101Config validates all fields at construction time.*
- `TestUCF101DatasetInit` (line 137) `class TestUCF101DatasetInit` - *Behaviour: dataset instantiation validates files and parses annotations.*
- `TestUCF101DatasetGetItem` (line 210) `class TestUCF101DatasetGetItem` - *Behaviour: __getitem__ returns correctly processed video tensors.*
- `TestUCF101DatasetErrors` (line 363) `class TestUCF101DatasetErrors` - *Behaviour: dataset handles I/O errors gracefully.*
- `TestUCF101Dataloader` (line 398) `class TestUCF101Dataloader` - *Behaviour: create_ucf101_dataloader returns a working DataLoader.*

**Functions:**
- `_make_test_video` (line 29) `def _make_test_video(path, num_frames, height, width, seed)`
- `_make_annotation_files` (line 48) `def _make_annotation_files(annotation_dir, split, split_index, entries)`
- `test_default_config_is_valid` (line 72) `def test_default_config_is_valid(self)`
- `test_valid_config_accepts_all_fields` (line 81) `def test_valid_config_accepts_all_fields(self)`
- `test_zero_frames_per_clip_raises` (line 102) `def test_zero_frames_per_clip_raises(self)`
- `test_negative_output_size_raises` (line 107) `def test_negative_output_size_raises(self)`
- `test_invalid_split_raises` (line 114) `def test_invalid_split_raises(self)`
- `test_invalid_split_index_raises` (line 119) `def test_invalid_split_index_raises(self)`
- `test_negative_num_workers_raises` (line 126) `def test_negative_num_workers_raises(self)`
- `test_zero_batch_size_raises` (line 131) `def test_zero_batch_size_raises(self)`
- `setUp` (line 140) `def setUp(self)`
- `tearDown` (line 148) `def tearDown(self)`
- `test_missing_annotation_file_raises` (line 151) `def test_missing_annotation_file_raises(self)`
- `test_empty_annotation_raises_runtime_error` (line 162) `def test_empty_annotation_raises_runtime_error(self)`
- `test_loads_samples_with_valid_annotations` (line 174) `def test_loads_samples_with_valid_annotations(self)`
- `test_num_classes_matches_annotation` (line 190) `def test_num_classes_matches_annotation(self)`
- `setUp` (line 213) `def setUp(self)`
- `tearDown` (line 234) `def tearDown(self)`
- `test_output_shape_with_resize` (line 237) `def test_output_shape_with_resize(self)`
- `test_output_shape_without_resize` (line 253) `def test_output_shape_without_resize(self)`
- `test_pixel_range` (line 271) `def test_pixel_range(self)`
- `test_dtype_is_float32` (line 287) `def test_dtype_is_float32(self)`
- `test_different_indices_return_different_tensors` (line 300) `def test_different_indices_return_different_tensors(self)`
- `test_short_video_gets_padded` (line 314) `def test_short_video_gets_padded(self)`
- `test_deterministic_output_for_same_index` (line 347) `def test_deterministic_output_for_same_index(self)`
- `setUp` (line 366) `def setUp(self)`
- `tearDown` (line 374) `def tearDown(self)`
- `test_missing_video_file_returns_dummy` (line 377) `def test_missing_video_file_returns_dummy(self)`
- `setUp` (line 401) `def setUp(self)`
- `tearDown` (line 424) `def tearDown(self)`
- `test_dataloader_returns_batched_tensors` (line 427) `def test_dataloader_returns_batched_tensors(self)`
- `test_dataloader_works_with_trainer_pattern` (line 450) `def test_dataloader_works_with_trainer_pattern(self)`

### SH (1 files)

#### `install.sh`
**Path:** `install.sh`

*No symbols extracted*
