from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# from sklearn.preprocessing import LabelEncoder
import sqlite3
import pickle
import csv
import pandas as pd
import random


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("./api/models/LR.pkl", "rb") as f:
    clf2 = pickle.load(f)


# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


# Function to initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            income INTEGER NOT NULL,
            education TEXT NOT NULL,
            region TEXT NOT NULL,
            loyalty_status TEXT NOT NULL,
            purchase_frequency TEXT NOT NULL,
            purchase_amount INTEGER NOT NULL,
            product_category TEXT NOT NULL,
            promotion_usage INTEGER NOT NULL,
            satisfaction_score INTEGER NOT NULL
        )
    """
    )
    conn.commit()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS encodedUsers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER NOT NULL,
            gender INTEGER NOT NULL,
            income INTEGER NOT NULL,
            education INTEGER NOT NULL,
            region INTEGER NOT NULL,
            loyalty_status INTEGER NOT NULL,
            purchase_frequency INTEGER NOT NULL,
            purchase_amount INTEGER NOT NULL,
            product_category INTEGER NOT NULL,
            promotion_usage INTEGER NOT NULL,
            satisfaction_score INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


class User(BaseModel):
    id: int
    age: int
    gender: str
    income: int
    education: str
    region: str
    loyalty_status: str
    purchase_frequency: str
    purchase_amount: int
    product_category: str
    promotion_usage: int
    satisfaction_score: int


class EncodedUser(BaseModel):
    id: int
    age: int
    gender: int
    income: int
    education: int
    region: int
    loyalty_status: int
    purchase_frequency: int
    purchase_amount: int
    product_category: int
    promotion_usage: int
    satisfaction_score: int


@app.get("/api/user")
def get_comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 100")
    users = cursor.fetchall()
    conn.close()
    return users


@app.get("/api/encodedUser")
def get_comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM encodedUsers LIMIT 100")
    users = cursor.fetchall()
    conn.close()
    return users


@app.get("/api/predict/{user_id}")
def predict(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM encodedUsers WHERE id = ?", (user_id,))
    encodedUser = cursor.fetchone()
    conn.close()

    encodedUser = list(encodedUser)
    del encodedUser[9]  # Remove product_category from encodedUser
    encodedUser = tuple(encodedUser)

    predict = clf2.predict([encodedUser])

    predict_category = ""
    predict[0] = predict
    # if predict[0] == 1:
    #     predict_category = "Books"
    # elif predict[0] == 2:
    #     predict_category = "Clothing"
    # elif predict[0] == 3:
    #     predict_category = "Electronics"
    # elif predict[0] == 4:
    #     predict_category = "Food"
    # elif predict[0] == 5:
    #     predict_category = "Health"
    # elif predict[0] == 6:
    #     predict_category = "Home"

    ran = random.randint(1, 6)
    if ran == 1:
        predict_category = "Books"
    elif ran == 2:
        predict_category = "Clothing"
    elif ran == 3:
        predict_category = "Electronics"
    elif ran == 4:
        predict_category = "Food"
    elif ran == 5:
        predict_category = "Health"
    elif ran == 6:
        predict_category = "Home"

    print("[userData]: ", predict_category)

    return {"predict_popup": random.randint(0, 1), "predict_category": predict_category}


# predict_category
# 1 -> "Books"
# 2 -> "Clothing"
# 3 -> "Electronics"
# 4 -> "Food"
# 5 -> "Health"
# 6 -> "Home"

# parse customer_data는 실 배포 때 사용하지 않음! 사이즈 문제 땜누에
# def parse_customer_data():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     with open('./api/data/customer_data.csv', 'r') as file:
#         reader = csv.reader(file)

#         next(reader)  # Skip header row

#         userList = pd.DataFrame(reader, columns=["id","age","gender","income","education","region","loyalty_status","purchase_frequency","purchase_amount","product_category","promotion_usage","satisfaction_score"])

#         encoder = LabelEncoder()
#         encodedColumn = ['gender', 'education', 'region', 'loyalty_status', 'product_category', 'purchase_frequency']

#         for column in encodedColumn:
#             userList[column] = encoder.fit_transform(userList[column])


#         for user in userList.iterrows():
#             extended_user = EncodedUser(
#                 id=int(user[1]['id']),
#                 age=int(user[1]['age']),
#                 gender=int(user[1]['gender']),
#                 income=int(user[1]['income']),
#                 education=int(user[1]['education']),
#                 region=int(user[1]['region']),
#                 loyalty_status=int(user[1]['loyalty_status']),
#                 purchase_frequency=int(user[1]['purchase_frequency']),
#                 purchase_amount=int(user[1]['purchase_amount']),
#                 product_category=int(user[1]['product_category']),
#                 promotion_usage=int(user[1]['promotion_usage']),
#                 satisfaction_score=int(user[1]['satisfaction_score'])
#             )
#             cursor.execute("""
#                 INSERT INTO encodedUsers (
#                     id, age, gender, income, education, region, loyalty_status,
#                     purchase_frequency, purchase_amount, product_category,
#                     promotion_usage, satisfaction_score
#                 )
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 extended_user.id, extended_user.age, extended_user.gender, extended_user.income, extended_user.education,
#                 extended_user.region, extended_user.loyalty_status, extended_user.purchase_frequency,
#                 extended_user.purchase_amount, extended_user.product_category, extended_user.promotion_usage,
#                 extended_user.satisfaction_score
#             ))

#     with open('./api/data/customer_data.csv', 'r') as file:
#         reader = csv.reader(file)

#         next(reader)  # Skip header row
#         print("[start!!]", reader.line_num)
#         for row in reader:
#             print
#             user = User(
#                 id=int(row[0]),
#                 age=int(row[1]),
#                 gender=row[2],
#                 income=int(row[3]),
#                 education=row[4],
#                 region=row[5],
#                 loyalty_status=row[6],
#                 purchase_frequency=row[7],
#                 purchase_amount=int(row[8]),
#                 product_category=row[9],
#                 promotion_usage=int(row[10]),
#                 satisfaction_score=int(row[11])
#             )
#             cursor.execute("""
#                 INSERT INTO users (
#                     id, age, gender, income, education, region, loyalty_status,
#                     purchase_frequency, purchase_amount, product_category,
#                     promotion_usage, satisfaction_score
#                 )
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 user.id, user.age, user.gender, user.income, user.education,
#                 user.region, user.loyalty_status, user.purchase_frequency,
#                 user.purchase_amount, user.product_category, user.promotion_usage,
#                 user.satisfaction_score
#             ))


#     conn.commit()
#     conn.close()


@app.post("/api/initialize")
def initialize():
    # parse_customer_data()
    return {"status": "success"}


# # API endpoint to create a new comment
# @app.post("/api/comments")
# def create_comment(comment: CommentCreate):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO comments (text) VALUES (?)", (comment.text,))
#     conn.commit()
#     comment_id = cursor.lastrowid
#     conn.close()
#     return {"id": comment_id, "text": comment.text}
