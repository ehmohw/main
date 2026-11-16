"""electric and storm sounds: sparks, buzz stabs, crackle, rain, thunder, lightning cracks"""
import numpy as np
from gv_music import SR, T, env, lp, hp, bp
from armada_music import osc, zap


def spark(amp=1.0, seed=0, dur=0.35):
    """a single electric spark: a sharp crackle and a tiny falling zap"""
    rng = np.random.default_rng(seed); t = T(dur); n = len(t)
    imp = (rng.random(n) > 0.97).astype(float) * np.exp(-t * 18)
    return amp * (hp(imp * rng.uniform(-1, 1, n), 2500) * 2.5 + zap(0.35, 6000, 900, dur) * np.exp(-t * 10))


def buzz(f, dur, amp=1.0):
    """an electric buzz-stab: a square wave through a fizzing high end, cut short - the sound of current"""
    t = T(dur); n = len(t)
    s = osc(np.full(n, f), 'pulse', 0.25) + 0.5 * osc(np.full(n, f * 2.005), 'pulse', 0.5)
    s = np.tanh(3 * s) + 0.3 * hp(np.random.uniform(-1, 1, n), 4000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 60 * t)))
    return amp * lp(s, 5000) * env(n, 0.003, 0.0, 1, 0.03) * np.exp(-t * 6)


def crackle(dur, amp=1.0, density=0.985, seed=0):
    """a bed of electric crackle"""
    rng = np.random.default_rng(seed); n = len(T(dur))
    imp = (rng.random(n) > density).astype(float) * rng.uniform(-1, 1, n)
    return amp * hp(imp, 3000) * 2.0


def rain(dur, amp=1.0, seed=0):
    """rain: a hiss with drops in it"""
    rng = np.random.default_rng(seed); t = T(dur); n = len(t)
    hiss = bp(rng.uniform(-1, 1, n), 1500, 9000) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.13 * t))
    drops = hp((rng.random(n) > 0.995).astype(float) * rng.uniform(-1, 1, n), 2000) * 1.2
    return amp * (hiss * 0.5 + drops) * env(n, min(1.0, dur / 4), 0, 1, min(1.0, dur / 4))


def thunder(amp=1.0, dur=5.0, seed=0, crack=True):
    """thunder: a crack (if close), then a long rolling rumble"""
    rng = np.random.default_rng(seed); t = T(dur); n = len(t)
    brown = np.cumsum(rng.uniform(-1, 1, n)); brown -= np.convolve(brown, np.ones(2000) / 2000, 'same')
    roll = np.abs(np.convolve(rng.uniform(-1, 1, n // 400 + 2).repeat(400)[:n], np.ones(1500) / 1500, 'same')) * 6
    s = lp(brown, 220) * 0.004 * (0.4 + roll) * np.exp(-t / (dur * 0.45)) * np.clip(t / 0.08, 0, 1)
    if crack:
        c = hp(rng.uniform(-1, 1, n), 1200) * np.exp(-t * 14) * 1.2 + bp(rng.uniform(-1, 1, n), 200, 2000) * np.exp(-t * 5) * 0.6
        s = s + c
    return amp * s


def strike(amp=1.0, seed=0):
    """lightning striking close: crackle, crack, thunder"""
    return thunder(amp, 4.0, seed, True) + np.pad(spark(amp * 0.8, seed, 0.5), (0, len(T(4.0)) - len(T(0.5))))
