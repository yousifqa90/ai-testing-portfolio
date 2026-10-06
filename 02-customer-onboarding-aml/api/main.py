from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from onboarding import get_decision
from database import init_db, country_exists, save_application
app = FastAPI(title="Customer Onboarding API")
init_db()

class Customer(BaseModel):
    name: str
    age: int = Field(ge=0, le=120)
    nationality: str
    is_pep: bool
    id_expiry: date


@app.post("/onboard")
def onboard(customer: Customer):
    data = customer.model_dump(mode="json")
    data["nationality"] = data["nationality"].strip().upper()

    if not country_exists(data["nationality"]):
        raise HTTPException(status_code=422, detail="Unknown nationality code")

    decision = get_decision(data)
    customer_id, application_id = save_application(data, decision)

    return {
        "application_id": application_id,
        "customer_id": customer_id,
        "name": customer.name,
        "decision": decision,
    }