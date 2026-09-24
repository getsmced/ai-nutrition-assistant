from __future__ import annotations
from email.policy import default
import uuid
from datetime import UTC, datetime, date

from pydantic import EmailStr
from sqlalchemy import DateTime , JSON
from sqlmodel import Field, Relationship, SQLModel
from typing import Literal


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list[Item] = Relationship(back_populates="owner", cascade_delete=True)
    nutrition_profile: NutritionProfile | None = Relationship(back_populates="owner")



# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


Sex = Literal["male", "female"]
NutritionGoal = Literal["fat_loss", "muscle_gain", "maintenance"]
GoalIntensity = Literal["mild", "moderate", "intense"]
ActivityLevel = Literal["sedentary", "light", "moderate", "very_active"]



class NutritionProfileBase(SQLModel):

    date_of_birth: date
    sex: Sex
    height_cm: float = Field(ge=120, le=240)
    current_weight_kg : float = Field(ge = 35, le = 250)
    primary_goal : NutritionGoal
    goal_intensity : GoalIntensity
    activity_level : ActivityLevel
    exercises: bool = False
    exercises_per_week: int | None = Field (default= None, ge=0, le=7)
    meals_per_day : int = Field (ge=2, le=6)
    selected_foods: list[str] = Field(default_factory=list, sa_type=JSON)
    excluded_foods: list[str] = Field(default_factory=list, sa_type=JSON)
    allergies: list[str] = Field(default_factory=list, sa_type=JSON)


class NutritionProfileCreate(NutritionProfileBase):
    pass


class NutritionProfileUpdate(SQLModel):
    date_of_birth: date | None = None
    sex: Sex | None = None
    height_cm: float | None = Field(default=None, ge=120, le=240)
    current_weight_kg: float | None = Field(default=None, ge=35, le=250)

    primary_goal: NutritionGoal | None = None
    goal_intensity: GoalIntensity | None = None
    activity_level: ActivityLevel | None = None

    exercises: bool | None = None
    exercises_per_week: int | None = Field(default=None, ge=0, le=7)

    meals_per_day: int | None = Field(default=None, ge=2, le=6)
    selected_foods: list[str] | None = None
    excluded_foods: list[str] | None = None
    allergies: list[str] | None = None






class NutritionProfile(NutritionProfileBase, table=True):
    __tablename__ = "nutrition_profile"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id",
        nullable=False,
        unique=True,
        ondelete="CASCADE",
    )
    owner: User | None = Relationship(back_populates="nutrition_profile")


class NutritionProfilePublic(NutritionProfileBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None