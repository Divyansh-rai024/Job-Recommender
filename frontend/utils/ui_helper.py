import streamlit as st

def display_results(results):
    st.subheader("🔍 Top Recommendations")
    for res in results:
        st.markdown(f"### [{res['name']}]({res['url']})")
        st.markdown(f"- **Type**: {res['type']}")
        st.markdown(f"- **Duration**: {res['duration']}")
        st.markdown(f"- **Remote**: {res['remote']} | Adaptive: {res['adaptive']}")
        st.markdown(f"- **Description**: {res['description']}")
        st.markdown("---")
