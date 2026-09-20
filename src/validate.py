import pandas as pd

# BASIC VALIDATION

def validateEmptyDataFrame(dataset: dict[str, pd.DataFrame]) -> None:
    for name, df in dataset.items():
        if df.empty:
            raise ValueError(f"Dataset '{name}' is empty")


PRIMARY_KEYS = {
    "orders": ["order_id"],
    "customers": ["customer_id"],
    "products": ["product_id"],
    "sellers": ["seller_id"],
    "order_items": ["order_id", "order_item_id"],
    "order_payments": ["order_id", "payment_sequential"],
    "order_reviews": ["order_id","review_id"],
    "category_translation": ["product_category_name"],
    "geolocation": None
}

def validatePrimaryKey(dataset: dict[str, pd.DataFrame]) -> None:
    for datasetName, keyCol in PRIMARY_KEYS.items():
        if keyCol is None:
            continue
        df = dataset[datasetName]
        duplicateCount = df.duplicated(
            subset = keyCol
        ).sum()

        if duplicateCount > 0:
            raise ValueError (f"{datasetName} contain {duplicateCount} duplicate PrimaryKey record")

def validateOrderItems(orderItems: pd.DataFrame) -> None:
    negativePrices = (orderItems["price"] < 0).sum()
    negativeFreight = (orderItems["freight_value"] < 0).sum()

    if negativePrices > 0:
        raise ValueError(f"Found {negativePrices} negative prices.")

    if negativeFreight > 0:
        raise ValueError(f"Found {negativeFreight} negative freight values.")
    
def validateReviews(reviews: pd.DataFrame) -> None:

    invalidScores = (~reviews["review_score"].between(1, 5)).sum()

    if invalidScores > 0:
        raise ValueError(f"Found {invalidScores} invalid review scores.")
    
def validateOrders(order: pd.DataFrame) -> None:
    missingDeliveryDate = order.loc[
        (order['order_status'] == 'delivered') & 
        (order['order_delivered_customer_date'].isna())
    ]
    print(f"Anomalies: {len(missingDeliveryDate)} Missing Delivery Date in Delivered Orders")

    deliveredMask = (
        (order['order_status'] == 'delivered') &
        (order['order_delivered_customer_date'].notna())
    )
    
    deliveredCount = deliveredMask.sum()
    print(f"Delivered Orders: {deliveredCount}")

    if deliveredCount > 0:
        lateDeliveredOrder = order.loc[
            deliveredMask & (order["delivery_delay_days"] > 0)
        ]
        lateDeliveredRate = (len(lateDeliveredOrder) / deliveredCount) * 100
        print(f"Late Delivery Rate: {lateDeliveredRate:.2f}%")
    else:
        print("Late Delivery Rate: N/A (No delivered orders)")

def validateRelationships(datasets: dict[str, pd.DataFrame]) -> None:

    orders = datasets["orders"]
    customers = datasets["customers"]
    orderItems = datasets["order_items"]
    products = datasets["products"]
    sellers = datasets["sellers"]

    missingCustomers = (
        set(orders["customer_id"])
        - set(customers["customer_id"])
    )

    missingOrders = (
        set(orderItems["order_id"])
        - set(orders["order_id"])
    )
    missingProducts = (
        set(orderItems["product_id"])
        - set(products["product_id"])
    )

    missingSellers = (
        set(orderItems["seller_id"])
        - set(sellers["seller_id"])
    )
    if missingCustomers:
        raise ValueError(
            f"Found {len(missingCustomers)} "
            "orders with missing customers."
        )

    if missingOrders:
        raise ValueError(
            f"Found {len(missingOrders)} "
            "order items with missing orders."
        )

    if missingProducts:
        raise ValueError(
            f"Found {len(missingProducts)} "
            "order items with missing products."
        )

    if missingSellers:
        raise ValueError(
            f"Found {len(missingSellers)} "
            "order items with missing sellers."
        )
    
# --------- COMPLETE VALIDATION ----------
def validateAll(dataset: dict[str, pd.DataFrame]) -> None:
    print("\nStarting data validation...")

    validateEmptyDataFrame(dataset)
    validatePrimaryKey(dataset)
    validateOrders(dataset["orders"])
    validateOrderItems(dataset["order_items"])
    validateReviews(dataset["order_reviews"])
    validateRelationships(dataset)

    print("Data validation completed successfully.")
