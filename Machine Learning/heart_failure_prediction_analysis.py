# Dataset from Kaggle: https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction

import pandas as pd

df = pd.read_csv("heart.csv.xls")

# check quality of dataset
df.describe()
df.info()
df.isnull().any()

df.columns # identify Y

X = df.drop(columns = "HeartDisease")
Y = df["HeartDisease"]

df.head() # check updated df

# Data Visualisation
df2 = df.loc[:,['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 
                'MaxHR', 'Oldpeak', 'HeartDisease']]
df2.boxplot(figsize=(30,20))
df2.hist(figsize = (20,20))

# Categorical data visualisation using matplotlib
import matplotlib.pyplot as plt
import numpy as np

df.groupby('Sex').size().plot(kind='pie', autopct='%1.1f%%')
plt.ylabel("Sex")

df.groupby('ChestPainType').size().plot(kind='pie', autopct='%1.1f%%')
plt.ylabel('Chest Pain Type')

df.groupby('RestingECG').size().plot(kind='pie', autopct='%1.1f%%')
plt.ylabel('Resting ECG')

df.groupby('ExerciseAngina').size().plot(kind='pie', autopct='%1.1f%%')
plt.ylabel('Exercise Angina')

# Finding out if there is any obvious correlation between heart disease and symptoms
import seaborn as sns
sns.heatmap(df2.corr())

sns.catplot(data=df2, x="HeartDisease", y="Age", kind='violin')
sns.catplot(data=df2, x="HeartDisease", y="Cholesterol", kind="violin")
sns.catplot(data=df2, x="HeartDisease", y="RestingBP", kind='violin')
sns.catplot(data=df2, x="HeartDisease", y="FastingBS", kind='violin')
sns.catplot(data=df2, x="HeartDisease", y="MaxHR", kind='violin')
sns.catplot(data=df2, x="HeartDisease", y="Oldpeak", kind='violin')

plt.scatter(df["HeartDisease"], df["Cholesterol"])
plt.title("Cholesterol and Heart Disease Analysis")
plt.xlabel("Heart Disease")
plt.ylabel("Cholesterol Level")

plt.scatter(df["HeartDisease"], df["Age"])
plt.title("Cholesterol and Heart Disease Analysis")
plt.xlabel("Heart Disease")
plt.ylabel("Cholesterol Level")

# Creating dummy variables for categorical Y
dummyS = pd.get_dummies(df["Sex"])
dummyC = pd.get_dummies(df['ChestPainType'])
dummyE = pd.get_dummies(df["RestingECG"])
dummyST = pd.get_dummies(df["ST_Slope"])
dummyA = pd.get_dummies(df["ExerciseAngina"])

df3 = df.merge(dummyS, left_index=True, right_index=True)
df3 = df3.drop(columns="Sex")
df3 = df3.merge(dummyC, left_index=True,right_index=True)
df3 = df3.drop(columns="ChestPainType")
df3 = df3.merge(dummyE, left_index=True, right_index=True)
df3 = df3.drop(columns="RestingECG")
df3 = df3.merge(dummyST, left_index=True, right_index=True)
df3 = df3.drop(columns="ST_Slope")
df3 = df3.merge(dummyA, left_index=True, right_index=True)
df3 = df3.drop(columns="ExerciseAngina")

# Oversampling with SMOTE
df3["HeartDisease"].value_counts() # checking if oversampling is required

X = df3.drop(columns="HeartDisease")
Y = df3["HeartDisease"]

# Splitting training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,random_state=1)

Y_train.value_counts()

from imblearn.over_sampling import SMOTE

Y_train.value_counts() # checking if Y is balanced

from sklearn import linear_model

model = linear_model.LogisticRegression(random_state=1)   
model.fit(X_train, Y_train)

from sklearn.metrics import confusion_matrix

pred = model.predict(X_test)
cm = confusion_matrix(Y_test,pred)
print("Accuracy is ", (cm[0,0] + cm[1,1])/(sum(sum(cm))))    # Logistic Regression model

from sklearn.metrics import plot_roc_curve

plot_roc_curve(model, X_test, Y_test)

from sklearn.metrics import plot_precision_recall_curve
plot_precision_recall_curve(model, X_test, Y_test)

from sklearn import tree

model_tree = tree.DecisionTreeClassifier(random_state=1)
model_tree.fit(X_train, Y_train)
pred = model_tree.predict(X_test)
cm = confusion_matrix(Y_test, pred)
print("Accuracy is ", (cm[0,0] + cm[1,1])/(sum(sum(cm))))     # Decision Tree model

from sklearn import ensemble

modelE = ensemble.RandomForestClassifier(random_state=1)
modelE.fit(X_train, Y_train)
pred = modelE.predict(X_test)
cm = confusion_matrix(Y_test, pred)
print("Accuracy is ", (cm[0,0] + cm[1,1])/(sum(sum(cm))))     # Random Forest model

modelG = ensemble.GradientBoostingClassifier(random_state=1)
modelG.fit(X_train, Y_train)
pred = modelG.predict(X_test)
cm = confusion_matrix(Y_test, pred)
print("Accuracy is ", (cm[0,0] + cm[1,1])/(sum(sum(cm))))    # Gradient Boosting model

from sklearn import neural_network

modelN = neural_network.MLPClassifier(random_state=1)
modelN.fit(X_train, Y_train)
pred = modelN.predict(X_test)
cm = confusion_matrix(Y_test, pred)
print("Accuracy is ", (cm[0,0] + cm[1,1])/(sum(sum(cm))))   # Neural Network model
