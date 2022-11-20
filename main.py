from src.scraper.yahoo_finance import scraper_to_statement
from src.scraper.utils import convert_to_float, extract_ttm_value
from src.valuation import intrinsic_value, compound, discount, return_table


def main():
    # Calculate Intrincic Value.
    df = intrinsic_value("AAPL")
    print("\tAAPL\n")
    print(df)

    # is_link = "https://finance.yahoo.com/quote/AAPL/financials?p=AAPL"
    # bs_link = "https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL"
    # cf_link = "https://finance.yahoo.com/quote/AAPL/cash-flow?p=AAPL"
    #
    # # Run scraping and return data frame.
    # income_df = scraper_to_statement(is_link)
    # balance_sheet_df = scraper_to_statement(bs_link)
    # cashflow_df = scraper_to_statement(cf_link)
    #
    # print("\tAAPL")
    # print("Income Report: ")
    # print(income_df)
    # print("\n")
    # print("Balance Sheet: ")
    # print(balance_sheet_df)
    # print("\n")
    # print("Cashflow Report: ")
    # print(cashflow_df)
    #
    # # Instantiate resulting table.
    # df = return_table()
    #
    # # Pulling in the desired fields ebit, depreciation & capex
    # df.at[0, 'incomeBeforeTax'] = extract_ttm_value(income_df, 'EBIT')
    # df.at[0, 'depreciation'] = extract_ttm_value(income_df, 'Reconciled Depreciation')
    # df.at[0, 'capitalExpenditures'] = extract_ttm_value(cashflow_df, 'Capital Expenditure')
    #
    # # Calculating Average Capital Expenditure.
    # cp_exp_row = cashflow_df[cashflow_df["Breakdown"] == "Capital Expenditure"]
    # mean_capex = cp_exp_row.iloc[:, 2:].mean(axis=1).astype(float)
    # df.at[0, 'Average Capex'] = mean_capex.iloc[0]
    #
    # # Calculating Owners Earnings
    # earnings = df['incomeBeforeTax'] + df['depreciation'] - df['Average Capex']
    # df.at[0, 'Owners Earnings'] = earnings.iloc[0]
    #
    # # Creating the calculation table.
    # compound_rate = 0.1
    # discount_rate = 0.05
    # terms = 5
    #
    # import pandas as pd
    # dfc = []
    # for y in range(1, terms + 1):
    #     z = compound(compound_rate, y)
    #     dfc.append(z)
    #
    # dfc1 = pd.DataFrame(dfc)
    #
    # dfd = []
    # for y in range(1, terms + 1):
    #     z = discount(discount_rate, y)
    #     dfd.append(z)
    # dfd1 = pd.DataFrame(dfd)
    #
    # calcs_table = pd.concat([dfc1, dfd1], axis=1)
    # calcs_table.columns=["Compound", "Discount"]
    #
    # # Find the DCF Multiplier
    # calcs_table["Amounts"] = calcs_table['Compound'] * calcs_table['Discount']
    # calcs_table1 = calcs_table.append(calcs_table.sum().rename('Total'))
    #
    # print(calcs_table)
    #
    # DCF_multiplier = pd.DataFrame(calcs_table1['Amounts'].tail(1)).reset_index(drop=True)
    # # print(calcs_table['Amounts'].tail(1).iloc[0])
    # DCF_multiplier.columns=["DCF_multiplier"]
    #
    # print(DCF_multiplier)
    # df["DCF_multiplier"] = DCF_multiplier["DCF_multiplier"]
    #
    # # Find the PV (Present Value) Multiplier
    # PV_multiplier = pd.DataFrame(calcs_table['Amounts'].tail(1)).reset_index(drop=True)
    # PV_multiplier.columns=["PV_multiplier"]
    # # PV_multiplier = PV_multiplier['PV_multiplier'] / discount_rate
    #
    # print(PV_multiplier)
    #
    # df["PV_multiplier"] = PV_multiplier['PV_multiplier'] / discount_rate
    #
    # # # Calculate the intrinsic value
    # # final_df = pd.concat([df1,PV_multiplier,DCF_multiplier],axis=1)
    # # df.at[0, 'OE*PV'] = df['Owners Earnings'] * df['PV_multiplier']
    # df['OE*PV'] = df['Owners Earnings'] * df['PV_multiplier']
    # df['OE*DCF'] = df['Owners Earnings'] * df['DCF_multiplier']
    # df['Intrinsic Value'] = df['OE*PV'] + df['OE*DCF']
    #
    # # Find Outstanding Shares.
    # df.at[0, "Outstanding Shares"] = income_df[income_df["Breakdown"] == "Diluted Average Shares"].iloc[:, 2].iloc[0]
    # df['Per Share'] = df['Intrinsic Value'] / df['Outstanding Shares']
    # # Show results.
    # # print("\n")
    # # print("calcs_table: \n", calcs_table)
    # print("\n")
    # print(df)


if __name__ == "__main__":
    main()
