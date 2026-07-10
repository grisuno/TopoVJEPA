#!/usr/bin/env python3
# _*_ coding: utf8 _*_
"""
app.py

Autor: Gris Iscomeback
Correo electrónico: grisiscomeback[at]gmail[dot]com
Fecha de creación: xx/xx/xxxx
Licencia: GPL v3

Descripción:  
"""
import model

config = VJEPAQConfig(
    D_MODEL=256,
    N_HEADS=8,
    NUM_FRAMES=32,
    TORUS_SOFT_ASSIGN_TEMPERATURE=0.5,
)
