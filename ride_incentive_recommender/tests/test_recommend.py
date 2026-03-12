import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
from recommend import recommend_optimal_incentive


def test_recommend_optimal_incentive():
    # Fixtures
    training_features = pd.DataFrame({
        'weekly_rides': [1, 2, 0, 3],
        'monthly_rides': [5, 8, 2, 12],
        'days_since_last_ride': [1, 3, 10, 0],
        'average_trip_value': [25.0, 30.0, 20.0, 35.0],
        'promotion_acceptance_rate': [0.2, 0.4, 0.1, 0.6]
    })
    conversion_targets = [1, 1, 0, 1]
    rider_profile = np.array([2, 8, 2, 28.0, 0.3])
    
    conversion_model = LogisticRegression(random_state=42)
    conversion_model.fit(training_features, conversion_targets)
    
    # Run
    result = recommend_optimal_incentive(conversion_model, rider_profile)
    
    # Assert
    assert list(result.keys()) == ['recommended_incentive', 'expected_conversion_rate', 'all_incentive_scores']
    assert result['recommended_incentive'] in ['No Incentive', '10% Discount', '15% Discount', '$5 Ride Credit']
    assert 0 <= result['expected_conversion_rate'] <= 1
    assert len(result['all_incentive_scores']) == 4
    assert result['all_incentive_scores']['10% Discount'] > result['all_incentive_scores']['No Incentive']