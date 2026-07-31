<div align="center">

# ❤️ CardioPredict AI

A machine learning web application that predicts the likelihood of heart failure using clinical patient data.

<p>
  <a href="https://heart-failure-predict-x9pu.onrender.com" target="_blank">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Visit%20Application-red?style=for-the-badge" alt="Live Demo">
  </a>
</p>

</div>

---

## About

CardioPredict AI is a Flask-based web application built around a Random Forest model trained on the Heart Failure Clinical Records dataset. The goal of this project was to take a machine learning model beyond a Jupyter notebook and turn it into a complete, deployable web application with a clean user interface.

Users can enter clinical parameters such as age, ejection fraction, serum creatinine, blood pressure, and other medical indicators to receive an instant prediction indicating whether the patient is at a higher or lower risk of heart failure.

> **Note:** This project is intended for educational purposes only and should not be used as a medical diagnostic tool.

---

## Live Demo

🔗 **https://heart-failure-predict-x9pu.onrender.com**

---

## Features

- Predicts heart failure risk using a trained Random Forest model
- Simple and responsive web interface
- Instant prediction results
- Flask backend
- Responsive design for desktop and mobile
- Fully deployed on Render

---

## Tech Stack

**Frontend**

- HTML
- CSS
- JavaScript

**Backend**

- Flask
- Gunicorn

**Machine Learning**

- Scikit-learn
- Pandas
- NumPy

**Deployment**

- Render
- Docker

---

## Model Inputs

The prediction is generated using the following clinical features:

- Age
- Anaemia
- Creatinine Phosphokinase
- Diabetes
- Ejection Fraction
- High Blood Pressure
- Platelets
- Serum Creatinine
- Serum Sodium
- Sex
- Smoking
- Follow-up Time

---

## Project Structure

```
heart-failure-predict
│
├── static/
├── templates/
├── app.py
├── train_model.py
├── model.pkl
├── dataset.csv
├── requirements.txt
├── Dockerfile
├── Procfile
└── README.md
```

---

## Running Locally

Clone the repository

```bash
git clone https://github.com/aishwarya426/heart-failure-predict.git
```

Move into the project

```bash
cd heart-failure-predict
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## Future Improvements

- Prediction probability visualization
- Feature importance charts
- REST API for predictions
- User authentication
- Prediction history
- Export prediction reports

---

## License

This project is licensed under the MIT License.

---

## Author

**Aishwarya Tolani**

GitHub: **https://github.com/aishwarya426**

---
