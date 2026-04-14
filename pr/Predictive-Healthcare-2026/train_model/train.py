
# # ✅ Load dataset
# df = pd.read_csv(
#     'D:\\projectforsem6\\Predictive-Healthcare\\data\\final_150_fully_realistic_datas.csv',
#     sep='\t'
# )
import numpy as np
import pandas as pd
import re
import os
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# # ✅ Load dataset
df = pd.read_csv(
    'D:\\projectforsem6\\Predictive-Healthcare\\data\\medical_training_dataset_5000.csv'
)

# ✅ Clean columns
df.columns = df.columns.str.strip()

# ✅ Remove null & shuffle
df = df.dropna()
df = df.sample(frac=1, random_state=42)

# ✅ Text cleaning
df['Symptoms'] = df['Symptoms'].str.lower()
df['Symptoms'] = df['Symptoms'].apply(lambda x: re.sub(r'[^a-zA-Z, ]', '', x))
df['Symptoms'] = df['Symptoms'].apply(lambda x: x.replace(",", " "))

# ✅ Encode target
le = LabelEncoder()
y = le.fit_transform(df['Type'])

# ✅ Feature
X = df['Symptoms']

print("\nClass Distribution:\n", df['Type'].value_counts())

# ✅ Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42
)

# ✅ Models
models = {
    'LogisticRegression': LogisticRegression(max_iter=1000, C=3, class_weight='balanced'),
    'SVM': LinearSVC(C=2, max_iter=5000),
    'NaiveBayes': MultinomialNB(alpha=0.1)
}

best_score = 0
best_model = None
best_name = None

# ✅ Cross Validation + Best Model Selection
for name, model in models.items():
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('model', model)
    ])
    
    score = cross_val_score(pipe, X, y, cv=7).mean()
    print(f"{name} CV Accuracy: {score:.3f}")
    
    if score > best_score:
        best_score = score
        best_model = pipe
        best_name = name

# ✅ Train Best Model
best_model.fit(X_train, y_train)

# ✅ Predict
y_pred = best_model.predict(X_test)

# ✅ Accuracy
test_accuracy = accuracy_score(y_test, y_pred)

print(f"\n🏆 BEST MODEL: {best_name}")
print(f"📊 Cross Validation Accuracy: {best_score:.3f}")
print(f"🎯 Test Accuracy: {test_accuracy:.3f}")

# ✅ Report
print("\n📋 Classification Report:\n")
print(classification_report(y_test, y_pred))

# ✅ Save
os.makedirs('models', exist_ok=True)
joblib.dump(best_model, 'models/best_model.joblib')
joblib.dump(le, 'models/label_encoder.joblib')

print("\n✅ SUCCESS! Run: streamlit run app.py")