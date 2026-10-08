# src

*Community 0 | 5 files | cohesion 1.00*

## Definition

This community groups 5 file(s) rooted at `src` with dominant language py (cohesion 1.00). Central symbols: `ComplexSpectralLayer`, `LRUVideoCache`, `MovingShapesDataset`, `PhaseAwareLRCallback`, `PhaseDiagramTracker`, `PreemptionHandler`, `QuaternionLinear`, `QuaternionOps`. Core file: `model.py` (194 symbols). Documented purpose: — Entry-point funcional para TopoVJEPA.  Uso: from app import create_model, create_trainer, create_dataset  # 3 líneas: modelo + datos + entrenar model = create.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `app.py` | py | utility | 5 | yes |
| `model.py` | py | business_logic | 194 | yes |
| `src/quaternion_ops.py` | py | utility | 11 | yes |
| `src/ucf101_dataset.py` | py | data_access | 28 | yes |
| `tests/test_ucf101_dataset.py` | py | testing | 37 | yes |

## Key Symbols

- `create_model` (function, `app.py:18`) `def create_model(scale)`
- `create_dataset` (function, `app.py:24`) `def create_dataset(config)`
- `create_trainer` (function, `app.py:28`) `def create_trainer(config)`
- `create_generator` (function, `app.py:32`) `def create_generator(config)`
- `create_generator_trainer` (function, `app.py:36`) `def create_generator_trainer(config)`
- `VJEPAQConfig` (class, `model.py:50`) `class VJEPAQConfig` - Central configuration for V-JEPA-Q model and training.
- `__post_init__` (method, `model.py:142`) `def __post_init__(self)`
- `to_dict` (method, `model.py:184`) `def to_dict(self)`
- `to_json` (method, `model.py:188`) `def to_json(self)`
- `from_json` (method, `model.py:196`) `def from_json(cls, path_or_str)`
- `auto_batch_size` (method, `model.py:211`) `def auto_batch_size(config, min_batch, max_batch)`
- `_setup_logger` (method, `model.py:240`) `def _setup_logger(name, level)`
- `_set_seed` (method, `model.py:251`) `def _set_seed(seed, device)`
- `_count_parameters` (method, `model.py:258`) `def _count_parameters(module)`
- `ComplexSpectralLayer` (class, `model.py:267`) `class ComplexSpectralLayer(Module)` - Spectral convolution with tuneable real/imaginary kernel ratio.
- `__init__` (method, `model.py:275`) `def __init__(self, channels, grid_h, grid_w, imaginary_ratio, init_scale)`
- `set_imaginary_ratio` (method, `model.py:299`) `def set_imaginary_ratio(self, ratio)`
- `get_effective_imaginary_ratio` (method, `model.py:306`) `def get_effective_imaginary_ratio(self)`
- `get_spectral_operator` (method, `model.py:315`) `def get_spectral_operator(self)`
- `forward` (method, `model.py:322`) `def forward(self, x)`
- `QuaternionSpectralLayer` (class, `model.py:343`) `class QuaternionSpectralLayer(Module)` - Full quaternion spectral convolution in Fourier domain.
- `__init__` (method, `model.py:351`) `def __init__(self, in_q, out_q, grid_h, grid_w, init_scale)`
- `_kernel` (method, `model.py:378`) `def _kernel(self, c)`
- `_gauss_contract` (method, `model.py:382`) `def _gauss_contract(W, X)`
- `forward` (method, `model.py:390`) `def forward(self, x)`
- `SpatiotemporalSpectralAE` (class, `model.py:424`) `class SpatiotemporalSpectralAE(Module)` - Two-level spectral autoencoder: temporal FFT + spatial quaternion spectral.
- `__init__` (method, `model.py:427`) `def __init__(self, config)`
- `_temporal_filter` (method, `model.py:448`) `def _temporal_filter(self, x, kr, ki)`
- `encode_temporal` (method, `model.py:454`) `def encode_temporal(self, x)`
- `decode_temporal` (method, `model.py:458`) `def decode_temporal(self, z)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 25
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- [INFERRED] shares_context community 0 <-> 1 (strength 0.5): Inferred shared context (layer utility) with no import path between community 0 (src) and community 1 (orphans).

## Risks

- [taint high] `model.py` -> `model.py` via `subprocess` (0 hops)
- [taint high] `model.py` -> `src/quaternion_ops.py` via `subprocess` (1 hops)
- [taint high] `model.py` -> `src/ucf101_dataset.py` via `subprocess` (1 hops)
- [taint high] `src/ucf101_dataset.py` -> `src/ucf101_dataset.py` via `subprocess` (0 hops)
- [taint medium] `src/ucf101_dataset.py` -> `src/ucf101_dataset.py` via `urllib.request` (0 hops)

## Open Questions

- Is the dangerous import `subprocess` in `model.py` still required, or can it be isolated?
- What would break if the most connected file in src changed?
- Should src be split, given cohesion 1.00?

## Sources

- `app.py`
- `model.py`
- `src/quaternion_ops.py`
- `src/ucf101_dataset.py`
- `tests/test_ucf101_dataset.py`
