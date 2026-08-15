from routers.users import *

@router.post("/")
async def user_login(user: UserCreate):
    with Session(engine) as session:
        username_exists = session.scalars(select(User).where(User.username == user.username)).first()
        if username_exists is None:
            raise HTTPException(status_code= 400, detail= "Username not found!")

        if not pbkdf2_sha256.verify(user.password, username_exists.password):
            raise HTTPException(status_code = 401, detail= "Invalid password")