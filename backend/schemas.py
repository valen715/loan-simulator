from pydantic import BaseModel

class LoanProductCreate(BaseModel):
    name: str
    annual_rate: float
    min_amount: float
    max_amount: float
    min_term: int
    max_term: int

class LoanSimulationInput(BaseModel):
    product_name: str
    amount: float
    term: int

class LoanSimulationResult(BaseModel):
    monthly_payment: float
    total_cost: float
