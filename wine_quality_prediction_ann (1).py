# -*- coding: utf-8 -*-
"""wine quality prediction  ANN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ktnX-AFWK0RjpP-Z0MrivWq5bAtNzqGf
"""

!pip install matplotlib tensorflow

!pip install graphviz

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
path = r'/content/drive/MyDrive/winequality (1).csv'
df = pd.read_csv(path)

"""Explore Data"""

df.head(5)

df.shape

"""Information about all the columns in the Dataset"""

df.info()

df.describe()

"""Data Cleaning

1.Locate Missing Data
"""

df.isnull()

df.isnull().sum()

df.duplicated()

df.drop_duplicates()

max_target_value = df['TARGET'].max()
print("Maximum target value:", max_target_value)

min_target_value = df['TARGET'].min()
print("Minimum target value:", min_target_value)

# Data
target_counts = df['TARGET'].value_counts().sort_index()

# Create bar plot
plt.figure(figsize=(8, 6))
target_counts.plot(kind='bar', color='skyblue')
plt.xlabel('Target Value')
plt.ylabel('Count')
plt.title('Distribution of Target Variable')
plt.xticks(rotation=0)
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Increase the size of the heatmap
plt.figure(figsize=(10, 10))

# Plot the heatmap with annotations
sns.heatmap(df.corr(), annot=True, cmap="Blues")

# Show the plot
plt.show()

# Visualizing Missing Data

missing_values = df.isnull().sum()
missing_values_percentage = (missing_values / len(df)) * 100

plt.figure(figsize=(12, 6))
missing_values_percentage.plot(kind='bar')
plt.xlabel('Features')
plt.ylabel('Percentage of Missing Values')
plt.title('Percentage of Missing Data in Each Column')
plt.xticks(rotation=45)
plt.show()

# Box plot for all numerical columns to detect outlier
plt.figure(figsize=(12, 6))
df.boxplot()
plt.title('All Numerical Features')
plt.xticks(rotation=45)
plt.show()

# Calculate Q1, Q3, and IQR for 'free sulfur dioxide'
Q1_free = df['free sulfur dioxide'].quantile(0.25)
Q3_free = df['free sulfur dioxide'].quantile(0.75)
IQR_free = Q3_free - Q1_free
# Calculate Q1, Q3, and IQR for 'total sulfur dioxide'
Q1_total = df['total sulfur dioxide'].quantile(0.25)
Q3_total = df['total sulfur dioxide'].quantile(0.75)
IQR_total = Q3_total - Q1_total

# Define bounds for 'free sulfur dioxide'
lower_free = Q1_free - 1.5 * IQR_free
upper_free = Q3_free + 1.5 * IQR_free

# Define bounds for 'total sulfur dioxide'
lower_total = Q1_total - 1.5 * IQR_total
upper_total = Q3_total + 1.5 * IQR_total

# Filter out the outliers from the dataset
df_filtered = df[(df['free sulfur dioxide'] >= lower_free) & (df['free sulfur dioxide'] <= upper_free) &
                 (df['total sulfur dioxide'] >= lower_total) & (df['total sulfur dioxide'] <= upper_total)]

# Check if outliers have been removed
if df.shape[0] != df_filtered.shape[0]:
    print("Outliers have been removed.")
    print("Original shape:", df.shape)
    print("Shape after removal:", df_filtered.shape)
else:
    print("No outliers were removed.")

# Optionally, you can also check the specific rows that were removed
removed_rows = df[~df.index.isin(df_filtered.index)]
print("Removed rows:", removed_rows)

import matplotlib.pyplot as plt

# Plot histograms of 'free sulfur dioxide' before and after filtering
plt.figure(figsize=(10, 6))
plt.hist(df['free sulfur dioxide'], bins=30, alpha=0.5, color='skyblue', label='Original')
plt.hist(df_filtered['free sulfur dioxide'], bins=30, alpha=0.5, color='orange', label='Filtered')
plt.xlabel('Free Sulfur Dioxide')
plt.ylabel('Frequency')
plt.title('Distribution of Free Sulfur Dioxide')
plt.legend()
plt.show()

# Plot histograms of 'total sulfur dioxide' before and after filtering
plt.figure(figsize=(10, 6))
plt.hist(df['total sulfur dioxide'], bins=30, alpha=0.5, color='skyblue', label='Original')
plt.hist(df_filtered['total sulfur dioxide'], bins=30, alpha=0.5, color='orange', label='Filtered')
plt.xlabel('Total Sulfur Dioxide')
plt.ylabel('Frequency')
plt.title('Distribution of Total Sulfur Dioxide')
plt.legend()
plt.show()

"""features selection"""

# Create a copy of the filtered DataFrame
df_filtered = df_filtered.copy()

# Create Classification version of target variable using .loc
df_filtered.loc[:, 'goodquality'] = df_filtered['TARGET'].apply(lambda x: 1 if x >= 7 else 0)

# Separate feature variables and target variable
X = df_filtered.drop(['TARGET', 'goodquality'], axis=1)
Y = df_filtered['goodquality']

# See proportion of good vs bad wines
print(df_filtered['goodquality'].value_counts())

"""Feature Importance"""

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()

from sklearn.ensemble import ExtraTreesClassifier
classifiern = ExtraTreesClassifier()
classifiern.fit(X,Y)
score = classifiern.feature_importances_
print(score)

"""Splitting Dataset"""

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3,random_state=7)

from sklearn.ensemble import RandomForestClassifier
model2 = RandomForestClassifier(random_state=1)
model2.fit(X_train, Y_train)
y_pred2 = model2.predict(X_test)

from sklearn.metrics import accuracy_score
print("Accuracy Score:",accuracy_score(Y_test,y_pred2))

"""Transforming quality to categorical data"""



import tensorflow as tf
Y_train_cat = tf.keras.utils.to_categorical(Y_train, 6) # Y train categorical data  convert to  one hot encode formate and 6 is a length of vector
Y_test_cat = tf.keras.utils.to_categorical(Y_test, 6)

"""Scaling features"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()     # creat sc object

X_train = sc.fit_transform(X_train)  # fit transformmethod used in training data scalling
X_test = sc.transform(X_test)   # fit transformed method used in testing data scaling

"""Machine learning modeling

Artificial neural network
"""

import tensorflow as tf

# Create a Sequential model
model = tf.keras.models.Sequential()

# Add layers to the model
# Example layers:
model.add(tf.keras.layers.Dense(units=16, activation='relu', input_shape=(11,)))  # Adjust input_shape according to your data   # hidden layer   unit 16 and  input layer unit 11
model.add(tf.keras.layers.Dense(units=8, activation='relu'))
model.add(tf.keras.layers.Dense(units=6, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()

# X_train represt
history = model.fit(X_train, Y_train_cat, batch_size=32, epochs=150, validation_data=(X_test, Y_test_cat))

import matplotlib.pyplot as plt

# Get training and validation loss from the history object
training_loss = history.history['loss']
validation_loss = history.history['val_loss']

# Get training and validation accuracy from the history object
training_accuracy = history.history['accuracy']
validation_accuracy = history.history['val_accuracy']

# Plot training and validation loss
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(training_loss, label='Training Loss')
plt.plot(validation_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plot training and validation accuracy
plt.subplot(1, 2, 2)
plt.plot(training_accuracy, label='Training Accuracy')
plt.plot(validation_accuracy, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()