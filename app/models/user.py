from sqlalchemy import Column, Integer, String, Enum, Boolean
from app.db.base_class import Base
from app.utils.security import hash_password, verify_password
import enum


class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    SUPERVISOR = "Supervisor"
    EMPLOYEE = "Employee"
    COMPLIANCE = "Compliance"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, index=True, nullable=False, default="")
    email = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "password" in kwargs:
            self.set_password(kwargs["password"])

        if "role" in kwargs:
            if kwargs["role"] not in UserRole:
                raise ValueError(f"Invalid role: {kwargs['role']}")

            if kwargs["role"] == UserRole.ADMIN:
                self.is_superuser = True
        else:
            self.role = UserRole.EMPLOYEE

    def set_password(self, password: str):
        """Hash and set the password."""
        self.password = hash_password(password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify a plain password against the stored hash."""
        return verify_password(plain_password, self.password)
