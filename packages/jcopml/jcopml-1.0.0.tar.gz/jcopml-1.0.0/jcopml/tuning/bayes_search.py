from skopt.space import Real, Integer, Categorical

rf_params = {
    "rf__n_estimators": Integer(100, 200),
    "rf__max_depth": Integer(20, 80),
    "rf__max_features": Real(0.1, 1),
    "rf__min_samples_leaf": Integer(1, 20)
}

knn_params = {
    "knn__n_neighbors": Integer(1, 40),
    "knn__weights": Categorical(['uniform', 'distance']),
    "knn__p": Real(1, 2)
}

svm_params = {
    "svm__gamma": Real(0.001, 1000, prior='log-uniform'),
    "svm__C": Real(0.001, 1000, prior='log-uniform')
}

xgb_params = {
    "xgb__max_depth": Integer(1, 10),
    "xgb__learning_rate": Real(0.01, 1, prior='log-uniform'),
    "xgb__n_estimators": Integer(100, 200),
    "xgb__subsample": Real(0.3, 0.8),
    "xgb__gamma": Integer(1, 10),
    "xgb__colsample_bytree": Real(0.1, 1),
    "xgb__reg_alpha": Real(0.001, 10, prior='log-uniform'),
    "xgb__reg_lambda": Real(0.001, 10, prior='log-uniform')
}

linreg_params = {
    "linreg__fit_intercept": Categorical([True, False])
}

enet_params = {
    "enet__fit_intercept": Categorical([True, False]),
    "enet__alpha": Real(0.0001, 100, prior='log-uniform'),
    "enet__l1_ratio": Real(0, 1)
}

logreg_params = {
    "logreg__fit_intercept": Categorical([True, False]),
    "logreg__C": Real(0.001, 1000, prior='log-uniform')
}

poly_params = {
    "poly__degree": Integer(1, 3),
    "poly__interaction_only": Categorical([True, False])
}

prep_poly_params = {
    "prep__numeric__poly__degree": Integer(1, 3),
    "prep__numeric__poly__interaction_only": Categorical([True, False])
}

rf_poly_params = {**poly_params, **rf_params}

knn_poly_params = {**poly_params, **knn_params}

svm_poly_params = {**poly_params, **svm_params}

xgb_poly_params = {**poly_params, **xgb_params}

linreg_poly_params = {**poly_params, **linreg_params}

enet_poly_params = {**poly_params, **enet_params}

logreg_poly_params = {**poly_params, **logreg_params}


rf_prep_poly_params = {**prep_poly_params, **rf_params}

knn_prep_poly_params = {**prep_poly_params, **knn_params}

svm_prep_poly_params = {**prep_poly_params, **svm_params}

xgb_prep_poly_params = {**prep_poly_params, **xgb_params}

linreg_prep_poly_params = {**prep_poly_params, **linreg_params}

enet_prep_poly_params = {**prep_poly_params, **enet_params}

logreg_prep_poly_params = {**prep_poly_params, **logreg_params}