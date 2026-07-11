"""
UCF101 video dataset for TopoVJEPA fine-tuning.

Loads UCF101 human action AVI files, extracts temporal clips,
resizes frames to a configurable output size (default 64x64),
and returns tensors compatible with the VJEPAQ model input
format: [T, C, H, W] float32 in [0, 1].

Contract: single-file module with centralized config, no hardcoded
paths, no magic numbers, production-safe I/O.

Video decoding backends (tried in order):
  1. torchcodec.decoders.SimpleVideoDecoder (torchvision >= 0.28)
  2. torchvision.io.read_video (torchvision < 0.28)
"""

import logging
import shutil
import ssl
import subprocess
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

logger = logging.getLogger(__name__)

_ANNOTATION_URL = (
    'https://www.crcv.ucf.edu/data/UCF101/'
    'UCF101TrainTestSplits-RecognitionTask.zip'
)
_VIDEOS_URL = 'https://www.crcv.ucf.edu/data/UCF101/UCF101.rar'


def _detect_video_backend() -> str:
    try:
        from torchcodec.decoders import SimpleVideoDecoder
        SimpleVideoDecoder
        return 'torchcodec'
    except ImportError:
        pass
    try:
        from torchvision.io import read_video
        read_video
        return 'read_video'
    except ImportError:
        pass
    return ''


_VIDEO_BACKEND = _detect_video_backend()


class VideoBackendError(RuntimeError):
    """Raised when no video decoding backend is available."""


class RarExtractError(RuntimeError):
    """Raised when .rar extraction fails."""


class SecurityError(RuntimeError):
    """Raised when a security check fails (e.g. zip-slip)."""


@dataclass(frozen=True)
class UCF101Config:
    root: str = './data/ucf101'
    annotation_dir: str = ''
    frames_per_clip: int = 16
    output_size: Tuple[int, int] = (64, 64)
    resize: bool = True
    split: str = 'train'
    split_index: int = 1
    download_annotations: bool = True
    download_videos: bool = True
    num_workers: int = 4
    batch_size: int = 16
    shuffle: bool = True

    def __post_init__(self) -> None:
        assert self.frames_per_clip > 0, 'frames_per_clip must be positive'
        assert self.output_size[0] > 0 and self.output_size[1] > 0, (
            'output_size dimensions must be positive'
        )
        assert self.split in ('train', 'test'), "split must be 'train' or 'test'"
        assert 1 <= self.split_index <= 3, 'split_index must be 1, 2, or 3'
        assert self.num_workers >= 0, 'num_workers must be non-negative'
        assert self.batch_size > 0, 'batch_size must be positive'


class UCF101Dataset(Dataset):
    """
    PyTorch Dataset for UCF101 human actions.

    Loads AVI video files from a local UCF101 directory structure,
    parses train/test split annotations, extracts temporal clips,
    and applies optional spatial resize.

    Annotations are auto-downloaded by default (small ZIP, ~200 KB).
    Videos can be auto-downloaded by setting download_videos=True
    (6.5 GB RAR archive). If download_videos=False, videos must be
    pre-downloaded from https://www.crcv.ucf.edu/data/UCF101/ and
    extracted into {root}/UCF101/ preserving subdirectory structure.

    __getitem__ returns:
        torch.Tensor: shape [T, C, H, W], float32, values in [0, 1]
    """

    def __init__(self, config: UCF101Config) -> None:
        if not _VIDEO_BACKEND:
            raise VideoBackendError(
                'No video decoding backend available. Install torchcodec '
                '(pip install torchcodec) or torchvision with PyAV support.'
            )
        self._config = config
        self._root = Path(config.root).expanduser().resolve()
        self._video_dir = self._root / 'UCF101'
        annotation_dir = (
            Path(config.annotation_dir).expanduser().resolve()
            if config.annotation_dir
            else self._root / 'annotations'
        )
        self._annotation_dir = annotation_dir
        self._acquire_annotations()
        if config.download_videos:
            self._download_and_extract_videos()
        self._samples: List[Tuple[str, int]] = []
        self._num_classes: int = 0
        self._parse_split()

    @property
    def num_classes(self) -> int:
        return self._num_classes

    @property
    def num_samples(self) -> int:
        return len(self._samples)

    @property
    def config(self) -> UCF101Config:
        return self._config

    def _acquire_annotations(self) -> None:
        if not self._config.download_annotations:
            return
        if not self._annotation_dir.exists():
            self._annotation_dir.mkdir(parents=True, exist_ok=True)
        class_ind_path = self._annotation_dir / 'classInd.txt'
        if class_ind_path.exists():
            return
        zip_path = self._annotation_dir / 'annotations.zip'
        logger.info('Downloading UCF101 annotations from %s', _ANNOTATION_URL)
        _download_url(_ANNOTATION_URL, str(zip_path))
        extract_dir = self._annotation_dir / '_zip_extract'
        extract_dir.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(str(zip_path), 'r') as zf:
                zf.extractall(str(extract_dir))
        except zipfile.BadZipFile as exc:
            raise RuntimeError(f'Corrupt annotation archive: {exc}') from exc
        for txt in extract_dir.rglob('*.txt'):
            dst = self._annotation_dir / txt.name
            resolved_dst = dst.resolve()
            if not str(resolved_dst).startswith(str(self._annotation_dir.resolve())):
                raise SecurityError(
                    f'Zip-slip detected: {txt} resolves outside {self._annotation_dir}'
                )
            shutil.move(str(txt), str(dst))
        shutil.rmtree(extract_dir)
        if zip_path.exists():
            zip_path.unlink()
        logger.info('Annotations extracted to %s', self._annotation_dir)

    def _normalize_video_dir(self) -> None:
        alt_dir = self._root / 'UCF-101'
        if alt_dir.exists() and not self._video_dir.exists():
            logger.info('Renaming UCF-101/ to UCF101/')
            alt_dir.rename(self._video_dir)

    def _cleanup_video_dir(self) -> None:
        if self._video_dir.exists():
            shutil.rmtree(self._video_dir)
        alt_dir = self._root / 'UCF-101'
        if alt_dir.exists():
            shutil.rmtree(alt_dir)

    def _download_and_extract_videos(self) -> None:
        self._normalize_video_dir()
        if self._video_dir.exists() and any(self._video_dir.iterdir()):
            return
        self._root.mkdir(parents=True, exist_ok=True)
        rar_path = self._root / 'UCF101.rar'

        _download_url(
            _VIDEOS_URL, str(rar_path),
            min_bytes=6_000_000_000,
        )
        logger.info('Extracting videos to %s', self._video_dir)
        for retry in range(2):
            try:
                _extract_rar(str(rar_path), str(self._root))
                self._normalize_video_dir()
                if not self._video_dir.exists():
                    raise RarExtractError(
                        f'Extraction did not create {self._video_dir}'
                    )
                break
            except RarExtractError:
                if retry == 1:
                    raise
                logger.warning('Extraction failed (corrupt download?). Retrying...')
                rar_path.unlink()
                self._cleanup_video_dir()
                _download()
        rar_path.unlink()
        logger.info('Videos extracted to %s', self._video_dir)

    def _parse_split(self) -> None:
        split_name = f'{self._config.split}list0{self._config.split_index}.txt'
        split_path = self._annotation_dir / split_name
        if not split_path.exists():
            raise FileNotFoundError(
                f'Annotation file not found: {split_path}. '
                f'Annotations auto-download by default; set '
                f'download_annotations=True or manually place files '
                f'from {_ANNOTATION_URL} into {self._annotation_dir}'
            )
        with open(split_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) < 2:
                    logger.warning('Skipping malformed annotation line: %s', line)
                    continue
                rel_path = parts[0]
                class_id = int(parts[1]) - 1
                abs_path = str(self._video_dir / rel_path)
                self._samples.append((abs_path, class_id))
        if not self._samples:
            raise RuntimeError(
                f'No valid samples found in {split_path}. '
                f'Verify UCF101 videos exist in {self._video_dir}'
            )
        self._num_classes = max(s[1] for s in self._samples) + 1

    def __len__(self) -> int:
        return len(self._samples)

    def __getitem__(self, index: int) -> torch.Tensor:
        video_path, _ = self._samples[index]
        try:
            frames = self._read_video(video_path)
        except Exception as exc:
            logger.warning('Failed to read video %s: %s', video_path, exc)
            return self._make_dummy()
        if self._config.resize:
            frames = F.interpolate(
                frames,
                size=self._config.output_size,
                mode='bilinear',
                align_corners=False,
            )
        frames = frames.contiguous()
        return frames

    def _read_video(self, path: str) -> torch.Tensor:
        if _VIDEO_BACKEND == 'torchcodec':
            from torchcodec.decoders import SimpleVideoDecoder as VideoDecoder
            decoder = VideoDecoder(path, dimension_order='NCHW')
            raw = decoder.get_all_frames()
            frames = raw.data if hasattr(raw, 'data') else raw
        elif _VIDEO_BACKEND == 'read_video':
            from torchvision.io import read_video
            video_frames, _, _ = read_video(path, pts_unit='sec')
            frames = video_frames.permute(0, 3, 1, 2)
        else:
            raise VideoBackendError(
                'No video backend available. Cannot read video file.'
            )
        frames = frames.to(dtype=torch.float32) / 255.0
        T, C, H, W = frames.shape
        target = self._config.frames_per_clip
        if T < target:
            pad = frames[-1:].expand(target - T, -1, -1, -1)
            frames = torch.cat([frames, pad], dim=0)
        else:
            start = (T - target) // 2
            frames = frames[start:start + target]
        return frames

    def _make_dummy(self) -> torch.Tensor:
        return torch.zeros(
            self._config.frames_per_clip, 3,
            *self._config.output_size,
            dtype=torch.float32,
        )


def _download_url(url: str, dst_path: str, min_bytes: int = 0) -> None:
    """Download a URL to a local path with SSL fallback and size check.

    Uses wget if available (more robust for large files), otherwise
    falls back to urllib with SSL-verified then SSL-unverified contexts.
    If min_bytes > 0 and the existing file is smaller, it is re-downloaded.
    """
    dst = Path(dst_path)
    if dst.exists() and min_bytes > 0 and dst.stat().st_size >= min_bytes:
        return
    if dst.exists() and min_bytes > 0:
        logger.warning(
            'Existing file %s is only %d bytes (expected >= %d), re-downloading...',
            dst.name, dst.stat().st_size, min_bytes,
        )
        dst.unlink()
    if dst.exists() and min_bytes == 0:
        return
    wget_exe = shutil.which('wget')
    if wget_exe:
        result = subprocess.run(
            [wget_exe, '--no-check-certificate', '-c', '-O', str(dst), url],
            timeout=7200,
        )
        if result.returncode != 0:
            if dst.exists():
                dst.unlink()
            raise RuntimeError(
                f'wget download failed with return code {result.returncode}'
            )
        return
    for attempt, ctx in [
        ('SSL-verified', ssl.create_default_context()),
        ('SSL-unverified', ssl._create_unverified_context()),
    ]:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ctx, timeout=300) as response:
                with open(dst, 'wb') as f:
                    shutil.copyfileobj(response, f)
            break
        except urllib.error.URLError as exc:
            if dst.exists():
                dst.unlink()
            if attempt == 'SSL-unverified':
                raise RuntimeError(f'Failed to download {url}: {exc}') from exc
            logger.warning(
                '%s download failed: %s. Retrying with unverified SSL.',
                attempt, exc,
            )


def _extract_rar(rar_path: str, output_dir: str) -> None:
    """Extract a .rar archive using available system tools."""
    for tool, args in [
        ('unrar', ['unrar', 'x', '-o+', rar_path, output_dir]),
        ('7z', ['7z', 'x', rar_path, f'-o{output_dir}', '-y']),
        ('7za', ['7za', 'x', rar_path, f'-o{output_dir}', '-y']),
    ]:
        exe = shutil.which(tool)
        if exe is None:
            continue
        try:
            result = subprocess.run(
                [exe] + args[1:],
                capture_output=True,
                text=True,
                timeout=3600,
            )
            if result.returncode == 0:
                return
            logger.warning('%s extraction returned code %d: %s', tool, result.returncode, result.stderr[:200])
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            continue
    raise RarExtractError(
        f'Failed to extract {rar_path}. Ensure unrar or 7z is installed.'
    )


def create_ucf101_dataloader(config: UCF101Config) -> DataLoader:
    """
    Create a DataLoader for the UCF101 dataset.

    The collate function stacks video tensors into [B, T, C, H, W]
    batches, compatible with both VJEPAQTrainer and VJEPAQGeneratorTrainer.
    """
    dataset = UCF101Dataset(config)

    def _collate_fn(batch):
        return torch.stack(batch)

    return DataLoader(
        dataset,
        batch_size=config.batch_size,
        shuffle=config.shuffle,
        num_workers=config.num_workers,
        drop_last=True,
        collate_fn=_collate_fn,
        worker_init_fn=lambda wid: torch.initial_seed(),
    )
