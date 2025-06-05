import streamlit as st
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="FICE - Find Inaccurate Credit Errors",
    page_icon="🧠",
    layout="centered"
)

# Title and introduction
st.title("🧠 FICE")
st.subheader("Find Inaccurate Credit Errors")

st.markdown("""
**FICE** (Find Inaccurate Credit Errors) is an automated agent designed to search for and identify errors on consumer credit reports.

With FICE, you can:
- 🔍 Detect inaccurate, outdated, or unverifiable account information  
- 📊 Highlight reporting violations or discrepancies  
- 🧾 Generate reports to support dispute letters  
- ⚖️ Stay informed and aligned with your FCRA rights

---

### 📤 Upload Your Credit Report
Please upload your credit report as a **CSV file** exported from your credit monitoring service.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your credit report (CSV only)", type=["csv"])

# When file is uploaded
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        
        st.markdown("### 🔍 Preview of Uploaded Data")
        st.dataframe(df.head())

        # Check for typical error keywords in a 'Status' or similar column
        st.markdown("### ⚠️ Error Scan Results")

        keyword_list = ["late", "collection", "charge off", "charged off", "default", "repossession", "foreclosure"]
        potential_issues = pd.DataFrame()

        # Auto-detect status-related column
        status_col = None
        for col in df.columns:
            if "status" in col.lower() or "remark" in col.lower():
                status_col = col
                break

        if status_col:
            df[status_col] = df[status_col].astype(str).str.lower()
            potential_issues = df[df[status_col].str.contains('|'.join(keyword_list), na=False)]

            if not potential_issues.empty:
                st.warning("The following accounts may be inaccurate or contain negative reporting:")
                st.dataframe(potential_issues)
            else:
                st.success("✅ No major negative indicators found in the selected column.")
        else:
            st.error("⚠️ No recognizable 'Status' or 'Remarks' column found. Please make sure your CSV contains one.")

    except Exception as e:
        st.error(f"❌ An error occurred while reading the file: {e}")

else:
    st.info("Please upload a file above to begin scanning.")

# Footer
st.markdown("---")
st.caption("© 2025 FICE - Find Inaccurate Credit Errors | Built for transparency and consumer empowerment.")
