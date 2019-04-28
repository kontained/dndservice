from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from datetime import datetime
import uuid
import os


class UsernameIndex(GlobalSecondaryIndex):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    username = UnicodeAttribute(hash_key=True)


class User(Model):
    class Meta:
        table_name = 'Users'
        write_capacity_units = 1
        read_capacity_units = 1
        region = 'us-west-2'
        host = os.environ.get('DYNAMODB_URL', default='http://localhost:8000')

    user_id = UnicodeAttribute(hash_key=True, default=str(uuid.uuid4()))
    username_index = UsernameIndex()
    username = UnicodeAttribute()
    password_hash = UnicodeAttribute()
    refresh_token = UnicodeAttribute()
    date_added = UTCDateTimeAttribute(default=datetime.utcnow())
