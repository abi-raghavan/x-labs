import pandas as pd
from metrics import users_by_variant, conversion_rate, revenue_per_user, absolute_lift, relative_lift


def test_users_by_variant():
    # fixtures
    df_input = pd.DataFrame({
        'variant': ['control', 'control', 'variant', 'variant', 'variant']
    })
    expected = pd.DataFrame({
        'variant': ['control', 'variant'],
        'count': [2, 3]
    })
    
    # run
    result = users_by_variant(df_input)
    
    # assert
    pd.testing.assert_frame_equal(result, expected)


def test_conversion_rate():
    # fixtures
    df_input = pd.DataFrame({
        'variant': ['control', 'control', 'variant', 'variant'],
        'converted': [True, False, True, True]
    })
    expected = pd.DataFrame({
        'variant': ['control', 'variant'],
        'sum': [1, 2],
        'count': [2, 2]
    })
    
    # run
    result = conversion_rate(df_input)
    
    # assert
    pd.testing.assert_frame_equal(result, expected)


def test_revenue_per_user():
    # fixtures
    df_input = pd.DataFrame({
        'variant': ['control', 'control', 'variant', 'variant'],
        'revenue': [10.0, 20.0, 30.0, 40.0]
    })
    expected = pd.DataFrame({
        'variant': ['control', 'variant'],
        'revenue': [15.0, 35.0]
    })
    
    # run
    result = revenue_per_user(df_input)
    
    # assert
    pd.testing.assert_frame_equal(result, expected)


def test_absolute_lift():
    # fixtures
    df_input = pd.DataFrame({
        'variant': ['control', 'control', 'variant', 'variant'],
        'converted': [False, False, True, True]
    })
    expected = 1.0
    
    # run
    result = absolute_lift(df_input)
    
    # assert
    assert result == expected


def test_relative_lift():
    # fixtures
    df_input = pd.DataFrame({
        'variant': ['control', 'control', 'variant', 'variant'],
        'converted': [True, False, True, True]
    })
    expected = 1.0
    
    # run
    result = relative_lift(df_input)
    
    # assert
    assert result == expected