from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field
from onboarding import get_decision

app = FastAPI(title="Customer Onboarding API")


class Customer(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    nationality: str
    is_pep: bool
    id_expiry: date


@app.post("/onboard")
def onboard(customer: Customer):
    decision = get_decision(customer.model_dump(mode="json"))
    return {"name": customer.name, "decision": decision}