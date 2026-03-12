import pandas as pd
import numpy as np


def generate_users(num_riders):
    np.random.seed(42)
    
    major_cities = ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Boston']
    
    rider_data = {
        'rider_id': range(1, num_riders + 1),
        'city': np.random.choice(major_cities, num_riders),
        'weekly_rides': np.random.poisson(2, num_riders),
        'monthly_rides': np.random.poisson(8, num_riders),
        'days_since_last_ride': np.random.exponential(5, num_riders).astype(int),
        'average_trip_value': np.random.normal(25, 8, num_riders).round(2),
        'promotion_acceptance_rate': np.random.beta(2, 5, num_riders).round(3)
    }
    
    riders_df = pd.DataFrame(rider_data)
    
    # Calculate conversion probability based on rider engagement patterns
    engagement_score = (
        riders_df['monthly_rides'] * 0.1 +
        riders_df['promotion_acceptance_rate'] * 0.3 +
        1 / (riders_df['days_since_last_ride'] + 1) * 0.4 +
        (riders_df['average_trip_value'] < 30).astype(int) * 0.2
    )
    
    conversion_probability = 1 / (1 + np.exp(-(engagement_score - 0.5) * 3))
    riders_df['will_book_ride'] = np.random.binomial(1, conversion_probability, num_riders)
    
    return riders_df