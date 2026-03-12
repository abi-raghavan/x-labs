import numpy as np
from stats import two_proportion_z_test, revenue_t_test


def test_two_proportion_z_test():
    # fixtures
    control_conv = 50
    control_n = 500
    variant_conv = 60
    variant_n = 500
    expected_p_value = 0.3122
    
    # run
    result = two_proportion_z_test(control_conv, control_n, variant_conv, variant_n)
    
    # assert
    assert 'p_value' in result
    assert 'confidence_interval' in result
    assert abs(result['p_value'] - expected_p_value) < 0.01
    assert len(result['confidence_interval']) == 2


def test_revenue_t_test():
    # fixtures
    control_revenue = np.array([25.0, 30.0, 20.0, 35.0, 28.0])
    variant_revenue = np.array([30.0, 35.0, 25.0, 40.0, 33.0])
    
    # run
    result = revenue_t_test(control_revenue, variant_revenue)
    
    # assert
    assert 'p_value' in result
    assert 'confidence_interval' in result
    assert isinstance(result['p_value'], float)
    assert len(result['confidence_interval']) == 2