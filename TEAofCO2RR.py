# CellArea_electrode = 1/10000
CurrentperArea_electrode = 0.3*10000 # A/m^2
Cell_voltaic = 2
Product_cathode = 'Ethanol'
Byproduct_cathode = 'Hydrogen'
Phase_productCath = 'Liquid'
Phase_byproductCath = 'Gas'
# FlowRate_electrolyteCath = 0.5/1000/1000/60
MW_productCath = 46.06/1000 # kg/mol
MW_CO2 = 44/1000 # kg/mol
MW_H2O = 18/1000
MW_byproductCath = 2.016/1000 # kg/mol
Density_productCath = 0.786*1000 # kg/m^3
Density_byproductCath = 0.089 # kg/m^3
Density_CO2 = 1.98 # kg/m^3
FaradayConstant = 96480 # C/mol
NumElectron_productCath = 12
NumElectron_byproductCath = 2
NumElectron_CO2 = 6
NumElectron_H2O = 4
FaradayEff = 0.9
OnePassCO2Eff = 0.5
TotalPassCO2Eff = 0.5
TotalPassFlowRatio_productCath = 0.1

# FlowRate_productCath = CurrentperArea_electrode * CellArea_electrode * FaradayEff / (NumElectron_productCath*FaradayConstant) * MW_productCath / Density_productCath
# OnepassRatio_productCath = FlowRate_productCath / FlowRate_electrolyteCath

ScaleMassRate_productCath = 100000/24/3600 # kg/s
Scale_current = ScaleMassRate_productCath / MW_productCath * NumElectron_productCath * FaradayConstant / FaradayEff
Scale_power = Scale_current * Cell_voltaic
Scale_area = Scale_current / CurrentperArea_electrode # m^2
ScaleMassRate_inCO2 = Scale_current * FaradayEff / (NumElectron_CO2 * FaradayConstant) * MW_CO2 / TotalPassCO2Eff # kg/s
ScaleMassRate_H2O = Scale_current / (NumElectron_H2O * FaradayConstant) * MW_H2O # kg/s
ScaleMassRate_byproductCath = Scale_current * (1 - FaradayEff) / (NumElectron_byproductCath * FaradayConstant) * MW_byproductCath # kg/s
ScaleFlowRate_electrolyteCath = ScaleMassRate_productCath / Density_productCath / TotalPassFlowRatio_productCath # m^3/s
ScaleFlowRate_gasCath = ScaleMassRate_inCO2 * (1 - TotalPassCO2Eff) / Density_CO2 + ScaleMassRate_byproductCath / Density_byproductCath # m^3/s

# if Phase_productCath == 'Gas':
#     ScaleFlowRate_productGas = ScaleFlowRate_CO2 + ScaleFlowRate_productCath
#     ScaleFlowRate_productLiquid = ScaleFlowRate_electrolyteCath
# elif Phase_productCath == 'Liquid':
#     ScaleFlowRate_productGas = ScaleFlowRate_CO2
#     ScaleFlowRate_productLiquid = ScaleFlowRate_electrolyteCath + ScaleFlowRate_productCath

InstallFactor = 1.2
CapExperArea_electrolyzer = 250.25/1000*0.175*10000*1.75 * InstallFactor # DOE H2A, $/m^2
CapEx_electrolyzer = CapExperArea_electrolyzer * Scale_area # $
CapExRatio_BoP = 0.35
CapEx_BoP = CapEx_electrolyzer * CapExRatio_BoP / (1 - CapExRatio_BoP)
CapEx_distill = 4162240 * (ScaleFlowRate_electrolyteCath / (1/60) ) ** 0.7 # $
CapEx_PSA = 1989043 * (ScaleFlowRate_gasCath / (1000/3600)) ** 0.7 # $
CapEx_total = CapEx_electrolyzer + CapEx_distill + CapEx_BoP + CapEx_PSA

ElectricityPrice = 0.03 # $/kWh
CO2Price = 40/1000 # $/kg
H2OPrice = 0.0054/3.785 # $/L(kg)
ProductCathPrice = 1.003
AnnualWorkDays = 350
OpEx_electric = Scale_power * AnnualWorkDays * 24/1000 * ElectricityPrice # $/year
OpEx_maintenance = 0.025 * CapEx_electrolyzer # $/year
OpEx_distill = 9895 * AnnualWorkDays * (ScaleFlowRate_electrolyteCath / (1/60)) # $/year
OpEx_PSA = 0.25 * ElectricityPrice * ScaleFlowRate_gasCath * 3600*24 * AnnualWorkDays # $/year
OpEx_CO2 = CO2Price * ScaleMassRate_inCO2 * OnePassCO2Eff * 3600*24 * AnnualWorkDays # $/year
OpEx_H2O = H2OPrice * ScaleMassRate_H2O * 3600*24 * AnnualWorkDays # $/year
Income_productCath = ProductCathPrice * ScaleMassRate_productCath * 3600*24 * AnnualWorkDays

GrossProfit = Income_productCath - OpEx_CO2 - OpEx_H2O - OpEx_distill - OpEx_electric - OpEx_maintenance - OpEx_PSA

Income_tax = 0.389
InterestRate = 0.1

print(CapEx_total)