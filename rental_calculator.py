HOUSE_PRICE = 200000
LISTING_PRICE = 200000
DOWN_PAYMENT = 40000
INTEREST_RATE = 0.04
LOAN_TERM_YEARS = 30

MONTHLY_RENT = 2000
MONTHLY_OPERATING_EXPENSES = 600  # taxes, insurance, maintenance — NOT debt service
VACANCY_RATE = 0.05               # % of gross rent set aside for vacancy
CAPEX_RATE = 0.05                 # % of gross rent set aside for capex reserve
PMI_RATE = 0.01

loan_amount = LISTING_PRICE - DOWN_PAYMENT
monthly_rate = INTEREST_RATE / 12
n_payments = LOAN_TERM_YEARS * 12

monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / (
    (1 + monthly_rate) ** n_payments - 1
)

# Amortize year 1 month-by-month to split interest vs. principal correctly
balance = loan_amount
year1_interest = 0
year1_principal = 0
for _ in range(12):
    interest_payment = balance * monthly_rate
    principal_payment = monthly_payment - interest_payment
    year1_interest += interest_payment
    year1_principal += principal_payment
    balance -= principal_payment

monthly_pmi = (PMI_RATE * LISTING_PRICE) / 12 if DOWN_PAYMENT < (LISTING_PRICE * 0.2) else 0
annual_pmi = monthly_pmi * 12

annual_rent = MONTHLY_RENT * 12
annual_vacancy_loss = annual_rent * VACANCY_RATE
annual_capex_reserve = annual_rent * CAPEX_RATE
annual_operating_expenses = MONTHLY_OPERATING_EXPENSES * 12

effective_gross_income = annual_rent - annual_vacancy_loss

# Unlevered NOI: excludes debt service (interest + principal) and PMI, per standard cap rate convention
noi = effective_gross_income - annual_operating_expenses - annual_capex_reserve
cap_rate = (noi / HOUSE_PRICE) * 100

# Levered cash flow: NOI minus actual debt service and PMI
annual_debt_service = year1_interest + year1_principal
annual_cash_flow = noi - annual_debt_service - annual_pmi
monthly_cash_flow = annual_cash_flow / 12
cash_on_cash_roi = (annual_cash_flow / DOWN_PAYMENT) * 100

# Total return also credits equity built via principal paydown
total_return = annual_cash_flow + year1_principal
total_roi = (total_return / DOWN_PAYMENT) * 100

print(f"HOUSE_PRICE: ${HOUSE_PRICE:,.2f}")
print(f"DOWN_PAYMENT: ${DOWN_PAYMENT:,.2f}")
print(f"LOAN_AMOUNT: ${loan_amount:,.2f}")
print(f"LOAN_TERM_YEARS: {LOAN_TERM_YEARS}")
print(f"MONTHLY_MORTGAGE_PAYMENT (P&I): ${monthly_payment:,.2f}")
print(f"MONTHLY_PMI: ${monthly_pmi:,.2f}")
print()
print(f"MONTHLY_RENT: ${MONTHLY_RENT:,.2f}")
print(f"MONTHLY_OPERATING_EXPENSES: ${MONTHLY_OPERATING_EXPENSES:,.2f}")
print(f"VACANCY_RESERVE ({VACANCY_RATE:.0%} of rent): ${annual_vacancy_loss/12:,.2f}/mo")
print(f"CAPEX_RESERVE ({CAPEX_RATE:.0%} of rent): ${annual_capex_reserve/12:,.2f}/mo")
print()
print(f"EFFECTIVE GROSS INCOME (annual): ${effective_gross_income:,.2f}")
print(f"ANNUAL NOI (unlevered, excl. debt service): ${noi:,.2f}")
print(f"CAP RATE: {cap_rate:.2f}%")
print()
print(f"YEAR 1 INTEREST PAID: ${year1_interest:,.2f}")
print(f"YEAR 1 PRINCIPAL PAID: ${year1_principal:,.2f}")
print(f"ANNUAL DEBT SERVICE (P&I): ${annual_debt_service:,.2f}")
print(f"ANNUAL CASH FLOW (levered): ${annual_cash_flow:,.2f}")
print(f"MONTHLY CASH FLOW (levered): ${monthly_cash_flow:,.2f}")
print(f"CASH-ON-CASH ROI: {cash_on_cash_roi:.2f}%")
print()
print(f"TOTAL RETURN (cash flow + principal paydown): ${total_return:,.2f}")
print(f"TOTAL ROI (incl. equity build): {total_roi:.2f}%")
