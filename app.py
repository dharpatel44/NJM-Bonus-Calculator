import streamlit as st

st.set_page_config(page_title="Store Bonus Calculation", layout="centered")

st.title("Manager Bonus Entry Form")
st.write("Enter the 11 required monthly data points below to calculate performance bonuses.")

# Dropdowns for Store and Month (Updated with all stores)
stores = [
    "4011", "4018", "4023", "4026", "4045", "4050", 
    "4054", "4065", "4076", "8063", "8066", "8091"
]
months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

col1, col2 = st.columns(2)
with col1:
    store = st.selectbox("Store #", stores)
with col2:
    month = st.selectbox("Month", months)

st.markdown("---")

# 1. Flexepos Data
st.header("1. Flexepos Data")
col3, col4 = st.columns(2)
with col3:
    total_sales = st.number_input("Total Royalty Sales ($)", min_value=0.0, step=100.0)
with col4:
    hourly_payroll_flex = st.number_input("Hourly Payroll ($)", min_value=0.0, step=100.0)

# 2. Crunchtime Data
st.header("2. Crunchtime Data")
col5, col6 = st.columns(2)
with col5:
    actual_food_cost_ct = st.number_input("Actual Food Cost ($)", min_value=0.0, step=100.0)
    actual_paper_cost_ct = st.number_input("Actual Paper Cost ($)", min_value=0.0, step=100.0)
with col6:
    theo_food_cost_ct = st.number_input("Theoretical Food Cost ($)", min_value=0.0, step=100.0)
    theo_paper_cost_ct = st.number_input("Theoretical Paper Cost ($)", min_value=0.0, step=100.0)

# 3. P&L Data
st.header("3. P&L Data")
col7, col8 = st.columns(2)
with col7:
    food_cost_pl = st.number_input("Food Cost ($)", min_value=0.0, step=100.0)
    paper_cost_pl = st.number_input("Paper Cost ($)", min_value=0.0, step=100.0)
    beverage_cost_pl = st.number_input("Beverage Cost ($)", min_value=0.0, step=100.0)
with col8:
    hourly_payroll_pl = st.number_input("P&L Hourly Payroll ($)", min_value=0.0, step=100.0)
    net_operating_income = st.number_input("Net Operating Income ($)", step=100.0) # Can be negative

# Approval flag identical to placing an "x" on the Recap tab 
st.markdown("---")
approved = st.checkbox("Are these metrics approved for bonus payout?")

# Compute and present Results
if st.button("Calculate Bonuses"):
    if total_sales > 0:
        # 1. P&L Food/Paper/Bev derived
        pl_food_paper_cost = food_cost_pl + paper_cost_pl + beverage_cost_pl
        
        # 2. Crunchtime Theoretical derived
        ct_theo_food_paper = theo_food_cost_ct + theo_paper_cost_ct
        
        # 3. Required Output Metrics
        delta_dollars = pl_food_paper_cost - ct_theo_food_paper
        delta_percent = delta_dollars / total_sales
        flexepos_labor_percent = hourly_payroll_flex / total_sales
        
        # 4. Bonus Pools
        noi = max(net_operating_income, 0)
        manager_bonus = noi * 0.075 if approved else 0.0
        ops_partner_bonus = noi * 0.05 if approved else 0.0
        
        st.subheader(f"📊 Recap Calculations: Store {store} - {month}")
        st.write(f"**P&L Actual / CT Theoretical Delta:** {delta_percent:.2%} (${delta_dollars:,.2f})")
        st.write(f"**Flexepos Labor %:** {flexepos_labor_percent:.2%}")
        st.write(f"**Net Operating Income:** ${noi:,.2f}")
        
        st.success(f"**Manager Bonus (7.5%):** ${manager_bonus:,.2f}")
        st.info(f"**Operations Partner Bonus (5%):** ${ops_partner_bonus:,.2f}")
    else:
        st.error("Total Royalty Sales must be greater than $0 to calculate percentages.")
    
