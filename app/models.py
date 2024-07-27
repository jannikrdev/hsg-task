from tortoise.models import Model
from tortoise import fields


class User(Model):
    email = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    collection = fields.CharField(max_length=255)

    def __str__(self) -> str:
        return self.email

