import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import run_agent

st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="🏢",
    layout="centered",
)

st.title("🏢 HR Policy Assistant")
st.caption("Ask about HR policies, employee profiles, leave balances, or raise a grievance.")
st.divider()

#  Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # LangChain message objects for agent memory

if "messages" not in st.session_state:
    st.session_state.messages = []      

# Render existing messages 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("tools_used"):
            tools_str = " · ".join(f"`{t}`" for t in msg["tools_used"])
            st.caption(f"🛠️ Tools used: {tools_str}")

# Chat input
user_input = st.chat_input("Ask about policies, employee info, or raise an HR request…")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response = run_agent(
                user_input=user_input,
                chat_history=st.session_state.chat_history,
            )

        answer     = response["answer"]
        tools_used = response["tools_used"]

        st.markdown(answer)
        if tools_used:
            tools_str = " · ".join(f"`{t}`" for t in tools_used)
            st.caption(f"🛠️ Tools used: {tools_str}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "tools_used": tools_used,
    })

    # Update LangChain memory
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(AIMessage(content=answer))

# Sidebar 
with st.sidebar:
    st.header("Options")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.messages     = []
        st.rerun()

    st.divider()
    st.markdown("**What you can ask:**")
    st.markdown(
        "- Leave / WFH / Attendance policy\n"
        "- Benefits, salary, reimbursements\n"
        "- Resignation & notice period\n"
        "- POSH / Code of conduct\n"
        "- Employee profile: `EMP001`\n"
        "- Leave balance: `EMP001`\n"
        "- Raise a grievance or complaint\n"
        "- HR contact details"
    )