# API

## app.py

### create_model `def create_model(scale)`
- Defined: `app.py:18`
- Depends on: `model.py`

### create_dataset `def create_dataset(config)`
- Defined: `app.py:24`
- Depends on: `model.py`

### create_trainer `def create_trainer(config)`
- Defined: `app.py:28`
- Depends on: `model.py`

### create_generator `def create_generator(config)`
- Defined: `app.py:32`
- Depends on: `model.py`

### create_generator_trainer `def create_generator_trainer(config)`
- Defined: `app.py:36`
- Depends on: `model.py`

## model.py

### _setup_logger `def _setup_logger(name, level)`
- Defined: `model.py:240`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _set_seed `def _set_seed(seed, device)`
- Defined: `model.py:251`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _count_parameters `def _count_parameters(module)`
- Defined: `model.py:258`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _visualize_video `def _visualize_video(input_path, output_path)`
- Defined: `model.py:2756`
- Doc: Load a .pt inference output and render it as .mp4 via ffmpeg.
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _create_dataloader `def _create_dataloader(config)`
- Defined: `model.py:2825`
- Doc: Create dataset and DataLoader based on config.DATA_MODE.
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### main `def main()`
- Defined: `model.py:2856`
- Doc: Entry point: parse args, create config, build dataset, train or generate.
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __post_init__ `def __post_init__(self)`
- Defined: `model.py:142`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### to_dict `def to_dict(self)`
- Defined: `model.py:184`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### to_json `def to_json(self)`
- Defined: `model.py:188`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### from_json `def from_json(cls, path_or_str)`
- Defined: `model.py:196`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### auto_batch_size `def auto_batch_size(config, min_batch, max_batch)`
- Defined: `model.py:211`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, channels, grid_h, grid_w, imaginary_ratio, init_scale)`
- Defined: `model.py:275`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### set_imaginary_ratio `def set_imaginary_ratio(self, ratio)`
- Defined: `model.py:299`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### get_effective_imaginary_ratio `def get_effective_imaginary_ratio(self)`
- Defined: `model.py:306`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### get_spectral_operator `def get_spectral_operator(self)`
- Defined: `model.py:315`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x)`
- Defined: `model.py:322`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, in_q, out_q, grid_h, grid_w, init_scale)`
- Defined: `model.py:351`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _kernel `def _kernel(self, c)`
- Defined: `model.py:378`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _gauss_contract `def _gauss_contract(W, X)`
- Defined: `model.py:382`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x)`
- Defined: `model.py:390`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:427`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _temporal_filter `def _temporal_filter(self, x, kr, ki)`
- Defined: `model.py:448`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### encode_temporal `def encode_temporal(self, x)`
- Defined: `model.py:454`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### decode_temporal `def decode_temporal(self, z)`
- Defined: `model.py:458`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x)`
- Defined: `model.py:462`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:481`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _compute_temporal_derivative `def _compute_temporal_derivative(video)`
- Defined: `model.py:499`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, video)`
- Defined: `model.py:504`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:553`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _generate_block_mask `def _generate_block_mask(h, w, mask_ratio, block_size, device)`
- Defined: `model.py:558`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### generate_masks `def generate_masks(self, batch_size, device)`
- Defined: `model.py:572`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, d_head, max_seq_len, base)`
- Defined: `model.py:612`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _build_cache `def _build_cache(self, seq_len)`
- Defined: `model.py:618`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _rotate_half `def _rotate_half(self, x)`
- Defined: `model.py:625`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, q, k)`
- Defined: `model.py:629`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, d_model, eps)`
- Defined: `model.py:644`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x)`
- Defined: `model.py:649`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, d_model, n_heads, config)`
- Defined: `model.py:662`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x, mask, is_causal)`
- Defined: `model.py:678`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, d_model, config)`
- Defined: `model.py:737`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _build_torus_graph `def _build_torus_graph(self)`
- Defined: `model.py:783`
- Doc: Build fully periodic 2D torus adjacency.
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _torus_soft_assign `def _torus_soft_assign(self, phi1, phi2)`
- Defined: `model.py:812`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _message_passing `def _message_passing(self, node_feat)`
- Defined: `model.py:827`
- Doc: Message passing with Lie algebra quaternion product.
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x)`
- Defined: `model.py:859`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, d_model, config)`
- Defined: `model.py:907`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _route `def _route(self, x)`
- Defined: `model.py:927`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x)`
- Defined: `model.py:954`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, d_model, n_heads, config)`
- Defined: `model.py:980`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _forward_impl `def _forward_impl(self, x, mask)`
- Defined: `model.py:989`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, x, mask)`
- Defined: `model.py:1000`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1018`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, video, mask)`
- Defined: `model.py:1029`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1066`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, encoder_output, encoder_mask, predictor_mask)`
- Defined: `model.py:1085`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1137`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### compute_delta `def compute_delta(self, model)`
- Defined: `model.py:1146`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### compute_kappa `def compute_kappa(self, model, gradient_buffer, max_dim)`
- Defined: `model.py:1154`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### compute_t_eff `def compute_t_eff(self, gradient_buffer, lr)`
- Defined: `model.py:1172`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### compute_alpha `def compute_alpha(delta)`
- Defined: `model.py:1182`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### compute_berry_phase `def compute_berry_phase(self, model)`
- Defined: `model.py:1187`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _stack_spectral_kernels `def _stack_spectral_kernels(self, model)`
- Defined: `model.py:1223`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### compute_goe_gue_stats `def compute_goe_gue_stats(self, model)`
- Defined: `model.py:1248`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### snapshot `def snapshot(self, model, step, gradient_buffer, lr)`
- Defined: `model.py:1292`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### format_log `def format_log(snap)`
- Defined: `model.py:1321`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1337`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### from_preset `def from_preset(cls, scale)`
- Defined: `model.py:1355`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, video)`
- Defined: `model.py:1360`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### get_phase_snapshot `def get_phase_snapshot(self, step, lr)`
- Defined: `model.py:1416`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1437`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _apply_spatial_stack `def _apply_spatial_stack(self, feat)`
- Defined: `model.py:1466`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, tokens, frame_offsets)`
- Defined: `model.py:1473`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1541`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _freeze_backbone `def _freeze_backbone(self)`
- Defined: `model.py:1551`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _make_gen_masks `def _make_gen_masks(self, batch_size, device)`
- Defined: `model.py:1557`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### forward `def forward(self, video)`
- Defined: `model.py:1574`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1625`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _temporal_gradient_loss `def _temporal_gradient_loss(self, generated, target)`
- Defined: `model.py:1658`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### train_epoch `def train_epoch(self, dataloader, epoch)`
- Defined: `model.py:1664`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### save_checkpoint `def save_checkpoint(self, epoch, metrics)`
- Defined: `model.py:1750`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### load_checkpoint `def load_checkpoint(self, path)`
- Defined: `model.py:1766`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config)`
- Defined: `model.py:1790`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __len__ `def __len__(self)`
- Defined: `model.py:1801`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _init_objects `def _init_objects(self, rng)`
- Defined: `model.py:1804`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _render_frame `def _render_frame(self, objects, grid_x, grid_y)`
- Defined: `model.py:1826`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _update_physics `def _update_physics(self, objects)`
- Defined: `model.py:1851`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __getitem__ `def __getitem__(self, idx)`
- Defined: `model.py:1869`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, video_dir, config)`
- Defined: `model.py:1901`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __len__ `def __len__(self)`
- Defined: `model.py:1924`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __getitem__ `def __getitem__(self, idx)`
- Defined: `model.py:1927`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, model, decay, start_step)`
- Defined: `model.py:1948`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### step `def step(self, model, global_step)`
- Defined: `model.py:1958`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### swap_swa `def swap_swa(self, model)`
- Defined: `model.py:1969`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### restore `def restore(self, model, saved)`
- Defined: `model.py:1978`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, kappa_threshold, max_kappa)`
- Defined: `model.py:1993`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### get_lr_scale `def get_lr_scale(self, kappa)`
- Defined: `model.py:1997`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self)`
- Defined: `model.py:2006`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### arm `def arm(self, checkpoint_fn)`
- Defined: `model.py:2010`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### disarm `def disarm(self)`
- Defined: `model.py:2014`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _handler `def _handler(self, signum, frame)`
- Defined: `model.py:2017`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, project, config, enabled)`
- Defined: `model.py:2031`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### log `def log(self, data, step)`
- Defined: `model.py:2043`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### finish `def finish(self)`
- Defined: `model.py:2048`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### __init__ `def __init__(self, config, swa, phase_lr, preempt, wandb)`
- Defined: `model.py:2069`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _emergency_save `def _emergency_save(self)`
- Defined: `model.py:2121`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### _cosine_lr `def _cosine_lr(self, step, total_steps)`
- Defined: `model.py:2125`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### train_epoch `def train_epoch(self, dataloader, epoch, total_steps)`
- Defined: `model.py:2140`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### save_checkpoint `def save_checkpoint(self, epoch, metrics, is_latest)`
- Defined: `model.py:2244`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### load_checkpoint `def load_checkpoint(self, path)`
- Defined: `model.py:2263`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2323`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_decoder_output_shape `def test_decoder_output_shape(self)`
- Defined: `model.py:2332`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_decoder_pixel_range `def test_decoder_pixel_range(self)`
- Defined: `model.py:2340`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_decoder_gradient_flows `def test_decoder_gradient_flows(self)`
- Defined: `model.py:2348`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2362`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_generator_output_shape `def test_generator_output_shape(self)`
- Defined: `model.py:2376`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_generator_backbone_frozen `def test_generator_backbone_frozen(self)`
- Defined: `model.py:2388`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2400`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_train_one_step `def test_train_one_step(self)`
- Defined: `model.py:2423`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_decoder_parameters_update `def test_decoder_parameters_update(self)`
- Defined: `model.py:2433`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2447`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_hamilton_product_identity `def test_hamilton_product_identity(self)`
- Defined: `model.py:2451`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_hamilton_product_ij_equals_k `def test_hamilton_product_ij_equals_k(self)`
- Defined: `model.py:2455`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_normalize_unit `def test_normalize_unit(self)`
- Defined: `model.py:2462`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_conjugate_product_identity `def test_conjugate_product_identity(self)`
- Defined: `model.py:2467`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_rotate_vector_norm_preserving `def test_rotate_vector_norm_preserving(self)`
- Defined: `model.py:2474`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_log_exp_roundtrip `def test_log_exp_roundtrip(self)`
- Defined: `model.py:2482`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_lie_product_approximation `def test_lie_product_approximation(self)`
- Defined: `model.py:2489`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_output_divisible_by_4 `def test_output_divisible_by_4(self)`
- Defined: `model.py:2503`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_gradient_flows `def test_gradient_flows(self)`
- Defined: `model.py:2509`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2521`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_forward_shape_matches_config `def test_forward_shape_matches_config(self)`
- Defined: `model.py:2527`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_temporal_derivative_handles_single_frame `def test_temporal_derivative_handles_single_frame(self)`
- Defined: `model.py:2537`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2549`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_mask_shapes `def test_mask_shapes(self)`
- Defined: `model.py:2552`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_predictor_mask_subset_of_encoder_mask `def test_predictor_mask_subset_of_encoder_mask(self)`
- Defined: `model.py:2559`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2570`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_forward_loss_scalar `def test_forward_loss_scalar(self)`
- Defined: `model.py:2577`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_encoder_output_shape `def test_encoder_output_shape(self)`
- Defined: `model.py:2587`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_predictor_output_shape `def test_predictor_output_shape(self)`
- Defined: `model.py:2598`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_torus_brain_forward `def test_torus_brain_forward(self)`
- Defined: `model.py:2611`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_quaternion_spectral_layer_forward `def test_quaternion_spectral_layer_forward(self)`
- Defined: `model.py:2619`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_complex_spectral_layer_forward `def test_complex_spectral_layer_forward(self)`
- Defined: `model.py:2627`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_moe_forward `def test_moe_forward(self)`
- Defined: `model.py:2633`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_attention_forward `def test_attention_forward(self)`
- Defined: `model.py:2640`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_block_forward `def test_block_forward(self)`
- Defined: `model.py:2647`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2658`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_output_shape `def test_output_shape(self)`
- Defined: `model.py:2665`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_pixel_range `def test_pixel_range(self)`
- Defined: `model.py:2671`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_deterministic `def test_deterministic(self)`
- Defined: `model.py:2677`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_different_indices_differ `def test_different_indices_differ(self)`
- Defined: `model.py:2683`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### setUp `def setUp(self)`
- Defined: `model.py:2693`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_train_one_step `def test_train_one_step(self)`
- Defined: `model.py:2711`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_train_multiple_steps `def test_train_multiple_steps(self)`
- Defined: `model.py:2721`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_bad_d_model_raises `def test_bad_d_model_raises(self)`
- Defined: `model.py:2734`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_bad_mask_ratio_raises `def test_bad_mask_ratio_raises(self)`
- Defined: `model.py:2738`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_bad_data_mode_raises `def test_bad_data_mode_raises(self)`
- Defined: `model.py:2742`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### test_micro_config_valid `def test_micro_config_valid(self)`
- Defined: `model.py:2746`
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

### to_frames `def to_frames(t)`
- Defined: `model.py:2782`
- Doc: [T, C, H, W] float -> [T, H, W, C] uint8.
- Depends on: `src/quaternion_ops.py`, `src/ucf101_dataset.py`
- Imported by: `app.py`

## src/quaternion_ops.py

### hamilton_product `def hamilton_product(q1, q2)`
- Defined: `src/quaternion_ops.py:31`
- Imported by: `model.py`

### normalize `def normalize(q, eps)`
- Defined: `src/quaternion_ops.py:42`
- Imported by: `model.py`

### conjugate `def conjugate(q)`
- Defined: `src/quaternion_ops.py:46`
- Imported by: `model.py`

### rotate_vector `def rotate_vector(v, q)`
- Defined: `src/quaternion_ops.py:50`
- Imported by: `model.py`

### log `def log(q, eps)`
- Defined: `src/quaternion_ops.py:59`
- Doc: Logarithmic map from SU(2) to so(3) (tangent space).
- Imported by: `model.py`

### exp `def exp(q, eps)`
- Defined: `src/quaternion_ops.py:79`
- Doc: Exponential map from so(3) to SU(2).
- Imported by: `model.py`

### lie_product `def lie_product(q1, q2, eps)`
- Defined: `src/quaternion_ops.py:103`
- Doc: Approximate quaternion product via Lie algebra addition.
- Imported by: `model.py`

### __init__ `def __init__(self, in_features, out_features, bias)`
- Defined: `src/quaternion_ops.py:122`
- Imported by: `model.py`

### forward `def forward(self, x)`
- Defined: `src/quaternion_ops.py:137`
- Imported by: `model.py`

## src/ucf101_dataset.py

### _detect_video_backend `def _detect_video_backend()`
- Defined: `src/ucf101_dataset.py:42`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _download_url `def _download_url(url, dst_path, min_bytes)`
- Defined: `src/ucf101_dataset.py:352`
- Doc: Download a URL to a local path with SSL fallback and size check.
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _extract_rar `def _extract_rar(rar_path, output_dir)`
- Defined: `src/ucf101_dataset.py:404`
- Doc: Extract a .rar archive using available system tools.
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### create_ucf101_dataloader `def create_ucf101_dataloader(config)`
- Defined: `src/ucf101_dataset.py:433`
- Doc: Create a DataLoader for the UCF101 dataset.
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### __init__ `def __init__(self, cache_dir, capacity)`
- Defined: `src/ucf101_dataset.py:69`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _cache_path `def _cache_path(self, video_path)`
- Defined: `src/ucf101_dataset.py:75`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### get_or_decode `def get_or_decode(self, video_path, decode_fn)`
- Defined: `src/ucf101_dataset.py:79`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### __post_init__ `def __post_init__(self)`
- Defined: `src/ucf101_dataset.py:129`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### __init__ `def __init__(self, config)`
- Defined: `src/ucf101_dataset.py:158`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### num_classes `def num_classes(self)`
- Defined: `src/ucf101_dataset.py:183`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### num_samples `def num_samples(self)`
- Defined: `src/ucf101_dataset.py:187`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### config `def config(self)`
- Defined: `src/ucf101_dataset.py:191`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _acquire_annotations `def _acquire_annotations(self)`
- Defined: `src/ucf101_dataset.py:194`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _normalize_video_dir `def _normalize_video_dir(self)`
- Defined: `src/ucf101_dataset.py:225`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _cleanup_video_dir `def _cleanup_video_dir(self)`
- Defined: `src/ucf101_dataset.py:231`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _download_and_extract_videos `def _download_and_extract_videos(self)`
- Defined: `src/ucf101_dataset.py:238`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _parse_split `def _parse_split(self)`
- Defined: `src/ucf101_dataset.py:269`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### __len__ `def __len__(self)`
- Defined: `src/ucf101_dataset.py:299`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### __getitem__ `def __getitem__(self, index)`
- Defined: `src/ucf101_dataset.py:302`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _read_video_raw `def _read_video_raw(self, path)`
- Defined: `src/ucf101_dataset.py:319`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _make_dummy `def _make_dummy(self)`
- Defined: `src/ucf101_dataset.py:344`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

### _collate_fn `def _collate_fn(batch)`
- Defined: `src/ucf101_dataset.py:442`
- Imported by: `model.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`, `tests/test_ucf101_dataset.py`

## tests/test_ucf101_dataset.py

### _make_test_video `def _make_test_video(path, num_frames, height, width, seed)`
- Defined: `tests/test_ucf101_dataset.py:29`
- Depends on: `src/ucf101_dataset.py`

### _make_annotation_files `def _make_annotation_files(annotation_dir, split, split_index, entries)`
- Defined: `tests/test_ucf101_dataset.py:48`
- Depends on: `src/ucf101_dataset.py`

### test_default_config_is_valid `def test_default_config_is_valid(self)`
- Defined: `tests/test_ucf101_dataset.py:72`
- Depends on: `src/ucf101_dataset.py`

### test_valid_config_accepts_all_fields `def test_valid_config_accepts_all_fields(self)`
- Defined: `tests/test_ucf101_dataset.py:81`
- Depends on: `src/ucf101_dataset.py`

### test_zero_frames_per_clip_raises `def test_zero_frames_per_clip_raises(self)`
- Defined: `tests/test_ucf101_dataset.py:102`
- Depends on: `src/ucf101_dataset.py`

### test_negative_output_size_raises `def test_negative_output_size_raises(self)`
- Defined: `tests/test_ucf101_dataset.py:107`
- Depends on: `src/ucf101_dataset.py`

### test_invalid_split_raises `def test_invalid_split_raises(self)`
- Defined: `tests/test_ucf101_dataset.py:114`
- Depends on: `src/ucf101_dataset.py`

### test_invalid_split_index_raises `def test_invalid_split_index_raises(self)`
- Defined: `tests/test_ucf101_dataset.py:119`
- Depends on: `src/ucf101_dataset.py`

### test_negative_num_workers_raises `def test_negative_num_workers_raises(self)`
- Defined: `tests/test_ucf101_dataset.py:126`
- Depends on: `src/ucf101_dataset.py`

### test_zero_batch_size_raises `def test_zero_batch_size_raises(self)`
- Defined: `tests/test_ucf101_dataset.py:131`
- Depends on: `src/ucf101_dataset.py`

### setUp `def setUp(self)`
- Defined: `tests/test_ucf101_dataset.py:140`
- Depends on: `src/ucf101_dataset.py`

### tearDown `def tearDown(self)`
- Defined: `tests/test_ucf101_dataset.py:148`
- Depends on: `src/ucf101_dataset.py`

### test_missing_annotation_file_raises `def test_missing_annotation_file_raises(self)`
- Defined: `tests/test_ucf101_dataset.py:151`
- Depends on: `src/ucf101_dataset.py`

### test_empty_annotation_raises_runtime_error `def test_empty_annotation_raises_runtime_error(self)`
- Defined: `tests/test_ucf101_dataset.py:162`
- Depends on: `src/ucf101_dataset.py`

### test_loads_samples_with_valid_annotations `def test_loads_samples_with_valid_annotations(self)`
- Defined: `tests/test_ucf101_dataset.py:174`
- Depends on: `src/ucf101_dataset.py`

### test_num_classes_matches_annotation `def test_num_classes_matches_annotation(self)`
- Defined: `tests/test_ucf101_dataset.py:190`
- Depends on: `src/ucf101_dataset.py`

### setUp `def setUp(self)`
- Defined: `tests/test_ucf101_dataset.py:213`
- Depends on: `src/ucf101_dataset.py`

### tearDown `def tearDown(self)`
- Defined: `tests/test_ucf101_dataset.py:234`
- Depends on: `src/ucf101_dataset.py`

### test_output_shape_with_resize `def test_output_shape_with_resize(self)`
- Defined: `tests/test_ucf101_dataset.py:237`
- Depends on: `src/ucf101_dataset.py`

### test_output_shape_without_resize `def test_output_shape_without_resize(self)`
- Defined: `tests/test_ucf101_dataset.py:253`
- Depends on: `src/ucf101_dataset.py`

### test_pixel_range `def test_pixel_range(self)`
- Defined: `tests/test_ucf101_dataset.py:271`
- Depends on: `src/ucf101_dataset.py`

### test_dtype_is_float32 `def test_dtype_is_float32(self)`
- Defined: `tests/test_ucf101_dataset.py:287`
- Depends on: `src/ucf101_dataset.py`

### test_different_indices_return_different_tensors `def test_different_indices_return_different_tensors(self)`
- Defined: `tests/test_ucf101_dataset.py:300`
- Depends on: `src/ucf101_dataset.py`

### test_short_video_gets_padded `def test_short_video_gets_padded(self)`
- Defined: `tests/test_ucf101_dataset.py:314`
- Depends on: `src/ucf101_dataset.py`

### test_deterministic_output_for_same_index `def test_deterministic_output_for_same_index(self)`
- Defined: `tests/test_ucf101_dataset.py:347`
- Depends on: `src/ucf101_dataset.py`

### setUp `def setUp(self)`
- Defined: `tests/test_ucf101_dataset.py:366`
- Depends on: `src/ucf101_dataset.py`

### tearDown `def tearDown(self)`
- Defined: `tests/test_ucf101_dataset.py:374`
- Depends on: `src/ucf101_dataset.py`

### test_missing_video_file_returns_dummy `def test_missing_video_file_returns_dummy(self)`
- Defined: `tests/test_ucf101_dataset.py:377`
- Depends on: `src/ucf101_dataset.py`

### setUp `def setUp(self)`
- Defined: `tests/test_ucf101_dataset.py:401`
- Depends on: `src/ucf101_dataset.py`

### tearDown `def tearDown(self)`
- Defined: `tests/test_ucf101_dataset.py:424`
- Depends on: `src/ucf101_dataset.py`

### test_dataloader_returns_batched_tensors `def test_dataloader_returns_batched_tensors(self)`
- Defined: `tests/test_ucf101_dataset.py:427`
- Depends on: `src/ucf101_dataset.py`

### test_dataloader_works_with_trainer_pattern `def test_dataloader_works_with_trainer_pattern(self)`
- Defined: `tests/test_ucf101_dataset.py:450`
- Depends on: `src/ucf101_dataset.py`
