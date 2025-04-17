import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File path for the trade log
log_file = "pnl_log.csv"

# Load data
if not os.path.exists(log_file):
    st.warning("No trade data found yet.")
    st.stop()

df = pd.read_csv(log_file, names=[
    "Timestamp", "Symbol", "Direction", "Entry", "Exit", "PnL", "Result", "Reason"
])

# Convert timestamps
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Layout
st.title("🧠 AI Quant Bot Dashboard")
st.subheader("📊 Executed Trades")

# Data table
st.dataframe(df[::-1], use_container_width=True)

# Summary Stats
st.subheader("📈 Summary Stats")
total_pnl = df["PnL"].sum()
num_trades = len(df)
wins = len(df[df["Result"] == "WIN"])
losses = len(df[df["Result"] == "LOSS"])
win_rate = (wins / num_trades) * 100 if num_trades > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total PnL", f"${total_pnl:.2f}")
col2.metric("Win Rate", f"{win_rate:.1f}%")
col3.metric("Total Trades", f"{num_trades}")
col4.metric("Wins / Losses", f"{wins} / {losses}")

# Equity Curve
st.subheader("📉 Equity Curve")

df["CumulativePnL"] = df["PnL"].cumsum()

fig, ax = plt.subplots()
ax.plot(df["Timestamp"], df["CumulativePnL"], marker='o', linestyle='-')
ax.set_xlabel("Time")
ax.set_ylabel("Cumulative PnL")
ax.set_title("Equity Growth Over Time")
ax.grid(True)
st.pyplot(fig)
