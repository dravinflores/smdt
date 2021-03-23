import pandas as pd

mainData = "C:/Users/Tension/Dropbox/sMDT/MainDatabase.csv"
tensionData = "C:/Users/Tension/Dropbox/sMDT/TensionStation/output/data_19.04.2019_13.59.33.out"

df_main = pd.read_csv(mainData, skiprows=1,
		names = ['barcode',
		'swager_userid',
		'swager_comments',
		'tension_userid',
		'length',
		'datetime_tension',
		'wire_frequency',
		'wire_tension',
		'tension_error',
		'second_datetime_tension',
		'second_frequency',
		'second_tension',
		'second_tension_error',
		'gas_leak_rate',
		'dark_current'])
df_main.set_index('barcode',inplace=True)

df_tension = pd.read_csv(tensionData,skiprows=1,names=['tension_userid',
													'datetime_tension',
													'barcode',
													'length',
													'wire_density',
													'wire_frequency',
													'wire_tension', 
													'tension_error'])
df_tension.set_index('barcode', inplace=True)
df_tension.dropna(how='all',inplace=True)
df_main = df_main.fillna(df_tension,inplace=True)
df_main.to_csv('C:/Users/Tension/Dropbox/sMDT/MainDatabase.csv')

print(df_main.head())