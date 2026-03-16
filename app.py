import streamlit as st

st.set_page_config(page_title="Store Bonus Calculation", layout="centered")

st.title("Manager Bonus Entry Form")
st.write("Enter the required monthly data points below to calculate performance bonuses.")

# Dropdowns for Store and Month
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

# Hardcoded targets based on standard company metrics
TARGET_LABOR = 0.17  # 17.0%
TARGET_DELTA = 0.02  # 2.0%

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
    # Note: NOI has no minimum value here, allowing for negative entry
    net_operating_income = st.number_input("Net Operating Income ($)", step=100.0) 

st.markdown("---")

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
        
        # 4. Automate Approval Verification based on standard targets
        labor_met = flexepos_labor_percent <= TARGET_LABOR
        delta_met = delta_percent <= TARGET_DELTA
        approved = labor_met and delta_met
        
        # 5. Bonus Pools (NOI maxed at 0 to prevent negative payouts)
        noi = max(net_operating_income, 0)
        manager_bonus = noi * 0.075 if approved else 0.0
        ops_partner_bonus = noi * 0.05 if approved else 0.0
        
        st.subheader(f"📊 Recap Calculations: Store {store} - {month}")
        st.write(f"**Net Operating Income:** ${net_operating_income:,.2f}")
        
        # Display the metrics with visual indicators (✅ or ❌)
        labor_icon = "✅ MET" if labor_met else "❌ MISSED"
        delta_icon = "✅ MET" if delta_met else "❌ MISSED"
        
        st.write(f"**Flexepos Labor %:** {flexepos_labor_percent:.2%} (Goal: $\le$ 17%) {labor_icon}")
        st.write(f"**P&L Actual / CT Theoretical Delta:** {delta_percent:.2%} (${delta_dollars:,.2f}) (Goal: $\le$ 2%) {delta_icon}")
        
        st.markdown("---")
        
        # Payout Logic
        if approved:
            if net_operating_income <= 0:
                # Store hit metrics but lost money
                st.warning("🌟 **Great job managing your metrics!** You successfully met both the labor and food cost goals. Because the Net Operating Income was below $0, the final bonus pool zeroes out this month, but keep up the excellent work controlling those costs!")
                st.write("**Manager Bonus (7.5%):** $0.00")
                st.write("**Operations Partner / Area Director Bonus (5%):** $0.00")
            else:
                # Store hit metrics and made money
                st.success("🎉 Store met both metrics and generated positive income! Bonuses approved.")
                st.write(f"**Manager Bonus (7.5%):** ${manager_bonus:,.2f}")
                st.write(f"**Operations Partner / Area Director Bonus (5%):** ${ops_partner_bonus:,.2f}")
        else:
            # Store missed metrics
            st.error("⚠️ Store failed to meet one or both metrics. Bonus pool is zeroed out.")
            st.write("**Manager Bonus (7.5%):** $0.00")
            st.write("**Operations Partner / Area Director Bonus (5%):** $0.00")
            
    else:
        st.error("Total Royalty Sales must be greater than $0 to calculate percentages.")
