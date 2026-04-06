import torch
import torch.nn.functional as F


def flow_warp(x, flow, interp_mode="bilinear", padding_mode="zeros", align_corners=True):
    n, _, h, w = x.size()
    device = x.device
    dtype = x.dtype

    grid_y_input = torch.arange(h, device=device, dtype=dtype)
    grid_x_input = torch.arange(w, device=device, dtype=dtype)
    try:
        grid_y, grid_x = torch.meshgrid(grid_y_input, grid_x_input, indexing="ij")
    except TypeError:
        grid_y, grid_x = torch.meshgrid(grid_y_input, grid_x_input)
    base_grid = torch.stack((grid_x, grid_y), dim=-1).unsqueeze(0).expand(n, -1, -1, -1)
    vgrid = base_grid + flow

    vgrid_x = 2.0 * vgrid[..., 0] / max(w - 1, 1) - 1.0
    vgrid_y = 2.0 * vgrid[..., 1] / max(h - 1, 1) - 1.0
    vgrid_scaled = torch.stack((vgrid_x, vgrid_y), dim=-1)

    return F.grid_sample(
        x,
        vgrid_scaled,
        mode=interp_mode,
        padding_mode=padding_mode,
        align_corners=align_corners,
    )
