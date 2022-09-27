CellArea_electrode = 1/10000
CurrentperArea_electrode = 300/1000
Product_cathode = 'Ethanol'
FlowRate_electrolyteCath = 0.5/1000/1000/60
MW_productCath = 46.06/1000
MW_CO2 = 44/1000
Density_productCath = 0.786
FaradayConstant = 96480
NumElectron_productCath = 12
NumElectron_CO2 = 6
FaradayEff = 0.9
OnePassCO2Eff = 0.5

FlowRate_productCath = CurrentperArea_electrode * CellArea_electrode * FaradayEff / (NumElectron_productCath*FaradayConstant) * MW_productCath / Density_productCath
OnepassRatio_productCath = FlowRate_productCath / FlowRate_electrolyteCath

ScaleRate_productCath = 100000/24/3600
Cell_voltaic = 2
Scale_current = ScaleRate_productCath / MW_productCath * NumElectron_productCath * FaradayConstant / FaradayEff
Scale_power = Scale_current * Cell_voltaic
Scale_area = Scale_current * FaradayEff / CurrentperArea_electrode
ScaleRate_CO2 = Scale_current * FaradayEff / (NumElectron_CO2*FaradayConstant) / MW_CO2 / OnePassCO2Eff

print(ScaleRate_CO2)