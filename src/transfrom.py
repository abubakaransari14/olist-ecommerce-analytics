import pandas as pd

# ----------- TRANSFORM ORDER -------------
def transformOrder(orders : pd.DataFrame) -> pd.DataFrame:
    """
    Convert Date Columns
    """
    df = orders.copy()
    dateColumns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in dateColumns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # STANDARDIZE ORDER STATUS
    df["order_status"] = (
        df["order_status"].astype('string')
        .str.strip()
        .str.lower()
    )

    # DELIVERY DURATION
    
    df["delivery_days"] = (
        df["order_delivered_customer_date"]  -
        df["order_purchase_timestamp"]
    ).dt.total_seconds() / (24*60*60)

    #  DELIVERY DELAY 
    
    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"] -
        df["order_estimated_delivery_date"]
    ).dt.total_seconds() / (24*60*60)

    # LATE DELIVERY FLAG
    
    df["is_late"] = (
        df["delivery_delay_days"] > 0
    )

    # DELIVERY STATUS

    df["delivery_status"] = "Not Delivered"


    deliveredMask = (
            (df['order_status']=='delivered') &
            (df['order_delivered_customer_date'].notna())
    )


    df.loc[deliveredMask & (df["is_late"] == True),
           "delivery_status"] = "Late"

    df.loc[deliveredMask & (df["is_late"] == False),
            "delivery_status"] = "On Time"

    return df

# ------------ CUSTOMERS TRANSFORMATION ---------
def transformCustomer(customers: pd.DataFrame) -> pd.DataFrame:

    df = customers.copy()

    # STANDARDIZE TEXT COLUMNS
    textColumns = ["customer_city","customer_state"]
    for col in textColumns:
        df[col] = (
            df[col].astype("string").str.strip()
        )

    # STATE TO UPPERCASE
    df['customer_state'] = (
        df['customer_state'].str.upper()
    )

    # CONVERT ZIP CODE TO STRING
    df["customer_zip_code_prefix"] = (
        pd.to_numeric(
            df["customer_zip_code_prefix"],
            errors="coerce"
        )
        .astype("Int64")
        .astype("string")
    )

    return df

# ---------- ORDER ITEMS TRANSFORMATION ----------
def transformOrderItems(orderItems: pd.DataFrame) -> pd.DataFrame:

    df = orderItems.copy()

    # CONVERT SHIPPING DATE
    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="coerce"
    )

    # NUMERIC CONVERSITION
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["freight_value"] = pd.to_numeric(
        df["freight_value"],
        errors="coerce"
    )

    # Item total
    df["item_total_value"] = (
        df["price"]
        + df["freight_value"]
    )

    return df

# ----------- PRODUCTS TRANSFORMATION ---------
def transformProducts(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()

    df["product_category_name"] = (
        df["product_category_name"]
        .astype("string")
        .str.strip()
    )

    numericColumns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    for column in numericColumns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df

# ----------- REVIEWS TRANSFORMATION ---------
def transformReviews(reviews: pd.DataFrame) -> pd.DataFrame:
    df = reviews.copy()

    dateColumns = [
        "review_creation_date",
        "review_answer_timestamp"
    ]

    for column in dateColumns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    df["review_score"] = pd.to_numeric(
        df["review_score"],
        errors="coerce"
    )

    # Clean review text
    textColumns = [
        "review_comment_title",
        "review_comment_message"
    ]

    for column in textColumns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df

# ----------- PAYMENTS TRANSFORMATION ---------
def transformPayment(payments: pd.DataFrame) -> pd.DataFrame:
    df = payments.copy()

    df["payment_type"] = (
        df["payment_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df["payment_value"] = pd.to_numeric(
        df["payment_value"],
        errors="coerce"
    )

    df["payment_installments"] = pd.to_numeric(
        df["payment_installments"],
        errors="coerce"
    )

    return df

# ----------- SELLERS TRANSFORMATION ---------
def transformSeller(sellers: pd.DataFrame) -> pd.DataFrame:
    df = sellers.copy()

    df["seller_city"] = (
        df["seller_city"]
        .astype("string")
        .str.strip()
    )

    df["seller_state"] = (
        df["seller_state"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    return df

# --------- GEOLOCATION TRANSFORMATION ----------
def transformGeoLocation(geoLocation: pd.DataFrame) -> pd.DataFrame:

    df = geoLocation.copy()

    # Rename columns to cleaner names
    df = df.rename(
        columns={
            "geolocation_zip_code_prefix":
                "zip_code_prefix",
            "geolocation_lat":
                "latitude",
            "geolocation_lng":
                "longitude",
            "geolocation_city":
                "city",
            "geolocation_state":
                "state"
        }
    )

    # Standardize text
    df["city"] = (
        df["city"]
        .astype("string")
        .str.strip()
    )

    df["state"] = (
        df["state"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Numeric coordinates
    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    return df

# ---------- CATEGORY TRANSLATION --------------
def transformCategoryTranslation(categoryTranslation: pd.DataFrame) -> pd.DataFrame:

    df = categoryTranslation.copy()

    df["product_category_name"] = (
        df["product_category_name"]
        .astype("string")
        .str.strip()
    )

    df["product_category_name_english"] = (
        df["product_category_name_english"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    return df



# ------------ Merge Functions ------------ 

# -------- MERGE THE CUSTOMER AND ORDERS ------------
def mergeCustomerOrder(orderDF: pd.DataFrame, customerDF: pd.DataFrame) -> pd.DataFrame:
    """
    Merges cleaned orders data with selected cleaned customer columns.
    """
    customerSubset = customerDF[["customer_id","customer_state","customer_city"]]

    customerOrderEDA = orderDF.merge(
        customerSubset,
        on="customer_id",
        how="left"
    )

    return customerOrderEDA

# ---------- ORDERITEMS AGGREGATION -----------
def aggregateOrderItem (orderItemsDF: pd.DataFrame) -> pd.DataFrame:
    orderTotal = (
        orderItemsDF.groupby("order_id")
        .agg(
            total_price=("price", "sum"),
            total_freight=("freight_value", "sum"),
            total_value=("item_total_value", "sum"),
            item_count = ("order_item_id", "count")
        )
        .reset_index()
    )
    return orderTotal

# ----------- mergeCustomerOrder WITH ORDER ITEM AGGREGATE ---------
def mergeCOwithAggOrderItem(customerOrdersDF: pd.DataFrame, 
                             orderItemsDF: pd.DataFrame) -> pd.DataFrame:
    """
    Merges aggregated order item financial totals with customer-order data.
    """
    orderTotals = aggregateOrderItem(orderItemsDF)
    
    customerOrderSale = customerOrdersDF.merge(
        orderTotals,
        on="order_id",
        how="left"
    )
    
    return customerOrderSale

# ---------- PRODUCT AND ORDERITEM WITH mergeCOwithAggOrderItem
def mergePrdouctOrderItemCOAgg ( 
        coAggOrdItem: pd.DataFrame, 
        orderItem: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
    
    customerOrderSubset = coAggOrdItem[[
        "order_id", "order_status", 
        "customer_state","customer_city"]]
    
    productSubset = product[["product_id","product_category_name"]]

    orderItemEDA = orderItem.merge(
            productSubset,
            on="product_id",
            how="left"
        ).merge(
            customerOrderSubset,
            on="order_id",
            how="left"
        )
    return orderItemEDA

# ---------Master - mergeCustomerOrder WITH REVIEWS -------
def mergeCOAggWithReviews(coAggDF: pd.DataFrame, reviewsDF: pd.DataFrame) -> pd.DataFrame:

    # reviewsSubset = reviewsDF[["order_id", "review_score"]]
    reviewsSubset = (
        reviewsDF.groupby("order_id")["review_score"]
        .mean()
        .reset_index()
    )

    masterOrder = coAggDF.merge(
        reviewsSubset,
        on = "order_id",
        how = "left"
    )

    return masterOrder

# ---------Master - mergePrdouctOrderItemCOAgg WITH PAYMENT AND SELLER ------
def mergeProdOrdItemCOAggPayAndSell(prodOrdItemCOAgg: pd.DataFrame, 
        payment: pd.DataFrame, seller: pd.DataFrame ) -> pd.DataFrame:

        paymentSubset = payment[["order_id","payment_type"]]
        sellerSubset = seller[["seller_id","seller_city","seller_state"]]

        masterOrderItem = prodOrdItemCOAgg.merge(
           paymentSubset,
           on = 'order_id',
           how = 'left' 
        ).merge(
            sellerSubset,
            on = 'seller_id',
            how = 'left'
        )

        return masterOrderItem

# ------- COMPLETE TRANSFORMATION ---------------
def transformAll(dataset : dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:

    transformed = {}

    # 1. CLEANED INDIVISUAL DATASET
    transformed["orders"] = transformOrder(dataset["orders"])
    transformed["customers"] = transformCustomer(dataset["customers"])
    transformed["order_items"] = transformOrderItems(dataset["order_items"])
    transformed["order_payments"] = transformPayment(dataset["order_payments"])
    transformed["order_reviews"] = transformReviews(dataset["order_reviews"])
    transformed["products"] = transformProducts(dataset["products"])
    transformed["sellers"] = transformSeller(dataset["sellers"])
    transformed["category_translation"] = transformCategoryTranslation(dataset["category_translation"]
    )
    transformed["geolocation"] = transformGeoLocation(dataset["geolocation"])

    # 2. MERGED ANALYTTICAL DATASET
    
    # A. CUSTOMER ORDER TABLE (Order Level)
    customerOrderDF = mergeCustomerOrder(
        transformed["orders"], 
        transformed["customers"]
    )

    # B. ORDER CUSTOMER AGG (OrdersCustomer + Aggregated Items)
    coAgg = mergeCOwithAggOrderItem(
        customerOrderDF, 
        transformed["order_items"]
    )

    # C. ORDER ITME WITH PRODUCT AND CUSTOMERORDERAGGREGATE
    prodItemCO = mergePrdouctOrderItemCOAgg(
        coAgg,
        transformed["order_items"],
        transformed["products"]
    )

    # Master - Level Table 
    transformed["master_orders"] = mergeCOAggWithReviews(
            coAgg, 
            transformed["order_reviews"]
        )

    transformed["master_order_items"] = mergeProdOrdItemCOAggPayAndSell(
        prodItemCO,
        transformed["order_payments"],
        transformed["sellers"]
    )

    print("\nAll datasets transformed and merged successfully.")

    return transformed
