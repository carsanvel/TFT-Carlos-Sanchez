import pandas as pd
import sklearn.feature_selection
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.metrics import roc_auc_score

variables_host = pd.read_excel('datos_host/variables.xlsx')
variables_infor = pd.read_excel('datos_host/variables.xlsx')
variables = [variables_host, variables_infor]

for i in range(len(variables)):

    variables[i].drop('NOMBRE', inplace=True, axis=1)
    y = variables[i].iloc[:,0]
    x = variables[i].iloc[:,1:48]

    # Calculamos las mejore según F de ANOVA
    best_features = sklearn.feature_selection.SelectKBest(score_func=sklearn.feature_selection.f_classif, k=10)
    fit = best_features.fit(x, y)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(x.columns)
    featurescores = pd.concat([dfcolumns, dfscores], axis=1)
    featurescores.columns = ['Variable', 'Scores']
    print(featurescores.nlargest(48, 'Scores'))

    # Calculamos las mejores segun ExtraTrees
    model = ExtraTreesClassifier()
    model.fit(x, y)
    feat_importances = pd.Series(model.feature_importances_, index=x.columns)
    print(feat_importances.nlargest(48))

    # Calculamos las mejores segun RandomForest
    model = RandomForestClassifier()
    model.fit(x, y)
    feat_importances = pd.Series(model.feature_importances_, index=x.columns)
    print(feat_importances.nlargest(48))

    # Calculamos el mejor modelo con RFECV
    model = RFECV(RandomForestClassifier(), scoring='roc_auc')
    model.fit(x, y)
    print(model.ranking_)