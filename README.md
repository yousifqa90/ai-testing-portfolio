# 01 — Account Statement Review

A Python program that reviews a customer's bank account statement, with automated tests that verify its rules.

## The problem

A reviewer needs a quick summary of a customer's statement: how much came in, how much went out, whether the balance reconciles, and whether any transactions look suspicious.

## What the program does

| Feature | Rule |
|---------|------|
| Totals | Positive amounts are deposits, negative amounts are withdrawals |
| Closing balance | Opening balance + all transactions |
| Suspicious transactions | Any single transaction above 5,000 SAR, in either direction |
| Risk level | `Low` = 0 suspicious, `Review` = 1–2, `High` = 3 or more |
| Reconciliation | Closing balance must equal opening balance + deposits + withdrawals |

## Sample output

```
===================================
   ACCOUNT STATEMENT REVIEW
===================================
Customer:          Yousif
Opening balance:   7500 SAR
Transactions:      6
Total deposits:    8500 SAR
Total withdrawals: -11600 SAR
Closing balance:   4400 SAR
Average txn:       -516.67 SAR
Suspicious txns:   2
Risk level:        Review
Reconciliation:    True
===================================
```

## Testing approach

| Technique | What was tested |
|-----------|-----------------|
| Reconciliation | Closing balance of a sample statement |
| Zero-One-Many | An empty statement returns the opening balance and does not crash |
| Boundary Value Analysis | `5000` and `-5000` are not suspicious; `5001` and `-5001` are |
| Equivalence partitioning | One test for each risk level |
| Mutation testing | Changing `>` to `>=` was caught by the `5000` boundary test |

## Open question

The requirement says transactions **above** 5,000 SAR are suspicious, but does not say whether exactly 5,000 SAR should be flagged. The code assumes *above* (`>`). In a real project this would be confirmed with the business analyst.

## How to run

1. Open `account_statement_review.ipynb` in [Google Colab](https://colab.research.google.com/)
2. Select **Runtime → Run all**

## Skills

Python · functions · loops · conditions · `assert` · test design (BVA, equivalence partitioning, Zero-One-Many) · mutation testing
