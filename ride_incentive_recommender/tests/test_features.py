import pandas as pd
from features import prepare_features


def test_prepare_features():
    # Fixtures
    riders_df = pd.DataFrame({
        'rider_id': [1, 2, 3],
        'city': ['New York', 'San Francisco', 'Los Angeles'],
        'weekly_rides': [2, 1, 3],
        'monthly_rides': [8, 5, 12],
        'days_since_last_ride': [2, 7, 1],
        'average_trip_value': [25.5, 30.2, 22.8],
        'promotion_acceptance_rate': [0.3, 0.1, 0.5],
        'will_book_ride': [1, 0, 1]
    })
    expected_features_shape = (3, 5)
    expected_target_values = [1, 0, 1]
    
    # Run
    rider_features, conversion_target = prepare_features(riders_df)
    
    # Assert
    assert rider_features.shape == expected_features_shape
    assert conversion_target.tolist() == expected_target_values
    assert rider_features.iloc[0, 0] == 2
    assert rider_features.iloc[1, 3] == 30.2