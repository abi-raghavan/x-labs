from sklearn.linear_model import LogisticRegression


def train_conversion_model(rider_features, conversion_target):
    conversion_model = LogisticRegression()
    conversion_model.fit(rider_features, conversion_target)
    return conversion_model


def predict_booking_probability(conversion_model, rider_features):
    return conversion_model.predict_proba(rider_features)[:, 1]