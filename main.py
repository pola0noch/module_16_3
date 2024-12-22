from fastapi import FastAPI, HTTPException, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def register_user(username: Annotated[str, Path(min_lenght=3,
                                                      max_lenght=20,
                                                      regex="^[a-zA-Z0-9_-]+$")] ,
                        age: Annotated[int, Path(gt=0,
                                                 le=150,
                                                 description='Age from 0 to 150')]) -> str:

    user_id = str(int(max(users, key=int)) + 1)
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"User {user_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[str, Path(min_length=1,
                                                   description='User id from str in dict')],
                      username: Annotated[str, Path(min_lenght=3,
                                                    max_lenght=20,
                                                    regex="^[a-zA-Z0-9_-]+$")],
                      age: Annotated[int, Path(gt=0,
                                               le=150,
                                               description='Age from 0 to 150')]) -> str:

    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"The user {user_id} is updated"

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[str, Path(min_length=1,
                                                   description='User id from str in dict')]) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User  not found")
    users.pop(user_id)
    return f"The user {user_id} has been deleted"

