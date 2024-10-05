import pandas as pd
import mysql.connector
import preprocessor
from sqlalchemy import create_engine
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Establish a connection to the MySQL database
con = mysql.connector.connect(
    host="localhost", 
    user="root",
    password="Niki*123",
    database="HRAnalytics"
)
engine = create_engine('mysql+mysqlconnector://root:Niki*123@localhost:3306/HRAnalytics')
cursor = con.cursor()

def cred():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('credentials.json')
    drive = GoogleDrive(gauth)
    folder_id = '1BqydcCTtPXYPzLq84GG8Yk1kVgfo1Wv_' 
    return drive

def Update_data_Employee():
    drive = cred()
    query = "SELECT * FROM Employee"
    df = pd.read_sql(query, engine)
    df.to_csv("Employee.csv", index=False)
    print(f'Uploading and replacing Employee.csv on Google Drive...')
    cleaned_file_to_upload = drive.CreateFile({'id':"1wNbaPfNkIRrUIQM8fBV5b9kPYketgzlk" })  
    cleaned_file_to_upload.SetContentFile("Employee.csv")    
    cleaned_file_to_upload.Upload()  

def Update_data_PerformanceRating():
    drive = cred()
    query = "SELECT * FROM PerformanceRating"
    df = pd.read_sql(query, engine)
    df.to_csv("PerformanceRating.csv", index=False)
    print(f'Uploading and replacing PerformanceRating.csv on Google Drive...')
    cleaned_file_to_upload = drive.CreateFile({'id':"1J7DT4GJkyEsRQZ_YNwBpPzZOqFeTaYet" }) 
    cleaned_file_to_upload.SetContentFile("PerformanceRating.csv")    
    cleaned_file_to_upload.Upload()  
    
# adding new data to database
def add_new_rows():
    print("""Choices for adding data in tables: 
             1. Add data in Employee Table
             2. Add data in Performance Rating Table""")
    
    select = int(input("Enter your choice: "))

    if select == 1:
        num_records = int(input("How many records do you want to add? "))

        for i in range(num_records):
            print(f"\nAdding record {i+1} to Employee Table:")

            # Input details for each record
            EmployeeID = input("Enter ID : ")
            FirstName = input("First Name : ")
            LastName = input("Last Name : ")
            gender  = input("Gender : ")
            Age  = int(input("Age : "))
            BusinessTravel = input("Business Travel : ")
            Department = input("Enter Department : ")
            Distance = int(input("Distance From Home (KM) : "))
            State = input("Enter State : ")
            Ethnicity = input("Ethnicity : ")
            Education = int(input("Education : "))
            EducationField = input("Enter EducationField : ")
            JobRole = input("Enter JobRole : ")
            MaritalStatus = input("Marital Status : ")
            Salary = int(input("Salary : "))
            StockOptionLevel = int(input("Stock Option Level : "))
            OverTime = input("Over Time (Yes/No) : ")
            HireDate = input("Hire Date (YYYY-MM-DD): ")
            Attrition = input("Attrition (Yes/No) : ")
            YearsAtCompany = int(input("Years At Company : "))
            YearsInMostRecentRole = int(input("Years In Most Recent Role : "))
            YearsSinceLastPromotion = int(input("Years Since Last Promotion : "))
            YearsWithCurrManager = int(input("Years With Current Manager : "))

            # Prepare SQL insert query
            insert_query = """
            INSERT INTO Employee (EmployeeID, FirstName, LastName, Gender, Age, BusinessTravel, Department, `DistanceFromHome (KM)`, 
            State, Ethnicity, Education, EducationField, JobRole, MaritalStatus, Salary, StockOptionLevel, 
            OverTime, HireDate, Attrition, YearsAtCompany, YearsInMostRecentRole, YearsSinceLastPromotion, YearsWithCurrManager)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Data to insert
            data = (EmployeeID, FirstName, LastName, gender, Age, BusinessTravel, Department, Distance, State, Ethnicity, Education, 
                    EducationField, JobRole, MaritalStatus, Salary, StockOptionLevel, OverTime, HireDate, Attrition, 
                    YearsAtCompany, YearsInMostRecentRole, YearsSinceLastPromotion, YearsWithCurrManager)

            # Execute the insert query for each record
            try:
                cursor.execute(insert_query, data)
                con.commit()  # Commit each transaction
                print(f"Record {i+1} added successfully.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                con.rollback()  # Rollback in case of error
            # Updating to Google Drive
            Update_data_Employee()
    
    elif select == 2:
        num_records = int(input("How many records do you want to add? "))

        # Loop for each record
        for i in range(num_records):
            print(f"\nEntering data for record {i + 1} to PerformanceRating Table:")
            PerformanceID = int(input("Enter Performance ID: "))
            EmployeeID = int(input("Enter Employee ID: "))
            ReviewDate = input("Enter Review Date (YYYY-MM-DD): ")
            EnvironmentSatisfaction = int(input("Enter Environment Satisfaction Level: "))
            JobSatisfaction = int(input("Enter Job Satisfaction Level: "))
            RelationshipSatisfaction = int(input("Enter Relationship Satisfaction Level: "))
            TrainingOpportunitiesWithinYear = int(input("Enter Training Opportunities Within Year: "))
            TrainingOpportunitiesTaken = int(input("Enter Training Opportunities Taken: "))
            WorkLifeBalance = int(input("Enter WorkLife Balance Rating: "))
            SelfRating = int(input("Enter Self Rating: "))
            ManagerRating = int(input("Enter Manager Rating: "))

            # Define the SQL query for inserting the record
            insert_query = """
            INSERT INTO PerformanceRating (PerformanceID, EmployeeID, ReviewDate, EnvironmentSatisfaction, JobSatisfaction, 
                                     RelationshipSatisfaction, TrainingOpportunitiesWithinYear, TrainingOpportunitiesTaken, 
                                     WorkLifeBalance, SelfRating, ManagerRating)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Execute the insert query with user input
            try:
                cursor.execute(insert_query, (PerformanceID, EmployeeID, ReviewDate, EnvironmentSatisfaction, 
                                              JobSatisfaction, RelationshipSatisfaction, TrainingOpportunitiesWithinYear, 
                                              TrainingOpportunitiesTaken, WorkLifeBalance, SelfRating, ManagerRating))
                con.commit()  # Commit each transaction
                print(f"Record {i + 1} added successfully.\n")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                con.rollback()  # Rollback in case of error
            # Updating to Google Drive
            Update_data_PerformanceRating()

    cursor.close()
    con.close()

choice = int(input("""How do you want to load Data:
            1. From Drive
            2. From Here
Enter your choice: """))

if choice == 1:
    preprocessor.Load_data_from_drive()
elif choice == 2:
    add_new_rows()
else:
    print("Invalid choice. Please select 1 or 2.")




