from risk import sample_ratio_mismatch, insufficient_sample_size


def test_sample_ratio_mismatch_no_srm():
    # fixtures
    control_n = 500
    variant_n = 500
    expected_split = 0.5
    expected = False
    
    # run
    result = sample_ratio_mismatch(control_n, variant_n, expected_split)
    
    # assert
    assert result == expected


def test_sample_ratio_mismatch_detected():
    # fixtures
    control_n = 400
    variant_n = 600
    expected_split = 0.5
    expected = True
    
    # run
    result = sample_ratio_mismatch(control_n, variant_n, expected_split)
    
    # assert
    assert result == expected


def test_insufficient_sample_size_adequate():
    # fixtures
    n_users = 50000
    min_detectable_effect = 0.1
    expected = False
    
    # run
    result = insufficient_sample_size(n_users, min_detectable_effect)
    
    # assert
    assert result == expected


def test_insufficient_sample_size_inadequate():
    # fixtures
    n_users = 100
    min_detectable_effect = 0.1
    expected = True
    
    # run
    result = insufficient_sample_size(n_users, min_detectable_effect)
    
    # assert
    assert result == expected