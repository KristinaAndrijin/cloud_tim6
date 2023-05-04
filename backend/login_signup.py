import boto3
import botocore
import re
import datetime

from keys import *
from flask import *
from flask_api import status

regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

db = session.client('dynamodb')


# @app.route('/', methods=['get'])
# def kme():
#     table = db.create_table(
#         TableName='users',
#         KeySchema=[{'AttributeName': 'username', 'KeyType': 'HASH'}],
#         AttributeDefinitions=[{'AttributeName': 'username', 'AttributeType': 'S'}],
#
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 5,
#             'WriteCapacityUnits': 3
#         },
#     )
#     # Wait for the table to become active
#     waiter = db.get_waiter('table_exists')
#     waiter.wait(TableName='users')
#
#     response = db.list_tables(
#         ExclusiveStartTableName='string',
#         Limit=10
#     )
#     return response


def is_valid(email):
    return re.fullmatch(regex_email, email)


def is_good_enough(password):
    return re.fullmatch(password_pattern, password)


def check_data(name, surname, birth_date, email, password):
    ret_string = ""

    if not is_valid(email):
        ret_string += "Wrong email format. \n"

    if not is_good_enough(password):
        ret_string += "Wrong password format. Password should have minimum 8 characters in length, " \
                      "at least one uppercase English letter, one lowercase English letter, one digit " \
                      "and one special character. \n"

    if not name.isalpha():
        ret_string += "Wrong name format. \n"

    if not surname.isalpha():
        ret_string += "Wrong surname format. \n"

    try:
        datetime.datetime.strptime(birth_date, '%d.%m.%Y.')
    except ValueError:
        ret_string += "Wrong date format. Correct: dd.MM.yyyy. \n"

    return ret_string


@app.route('/signup', methods=['post'])
def signup():
    # get data
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    birth_date = data['birth_date']
    username = data['username']
    email = data['email']
    password = data['password']

    # checking...
    ret_string = check_data(name, surname, birth_date, email, password)

    if ret_string != "":
        return ret_string, status.HTTP_400_BAD_REQUEST

    # input if ok
    item = {
        'username': {'S': username},
        'password': {'S': password},
        'email': {'S': email},
        'name': {'S': name},
        'surname': {'S': surname},
        'birth_date': {'S': birth_date}
    }

    try:
        response = db.put_item(
            TableName='users',
            Item=item,
            ConditionExpression='attribute_not_exists(username)'
        )
        return "Successful"
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return "User with username " + username + " already exists", status.HTTP_400_BAD_REQUEST
        else:
            return "Error:" + str(e), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/login', methods=['post'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    response = db.get_item(
        TableName="users",
        Key={
            'username': {'S': username}
        }
    )
    try:
        real_username = response['Item']['username']['S']
        real_password = response['Item']['password']['S']
        if username == real_username and password == real_password:
            return "Successful login"
        return "Wrong username or password", status.HTTP_400_BAD_REQUEST
    except KeyError:
        return "Wrong username or password", status.HTTP_400_BAD_REQUEST


if __name__ == "__main__":
    app.run(debug=True)
