import re
import pandas as pd
import mysql.connector
from sqlalchemy import text
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Establish a connection to the MySQL database
con = mysql.connector.connect(
    host="localhost", 
    user="root",
    password="Niki*123",
    database="HRAnalytics"
)
engine = create_engine('mysql+mysqlconnector://root:Niki*123@localhost:3306/HRAnalytics')
Session = sessionmaker(bind=engine)
session = Session()
cursor = con.cursor()

def clean_data(df):
     # Drop rows with too many NaN values (threshold)
    df_cleaned = df.dropna(thresh=len(df.columns) * 0.5, axis=0)

    # Drop columns with too many missing values (threshold: 50% missing)
    df_cleaned = df_cleaned.dropna(thresh=len(df_cleaned) * 0.5, axis=1)
    
    # Remove duplicates if any
    df_cleaned = df_cleaned.drop_duplicates()

    def is_valid_date_format(date_str):
    # Check if the date follows the 'YYYY-MM-DD' format using a regular expression
        return bool(re.match(r'\d{4}-\d{2}-\d{2}', str(date_str)))

    if 'ReviewDate' in df_cleaned.columns:
        df_cleaned['ReviewDate'] = df_cleaned['ReviewDate'].apply(
        lambda x: pd.to_datetime(x, format='%m/%d/%Y', errors='coerce') if not is_valid_date_format(x) else x
        )
        df_cleaned['ReviewDate'] = df_cleaned['ReviewDate'].apply(
        lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) and pd.notna(x) else x
        )

    Uploading_file_in_database(df_cleaned)
    return df_cleaned

# Designing Database
def Database_design():
    query = """CREATE TABLE IF NOT EXISTS EducationLevel (
                EducationLevelID INT NOT NULL PRIMARY KEY,
                EducationName TEXT);"""
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS Employee (
                EmployeeID VARCHAR(20) NOT NULL PRIMARY KEY,
                FirstName TEXT,
                LastName TEXT,
                Gender TEXT,
                Age INT,
                BusinessTravel TEXT,
                Department TEXT,
                `DistanceFromHome (KM)` INT,
                State TEXT,
                Ethnicity TEXT,
                Education INT,
                EducationField TEXT,
                JobRole TEXT,
                MaritalStatus TEXT, 
                Salary INT,
                StockOptionLevel INT,
                OverTime TEXT,
                HireDate DATE,
                Attrition TEXT,
                YearsAtCompany INT,
                YearsInMostRecentRole INT,
                YearsSinceLastPromotion INT,
                YearsWithCurrManager INT
                );"""
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS RatingLevel (
                RatingID INT NOT NULL PRIMARY KEY,
                RatingLevel TEXT
            );"""
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS SatisfiedLevel (
                SatisfactionID INT NOT NULL PRIMARY KEY,
                SatisfactionLevel TEXT
            );"""
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS PerformanceRating (
                PerformanceID VARCHAR(20) NOT NULL PRIMARY KEY,
                EmployeeID VARCHAR(20),
                ReviewDate DATE,
                EnvironmentSatisfaction INT,
                JobSatisfaction INT,
                RelationshipSatisfaction INT,
                TrainingOpportunitiesWithinYear INT,
                TrainingOpportunitiesTaken INT,
                WorkLifeBalance INT,
                SelfRating INT,
                ManagerRating INT);"""
    cursor.execute(query)
    con.commit()
 
def Uploading_file_in_database(df):
    Database_design()
    print("Updating Data to Database")
    
    # List of table names to check and update
    table_names = ["employee", "performancerating","educationlevel","ratinglevel","satisfiedlevel"]

    # Function to check if DataFrame columns match table columns
    def check_column_match(engine, table_name, df):
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        
        # Case-insensitive comparison
        if list(map(str.lower, df.columns)) == list(map(str.lower, columns)):
            return True

    # Function to truncate table
    def truncate_table(engine, table_name):
        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name}"))


    # Function to load data into the table
    def load_data_to_db(engine, df, table_name):
        truncate_table(engine, table_name)  
    
        # Loop through each row and insert it into the database
        for index, row in df.iterrows():
            try:
                # Insert the row into the database
                row.to_frame().T.to_sql(table_name, con=engine, if_exists='append', index=False)
                session.commit()
            except Exception as e:
                session.rollback() 
                # Print an error message and the problematic row index
                print(f"Error inserting row {index}: {e}")
                continue  
            finally:
                session.close()

    # Main process - loop through table names
    for table_name in table_names:
        if check_column_match(engine, table_name, df):
            load_data_to_db(engine, df, table_name)
    

def Load_data_from_drive():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('credentials.json')
    drive = GoogleDrive(gauth)

    # Define folder ID where files are located
    folder_id = '1BqydcCTtPXYPzLq84GG8Yk1kVgfo1Wv_' 
    # List files in the Google Drive folder
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

    # Loop through files, download, clean, and replace in Google Drive
    for file in file_list:
        file_id = file['id']
        file_name = file['title']
    
        print(f'Downloading and cleaning {file_name}...') 

        # Download the file
        file_to_download = drive.CreateFile({'id': file_id})
        file_to_download.GetContentFile(f'{file_name}')

        # Load the file into pandas DataFrame (assuming CSV format for this example)
        df = pd.read_csv(file_name)

        # Clean the DataFrame
        cleaned_df = clean_data(df)

        # Save the cleaned DataFrame to a new file
        cleaned_file_name = f'{file_name}'
        cleaned_df.to_csv(cleaned_file_name, index=False)

        # Replace the cleaned file in Google Drive
        print(f'Uploading and replacing {file_name} on Google Drive...')
        cleaned_file_to_upload = drive.CreateFile({'id': file_id})  # Use the same file ID to replace
        cleaned_file_to_upload.SetContentFile(cleaned_file_name)    # Set the cleaned file content
        cleaned_file_to_upload.Upload()  # Upload the cleaned file (this replaces the original file)

        print(f'{file_name} has been cleaned and replaced on Google Drive.')       

    
# callig function 
Load_data_from_drive()




