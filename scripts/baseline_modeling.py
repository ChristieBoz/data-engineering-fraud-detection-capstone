# import libraries

import pandas as pd
import numpy as np
import psycopg2
import sklearn
  
from sqlalchemy import create_engine
from sqlalchemy import text

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, classification_report
  

def baseline_modeling():

	## create database engine using postgresql connection string:
	USERNAME = "postgres"
	PASSWORD = "*******"
	HOST = "localhost"
	PORT = "5432"
	DB_NAME = "fraud_capstone"
  
	engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")
  
	#loading baseline (cleaned transactions)
	query = """
	SELECT * FROM staging_schema.cleaned_transactions
	"""
  
	df = pd.read_sql(query, engine)
  
	#seperate the features from the target
	x = df.drop(columns=["class"])
	y = df["class"]
  
	#split the data
	x_train, x_test, y_train, y_test = train_test_split(
		x,
      	y,
      	test_size=0.2,
      	stratify=y,
      	random_state=42
	)
  
	#verify
	print("Training fraud ratio:", y_train.mean())
	print("Testing fraud ratio:", y_test.mean())
  
	#create scaler
	scaler = StandardScaler()
  
	#fit scaler to training
	x_train_scaled = scaler.fit_transform(x_train)
  
	#fit scaler to testing
	x_test_scaled = scaler.transform(x_test)
  
	#verify scaling
	print(x_train_scaled.mean())
	print(x_train_scaled.std())
  
	#initialization
	log_model = LogisticRegression(
      class_weight="balanced",
    	  max_iter=1000,
    	  random_state=42
	)
  
	#train the model
	log_model.fit(x_train_scaled, y_train)
  
  
	##prediction generation
	y_pred_log = log_model.predict(x_test_scaled)
  
	print(y_pred_log)
  
	y_prob_log = log_model.predict_proba(x_test_scaled)[:,1]
  
	print(y_prob_log)
  
	print(classification_report(y_test, y_pred_log))
	print("ROC AUC:", roc_auc_score(y_test, y_prob_log))
  
	#view results
	precision = precision_score(y_test, y_pred_log)
	recall = recall_score(y_test, y_pred_log)
	f1 = f1_score(y_test, y_pred_log)
	roc = roc_auc_score(y_test, y_prob_log)
  
	print("Precision:", precision)
	print("Recall:", recall)
	print("F1:", f1)
	print("ROC AUC:", roc)
  
	#random forest
	rf_model = RandomForestClassifier(
    	  n_estimators=100,
   	   class_weight="balanced",
   	   random_state=42,
      n_jobs=-1
	)
  
	#train model
	rf_model.fit(x_train, y_train)
    
	#prediction generation
	y_pred_rf = rf_model.predict(x_test)
  
	#probability of fraud
	y_prob_rf = rf_model.predict_proba(x_test)[:,1]
  
	#model eval
	print(classification_report(y_test, y_pred_rf))
	print("ROC AUC:", roc_auc_score(y_test, y_prob_rf))
  
	#metrics
	rf_precision = precision_score(y_test, y_pred_rf)
	rf_recall = recall_score(y_test, y_pred_rf)
	rf_f1 = f1_score(y_test, y_pred_rf)
	rf_roc = roc_auc_score(y_test, y_prob_rf)
  
	print("Precision:", rf_precision)
	print("Recall:", rf_recall)
	print("F1:", rf_f1)
	print("ROC AUC:", rf_roc)
  
	#create csv of results
	results_baseline = pd.DataFrame({"Model": ["Baseline Logistic", "Baseline Random Forest"],
   		"Precision": [precision, rf_precision], "Recall": [recall, rf_recall],"F1": [f1, rf_f1],
   		"ROC_AUC": [roc, rf_roc]
	})
  
	results_baseline.to_csv("baseline_results.csv", index=False)
