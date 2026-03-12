import numpy as np


def sample_ratio_mismatch(control_n, variant_n, expected_split):
    total_n = control_n + variant_n
    expected_control = total_n * expected_split
    expected_variant = total_n * (1 - expected_split)
    
    chi2_stat = ((control_n - expected_control)**2 / expected_control + 
                 (variant_n - expected_variant)**2 / expected_variant)
    
    critical_value = 3.84
    return chi2_stat > critical_value


def insufficient_sample_size(n_users, min_detectable_effect, alpha=0.05, power=0.8):
    z_alpha = 1.96
    z_beta = 0.84
    
    p_baseline = 0.10
    p_variant = p_baseline * (1 + min_detectable_effect)
    
    p_avg = (p_baseline + p_variant) / 2
    
    required_per_group = (2 * p_avg * (1 - p_avg) * (z_alpha + z_beta)**2) / (p_variant - p_baseline)**2
    
    return n_users < (2 * required_per_group)