# Subsystem: src

## src/__init__.py
- Layer: utility
- Language: py

## src/quaternion_ops.py
- Layer: utility
- Language: py
- Symbols:
  - `QuaternionOps` (class, line 17) `class QuaternionOps`
  - `QuaternionLinear` (class, line 115) `class QuaternionLinear(Module)`
  - `hamilton_product` (method, line 31) `def hamilton_product(q1, q2)`
  - `normalize` (method, line 42) `def normalize(q, eps)`
  - `conjugate` (method, line 46) `def conjugate(q)`
  - `rotate_vector` (method, line 50) `def rotate_vector(v, q)`
  - `log` (method, line 59) `def log(q, eps)`
  - `exp` (method, line 79) `def exp(q, eps)`
  - `lie_product` (method, line 103) `def lie_product(q1, q2, eps)`
  - `__init__` (method, line 122) `def __init__(self, in_features, out_features, bias)`
  - `forward` (method, line 137) `def forward(self, x)`
- Imported by: `model.py`

## src/ucf101_dataset.py
- Layer: data_access
- Language: py
- Symbols:
  - `_detect_video_backend` (function, line 42) `def _detect_video_backend()`
  - `LRUVideoCache` (class, line 61) `class LRUVideoCache`
  - `VideoBackendError` (class, line 100) `class VideoBackendError(RuntimeError)`
  - `RarExtractError` (class, line 104) `class RarExtractError(RuntimeError)`
  - `SecurityError` (class, line 108) `class SecurityError(RuntimeError)`
  - `UCF101Config` (class, line 113) `class UCF101Config`
  - `UCF101Dataset` (class, line 140) `class UCF101Dataset(Dataset)`
  - `_download_url` (method, line 352) `def _download_url(url, dst_path, min_bytes)`
  - `_extract_rar` (method, line 404) `def _extract_rar(rar_path, output_dir)`
  - `create_ucf101_dataloader` (method, line 433) `def create_ucf101_dataloader(config)`
  - `__init__` (method, line 69) `def __init__(self, cache_dir, capacity)`
  - `_cache_path` (method, line 75) `def _cache_path(self, video_path)`
  - `get_or_decode` (method, line 79) `def get_or_decode(self, video_path, decode_fn)`
  - `__post_init__` (method, line 129) `def __post_init__(self)`
  - `__init__` (method, line 158) `def __init__(self, config)`
  - `num_classes` (method, line 183) `def num_classes(self)`
  - `num_samples` (method, line 187) `def num_samples(self)`
  - `config` (method, line 191) `def config(self)`
  - `_acquire_annotations` (method, line 194) `def _acquire_annotations(self)`
  - `_normalize_video_dir` (method, line 225) `def _normalize_video_dir(self)`
  - `_cleanup_video_dir` (method, line 231) `def _cleanup_video_dir(self)`
  - `_download_and_extract_videos` (method, line 238) `def _download_and_extract_videos(self)`
  - `_parse_split` (method, line 269) `def _parse_split(self)`
  - `__len__` (method, line 299) `def __len__(self)`
  - `__getitem__` (method, line 302) `def __getitem__(self, index)`
  - `_read_video_raw` (method, line 319) `def _read_video_raw(self, path)`
  - `_make_dummy` (method, line 344) `def _make_dummy(self)`
  - `_collate_fn` (method, line 442) `def _collate_fn(batch)`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`
