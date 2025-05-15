# --- Pydantic Models for Structured Output ---
# These models define the expected JSON structure.
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    item_total: Optional[float] = None

    class Config:
        # For Pydantic V1, use allow_population_by_field_name = True if using aliases
        # For Pydantic V2, populate_by_name = True (in model_config dict)
        pass

class InvoiceMetadata(BaseModel):
    issue_date: Optional[str] = None # Expected format YYYY-MM-DD (LLM should handle conversion)
    order_id: Optional[str] = None
    document_type: Optional[str] = "Invoice"
    description: Optional[str] = None # Summary of the invoice

class SellerDetails(BaseModel):
    name: Optional[str] = None

class CustomerDetails(BaseModel):
    # Using aliases to match the exact keys from your specification if they contain dots.
    # Pydantic field names cannot contain dots.
    bill_to_name: Optional[str] = Field(default=None, alias="bill_to.name")
    ship_to_city: Optional[str] = Field(default=None, alias="ship_to.city")
    ship_to_region: Optional[str] = Field(default=None, alias="ship_to.region")
    ship_to_country: Optional[str] = Field(default=None, alias="ship_to.country")

    class Config:
        # Pydantic V2 model_config example:
        # model_config = {'populate_by_name': True}
        # Pydantic V1 Config class:
        allow_population_by_field_name = True


class ShippingDetails(BaseModel):
    ship_mode: Optional[str] = None
    shipping_cost: Optional[float] = None

class Financials(BaseModel):
    subtotal: Optional[float] = None
    shipping_total: Optional[float] = None
    total_amount_due: Optional[float] = None
    balance_due: Optional[float] = None
    line_items: Optional[List[LineItem]] = None

class AdditionalInfo(BaseModel):
    additional_info_json_string: Optional[str] = Field(default=None, description="A JSON string containing any additional notes, terms, etc.")


class InvoiceSchema(BaseModel): # This is the main schema for the entire invoice
    invoice_metadata: Optional[InvoiceMetadata] = None
    seller_details: Optional[SellerDetails] = None
    customer_details: Optional[CustomerDetails] = None
    shipping_details: Optional[ShippingDetails] = None
    financials: Optional[Financials] = None
    additional_info: Optional[AdditionalInfo] = None
    class Config:
        # Pydantic V2 model_config example:
        # model_config = {'populate_by_name': True}
        # Pydantic V1 Config class:
        allow_population_by_field_name = True