#!/usr/bin/env python3
# _*_ coding: utf8 _*_
"""
app.py — Entry-point funcional para TopoVJEPA.

Uso:
    from app import create_model, create_trainer, create_dataset

    # 3 líneas: modelo + datos + entrenar
    model = create_model('micro')
    loader = create_dataset(model.config)
    trainer = create_trainer(model.config)
    metrics = trainer.train_epoch(loader, epoch=0, total_steps=10)
"""
import model


def create_model(scale='micro', **overrides):
    m = model.VJEPAQ.from_preset(scale, **overrides)
    print(f"Modelo {scale}: {sum(p.numel() for p in m.parameters())} params")
    return m


def create_dataset(config):
    return model.MovingShapesDataset(config)


def create_trainer(config):
    return model.VJEPAQTrainer(config)


def create_generator(config):
    return model.VJEPAQVideoGenerator(config)


def create_generator_trainer(config):
    return model.VJEPAQGeneratorTrainer(config)


if __name__ == '__main__':
    m = create_model('micro')
    ds = create_dataset(m.config)
    print(f"Dataset: {len(ds)} samples, shape={ds[0].shape}")
