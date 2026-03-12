from assignment import assign_variant


def test_assign_variant_deterministic():
    # fixtures
    user_id = "user123"
    experiment_id = "exp456"
    split = 0.5
    expected = "variant"
    
    # run
    result = assign_variant(user_id, experiment_id, split)
    
    # assert
    assert result == expected


def test_assign_variant_different_user():
    # fixtures
    user_id = "user999"
    experiment_id = "exp456"
    split = 0.5
    expected = "control"
    
    # run
    result = assign_variant(user_id, experiment_id, split)
    
    # assert
    assert result == expected


def test_assign_variant_zero_split():
    # fixtures
    user_id = "user123"
    experiment_id = "exp456"
    split = 0.0
    expected = "variant"
    
    # run
    result = assign_variant(user_id, experiment_id, split)
    
    # assert
    assert result == expected


def test_assign_variant_full_split():
    # fixtures
    user_id = "user123"
    experiment_id = "exp456"
    split = 1.0
    expected = "control"
    
    # run
    result = assign_variant(user_id, experiment_id, split)
    
    # assert
    assert result == expected