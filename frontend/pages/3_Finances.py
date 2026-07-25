from datetime import date

import streamlit as st

from api_client import create_transaction, delete_transaction, get_finance_balance, list_transactions

st.set_page_config(page_title="Finances — TrackItAll", layout="wide")
st.title("Finances")

balance = float(get_finance_balance()["balance"])
st.metric("Solde", f"{balance:.2f} €")

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
    for transaction in reversed(transactions):
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
                sign = "+" if transaction["type"] == "income" else "-"
                st.markdown(f"**{sign}{transaction['amount']} €**")
            with col3:
                if st.button(
                    "🗑️", key=f"delete_{transaction['id']}", use_container_width=True
                ):
                    delete_transaction(transaction["id"])
                    st.rerun()
