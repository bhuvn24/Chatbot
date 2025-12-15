# src/utils/privacy.py
import numpy as np
from src.config.settings import Settings

def add_dp_noise(embeds: np.ndarray) -> np.ndarray:
    """Add Laplace noise for differential privacy (epsilon from settings)."""
    noise = np.random.laplace(0, 1.0 / Settings.EPSILON_DP, embeds.shape)
    return embeds + noise