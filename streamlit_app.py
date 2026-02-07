import streamlit as st
import requests
import pandas as pd

API_URL = "https://corep-backend.onrender.com/report"

st.set_page_config(page_title="COREP Assistant", layout="wide")

st.title("📊 COREP Regulatory Reporting Assistant")

query = st.text_area(
    "Enter reporting scenario:",
    height=120
)

template_option = st.selectbox(
    "Select Template",
    ["C01.00 – Own Funds", "C02.00 – Capital Requirements"]
)

if st.button("Generate Report"):

    if not query:
        st.warning("Enter a scenario.")
        st.stop()

    with st.spinner("Generating..."):

        res = requests.post(
            API_URL,
            params={"query": query}
        )

        if res.status_code != 200:
            st.error("API Error")
            st.stop()

        data = res.json()

    # =========================
    # TEMPLATE TABLE
    # =========================

    st.subheader("📄 Template Extract")

    df = pd.DataFrame(data["template_extract"])

    st.dataframe(df, use_container_width=True)

    # Export button
    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False),
        "corep_template.csv"
    )

    # =========================
    # CONFIDENCE BADGES
    # =========================

    st.subheader("🧠 Confidence")

    for field in data["structured_output"]["fields"]:
        st.success(
            f"{field['label']} → High confidence"
        )

    # =========================
    # MISSING DATA
    # =========================

    missing = data["structured_output"]["missing_data"]

    if missing:
        st.warning("⚠ Missing Data:")
        for m in missing:
            st.write(m)

    # =========================
    # VALIDATION FLAGS
    # =========================

    flags = data["structured_output"]["validation_flags"]

    if flags:
        st.error("🚨 Validation Issues:")
        for f in flags:
            st.write(f)

    # =========================
    # AUDIT LOG
    # =========================

    st.subheader("📜 Audit Log")

    for rule in data["audit_log"]:
        st.info(rule)
