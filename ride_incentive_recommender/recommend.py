from model import predict_booking_probability


def recommend_optimal_incentive(conversion_model, rider_profile):
    baseline_probability = predict_booking_probability(conversion_model, rider_profile.reshape(1, -1))[0]
    
    incentive_impact = {
        'No Incentive': 0.00,
        '10% Discount': 0.10,
        '15% Discount': 0.15,
        '$5 Ride Credit': 0.12
    }
    
    incentive_scores = {
        incentive: min(baseline_probability + lift, 1.0) 
        for incentive, lift in incentive_impact.items()
    }
    
    optimal_incentive = max(incentive_scores, key=incentive_scores.get)
    expected_conversion = incentive_scores[optimal_incentive]
    
    return {
        'recommended_incentive': optimal_incentive,
        'expected_conversion_rate': expected_conversion,
        'all_incentive_scores': incentive_scores
    }