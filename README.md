
# Telecom Customer Churn Prediction System

## Overview
This project implements an end-to-end machine learning pipeline to predict telecom customer churn. The system identifies customers who are likely to leave a telecom service provider, enabling businesses to implement retention strategies.

The project follows a production-style MLOps architecture including data ingestion, validation, transformation, model training, evaluation, and deployment.

---

## Features

- End-to-end machine learning pipeline
- Class imbalance handling using SMOTE
- Experiment tracking with MLflow
- Ensemble models (Random Forest, XGBoost)
- Model registry using AWS S3
- FastAPI prediction API
- Docker containerization
- CI/CD pipeline using GitHub Actions
- Deployment on AWS EC2

---

## Project Architecture

Data Source → Data Ingestion → Data Validation → Data Transformation → Model Training → Model Evaluation → Model Registry → FastAPI → Docker → AWS EC2

---

## Model Evaluation

Models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

The best performing model was automatically selected and deployed.

---

## Technologies Used

- Python
- Scikit-learn
- XGBoost
- MLflow
- MongoDB Atlas
- FastAPI
- Docker
- AWS (EC2, S3, ECR)
- GitHub Actions

---

## Deployment

The application is deployed using Docker containers on AWS EC2 with CI/CD automation.

---

## Future Improvements

- Add model monitoring
- Implement data drift detection
- Add feature store integration
