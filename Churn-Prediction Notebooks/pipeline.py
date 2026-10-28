import pickle
import pandas as pd
import numpy as np
from supabase import create_client, Client
from sklearn.preprocessing import LabelEncoder

# ---------------- SUPABASE ----------------
SUPABASE_URL = "https://mjeqrfkesqgheynybtta.supabase.co"
SUPABASE_KEY = "sb_publishable_vMTMBHF6sL2fcsvJwWEung_Du1-kyMI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- LOAD MODEL ----------------
with open("churn.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------- FETCH DATA ----------------
def fetch_table(table_name):
    resp = supabase.table(table_name).select("*").execute()
    if resp.data:
        return pd.DataFrame(resp.data)
    else:
        return pd.DataFrame()

users_df = fetch_table("User")
orders_df = fetch_table("Order")
order_items_df = fetch_table("OrderItem")
products_df = fetch_table("Product")
reviews_df = fetch_table("Review")
sessions_df = fetch_table("UserSession")

df = users_df.copy()

# ---------------- FEATURE ENGINEERING ----------------
# Tenure in days
df["Tenure"] = (pd.Timestamp.now(tz='UTC') - pd.to_datetime(df["joinedat"])).dt.days

# ---------------- RANDOM DEFAULTS ----------------
np.random.seed(42)  # reproducible random values

# PreferredLoginDevice
df["PreferredLoginDevice"] = np.random.choice(["Mobile","Desktop","Tablet"], size=len(df))

# CityTier
tier_map = {"Tier1City":1, "Tier2City":2, "Tier3City":3}
if "city" in df.columns:
    df["CityTier"] = df["city"].map(tier_map)
    mask = df["CityTier"].isna()
    df.loc[mask, "CityTier"] = np.random.choice([1,2,3], size=mask.sum())
else:
    df["CityTier"] = np.random.choice([1,2,3], size=len(df))

# WarehouseToHome
df["WarehouseToHome"] = np.random.randint(3,15,size=len(df))

# PreferredPaymentMode
df["PreferredPaymentMode"] = np.random.choice(["UPI","DC","Credit Card","Cash"], size=len(df))

# Gender
df["Gender"] = np.random.choice(["Male","Female","Other"], size=len(df))

# NumberOfDeviceRegistered
df["NumberOfDeviceRegistered"] = np.random.randint(1,5,size=len(df))

# SatisfactionScore
if not reviews_df.empty:
    avg_rating = reviews_df.groupby("userid")["rating"].mean().reset_index()
    df = df.merge(avg_rating, left_on="auth_id", right_on="userid", how="left")
    df["SatisfactionScore"] = df["rating"].fillna(np.random.randint(1,6))
else:
    df["SatisfactionScore"] = np.random.randint(1,6,size=len(df))

# MaritalStatus
df["MaritalStatus"] = np.random.choice(["Single","Married","Divorced"], size=len(df))

# NumberOfAddress
df["NumberOfAddress"] = np.random.randint(1,10,size=len(df))

# Complain
df["Complain"] = np.random.choice([0,1], size=len(df))

# DaySinceLastOrder
df["DaySinceLastOrder"] = np.random.randint(1,20,size=len(df))

# CashbackAmount
df["CashbackAmount"] = np.round(np.random.uniform(0,200,size=len(df)),2)

# PreferedOrderCat
df["PreferedOrderCat"] = np.random.choice(
    ["Power Backup","Washing Machines & Dryers","Air Conditioners","Blenders & Juicers"], 
    size=len(df)
)

# ---------------- ENCODE CATEGORICAL FOR MODEL ----------------
cat_cols = ["PreferredLoginDevice","PreferredPaymentMode","Gender","MaritalStatus","PreferedOrderCat"]
encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col + "_enc"] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

# ---------------- SELECT FEATURES ----------------
feature_cols = ["Tenure","PreferredLoginDevice_enc","CityTier","WarehouseToHome",
                "PreferredPaymentMode_enc","Gender_enc","NumberOfDeviceRegistered",
                "SatisfactionScore","MaritalStatus_enc","NumberOfAddress",
                "Complain","DaySinceLastOrder","CashbackAmount","PreferedOrderCat_enc"]

X = df[feature_cols]

# ---------------- PREDICT ----------------
df["Churn"] = model.predict(X)

# ---------------- SAVE FINAL CSV ----------------
final_cols = ["Churn","Tenure","PreferredLoginDevice","CityTier","WarehouseToHome",
              "PreferredPaymentMode","Gender","NumberOfDeviceRegistered","SatisfactionScore",
              "MaritalStatus","NumberOfAddress","Complain","DaySinceLastOrder","CashbackAmount",
              "PreferedOrderCat"]

df[final_cols].to_csv("churn_predictions.csv", index=False)
print("Final CSV saved with random realistic data and churn predictions.")
