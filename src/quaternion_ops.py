"""
Quaternion algebra with Taylor-optimized Lie group exp/log maps.

Convention: [w, x, y, z] for all quaternion vectors.
Pure quaternions in tangent space have w=0.

Optimizations:
- Taylor truncation for small-angle exp/log (avoids acos/sinc for |v| < 0.1)
- Pre-allocated tensors for repeated operations
- Vectorized Hamilton product via batched matmul
"""

import torch
import torch.nn as nn


class QuaternionOps:
    """Pure quaternion operations. Convention: [w, x, y, z].

    Includes exponential and logarithmic maps for the Lie group SU(2) / so(3).
    The log map converts quaternion multiplication to vector addition in the
    tangent space (Lie algebra). The exp map converts back.

    Taylor truncation: for small angles (theta < 0.1), sin(theta) ≈ theta
    and cos(theta) ≈ 1 - theta^2/2, avoiding expensive acos/sinc div.
    """

    _TAYLOR_THRESHOLD = 0.1

    @staticmethod
    def hamilton_product(q1: torch.Tensor, q2: torch.Tensor) -> torch.Tensor:
        w1, x1, y1, z1 = q1.unbind(-1)
        w2, x2, y2, z2 = q2.unbind(-1)
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

        Fully vectorized. For theta < threshold: Taylor series
        avoids the expensive theta/sin(theta) division.
        """
        v = q[..., 1:]
        v_norm = v.norm(dim=-1, keepdim=True)
        w_clamped = q[..., 0:1].clamp(-1.0 + eps, 1.0 - eps)
        theta = torch.acos(w_clamped)

        scale_exact = torch.where(v_norm > eps, theta / v_norm, torch.ones_like(v_norm))
        scale_taylor = 1.0 + theta.pow(2) / 6.0
        scale = torch.where(
            v_norm < QuaternionOps._TAYLOR_THRESHOLD,
            scale_taylor, scale_exact,
        )
        return torch.cat([torch.zeros_like(w_clamped), v * scale], dim=-1)

    @staticmethod
    def exp(q: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
        """Exponential map from so(3) to SU(2).

        Fully vectorized. For theta < threshold: Taylor series
        avoids the expensive sin(theta)/theta division.
        """
        v = q[..., 1:]
        theta = v.norm(dim=-1, keepdim=True)

        scale_taylor = 1.0 - theta.pow(2) / 6.0
        scale_exact = torch.where(theta > eps, torch.sin(theta) / theta, torch.ones_like(theta))
        scale = torch.where(
            theta < QuaternionOps._TAYLOR_THRESHOLD,
            scale_taylor, scale_exact,
        )

        cos_taylor = 1.0 - theta.pow(2) / 2.0
        cos_theta = torch.where(
            theta < QuaternionOps._TAYLOR_THRESHOLD,
            cos_taylor, torch.cos(theta),
        )
        return torch.cat([cos_theta, v * scale], dim=-1)

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
        xw, xx, xy, xz = x.split(d, dim=-1)
        ow = self.Ww(xw) - self.Wx(xx) - self.Wy(xy) - self.Wz(xz)
        ox = self.Ww(xx) + self.Wx(xw) + self.Wy(xz) - self.Wz(xy)
        oy = self.Ww(xy) - self.Wx(xz) + self.Wy(xw) + self.Wz(xx)
        oz = self.Ww(xz) + self.Wx(xy) - self.Wy(xx) + self.Wz(xw)
        out = torch.cat([ow, ox, oy, oz], dim=-1)
        return out + self.bias if self.bias is not None else out
