import streamlit as st
import requests
st.set_page_config(page_title="Intelligent IT Support Agent", page_icon="🛠️", layout="wide")
st.title("🛠️ Intelligent IT Support Agent")
st.caption("ML ticket classification · RAG retrieval · LangGraph workflow · simulated diagnostics")
api_url = st.sidebar.text_input("API base URL", "http://127.0.0.1:8000")
with st.form("ticket_form"):
    title = st.text_input("Ticket title", "VPN login fails after password reset")
    description = st.text_area("Describe the issue", "I cannot connect to the corporate VPN. It says authentication failed after I changed my password.", height=130)
    submitted = st.form_submit_button("Analyze ticket", type="primary")
if submitted:
    try:
        r = requests.post(f"{api_url.rstrip('/')}/tickets/analyze", json={"title": title, "description": description}, timeout=180)
        r.raise_for_status(); result = r.json()
        c1, c2 = st.columns(2)
        c1.metric("Predicted category", result["predicted_category"])
        c1.metric("Confidence", f"{result['category_confidence']:.1%}")
        c2.metric("Suggested priority", result["priority"])
        c2.info(result["recommendation"].replace("_", " ").title())
        st.subheader("Suggested response"); st.write(result["response"])
        st.subheader("Retrieved evidence")
        for s in result["sources"]:
            with st.expander(f"{s['title']} · {s['source']} · score {s['score']:.3f}"): st.write(s["excerpt"])
        st.subheader("Simulated diagnostics"); st.json(result["diagnostics"])
        st.subheader("Workflow audit trail")
        for entry in result["audit_trail"]: st.write("• " + entry)
        st.caption(result["disclaimer"])
    except requests.RequestException as exc:
        st.error(f"Could not call API. Start FastAPI first. Details: {exc}")
