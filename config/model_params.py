from scipy.stats import uniform, randint


LIGHTGBM_PARAMS = {
    'n_estimators': randint(100, 500),
    'learning_rate': uniform(0.01, 0.2),
    'num_leaves': randint(20, 1100),
    'max_depth': randint(5, 50),
    'boosting_type': ['gbdt', 'dart', 'goss'],
}

RANDOM_SEARCH_PARAMS = {
    'n_iter': 4,
    'cv':2, # should be greater than 1
    'n_jobs': -1, # use all cpu
    'verbose': 2,
    'random_state': 42,
    'scoring': 'accuracy'
}