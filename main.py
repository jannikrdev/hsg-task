import fastapi
import task.api as api
import task.crud as crud
import task.models as models


models.create_db_and_tables()
john = crud.create_user("john@test.de", "secret")
token = crud.login_user("john@test.de", "secret")
print(token.token)
crud.get_current_user(token.token)
print((crud.get_current_user(token.token)))
document = "This is a test"
doc2 = "hello, Mom!"
crud.create_document(john.collection, doc2, "doc2")
crud.create_document(john.collection, document, "doc1")
search_string = "hello"
print(crud.read_document(john.collection, search_string))
print(crud.get_documents(john.collection))
