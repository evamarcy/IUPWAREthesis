# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 14:02:32 2022

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#code for WP1: 

#caluculates sensitivity of TAS to change in treefrac for end of future period
#creates scatterplots of change in TAS vs change in TreeArea
#creates maps of treecover, temperature and senstivitiy changes
#creates histograms of sensitivity values for each continent

# - both future scenarios (SSP1-2.6 and SSP3-7.0)
# - annual minimum values only
# - ensemble pairwise realizations only
# - filter for cells with a certain % of treefrac change
# - option to use pixels with snow cover only


#%%==============================================================================
# imports
# ===============================================================================
import os
import pandas as pd
import numpy as np
import future_functions as fn
import future_map_functions as mfn
from tabulate import tabulate

#%%==============================================================================
# file paths
#================================================================================
dataDIR = 'C:/Users/eveem/Google Drive/School/Thesis/Data/'
os.chdir(dataDIR)

# data input directories
gridDIR = os.path.join(dataDIR, 'gridarea')
futDIR = os.path.join(dataDIR, 'future')

anminDIR = os.path.join(futDIR, 'annualmin')

anminDIR_ip = os.path.join(anminDIR, 'individual_pairwiserealizations')
anminDIR_ep = os.path.join(anminDIR, 'ensemble_pairwiserealizations')
anminDIR_ea = os.path.join(anminDIR, 'ensemble_allrealizations')


# ouput directories
mapDIR = os.path.join(futDIR, 'maps')
plotDIR = os.path.join(futDIR, 'scatterplots')

#%%==============================================================================
# define variables 
#================================================================================
models = ['CanESM5', 'CNRM-ESM2-1', 'IPSL-CM6A-LR','UKESM1-0-LL', 'multimodel_average']

continents = {}
continents['North America'] = [1,2,3,4,5,6,7,8]
continents['South America'] = [9,10,11,12,13,14,15]
continents['Europe'] = [16, 17, 18, 19]
continents['Asia'] = [28,29,30,31,32,33,34,35,37,38]
continents['Africa'] = [21,22,23,24,25,26]

regionlist=[]
for cont in continents:
    for i in continents[cont]:
        regionlist.append(i)


letters=['a','b','c','d','e','f','g',
         'h','i','j','k','l','m','n',
         'o','p','q','r','s','t','u',
         'v','w','x','y','z']

#%%==============================================================================
# settings
#================================================================================
y1=2015
duration = 85

# threshold of tree fraction change (as %) that will be shown in the scatterplots
percent_threshold = 5

#threshold for plotting where snow occurs
#uses max snow depth for the season when using min temp, average winter depth when using average winter temp
snd_thres = 0.1  # m of max or winteraverage snow depth

                
#%%==============================================================================
# calulations
#================================================================================

# annual minimum - ensemble pairwise realizations
#================================================================================

print('\n\nannual minimum - ensemble pairwise realizations==================\n\n')
# open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
gridarea = fn.load_gridarea(gridDIR)
data_dict = fn.create_datadict(anminDIR_ep, 'min', y1, duration, True) 
GMT_data_dict = fn.create_datadict(anminDIR_ep, 'av_', y1, duration, True) 

# "ssp126-ssp370Lu"==========================================================
# convert to to tree area from treefrac and calculate changes in TAS and tree area
change_treeArea_126, change_treefrac_126, change_tas_126, sndbase_126, mean_tasbase_126, tasbase_126, base_treearea_126, noLu_treearea_126, gridarea1 = fn.thirty_year_averages(data_dict, 
                                                                                                                                                                     GMT_data_dict,
                                                                                                                                                                     gridarea, 
                                                                                                                                                                     "ssp126", "ssp126-ssp370Lu",
                                                                                                                                                                     y1, duration, 
                                                                                                                                                                    True)
# add change_treeArea and change_tas to a data frame 
df_126 = fn.create_df(change_treeArea_126, 
                      change_treefrac_126, 
                      change_tas_126, 
                      sndbase_126, 
                      tasbase_126, 
                      base_treearea_126, 
                      noLu_treearea_126,
                      gridarea1)

#apply the percent threshold for plotting to the dataframe and label the continents 
df_am_ep_126  = fn.label_df(fn.threshold_df(df_126,percent_threshold))

#get sensitivity using linear regression
sensitivity_am_ep_126 = fn.getsensitivity(df_am_ep_126, mean_tasbase_126, 'change_tas', snd_thres)    
    
#caluculate sensitivity by pixel
tas_sensitivity_bypixel_126, change_treeArea_masked_126, mask_126 = fn.pixel_sensitivity_calc(change_treeArea_126, change_treefrac_126, change_tas_126, percent_threshold)
#add sensitivity by pixel to a data frame 
sens_df_126 = fn.pixel_sensitivity_df(tas_sensitivity_bypixel_126, sndbase_126, mask_126)
#label the continents 
sens_df_126 = fn.label_sens_df(sens_df_126)

#caculate % of each continent covered by snow based on km2 (not number of cells but total area of cells)
snowpercent_am_ep_126 = fn.getsnowpercent(df_am_ep_126 , snd_thres)


# "ssp370-ssp126Lu"==========================================================
# convert to to tree area from treefrac and calculate changes in TAS andNo documentat tree area
change_treeArea_370, change_treefrac_370, change_tas_370, sndbase_370, mean_tasbase_370, tasbase_370, base_treearea_370, noLu_treearea_370, gridarea1 = fn.thirty_year_averages(data_dict,
                                                                                                                                                                     GMT_data_dict,
                                                                                                                                                                     gridarea, 
                                                                                                                                                                     "ssp370", "ssp370-ssp126Lu", 
                                                                                                                                                                     y1, duration, 
                                                                                                                                                                     True)

# add change_treeArea and change_tas to a data frame 
df_370 = fn.create_df(change_treeArea_370, 
                      change_treefrac_370, 
                      change_tas_370, 
                      sndbase_370, 
                      tasbase_370, 
                      base_treearea_370, 
                      noLu_treearea_370,
                      gridarea1)

#apply the percent threshold for plotting to the dataframe and label the continents 
df_am_ep_370 = fn.label_df(fn.threshold_df(df_370,percent_threshold))

#get sensitivity using linear regression
sensitivity_am_ep_370 = fn.getsensitivity(df_am_ep_370, mean_tasbase_370,'change_tas', snd_thres)
    
#caluculate sensitivity by pixel
tas_sensitivity_bypixel_370, change_treeArea_masked_370, mask_370 = fn.pixel_sensitivity_calc(change_treeArea_370, change_treefrac_370, change_tas_370, percent_threshold)
#add sensitivity by pixel to a data frame 
sens_df_370 = fn.pixel_sensitivity_df(tas_sensitivity_bypixel_370, sndbase_370, mask_370)
#label the continents 
sens_df_370 = fn.label_sens_df(sens_df_370)

#caculate % of each continent covered by snow
snowpercent_am_ep_370 = fn.getsnowpercent(df_am_ep_370, snd_thres)

sensitivity_am_ep_126.to_csv(dataDIR + '/126_tas_sensitivity_2070-2099.csv',index=False)
sensitivity_am_ep_370.to_csv(dataDIR + '/370_tas_sensitivity_2070-2099.csv',index=False)


#%%==============================================================================
# plots
#================================================================================

#histogram of sensitivities for each pixel for each continent, hue=model or hue=snowcover
histogram_sens_df_126 = sens_df_126[sens_df_126['model'] != 'multimodel_average']
histogram_sens_df_370 = sens_df_370[sens_df_370['model'] != 'multimodel_average']
histogram_sens_df_126['scenario'] = 'ssp126-ssp370Lu'
histogram_sens_df_370['scenario'] = 'ssp370-ssp126Lu'
histogram_sens_df = pd.concat([histogram_sens_df_126,histogram_sens_df_370])
histogram_sens_df['snowcover'] = np.where(histogram_sens_df['snd'] > snd_thres, True, False)
fn.bypixel_hist_2row(histogram_sens_df,'sensitivity', plotDIR, 'histogram of sensitivities by pixel both future scenarios')
fn.bypixel_hist_snowcover(histogram_sens_df,'sensitivity', plotDIR, 'histogram of sensitivities by pixel snowcover as hue both future scenarios')

#scatterplot by continent and by model with BOTH SCENARIO PAIRS and sensitivity labels  
df_am_ep_126['scenario'] = 'ssp126-ssp370Lu'
df_am_ep_370['scenario'] = 'ssp370-ssp126Lu'
df_am_ep = pd.concat([df_am_ep_126,df_am_ep_370])
fn.scatterplot_future_scen(df_am_ep, plotDIR, 'scatterplots_annualmin_ensemblepairs_bothscenarios',sensitivity_am_ep_126,sensitivity_am_ep_370, False)

#scatterplot by continent and by model with BOTH SCENARIO PAIRS and sensitivity labels, snow cover cells only
df_am_ep_126_snow = df_am_ep_126[df_am_ep_126['snd'] > snd_thres]
df_am_ep_370_snow = df_am_ep_370[df_am_ep_370['snd'] > snd_thres]
sensitivity_am_ep_126_snow = fn.getsensitivity(df_am_ep_126_snow, mean_tasbase_126,'change_tas', snd_thres)
sensitivity_am_ep_370_snow = fn.getsensitivity(df_am_ep_370_snow, mean_tasbase_370,'change_tas', snd_thres)
df_am_ep_snow = df_am_ep[df_am_ep['snd'] > snd_thres]
fn.scatterplot_future_scen(df_am_ep_snow, plotDIR, 'scatterplots_annualmin_ensemblepairs_bothscenarios_snowcover_only',sensitivity_am_ep_126_snow,sensitivity_am_ep_370_snow, True)


#%%==============================================================================
# maps
#================================================================================

#maps of change in tas and sensitivity 
print('starting tas and sensitivity maps')     
mfn.combined_plot(change_tas_126, change_tas_370, tas_sensitivity_bypixel_126, tas_sensitivity_bypixel_370, models, letters, mapDIR, '/map_combined_trends_sensitivity.png')

#maps of change in tree area
print('starting tree cover area maps') 
mfn.futurelanduse_plot(base_treearea_126, base_treearea_370, change_treeArea_masked_126, models, letters, mapDIR, '/map_treearea.png')

#maps of tas for each scenario
print('starting tas maps') 
ssp126_tas, ssp126_ssp370Lu_tas = fn.final_tas(data_dict, gridarea,  "ssp126", "ssp126-ssp370Lu", y1, duration, True)  
ssp370_tas, ssp370_ssp126Lu_tas = fn.final_tas(data_dict, gridarea,  "ssp370", "ssp370-ssp126Lu", y1, duration, True)    
mfn.tasmaps_plot(ssp126_tas, ssp370_tas, ssp126_ssp370Lu_tas, ssp370_ssp126Lu_tas, models, letters, mapDIR, '/map_tas.png')


#%%==============================================================================
# tables
#================================================================================

#"ssp126-ssp370Lu"==========================================================
print("\n\nssp126-ssp370Lu")
print('change in tree area')
change_area_df=fn.tree_area_calc(fn.label_df(df_126),'change_area')
print(tabulate(change_area_df.pivot(index="model", columns="continent", values="change_area"), headers = 'keys', tablefmt = 'plain'))

print('ssp126_treeArea')
base_area_df=fn.tree_area_calc(fn.label_df(df_126),'base_treearea')
print(tabulate(base_area_df.pivot(index="model", columns="continent", values='base_treearea'), headers = 'keys', tablefmt = 'plain'))
print('ssp370_treeArea')
noLu_area_df=fn.tree_area_calc(fn.label_df(df_126),'noLu_treearea')
print(tabulate(noLu_area_df.pivot(index="model", columns="continent", values='noLu_treearea'), headers = 'keys', tablefmt = 'plain'))

tas_stats_df=fn.descriptive_stats(df_am_ep_126 ,'change_tas')
multimod_df_126 = df_am_ep_126.loc[df_am_ep_126['model'] == 'multimodel_average']
global_ave_tas_126 = multimod_df_126['change_tas'].mean()
print('TAS')
for stat in ['minimum','maximum','average']:
    print(stat)
    print(tabulate(tas_stats_df.pivot(index="model", columns="continent", values=stat), headers = 'keys', tablefmt = 'plain'))

sens_stats_df=fn.descriptive_stats(sens_df_126,'sensitivity')
print('Sensitivity')
for stat in ['minimum','maximum','average']:
    print(stat)
    print(tabulate(sens_stats_df.pivot(index="model", columns="continent", values=stat), headers = 'keys', tablefmt = 'plain'))

print('scatterplot slopes')
print('TAS ssp126-ssp370Lu')
print(tabulate(sensitivity_am_ep_126.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
print('scatterplot slopes snow cover only')
print(tabulate(sensitivity_am_ep_126_snow.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))

print('snow cover percent')
print(tabulate(snowpercent_am_ep_126.pivot(index="Model", columns="Continent", values='Snow %'), headers = 'keys', tablefmt = 'plain'))



#"ssp370-ssp126Lu"==========================================================
print('\n\n\nssp370-ssp126Lu')
print('change in tree area')
change_area_df=fn.tree_area_calc(fn.label_df(df_370),'change_area')
print(tabulate(change_area_df.pivot(index="model", columns="continent", values="change_area"), headers = 'keys', tablefmt = 'plain'))

print('ssp370_treeArea')
base_area_df=fn.tree_area_calc(fn.label_df(df_370),'base_treearea')
print(tabulate(base_area_df.pivot(index="model", columns="continent", values='base_treearea'), headers = 'keys', tablefmt = 'plain'))
print('ssp126_treeArea')
noLu_area_df=fn.tree_area_calc(fn.label_df(df_370),'noLu_treearea')
print(tabulate(noLu_area_df.pivot(index="model", columns="continent", values='noLu_treearea'), headers = 'keys', tablefmt = 'plain'))


tas_stats_df=fn.descriptive_stats(df_am_ep_370,'change_tas')
multimod_df_370 = df_am_ep_370.loc[df_am_ep_370['model'] == 'multimodel_average']
global_ave_tas_370 = multimod_df_370['change_tas'].mean()
print('TAS ssp370-ssp126Lu')
for stat in ['minimum','maximum','average']:
    print(stat)
    print(tabulate(tas_stats_df.pivot(index="model", columns="continent", values=stat), headers = 'keys', tablefmt = 'plain'))


sens_stats_df=fn.descriptive_stats(sens_df_370,'sensitivity')
print('Sensitivity')
for stat in ['minimum','maximum','average']:
    print(stat)
    print(tabulate(sens_stats_df.pivot(index="model", columns="continent", values=stat), headers = 'keys', tablefmt = 'plain'))

print('scatterplot slopes')
print('TAS ssp370-ssp126Lu')
print(tabulate(sensitivity_am_ep_370.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
print('scatterplot slopes snow cover only')
print(tabulate(sensitivity_am_ep_370_snow.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))


print('snow cover percent')
print(tabulate(snowpercent_am_ep_370.pivot(index="Model", columns="Continent", values='Snow %'), headers = 'keys', tablefmt = 'plain'))
