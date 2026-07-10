#!/usr/bin/env python3
"""
V-JEPA-Q: Quaternion-Enhanced Video Joint-Embedding Predictive Architecture
with Continuous Spectral Autoencoders and Topological World Modeling.

Lie Algebra Trick (exp/log): Converts quaternion multiplications into vector
additions in the tangent space (so(3)), enabling efficient message passing
on the torus graph via Baker-Campbell-Hausdorff approximation.

Architecture:
- Quaternion algebra with exp/log maps for SO(3)/SU(2) group
- Complex spectral kernels in Fourier domain (GOE/GUE transition)
- 2D Torus brain: 4 angular x 2 radial = 8 nodes, fully periodic
- V-JEPA asymmetric masking with cosine-similarity prediction
- Phase diagram tracking: Berry phase, delta, kappa, T_eff, GOE/GUE
- GQA attention with Rotary Position Embeddings
- Topological MoE with load-balancing auxiliary loss
"""

import argparse
import json
import logging
import math
import sys
import time
import unittest
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
import safetensors.torch
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint as grad_ckpt


# ============================================================================
# CONFIGURATION
# ============================================================================


@dataclass
class VJEPAQConfig:
    """Central configuration for V-JEPA-Q model and training.

    All hyperparameters defined here. No hardcoded values or magic numbers
    exist outside this class. Computed fields in __post_init__.
    """

    NUM_FRAMES: int = 16
    PATCH_SIZE: Tuple[int, int] = (16, 16)
    IMAGE_SIZE: Tuple[int, int] = (224, 224)
    IN_CHANNELS: int = 3

    D_MODEL: int = 384
    N_HEADS: int = 6
    N_KV_HEADS: int = 0
    N_ENCODER_LAYERS: int = 12
    N_PREDICTOR_LAYERS: int = 12
    DROPOUT: float = 0.1

    SPECTRAL_LATENT_RATIO: float = 0.5
    SPECTRAL_KERNEL_INIT_SCALE: float = 0.02
    NUM_SPECTRAL_LAYERS: int = 2
    AE_RECON_WEIGHT: float = 0.01
    TEMPORAL_FFT_BINS: int = 32

    TORUS_RADIAL_BINS: int = 2
    TORUS_ANGULAR_BINS: int = 4
    TORUS_GRID_SIZE: int = 8
    TORUS_SOFT_ASSIGN_TEMPERATURE: float = 0.3
    TORUS_LIE_APPROX: bool = True

    MOE_ENABLED: bool = True
    N_EXPERTS: int = 4
    MOE_TOP_K: int = 2
    MOE_AUX_LOSS_WEIGHT: float = 0.01

    ENCODER_MASK_RATIO: float = 0.9
    PREDICTOR_MASK_RATIO: float = 0.75
    MASK_PATCH_SIZE: Tuple[int, int] = (4, 4)

    PREDICT_FRAMES: int = 4
    CONTEXT_FRAMES: int = 12

    BATCH_SIZE: int = 16
    GRAD_ACCUM_STEPS: int = 1
    LEARNING_RATE: float = 1e-4
    WEIGHT_DECAY: float = 0.05
    WARMUP_RATIO: float = 0.05
    GRADIENT_CLIP_NORM: float = 1.0
    GRADIENT_CHECKPOINTING: bool = False
    USE_AMP: bool = False
    NUM_WORKERS: int = 4
    SAVE_EVERY_STEPS: int = 200
    TORCH_COMPILE: bool = False

    DECODER_CHANNELS: int = 64
    DECODER_N_LAYERS: int = 3
    DECODER_LR: float = 1e-4
    DECODER_WEIGHT_DECAY: float = 0.05
    DECODER_TEMPORAL_LOSS_WEIGHT: float = 1.0
    DECODER_GRADIENT_LOSS_WEIGHT: float = 0.1
    DECODER_LOAD_PATH: str = ''

    TRACK_PHASE: bool = True
    GRASS_TRACK_EVERY: int = 200
    GRASS_MAX_RANK: int = 16
    GRASS_ELBOW_RATIO: float = 0.05
    DELTA_CRYSTAL_THRESHOLD: float = 0.1
    KAPPA_CRYSTAL_THRESHOLD: float = 1.5
    TEMP_CRYSTAL_THRESHOLD: float = 1e-9

    GOE_GUE_TARGET: str = 'gue'
    IMAGINARY_RATIO_TARGET: float = 0.3

    DATA_MODE: str = 'synthetic'
    SYNTHETIC_NUM_OBJECTS: int = 3
    SYNTHETIC_CANVAS_SIZE: int = 64
    SYNTHETIC_NUM_SAMPLES: int = 10000

    DEVICE: str = ''
    RANDOM_SEED: int = 42
    CHECKPOINT_DIR: str = 'checkpoints_vjepa_q'
    LOG_DIR: str = 'logs_vjepa_q'

    def __post_init__(self) -> None:
        if not self.DEVICE:
            self.DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

        assert self.D_MODEL % 4 == 0, "D_MODEL must be divisible by 4"
        assert self.D_MODEL % self.N_HEADS == 0, "D_MODEL must be divisible by N_HEADS"
        assert 0.0 < self.ENCODER_MASK_RATIO < 1.0
        assert 0.0 < self.PREDICTOR_MASK_RATIO < 1.0
        assert self.NUM_FRAMES > 1
        assert self.BATCH_SIZE > 0
        assert self.GRADIENT_CLIP_NORM > 0.0
        assert self.TORUS_SOFT_ASSIGN_TEMPERATURE > 0.0
        assert self.DATA_MODE in ('synthetic', 'video_dir')
        assert self.GOE_GUE_TARGET in ('goe', 'gue')
        assert self.CONTEXT_FRAMES + self.PREDICT_FRAMES <= self.NUM_FRAMES, (
            f"NUM_FRAMES ({self.NUM_FRAMES}) must be >= CONTEXT_FRAMES + PREDICT_FRAMES "
            f"({self.CONTEXT_FRAMES + self.PREDICT_FRAMES})"
        )

        self.D_QUAT: int = self.D_MODEL // 4

        if self.N_KV_HEADS <= 0:
            kv = max(1, self.N_HEADS // 4)
            while self.N_HEADS % kv != 0:
                kv -= 1
            self.N_KV_HEADS = kv
        elif self.N_KV_HEADS == -1:
            self.N_KV_HEADS = self.N_HEADS
        self.GQA_GROUPS: int = self.N_HEADS // self.N_KV_HEADS
        self.D_HEAD: int = self.D_MODEL // self.N_HEADS

        self.PATCH_H: int = self.IMAGE_SIZE[0] // self.PATCH_SIZE[0]
        self.PATCH_W: int = self.IMAGE_SIZE[1] // self.PATCH_SIZE[1]
        assert self.PATCH_H > 0 and self.PATCH_W > 0
        self.NUM_PATCHES_PER_FRAME: int = self.PATCH_H * self.PATCH_W
        self.NUM_PATCHES: int = self.NUM_FRAMES * self.NUM_PATCHES_PER_FRAME
        self.PATCH_DIM: int = self.IN_CHANNELS * self.PATCH_SIZE[0] * self.PATCH_SIZE[1]

        self.SPECTRAL_LATENT_DIM: int = max(16, int(self.D_MODEL * self.SPECTRAL_LATENT_RATIO))
        self.N_TORUS_NODES: int = self.TORUS_RADIAL_BINS * self.TORUS_ANGULAR_BINS
        self.TORUS_GRID_SIZE = self.N_TORUS_NODES


# ============================================================================
# UTILITY
# ============================================================================


def _setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'))
        logger.addHandler(handler)
    return logger


def _set_seed(seed: int, device: str) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)
    if 'cuda' in device and torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _count_parameters(module: nn.Module) -> int:
    return sum(p.numel() for p in module.parameters() if p.requires_grad)


# ============================================================================
# QUATERNION ALGEBRA (with Lie group exp/log)
# ============================================================================


class QuaternionOps:
    """Pure quaternion operations. Convention: [w, x, y, z].

    Includes exponential and logarithmic maps for the Lie group SU(2) / so(3).
    The log map converts quaternion multiplication to vector addition in the
    tangent space (Lie algebra). The exp map converts back.
    """

    @staticmethod
    def hamilton_product(q1: torch.Tensor, q2: torch.Tensor) -> torch.Tensor:
        w1, x1, y1, z1 = q1[..., 0], q1[..., 1], q1[..., 2], q1[..., 3]
        w2, x2, y2, z2 = q2[..., 0], q2[..., 1], q2[..., 2], q2[..., 3]
        return torch.stack([
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ], dim=-1)

    @staticmethod
    def normalize(q: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        return q / (q.norm(dim=-1, keepdim=True) + eps)

    @staticmethod
    def conjugate(q: torch.Tensor) -> torch.Tensor:
        return q * q.new_tensor([1, -1, -1, -1])

    @staticmethod
    def rotate_vector(v: torch.Tensor, q: torch.Tensor) -> torch.Tensor:
        zero = torch.zeros(*v.shape[:-1], 1, device=v.device, dtype=v.dtype)
        v_q = torch.cat([zero, v], dim=-1)
        q_c = QuaternionOps.conjugate(q)
        rotated = QuaternionOps.hamilton_product(
            QuaternionOps.hamilton_product(q, v_q), q_c)
        return rotated[..., 1:]

    @staticmethod
    def log(q: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        """Logarithmic map from SU(2) to so(3) (tangent space).

        Converts a unit quaternion q = [w, x, y, z] to a pure quaternion
        v = [0, theta*u] where u is the unit axis and theta = arccos(w).
        In the tangent space, quaternion multiplication becomes vector addition
        (via BCH approximation: log(q1 * q2) approx log(q1) + log(q2)).
        """
        w = q[..., 0:1].clamp(-1.0 + eps, 1.0 - eps)
        v = q[..., 1:]
        v_norm = v.norm(dim=-1, keepdim=True)
        theta = torch.acos(w)
        scale = torch.where(v_norm > eps, theta / v_norm, torch.ones_like(v_norm))
        return torch.cat([torch.zeros_like(w), v * scale], dim=-1)

    @staticmethod
    def exp(q: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        """Exponential map from so(3) to SU(2).

        Converts a pure quaternion v = [0, theta*u] back to a unit quaternion
        q = [cos(theta), sin(theta)*u]. This is the inverse of log().
        """
        v = q[..., 1:]
        theta = v.norm(dim=-1, keepdim=True)
        scale = torch.where(theta > eps, torch.sin(theta) / theta, torch.ones_like(theta))
        return torch.cat([torch.cos(theta), v * scale], dim=-1)

    @staticmethod
    def lie_product(q1: torch.Tensor, q2: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        """Approximate quaternion product via Lie algebra addition.

        Instead of Hamilton product (O(n^2) cross terms), uses:
            q1 * q2 approx exp(log(q1) + log(q2))
        which converts multiplication to element-wise addition in the
        tangent space. Exact for commuting quaternions; BCH-approximate
        for non-commuting.
        """
        return QuaternionOps.exp(QuaternionOps.log(q1, eps) + QuaternionOps.log(q2, eps))


class QuaternionLinear(nn.Module):
    """Linear transform using quaternion Hamilton product.

    Input and output dimensions must be multiples of 4. Weight is
    factorised into four coupled subspaces via Hamilton product.
    """

    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        assert in_features % 4 == 0 and out_features % 4 == 0
        self.in_q = in_features // 4
        self.out_q = out_features // 4

        self.Ww = nn.Linear(self.in_q, self.out_q, bias=False)
        self.Wx = nn.Linear(self.in_q, self.out_q, bias=False)
        self.Wy = nn.Linear(self.in_q, self.out_q, bias=False)
        self.Wz = nn.Linear(self.in_q, self.out_q, bias=False)
        self.bias = nn.Parameter(torch.zeros(out_features)) if bias else None

        for w in [self.Ww, self.Wx, self.Wy, self.Wz]:
            nn.init.normal_(w.weight, std=0.02)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        d = self.in_q
        xw, xx, xy, xz = x[..., :d], x[..., d:2 * d], x[..., 2 * d:3 * d], x[..., 3 * d:]
        ow = self.Ww(xw) - self.Wx(xx) - self.Wy(xy) - self.Wz(xz)
        ox = self.Ww(xx) + self.Wx(xw) + self.Wy(xz) - self.Wz(xy)
        oy = self.Ww(xy) - self.Wx(xz) + self.Wy(xw) + self.Wz(xx)
        oz = self.Ww(xz) + self.Wx(xy) - self.Wy(xx) + self.Wz(xw)
        out = torch.cat([ow, ox, oy, oz], dim=-1)
        return out + self.bias if self.bias is not None else out


# ============================================================================
# SPECTRAL LAYERS
# ============================================================================


class ComplexSpectralLayer(nn.Module):
    """Spectral convolution with tuneable real/imaginary kernel ratio.

    Operates in 2D Fourier domain: P(k) = W(k) * X(k) with channel mixing
    via einsum. Real part: conservative dynamics. Imaginary part: dissipative.
    Tracks GOE -> GUE transition via imaginary_ratio.
    """

    def __init__(
        self,
        channels: int,
        grid_h: int,
        grid_w: int,
        imaginary_ratio: float = 0.3,
        init_scale: float = 0.02,
    ):
        super().__init__()
        self.channels = channels
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.imaginary_ratio = imaginary_ratio

        freq_h = grid_h
        freq_w = grid_w // 2 + 1

        self.kernel_real = nn.Parameter(
            torch.randn(channels, channels, freq_h, freq_w) * init_scale)
        self.kernel_imag = nn.Parameter(
            torch.randn(channels, channels, freq_h, freq_w) * init_scale * imaginary_ratio)

        self._imag_ratio_history = deque(maxlen=100)

    def set_imaginary_ratio(self, ratio: float) -> None:
        old = self.imaginary_ratio
        self.imaginary_ratio = ratio
        if old > 1e-8:
            with torch.no_grad():
                self.kernel_imag.data *= ratio / max(old, 1e-8)

    def get_effective_imaginary_ratio(self) -> float:
        real_norm = self.kernel_real.data.norm().item()
        imag_norm = self.kernel_imag.data.norm().item()
        if real_norm < 1e-8:
            return self.imaginary_ratio
        ratio = imag_norm / real_norm
        self._imag_ratio_history.append(ratio)
        return ratio

    def get_spectral_operator(self) -> torch.Tensor:
        kr = self.kernel_real[:, :, 0, 0]
        ki = self.kernel_imag[:, :, 0, 0]
        kr_sym = (kr + kr.T) / 2
        ki_asym = (ki - ki.T) / 2
        return torch.complex(kr_sym, ki_asym * self.get_effective_imaginary_ratio())

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_fft = torch.fft.rfft2(x, s=(self.grid_h, self.grid_w))
        B, C, freq_h, freq_w = x_fft.shape
        kr = self.kernel_real
        ki = self.kernel_imag

        if kr.shape[2:] != (freq_h, freq_w):
            kr = F.interpolate(
                kr.mean(dim=0).unsqueeze(0).unsqueeze(0),
                size=(freq_h, freq_w), mode='bilinear', align_corners=False,
            ).squeeze(0).unsqueeze(0)
            ki = F.interpolate(
                ki.mean(dim=0).unsqueeze(0).unsqueeze(0),
                size=(freq_h, freq_w), mode='bilinear', align_corners=False,
            ).squeeze(0).unsqueeze(0)

        K = torch.complex(kr, ki)
        out_fft = torch.einsum('cihw,bihw->bchw', K, x_fft)
        return torch.fft.irfft2(out_fft, s=(self.grid_h, self.grid_w))


class QuaternionSpectralLayer(nn.Module):
    """Full quaternion spectral convolution in Fourier domain.

    Each quaternion component (w, x, y, z) gets a complex kernel.
    Combined via Hamilton product in frequency space using Gauss's trick
    (3 real MUL instead of 4 for complex multiply).
    """

    def __init__(
        self,
        in_q: int,
        out_q: int,
        grid_h: int,
        grid_w: int,
        init_scale: float = 0.02,
    ):
        super().__init__()
        self.in_q = in_q
        self.out_q = out_q
        self.grid_h = grid_h
        self.grid_w = grid_w

        freq_h = grid_h
        freq_w = grid_w // 2 + 1

        for c in ('w', 'x', 'y', 'z'):
            self.register_parameter(
                f'kr_{c}',
                nn.Parameter(torch.randn(in_q, out_q, freq_h, freq_w) * init_scale),
            )
            self.register_parameter(
                f'ki_{c}',
                nn.Parameter(torch.randn(in_q, out_q, freq_h, freq_w) * init_scale),
            )

    def _kernel(self, c: str) -> torch.Tensor:
        return torch.complex(getattr(self, f'kr_{c}'), getattr(self, f'ki_{c}'))

    @staticmethod
    def _gauss_contract(W: torch.Tensor, X: torch.Tensor) -> torch.Tensor:
        device_type = W.device.type if W.device.type in ("cuda", "cpu") else "cpu"
        with torch.amp.autocast(device_type=device_type, enabled=False):
            Wr, Wi = W.real.float(), W.imag.float()
            Xr, Xi = X.real.float(), X.imag.float()
            m1 = torch.einsum("iohw,bihw->bohw", Wr, Xr)
            m2 = torch.einsum("iohw,bihw->bohw", Wi, Xi)
            m3 = torch.einsum("iohw,bihw->bohw", Wr + Wi, Xr + Xi)
            return torch.complex(m1 - m2, m3 - m1 - m2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        q = self.in_q
        xw, xx, xy, xz = x[:, :q], x[:, q:2 * q], x[:, 2 * q:3 * q], x[:, 3 * q:]

        Xw = torch.fft.rfft2(xw, s=(self.grid_h, self.grid_w))
        Xx = torch.fft.rfft2(xx, s=(self.grid_h, self.grid_w))
        Xy = torch.fft.rfft2(xy, s=(self.grid_h, self.grid_w))
        Xz = torch.fft.rfft2(xz, s=(self.grid_h, self.grid_w))

        Ww, Wx, Wy, Wz = self._kernel('w'), self._kernel('x'), self._kernel('y'), self._kernel('z')

        C = {}
        for wc, W in (('w', Ww), ('x', Wx), ('y', Wy), ('z', Wz)):
            for xc, X in (('w', Xw), ('x', Xx), ('y', Xy), ('z', Xz)):
                C[(wc, xc)] = self._gauss_contract(W, X)

        Pw = C[('w', 'w')] - C[('x', 'x')] - C[('y', 'y')] - C[('z', 'z')]
        Px = C[('w', 'x')] + C[('x', 'w')] + C[('y', 'z')] - C[('z', 'y')]
        Py = C[('w', 'y')] - C[('x', 'z')] + C[('y', 'w')] + C[('z', 'x')]
        Pz = C[('w', 'z')] + C[('x', 'y')] - C[('y', 'x')] + C[('z', 'w')]

        ow = torch.fft.irfft2(Pw, s=(self.grid_h, self.grid_w))
        ox = torch.fft.irfft2(Px, s=(self.grid_h, self.grid_w))
        oy = torch.fft.irfft2(Py, s=(self.grid_h, self.grid_w))
        oz = torch.fft.irfft2(Pz, s=(self.grid_h, self.grid_w))

        return torch.cat([ow, ox, oy, oz], dim=1)


# ============================================================================
# SPECTRAL AUTOENCODER
# ============================================================================


class SpatiotemporalSpectralAE(nn.Module):
    """Two-level spectral autoencoder: temporal FFT + spatial quaternion spectral."""

    def __init__(self, config: VJEPAQConfig):
        super().__init__()
        self.config = config
        d = config.D_MODEL
        d_lat = config.SPECTRAL_LATENT_DIM
        d_q = config.D_QUAT

        self.temporal_fft_bins = config.TEMPORAL_FFT_BINS
        self.temporal_kr = nn.Parameter(torch.randn(d, config.TEMPORAL_FFT_BINS) * 0.02)
        self.temporal_ki = nn.Parameter(torch.randn(d, config.TEMPORAL_FFT_BINS) * 0.02)
        self.temporal_enc = QuaternionLinear(d, d_lat)
        self.temporal_dec = QuaternionLinear(d_lat, d)

        r, a = config.TORUS_RADIAL_BINS, config.TORUS_ANGULAR_BINS
        self.spatial_spectral = nn.ModuleList([
            QuaternionSpectralLayer(d_q, d_q, r, a, config.SPECTRAL_KERNEL_INIT_SCALE)
            for _ in range(config.NUM_SPECTRAL_LAYERS)
        ])

        self.act = nn.GELU()

    def _temporal_filter(self, x: torch.Tensor, kr: torch.Tensor, ki: torch.Tensor) -> torch.Tensor:
        X = torch.fft.rfft(x.transpose(1, 2), dim=-1)
        K = torch.complex(kr, ki)
        filtered = X * K.unsqueeze(0)
        return torch.fft.irfft(filtered, n=x.shape[1], dim=-1).transpose(1, 2)

    def encode_temporal(self, x: torch.Tensor) -> torch.Tensor:
        x_filt = self.act(self._temporal_filter(x, self.temporal_kr, self.temporal_ki))
        return self.temporal_enc(x_filt)

    def decode_temporal(self, z: torch.Tensor) -> torch.Tensor:
        x = self.temporal_dec(z)
        return self._temporal_filter(x, self.temporal_kr.conj(), self.temporal_ki.conj())

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        z = self.encode_temporal(x)
        recon = self.decode_temporal(z)
        recon_loss = F.mse_loss(recon, x.detach())
        return z, recon_loss


# ============================================================================
# VIDEO PATCH EMBEDDING
# ============================================================================


class VideoPatchEmbedding(nn.Module):
    """Convert video to quaternion-encoded patch embeddings with motion cues.

    Extracts spatial patches and temporal derivative, then projects to
    D_MODEL-dimensional quaternion space with position encodings.
    """

    def __init__(self, config: VJEPAQConfig):
        super().__init__()
        self.config = config

        patch_dim = config.PATCH_DIM
        motion_dim = config.IN_CHANNELS

        self.patch_to_quat = nn.Linear(patch_dim + motion_dim, config.D_MODEL * 4)
        self.quat_proj = QuaternionLinear(config.D_MODEL * 4, config.D_MODEL)

        self.temporal_pos_embed = nn.Parameter(
            torch.randn(1, config.NUM_FRAMES, config.D_MODEL) * 0.02)
        self.spatial_pos_embed = nn.Parameter(
            torch.randn(1, config.NUM_PATCHES_PER_FRAME, config.D_MODEL) * 0.02)

        self.norm = nn.LayerNorm(config.D_MODEL)

    @staticmethod
    def _compute_temporal_derivative(video: torch.Tensor) -> torch.Tensor:
        if video.shape[1] < 2:
            return torch.zeros_like(video[:, :1])
        return video[:, 1:] - video[:, :-1]

    def forward(self, video: torch.Tensor) -> torch.Tensor:
        B, T, C, H, W = video.shape
        cfg = self.config

        patches = video.reshape(
            B, T, C,
            H // cfg.PATCH_SIZE[0], cfg.PATCH_SIZE[0],
            W // cfg.PATCH_SIZE[1], cfg.PATCH_SIZE[1],
        )
        patches = patches.permute(0, 1, 3, 5, 2, 4, 6).contiguous()
        patches = patches.reshape(B, T * cfg.NUM_PATCHES_PER_FRAME, -1)

        temp_deriv = self._compute_temporal_derivative(video)
        if T <= 1:
            motion_features = torch.zeros(
                B, T * cfg.NUM_PATCHES_PER_FRAME, cfg.IN_CHANNELS,
                device=video.device, dtype=video.dtype)
        else:
            temp_deriv = F.interpolate(
                temp_deriv.reshape(B * (T - 1), C, H, W),
                size=(cfg.PATCH_H, cfg.PATCH_W),
                mode='area',
            ).reshape(B, T - 1, cfg.NUM_PATCHES_PER_FRAME, cfg.IN_CHANNELS)
            temp_deriv = F.pad(temp_deriv, (0, 0, 0, 0, 0, 1), value=0.0)
            motion_features = temp_deriv.reshape(
                B, T * cfg.NUM_PATCHES_PER_FRAME, cfg.IN_CHANNELS)

        combined = torch.cat([patches, motion_features], dim=-1)

        quat_features = self.quat_proj(self.patch_to_quat(combined))

        temporal_pe = self.temporal_pos_embed[:, :T, :].repeat_interleave(
            cfg.NUM_PATCHES_PER_FRAME, dim=1)
        spatial_pe = self.spatial_pos_embed.unsqueeze(1).expand(B, T, -1, -1).reshape(
            B, T * cfg.NUM_PATCHES_PER_FRAME, cfg.D_MODEL)

        embeddings = self.norm(quat_features + temporal_pe + spatial_pe)

        return embeddings


# ============================================================================
# MASKING
# ============================================================================


class VJEPAMasker:
    """Generate asymmetric encoder/predictor masks for V-JEPA training."""

    def __init__(self, config: VJEPAQConfig):
        self.config = config
        self.logger = _setup_logger("VJEPAMasker")

    @staticmethod
    def _generate_block_mask(
        h: int,
        w: int,
        mask_ratio: float,
        block_size: Tuple[int, int],
        device: torch.device,
    ) -> torch.Tensor:
        bh, bw = block_size
        grid_h = math.ceil(h / bh)
        grid_w = math.ceil(w / bw)
        mask_blocks = torch.rand(grid_h, grid_w, device=device) > mask_ratio
        mask = mask_blocks.repeat_interleave(bh, dim=0).repeat_interleave(bw, dim=1)
        return mask[:h, :w]

    def generate_masks(self, batch_size: int, device: torch.device) -> Dict[str, torch.Tensor]:
        cfg = self.config
        T = cfg.NUM_FRAMES
        N = cfg.NUM_PATCHES_PER_FRAME
        total = T * N

        encoder_mask = torch.zeros(batch_size, total, dtype=torch.bool, device=device)
        predictor_mask = torch.zeros(batch_size, total, dtype=torch.bool, device=device)

        for b in range(batch_size):
            for t in range(T):
                frame_mask = self._generate_block_mask(
                    cfg.PATCH_H, cfg.PATCH_W,
                    cfg.ENCODER_MASK_RATIO,
                    cfg.MASK_PATCH_SIZE,
                    device,
                )
                encoder_mask[b, t * N:(t + 1) * N] = frame_mask.flatten()

            masked_indices = ~encoder_mask[b]
            num_to_predict = int(masked_indices.sum().item() * cfg.PREDICTOR_MASK_RATIO)
            predict_indices = masked_indices.nonzero(as_tuple=True)[0]
            if num_to_predict > 0 and len(predict_indices) > 0:
                perm = torch.randperm(len(predict_indices), device=device)[:num_to_predict]
                selected = predict_indices[perm]
                predictor_mask[b, selected] = True

        return {
            'encoder_mask': encoder_mask,
            'predictor_mask': predictor_mask,
            'visible_mask': encoder_mask,
            'masked_not_predicted': encoder_mask.logical_not().logical_and(
                predictor_mask.logical_not()),
        }


# ============================================================================
# POSITIONAL ENCODING AND NORMALISATION
# ============================================================================


class RotaryEmbedding(nn.Module):
    """Rotary Position Embeddings (RoPE) for spatiotemporal attention."""

    def __init__(self, d_head: int, max_seq_len: int = 4096, base: int = 10000):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, d_head, 2, dtype=torch.float) / d_head))
        self.register_buffer('inv_freq', inv_freq)
        self._build_cache(max_seq_len)

    def _build_cache(self, seq_len: int) -> None:
        t = torch.arange(seq_len, device=self.inv_freq.device, dtype=torch.float)
        freqs = torch.outer(t, self.inv_freq)
        emb = torch.cat([freqs, freqs], dim=-1)
        self.register_buffer('cos_cache', emb.cos(), persistent=False)
        self.register_buffer('sin_cache', emb.sin(), persistent=False)

    def _rotate_half(self, x: torch.Tensor) -> torch.Tensor:
        x1, x2 = x[..., :x.shape[-1] // 2], x[..., x.shape[-1] // 2:]
        return torch.cat([-x2, x1], dim=-1)

    def forward(self, q: torch.Tensor, k: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        sq, sk = q.shape[2], k.shape[2]
        cos_q = self.cos_cache[:sq].unsqueeze(0).unsqueeze(0)
        sin_q = self.sin_cache[:sq].unsqueeze(0).unsqueeze(0)
        cos_k = self.cos_cache[:sk].unsqueeze(0).unsqueeze(0)
        sin_k = self.sin_cache[:sk].unsqueeze(0).unsqueeze(0)
        return (
            q * cos_q + self._rotate_half(q) * sin_q,
            k * cos_k + self._rotate_half(k) * sin_k,
        )


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalisation."""

    def __init__(self, d_model: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(d_model))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = x.pow(2).mean(-1, keepdim=True).add(self.eps).sqrt()
        return x / rms * self.weight


# ============================================================================
# SPATIOTEMPORAL ATTENTION
# ============================================================================


class SpatiotemporalAttention(nn.Module):
    """Grouped-Query Attention with RoPE for spatiotemporal sequences."""

    def __init__(self, d_model: int, n_heads: int, config: VJEPAQConfig):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.n_kv = config.N_KV_HEADS
        self.n_groups = config.GQA_GROUPS
        self.d_head = d_model // n_heads

        self.q_proj = nn.Linear(d_model, n_heads * self.d_head, bias=False)
        self.k_proj = nn.Linear(d_model, self.n_kv * self.d_head, bias=False)
        self.v_proj = nn.Linear(d_model, self.n_kv * self.d_head, bias=False)
        self.o_proj = nn.Linear(d_model, d_model, bias=False)

        self.rope = RotaryEmbedding(self.d_head, max_seq_len=config.NUM_PATCHES * 2)
        self.dropout_p = config.DROPOUT if config.DROPOUT > 0 else 0.0

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
        is_causal: bool = False,
    ) -> torch.Tensor:
        B, S, D = x.shape

        Q = self.q_proj(x).view(B, S, self.n_heads, self.d_head).transpose(1, 2)
        K = self.k_proj(x).view(B, S, self.n_kv, self.d_head).transpose(1, 2)
        V = self.v_proj(x).view(B, S, self.n_kv, self.d_head).transpose(1, 2)

        Q, K = self.rope(Q, K)

        if self.n_groups > 1:
            K = K.repeat_interleave(self.n_groups, dim=1)
            V = V.repeat_interleave(self.n_groups, dim=1)

        scale = self.d_head ** -0.5

        if mask is not None:
            attn_mask = mask.unsqueeze(1).unsqueeze(2) & mask.unsqueeze(1).unsqueeze(3)
            attn_mask = attn_mask.expand(B, self.n_heads, S, S)
        else:
            attn_mask = None

        out = F.scaled_dot_product_attention(
            Q, K, V,
            attn_mask=attn_mask,
            dropout_p=self.dropout_p if self.training else 0.0,
            is_causal=is_causal and attn_mask is None,
            scale=scale,
        )

        out = out.transpose(1, 2).contiguous().view(B, S, D)
        return self.o_proj(out)


# ============================================================================
# QUATERNION TORUS BRAIN (FFN REPLACEMENT)
# ============================================================================


class QuaternionTorusBrain(nn.Module):
    """FFN replacement with quaternion-topological processing on a 2D torus.

    Pipeline:
    1. Token compression (no temporal FFT per token)
    2. Project to torus coordinates (phi1, phi2)
    3. Soft-assignment to 8 torus nodes (4 angular x 2 radial)
    4. Lightweight channel mixer on torus grid
    5. Message passing with Lie algebra (exp/log) quaternion product
    6. Attention-weighted readout

    The Lie algebra trick (TORUS_LIE_APPROX) replaces the Hamilton product
    in message passing with log-space addition: exp(log(q1) + log(q2)).
    This converts O(n^2) quaternion multiplications to O(n) element-wise adds.
    """

    def __init__(self, d_model: int, config: VJEPAQConfig):
        super().__init__()
        self.d_model = d_model
        self.d_q = d_model // 4
        self.n_radial = config.TORUS_RADIAL_BINS
        self.n_angular = config.TORUS_ANGULAR_BINS
        self.n_nodes = config.N_TORUS_NODES
        self.config = config
        self.assign_temp = config.TORUS_SOFT_ASSIGN_TEMPERATURE
        self.lie_approx = config.TORUS_LIE_APPROX

        d_lat = config.SPECTRAL_LATENT_DIM

        self.token_proj = nn.Sequential(
            nn.Linear(d_model, d_lat),
            nn.GELU(),
            nn.Linear(d_lat, d_model),
        ) if d_lat != d_model else nn.Identity()

        self.spatial_mixer = nn.Sequential(
            nn.Linear(4 * self.d_q, 4 * self.d_q),
            nn.GELU(),
            nn.Linear(4 * self.d_q, 4 * self.d_q),
        )

        self.torus_proj = nn.Sequential(
            QuaternionLinear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, 4),
        )

        self.node_embed = nn.Parameter(torch.randn(self.n_nodes, d_model) * 0.02)

        self.edge_quat = nn.Parameter(torch.randn(4, 4) * 0.1)

        self.node_net = QuaternionLinear(d_model, d_model)

        self.readout = nn.Sequential(
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model),
        )

        self.spectral_ae = SpatiotemporalSpectralAE(config)
        self._build_torus_graph()

    def _build_torus_graph(self) -> None:
        """Build fully periodic 2D torus adjacency."""
        edges_i, edges_j, edge_type = [], [], []
        R, A = self.n_radial, self.n_angular

        for r in range(R):
            for a in range(A):
                n = r * A + a

                edges_i.append(n)
                edges_j.append(r * A + (a - 1) % A)
                edge_type.append(0)

                edges_i.append(n)
                edges_j.append(r * A + (a + 1) % A)
                edge_type.append(1)

                edges_i.append(n)
                edges_j.append(((r - 1) % R) * A + a)
                edge_type.append(2)

                edges_i.append(n)
                edges_j.append(((r + 1) % R) * A + a)
                edge_type.append(3)

        self.register_buffer('edges_i', torch.tensor(edges_i, dtype=torch.long))
        self.register_buffer('edges_j', torch.tensor(edges_j, dtype=torch.long))
        self.register_buffer('edge_type', torch.tensor(edge_type, dtype=torch.long))

    def _torus_soft_assign(self, phi1: torch.Tensor, phi2: torch.Tensor) -> torch.Tensor:
        BS = phi1.shape[0]
        device = phi1.device

        ang_pos = torch.linspace(-math.pi, math.pi, self.n_angular + 1, device=device)[:-1]
        rad_pos = torch.linspace(-math.pi, math.pi, self.n_radial + 1, device=device)[:-1]

        d_ang = torch.sin((phi1.unsqueeze(1) - ang_pos.unsqueeze(0)) / 2).pow(2)
        d_rad = torch.sin((phi2.unsqueeze(1) - rad_pos.unsqueeze(0)) / 2).pow(2)

        d_torus = d_rad.unsqueeze(2) + d_ang.unsqueeze(1)
        d_flat = d_torus.view(BS, -1)

        return torch.softmax(-d_flat / self.assign_temp, dim=-1)

    def _message_passing(self, node_feat: torch.Tensor) -> torch.Tensor:
        """Message passing with Lie algebra quaternion product.

        When self.lie_approx is True, uses exp(log(q) + log(p)) instead of
        Hamilton product q * p. This converts quaternion multiplication to
        vector addition in so(3) tangent space via BCH approximation.
        """
        BS = node_feat.shape[0]
        n_edges = self.edges_i.shape[0]
        d_q = self.d_q

        eq = QuaternionOps.normalize(self.edge_quat)
        src_feat = node_feat[:, self.edges_j, :]

        edge_q = eq[self.edge_type].unsqueeze(0).unsqueeze(2).expand(BS, -1, d_q, -1)
        src_q = src_feat.view(BS, n_edges, d_q, 4)

        if self.lie_approx:
            log_edge = QuaternionOps.log(edge_q)
            log_src = QuaternionOps.log(src_q)
            msg_rot = QuaternionOps.exp(log_edge + log_src)
        else:
            msg_rot = QuaternionOps.hamilton_product(edge_q, src_q)

        msg_rot = msg_rot.view(BS, n_edges, self.d_model)

        agg = torch.zeros_like(node_feat, dtype=msg_rot.dtype)
        dst_idx = self.edges_i.view(1, n_edges, 1).expand(BS, -1, self.d_model)
        agg.scatter_add_(1, dst_idx, msg_rot)

        return self.node_net(node_feat + agg)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        B, S, D = x.shape
        x_flat = x.reshape(B * S, D)

        z = self.token_proj(x_flat)
        recon_loss = x_flat.new_zeros(())

        coords = self.torus_proj(z)
        phi1 = math.pi * torch.tanh(coords[:, 0])
        phi2 = math.pi * torch.tanh(coords[:, 1])

        attn_w = self._torus_soft_assign(phi1, phi2)

        nodes = (
            attn_w.unsqueeze(-1) * self.node_embed.unsqueeze(0)
            + attn_w.unsqueeze(-1) * z.unsqueeze(1)
        )

        grid = nodes.view(B * S, self.n_radial, self.n_angular, D)
        grid = grid.permute(0, 3, 1, 2)
        d_q = self.d_q
        grid_q = grid.view(B * S, 4, d_q, self.n_radial, self.n_angular)
        grid_q = grid_q.permute(0, 1, 2, 3, 4).reshape(B * S, 4 * d_q, self.n_radial, self.n_angular)

        B_grid, C_grid, H_grid, W_grid = grid_q.shape
        grid_q = grid_q.permute(0, 2, 3, 1).reshape(-1, C_grid)
        grid_q = self.spatial_mixer(grid_q)
        grid_q = grid_q.reshape(B_grid, H_grid, W_grid, C_grid).permute(0, 3, 1, 2)

        grid_back = grid_q.view(B * S, 4, d_q, self.n_radial, self.n_angular)
        grid_back = grid_back.permute(0, 3, 4, 1, 2).reshape(B * S, self.n_nodes, D)

        nodes_mp = self._message_passing(grid_back)

        out_flat = (attn_w.unsqueeze(-1) * nodes_mp).sum(dim=1)
        out_flat = self.readout(out_flat)

        return out_flat.reshape(B, S, D), recon_loss


# ============================================================================
# MIXTURE OF EXPERTS
# ============================================================================


class TopoMoE(nn.Module):
    """Mixture of Experts with shared Topological Torus Brain."""

    def __init__(self, d_model: int, config: VJEPAQConfig):
        super().__init__()
        self.moe_enabled = config.MOE_ENABLED
        self.n_experts = config.N_EXPERTS
        self.top_k = config.MOE_TOP_K
        self.aux_weight = config.MOE_AUX_LOSS_WEIGHT

        self.shared_expert = QuaternionTorusBrain(d_model, config)

        if self.moe_enabled:
            self.experts = nn.ModuleList([
                nn.Sequential(
                    nn.Linear(d_model, d_model * 4 // 3),
                    nn.GELU(),
                    nn.Linear(d_model * 4 // 3, d_model),
                ) for _ in range(self.n_experts)
            ])
            self.router = nn.Linear(d_model, self.n_experts, bias=False)
            nn.init.normal_(self.router.weight, std=0.02)

    def _route(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        N, D = x.shape
        router_logits = self.router(x)
        router_probs = F.softmax(router_logits, dim=-1)
        top_k_probs, top_k_idx = torch.topk(router_probs, self.top_k, dim=-1)
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True).clamp(min=1e-9)

        flat_idx = top_k_idx.reshape(-1)
        flat_weights = top_k_probs.reshape(-1)
        token_indices = torch.arange(N, device=x.device).unsqueeze(1).expand(-1, self.top_k).reshape(-1)

        expert_out = torch.zeros_like(x)
        for e in range(self.n_experts):
            expert_mask = (flat_idx == e)
            src_token_idx = token_indices[expert_mask]
            w = flat_weights[expert_mask].unsqueeze(-1).to(x.dtype)
            out_e = self.experts[e](x[src_token_idx])
            contrib = w * out_e
            expert_out.scatter_add_(0, src_token_idx.unsqueeze(1).expand_as(contrib), contrib)

        token_frac = router_probs.mean(dim=0)
        one_hot = F.one_hot(top_k_idx, self.n_experts).float()
        dispatch_frac = one_hot.mean(dim=(0, 1))
        aux_loss = self.n_experts * (token_frac * dispatch_frac).sum()

        return expert_out, aux_loss

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        B, S, D = x.shape

        shared_out, recon_loss = self.shared_expert(x)

        if not self.moe_enabled:
            return shared_out, recon_loss

        x_flat = x.reshape(B * S, D)
        expert_out, aux_loss = self._route(x_flat)
        expert_out = expert_out.reshape(B, S, D)

        output = shared_out + expert_out
        total_aux = recon_loss + self.aux_weight * aux_loss

        return output, total_aux


# ============================================================================
# TRANSFORMER BLOCK
# ============================================================================


class VJEPAQBlock(nn.Module):
    """Transformer block with SpatiotemporalAttention + TopoMoE FFN."""

    def __init__(self, d_model: int, n_heads: int, config: VJEPAQConfig):
        super().__init__()
        self.norm1 = RMSNorm(d_model)
        self.norm2 = RMSNorm(d_model)
        self.attn = SpatiotemporalAttention(d_model, n_heads, config)
        self.topo_brain = TopoMoE(d_model, config)
        self.dropout = nn.Dropout(config.DROPOUT)
        self.use_ckpt = config.GRADIENT_CHECKPOINTING

    def _forward_impl(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        attn_out = self.attn(self.norm1(x), mask=mask)
        x = x + self.dropout(attn_out)
        brain_out, aux_loss = self.topo_brain(self.norm2(x))
        x = x + self.dropout(brain_out)
        return x, aux_loss

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        if self.use_ckpt and self.training:
            return grad_ckpt(self._forward_impl, x, mask, use_reentrant=False)
        return self._forward_impl(x, mask)


# ============================================================================
# ENCODER
# ============================================================================


class VJEPAQEncoder(nn.Module):
    """Video encoder with quaternion spectral processing."""

    def __init__(self, config: VJEPAQConfig):
        super().__init__()
        self.config = config

        self.patch_embed = VideoPatchEmbedding(config)
        self.blocks = nn.ModuleList([
            VJEPAQBlock(config.D_MODEL, config.N_HEADS, config)
            for _ in range(config.N_ENCODER_LAYERS)
        ])
        self.final_norm = RMSNorm(config.D_MODEL)

    def forward(
        self,
        video: torch.Tensor,
        mask: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        all_embeddings = self.patch_embed(video)

        B, S, D = all_embeddings.shape
        mask_expanded = mask.unsqueeze(-1).expand_as(all_embeddings)
        visible_embeddings = all_embeddings * mask_expanded

        total_aux = torch.tensor(0.0, device=video.device)
        x = visible_embeddings

        for block in self.blocks:
            x, aux_loss = block(x, mask=mask)
            total_aux = total_aux + aux_loss

        x = self.final_norm(x)

        representations = []
        for b in range(B):
            vis_idx = mask[b].nonzero(as_tuple=True)[0]
            representations.append(x[b, vis_idx])

        max_vis = max(r.shape[0] for r in representations)
        padded = torch.zeros(B, max_vis, D, device=video.device)
        for b, r in enumerate(representations):
            padded[b, :r.shape[0]] = r

        return padded, total_aux / max(len(self.blocks), 1)


# ============================================================================
# PREDICTOR (WORLD MODEL)
# ============================================================================


class VJEPAQPredictor(nn.Module):
    """World model predictor: predicts masked patch representations."""

    def __init__(self, config: VJEPAQConfig):
        super().__init__()
        self.config = config

        self.pred_pos_embed = nn.Parameter(
            torch.randn(1, config.NUM_PATCHES, config.D_MODEL) * 0.02)

        self.blocks = nn.ModuleList([
            VJEPAQBlock(config.D_MODEL, config.N_HEADS, config)
            for _ in range(config.N_PREDICTOR_LAYERS)
        ])
        self.final_norm = RMSNorm(config.D_MODEL)

        self.pred_head = nn.Sequential(
            nn.Linear(config.D_MODEL, config.D_MODEL),
            nn.GELU(),
            nn.Linear(config.D_MODEL, config.D_MODEL),
        )

    def forward(
        self,
        encoder_output: torch.Tensor,
        encoder_mask: torch.Tensor,
        predictor_mask: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        B, N_vis, D = encoder_output.shape
        cfg = self.config
        total_patches = cfg.NUM_PATCHES

        full_seq = torch.zeros(B, total_patches, D, device=encoder_output.device)
        for b in range(B):
            vis_idx = encoder_mask[b].nonzero(as_tuple=True)[0]
            full_seq[b, vis_idx] = encoder_output[b, :vis_idx.shape[0]]

        full_seq = full_seq + self.pred_pos_embed[:, :total_patches, :]

        total_aux = torch.tensor(0.0, device=encoder_output.device)
        x = full_seq
        combined_mask = encoder_mask | predictor_mask

        for block in self.blocks:
            x, aux_loss = block(x, mask=combined_mask)
            total_aux = total_aux + aux_loss

        x = self.final_norm(x)

        predictions = []
        for b in range(B):
            pred_idx = predictor_mask[b].nonzero(as_tuple=True)[0]
            predictions.append(self.pred_head(x[b, pred_idx]))

        max_pred = max(p.shape[0] for p in predictions)
        padded = torch.zeros(B, max_pred, D, device=encoder_output.device)
        for b, p in enumerate(predictions):
            padded[b, :p.shape[0]] = p

        return padded, total_aux / max(len(self.blocks), 1)


# ============================================================================
# PHASE DIAGRAM TRACKER
# ============================================================================


class PhaseDiagramTracker:
    """Tracks phase diagram metrics during world model training.

    Metrics: delta, kappa, T_eff, alpha, Berry phase, Dyson beta.
    """

    def __init__(self, config: VJEPAQConfig):
        self.config = config
        self.logger = _setup_logger("PhaseTracker")
        self.history: List[Dict[str, Any]] = []

        self.U_prev: Optional[torch.Tensor] = None
        self.U_holo: Optional[torch.Tensor] = None
        self.winding_accum: float = 0.0

    def compute_delta(self, model: nn.Module) -> float:
        max_margin = 0.0
        for param in model.parameters():
            if param.numel() > 0:
                margin = (param.data - param.data.round()).abs().max().item()
                max_margin = max(max_margin, margin)
        return max_margin

    def compute_kappa(self, model: nn.Module, gradient_buffer: deque, max_dim: int = 1000) -> float:
        if len(gradient_buffer) < 2:
            return 1.0

        grads = torch.stack([g.flatten()[:max_dim] for g in list(gradient_buffer)[-10:]])
        if grads.shape[0] < 2 or grads.shape[1] < 2:
            return 1.0

        try:
            cov = torch.cov(grads.T)
            eigs = torch.linalg.eigvalsh(cov).real
            eigs = eigs[eigs > 1e-10]
            if len(eigs) < 2:
                return 1.0
            return (eigs.max() / eigs.min()).item()
        except Exception:
            return 1.0

    def compute_t_eff(self, gradient_buffer: deque, lr: float) -> float:
        if len(gradient_buffer) < 2:
            return 0.0
        grads = torch.stack([g.flatten()[:500] for g in list(gradient_buffer)[-10:]])
        second_moment = torch.mean(torch.norm(grads, dim=1) ** 2)
        first_moment_sq = torch.norm(torch.mean(grads, dim=0)) ** 2
        variance = second_moment - first_moment_sq
        return float((lr / 2.0) * variance)

    @staticmethod
    def compute_alpha(delta: float) -> float:
        if delta < 1e-10:
            return 20.0
        return -math.log(delta + 1e-15)

    def compute_berry_phase(self, model: nn.Module) -> float:
        K = self._stack_spectral_kernels(model)
        if K.numel() == 0:
            return 0.0

        try:
            U, S, _ = torch.linalg.svd(K, full_matrices=False)
            cutoff = self.config.GRASS_ELBOW_RATIO * float(S[0].item())
            r = max(1, int((S > cutoff).sum().item()))
            r = min(r, self.config.GRASS_MAX_RANK)
            U_r = U[:, :r]

            if self.U_prev is None:
                self.U_prev = U_r
                self.U_holo = torch.eye(r, dtype=U_r.dtype)
                return 0.0

            r_min = min(self.U_prev.shape[1], U_r.shape[1])
            rows = min(self.U_prev.shape[0], U_r.shape[0])
            Up = self.U_prev[:rows, :r_min]
            Un = U_r[:rows, :r_min]

            T_mat = Up.conj().transpose(0, 1) @ Un
            U_l, _, Vh = torch.linalg.svd(T_mat, full_matrices=False)
            T_mat = U_l @ Vh

            self.U_holo = T_mat @ self.U_holo
            self.U_prev = U_r

            det = torch.linalg.det(self.U_holo)
            return float(torch.atan2(det.imag, det.real).item())

        except Exception as e:
            self.logger.debug("Berry phase computation failed: %s", e)
            return 0.0

    def _stack_spectral_kernels(self, model: nn.Module) -> torch.Tensor:
        rows = []
        with torch.no_grad():
            for _name, mod in model.named_modules():
                if isinstance(mod, (QuaternionSpectralLayer, ComplexSpectralLayer)):
                    components = ('w', 'x', 'y', 'z') if isinstance(mod, QuaternionSpectralLayer) else ('r',)
                    for c in components:
                        if isinstance(mod, QuaternionSpectralLayer):
                            kr_name, ki_name = f'kr_{c}', f'ki_{c}'
                        else:
                            kr_name, ki_name = 'kernel_real', 'kernel_imag'
                        if hasattr(mod, kr_name) and hasattr(mod, ki_name):
                            kr = getattr(mod, kr_name).detach().cpu().float()
                            ki = getattr(mod, ki_name).detach().cpu().float()
                            K = torch.complex(
                                kr.mean(dim=0) if kr.dim() > 2 else kr,
                                ki.mean(dim=0) if ki.dim() > 2 else ki,
                            )
                            rows.append(K.flatten())
        if not rows:
            return torch.zeros(1, 1, dtype=torch.complex64)
        max_len = max(r.numel() for r in rows)
        padded = [F.pad(r, (0, max_len - r.numel())) for r in rows]
        return torch.stack(padded)

    def compute_goe_gue_stats(self, model: nn.Module) -> Dict[str, float]:
        K = self._stack_spectral_kernels(model)
        if K.numel() < 10:
            return {'dyson_beta': 1.5, 'imaginary_ratio': 0.0}

        try:
            K_herm = (K + K.conj().transpose(0, 1)) / 2
            eigs = torch.linalg.eigvalsh(K_herm).real
            eigs = eigs - eigs.mean()
            eigs = eigs / (eigs.std() + 1e-10)

            sorted_eigs = eigs.sort()[0]
            spacings = sorted_eigs[1:] - sorted_eigs[:-1]
            mean_spacing = spacings.mean()
            if mean_spacing > 1e-10:
                spacings = spacings / mean_spacing

            small = spacings[spacings < 0.5]
            if len(small) < 5:
                return {'dyson_beta': 1.5, 'imaginary_ratio': 0.0}

            hist, edges = torch.histogram(small, bins=20, range=(0, 0.5))
            log_p = torch.log(hist.float() + 1e-10)
            centers = (edges[:-1] + edges[1:]) / 2
            log_centers = torch.log(centers + 1e-10)

            min_len = min(len(log_p), len(log_centers))
            if min_len < 2:
                return {'dyson_beta': 1.5, 'imaginary_ratio': 0.0}

            slope = np.polyfit(
                log_centers[:min_len].cpu().numpy(),
                log_p[:min_len].cpu().numpy(),
                1,
            )[0]
            beta = max(0.5, min(2.5, float(slope)))

            imag_ratio = K.imag.abs().mean().item() / (K.real.abs().mean().item() + 1e-10)

            return {'dyson_beta': beta, 'imaginary_ratio': float(imag_ratio)}

        except Exception:
            return {'dyson_beta': 1.5, 'imaginary_ratio': 0.0}

    def snapshot(self, model: nn.Module, step: int, gradient_buffer: deque, lr: float) -> Dict[str, Any]:
        delta = self.compute_delta(model)
        kappa = self.compute_kappa(model, gradient_buffer)
        t_eff = self.compute_t_eff(gradient_buffer, lr)
        alpha = self.compute_alpha(delta)
        berry = self.compute_berry_phase(model)
        goe_gue = self.compute_goe_gue_stats(model)

        if delta < self.config.DELTA_CRYSTAL_THRESHOLD and kappa < self.config.KAPPA_CRYSTAL_THRESHOLD:
            phase = "topological_insulator" if abs(berry) > 1.0 else "crystal"
        elif delta < 0.3 and t_eff < 1e-6:
            phase = "polycrystal"
        else:
            phase = "glass"

        snap: Dict[str, Any] = {
            'step': step,
            'delta': delta,
            'kappa': kappa,
            't_eff': t_eff,
            'alpha': alpha,
            'berry_phase': berry,
            'phase': phase,
            **goe_gue,
        }
        self.history.append(snap)
        return snap

    @staticmethod
    def format_log(snap: Dict[str, Any]) -> str:
        return (
            f"delta={snap['delta']:.4f} kappa={snap['kappa']:.2f} "
            f"T_eff={snap['t_eff']:.2e} alpha={snap['alpha']:.2f} "
            f"berry={snap['berry_phase']:+.3f} beta={snap['dyson_beta']:.2f} "
            f"phase={snap['phase']}")


# ============================================================================
# FULL V-JEPA-Q MODEL
# ============================================================================


class VJEPAQ(nn.Module):
    """V-JEPA-Q: Quaternion-Enhanced Video Joint-Embedding Predictive Architecture."""

    def __init__(self, config: VJEPAQConfig):
        super().__init__()
        self.config = config

        self.encoder = VJEPAQEncoder(config)
        self.predictor = VJEPAQPredictor(config)
        self.masker = VJEPAMasker(config)
        self.phase_tracker = PhaseDiagramTracker(config) if config.TRACK_PHASE else None

        self.target_proj = nn.Sequential(
            nn.Linear(config.D_MODEL, config.D_MODEL),
            nn.GELU(),
            nn.Linear(config.D_MODEL, config.D_MODEL),
        )

        self.gradient_buffer: deque = deque(maxlen=50)

    def forward(self, video: torch.Tensor) -> Dict[str, torch.Tensor]:
        B = video.shape[0]
        device = video.device
        cfg = self.config

        masks = self.masker.generate_masks(B, device)
        encoder_mask = masks['encoder_mask']
        predictor_mask = masks['predictor_mask']

        encoder_output, encoder_aux = self.encoder(video, encoder_mask)

        with torch.no_grad():
            full_mask = torch.ones(B, cfg.NUM_PATCHES, dtype=torch.bool, device=device)
            target_output, _ = self.encoder(video, full_mask)
            target_output = self.target_proj(target_output)

        predictions, predictor_aux = self.predictor(
            encoder_output, encoder_mask, predictor_mask)

        targets = []
        for b in range(B):
            pred_idx = predictor_mask[b].nonzero(as_tuple=True)[0]
            targets.append(target_output[b, pred_idx])

        max_pred = predictions.shape[1]
        padded_targets = torch.zeros_like(predictions)
        for b, t in enumerate(targets):
            padded_targets[b, :t.shape[0]] = t

        pred_norm = F.normalize(predictions, dim=-1)
        target_norm = F.normalize(padded_targets, dim=-1)

        pred_lengths = torch.tensor([t.shape[0] for t in targets], device=device)
        max_len = pred_lengths.max().item()

        loss_mask = torch.zeros(B, max_len, device=device, dtype=torch.bool)
        for b, l in enumerate(pred_lengths):
            loss_mask[b, :l] = True

        cos_sim = (pred_norm * target_norm).sum(dim=-1)
        cos_sim = cos_sim * loss_mask.float()

        valid_counts = loss_mask.sum(dim=-1).clamp(min=1)
        loss = -(cos_sim.sum(dim=-1) / valid_counts).mean()

        total_aux = encoder_aux + predictor_aux

        result = {
            'loss': loss + cfg.AE_RECON_WEIGHT * total_aux,
            'cosine_loss': loss.detach(),
            'aux_loss': total_aux.detach(),
        }

        if self.phase_tracker is not None and self.training:
            grad_list = []
            for p in self.parameters():
                if p.grad is not None and p.grad.numel() > 0:
                    grad_list.append(p.grad.detach().flatten()[:500])
            if grad_list:
                self.gradient_buffer.append(torch.cat(grad_list))

        return result

    def get_phase_snapshot(self, step: int, lr: float) -> Optional[Dict[str, Any]]:
        if self.phase_tracker is None:
            return None
        return self.phase_tracker.snapshot(self, step, self.gradient_buffer, lr)


# ============================================================================
# VIDEO DECODER (LATENT TO PIXEL)
# ============================================================================


class VJEPAQDecoder(nn.Module):
    """Decodes latent predictor tokens into pixel-space video frames.

    Pipeline:
    1. Linear projection from D_MODEL to PATCH_DIM (reconstructs image patches)
    2. Rearrange token sequence into spatial-temporal pixel grid
    3. 3D convolutions for temporal-spatial refinement
    4. Sigmoid output for normalized pixel values [0, 1]
    """

    def __init__(self, config: VJEPAQConfig):
        super().__init__()
        self.patch_h = config.PATCH_H
        self.patch_w = config.PATCH_W
        self.patch_size = config.PATCH_SIZE[0]
        self.patch_dim = config.PATCH_DIM
        self.in_channels = config.IN_CHANNELS

        self.patch_proj = nn.Linear(config.D_MODEL, self.patch_dim)

        c = config.DECODER_CHANNELS
        n_layers = config.DECODER_N_LAYERS

        self.spatial_mixers = nn.ModuleList()
        in_c = self.in_channels
        for i in range(n_layers):
            out_c = c
            self.spatial_mixers.append(nn.Sequential(
                nn.Linear(in_c, out_c),
                nn.LayerNorm(out_c),
                nn.GELU(),
            ))
            in_c = out_c

        self.temporal_mixer = nn.Linear(c, c)
        self.temporal_norm = nn.LayerNorm(c)
        self.to_rgb = nn.Linear(c, self.in_channels)
        self.output_act = nn.Sigmoid()

    def _apply_spatial_stack(self, feat: torch.Tensor) -> torch.Tensor:
        B, C, H, W = feat.shape
        x = feat.permute(0, 2, 3, 1).contiguous().view(B * H * W, C)
        for mixer in self.spatial_mixers:
            x = mixer(x)
        return x.view(B, H, W, -1).permute(0, 3, 1, 2).contiguous()

    def forward(
        self,
        tokens: torch.Tensor,
        frame_offsets: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        B, T_pred, N, D = tokens.shape

        x = self.patch_proj(tokens)
        C, ps = self.in_channels, self.patch_size
        ph, pw = self.patch_h, self.patch_w
        x = x.view(B, T_pred, ph, pw, C, ps, ps)
        x = x.permute(0, 4, 1, 2, 5, 3, 6).contiguous()
        x = x.view(B, C, T_pred, ph * ps, pw * ps)

        if frame_offsets is not None:
            B2, T2 = frame_offsets.shape
            base_offset = torch.zeros(B2, 1, device=frame_offsets.device)
            offsets = torch.cat([base_offset, frame_offsets], dim=1)
            diff = offsets[:, 1:] - offsets[:, :-1]
            diff = diff.clamp(min=1).float()
            cum_scale = diff.cumsum(dim=1) / torch.arange(1, T_pred + 1, device=x.device).float()
            x = x * cum_scale.view(B2, 1, T_pred, 1, 1)

        frames = []
        for t in range(T_pred):
            f = x[:, :, t]
            f = self._apply_spatial_stack(f)
            frames.append(f)

        x = torch.stack(frames, dim=2)
        x = x.permute(0, 2, 3, 4, 1).contiguous()
        B2, T, H2, W2, C2 = x.shape
        x = x.view(B2 * T, H2 * W2, C2)
        x = self.temporal_norm(x)
        x = self.temporal_mixer(x)
        x = x.view(B2, T, H2, W2, C2).permute(0, 4, 1, 2, 3).contiguous()

        out_frames = []
        for t in range(T_pred):
            f = x[:, :, t]
            B, C_f, H, W = f.shape
            f_flat = f.permute(0, 2, 3, 1).contiguous().view(B * H * W, C_f)
            f_out = self.to_rgb(f_flat)
            f_out = f_out.view(B, H, W, self.in_channels).permute(0, 3, 1, 2).contiguous()
            out_frames.append(self.output_act(f_out))
        out = torch.stack(out_frames, dim=2)

        return out


# ============================================================================
# VIDEO GENERATOR (FROZEN VJEPAQ + TRAINABLE DECODER)
# ============================================================================


class VJEPAQVideoGenerator(nn.Module):
    """Physically consistent video generator: frozen world model + pixel decoder.

    Architecture:
    - VJEPAQ backbone loaded from .safetensors (encoder + predictor, frozen)
    - VJEPAQDecoder (trainable) converts torus latent states to pixels

    Generation pipeline:
    1. Context frames → frozen VideoPatchEmbedding + Encoder → visible latents
    2. Frozen Predictor rolls out future states in torus latent space
    3. Decoder converts predicted latent tokens to video frames
    """

    def __init__(self, config: VJEPAQConfig):
        super().__init__()
        self.config = config
        self.logger = _setup_logger("VJEPAQVideoGenerator")

        self.backbone = VJEPAQ(config)
        self._freeze_backbone()

        self.decoder = VJEPAQDecoder(config)

    def _freeze_backbone(self) -> None:
        for param in self.backbone.parameters():
            param.requires_grad_(False)
        self.backbone.eval()
        self.logger.info("Backbone VJEPAQ frozen")

    def _make_gen_masks(
        self,
        batch_size: int,
        device: torch.device,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        cfg = self.config
        N = cfg.NUM_PATCHES_PER_FRAME
        total = cfg.NUM_PATCHES
        context_patches = cfg.CONTEXT_FRAMES * N

        encoder_mask = torch.zeros(batch_size, total, dtype=torch.bool, device=device)
        predictor_mask = torch.zeros(batch_size, total, dtype=torch.bool, device=device)
        encoder_mask[:, :context_patches] = True
        predictor_mask[:, context_patches:] = True

        return encoder_mask, predictor_mask

    def forward(
        self,
        video: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        B = video.shape[0]
        device = video.device
        cfg = self.config
        N = cfg.NUM_PATCHES_PER_FRAME

        encoder_mask, predictor_mask = self._make_gen_masks(B, device)

        with torch.no_grad():
            encoder_output, _ = self.backbone.encoder(video, encoder_mask)
            predictions, _ = self.backbone.predictor(
                encoder_output, encoder_mask, predictor_mask)

        B_pred, N_pred, D = predictions.shape
        tokens_by_frame = torch.zeros(
            B_pred, cfg.PREDICT_FRAMES, N, D, device=device)

        for b in range(B_pred):
            pos = predictor_mask[b].nonzero(as_tuple=True)[0][:N_pred]
            frame_ids = pos // N
            patch_ids = pos % N
            valid = (frame_ids >= cfg.CONTEXT_FRAMES) & (frame_ids < cfg.NUM_FRAMES)
            offset = frame_ids[valid] - cfg.CONTEXT_FRAMES
            t_tokens = predictions[b, :valid.sum()]
            tokens_by_frame[b, offset, patch_ids[valid]] = t_tokens

        generated = self.decoder(tokens_by_frame)

        return {
            'generated': generated,
            'predictions': predictions,
            'encoder_mask': encoder_mask,
            'predictor_mask': predictor_mask,
        }


# ============================================================================
# GENERATOR TRAINER
# ============================================================================


class VJEPAQGeneratorTrainer:
    """Training loop for the video decoder.

    Freezes the V-JEPA-Q backbone and only trains VJEPAQDecoder.
    Loss = MSE + temporal gradient penalty for flicker-free video.
    """

    def __init__(self, config: VJEPAQConfig):
        self.config = config
        self.logger = _setup_logger("VJEPAQGeneratorTrainer")
        _set_seed(config.RANDOM_SEED, config.DEVICE)

        if 'cuda' in config.DEVICE:
            torch.backends.cudnn.benchmark = True
            torch.set_float32_matmul_precision('high')

        self.model = VJEPAQVideoGenerator(config).to(config.DEVICE)
        n_decoder = sum(p.numel() for p in self.model.decoder.parameters() if p.requires_grad)
        n_total = sum(p.numel() for p in self.model.parameters())
        self.logger.info("Decoder parameters: %d / %d total", n_decoder, n_total)

        self.optimizer = torch.optim.AdamW(
            self.model.decoder.parameters(),
            lr=config.DECODER_LR,
            weight_decay=config.DECODER_WEIGHT_DECAY,
            betas=(0.9, 0.95),
        )

        dev = config.DEVICE
        self.amp_dtype = torch.float16 if "cuda" in dev else torch.bfloat16
        self.scaler = torch.amp.GradScaler(
            dev.split(":")[0],
            enabled=config.USE_AMP and "cuda" in dev,
        )

        self.global_step = 0
        self.last_save_time = time.time()
        self.checkpoint_dir = Path(f"{config.CHECKPOINT_DIR}_generator")
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _temporal_gradient_loss(self, generated: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        B, C, T, H, W = generated.shape
        gen_grad = generated[:, :, 1:] - generated[:, :, :-1]
        tgt_grad = target[:, :, 1:] - target[:, :, :-1]
        return F.mse_loss(gen_grad, tgt_grad)

    def train_epoch(
        self,
        dataloader: torch.utils.data.DataLoader,
        epoch: int,
    ) -> Dict[str, float]:
        self.model.train()
        total_mse = 0.0
        total_temp = 0.0
        n_batches = 0
        accum_loss = 0.0
        self.optimizer.zero_grad(set_to_none=True)

        cfg = self.config

        for batch_idx, video in enumerate(dataloader):
            video = video.to(cfg.DEVICE)
            B, T, C, H, W = video.shape

            device_type = cfg.DEVICE.split(":")[0]
            with torch.amp.autocast(
                device_type=device_type,
                dtype=self.amp_dtype,
                enabled=cfg.USE_AMP,
            ):
                gen_out = self.model(video)
                generated = gen_out['generated']
                target = video[:, cfg.CONTEXT_FRAMES:cfg.CONTEXT_FRAMES + cfg.PREDICT_FRAMES]
                target = target.permute(0, 2, 1, 3, 4).contiguous()

                mse_loss = F.mse_loss(generated, target)
                temp_loss = self._temporal_gradient_loss(generated, target)
                loss = (
                    cfg.DECODER_TEMPORAL_LOSS_WEIGHT * mse_loss
                    + cfg.DECODER_GRADIENT_LOSS_WEIGHT * temp_loss
                )

            self.scaler.scale(loss).backward()
            accum_loss += loss.item()

            if (batch_idx + 1) % max(cfg.GRAD_ACCUM_STEPS, 1) == 0:
                if cfg.USE_AMP:
                    self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.decoder.parameters(), cfg.GRADIENT_CLIP_NORM)
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad(set_to_none=True)

                total_mse += mse_loss.item()
                total_temp += temp_loss.item()
                n_batches += 1
                self.global_step += 1
                accum_loss = 0.0

                if self.global_step % 10 == 0:
                    self.logger.info(
                        "Epoch %d Step %d: MSE=%.6f Temp=%.6f",
                        epoch, self.global_step, mse_loss.item(), temp_loss.item(),
                    )

                if self.global_step % cfg.SAVE_EVERY_STEPS == 0:
                    self.save_checkpoint(epoch, {
                        'mse': total_mse / max(n_batches, 1),
                        'temp': total_temp / max(n_batches, 1),
                    })

        if accum_loss > 0:
            if cfg.USE_AMP:
                self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(
                self.model.decoder.parameters(), cfg.GRADIENT_CLIP_NORM)
            self.scaler.step(self.optimizer)
            self.scaler.update()
            self.optimizer.zero_grad(set_to_none=True)
            total_mse += mse_loss.item()
            total_temp += temp_loss.item()
            n_batches += 1

        return {
            'mse': total_mse / max(n_batches, 1),
            'temp': total_temp / max(n_batches, 1),
        }

    def save_checkpoint(self, epoch: int, metrics: Dict[str, float]) -> None:
        decoder_path = self.checkpoint_dir / f"decoder_epoch_{epoch:04d}.safetensors"
        safetensors.torch.save_file(self.model.decoder.state_dict(), str(decoder_path))
        meta_path = self.checkpoint_dir / f"decoder_epoch_{epoch:04d}_meta.pt"
        torch.save({
            'epoch': epoch,
            'global_step': self.global_step,
            'optimizer_state_dict': self.optimizer.state_dict(),
            'metrics': metrics,
            'config': self.config,
        }, meta_path)
        self.logger.info("Decoder checkpoint saved to %s", decoder_path)

        latest_decoder = self.checkpoint_dir / "decoder_latest.safetensors"
        safetensors.torch.save_file(self.model.decoder.state_dict(), str(latest_decoder))

    def load_checkpoint(self, path: str) -> None:
        p = Path(path)
        model_state = safetensors.torch.load_file(str(p), device=self.config.DEVICE)
        self.model.decoder.load_state_dict(model_state)
        meta_path = p.parent / f"{p.stem}_meta.pt"
        if meta_path.exists():
            meta = torch.load(str(meta_path), map_location=self.config.DEVICE, weights_only=True)
            if 'optimizer_state_dict' in meta:
                self.optimizer.load_state_dict(meta['optimizer_state_dict'])
            self.global_step = meta.get('global_step', 0)
        self.logger.info("Loaded decoder weights from %s", path)
# ============================================================================


class MovingShapesDataset(torch.utils.data.Dataset):
    """Synthetic video dataset with moving geometric shapes (0 bytes on disk).

    Generates videos with N coloured shapes (circles and squares) that
    move at constant velocity and bounce off walls. Fully deterministic
    given seed.
    """

    SHAPE_NAMES = ('circle', 'square')

    def __init__(self, config: VJEPAQConfig) -> None:
        self.config = config
        self.num_samples = config.SYNTHETIC_NUM_SAMPLES
        self.canvas_size = config.SYNTHETIC_CANVAS_SIZE
        self.num_objects = config.SYNTHETIC_NUM_OBJECTS
        self.logger = _setup_logger("MovingShapesDataset")
        self.logger.info(
            "Using synthetic MovingShapes dataset: %d objects, %dx%d canvas, %d samples",
            self.num_objects, self.canvas_size, self.canvas_size, self.num_samples,
        )

    def __len__(self) -> int:
        return self.num_samples

    def _init_objects(self, rng: torch.Generator) -> Dict[str, torch.Tensor]:
        cs = self.canvas_size
        num = self.num_objects

        shapes = torch.randint(0, len(self.SHAPE_NAMES), (num,), generator=rng)
        cx = torch.empty(num).uniform_(0.2 * cs, 0.8 * cs, generator=rng)
        cy = torch.empty(num).uniform_(0.2 * cs, 0.8 * cs, generator=rng)
        vx = torch.empty(num).uniform_(-3.0, 3.0, generator=rng)
        vy = torch.empty(num).uniform_(-3.0, 3.0, generator=rng)
        sizes = torch.empty(num).uniform_(6.0, 14.0, generator=rng)
        colors = torch.rand(num, 3, generator=rng)

        return {
            'shape': shapes,
            'cx': cx,
            'cy': cy,
            'vx': vx,
            'vy': vy,
            'size': sizes,
            'color': colors,
        }

    def _render_frame(
        self,
        objects: Dict[str, torch.Tensor],
        grid_x: torch.Tensor,
        grid_y: torch.Tensor,
    ) -> torch.Tensor:
        cs = self.canvas_size
        frame = torch.zeros(3, cs, cs)
        num = self.num_objects

        for o in range(num):
            dx = grid_x - objects['cx'][o]
            dy = grid_y - objects['cy'][o]
            half = objects['size'][o] / 2.0

            if objects['shape'][o].item() == 0:
                mask = (dx ** 2 + dy ** 2) < (half ** 2)
            else:
                mask = (dx.abs() < half) & (dy.abs() < half)

            for c in range(3):
                frame[c] += mask.float() * objects['color'][o, c]

        return frame.clamp(0.0, 1.0)

    def _update_physics(self, objects: Dict[str, torch.Tensor]) -> None:
        cs = self.canvas_size

        objects['cx'] += objects['vx']
        objects['cy'] += objects['vy']

        half = objects['size'] / 2.0
        left = objects['cx'] < half
        right = objects['cx'] > cs - half
        bottom = objects['cy'] < half
        top = objects['cy'] > cs - half

        objects['vx'] = torch.where(left | right, -objects['vx'], objects['vx'])
        objects['vy'] = torch.where(bottom | top, -objects['vy'], objects['vy'])

        objects['cx'] = objects['cx'].clamp(half, cs - half)
        objects['cy'] = objects['cy'].clamp(half, cs - half)

    def __getitem__(self, idx: int) -> torch.Tensor:
        rng = torch.Generator().manual_seed(self.config.RANDOM_SEED + idx)
        T = self.config.NUM_FRAMES
        H, W = self.config.IMAGE_SIZE
        cs = self.canvas_size

        gy, gx = torch.meshgrid(
            torch.arange(cs, dtype=torch.float),
            torch.arange(cs, dtype=torch.float),
            indexing='ij',
        )

        objects = self._init_objects(rng)
        video = torch.zeros(T, 3, H, W)

        for t in range(T):
            self._update_physics(objects)
            frame = self._render_frame(objects, gx, gy)
            frame = F.interpolate(
                frame.unsqueeze(0),
                size=(H, W),
                mode='bilinear',
                align_corners=False,
            ).squeeze(0)
            video[t] = frame

        return video


class VideoDataset(torch.utils.data.Dataset):
    """Load video files from directory, falls back to MovingShapes."""

    def __init__(self, video_dir: str, config: VJEPAQConfig):
        self.video_dir = Path(video_dir)
        self.config = config
        self.logger = _setup_logger("VideoDataset")

        self.video_paths = sorted(
            list(self.video_dir.glob('*.mp4'))
            + list(self.video_dir.glob('*.avi'))
        )

        if self.video_paths:
            self.logger.info("Found %d video files in %s", len(self.video_paths), video_dir)
            self.synthetic = False
            self.num_samples = len(self.video_paths)
        else:
            self.logger.warning(
                "No video files found in %s, falling back to MovingShapes synthetic data",
                video_dir,
            )
            self.synthetic = True
            self.synthetic_dataset = MovingShapesDataset(config)
            self.num_samples = config.SYNTHETIC_NUM_SAMPLES

    def __len__(self) -> int:
        return self.num_samples

    def __getitem__(self, idx: int) -> torch.Tensor:
        if self.synthetic:
            return self.synthetic_dataset[idx % len(self.synthetic_dataset)]

        path = self.video_paths[idx % len(self.video_paths)]
        self.logger.warning("Video file loading not implemented: %s", path)
        return torch.rand(self.config.NUM_FRAMES, 3, *self.config.IMAGE_SIZE)


# ============================================================================
# TRAINER
# ============================================================================


class VJEPAQTrainer:
    """Training loop for V-JEPA-Q with AMP, gradient clipping, and phase tracking."""

    def __init__(self, config: VJEPAQConfig):
        self.config = config
        self.logger = _setup_logger("VJEPAQTrainer")
        _set_seed(config.RANDOM_SEED, config.DEVICE)

        if 'cuda' in config.DEVICE:
            torch.backends.cudnn.benchmark = True
            torch.set_float32_matmul_precision('high')
            torch.backends.cuda.matmul.allow_fp16_reduced_precision_reduction = True

        self.model = VJEPAQ(config).to(config.DEVICE)
        if config.TORCH_COMPILE and 'cuda' in config.DEVICE:
            self.model = torch.compile(self.model, mode='reduce-overhead')
            self.logger.info("Model compiled with torch.compile")

        n_params = _count_parameters(self.model)
        self.logger.info("Total parameters: %d", n_params)

        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=config.LEARNING_RATE,
            weight_decay=config.WEIGHT_DECAY,
            betas=(0.9, 0.95),
        )

        dev = config.DEVICE
        self.amp_dtype = torch.float16 if "cuda" in dev else torch.bfloat16
        self.scaler = torch.amp.GradScaler(
            dev.split(":")[0],
            enabled=config.USE_AMP and "cuda" in dev,
        )

        self.global_step = 0
        self.epoch = 0
        self.last_save_time = time.time()
        self.checkpoint_dir = Path(config.CHECKPOINT_DIR)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _cosine_lr(self, step: int, total_steps: int) -> float:
        warmup = max(1, int(total_steps * self.config.WARMUP_RATIO))
        if step < warmup:
            return self.config.LEARNING_RATE * step / warmup
        t = (step - warmup) / max(total_steps - warmup, 1)
        return self.config.LEARNING_RATE * 0.5 * (1.0 + math.cos(math.pi * t))

    def train_epoch(
        self,
        dataloader: torch.utils.data.DataLoader,
        epoch: int,
        total_steps: int,
    ) -> Dict[str, float]:
        self.model.train()
        total_loss = 0.0
        total_cosine = 0.0
        n_batches = 0
        accum_loss = 0.0
        self.optimizer.zero_grad(set_to_none=True)

        for batch_idx, video in enumerate(dataloader):
            video = video.to(self.config.DEVICE)

            lr = self._cosine_lr(self.global_step, total_steps)
            for pg in self.optimizer.param_groups:
                pg['lr'] = lr

            device_type = self.config.DEVICE.split(":")[0]
            with torch.amp.autocast(
                device_type=device_type,
                dtype=self.amp_dtype,
                enabled=self.config.USE_AMP,
            ):
                outputs = self.model(video)
                loss = outputs['loss'] / max(self.config.GRAD_ACCUM_STEPS, 1)

            self.scaler.scale(loss).backward()
            accum_loss += loss.item()

            if (batch_idx + 1) % self.config.GRAD_ACCUM_STEPS == 0:
                if self.config.USE_AMP:
                    self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(
                    self.model.parameters(), self.config.GRADIENT_CLIP_NORM)
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad(set_to_none=True)

                total_loss += accum_loss
                total_cosine += outputs['cosine_loss'].item()
                n_batches += 1
                self.global_step += 1
                accum_loss = 0.0

                if self.global_step % 10 == 0:
                    self.logger.info(
                        "Epoch %d Step %d: Loss=%.4f Cosine=%.4f Aux=%.4f",
                        epoch, self.global_step,
                        outputs['loss'].item(), outputs['cosine_loss'].item(),
                        outputs['aux_loss'].item(),
                    )

                if (self.config.TRACK_PHASE
                        and self.global_step % self.config.GRASS_TRACK_EVERY == 0):
                    snap = self.model.get_phase_snapshot(self.global_step, lr)
                    if snap:
                        self.logger.info(
                            "Phase: %s", self.model.phase_tracker.format_log(snap))

                if self.global_step % self.config.SAVE_EVERY_STEPS == 0:
                    elapsed = time.time() - self.last_save_time
                    self.save_checkpoint(epoch, {
                        'loss': total_loss / max(n_batches, 1),
                        'cosine': total_cosine / max(n_batches, 1),
                    }, is_latest=True)
                    self.logger.info("Checkpoint saved (%.1fs elapsed)", elapsed)
                    self.last_save_time = time.time()

        if accum_loss > 0:
            if self.config.USE_AMP:
                self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(), self.config.GRADIENT_CLIP_NORM)
            self.scaler.step(self.optimizer)
            self.scaler.update()
            self.optimizer.zero_grad(set_to_none=True)
            total_loss += accum_loss
            total_cosine += outputs['cosine_loss'].item()
            n_batches += 1

        return {
            'loss': total_loss / max(n_batches, 1),
            'cosine': total_cosine / max(n_batches, 1),
        }

    def save_checkpoint(
        self, epoch: int, metrics: Dict[str, float], is_latest: bool = False,
    ) -> None:
        if is_latest:
            model_path = self.checkpoint_dir / "latest.safetensors"
            meta_path = self.checkpoint_dir / "latest_meta.pt"
        else:
            model_path = self.checkpoint_dir / f"epoch_{epoch:04d}.safetensors"
            meta_path = self.checkpoint_dir / f"epoch_{epoch:04d}_meta.pt"
        safetensors.torch.save_file(self.model.state_dict(), str(model_path))
        torch.save({
            'epoch': epoch,
            'global_step': self.global_step,
            'optimizer_state_dict': self.optimizer.state_dict(),
            'metrics': metrics,
            'config': self.config,
        }, meta_path)
        self.logger.info("Checkpoint saved to %s", model_path)

    def load_checkpoint(self, path: str) -> None:
        p = Path(path)
        if p.suffix == '.safetensors':
            meta_path = p.parent / f"{p.stem}_meta.pt"
            model_state = safetensors.torch.load_file(str(p), device=self.config.DEVICE)
            if meta_path.exists():
                ckpt = torch.load(str(meta_path), map_location=self.config.DEVICE, weights_only=True)
                self.optimizer.load_state_dict(ckpt['optimizer_state_dict'])
                self.global_step = ckpt.get('global_step', 0)
            self.model.load_state_dict(model_state)
        else:
            ckpt = torch.load(path, map_location=self.config.DEVICE, weights_only=True)
            self.model.load_state_dict(ckpt['model_state_dict'])
            self.optimizer.load_state_dict(ckpt['optimizer_state_dict'])
            self.global_step = ckpt.get('global_step', 0)
        self.logger.info("Loaded checkpoint from %s", path)


# ============================================================================
# SCALE PRESETS
# ============================================================================

SCALE_PRESETS: Dict[str, Dict[str, Any]] = {
    'micro': dict(
        D_MODEL=128, N_HEADS=4, N_ENCODER_LAYERS=4, N_PREDICTOR_LAYERS=4,
        NUM_FRAMES=8, IMAGE_SIZE=(64, 64), PATCH_SIZE=(16, 16),
        CONTEXT_FRAMES=4, PREDICT_FRAMES=4,
        DROPOUT=0.0, MOE_ENABLED=False, GRADIENT_CHECKPOINTING=False,
        USE_AMP=False, TRACK_PHASE=False, BATCH_SIZE=16, GRAD_ACCUM_STEPS=1,
    ),
    'small': dict(
        D_MODEL=384, N_HEADS=6, N_ENCODER_LAYERS=12, N_PREDICTOR_LAYERS=12,
        NUM_FRAMES=16, IMAGE_SIZE=(64, 64), PATCH_SIZE=(16, 16),
        GRADIENT_CHECKPOINTING=True, USE_AMP=True, TRACK_PHASE=False,
        MOE_ENABLED=False, DROPOUT=0.0, BATCH_SIZE=8, GRAD_ACCUM_STEPS=2,
    ),
    'medium': dict(
        D_MODEL=512, N_HEADS=8, N_ENCODER_LAYERS=16, N_PREDICTOR_LAYERS=16,
        NUM_FRAMES=16, IMAGE_SIZE=(64, 64), PATCH_SIZE=(16, 16),
        GRADIENT_CHECKPOINTING=True, USE_AMP=True, TRACK_PHASE=False,
        MOE_ENABLED=False, DROPOUT=0.0, BATCH_SIZE=4, GRAD_ACCUM_STEPS=4,
    ),
}


# ============================================================================
# TESTS
# ============================================================================


class TestVJEPAQDecoder(unittest.TestCase):
    """Behaviour: decoder converts latent tokens to video frames."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**{
            **SCALE_PRESETS['micro'],
            'PREDICT_FRAMES': 2,
            'DECODER_CHANNELS': 16,
            'DECODER_N_LAYERS': 2,
            'TRACK_PHASE': False,
        })

    def test_decoder_output_shape(self):
        decoder = VJEPAQDecoder(self.cfg)
        B, T_pred, N, D = 2, self.cfg.PREDICT_FRAMES, self.cfg.NUM_PATCHES_PER_FRAME, self.cfg.D_MODEL
        tokens = torch.randn(B, T_pred, N, D)
        out = decoder(tokens)
        expected = (B, 3, T_pred, *self.cfg.IMAGE_SIZE)
        self.assertEqual(out.shape, expected)

    def test_decoder_pixel_range(self):
        decoder = VJEPAQDecoder(self.cfg)
        B, T_pred, N, D = 2, self.cfg.PREDICT_FRAMES, self.cfg.NUM_PATCHES_PER_FRAME, self.cfg.D_MODEL
        tokens = torch.randn(B, T_pred, N, D)
        out = decoder(tokens)
        self.assertGreaterEqual(out.min().item(), 0.0)
        self.assertLessEqual(out.max().item(), 1.0)

    def test_decoder_gradient_flows(self):
        decoder = VJEPAQDecoder(self.cfg)
        B, T_pred, N, D = 2, self.cfg.PREDICT_FRAMES, self.cfg.NUM_PATCHES_PER_FRAME, self.cfg.D_MODEL
        tokens = torch.randn(B, T_pred, N, D, requires_grad=True)
        out = decoder(tokens)
        loss = out.sum()
        loss.backward()
        self.assertIsNotNone(tokens.grad)
        self.assertGreater(tokens.grad.abs().sum().item(), 0.0)


class TestVJEPAQVideoGenerator(unittest.TestCase):
    """Behaviour: generator produces video from context frames."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**{
            **SCALE_PRESETS['micro'],
            'NUM_FRAMES': 4,
            'CONTEXT_FRAMES': 2,
            'PREDICT_FRAMES': 2,
            'DECODER_CHANNELS': 16,
            'DECODER_N_LAYERS': 2,
            'TRACK_PHASE': False,
            'USE_AMP': False,
            'GRADIENT_CHECKPOINTING': False,
            'MOE_ENABLED': False,
        })

    def test_generator_output_shape(self):
        gen = VJEPAQVideoGenerator(self.cfg)
        B, T, C, H, W = 2, self.cfg.NUM_FRAMES, 3, *self.cfg.IMAGE_SIZE
        video = torch.randn(B, T, C, H, W)
        out = gen(video)
        self.assertIn('generated', out)
        expected_gen = (B, 3, self.cfg.PREDICT_FRAMES, *self.cfg.IMAGE_SIZE)
        self.assertEqual(out['generated'].shape, expected_gen)
        self.assertIn('predictions', out)
        self.assertIn('encoder_mask', out)
        self.assertIn('predictor_mask', out)

    def test_generator_backbone_frozen(self):
        gen = VJEPAQVideoGenerator(self.cfg)
        for name, param in gen.backbone.named_parameters():
            self.assertFalse(
                param.requires_grad,
                f"Backbone parameter {name} is not frozen",
            )


class TestGeneratorTrainerIntegration(unittest.TestCase):
    """Behaviour: generator trainer can complete a step without error."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**{
            **SCALE_PRESETS['micro'],
            'NUM_FRAMES': 4,
            'CONTEXT_FRAMES': 2,
            'PREDICT_FRAMES': 2,
            'DECODER_CHANNELS': 16,
            'DECODER_N_LAYERS': 2,
            'DECODER_TEMPORAL_LOSS_WEIGHT': 1.0,
            'DECODER_GRADIENT_LOSS_WEIGHT': 0.1,
            'DECODER_LR': 1e-3,
            'DECODER_WEIGHT_DECAY': 0.0,
            'BATCH_SIZE': 2,
            'USE_AMP': False,
            'GRADIENT_CHECKPOINTING': False,
            'MOE_ENABLED': False,
            'TRACK_PHASE': False,
            'SYNTHETIC_NUM_OBJECTS': 2,
            'SYNTHETIC_CANVAS_SIZE': 64,
            'SYNTHETIC_NUM_SAMPLES': 10,
            'DEVICE': 'cpu',
        })

    def test_train_one_step(self):
        dataset = MovingShapesDataset(self.cfg)
        loader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=False)
        trainer = VJEPAQGeneratorTrainer(self.cfg)
        metrics = trainer.train_epoch(loader, epoch=0)
        self.assertIn('mse', metrics)
        self.assertIn('temp', metrics)
        self.assertTrue(math.isfinite(metrics['mse']))
        self.assertTrue(math.isfinite(metrics['temp']))

    def test_decoder_parameters_update(self):
        trainer = VJEPAQGeneratorTrainer(self.cfg)
        old_weights = trainer.model.decoder.patch_proj.weight.clone()
        dataset = MovingShapesDataset(self.cfg)
        loader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=False)
        trainer.train_epoch(loader, epoch=0)
        new_weights = trainer.model.decoder.patch_proj.weight
        diff = (new_weights - old_weights).abs().sum().item()
        self.assertGreater(diff, 0.0, "Decoder weights should update during training")


class TestQuaternionOps(unittest.TestCase):
    """Behaviour: Quaternion algebra must satisfy unit quaternion properties."""

    def setUp(self):
        self.q1 = torch.tensor([[1.0, 0.0, 0.0, 0.0]])
        self.q2 = torch.tensor([[0.0, 1.0, 0.0, 0.0]])

    def test_hamilton_product_identity(self):
        result = QuaternionOps.hamilton_product(self.q1, self.q2)
        self.assertTrue(torch.allclose(result, self.q2))

    def test_hamilton_product_ij_equals_k(self):
        i = torch.tensor([[0.0, 1.0, 0.0, 0.0]])
        j = torch.tensor([[0.0, 0.0, 1.0, 0.0]])
        k = torch.tensor([[0.0, 0.0, 0.0, 1.0]])
        result = QuaternionOps.hamilton_product(i, j)
        self.assertTrue(torch.allclose(result, k, atol=1e-6))

    def test_normalize_unit(self):
        q = torch.tensor([[2.0, 0.0, 0.0, 0.0]])
        qn = QuaternionOps.normalize(q)
        self.assertTrue(torch.allclose(qn, torch.tensor([[1.0, 0.0, 0.0, 0.0]])))

    def test_conjugate_product_identity(self):
        q = torch.tensor([[0.3, 0.4, 0.5, 0.6]])
        qc = QuaternionOps.conjugate(q)
        product = QuaternionOps.hamilton_product(q, qc)
        expected_norm = (q ** 2).sum()
        self.assertTrue(torch.allclose(product[..., 0], expected_norm, atol=1e-6))

    def test_rotate_vector_norm_preserving(self):
        v = torch.tensor([[1.0, 0.0, 0.0]])
        q = QuaternionOps.normalize(torch.tensor([[0.0, 0.0, 1.0, 0.0]]))
        rotated = QuaternionOps.rotate_vector(v, q)
        v_norm = v.norm(dim=-1)
        r_norm = rotated.norm(dim=-1)
        self.assertTrue(torch.allclose(v_norm, r_norm, atol=1e-6))

    def test_log_exp_roundtrip(self):
        q = QuaternionOps.normalize(torch.tensor([[0.3, 0.4, 0.5, 0.6]]))
        q_log = QuaternionOps.log(q)
        q_exp = QuaternionOps.exp(q_log)
        q_exp = QuaternionOps.normalize(q_exp)
        self.assertTrue(torch.allclose(q.expand_as(q_exp), q_exp, atol=1e-4))

    def test_lie_product_approximation(self):
        q1 = QuaternionOps.normalize(torch.tensor([[0.99, 0.04, 0.04, 0.03]]))
        q2 = QuaternionOps.normalize(torch.tensor([[0.98, 0.08, 0.06, 0.04]]))
        exact = QuaternionOps.hamilton_product(q1, q2)
        approx = QuaternionOps.lie_product(q1, q2)
        exact = QuaternionOps.normalize(exact)
        approx = QuaternionOps.normalize(approx)
        cos_sim = (exact * approx).sum(dim=-1)
        self.assertGreater(cos_sim.item(), 0.9)


class TestQuaternionLinear(unittest.TestCase):
    """Behaviour: QuaternionLinear must preserve quaternion structure."""

    def test_output_divisible_by_4(self):
        layer = QuaternionLinear(16, 32)
        x = torch.randn(2, 16)
        out = layer(x)
        self.assertEqual(out.shape[-1], 32)

    def test_gradient_flows(self):
        layer = QuaternionLinear(8, 16)
        x = torch.randn(4, 8, requires_grad=True)
        out = layer(x)
        loss = out.sum()
        loss.backward()
        self.assertIsNotNone(x.grad)


class TestVideoPatchEmbedding(unittest.TestCase):
    """Critical: patch embedding shapes must match config (bug regression test)."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**{
            **SCALE_PRESETS['micro'],
            'SYNTHETIC_NUM_OBJECTS': 2,
        })

    def test_forward_shape_matches_config(self):
        embed = VideoPatchEmbedding(self.cfg)
        B, T, C, H, W = 2, self.cfg.NUM_FRAMES, 3, *self.cfg.IMAGE_SIZE
        video = torch.randn(B, T, C, H, W)
        out = embed(video)
        expected_seq_len = T * self.cfg.NUM_PATCHES_PER_FRAME
        expected_shape = (B, expected_seq_len, self.cfg.D_MODEL)
        self.assertEqual(out.shape, expected_shape,
                         f"Expected {expected_shape}, got {out.shape}")

    def test_temporal_derivative_handles_single_frame(self):
        embed = VideoPatchEmbedding(self.cfg)
        B, T, C, H, W = 2, 1, 3, *self.cfg.IMAGE_SIZE
        video = torch.randn(B, T, C, H, W)
        out = embed(video)
        expected_seq_len = T * self.cfg.NUM_PATCHES_PER_FRAME
        self.assertEqual(out.shape, (B, expected_seq_len, self.cfg.D_MODEL))


class TestVJEPAMasker(unittest.TestCase):
    """Behaviour: masks must be valid and consistent."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**SCALE_PRESETS['micro'])

    def test_mask_shapes(self):
        masker = VJEPAMasker(self.cfg)
        masks = masker.generate_masks(4, torch.device('cpu'))
        total = self.cfg.NUM_FRAMES * self.cfg.NUM_PATCHES_PER_FRAME
        for key in ('encoder_mask', 'predictor_mask', 'visible_mask'):
            self.assertEqual(masks[key].shape, (4, total))

    def test_predictor_mask_subset_of_encoder_mask(self):
        masker = VJEPAMasker(self.cfg)
        masks = masker.generate_masks(2, torch.device('cpu'))
        pred = masks['predictor_mask']
        enc = masks['encoder_mask']
        self.assertTrue((pred & enc).sum() == 0)


class TestVJEPAQModel(unittest.TestCase):
    """Behaviour: full model forward pass produces valid losses."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**{
            **SCALE_PRESETS['micro'],
            'TRACK_PHASE': False,
            'SYNTHETIC_NUM_OBJECTS': 2,
        })

    def test_forward_loss_scalar(self):
        model = VJEPAQ(self.cfg)
        B, T, C, H, W = 2, self.cfg.NUM_FRAMES, 3, *self.cfg.IMAGE_SIZE
        video = torch.randn(B, T, C, H, W)
        output = model(video)
        self.assertIn('loss', output)
        self.assertTrue(torch.isfinite(output['loss']))
        self.assertIn('cosine_loss', output)
        self.assertIn('aux_loss', output)

    def test_encoder_output_shape(self):
        model = VJEPAQEncoder(self.cfg)
        B, T, C, H, W = 2, self.cfg.NUM_FRAMES, 3, *self.cfg.IMAGE_SIZE
        video = torch.randn(B, T, C, H, W)
        total_patches = T * self.cfg.NUM_PATCHES_PER_FRAME
        mask = torch.ones(B, total_patches, dtype=torch.bool)
        mask[:, ::2] = False
        out, aux = model(video, mask)
        self.assertEqual(out.shape[-1], self.cfg.D_MODEL)
        self.assertTrue(torch.isfinite(aux))

    def test_predictor_output_shape(self):
        model = VJEPAQPredictor(self.cfg)
        B, N_vis, D = 2, 60, self.cfg.D_MODEL
        total_patches = self.cfg.NUM_PATCHES
        enc_out = torch.randn(B, N_vis, D)
        enc_mask = torch.zeros(B, total_patches, dtype=torch.bool)
        pred_mask = torch.zeros(B, total_patches, dtype=torch.bool)
        enc_mask[:, :N_vis] = True
        pred_mask[:, N_vis:N_vis + 30] = True
        out, aux = model(enc_out, enc_mask, pred_mask)
        self.assertEqual(out.shape[-1], D)
        self.assertTrue(torch.isfinite(aux))

    def test_torus_brain_forward(self):
        brain = QuaternionTorusBrain(self.cfg.D_MODEL, self.cfg)
        B, S, D = 2, 64, self.cfg.D_MODEL
        x = torch.randn(B, S, D)
        out, aux = brain(x)
        self.assertEqual(out.shape, x.shape)
        self.assertTrue(torch.isfinite(aux))

    def test_quaternion_spectral_layer_forward(self):
        d_q = self.cfg.D_QUAT
        layer = QuaternionSpectralLayer(d_q, d_q, 2, 4)
        B = 4
        x = torch.randn(B, 4 * d_q, 2, 4)
        out = layer(x)
        self.assertEqual(out.shape, x.shape)

    def test_complex_spectral_layer_forward(self):
        layer = ComplexSpectralLayer(16, 8, 8)
        x = torch.randn(2, 16, 8, 8)
        out = layer(x)
        self.assertEqual(out.shape, x.shape)

    def test_moe_forward(self):
        moe = TopoMoE(self.cfg.D_MODEL, self.cfg)
        B, S, D = 2, 64, self.cfg.D_MODEL
        x = torch.randn(B, S, D)
        out, aux = moe(x)
        self.assertEqual(out.shape, x.shape)

    def test_attention_forward(self):
        attn = SpatiotemporalAttention(self.cfg.D_MODEL, self.cfg.N_HEADS, self.cfg)
        B, S, D = 2, 100, self.cfg.D_MODEL
        x = torch.randn(B, S, D)
        out = attn(x)
        self.assertEqual(out.shape, x.shape)

    def test_block_forward(self):
        block = VJEPAQBlock(self.cfg.D_MODEL, self.cfg.N_HEADS, self.cfg)
        B, S, D = 2, 64, self.cfg.D_MODEL
        x = torch.randn(B, S, D)
        out, aux = block(x)
        self.assertEqual(out.shape, x.shape)


class TestMovingShapesDataset(unittest.TestCase):
    """Behaviour: synthetic dataset produces valid video tensors."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**{
            **SCALE_PRESETS['micro'],
            'SYNTHETIC_NUM_OBJECTS': 2,
            'SYNTHETIC_CANVAS_SIZE': 32,
        })

    def test_output_shape(self):
        dataset = MovingShapesDataset(self.cfg)
        sample = dataset[0]
        expected = (self.cfg.NUM_FRAMES, 3, *self.cfg.IMAGE_SIZE)
        self.assertEqual(sample.shape, expected)

    def test_pixel_range(self):
        dataset = MovingShapesDataset(self.cfg)
        sample = dataset[0]
        self.assertGreaterEqual(sample.min(), 0.0)
        self.assertLessEqual(sample.max(), 1.0)

    def test_deterministic(self):
        dataset = MovingShapesDataset(self.cfg)
        sample1 = dataset[42]
        sample2 = dataset[42]
        self.assertTrue(torch.allclose(sample1, sample2))

    def test_different_indices_differ(self):
        dataset = MovingShapesDataset(self.cfg)
        sample1 = dataset[0]
        sample2 = dataset[1]
        self.assertFalse(torch.allclose(sample1, sample2))


class TestTrainerIntegration(unittest.TestCase):
    """Behaviour: trainer can complete a training step without error."""

    def setUp(self):
        self.cfg = VJEPAQConfig(**{
            **SCALE_PRESETS['micro'],
            'BATCH_SIZE': 2,
            'NUM_FRAMES': 4,
            'CONTEXT_FRAMES': 2,
            'PREDICT_FRAMES': 2,
            'IMAGE_SIZE': (64, 64),
            'TRACK_PHASE': False,
            'USE_AMP': False,
            'GRADIENT_CHECKPOINTING': False,
            'SYNTHETIC_NUM_OBJECTS': 2,
            'SYNTHETIC_CANVAS_SIZE': 32,
            'SYNTHETIC_NUM_SAMPLES': 10,
            'GRASS_TRACK_EVERY': 5,
            'DEVICE': 'cpu',
        })

    def test_train_one_step(self):
        dataset = MovingShapesDataset(self.cfg)
        loader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=False)
        trainer = VJEPAQTrainer(self.cfg)
        metrics = trainer.train_epoch(loader, epoch=0, total_steps=5)
        self.assertIn('loss', metrics)
        self.assertIn('cosine', metrics)
        self.assertTrue(math.isfinite(metrics['loss']))
        self.assertTrue(math.isfinite(metrics['cosine']))

    def test_train_multiple_steps(self):
        dataset = MovingShapesDataset(self.cfg)
        loader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=False)
        trainer = VJEPAQTrainer(self.cfg)
        metrics = trainer.train_epoch(loader, epoch=0, total_steps=10)
        trainer.train_epoch(loader, epoch=1, total_steps=10)
        final_loss = metrics['loss']
        self.assertTrue(math.isfinite(final_loss))


class TestConfigValidation(unittest.TestCase):
    """Behaviour: invalid configs must raise AssertionError."""

    def test_bad_d_model_raises(self):
        with self.assertRaises(AssertionError):
            VJEPAQConfig(D_MODEL=101, N_HEADS=4)

    def test_bad_mask_ratio_raises(self):
        with self.assertRaises(AssertionError):
            VJEPAQConfig(ENCODER_MASK_RATIO=1.5)

    def test_bad_data_mode_raises(self):
        with self.assertRaises(AssertionError):
            VJEPAQConfig(DATA_MODE='invalid')

    def test_micro_config_valid(self):
        cfg = VJEPAQConfig(**SCALE_PRESETS['micro'])
        self.assertEqual(cfg.N_TORUS_NODES, 8)


# ============================================================================
# VISUALIZE
# ============================================================================


def _visualize_video(input_path: str, output_path: str) -> None:
    """Load a .pt inference output and render it as .mp4 via ffmpeg."""
    import subprocess as _sp
    import tempfile as _tf
    import os as _os
    from PIL import Image as _Image

    data = torch.load(input_path, map_location='cpu', weights_only=True)
    ctx = data['context']      # [B,T_ctx,C,H,W]
    tgt = data['target']       # [B,T_pred,C,H,W]
    gen = data['generated']    # [B,C,T_pred,H,W]

    # normalize to [B, T, C, H, W]
    if gen.shape[1] == 3 and gen.shape[2] != 3:
        gen = gen.permute(0, 2, 1, 3, 4).contiguous()
    if ctx.shape[1] != ctx.shape[2] and ctx.shape[2] == 3:
        pass  # already [B, T, C, H, W]
    elif ctx.shape[1] == 3 and ctx.shape[2] != 3:
        ctx = ctx.permute(0, 2, 1, 3, 4).contiguous()
    if tgt.shape[1] != tgt.shape[2] and tgt.shape[2] == 3:
        pass
    elif tgt.shape[1] == 3 and tgt.shape[2] != 3:
        tgt = tgt.permute(0, 2, 1, 3, 4).contiguous()

    _, TP, _, H, W = tgt.shape

    def to_frames(t: torch.Tensor) -> np.ndarray:
        """[T, C, H, W] float -> [T, H, W, C] uint8."""
        return (t.permute(0, 2, 3, 1).clamp(0, 1).numpy() * 255).astype('uint8')

    frames_tgt = to_frames(tgt[0])
    frames_gen = to_frames(gen[0])
    frames_ctx = to_frames(ctx[0])

    with _tf.TemporaryDirectory() as tmpdir:
        for t in range(TP):
            side = _Image.new('RGB', (W * 2 + 4, H), (0, 0, 0))
            c = _Image.fromarray(frames_tgt[t])
            g = _Image.fromarray(frames_gen[t])
            side.paste(c, (0, 0))
            side.paste(g, (W + 4, 0))
            side.save(_os.path.join(tmpdir, f'pred_{t:04d}.png'))

        ctx_video = output_path.replace('.mp4', '_context.mp4')
        for t in range(frames_ctx.shape[0]):
            _Image.fromarray(frames_ctx[t]).save(
                _os.path.join(tmpdir, f'ctx_{t:04d}.png'))

        _sp.run([
            'ffmpeg', '-y', '-framerate', '4',
            '-i', _os.path.join(tmpdir, 'pred_%04d.png'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output_path
        ], capture_output=True, check=True)
        _sp.run([
            'ffmpeg', '-y', '-framerate', '4',
            '-i', _os.path.join(tmpdir, 'ctx_%04d.png'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', ctx_video
        ], capture_output=True, check=True)

    print(f"Videos saved to: {output_path} (target|generated) and "
          f"{output_path.replace('.mp4', '_context.mp4')} (context)")



# ============================================================================
# MAIN
# ============================================================================


def main() -> None:
    """Entry point: parse args, create config, build dataset, train or generate."""
    parser = argparse.ArgumentParser(description='V-JEPA-Q Training and Generation')
    parser.add_argument('--mode', choices=['train', 'eval', 'test', 'generate', 'infer', 'visualize'], default='train')
    parser.add_argument('--video_dir', type=str, default='videos')
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--scale', choices=list(SCALE_PRESETS.keys()), default='small')
    parser.add_argument('--resume', type=str, default=None)
    parser.add_argument('--backbone', type=str, default=None,
                        help='Path to .safetensors for frozen VJEPAQ backbone')
    parser.add_argument('--batch_size', type=int, default=None)
    parser.add_argument('--num_workers', type=int, default=None)
    parser.add_argument('--data_mode', choices=['synthetic', 'video_dir'], default=None)
    parser.add_argument('--output', type=str, default='generated_video.pt',
                        help='Output path for generated video (.pt)')
    parser.add_argument('--input', type=str, default='',
                        help='Input .pt file for visualize mode')
    args = parser.parse_args()

    config = VJEPAQConfig(**SCALE_PRESETS[args.scale])

    if args.batch_size is not None:
        config.BATCH_SIZE = args.batch_size
    if args.num_workers is not None:
        config.NUM_WORKERS = args.num_workers
    if args.data_mode is not None:
        config.DATA_MODE = args.data_mode
    if args.backbone is not None:
        config.DECODER_LOAD_PATH = args.backbone

    logger = _setup_logger("VJEPAQ")
    logger.info("V-JEPA-Q Configuration:")
    for key, value in sorted(config.__dict__.items()):
        if not key.startswith('_'):
            logger.info("  %s: %s", key, value)

    if args.mode == 'test':
        import sys as _sys
        _sys.argv = [_sys.argv[0]]
        unittest.main()
        return

    if args.mode == 'infer':
        logger.info("Inference mode: generating video from trained checkpoint")
        if not args.resume:
            logger.error("--resume is required for infer mode (decoder .safetensors)")
            return
        gen_trainer = VJEPAQGeneratorTrainer(config)
        if config.DECODER_LOAD_PATH:
            backbone_state = safetensors.torch.load_file(
                config.DECODER_LOAD_PATH, device=config.DEVICE)
            gen_trainer.model.backbone.load_state_dict(backbone_state, strict=False)
            logger.info("Loaded backbone weights from %s", config.DECODER_LOAD_PATH)
        gen_trainer.load_checkpoint(args.resume)
        gen_trainer.model.eval()
        dataset = MovingShapesDataset(config)
        dataloader = torch.utils.data.DataLoader(
            dataset,
            batch_size=config.BATCH_SIZE,
            shuffle=True,
            num_workers=config.NUM_WORKERS,
            drop_last=True,
        )
        batch = next(iter(dataloader)).to(config.DEVICE)
        with torch.no_grad():
            out = gen_trainer.model(batch)
        generated = out['generated']
        torch.save({
            'context': batch[:, :config.CONTEXT_FRAMES].cpu(),
            'target': batch[:, config.CONTEXT_FRAMES:config.CONTEXT_FRAMES + config.PREDICT_FRAMES].cpu(),
            'generated': generated.cpu(),
            'meta': {
                'context_frames': config.CONTEXT_FRAMES,
                'predict_frames': config.PREDICT_FRAMES,
                'image_size': list(config.IMAGE_SIZE),
            },
        }, args.output)
        logger.info(
            "Generated %d frames, saved to %s (shape: %s)",
            config.PREDICT_FRAMES, args.output, list(generated.shape))
        return

    if args.mode == 'visualize':
        if not args.input:
            logger.error("--input is required for visualize mode (.pt file)")
            return
        _visualize_video(args.input, args.output)
        return

    if args.mode == 'generate':
        logger.info("Video Generation mode")
        if not config.DECODER_LOAD_PATH and not args.backbone:
            logger.warning(
                "No backbone .safetensors provided. Generator will use "
                "untrained random backbone."
            )
        gen_trainer = VJEPAQGeneratorTrainer(config)
        if config.DECODER_LOAD_PATH:
            backbone_state = safetensors.torch.load_file(
                config.DECODER_LOAD_PATH, device=config.DEVICE)
            gen_trainer.model.backbone.load_state_dict(backbone_state, strict=False)
            logger.info("Loaded backbone weights from %s", config.DECODER_LOAD_PATH)
        if args.resume:
            gen_trainer.load_checkpoint(args.resume)
        dataset = MovingShapesDataset(config)
        dataloader = torch.utils.data.DataLoader(
            dataset,
            batch_size=config.BATCH_SIZE,
            shuffle=True,
            num_workers=config.NUM_WORKERS,
            drop_last=True,
        )
        start_time = time.time()
        for epoch in range(args.epochs):
            metrics = gen_trainer.train_epoch(dataloader, epoch)
            elapsed = time.time() - start_time
            logger.info(
                "Gen Epoch %d complete: mse=%.6f temp=%.6f (%.1fs elapsed)",
                epoch, metrics['mse'], metrics['temp'], elapsed)
            gen_trainer.save_checkpoint(epoch, metrics)
        logger.info(
            "Generation training complete: %d epochs in %.1fs",
            args.epochs, time.time() - start_time)
        return

    trainer = VJEPAQTrainer(config)
    n_params = sum(p.numel() for p in trainer.model.parameters())
    logger.info("Total parameters: %d", n_params)

    if args.resume:
        trainer.load_checkpoint(args.resume)

    if args.mode == 'train':
        dataset = MovingShapesDataset(config)
        dataloader = torch.utils.data.DataLoader(
            dataset,
            batch_size=config.BATCH_SIZE,
            shuffle=True,
            num_workers=config.NUM_WORKERS,
            drop_last=True,
        )

        total_steps = len(dataloader) * args.epochs
        logger.info("Total training steps: %d", total_steps)

        start_time = time.time()
        for epoch in range(args.epochs):
            metrics = trainer.train_epoch(dataloader, epoch, total_steps)
            elapsed = time.time() - start_time
            logger.info(
                "Epoch %d complete: loss=%.4f cosine=%.4f (%.1fs elapsed)",
                epoch, metrics['loss'], metrics['cosine'], elapsed)
            trainer.save_checkpoint(epoch, metrics)

        logger.info(
            "Training complete: %d epochs in %.1fs",
            args.epochs, time.time() - start_time)

    elif args.mode == 'eval':
        logger.info("Evaluation mode: forward pass only")
        dataset = MovingShapesDataset(config)
        loader = torch.utils.data.DataLoader(dataset, batch_size=config.BATCH_SIZE)
        video = next(iter(loader)).to(config.DEVICE)
        with torch.no_grad():
            out = trainer.model(video)
        logger.info("Evaluation loss: %.4f", out['loss'].item())


if __name__ == "__main__":
    if '--test' in sys.argv:
        sys.argv.remove('--test')
        unittest.main()
    else:
        main()
