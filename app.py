# app.py

import time
import random
import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("mock-api")

# -------------------------------------------------------------------
# In-Memory Mock Database
# -------------------------------------------------------------------
users: Dict[str, Dict] = {
    "1001": {"name": "Ali Veli", "package": "Premium", "balance": 23.45},
    "1002": {"name": "Ayşe Demir", "package": "Standart", "balance": 0.00},
    "1003": {"name": "Mehmet Can", "package": "Gold", "balance": 120.00},
    "1004": {"name": "Elif Yılmaz", "package": "Silver", "balance": 5.75},
    "1005": {"name": "Berke Kara", "package": "Bronze", "balance": -15.20},
}

packages: Dict[str, Dict] = {
    "Bronze": {"price": 25, "features": ["50 DK Arama", "10 GB İnternet"]},
    "Silver": {"price": 50, "features": ["200 DK Arama", "50 GB İnternet"]},
    "Gold":   {"price": 100, "features": ["Limitsiz Arama", "100 GB İnternet"]},
    "Standart": {"price": 75, "features": ["100 DK Arama", "50 GB İnternet"]},
    "Premium": {"price": 150, "features": ["Limitsiz Arama", "Limitsiz İnternet"]},
}

billing_records: Dict[str, List[Dict]] = {
    "1001": [
        {"month": "2025-06", "amount": 145.00, "paid": True},
        {"month": "2025-07", "amount": 150.00, "paid": False},
    ],
    # ... similar entries for other users
}

usage_stats: Dict[str, Dict] = {
    "1001": {"calls": 120, "data_mb": 20480, "sms": 30},
    # ... similar entries for other users
}

# -------------------------------------------------------------------
# Pydantic Models
# -------------------------------------------------------------------
class StandardResponse(BaseModel):
    status: str = Field(..., example="success")
    data: Optional[Dict] = None
    message: Optional[str] = None

class PackageChangeRequest(BaseModel):
    customer_id: str = Field(..., example="1001")
    new_package: str = Field(..., example="Gold")

class PaymentRequest(BaseModel):
    customer_id: str = Field(..., example="1001")
    month: str = Field(..., example="2025-07")
    amount: float = Field(..., example=150.00)

# -------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------
def simulate_latency(min_ms: int = 50, max_ms: int = 300):
    """Random delay to mimic real API response times."""
    delay = random.uniform(min_ms / 1000, max_ms / 1000)
    time.sleep(delay)

def random_failure(chance: float = 0.05):
    """Randomly raise a 503 to simulate transient errors."""
    if random.random() < chance:
        logger.warning("Simulated downstream service failure")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Geçici hizmet kesintisi, lütfen tekrar deneyin")

# -------------------------------------------------------------------
# FastAPI Initialization
# -------------------------------------------------------------------
app = FastAPI(
    title="Mock Çağrı Merkezi API",
    version="1.0.0",
    description="Test ve geliştirme amaçlı sahte çağrı merkezi servisleri."
)

# -------------------------------------------------------------------
# API Endpoints
# -------------------------------------------------------------------

@app.get("/getUserInfo/{customer_id}", response_model=StandardResponse)
def get_user_info(customer_id: str):
    """Kullanıcı bilgilerini döner."""
    simulate_latency()
    random_failure()
    
    user = users.get(customer_id)
    if not user:
        logger.error(f"getUserInfo: {customer_id} bulunamadı")
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    logger.info(f"getUserInfo: {customer_id} başarıyla getirildi")
    return StandardResponse(status="success", data=user)


@app.get("/getAvailablePackages/{customer_id}", response_model=StandardResponse)
def get_available_packages(customer_id: str):
    """Mevcut paket listesini döner."""
    simulate_latency()
    random_failure()
    
    if customer_id not in users:
        logger.error(f"getAvailablePackages: {customer_id} bulunamadı")
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    logger.info(f"getAvailablePackages: paket listesi sağlandı")
    return StandardResponse(status="success", data=packages)


@app.post("/initiatePackageChange", response_model=StandardResponse)
def initiate_package_change(req: PackageChangeRequest):
    """Kullanıcının paketini değiştirir."""
    simulate_latency()
    random_failure()
    
    user = users.get(req.customer_id)
    if not user:
        logger.error(f"initiatePackageChange: {req.customer_id} bulunamadı")
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    if req.new_package not in packages:
        logger.error(f"initiatePackageChange: {req.new_package} geçersiz")
        raise HTTPException(status_code=400, detail="Paket bulunamadı")
    
    old = user["package"]
    user["package"] = req.new_package
    logger.info(f"{req.customer_id}: {old} → {req.new_package}")
    return StandardResponse(
        status="success",
        message=f"Paket başarıyla {req.new_package} olarak güncellendi"
    )


@app.get("/getBillingInfo/{customer_id}", response_model=StandardResponse)
def get_billing_info(customer_id: str):
    """Müşterinin fatura geçmişini getirir."""
    simulate_latency()
    random_failure()
    
    if customer_id not in users:
        logger.error(f"getBillingInfo: {customer_id} bulunamadı")
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    records = billing_records.get(customer_id, [])
    logger.info(f"getBillingInfo: {customer_id} için {len(records)} kayıt bulundu")
    return StandardResponse(status="success", data={"bills": records})


@app.get("/getUsageStats/{customer_id}", response_model=StandardResponse)
def get_usage_stats(customer_id: str):
    """Müşteri kullanım istatistiklerini döner."""
    simulate_latency()
    random_failure()
    
    if customer_id not in users:
        logger.error(f"getUsageStats: {customer_id} bulunamadı")
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    stats = usage_stats.get(customer_id, {"calls": 0, "data_mb": 0, "sms": 0})
    logger.info(f"getUsageStats: {customer_id} istatistik gönderildi")
    return StandardResponse(status="success", data=stats)


@app.post("/payBill", response_model=StandardResponse)
def pay_bill(req: PaymentRequest):
    """Fatura ödemesi gerçekleştirir."""
    simulate_latency()
    random_failure()
    
    user = users.get(req.customer_id)
    if not user:
        logger.error(f"payBill: {req.customer_id} bulunamadı")
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    # Fatura kaydı güncellemesi (mock)
    bills = billing_records.setdefault(req.customer_id, [])
    for bill in bills:
        if bill["month"] == req.month:
            if bill["paid"]:
                raise HTTPException(status_code=409, detail="Fatura zaten ödenmiş")
            if abs(bill["amount"] - req.amount) > 0.01:
                raise HTTPException(status_code=400, detail="Tutar uyuşmuyor")
            bill["paid"] = True
            user["balance"] -= req.amount
            logger.info(f"{req.customer_id}: {req.month} faturası ödendi")
            return StandardResponse(status="success", message="Fatura ödendi")
    
    raise HTTPException(status_code=404, detail="Fatura bulunamadı")


# -------------------------------------------------------------------
# Uvicorn ile Çalıştırma
# -------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)