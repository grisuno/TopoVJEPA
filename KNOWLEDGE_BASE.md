# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM.
> No LLMs. No tokens. Pure static analysis. See more [here](https://github.com/grisuno/ReadMenator) 

**Total Files Parsed:** 3 | **Total Symbols Extracted:** 181 | **Total Imports:** 23

## Structural Knowledge Map
```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray: 5 5,color:#aaa;
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
    app_py["app.py (py)"]
    class app_py mod;
    install_sh["install.sh (sh)"]
    class install_sh mod;
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
    model_py -.->|imports| ext_sys
```

---

## Architecture Reference

### PY (2 files)

#### `app.py`
**Path:** `app.py`

*No symbols extracted*

#### `model.py`
**Path:** `model.py`

**Classs:**
- `VJEPAQConfig` (line 46) - *Central configuration for V-JEPA-Q model and training.

All hyperparameters defined here. No hardcoded values or magic numbers
exist outside this class. Computed fields in __post_init__.*
- `QuaternionOps` (line 205) - *Pure quaternion operations. Convention: [w, x, y, z].

Includes exponential and logarithmic maps for the Lie group SU(2) / so(3).
The log map converts quaternion multiplication to vector addition in the
tangent space (Lie algebra). The exp map converts back.*
- `QuaternionLinear` (line 282) - *Linear transform using quaternion Hamilton product.

Input and output dimensions must be multiples of 4. Weight is
factorised into four coupled subspaces via Hamilton product.*
- `ComplexSpectralLayer` (line 320) - *Spectral convolution with tuneable real/imaginary kernel ratio.

Operates in 2D Fourier domain: P(k) = W(k) * X(k) with channel mixing
via einsum. Real part: conservative dynamics. Imaginary part: dissipative.
Tracks GOE -> GUE transition via imaginary_ratio.*
- `QuaternionSpectralLayer` (line 396) - *Full quaternion spectral convolution in Fourier domain.

Each quaternion component (w, x, y, z) gets a complex kernel.
Combined via Hamilton product in frequency space using Gauss's trick
(3 real MUL instead of 4 for complex multiply).*
- `SpatiotemporalSpectralAE` (line 479) - *Two-level spectral autoencoder: temporal FFT + spatial quaternion spectral.*
- `VideoPatchEmbedding` (line 529) - *Convert video to quaternion-encoded patch embeddings with motion cues.

Extracts spatial patches and temporal derivative, then projects to
D_MODEL-dimensional quaternion space with position encodings.*
- `VJEPAMasker` (line 605) - *Generate asymmetric encoder/predictor masks for V-JEPA training.*
- `RotaryEmbedding` (line 668) - *Rotary Position Embeddings (RoPE) for spatiotemporal attention.*
- `RMSNorm` (line 700) - *Root Mean Square Layer Normalisation.*
- `SpatiotemporalAttention` (line 718) - *Grouped-Query Attention with RoPE for spatiotemporal sequences.*
- `QuaternionTorusBrain` (line 780) - *FFN replacement with quaternion-topological processing on a 2D torus.

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
- `TopoMoE` (line 963) - *Mixture of Experts with shared Topological Torus Brain.*
- `VJEPAQBlock` (line 1036) - *Transformer block with SpatiotemporalAttention + TopoMoE FFN.*
- `VJEPAQEncoder` (line 1074) - *Video encoder with quaternion spectral processing.*
- `VJEPAQPredictor` (line 1126) - *World model predictor: predicts masked patch representations.*
- `PhaseDiagramTracker` (line 1193) - *Tracks phase diagram metrics during world model training.

Metrics: delta, kappa, T_eff, alpha, Berry phase, Dyson beta.*
- `VJEPAQ` (line 1396) - *V-JEPA-Q: Quaternion-Enhanced Video Joint-Embedding Predictive Architecture.*
- `VJEPAQDecoder` (line 1490) - *Decodes latent predictor tokens into pixel-space video frames.

Pipeline:
1. Linear projection from D_MODEL to PATCH_DIM (reconstructs image patches)
2. Rearrange token sequence into spatial-temporal pixel grid
3. 3D convolutions for temporal-spatial refinement
4. Sigmoid output for normalized pixel values [0, 1]*
- `VJEPAQVideoGenerator` (line 1591) - *Physically consistent video generator: frozen world model + pixel decoder.

Architecture:
- VJEPAQ backbone loaded from .safetensors (encoder + predictor, frozen)
- VJEPAQDecoder (trainable) converts torus latent states to pixels

Generation pipeline:
1. Context frames → frozen VideoPatchEmbedding + Encoder → visible latents
2. Frozen Predictor rolls out future states in torus latent space
3. Decoder converts predicted latent tokens to video frames*
- `VJEPAQGeneratorTrainer` (line 1681) - *Training loop for the video decoder.

Freezes the V-JEPA-Q backbone and only trains VJEPAQDecoder.
Loss = MSE + temporal gradient penalty for flicker-free video.*
- `MovingShapesDataset` (line 1840) - *Synthetic video dataset with moving geometric shapes (0 bytes on disk).

Generates videos with N coloured shapes (circles and squares) that
move at constant velocity and bounce off walls. Fully deterministic
given seed.*
- `VideoDataset` (line 1958) - *Load video files from directory, falls back to MovingShapes.*
- `VJEPAQTrainer` (line 2001) - *Training loop for V-JEPA-Q with AMP, gradient clipping, and phase tracking.*
- `TestVJEPAQDecoder` (line 2206) - *Behaviour: decoder converts latent tokens to video frames.*
- `TestVJEPAQVideoGenerator` (line 2245) - *Behaviour: generator produces video from context frames.*
- `TestGeneratorTrainerIntegration` (line 2283) - *Behaviour: generator trainer can complete a step without error.*
- `TestQuaternionOps` (line 2330) - *Behaviour: Quaternion algebra must satisfy unit quaternion properties.*
- `TestQuaternionLinear` (line 2386) - *Behaviour: QuaternionLinear must preserve quaternion structure.*
- `TestVideoPatchEmbedding` (line 2404) - *Critical: patch embedding shapes must match config (bug regression test).*
- `TestVJEPAMasker` (line 2432) - *Behaviour: masks must be valid and consistent.*
- `TestVJEPAQModel` (line 2453) - *Behaviour: full model forward pass produces valid losses.*
- `TestMovingShapesDataset` (line 2541) - *Behaviour: synthetic dataset produces valid video tensors.*
- `TestTrainerIntegration` (line 2576) - *Behaviour: trainer can complete a training step without error.*
- `TestConfigValidation` (line 2617) - *Behaviour: invalid configs must raise AssertionError.*

**Functions:**
- `_setup_logger` (line 178)
- `_set_seed` (line 189)
- `_count_parameters` (line 196)
- `_visualize_video` (line 2642) - *Load a .pt inference output and render it as .mp4 via ffmpeg.*
- `main` (line 2711) - *Entry point: parse args, create config, build dataset, train or generate.*
- `__post_init__` (line 130)
- `hamilton_product` (line 214)
- `normalize` (line 225)
- `conjugate` (line 229)
- `rotate_vector` (line 233)
- `log` (line 242) - *Logarithmic map from SU(2) to so(3) (tangent space).

Converts a unit quaternion q = [w, x, y, z] to a pure quaternion
v = [0, theta*u] where u is the unit axis and theta = arccos(w).
In the tangent space, quaternion multiplication becomes vector addition
(via BCH approximation: log(q1 * q2) approx log(q1) + log(q2)).*
- `exp` (line 258) - *Exponential map from so(3) to SU(2).

Converts a pure quaternion v = [0, theta*u] back to a unit quaternion
q = [cos(theta), sin(theta)*u]. This is the inverse of log().*
- `lie_product` (line 270) - *Approximate quaternion product via Lie algebra addition.

Instead of Hamilton product (O(n^2) cross terms), uses:
    q1 * q2 approx exp(log(q1) + log(q2))
which converts multiplication to element-wise addition in the
tangent space. Exact for commuting quaternions; BCH-approximate
for non-commuting.*
- `__init__` (line 289)
- `forward` (line 304)
- `__init__` (line 328)
- `set_imaginary_ratio` (line 352)
- `get_effective_imaginary_ratio` (line 359)
- `get_spectral_operator` (line 368)
- `forward` (line 375)
- `__init__` (line 404)
- `_kernel` (line 431)
- `_gauss_contract` (line 435)
- `forward` (line 445)
- `__init__` (line 482)
- `_temporal_filter` (line 503)
- `encode_temporal` (line 509)
- `decode_temporal` (line 513)
- `forward` (line 517)
- `__init__` (line 536)
- `_compute_temporal_derivative` (line 554)
- `forward` (line 559)
- `__init__` (line 608)
- `_generate_block_mask` (line 613)
- `generate_masks` (line 627)
- `__init__` (line 671)
- `_build_cache` (line 677)
- `_rotate_half` (line 684)
- `forward` (line 688)
- `__init__` (line 703)
- `forward` (line 708)
- `__init__` (line 721)
- `forward` (line 737)
- `__init__` (line 796)
- `_build_torus_graph` (line 842) - *Build fully periodic 2D torus adjacency.*
- `_torus_soft_assign` (line 871)
- `_message_passing` (line 886) - *Message passing with Lie algebra quaternion product.

When self.lie_approx is True, uses exp(log(q) + log(p)) instead of
Hamilton product q * p. This converts quaternion multiplication to
vector addition in so(3) tangent space via BCH approximation.*
- `forward` (line 918)
- `__init__` (line 966)
- `_route` (line 986)
- `forward` (line 1013)
- `__init__` (line 1039)
- `_forward_impl` (line 1048)
- `forward` (line 1059)
- `__init__` (line 1077)
- `forward` (line 1088)
- `__init__` (line 1129)
- `forward` (line 1148)
- `__init__` (line 1199)
- `compute_delta` (line 1208)
- `compute_kappa` (line 1216)
- `compute_t_eff` (line 1234)
- `compute_alpha` (line 1244)
- `compute_berry_phase` (line 1249)
- `_stack_spectral_kernels` (line 1285)
- `compute_goe_gue_stats` (line 1310)
- `snapshot` (line 1354)
- `format_log` (line 1383)
- `__init__` (line 1399)
- `forward` (line 1416)
- `get_phase_snapshot` (line 1479)
- `__init__` (line 1500)
- `_apply_spatial_stack` (line 1529)
- `forward` (line 1536)
- `__init__` (line 1604)
- `_freeze_backbone` (line 1614)
- `_make_gen_masks` (line 1620)
- `forward` (line 1637)
- `__init__` (line 1688)
- `_temporal_gradient_loss` (line 1721)
- `train_epoch` (line 1727)
- `save_checkpoint` (line 1810)
- `load_checkpoint` (line 1826)
- `__init__` (line 1850)
- `__len__` (line 1861)
- `_init_objects` (line 1864)
- `_render_frame` (line 1886)
- `_update_physics` (line 1911)
- `__getitem__` (line 1929)
- `__init__` (line 1961)
- `__len__` (line 1984)
- `__getitem__` (line 1987)
- `__init__` (line 2004)
- `_cosine_lr` (line 2042)
- `train_epoch` (line 2049)
- `save_checkpoint` (line 2137)
- `load_checkpoint` (line 2156)
- `setUp` (line 2209)
- `test_decoder_output_shape` (line 2218)
- `test_decoder_pixel_range` (line 2226)
- `test_decoder_gradient_flows` (line 2234)
- `setUp` (line 2248)
- `test_generator_output_shape` (line 2262)
- `test_generator_backbone_frozen` (line 2274)
- `setUp` (line 2286)
- `test_train_one_step` (line 2309)
- `test_decoder_parameters_update` (line 2319)
- `setUp` (line 2333)
- `test_hamilton_product_identity` (line 2337)
- `test_hamilton_product_ij_equals_k` (line 2341)
- `test_normalize_unit` (line 2348)
- `test_conjugate_product_identity` (line 2353)
- `test_rotate_vector_norm_preserving` (line 2360)
- `test_log_exp_roundtrip` (line 2368)
- `test_lie_product_approximation` (line 2375)
- `test_output_divisible_by_4` (line 2389)
- `test_gradient_flows` (line 2395)
- `setUp` (line 2407)
- `test_forward_shape_matches_config` (line 2413)
- `test_temporal_derivative_handles_single_frame` (line 2423)
- `setUp` (line 2435)
- `test_mask_shapes` (line 2438)
- `test_predictor_mask_subset_of_encoder_mask` (line 2445)
- `setUp` (line 2456)
- `test_forward_loss_scalar` (line 2463)
- `test_encoder_output_shape` (line 2473)
- `test_predictor_output_shape` (line 2484)
- `test_torus_brain_forward` (line 2497)
- `test_quaternion_spectral_layer_forward` (line 2505)
- `test_complex_spectral_layer_forward` (line 2513)
- `test_moe_forward` (line 2519)
- `test_attention_forward` (line 2526)
- `test_block_forward` (line 2533)
- `setUp` (line 2544)
- `test_output_shape` (line 2551)
- `test_pixel_range` (line 2557)
- `test_deterministic` (line 2563)
- `test_different_indices_differ` (line 2569)
- `setUp` (line 2579)
- `test_train_one_step` (line 2597)
- `test_train_multiple_steps` (line 2607)
- `test_bad_d_model_raises` (line 2620)
- `test_bad_mask_ratio_raises` (line 2624)
- `test_bad_data_mode_raises` (line 2628)
- `test_micro_config_valid` (line 2632)
- `to_frames` (line 2668) - *[T, C, H, W] float -> [T, H, W, C] uint8.*

### SH (1 files)

#### `install.sh`
**Path:** `install.sh`

*No symbols extracted*
