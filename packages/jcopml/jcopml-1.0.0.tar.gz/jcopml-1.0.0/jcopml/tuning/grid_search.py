import numpy as np

rf_params = {
    "rf__n_estimators": [100, 150, 200],
    "rf__max_depth": [20, 50, 80],
    "rf__max_features": [0.3, 0.6, 0.8],
    "rf__min_samples_leaf": [1, 5, 10]
}

knn_params = {
    "knn__n_neighbors": np.arange(1, 31, 2),
    "knn__weights": ['uniform', 'distance'],
    "knn__p": [1, 1.5, 2]
}

svm_params = {
    "svm__gamma": np.logspace(-3, 3, 7),
    "svm__C": np.logspace(-3, 3, 7)
}

svm_imbalance_params = {
    "svm__gamma": np.logspace(-3, 3, 7),
    "svm__C": np.logspace(-3, 3, 7),
    "svm__class_weight": [{0: x, 1: 1-x} for x in [0.01, 0.3, 0.7, 0.99]]
}

xgb_params = {
    "xgb__max_depth": [3, 6, 10],
    "xgb__colsample_bytree": [0.4, 0.6, 0.8],
    "xgb__n_estimators": [100, 150, 200],
    "xgb__subsample": [0.4, 0.6, 0.8],
    "xgb__gamma": [1, 5, 10],
    "xgb__learning_rate": [0.01, 0.1, 1],
    "xgb__reg_alpha": [0.01, 0.1, 10],
    "xgb__reg_lambda": [0.01, 0.1, 10]
}

linreg_params = {
    "linreg__fit_intercept": [True, False]
}

enet_params = {
    "enet__fit_intercept": [True, False],
    "enet__alpha": np.logspace(-3, 2, 6),
    "enet__l1_ratio": [0, 0.25, 0.5, 0.75, 1]
}

logreg_params = {
    "logreg__fit_intercept": [True, False],
    "logreg__C": np.logspace(-3, 3, 7)
}

logreg_imbalance_params = {
    "logreg__fit_intercept": [True, False],
    "logreg__C": np.logspace(-3, 3, 7),
    "logreg__class_weight": [{0: x, 1: 1-x} for x in [0.01, 0.3, 0.7, 0.99]]
}

poly_params = {
    "poly__degree": [1, 2, 3],
    "poly__interaction_only": [True, False]
}

prep_poly_params = {
    "prep__numeric__poly__degree": [1, 2, 3],
    "prep__numeric__poly__interaction_only": [True, False]
}

rf_poly_params = {**poly_params, **rf_params}

knn_poly_params = {**poly_params, **knn_params}

svm_poly_params = {**poly_params, **svm_params}

svm_imbalance_poly_params = {**poly_params, **svm_imbalance_params}

xgb_poly_params = {**poly_params, **xgb_params}

linreg_poly_params = {**poly_params, **linreg_params}

enet_poly_params = {**poly_params, **enet_params}

logreg_poly_params = {**poly_params, **logreg_params}

logreg_imbalance_poly_params = {**poly_params, **logreg_imbalance_params}


rf_prep_poly_params = {**prep_poly_params, **rf_params}

knn_prep_poly_params = {**prep_poly_params, **knn_params}

svm_prep_poly_params = {**prep_poly_params, **svm_params}

svm_prep_imbalance_poly_params = {**prep_poly_params, **svm_imbalance_params}

xgb_prep_poly_params = {**prep_poly_params, **xgb_params}

linreg_prep_poly_params = {**prep_poly_params, **linreg_params}

enet_prep_poly_params = {**prep_poly_params, **enet_params}

logreg_prep_imbalance_poly_params = {**prep_poly_params, **logreg_imbalance_params}
