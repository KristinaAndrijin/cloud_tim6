import boto3
from keys import *
from flask import *

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name='eu-central-1'
)

db = session.client('dynamodb')
users = None

# zakomentarisati 23-35 posle prvog pokretanja jer ne mozemo imati dve tabele istog imena ofc
@app.route('/', methods=['get'])
def kme():
    table = db.create_table(
        TableName='users2',
        KeySchema=[{'AttributeName': 'username', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'username', 'AttributeType': 'S'}],

        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 3
        },
    )
    # Wait for the table to become active
    waiter = db.get_waiter('table_exists')
    waiter.wait(TableName='users2')

    response = db.list_tables(
        ExclusiveStartTableName='string',
        Limit=10
    )
    return response


@app.route('/signup', methods=['post'])
def signup():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    birth = data['birth']
    username = data['username']
    email = data['email']
    password = data['password']

    item = {
        'username': {'S': username},
        'password': {'S': password},
        'email': {'S': email},
        'name': {'S': name},
        'surname': {'S': surname},
        'birth': {'S': birth}
    }

    response = db.put_item(
        TableName='users2',
        Item=item
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
