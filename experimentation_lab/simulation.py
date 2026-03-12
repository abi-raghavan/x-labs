import pandas as pd
import numpy as np
from assignment import assign_variant


def simulate_users(n_users, experiment_id="default_exp", split=0.5):
    np.random.seed(42)
    
    user_ids = [f"user_{i}" for i in range(n_users)]
    variants = [assign_variant(user_id, experiment_id, split) for user_id in user_ids]
    
    conversions = []
    revenues = []
    
    for variant in variants:
        if variant == "control":
            converted = np.random.random() < 0.10
            revenue = np.random.normal(25.0, 5.0) if converted else 0.0
        else:
            converted = np.random.random() < 0.12
            revenue = np.random.normal(30.0, 6.0) if converted else 0.0
        
        conversions.append(converted)
        revenues.append(max(0, revenue))
    
    return pd.DataFrame({
        'user_id': user_ids,
        'variant': variants,
        'converted': conversions,
        'revenue': revenues
    })