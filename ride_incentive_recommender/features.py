def prepare_features(riders_df):
    feature_columns = ['weekly_rides', 'monthly_rides', 'days_since_last_ride', 
                      'average_trip_value', 'promotion_acceptance_rate']
    rider_features = riders_df[feature_columns].copy()
    conversion_target = riders_df['will_book_ride'].copy()
    return rider_features, conversion_target