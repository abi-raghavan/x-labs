import pandas as pd
import numpy as np
from data import generate_users


def test_generate_users():
    # Fixtures
    num_riders = 5
    expected_columns = [
        'rider_id', 'city', 'weekly_rides', 'monthly_rides',
        'days_since_last_ride', 'average_trip_value', 'promotion_acceptance_rate', 'will_book_ride'
    ]
    expected_shape = (5, 8)
    
    # Run
    result = generate_users(num_riders)
    
    # Assert
    assert result.shape == expected_shape
    assert list(result.columns) == expected_columns
    assert result['rider_id'].tolist() == [1, 2, 3, 4, 5]
    assert result['will_book_ride'].dtype == 'int64'
    assert all(result['city'].isin(['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Boston']))


def test_generate_users_deterministic():
    # Fixtures
    num_riders = 3
    expected_first_row = {
        'rider_id': 1,
        'city': 'Chicago',
        'weekly_rides': 3,
        'monthly_rides': 4,
        'days_since_last_ride': 4,
        'average_trip_value': 34.07,
        'promotion_acceptance_rate': 0.533,
        'will_book_ride': 1
    }
    
    # Run
    result = generate_users(num_riders)
    
    # Assert
    first_row = result.iloc[0].to_dict()
    for key, expected_value in expected_first_row.items():
        assert first_row[key] == expected_value