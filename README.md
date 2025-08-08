# Data Preprocessing Chatbot

## 📖 Overview

This project is an interactive web application built with Streamlit that allows users to upload a CSV file and perform common data preprocessing tasks through a simple, user-friendly interface. The goal of this tool is to make data cleaning and preparation more accessible and transparent.

---

## ✨ Features

- **Upload CSV:** Easily upload your dataset in CSV format.
- **Data Preview:** Instantly view the first few rows of your data.
- **Detailed Summary:** Get a comprehensive summary including data types, descriptive statistics, and missing value counts.
- **Handle Missing Values:** Choose from multiple strategies to handle missing data:
  - Drop rows with null values.
  - Fill numerical columns with the mean or median.
  - Fill any column with the mode.
- **Remove Duplicates:** Clean your dataset by removing duplicate rows with a single click.
- **Feature Scaling:** Scale numerical features using:
  - **Normalization** (Min-Max Scaling to [0, 1]).
  - **Standardization** (Z-score Scaling).
- **Reset Data:** Revert all changes and go back to the original uploaded data at any time.
- **Download Processed Data:** Export the cleaned and transformed dataset as a new CSV file.

---

## 🛠️ Technologies Used

- **Backend & Logic:** Python
- **Data Manipulation:** Pandas
- **Machine Learning (Scaling):** Scikit-learn
- **Web Framework:** Streamlit

---

## 🚀 How to Run Locally

To run this application on your local machine, please follow these steps:

**1. Clone the repository:**
