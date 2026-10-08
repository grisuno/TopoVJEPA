# Concepts

Second-brain semantic layer: nouns map atomically to file sets (EXTRACTED); verbs aggregate structural edges (INFERRED).

| Concept | Files | Mentions | Top Files |
|---------|-------|----------|-----------|
| `dataset` | 4 | 25 | `app.py`, `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `config` | 4 | 18 | `app.py`, `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `create` | 4 | 17 | `app.py`, `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `output` | 4 | 14 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `trainer` | 4 | 14 | `app.py`, `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `tensors` | 4 | 8 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `loader` | 4 | 5 | `app.py`, `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `video` | 3 | 36 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `model` | 3 | 17 | `app.py`, `model.py`, `src/ucf101_dataset.py` |
| `via` | 3 | 11 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py` |
| `shape` | 3 | 9 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `frames` | 3 | 8 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `train` | 3 | 8 | `app.py`, `model.py`, `src/ucf101_dataset.py` |
| `error` | 3 | 7 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `must` | 3 | 7 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py` |
| `data` | 3 | 6 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `dataloader` | 3 | 6 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `files` | 3 | 6 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `get` | 3 | 6 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `getitem` | 3 | 5 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `size` | 3 | 5 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `when` | 3 | 5 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `all` | 3 | 4 | `model.py`, `src/quaternion_ops.py`, `tests/test_ucf101_dataset.py` |
| `make` | 3 | 4 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `topo` | 3 | 4 | `app.py`, `model.py`, `src/ucf101_dataset.py` |
| `back` | 3 | 3 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py` |
| `normalize` | 3 | 3 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py` |
| `then` | 3 | 3 | `model.py`, `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `uses` | 3 | 3 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py` |
| `using` | 3 | 3 | `model.py`, `src/quaternion_ops.py`, `src/ucf101_dataset.py` |
| `quaternion` | 2 | 34 | `model.py`, `src/quaternion_ops.py` |
| `forward` | 2 | 26 | `model.py`, `src/quaternion_ops.py` |
| `ucf101` | 2 | 24 | `src/ucf101_dataset.py`, `tests/test_ucf101_dataset.py` |
| `log` | 2 | 18 | `model.py`, `src/quaternion_ops.py` |
| `product` | 2 | 16 | `model.py`, `src/quaternion_ops.py` |
| `behaviour` | 2 | 15 | `model.py`, `tests/test_ucf101_dataset.py` |
| `set` | 2 | 15 | `model.py`, `tests/test_ucf101_dataset.py` |
| `temporal` | 2 | 14 | `model.py`, `src/ucf101_dataset.py` |
| `exp` | 2 | 12 | `model.py`, `src/quaternion_ops.py` |
| `lie` | 2 | 12 | `model.py`, `src/quaternion_ops.py` |
| `raises` | 2 | 11 | `model.py`, `tests/test_ucf101_dataset.py` |
| `space` | 2 | 11 | `model.py`, `src/quaternion_ops.py` |
| `generator` | 2 | 10 | `app.py`, `model.py` |
| `hamilton` | 2 | 10 | `model.py`, `src/quaternion_ops.py` |
| `algebra` | 2 | 9 | `model.py`, `src/quaternion_ops.py` |
| `converts` | 2 | 9 | `model.py`, `src/quaternion_ops.py` |
| `decoder` | 2 | 9 | `model.py`, `src/ucf101_dataset.py` |
| `pixel` | 2 | 7 | `model.py`, `tests/test_ucf101_dataset.py` |
| `valid` | 2 | 7 | `model.py`, `tests/test_ucf101_dataset.py` |
| `cache` | 2 | 6 | `model.py`, `src/ucf101_dataset.py` |

## Verb Edges

| Source | Verb | Target | Strength |
|--------|------|--------|----------|
| `config` | `depends_on` | `back` | 1.00 |
| `config` | `depends_on` | `must` | 1.00 |
| `config` | `depends_on` | `normalize` | 1.00 |
| `config` | `depends_on` | `output` | 1.00 |
| `config` | `depends_on` | `tensors` | 1.00 |
| `config` | `depends_on` | `uses` | 1.00 |
| `config` | `depends_on` | `using` | 1.00 |
| `config` | `depends_on` | `via` | 1.00 |
| `create` | `depends_on` | `back` | 1.00 |
| `create` | `depends_on` | `must` | 1.00 |
| `create` | `depends_on` | `normalize` | 1.00 |
| `create` | `depends_on` | `output` | 1.00 |
| `create` | `depends_on` | `tensors` | 1.00 |
| `create` | `depends_on` | `uses` | 1.00 |
| `create` | `depends_on` | `using` | 1.00 |
| `create` | `depends_on` | `via` | 1.00 |
| `dataset` | `depends_on` | `back` | 1.00 |
| `dataset` | `depends_on` | `must` | 1.00 |
| `dataset` | `depends_on` | `normalize` | 1.00 |
| `dataset` | `depends_on` | `output` | 1.00 |
| `dataset` | `depends_on` | `tensors` | 1.00 |
| `dataset` | `depends_on` | `uses` | 1.00 |
| `dataset` | `depends_on` | `using` | 1.00 |
| `dataset` | `depends_on` | `via` | 1.00 |
| `loader` | `depends_on` | `back` | 1.00 |
| `loader` | `depends_on` | `must` | 1.00 |
| `loader` | `depends_on` | `normalize` | 1.00 |
| `loader` | `depends_on` | `output` | 1.00 |
| `loader` | `depends_on` | `tensors` | 1.00 |
| `loader` | `depends_on` | `uses` | 1.00 |
| `loader` | `depends_on` | `using` | 1.00 |
| `loader` | `depends_on` | `via` | 1.00 |
| `trainer` | `depends_on` | `back` | 1.00 |
| `trainer` | `depends_on` | `must` | 1.00 |
| `trainer` | `depends_on` | `normalize` | 1.00 |
| `trainer` | `depends_on` | `output` | 1.00 |
| `trainer` | `depends_on` | `tensors` | 1.00 |
| `trainer` | `depends_on` | `uses` | 1.00 |
| `trainer` | `depends_on` | `using` | 1.00 |
| `trainer` | `depends_on` | `via` | 1.00 |
| `all` | `depends_on` | `back` | 0.75 |
| `all` | `depends_on` | `must` | 0.75 |
| `all` | `depends_on` | `normalize` | 0.75 |
| `all` | `depends_on` | `output` | 0.75 |
| `all` | `depends_on` | `tensors` | 0.75 |
| `all` | `depends_on` | `uses` | 0.75 |
| `all` | `depends_on` | `using` | 0.75 |
| `all` | `depends_on` | `via` | 0.75 |
| `behaviour` | `depends_on` | `back` | 0.75 |
| `behaviour` | `depends_on` | `must` | 0.75 |

## Dialectic Prompts

- Thesis: `algebra` centralizes 2 files; Antithesis: `all` pulls 3 files with 2 shared (Jaccard 0.67); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `back` pulls 3 files with 2 shared (Jaccard 0.67); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `converts` pulls 2 files with 2 shared (Jaccard 1.00); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `exp` pulls 2 files with 2 shared (Jaccard 1.00); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `forward` pulls 2 files with 2 shared (Jaccard 1.00); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `hamilton` pulls 2 files with 2 shared (Jaccard 1.00); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `lie` pulls 2 files with 2 shared (Jaccard 1.00); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `log` pulls 2 files with 2 shared (Jaccard 1.00); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `must` pulls 3 files with 2 shared (Jaccard 0.67); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
- Thesis: `algebra` centralizes 2 files; Antithesis: `normalize` pulls 3 files with 2 shared (Jaccard 0.67); Synthesis: should they merge, split by layer, or keep `bridges` explicit?
