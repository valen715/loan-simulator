def calculate_monthly_payment(amount: float, annual_rate: float, months: int) -> float:
    monthly_rate = (1 + annual_rate / 100) ** (1 / 12) - 1
    if monthly_rate == 0:
        return amount / months
    return amount * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
