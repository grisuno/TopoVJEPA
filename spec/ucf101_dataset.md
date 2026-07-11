# UCF101 Dataset Specification

## Module
`src/ucf101_dataset.py`

## Contract
The UCF101 dataset module provides a PyTorch `Dataset` for loading,
processing, and iterating over the UCF101 human actions dataset
for fine-tuning video prediction models (VJEPAQ backbone).

## Dependencies
- Python 3.10+
- PyTorch 2.0+ (torch)
- torchvision (video I/O)
- numpy

## Configuration

### `UCF101Config` dataclass (frozen)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `root` | `str` | `'./data/ucf101'` | Root directory for UCF101 data; must contain `UCF101/` subdirectory with AVI files |
| `annotation_dir` | `str` | `''` | Directory with annotation files; empty means `{root}/annotations` |
| `frames_per_clip` | `int` | `16` | Number of frames per returned clip |
| `output_size` | `Tuple[int, int]` | `(64, 64)` | Target (H, W) for frame resize |
| `resize` | `bool` | `True` | If True, frames are resized to `output_size`; if False, original resolution is preserved |
| `split` | `str` | `'train'` | Dataset split: `'train'` or `'test'` |
| `split_index` | `int` | `1` | Split index (1, 2, or 3 for UCF101's 3 train/test splits) |
| `download_annotations` | `bool` | `False` | If True and annotations are missing, download them automatically from `https://www.crcv.ucf.edu/data/UCF101/UCF101TrainTestSplits-RecognitionTask.zip` |
| `num_workers` | `int` | `4` | DataLoader worker count |
| `batch_size` | `int` | `16` | Batch size for DataLoader |
| `shuffle` | `bool` | `True` | Shuffle flag for DataLoader |

### Validation (`__post_init__`)
- `frames_per_clip > 0`
- `output_size[0] > 0` and `output_size[1] > 0`
- `split in ('train', 'test')`
- `1 <= split_index <= 3`
- `num_workers >= 0`
- `batch_size > 0`

## Output Format

### `__getitem__(index) -> torch.Tensor`
- Shape: `[T, C, H, W]` where `T = frames_per_clip`, `C = 3`, `H, W = output_size` (or original size if resize=False)
- Dtype: `torch.float32`
- Value range: `[0.0, 1.0]`
- Channel order: RGB

## Scenarios (BDD Given-When-Then)

### Happy Path 1: Dataset loads with valid configuration
```
Given a UCF101Config with resize=True and output_size=(64, 64)
  And the UCF101 video directory exists at {root}/UCF101/
  And annotation files exist at {annotation_dir}/
When the dataset is instantiated
Then the dataset contains a positive number of samples
  And each sample is a tuple of (video_path, class_id)
  And num_classes equals the number of unique class IDs
```

### Happy Path 2: Video frames are resized to target output size
```
Given a UCF101Config with resize=True and output_size=(64, 64)
  And the dataset is instantiated with real video files
When __getitem__ is called with a valid index
Then the returned tensor has shape [frames_per_clip, 3, 64, 64]
  And all pixel values are in [0.0, 1.0]
  And the dtype is torch.float32
```

### Happy Path 3: Video frames preserve original size when resize=False
```
Given a UCF101Config with resize=False
  And the dataset is instantiated
When __getitem__ is called with a valid index
Then the returned tensor preserves the original spatial dimensions
  And all pixel values are in [0.0, 1.0]
```

### Happy Path 4: Annotation download works
```
Given a UCF101Config with download_annotations=True
  And no existing annotation files at {annotation_dir}/
When the dataset is instantiated
Then annotation files are downloaded and extracted
  And the dataset loads samples successfully
```

### Edge Case 1: Short video is padded to frames_per_clip
```
Given a video file with fewer frames than frames_per_clip
When __getitem__ is called for that sample
Then the returned tensor has exactly frames_per_clip frames
  And the trailing frames duplicate the last available frame
```

### Edge Case 2: Missing or corrupt video file returns dummy
```
Given a sample whose video file does not exist or cannot be decoded
When __getitem__ is called for that sample
Then a zero tensor of shape [frames_per_clip, 3, H, W] is returned
  And no exception propagates to the caller
```

### Edge Case 3: Empty annotation file raises RuntimeError
```
Given a split file with no valid sample entries
When the dataset is instantiated
Then a RuntimeError is raised with message "No valid samples found"
```

### Sad Path 1: Missing annotation file raises FileNotFoundError
```
Given a UCF101Config with download_annotations=False
  And no annotation file at {annotation_dir}/{split}list{split_index}.txt
When the dataset is instantiated
Then a FileNotFoundError is raised
```

### Sad Path 2: Invalid split value raises AssertionError
```
Given a UCF101Config with split='invalid'
When __post_init__ is called
Then an AssertionError is raised
```

### Sad Path 3: Invalid output_size raises AssertionError
```
Given a UCF101Config with output_size=(0, 64)
When __post_init__ is called
Then an AssertionError is raised
```

### Sad Path 4: Invalid split_index raises AssertionError
```
Given a UCF101Config with split_index=0
When __post_init__ is called
Then an AssertionError is raised
```

### Sad Path 5: Negative num_workers raises AssertionError
```
Given a UCF101Config with num_workers=-1
When __post_init__ is called
Then an AssertionError is raised
```

## Security Considerations

1. **Download security**: Annotation download uses HTTPS only. The ZIP extraction validates member paths against zip-slip attacks (no `../` traversal allowed outside target directory).
2. **Path resolution**: All paths are resolved via `Path.expanduser().resolve()` to prevent symlink-based attacks. No absolute system paths are hardcoded.
3. **File handling**: Opened files use context managers (`with open(...)`). Temporary download files are cleaned up even on failure.
4. **Error isolation**: Video I/O errors are caught per-sample, returning a dummy tensor instead of crashing the entire epoch.

## Out of Scope
- Video file downloading (UCF101 videos are 6.5 GB; must be downloaded manually from https://www.crcv.ucf.edu/data/UCF101/UCF101.rar)
- Data augmentation (random crops, flips, etc.)
- Frame-rate conversion or temporal interpolation
- Multi-GPU data partitioning
- Streaming from remote storage
