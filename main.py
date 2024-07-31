import fastapi
import task.api
import task.crud as crud
import task.models


task.models.create_db_and_tables()
crud.create_user("john@test.de", "secret")
token = crud.login_user("john@test.de", "secret")
print(token)
