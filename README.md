# AI Testing Portfolio — Banking QA

Senior banking QA professional (13+ years) building hands-on skills in **Python, data analysis, and AI/ML testing**, with every project grounded in real banking scenarios: payments, fraud, statements, and customer-facing AI.

## Projects

| # | Project | Skills | Status |
|---|---------|--------|--------|
| 01 | [Account Statement Review](01-account-statement-review/) | Python basics, loops, conditions, functions, `assert`, BVA, mutation testing | ✅ Done |
| 02 | [Customer Onboarding & AML Screening](02-customer-onboarding-aml/) | Dictionaries, text normalization, sanctions screening, combination testing | 🔄 Logic + API done · DB, UI next |
| 03 | Card Transaction Authorization | Luhn check, card status, limits, PIN attempts | 📋 Planned |
| 04 | Fraud Detection Model Testing | Pandas, ML metrics, fairness, Power BI | 📋 Planned |
| 05 | Arabic Banking Chatbot Evaluation | LLM evaluation, hallucination, dialect handling | 📋 Planned |
---

## 01 — Account Statement Review

A small program that reviews a customer's account statement:

- Calculates total deposits, withdrawals, and closing balance
- Flags suspicious transactions (above 5,000 SAR in either direction)
- Assigns a risk level: `Low`, `Review`, or `High`
- Prints a formatted review report

### Testing approach

The logic is split into small functions and verified with automated `assert` tests:

- **Reconciliation:** closing balance must equal opening balance plus all transactions
- **Boundary Value Analysis:** `5000` (not suspicious), `5001` and `-5001` (suspicious)
- **Zero-One-Many:** an empty statement must not crash and must return the opening balance
- **Mutation testing:** changing `>` to `>=` in the suspicious-transaction rule was deliberately introduced and caught by the `5000` boundary test

### How to run

Open the notebook in [Google Colab](https://colab.research.google.com/) and select **Runtime → Run all**.

---

## About me

**Yousif** — UAT Test Manager | ISTQB Trainer (CTFL, CT-GenAI) | Riyadh, Saudi Arabia

Core banking (T24, FLEXCUBE) · GCC payments (Mada, SARIE, SADAD) · Cards · SAMA frameworks


