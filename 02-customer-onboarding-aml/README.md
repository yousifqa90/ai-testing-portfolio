# 02 — Customer Onboarding & AML Screening

A Python program that decides whether a new bank customer can open an account, with automated tests that verify its rules.

> All names, lists, and country codes are fictional and used for training only.

## The problem

Before opening an account, a bank must check that the applicant is eligible and is not on a sanctions list. Higher-risk applicants need Enhanced Due Diligence (EDD) before approval.

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

## Testing approach

| Technique | What was tested |
|-----------|-----------------|
| Boundary Value Analysis | Age 17 and 18; ID expiring yesterday, today, and tomorrow |
| Input variations | Letter case and extra spaces must not bypass sanctions screening |
| Equivalence partitioning | One test for each possible decision |
| Combination testing | A customer with two problems gets the right decision |
| Mutation testing | Swapping the rule order was caught by a combination test |

**Test data builder:** `make_customer()` returns a valid customer, and each test changes only the field under test.

## Defect found

The first version of the name normalization used `strip()`, which only removes spaces at the ends of a name. A sanctioned name typed with extra spaces between words passed screening (a **false negative**). The fix rebuilds the name with single spaces: `" ".join(name.split()).lower()`.

## Mutation testing result

The rule order was deliberately swapped so that eligibility ran before sanctions screening. All single-rule tests still passed, but the combination test *"Sanctions must win over age"* failed. Rule-order defects only appear when one customer triggers two rules.

## Open questions and known limitations

- **Open:** should an ID that expires today be accepted? Is exactly 18 allowed? The code assumes yes to both.
- **Limitation:** Arabic names written in English vary (*Salem* / *Salim*, *Omar* / *Umar*). Exact matching misses these. Production systems use fuzzy matching, which balances false negatives against false positives.

## How to run

1. Open `customer_onboarding_aml.ipynb` in [Google Colab](https://colab.research.google.com/)
2. Select **Runtime → Run all**

## Next phases

- [ ] REST API with FastAPI, tested with Postman and pytest
- [ ] SQLite audit table, verified with SQL
- [ ] Streamlit page, tested with Playwright

## Skills

Python · dictionaries · text normalization · functions · `assert` · test design (BVA, equivalence partitioning, combination testing) · mutation testing · AML concepts (sanctions screening, PEP, EDD)
