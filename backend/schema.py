"""
backend/schema.py — request/response models for the predict endpoint.
"""

from typing import List, Optional, Tuple

from pydantic import BaseModel, Field


class StudentInput(BaseModel):
    # --- numeric features ---
    age: int = Field(..., ge=15, le=22, description="Student age (15-22)")
    Medu: int = Field(..., ge=0, le=4, description="Mother's education (0-4)")
    Fedu: int = Field(..., ge=0, le=4, description="Father's education (0-4)")
    traveltime: int = Field(..., ge=1, le=4, description="Home to school travel time (1-4)")
    studytime: int = Field(..., ge=1, le=4, description="Weekly study time (1-4)")
    failures: int = Field(..., ge=0, le=4, description="Past class failures (0-4)")
    famrel: int = Field(..., ge=1, le=5, description="Quality of family relationships (1-5)")
    freetime: int = Field(..., ge=1, le=5, description="Free time after school (1-5)")
    goout: int = Field(..., ge=1, le=5, description="Going out with friends (1-5)")
    Dalc: int = Field(..., ge=1, le=5, description="Workday alcohol consumption (1-5)")
    Walc: int = Field(..., ge=1, le=5, description="Weekend alcohol consumption (1-5)")
    health: int = Field(..., ge=1, le=5, description="Current health status (1-5)")
    absences: int = Field(..., ge=0, le=100, description="Number of school absences")
    G1: float = Field(..., ge=0, le=20, description="First period grade (0-20)")
    G2: float = Field(..., ge=0, le=20, description="Second period grade (0-20)")

    # --- categorical features ---
    school: str = Field(..., description="'GP' or 'MS'")
    sex: str = Field(..., description="'F' or 'M'")
    address: str = Field(..., description="'U' (urban) or 'R' (rural)")
    famsize: str = Field(..., description="'LE3' or 'GT3'")
    Pstatus: str = Field(..., description="'T' (together) or 'A' (apart)")
    Mjob: str
    Fjob: str
    reason: str
    guardian: str
    schoolsup: str = Field(..., description="'yes' or 'no'")
    famsup: str = Field(..., description="'yes' or 'no'")
    paid: str = Field(..., description="'yes' or 'no'")
    activities: str = Field(..., description="'yes' or 'no'")
    nursery: str = Field(..., description="'yes' or 'no'")
    higher: str = Field(..., description="'yes' or 'no'")
    internet: str = Field(..., description="'yes' or 'no'")
    romantic: str = Field(..., description="'yes' or 'no'")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 17, "Medu": 3, "Fedu": 2, "traveltime": 1, "studytime": 2,
                "failures": 0, "famrel": 4, "freetime": 3, "goout": 3, "Dalc": 1,
                "Walc": 2, "health": 4, "absences": 4, "G1": 14, "G2": 15,
                "school": "GP", "sex": "F", "address": "U", "famsize": "GT3",
                "Pstatus": "T", "Mjob": "teacher", "Fjob": "other", "reason": "course",
                "guardian": "mother", "schoolsup": "no", "famsup": "yes", "paid": "no",
                "activities": "yes", "nursery": "yes", "higher": "yes",
                "internet": "yes", "romantic": "no",
            }
        }


class FeatureContribution(BaseModel):
    feature: str
    importance: float


class PredictionResponse(BaseModel):
    predicted_g3: float
    predicted_grade_percent: float
    pass_fail: str
    top_features: List[FeatureContribution]
