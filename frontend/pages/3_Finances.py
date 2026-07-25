from datetime import date

import streamlit as st

from api_client import create_transaction, delete_transaction, get_finance_balance, list_transactions
from chart_theme import GRIDLINE, MUTED_INK, NEGATIVE, POSITIVE, SURFACE

st.set_page_config(page_title="Finances — TrackItAll", layout="wide")
st.title("Finances")

balance = float(get_finance_balance()["balance"])
balance_color = NEGATIVE if balance < 0 else POSITIVE
sign = "" if balance < 0 else "+"
st.markdown(
    f"""
    <div style="
        padding: 1.5rem 1.75rem;
        border-radius: 14px;
        background-color: {SURFACE};
        border: 1px solid {GRIDLINE};
        margin-bottom: 1.5rem;
    ">
        <div style="color: {MUTED_INK}; font-size: 0.8rem; text-transform: uppercase;
                    letter-spacing: 0.08em; margin-bottom: 0.35rem;">Solde</div>
        <div style="color: {balance_color}; font-size: 2.5rem; font-weight: 650;
                    font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;">
            {sign}{balance:.2f} €
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

type_labels = {"income": "Revenu", "expense": "Dépense"}

with st.form("create_transaction_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        transaction_date = st.date_input("Date", value=date.today())
    with col2:
        amount = st.number_input("Montant", min_value=0.01, step=0.01, format="%.2f")
    with col3:
        transaction_type = st.selectbox(
            "Type", ["income", "expense"], format_func=lambda t: type_labels[t]
        )
    category = st.text_input("Catégorie")
    description = st.text_area("Description", placeholder="Optionnel")
    submitted = st.form_submit_button("Ajouter la transaction", use_container_width=True)

    if submitted:
        if not category.strip():
            st.error("La catégorie est obligatoire.")
        else:
            create_transaction(
                date=transaction_date.isoformat(),
                amount=str(amount),
                type=transaction_type,
                category=category,
                description=description or None,
            )
            st.success("Transaction ajoutée.")
            st.rerun()

st.divider()
st.subheader("Transactions")

transactions = list_transactions()
type_icons = {"income": "🟢", "expense": "🔴"}

if not transactions:
    st.info("Aucune transaction pour l'instant — ajoute-en une ci-dessus.")
else:
    for transaction in sorted(transactions, key=lambda t: t["date"], reverse=True):
        amount_color = POSITIVE if transaction["type"] == "income" else NEGATIVE
        amount_sign = "+" if transaction["type"] == "income" else "-"
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(
                    f"{type_icons[transaction['type']]} **{transaction['category']}**"
                )
                if transaction["description"]:
                    st.caption(transaction["description"])
                st.caption(transaction["date"])
            with col2:
                st.markdown(
                    f"<div style='color: {amount_color}; font-weight: 600; font-size: 1.1rem; "
                    f"text-align: right; padding-top: 0.4rem;'>"
                    f"{amount_sign}{transaction['amount']} €</div>",
                    unsafe_allow_html=True,
                )
            with col3:
                if st.button(
                    "🗑️", key=f"delete_{transaction['id']}", use_container_width=True
                ):
                    delete_transaction(transaction["id"])
                    st.rerun()
