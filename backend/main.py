from fastapi import FastAPI, HTTPException
from models import loan_products
from schemas import LoanProductCreate, LoanSimulationInput, LoanSimulationResult
from utils import calculate_monthly_payment
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Servidor activo y funcionando"}

@app.get("/products")
def list_products():
    return loan_products

@app.post("/products")
def create_product(product: LoanProductCreate):
    if product.min_amount >= product.max_amount or product.min_term >= product.max_term:
        raise HTTPException(status_code=400, detail="Rangos inválidos")
    loan_products.append(product)
    return product

@app.post("/simulate", response_model=LoanSimulationResult)
def simulate(input: LoanSimulationInput):
    # Buscar el producto
    product = next((p for p in loan_products if p["name"] == input.product_name), None)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not (product["min_amount"] <= input.amount <= product["max_amount"]):
        raise HTTPException(status_code=400, detail="Monto fuera de rango")

    if not (product["min_term"] <= input.term <= product["max_term"]):
        raise HTTPException(status_code=400, detail="Plazo fuera de rango")

    monthly = calculate_monthly_payment(input.amount, product["annual_rate"], input.term)
    total = monthly * input.term

    return LoanSimulationResult(monthly_payment=round(monthly, 2), total_cost=round(total, 2))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)