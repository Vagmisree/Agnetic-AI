import streamlit as st

class Chatbot:
    @staticmethod
    def run_chatbot_page(dataset_preview: str):
        st.title("🤖 Retail Simulation Chatbot")

        st.markdown("Ask about stock levels, robots, or dataset info.")
        st.subheader("📄 Dataset Preview")
        if dataset_preview:
            st.text_area("Preview", dataset_preview[:1000], height=200)
        else:
            st.info("Upload a dataset first.")

        quick_qs = {
            "Robot status": "All robots are active and assigned tasks efficiently.",
            "Low stock shelves": "Shelves S02, S04, and S05 are below reorder threshold.",
            "Completed tasks": "5 out of 10 restocking tasks are completed.",
            "Stock summary": "Overall shelf stock is stable with 10% below limit.",
            "Dataset preview": dataset_preview[:300] if dataset_preview else "Upload data to preview.",
        }

        st.subheader("💬 Quick Questions")
        cols = st.columns(3)
        keys = list(quick_qs.keys())
        for i, col in enumerate(cols):
            for j in range(i, len(keys), 3):
                if col.button(keys[j]):
                    st.session_state["answer"] = quick_qs[keys[j]]

        if "answer" in st.session_state:
            st.text_area("Chatbot Answer", st.session_state["answer"], height=250)

        query = st.text_input("Type your question:")
        if query:
            query_lower = query.lower()
            for key, ans in quick_qs.items():
                if key.lower() in query_lower:
                    st.session_state["answer"] = ans
                    break
            else:
                st.session_state["answer"] = "I'm trained for quick queries. Try one of the buttons!"
