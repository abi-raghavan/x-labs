import pandas as pd


def users_by_variant(df):
    return df.groupby('variant').size().reset_index(name='count')


def conversion_rate(df):
    return df.groupby('variant')['converted'].agg(['sum', 'count']).reset_index()


def revenue_per_user(df):
    return df.groupby('variant')['revenue'].mean().reset_index()


def absolute_lift(df):
    conv_rates = df.groupby('variant')['converted'].mean()
    return conv_rates.get('variant', 0) - conv_rates.get('control', 0)


def relative_lift(df):
    conv_rates = df.groupby('variant')['converted'].mean()
    control_rate = conv_rates.get('control', 0)
    variant_rate = conv_rates.get('variant', 0)
    return (variant_rate - control_rate) / control_rate if control_rate > 0 else 0