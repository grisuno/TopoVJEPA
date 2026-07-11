"""
Tests for the UCF101 dataset module.

BDD Given-When-Then scenarios covering happy paths, edge cases,
and sad paths for UCF101Config and UCF101Dataset.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Tuple

import torch

_VIDEO_WRITE_AVAILABLE = False
try:
    from torchcodec.encoders import VideoEncoder
    _VIDEO_WRITE_AVAILABLE = True
except ImportError:
    try:
        from torchvision.io import write_video
        _VIDEO_WRITE_AVAILABLE = True
    except ImportError:
        pass


def _make_test_video(
    path: Path,
    num_frames: int = 32,
    height: int = 240,
    width: int = 320,
    seed: int = 0,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(seed)
    frames = torch.randint(0, 256, (num_frames, 3, height, width), dtype=torch.uint8)
    try:
        encoder = VideoEncoder(frames, frame_rate=30.0)
        encoder.to_file(str(path))
    except NameError:
        from torchvision.io import write_video
        frames_nhwc = frames.permute(0, 2, 3, 1)
        write_video(str(path), frames_nhwc, fps=30)


def _make_annotation_files(
    annotation_dir: Path,
    split: str = 'train',
    split_index: int = 1,
    entries: Tuple[Tuple[str, int], ...] = (),
) -> None:
    annotation_dir.mkdir(parents=True, exist_ok=True)
    class_ind_path = annotation_dir / 'classInd.txt'
    seen_classes = {}
    for rel_path, class_id in entries:
        if class_id not in seen_classes:
            seen_classes[class_id] = f'class_{class_id}'
    with open(class_ind_path, 'w') as f:
        for cid in sorted(seen_classes.keys()):
            f.write(f'{cid + 1} {seen_classes[cid]}\n')
    split_path = annotation_dir / f'{split}list0{split_index}.txt'
    with open(split_path, 'w') as f:
        for rel_path, class_id in entries:
            f.write(f'{rel_path} {class_id + 1}\n')


class TestUCF101Config(unittest.TestCase):
    """Behaviour: UCF101Config validates all fields at construction time."""

    def test_default_config_is_valid(self) -> None:
        from src.ucf101_dataset import UCF101Config
        cfg = UCF101Config()
        self.assertEqual(cfg.frames_per_clip, 16)
        self.assertEqual(cfg.output_size, (64, 64))
        self.assertTrue(cfg.resize)
        self.assertEqual(cfg.split, 'train')
        self.assertEqual(cfg.split_index, 1)

    def test_valid_config_accepts_all_fields(self) -> None:
        from src.ucf101_dataset import UCF101Config
        cfg = UCF101Config(
            root='/tmp/ucf101',
            frames_per_clip=32,
            output_size=(128, 128),
            resize=True,
            split='test',
            split_index=3,
            download_annotations=True,
            num_workers=8,
            batch_size=32,
            shuffle=False,
        )
        self.assertEqual(cfg.root, '/tmp/ucf101')
        self.assertEqual(cfg.frames_per_clip, 32)
        self.assertEqual(cfg.output_size, (128, 128))
        self.assertTrue(cfg.resize)
        self.assertEqual(cfg.split, 'test')
        self.assertEqual(cfg.split_index, 3)

    def test_zero_frames_per_clip_raises(self) -> None:
        from src.ucf101_dataset import UCF101Config
        with self.assertRaises(AssertionError):
            UCF101Config(frames_per_clip=0)

    def test_negative_output_size_raises(self) -> None:
        from src.ucf101_dataset import UCF101Config
        with self.assertRaises(AssertionError):
            UCF101Config(output_size=(0, 64))
        with self.assertRaises(AssertionError):
            UCF101Config(output_size=(64, -1))

    def test_invalid_split_raises(self) -> None:
        from src.ucf101_dataset import UCF101Config
        with self.assertRaises(AssertionError):
            UCF101Config(split='invalid')

    def test_invalid_split_index_raises(self) -> None:
        from src.ucf101_dataset import UCF101Config
        with self.assertRaises(AssertionError):
            UCF101Config(split_index=0)
        with self.assertRaises(AssertionError):
            UCF101Config(split_index=4)

    def test_negative_num_workers_raises(self) -> None:
        from src.ucf101_dataset import UCF101Config
        with self.assertRaises(AssertionError):
            UCF101Config(num_workers=-1)

    def test_zero_batch_size_raises(self) -> None:
        from src.ucf101_dataset import UCF101Config
        with self.assertRaises(AssertionError):
            UCF101Config(batch_size=0)


class TestUCF101DatasetInit(unittest.TestCase):
    """Behaviour: dataset instantiation validates files and parses annotations."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.mkdtemp(prefix='ucf101_test_')
        self._root = Path(self._tmpdir)
        self._video_dir = self._root / 'UCF101'
        self._video_dir.mkdir(parents=True, exist_ok=True)
        self._annotation_dir = self._root / 'annotations'
        self._annotation_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self._tmpdir)

    def test_missing_annotation_file_raises(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            download_annotations=False,
            download_videos=False,
        )
        with self.assertRaises(FileNotFoundError):
            UCF101Dataset(cfg)

    def test_empty_annotation_raises_runtime_error(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        _make_annotation_files(self._annotation_dir, entries=())
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            download_annotations=False,
            download_videos=False,
        )
        with self.assertRaises(RuntimeError):
            UCF101Dataset(cfg)

    def test_loads_samples_with_valid_annotations(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        entries = (
            ('ApplyEyeMakeup/v_ApplyEyeMakeup_g01_c01.avi', 0),
            ('Archery/v_Archery_g01_c01.avi', 1),
        )
        _make_annotation_files(self._annotation_dir, entries=entries)
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        self.assertEqual(len(dataset), 2)

    def test_num_classes_matches_annotation(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        entries = (
            ('class_a/v_a01.avi', 0),
            ('class_a/v_a02.avi', 0),
            ('class_b/v_b01.avi', 1),
            ('class_c/v_c01.avi', 2),
        )
        _make_annotation_files(self._annotation_dir, entries=entries)
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        self.assertEqual(dataset.num_classes, 3)


@unittest.skipIf(not _VIDEO_WRITE_AVAILABLE, 'no video encoding backend')
class TestUCF101DatasetGetItem(unittest.TestCase):
    """Behaviour: __getitem__ returns correctly processed video tensors."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.mkdtemp(prefix='ucf101_test_')
        self._root = Path(self._tmpdir)
        self._video_dir = self._root / 'UCF101'
        self._video_dir.mkdir(parents=True, exist_ok=True)
        self._annotation_dir = self._root / 'annotations'
        self._annotation_dir.mkdir(parents=True, exist_ok=True)
        self._entries = (
            ('ApplyEyeMakeup/v_ApplyEyeMakeup_g01_c01.avi', 0),
            ('Archery/v_Archery_g01_c01.avi', 1),
        )
        _make_annotation_files(self._annotation_dir, entries=self._entries)
        for idx, (rel_path, _) in enumerate(self._entries):
            _make_test_video(
                self._video_dir / rel_path,
                num_frames=48,
                height=240,
                width=320,
                seed=idx,
            )

    def tearDown(self) -> None:
        shutil.rmtree(self._tmpdir)

    def test_output_shape_with_resize(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=16,
            output_size=(64, 64),
            resize=True,
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        video = dataset[0]
        expected_shape = (16, 3, 64, 64)
        self.assertEqual(video.shape, expected_shape)

    def test_output_shape_without_resize(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=16,
            output_size=(64, 64),
            resize=False,
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        video = dataset[0]
        self.assertEqual(video.shape[0], 16)
        self.assertEqual(video.shape[1], 3)
        self.assertGreater(video.shape[2], 64)
        self.assertGreater(video.shape[3], 64)

    def test_pixel_range(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=16,
            output_size=(64, 64),
            resize=True,
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        video = dataset[0]
        self.assertGreaterEqual(video.min().item(), 0.0)
        self.assertLessEqual(video.max().item(), 1.0)

    def test_dtype_is_float32(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            output_size=(64, 64),
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        video = dataset[0]
        self.assertEqual(video.dtype, torch.float32)

    def test_different_indices_return_different_tensors(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=8,
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        v0 = dataset[0]
        v1 = dataset[1]
        self.assertFalse(torch.allclose(v0, v1))

    def test_short_video_gets_padded(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        short_rel = 'short/short_test.avi'
        _make_test_video(
            self._video_dir / short_rel,
            num_frames=5,
            height=240,
            width=320,
        )
        short_entries = (
            ('short/short_test.avi', 0),
        )
        _make_annotation_files(
            self._annotation_dir,
            split='test',
            split_index=1,
            entries=short_entries,
        )
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=16,
            output_size=(64, 64),
            resize=True,
            split='test',
            split_index=1,
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        video = dataset[0]
        self.assertEqual(video.shape[0], 16)

    def test_deterministic_output_for_same_index(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=8,
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        v0a = dataset[0]
        v0b = dataset[0]
        self.assertTrue(torch.allclose(v0a, v0b))


@unittest.skipIf(not _VIDEO_WRITE_AVAILABLE, 'no video encoding backend')
class TestUCF101DatasetErrors(unittest.TestCase):
    """Behaviour: dataset handles I/O errors gracefully."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.mkdtemp(prefix='ucf101_test_')
        self._root = Path(self._tmpdir)
        self._video_dir = self._root / 'UCF101'
        self._video_dir.mkdir(parents=True, exist_ok=True)
        self._annotation_dir = self._root / 'annotations'
        self._annotation_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self._tmpdir)

    def test_missing_video_file_returns_dummy(self) -> None:
        from src.ucf101_dataset import UCF101Config, UCF101Dataset
        entries = (
            ('nonexistent/missing.avi', 0),
        )
        _make_annotation_files(self._annotation_dir, entries=entries)
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=16,
            output_size=(64, 64),
            resize=True,
            download_annotations=False,
            download_videos=False,
        )
        dataset = UCF101Dataset(cfg)
        video = dataset[0]
        self.assertEqual(video.shape, (16, 3, 64, 64))
        self.assertEqual(video.sum().item(), 0.0)


class TestUCF101Dataloader(unittest.TestCase):
    """Behaviour: create_ucf101_dataloader returns a working DataLoader."""

    def setUp(self) -> None:
        self._tmpdir = tempfile.mkdtemp(prefix='ucf101_test_')
        self._root = Path(self._tmpdir)
        self._video_dir = self._root / 'UCF101'
        self._video_dir.mkdir(parents=True, exist_ok=True)
        self._annotation_dir = self._root / 'annotations'
        self._annotation_dir.mkdir(parents=True, exist_ok=True)
        self._entries = (
            ('class_a/v_a01.avi', 0),
            ('class_a/v_a02.avi', 0),
            ('class_b/v_b01.avi', 1),
        )
        _make_annotation_files(self._annotation_dir, entries=self._entries)
        if _VIDEO_WRITE_AVAILABLE:
            for idx, (rel_path, _) in enumerate(self._entries):
                _make_test_video(
                    self._video_dir / rel_path,
                    num_frames=24,
                    height=240,
                    width=320,
                    seed=idx,
                )

    def tearDown(self) -> None:
        shutil.rmtree(self._tmpdir)

    def test_dataloader_returns_batched_tensors(self) -> None:
        from src.ucf101_dataset import UCF101Config, create_ucf101_dataloader
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=16,
            output_size=(64, 64),
            resize=True,
            batch_size=2,
            shuffle=False,
            download_annotations=False,
            download_videos=False,
        )
        loader = create_ucf101_dataloader(cfg)
        batch = next(iter(loader))
        self.assertEqual(batch.shape[0], 2)
        if _VIDEO_WRITE_AVAILABLE:
            self.assertEqual(batch.shape[1], 16)
            self.assertEqual(batch.shape[2], 3)
            self.assertEqual(batch.shape[3], 64)
            self.assertEqual(batch.shape[4], 64)
            self.assertEqual(batch.dtype, torch.float32)

    def test_dataloader_works_with_trainer_pattern(self) -> None:
        from src.ucf101_dataset import UCF101Config, create_ucf101_dataloader
        cfg = UCF101Config(
            root=str(self._root),
            annotation_dir=str(self._annotation_dir),
            frames_per_clip=8,
            output_size=(64, 64),
            resize=True,
            batch_size=2,
            num_workers=0,
            shuffle=False,
            download_annotations=False,
            download_videos=False,
        )
        loader = create_ucf101_dataloader(cfg)
        for batch_idx, video in enumerate(loader):
            self.assertIsInstance(video, torch.Tensor)
            if _VIDEO_WRITE_AVAILABLE:
                self.assertEqual(video.dtype, torch.float32)
                self.assertGreaterEqual(video.min().item(), 0.0)
                self.assertLessEqual(video.max().item(), 1.0)
            if batch_idx >= 0:
                break


if __name__ == '__main__':
    unittest.main()
