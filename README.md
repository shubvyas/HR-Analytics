# HR-Analytics
<img src="https://github.com/user-attachments/assets/1cac8a27-ae6a-4228-8920-a25e05af8d43" alt="HR_logo" width="200" height="auto">






# Employee Performance & Satisfaction Data Dictionary

## Overview

This document provides a comprehensive overview of the key data tables and fields relevant to employee performance, satisfaction, and demographic details. This data is essential for understanding employee engagement, job satisfaction, and performance metrics within the organization. It assists HR in making informed decisions related to employee development, retention, and workplace improvements.

## HR Perspective

From an HR perspective, this dataset is invaluable for assessing various aspects of the employee experience. By analyzing these data points, HR can identify patterns and areas for improvement within the workplace, such as enhancing job satisfaction, increasing work-life balance, and developing targeted training programs. This data also aids in evaluating the effectiveness of current HR strategies and initiatives aimed at improving employee retention and fostering a positive organizational culture.

## Project Overview
**The pipeline performs the following steps:**

**Data Access**: Files are uploaded to a Google Drive folder. Using the Google Cloud API, the data is accessed and downloaded to a Python environment.

**Data Cleaning**: With pandas, the data is cleaned and prepared for database insertion.

**Data Storage**: Cleaned data is loaded into a MySQL database. We use Python libraries such as MySQL Connector and SQLAlchemy to handle data uploads.

**Database Management**: Tables in the database are truncated each time new data is added, ensuring consistency without duplicate records.

**Visualization**: MySQL is connected to Power BI for building dashboards and visualizing the processed data.





## Prerequisites
**To successfully set up and use this project, we need the following:**

### Prerequisites

- Python 3.x and the following libraries:
  - pandas
  - MySQL Connector
  - SQLAlchemy
  - Google Cloud API client libraries
- Google Cloud Project with access to Google Drive API
- MySQL Server
- Power BI Desktop for dashboard creation


# Data Dictionary

## FactPerformanceRating

This table contains the performance review details for each employee, including various ratings and assessments.

| Column Name                  | Description                                                                           |
|------------------------------|---------------------------------------------------------------------------------------|
| **PerformanceID**            | Unique identifier for each performance review.                                        |
| **EmployeeID**               | Unique identifier for the employee being reviewed.                                    |
| **ReviewDate**               | The date of the performance review.                                                   |
| **EnvironmentSatisfaction**  | Rating of the employee's satisfaction with their work environment.                    |
| **JobSatisfaction**          | Rating of the employee's satisfaction with their job.                                 |
| **RelationshipSatisfaction** | Rating of the employee's satisfaction with workplace relationships.                   |
| **TrainingOpportunitiesWithinYear** | Number of training opportunities available to the employee within the year.    |
| **TrainingOpportunitiesTaken**      | Number of training opportunities the employee has taken.                       |
| **WorkLifeBalance**          | Rating of the employee's work-life balance.                                           |
| **SelfRating**               | The employee's self-assessment rating.                                                |
| **ManagerRating**            | The manager's rating of the employee's performance.                                   |

---

## DimEmployee

This table contains details about each employee, including personal information, job details, and employment history.

| Column Name                 | Description                                                                |
|-----------------------------|----------------------------------------------------------------------------|
| **EmployeeID**              | Unique identifier for each employee.                                       |
| **FirstName**               | The first name of the employee.                                            |
| **LastName**                | The last name of the employee.                                             |
| **Gender**                  | The gender of the employee.                                                |
| **Age**                     | The age of the employee.                                                   |
| **BusinessTravel**          | The frequency of business travel for the employee.                         |
| **Department**              | The department in which the employee works.                                |
| **DistanceFromHome (KM)**   | The distance between the employee's home and workplace in kilometers.      |
| **State**                   | The state in which the employee resides.                                   |
| **Ethnicity**               | The ethnicity of the employee.                                             |
| **MaritalStatus**           | The marital status of the employee.                                        |
| **Salary**                  | The annual salary of the employee.                                         |
| **StockOptionLevel**        | The level of stock options granted to the employee.                        |
| **OverTime**                | Whether the employee works overtime (Yes/No).                              |
| **HireDate**                | The date the employee was hired.                                           |
| **Attrition**               | Whether the employee has left the company (Yes/No).                        |
| **YearsAtCompany**          | The number of years the employee has been with the company.                |
| **YearsInMostRecentRole**   | The number of years the employee has been in their most recent role.       |
| **YearsSinceLastPromotion** | The number of years since the employee's last promotion.                   |
| **YearsWithCurrManager**    | The number of years the employee has worked with their current manager.    |

---

## SatisfiedLevel

This table contains information about satisfaction levels, from very dissatisfied to very satisfied.

| Column Name      | Description                                               |
|------------------|-----------------------------------------------------------|
| **SatisfactionID**    | Unique identifier for the satisfaction level.           |
| **SatisfactionLevel** | The level of satisfaction, ranging from "Very Dissatisfied" to "Very Satisfied." |

---

## RatingLevel

This table provides the different performance rating levels, describing employee performance ratings.

| Column Name      | Description                                               |
|------------------|-----------------------------------------------------------|
| **RatingID**     | Unique identifier for the rating level.                   |
| **RatingLevel**  | The performance rating, ranging from "Unacceptable" to "Above and Beyond." |

---

## EducationLevel

This table includes various education levels achieved by employees, from no formal qualifications to a doctorate.

| Column Name         | Description                                                          |
|---------------------|----------------------------------------------------------------------|
| **EducationLevelID** | Unique identifier for the education level.                          |
| **EducationLevel**   | The level of education achieved, ranging from "No Formal Qualifications" to "Doctorate." |

---

This document provides an overview of the key tables and columns in the dataset, helping to understand the structure of employee data and the details associated with performance reviews, satisfaction levels, ratings, and education levels.

# Entity-Relationship Diagram
![drawSQL-image-export-2024-10-06](https://github.com/user-attachments/assets/cfaa95dd-2cc6-46b5-a4a3-b6700fd84abb)




# Dashboard

![Empl](https://github.com/user-attachments/assets/a90f9431-fbc5-48ba-a3a3-4f6c0489f09e)
![dep](https://github.com/user-attachments/assets/e7e4fb44-627d-400c-9547-27ff2d2c5d31)



