import subprocess
try:
    import lightgbm as lgb
except ImportError:
    subprocess.check_call(['pip', 'install', 'lightgbm'])
    import lightgbm as lgb

import pandas as pd
import numpy as np
import json
import os
import sys
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import torch

# Check for GPU availability
if torch.cuda.is_available():
    device = 'GPU'
    print("GPU is available. Using GPU for training.")
else:
    device = 'CPU'
    print("GPU not available. Using CPU for training.")

# Load datasets
train = pd.read_csv('train.csv', encoding='utf-8')
test = pd.read_csv('test.csv', encoding='utf-8')

# Combine train and test for consistent preprocessing
test['Transported'] = np.nan
data = pd.concat([train, test], sort=False).reset_index(drop=True)

# Fill missing values
data['Age'].fillna(data['Age'].median(), inplace=True)
data['CryoSleep'].fillna(False, inplace=True)
data['VIP'].fillna(False, inplace=True)
data['RoomService'].fillna(0, inplace=True)
data['FoodCourt'].fillna(0, inplace=True)
data['ShoppingMall'].fillna(0, inplace=True)
data['Spa'].fillna(0, inplace=True)
data['VRDeck'].fillna(0, inplace=True)
data['Cabin'].fillna('Unknown/0/Unknown', inplace=True)
data['HomePlanet'].fillna('Unknown', inplace=True)
data['Destination'].fillna('Unknown', inplace=True)

# Feature Engineering: Parse Cabin
data['Deck'] = data['Cabin'].apply(lambda x: x.split('/')[0] if '/' in x else 'Unknown')
data['Cabin_Number'] = data['Cabin'].apply(lambda x: int(x.split('/')[1]) if '/' in x and x.split('/')[1].isdigit() else 0)
data['Cabin_Side'] = data['Cabin'].apply(lambda x: x.split('/')[2] if '/' in x else 'Unknown')

# Feature Engineering: Extract Group from PassengerId
data['Group'] = data['PassengerId'].apply(lambda x: x.split('_')[0])
data['PassengerNum'] = data['PassengerId'].apply(lambda x: int(x.split('_')[1]))

# Convert boolean columns to int
bool_cols = ['CryoSleep', 'VIP']
for col in bool_cols:
    data[col] = data[col].astype(int)

# Label Encoding for categorical variables
categorical_cols = ['HomePlanet', 'Destination', 'Deck', 'Cabin_Side', 'Group']
le = LabelEncoder()
for col in categorical_cols:
    data[col] = le.fit_transform(data[col])

# Drop unnecessary columns
data.drop(['PassengerId', 'Name', 'Cabin'], axis=1, inplace=True)

# Split back into train and test
train = data[data['Transported'].notnull()]
test = data[data['Transported'].isnull()].drop(['Transported'], axis=1)

# Define features and target
X = train.drop('Transported', axis=1)
y = train['Transported'].astype(int)

# Split into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Create LightGBM datasets
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_val, y_val, reference=lgb_train)

# Set LightGBM parameters
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': 'binary_logloss',
    'verbosity': -1,
    'seed': 42,
    'force_row_wise': True
}

# Use GPU if available
if device == 'GPU':
    params['device'] = 'gpu'
    params['gpu_platform_id'] = 0
    params['gpu_device_id'] = 0

# Initialize progress report
progress_report = {
    'device': device,
    'cross_val_accuracy': [],
    'validation_accuracy': 0,
    'test_accuracy': 0
}

# Cross-validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []
print("Starting cross-validation...")
for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
    X_tr, X_va = X.iloc[train_idx], X.iloc[val_idx]
    y_tr, y_va = y.iloc[train_idx], y.iloc[val_idx]
    lgb_tr = lgb.Dataset(X_tr, y_tr)
    lgb_va = lgb.Dataset(X_va, y_va, reference=lgb_tr)
    gbm = lgb.train(params,
                    lgb_tr,
                    num_boost_round=1000,
                    valid_sets=[lgb_tr, lgb_va],
                    verbose_eval=100)
    y_pred = gbm.predict(X_va, num_iteration=gbm.best_iteration)
    y_pred_binary = [1 if x >= 0.5 else 0 for x in y_pred]
    acc = accuracy_score(y_va, y_pred_binary)
    cv_scores.append(acc)
    progress_report['cross_val_accuracy'].append(acc)
    print(f"Fold {fold} Accuracy: {acc:.4f}")

# Train final model on all training data
print("Training final model on all training data...")
gbm_final = lgb.train(params,
                      lgb_train,
                      num_boost_round=gbm.best_iteration)

# Validate on validation set
y_val_pred = gbm_final.predict(X_val, num_iteration=gbm_final.best_iteration)
y_val_pred_binary = [1 if x >= 0.5 else 0 for x in y_val_pred]
val_accuracy = accuracy_score(y_val, y_val_pred_binary)
progress_report['validation_accuracy'] = val_accuracy
print(f"Validation Accuracy: {val_accuracy:.4f}")

# Make predictions on test set
test_pred = gbm_final.predict(test, num_iteration=gbm_final.best_iteration)
test_pred_binary = [bool(x >= 0.5) for x in test_pred]

# Prepare submission
submission = pd.DataFrame({
    'PassengerId': pd.read_csv('test.csv', encoding='utf-8')['PassengerId'],
    'Transported': test_pred_binary
})
submission.to_csv('submission.csv', index=False, encoding='utf-8')
print("Submission file saved as submission.csv")

# Save progress report
progress_report['cross_val_accuracy_mean'] = np.mean(cv_scores)
progress_report['cross_val_accuracy_std'] = np.std(cv_scores)
progress_report['test_accuracy'] = val_accuracy

with open('progress_report.json', 'w', encoding='utf-8') as f:
    json.dump(progress_report, f, ensure_ascii=False, indent=4)
print("Progress report saved as progress_report.json")