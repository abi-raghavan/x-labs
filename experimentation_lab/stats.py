import numpy as np
from scipy import stats


def two_proportion_z_test(control_conv, control_n, variant_conv, variant_n):
    p1 = control_conv / control_n
    p2 = variant_conv / variant_n
    
    p_pooled = (control_conv + variant_conv) / (control_n + variant_n)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/control_n + 1/variant_n))
    
    z_score = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    margin_error = 1.96 * se
    ci_lower = (p2 - p1) - margin_error
    ci_upper = (p2 - p1) + margin_error
    
    return {
        'p_value': p_value,
        'confidence_interval': (ci_lower, ci_upper)
    }


def revenue_t_test(control_revenue, variant_revenue):
    t_stat, p_value = stats.ttest_ind(variant_revenue, control_revenue, equal_var=False)
    
    mean_diff = np.mean(variant_revenue) - np.mean(control_revenue)
    se_diff = np.sqrt(np.var(variant_revenue, ddof=1)/len(variant_revenue) + 
                      np.var(control_revenue, ddof=1)/len(control_revenue))
    
    margin_error = 1.96 * se_diff
    ci_lower = mean_diff - margin_error
    ci_upper = mean_diff + margin_error
    
    return {
        'p_value': p_value,
        'confidence_interval': (ci_lower, ci_upper)
    }