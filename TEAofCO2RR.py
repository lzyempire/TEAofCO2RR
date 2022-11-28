from cmath import nan
from math import prod
import numpy as np
import pandas as pd


def CaseCustom(
    Custom_ElectricityPrice = 0.05, 
    Custom_CurrentDensity = 200, 
    Custom_CellVoltage = 2.3, 
    Custom_CO2Price = 70, 
    Custom_ElectrolyzerCost = 250.25/1000*0.175*10000*1.75*1.2*2, 
    Custom_SellPriceRate = 1, 
    Custom_Selectivity = 90, 
    Custom_Conversion = 50
):
    CaseChart = pd.DataFrame(
        columns=['Current', 'Optimistic', 'Better', 'Worse'],
        data=[
            [0.05, 0.03, 0.02, 0.04], # $/kWh
            [200, 300, 100, 500], # mA/cm^2
            [2.3, 2, 1.7, 2.3],  # V
            [70, 40, 0, 70],  # $/ton
            [250.25/1000*0.175*10000*1.75*1.2*2, 250.25/1000*0.175*10000*1.75*1.2, 460, 250.25/1000*0.175*10000*1.75*1.2*2],
            [1, 1, 1.15, 0.85], 
            [90, 90, 100, 80], 
            [50, 50, 70, 30]], # $/m^2
        index=['ElectricityPrice', 'CurrentDensity', 'CellVoltage', 'CO2Price', 'ElectrolyzerCost', 'SellPriceRate', 'Selectivity', 'Conversion']
    )

    CaseChart['Custom'] = [Custom_ElectricityPrice, Custom_CurrentDensity, Custom_CellVoltage, Custom_CO2Price, Custom_ElectrolyzerCost, Custom_SellPriceRate, Custom_Selectivity, 
    Custom_Conversion]
    return CaseChart



def NPVCal(Case = 'Optimistic', Product_cathode = 'EtOH'):


    PptChart = pd.DataFrame(
        columns=['Name', 'NumElectron', 'MoleRatiotoCO2', 'MW', 'Density', 'Phase', 'Price', 'Voltage'], 
        data=[
            ['Hydrogen', 2, nan, 2.016, 0.089, 'Gas', 4, nan], 
            ['Carbon monoxide', 2, 1, 28.01, 1.14, 'Gas', 0.6, 1.736], 
            ['Ethanol', 12, 2, 46.06, 789, 'Liquid', 1.003, 1.546], 
            ['Ethylene', 12, 2, 28.05, 1.18, 'Gas', 1.3, 1.566], 
            ['Formic acid', 2, 1, 46.025, 1221, 'Liquid', 0.735, 1.88], 
            ['Methane', 8, 1, 16.04, 0.656, 'Gas', 0.18, 1.461], 
            ['Methanol', 6, 1, 32.04, 792, 'Liquid', 0.577, 1.614], 
            ['Propanol', 18, 3, 60.06, 803, 'Liquid', 1.435, 1.535], 
            ['Water', 4, nan, 18, 1000, 'Liquid', 0.0054/3.785, nan],
            ['Carbon dioxide', 4, nan, 44, 1.98, 'Gas', 40/1000, nan],
            ['Oxygen', 4, nan, 32, 1.429, 'Gas', 0.05, nan]], 
        index = ['H2', 'CO', 'EtOH', 'C2H4', 'HCOOH', 'CH4', 'MeOH', 'PrOH', 'H2O', 'CO2', 'O2']
        )

    CaseChart = CaseCustom()

    PriceChart = pd.DataFrame(
        data=[
            [4162240, 3463310], 
            [6896190, 11213200],
            [4514670, 4027820],
            [4687910, 5610420], 
            [0, 0], [0, 0], [0, 0]], 
        columns=['RefCapCost', 'RefOperatCost'],
        index=['EtOH', 'HCOOH', 'MeOH', 'PrOH', 'CO', 'C2H4', 'CH4']
    )
    # CellArea_electrode = 1/10000
    CurrentperArea_electrode = CaseChart.loc['CurrentDensity', Case]*10000/1000 # A/m^2
    FaradayConstant = 96480 # C/mol
    Byproduct_cathode = 'H2'
    Cell_voltage = 0.454 + PptChart.loc[Product_cathode, 'Voltage'] + CaseChart.loc['CellVoltage', Case] - 2
    Phase_productCath = PptChart.loc[Product_cathode, 'Phase']
    Phase_byproductCath = PptChart.loc[Byproduct_cathode,'Phase']
    MW_productCath = PptChart.loc[Product_cathode,'MW']/1000 # kg/mol
    MW_CO2 = PptChart.loc['CO2','MW']/1000 # kg/mol
    MW_H2O = PptChart.loc['H2O','MW']/1000
    MW_byproductCath = PptChart.loc[Byproduct_cathode,'MW']/1000 # kg/mol
    Density_productCath = PptChart.loc[Product_cathode,'Density'] # kg/m^3
    Density_byproductCath = PptChart.loc[Byproduct_cathode,'Density'] # kg/m^3
    Density_CO2 = PptChart.loc['CO2','Density'] # kg/m^3
    NumElectron_productCath = PptChart.loc[Product_cathode,'NumElectron']
    NumElectron_byproductCath = PptChart.loc[Byproduct_cathode, 'NumElectron']
    NumElectron_CO2 = PptChart.loc['CO2', 'NumElectron']
    NumElectron_H2O = PptChart.loc['H2O', 'NumElectron']
    FaradayEff = CaseChart.loc['Selectivity', Case] / 100
    # OnePassCO2Eff = 0.5
    TotalPassCO2Eff = CaseChart.loc['Conversion', Case] / 100
    TotalPassFlowRatio_productCath = 0.1

    # FlowRate_productCath = CurrentperArea_electrode * CellArea_electrode * FaradayEff / (NumElectron_productCath*FaradayConstant) * MW_productCath / Density_productCath
    # OnepassRatio_productCath = FlowRate_productCath / FlowRate_electrolyteCath

    ScaleMassRate_productCath = 100000/24/3600 # kg/s
    Scale_current = ScaleMassRate_productCath / MW_productCath * NumElectron_productCath * FaradayConstant / FaradayEff
    Scale_power = Scale_current * Cell_voltage
    Scale_area = Scale_current / CurrentperArea_electrode # m^2
    ScaleMassRate_inCO2 = ScaleMassRate_productCath / MW_productCath * PptChart.loc[Product_cathode, 'MoleRatiotoCO2'] * MW_CO2 / (1 - TotalPassCO2Eff) # kg/s
    ScaleMassRate_H2O = Scale_current / (NumElectron_H2O * FaradayConstant) * MW_H2O # kg/s
    ScaleMassRate_byproductCath = Scale_current * (1 - FaradayEff) / (NumElectron_byproductCath * FaradayConstant) * MW_byproductCath # kg/s
    # ScaleFlowRate_electrolyteCath = ScaleMassRate_productCath / Density_productCath / TotalPassFlowRatio_productCath # m^3/s
    # ScaleFlowRate_gasCath = ScaleMassRate_inCO2 * TotalPassCO2Eff / Density_CO2 + ScaleMassRate_byproductCath / Density_byproductCath # m^3/s

    if Phase_productCath == 'Gas':
        ScaleFlowRate_productGas = ScaleMassRate_inCO2 * TotalPassCO2Eff / Density_CO2 + ScaleMassRate_byproductCath / Density_byproductCath + ScaleMassRate_productCath / Density_productCath
        ScaleFlowRate_productLiquid = 0
    elif Phase_productCath == 'Liquid':
        ScaleFlowRate_productGas = ScaleMassRate_inCO2 * TotalPassCO2Eff / Density_CO2 + ScaleMassRate_byproductCath / Density_byproductCath
        ScaleFlowRate_productLiquid = ScaleMassRate_productCath / Density_productCath / TotalPassFlowRatio_productCath



    # InstallFactor = 1.2
    # CapExperArea_electrolyzer = 250.25/1000*0.175*10000*1.75 * InstallFactor # DOE H2A, $/m^2
    CapExperArea_electrolyzer = CaseChart.loc['ElectrolyzerCost', Case]
    CapEx_electrolyzer = CapExperArea_electrolyzer * Scale_area # $
    CapExRatio_BoP = 0.35
    CapEx_BoP = CapEx_electrolyzer * CapExRatio_BoP / (1 - CapExRatio_BoP)
    CapEx_distill = PriceChart.loc[Product_cathode, 'RefCapCost'] * (ScaleFlowRate_productLiquid / (1/60) ) ** 0.7 # $
    CapEx_PSA = 1989043 * (ScaleFlowRate_productGas / (1000/3600)) ** 0.7 # $
    CapEx_total = CapEx_electrolyzer + CapEx_distill + CapEx_BoP + CapEx_PSA
    CapEx_Cost = pd.Series([CapEx_electrolyzer, CapEx_BoP, CapEx_distill, CapEx_PSA], index=['Electrolyzer', 'BoP', 'Distillation', 'PSA'])

    ElectricityPrice = CaseChart.loc['ElectricityPrice', Case] # $/kWh
    CO2Price = PptChart.loc['CO2', 'Price'] + (CaseChart.loc['CO2Price', Case] - 40)/1000 # $/kg
    H2OPrice = PptChart.loc['H2O', 'Price'] # $/L(kg)
    ProductCathPrice = PptChart.loc[Product_cathode, 'Price'] * CaseChart.loc['SellPriceRate', Case]
    AnnualWorkDays = 350
    OpEx_electric = Scale_power * AnnualWorkDays * 24/1000 * ElectricityPrice # $/year
    OpEx_maintenance = 0.025 * CapEx_electrolyzer # $/year
    OpEx_distill = PriceChart.loc[Product_cathode, 'RefOperatCost'] * (ScaleFlowRate_productLiquid / (1/60)) # $/year
    OpEx_PSA = 0.25 * ElectricityPrice * ScaleFlowRate_productGas * 3600*24 * AnnualWorkDays # $/year
    OpEx_CO2 = CO2Price * ScaleMassRate_inCO2 * TotalPassCO2Eff * 3600*24 * AnnualWorkDays # $/year
    OpEx_H2O = H2OPrice * ScaleMassRate_H2O * 3600*24 * AnnualWorkDays # $/year
    OpEx_Cost = pd.Series([OpEx_CO2, OpEx_H2O, OpEx_distill, OpEx_PSA, OpEx_maintenance, OpEx_electric], index=['CO2 Purchase', 'Water Usage', 'Distillation', 'PSA', 'Maintanenece', 'Electrolyzer Electricity'])
    Income_productCath = ProductCathPrice * ScaleMassRate_productCath * 3600*24 * AnnualWorkDays

    GrossProfit = Income_productCath - OpEx_CO2 - OpEx_H2O - OpEx_distill - OpEx_electric - OpEx_maintenance - OpEx_PSA

    # Net Present Value Calculation
    Income_tax = 0.389
    InterestRate = 0.1
    CapEx_workingRatio = 0.05
    SalvageValue = 0.2
    Year_Construct = 1
    Year_Lifetime = 20
    MACRS_Year10 = [10, 18, 14.4, 11.52, 9.22, 7.37, 6.55, 6.55, 6.56, 6.55, 3.28]
    DepreciationPercent = MACRS_Year10
    NPVChart = pd.DataFrame({'Year': range(0, Year_Lifetime + 1)})
    NPVChart.loc[Year_Construct:len(DepreciationPercent), 'DepreciationPercentage'] = DepreciationPercent
    NPVChart['Depreciation'] = NPVChart['DepreciationPercentage'] * CapEx_total /100
    NPVChart.loc[Year_Construct:, 'NetProfit'] = GrossProfit
    NPVChart.fillna(0, inplace=True)
    NPVChart['NetEarning'] = (NPVChart['NetProfit'] - NPVChart['Depreciation']) * (1 - Income_tax)
    NPVChart['CashFlow_Discounted'] = NPVChart['NetEarning'] + NPVChart['Depreciation']
    NPVChart.loc[NPVChart.index[0], 'CashFlow_Discounted'] = - CapEx_total * (1 + CapEx_workingRatio)
    NPVChart.loc[NPVChart.index[-1], 'CashFlow_Discounted'] = NPVChart.loc[NPVChart.index[-1], 'CashFlow_Discounted'] + CapEx_total * (SalvageValue + CapEx_workingRatio)
    NPVChart['CashFlow_PV'] = NPVChart['CashFlow_Discounted']/(1+InterestRate)**NPVChart['Year']
    NPVChart['CumCash_PV'] = NPVChart['CashFlow_PV'].cumsum()


    return NPVChart.loc[NPVChart.index[-1], 'CumCash_PV'], CapEx_Cost, OpEx_Cost

def OpCost_yield():
    for products in ['EtOH', 'HCOOH', 'MeOH', 'PrOH', 'CO', 'C2H4', 'CH4']:
        _, _, OpCost = NPVCal('Optimistic', products)
        yield OpCost
OpEx_df = pd.concat(OpCost_yield(), axis=1, keys=['Ethanol', 'Formic Acid', 'Methanol', 'n-Propanol', 'Carbon Monoxide', 'Ethylene', 'Methane'])

def CapCost_yield():
    for products in ['EtOH', 'HCOOH', 'MeOH', 'PrOH', 'CO', 'C2H4', 'CH4']:
        _, CapCost, _ = NPVCal('Optimistic', products)
        yield CapCost
CapEx_df = pd.concat(CapCost_yield(), axis=1, keys=['Ethanol', 'Formic Acid', 'Methanol', 'n-Propanol', 'Carbon Monoxide', 'Ethylene', 'Methane'])

NPV_dic = {}
def NPV_yield():
    for cases in ['Current', 'Optimistic', 'Better', 'Worse']:
        for products in ['EtOH', 'HCOOH', 'MeOH', 'PrOH', 'CO', 'C2H4', 'CH4']:
            NPV_Value, _, _ = NPVCal(cases, products)
            NPV_dic[products] = NPV_Value
        NPV_Series = pd.Series(NPV_dic)
        yield NPV_Series
NPV_df = pd.concat(NPV_yield(), axis=1, keys=['Current', 'Optimistic', 'Better', 'Worse'])
NPV_df.index = ['Ethanol', 'Formic Acid', 'Methanol', 'n-Propanol', 'Carbon Monoxide', 'Ethylene', 'Methane']

