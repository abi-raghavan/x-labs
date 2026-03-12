import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from model import predict_booking_probability


def test_predict_booking_probability():
    # Fixtures
    training_features = pd.DataFrame({
        'weekly_rides': [1, 2, 0, 3],
        'monthly_rides': [5, 8, 2, 12],
        'days_since_last_ride': [1, 3, 10, 0],
        'average_trip_value': [25.0, 30.0, 20.0, 35.0],
        'promotion_acceptance_rate': [0.2, 0.4, 0.1, 0.6]
    })
    conversion_targets = [1, 1, 0, 1]
    test_features = pd.DataFrame({
        'weekly_rides': [2, 0],
        'monthly_rides': [8, 1],
        'days_since_last_ride': [2, 15],
        'average_trip_value': [28.0, 18.0],
        'promotion_acceptance_rate': [0.3, 0.05]
    })
    
    conversion_model = LogisticRegression(random_state=42)
    conversion_model.fit(training_features, conversion_targets)
    
    # Run
    result = predict_booking_probability(conversion_model, test_features)
    
    # Assert
    assert result.shape == (2,)
    assert all(0 <= prob <= 1 for prob in result)
    assert result[0] > result[1]