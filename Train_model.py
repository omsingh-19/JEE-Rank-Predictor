import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split , GridSearchCV
from sklearn.preprocessing import StandardScaler , OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline , make_pipeline
from sklearn.compose import ColumnTransformer , TransformedTargetRegressor
from sklearn.metrics import mean_squared_error
import joblib

#Loading Data
df=pd.read_csv("Data/JEE_mains_dataset.csv")

X=df.drop(columns=['Predicted_Rank',"JEE_Percentile"])
y=df[['Predicted_Rank',"JEE_Percentile"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


#Preprocessing
numerical_cols = ["Maths_Marks","Physics_Marks","Chemistry_Marks","Average_Mock_Test_Marks"]
categorical_cols = ['Shift_Difficulty']

num_preprocessor=Pipeline(steps=[('scaler',StandardScaler())])
cat_preprocessor = Pipeline(steps=[('encoder',OneHotEncoder(handle_unknown="ignore"))])

preprocessor=ColumnTransformer([
    ("numerical_data",num_preprocessor,numerical_cols),
    ('categorical_data',cat_preprocessor,categorical_cols)
])


#Base Pipeline
base_pipeline=make_pipeline(preprocessor,RandomForestRegressor(random_state=42))


#Target Scaling
model=TransformedTargetRegressor(
    regressor=base_pipeline,
    transformer=StandardScaler()
)


#Grid Search
parameters = {
    "regressor__randomforestregressor__n_estimators":[100,200,300],
    "regressor__randomforestregressor__max_depth":[5,10,15],
    "regressor__randomforestregressor__max_features":["sqrt","log2",None]
}

cv_pipeline = GridSearchCV(
    model,
    parameters,
    cv=5,
    scoring="neg_mean_squared_error",
    n_jobs=-1
)
cv_pipeline.fit(X_train, y_train)


#Evaluation
y_pred = cv_pipeline.predict(X_test)

rmse_percentile = np.sqrt(mean_squared_error(
    y_test["JEE_Percentile"], y_pred[:,1]
))

rmse_rank = np.sqrt(mean_squared_error(
    y_test["Predicted_Rank"], y_pred[:,0]
))

print(rmse_percentile, rmse_rank)


#Saving model
joblib.dump(cv_pipeline,"model/Final_Model.pkl")