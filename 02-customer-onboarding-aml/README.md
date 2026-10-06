# 02 — Customer Onboarding & AML Screening

A bank onboarding service that decides whether a new customer can open an account. Built first as Python logic in a notebook, then exposed as a REST API with FastAPI, and tested with pytest and Postman.

> All names, lists, and country codes are fictional and used for training only.

## Decision rules

Checks run in this order. The first rule that matches decides the result.

| Order | Check | Decision |
|-------|-------|----------|
| 1 | Name matches the sanctions list | `Reject: sanctions match` |
| 2 | Age under 18 | `Reject: under 18` |
| 3 | ID expired | `Reject: ID expired` |
| 4 | Politically exposed person or high-risk country | `EDD` |
| 5 | None of the above | `Approve` |

Sanctions screening runs first so that every sanctions match is recorded with the correct reason, even when the applicant would also fail another rule.

## Project structure

| Path | What it is |
|------|------------|
| `customer_onboarding_aml.ipynb` | Phase 1: the logic and 19 unit tests in Google Colab |
| `api/onboarding.py` | Business rules used by the API |
| `api/main.py` | FastAPI service with the request contract (`POST /onboard`) |
| `api/test_api.py` | 17 automated API and database tests with pytest |
| `api/onboarding-api.postman_collection.json` | Postman collection with test scripts |
| `api/requirements.txt` | Python packages needed |

## Defects found and fixed

| # | Found with | Input | Expected | Actual before fix | Fix |
|---|------------|-------|----------|-------------------|-----|
| 1 | Colab | `"Salem    Nasser"` (extra spaces) | Sanctions match | Passed screening | Rebuild the name with single spaces |
| 2 | Swagger | `"age": -5` | 422 | 200, `Reject: under 18` | `age: int = Field(ge=0, le=120)` |
| 3 | Swagger | `"id_expiry": "01-09-2027"` | 422 | 200, `Reject: ID expired` | `id_expiry: date` in the contract |
| 4 | Postman | `"nationality": "xa"` | `EDD` | `Approve` | Normalize the country code before comparing |

Defects 1 and 4 are the same class: exact text comparison without normalization. In AML screening, both are **false negatives**, where a risky customer passes a control silently.

## Testing approach

| Technique | Where |
|-----------|-------|
| Boundary Value Analysis | Age 0, 17, 18, 120, 121; ID expiring yesterday, today, and tomorrow |
| Input variations | Letter case and extra spaces in names and country codes |
| Combination testing | A customer with two problems gets the right decision |
| Contract validation | Wrong types, missing fields, wrong date format, impossible dates |
| Mutation testing | Swapping the rule order was caught by a combination test |
| Regression | Every fixed defect has an automated test |

## How to run the API

```
cd api
python -m pip install -r requirements.txt
python -m fastapi dev main.py
```

Open http://127.0.0.1:8000/docs to try the API in Swagger.

**Run the tests** (in a second terminal, from the `api` folder):

```
python -m pytest -v
```

**Postman:** import `onboarding-api.postman_collection.json`, then set the collection variable `baseUrl` to `http://127.0.0.1:8000`.

## Open questions and known limitations

- **Open:** should an ID that expires today be accepted? Is exactly 18 allowed? The code assumes yes to both.
- **Open:** malformed JSON returns 422. Some API standards expect 400 for this case.
- **Limitation:** Arabic names written in English vary (*Salem* / *Salim*, *Omar* / *Umar*). Exact matching misses these. Production systems use fuzzy matching, which balances false negatives against false positives.

## Progress

- [x] Business logic with unit tests (Colab)
- [x] REST API with FastAPI
- [x] Automated API tests (pytest) and Postman collection
- [x] SQLite database: reference tables, audit trail, isolated test database
- [ ] Streamlit page, tested with Playwright

## Skills

Python · FastAPI · Pydantic · pytest · Postman · REST API testing · test design (BVA, equivalence partitioning, combination testing) · mutation testing · defect reporting · AML concepts (sanctions screening, PEP, EDD)
