import pandas as pd

import glob

act = glob.glob('Active_Count_*.csv')[0]     #Active Terminals
inact = glob.glob('Total_Count_*.csv')[0]    #Total Terminals
df_dep = glob.glob('Deposit_*.csv')[0]       #Deposits
df_net = glob.glob('Game_Type_Wise_Net_S_*.csv')[0]       #Disbursements
df_pay = glob.glob('Pay_*.csv')[0]       #Pay
df_dis = glob.glob('Disbursement_*.csv')[0]
df_sales_staff = pd.read_excel('SALES STAFF.xlsx', sheet_name = 'Sheet2')
df_sbm = pd.read_excel('SBMs.xlsx')
df_state = pd.read_excel('State.xlsx')

act_term = pd.read_csv(act, na_values=['.'])
inact_term = pd.read_csv(inact, na_values=['.'])
df_deposits = pd.read_csv(df_dep, na_values=['.'])
df_net_sales = pd.read_csv(df_net, na_values=['.'])
df_payouts = pd.read_csv(df_pay, na_values=['.'])
df_disbursements = pd.read_csv(df_dis, na_values=['.'])

act_inact = pd.merge(act_term, inact_term, on = 'rm', how = 'left')
deposit_merge = pd.merge(act_inact, df_deposits, left_on = 'rm', right_on = 'RM_name', how = 'left')
disbursement_merge = pd.merge(deposit_merge, df_disbursements, left_on = 'rm', right_on = 'RM_name', how = 'left')
payouts_merge = pd.merge(disbursement_merge, df_payouts, left_on = 'rm', right_on = 'user_name', how = 'left')

filtered_payouts = payouts_merge.loc[:, ['rm', 'terminal_id (DISTINCT_COUNT)_x', 'terminal_id (DISTINCT_COUNT)_y', 'deposit (SUM)', 'Disbursment (SUM)', 'pay_amt (SUM)']]
filtered_payouts.rename(columns={'terminal_id (DISTINCT_COUNT)_x':'Active', 'terminal_id (DISTINCT_COUNT)_y':'Total Terminals', 'deposit (SUM)':'Deposits', 'Disbursment (SUM)':'Disbursements', 'pay_amt (SUM)':'Payouts'},errors='raise',inplace='True')

filtered_payouts['Inactive Terminals'] = filtered_payouts['Total Terminals'] - filtered_payouts['Active']
grouped = df_net_sales[df_net_sales['game_name'] == 'Lotto 5/90-Ghana'].groupby('user_name')['Net Sell'].sum().to_frame('Ghana Games').reset_index()

grouped2 = df_net_sales[df_net_sales['game_name'] == 'Lotto 5/90-Inhouse'].groupby('user_name')['Net Sell'].sum().to_frame('Inhouse Games').reset_index()

game_merge = pd.merge(grouped, grouped2, on = 'user_name', how = 'left')

draft_merge = pd.merge(game_merge, filtered_payouts, left_on = 'user_name', right_on = 'rm', how = 'left' ).fillna('')

df_filtered = df_sales_staff.loc[:,['System Name (ASM)','Area Sales Manager (ASM', 'ASM Phone']]
merge_draft = pd.merge(draft_merge, df_filtered, left_on = 'user_name', right_on = 'System Name (ASM)', how = 'left')

merge_final = merge_draft.loc[:, ['Area Sales Manager (ASM','ASM Phone','user_name', 'Inhouse Games', 'Ghana Games', 'Active', 'Inactive Terminals', 'Total Terminals', 'Deposits', 'Disbursements', 'Payouts']]
sbm_merge = pd.merge(df_sbm, merge_final, on = 'user_name', how = 'left')
zm_merge = pd.merge(sbm_merge, df_state, on = 'user_name', how = 'left')
final_list = zm_merge.loc[:, ['ZONAL','SBMs', 'Area Sales Manager (ASM', 'user_name','ASM Phone', 'Inhouse Games', 'Ghana Games', 'Active', 'Inactive Terminals', 'Total Terminals', 'Deposits', 'Disbursements', 'Payouts']]

final_list.to_excel('MTD Report.xlsx')
