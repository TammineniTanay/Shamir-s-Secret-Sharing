import streamlit as st
from sss import create_shares, reconstruct_secret

st.title("🔐 Shamir's Secret Sharing Demo")
st.write("Split a secret into multiple parts using 127-bit prime field math.")

# Input Section
secret = st.number_input("Enter a Secret (Integer)", value=12345)
t = st.slider("Threshold (K)", 2, 10, 3)
n = st.slider("Total Shares (N)", t, 15, 5)

if st.button("Generate Shares"):
    shares = create_shares(secret, t, n)
    st.success(f"Generated {n} shares. You need {t} to recover the secret.")
    st.write(shares)

# Recovery Section
st.subheader("Recover Secret")
input_shares = st.text_area("Paste shares here (e.g., [(1, y1), (2, y2)])")
if st.button("Decrypt"):
    try:
        recovered = reconstruct_secret(eval(input_shares))
        st.balloons()
        st.write(f"Original Secret: **{recovered}**")
    except Exception as e:
        st.error(f"Error: {e}")