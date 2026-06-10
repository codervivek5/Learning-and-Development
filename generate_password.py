from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

hashed = pwd_context.hash("vivek@123")
print(hashed)