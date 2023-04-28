# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 14:02:32 2022

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#code for WP1: 

#caluculates sensitivity of TAS to change in treefrac for end of historical period
#creates scatterplots of change in TAS or TASMAX vs change in TreeArea
#creates maps of treecover, temperature and senstivitiy changes
#creates histograms of sensitivity values for each continent

# - both winteraverage and annual minimum values
# - indiviual pairwise realisations, and both options for ensemble averages (pairwise only versus all realizations)
# - filter for cells with a certain % of treefrac change
# - option to use pixels with snow cover only, or filter by latitude


#%%==============================================================================
# imports
# ===============================================================================
import os
import pandas as pd
import numpy as np
import hist_functions as fn
import hist_map_functions as mfn
from tabulate import tabulate

#%%==============================================================================
# file paths
#================================================================================
dataDIR = 'C:/Users/eveem/Google Drive/School/Thesis/Data/'
os.chdir(dataDIR)

# data input directories
gridDIR = os.path.join(dataDIR, 'gridarea')
histDIR = os.path.join(dataDIR, 'historical')

anminDIR = os.path.join(histDIR, 'in-annualmin')
winteravDIR = os.path.join(histDIR, 'in-winteraverage')

anminDIR_ip = os.path.join(anminDIR, 'individual_pairwiserealizations')
anminDIR_ep = os.path.join(anminDIR, 'ensemble_pairwiserealizations')
anminDIR_ea = os.path.join(anminDIR, 'ensemble_allrealizations')

winteravDIR_ip = os.path.join(winteravDIR, 'individual_pairwiserealizations')
winteravDIR_ep = os.path.join(winteravDIR, 'ensemble_pairwiserealizations')
winteravDIR_ea = os.path.join(winteravDIR, 'ensemble_allrealizations')

# ouput directories
mapDIR = os.path.join(histDIR, 'maps')
plotDIR = os.path.join(histDIR, 'plots')

#%%==============================================================================
# define variables 
#================================================================================
models = ['CanESM5', 'CNRM-ESM2-1', 'IPSL-CM6A-LR', 'UKESM1-0-LL', 'multimodel_average']

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

labels = {}
labels['North America'] = ['WNA', 'CNA', 'ENA']
labels['South America'] = ['NWS', 'NSA', 'NES', 'SAM', 'SES']
labels['Europe'] = ['NEU', 'WCE', 'EEU', 'MED']
labels['Asia'] = ['WSB', 'ESB', 'WCA', 'EAS', 'SAS']
labels['Africa'] = ['WAF', 'CAF', 'NEAF', 'SEAF', 'SWAF', 'ESAF']

letters=['a','b','c','d','e','f','g',
         'h','i','j','k','l','m','n',
         'o','p','q','r','s','t','u',
         'v','w','x','y','z']

#%%==============================================================================
# settings
#================================================================================
y1=1850
duration = 165

# threshold of tree fraction change (as %) that will be shown in the scatterplots
percent_threshold = 5

#threshold for plotting where snow occurs
#uses max snow depth for the season when using min temp, average winter depth when using average winter temp
snd_thres = 0.1  # m of max or winteraverage snow depth

                
#%%==============================================================================
# main text body calulations
#================================================================================

# annual minimum
#================================================================================

# individual pairwise realizations==========================================
print('\n\nannual minimum - individual pairwise realizations================\n\n')
# open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
gridarea = fn.load_gridarea(gridDIR)
data_dict = fn.create_datadict(anminDIR_ip, 'min', y1, duration, False) #gives annual values with dates from 1850(-01-01) to 2014(-01-01)
# convert to to tree area from treefrac and calculate changes in TAS and tree area
change_treeArea, change_treefrac, change_tas, change_tasmax, sndhist, mean_tashist, tashist, gridarea1 = fn.thirty_year_averages(data_dict, gridarea, y1, duration, False)
# add change_treeArea and change_tas to a data frame 
df = fn.create_df(change_treeArea, change_treefrac, change_tas, change_tasmax, sndhist, tashist, gridarea1)
#apply the percent threshold for plotting to the dataframe and label the continents 
df_am_ip = fn.label_df(fn.threshold_df(df,percent_threshold))
#subset the df


#get sensitivity using linear regression
sensitivity_am_ip_tas = fn.getsensitivity(df_am_ip, 'change_tas', snd_thres)
sensitivity_am_ip_tasmax = fn.getsensitivity(df_am_ip, 'change_tasmax', snd_thres)


snowpercent_am_ip = fn.getsnowpercent(df_am_ip, snd_thres)
    
    
#caluculate sensitivity by pixel
indiv_tas_sensitivity_bypixel, indiv_change_treeArea_masked, indiv_mask = fn.pixel_sensitivity_calc(change_treeArea, change_treefrac, change_tas, percent_threshold)
#add sensitivity by pixel to a data frame 
indiv_sens_df = fn.pixel_sensitivity_df(indiv_tas_sensitivity_bypixel,sndhist,indiv_mask)
# label the continents 
indiv_sens_df = fn.label_sens_df(indiv_sens_df)


indiv_sens_df['snowcover'] = np.where(indiv_sens_df['snd'] > snd_thres, True, False)



sens_stats_df=fn.descriptive_stats(indiv_sens_df,'sensitivity')
print('Sensitivity')
for stat in ['minimum','maximum','average']:
    print(stat)
    print(tabulate(sens_stats_df.pivot(index="model", columns="continent", values=stat), headers = 'keys', tablefmt = 'plain'))
 


# ensemble pairwise realizations============================================
print('\n\nannual minimum - ensemble pairwise realizations==================\n\n')
# open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
gridarea = fn.load_gridarea(gridDIR)
data_dict = fn.create_datadict(anminDIR_ep, 'min', y1, duration, True) 
GMT_data_dict = fn.create_datadict(anminDIR_ep, 'av_', y1, duration, True) 
# convert to to tree area from treefrac and calculate changes in TAS and tree area
change_treeArea, change_treefrac, change_tas, change_tasmax, sndhist, mean_tashist, tashist, gridarea1 = fn.thirty_year_averages(data_dict, gridarea, y1, duration, True, GMT_data_dict)
# add change_treeArea and change_tas to a data frame 
df = fn.create_df(change_treeArea, change_treefrac, change_tas, change_tasmax, sndhist, tashist, gridarea1)
#apply the percent threshold for plotting to the dataframe and label the continents 
df_am_ep = fn.label_df(fn.threshold_df(df,percent_threshold))

#get sensitivity using linear regression
sensitivity_am_ep_tas = fn.getsensitivity(df_am_ep,'change_tas', snd_thres, mean_tashist)
sensitivity_am_ep_tasmax = fn.getsensitivity(df_am_ep,'change_tasmax', snd_thres, mean_tashist)
# sensitivity_am_ep_tas.to_csv(dataDIR + '/hist_tas_sensitivity_1985-2014.csv',index=False)

snowpercent_am_ep = fn.getsnowpercent(df_am_ep, snd_thres)
print('snow percent')
print(tabulate(snowpercent_am_ep.pivot(index="Model", columns="Continent", values='Snow %'), headers = 'keys', tablefmt = 'plain'))
    
    
#caluculate sensitivity by pixel
tas_sensitivity_bypixel, change_treeArea_masked, mask = fn.pixel_sensitivity_calc(change_treeArea, change_treefrac, change_tas, percent_threshold)
#add sensitivity by pixel to a data frame 
sens_df = fn.pixel_sensitivity_df(tas_sensitivity_bypixel, sndhist, mask)
#label the continents 
sens_df = fn.label_sens_df(sens_df)


area_df=fn.deforestation_area_calc(fn.label_df(df))
print(tabulate(area_df.pivot(index="model", columns="continent", values="change_area"), headers = 'keys', tablefmt = 'plain'))

tas_stats_df=fn.descriptive_stats(df_am_ep,'change_tas')
print('TAS')
for stat in ['minimum','maximum','average']:
    print(stat)
    print(tabulate(tas_stats_df.pivot(index="model", columns="continent", values=stat), headers = 'keys', tablefmt = 'plain'))


#%%==============================================================================
# appendix calulations - may not be updated to work with new function library
#================================================================================

# # ensemble all realizations=================================================
# print('\n\nannual minimum - ensemble all realizations=======================\n\n')
# # open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
# gridarea = fn.load_gridarea(gridDIR)
# data_dict = fn.create_datadict(anminDIR_ea, 'min', y1, duration, True)  
# # convert to to tree area from treefrac and calculate changes in TAS and tree area
# change_treeArea, change_treefrac, change_tas, change_tasmax, sndnolu, tashist = fn.thirty_year_averages(data_dict, gridarea, y1, duration, True)
# # add change_treeArea and change_tas to a data frame 
# df = fn.create_df(change_treeArea, change_treefrac, change_tas, change_tasmax, sndnolu, tashist)
# #apply the percent threshold for plotting to the dataframe and label the continents 
# regions_df = fn.label_df(fn.threshold_df(df,percent_threshold))
# #subset the df
# df_am_ea = fn.subset_df (regions_df, lat_flag, lat_thres, snd_flag, snd_thres)
# #get sensitivity using linear regression
# sensitivity_am_ea_tas = fn.getsensitivity(df_am_ea,'change_tas')
# sensitivity_am_ea_tasmax = fn.getsensitivity(df_am_ea,'change_tasmax')

# if snd_flag == True:
#     snowpercent_am_ea = fn.getsnowpercent(regions_df, snd_thres)
  
# # winter average
# #================================================================================

# # individual pairwise realizations==========================================
# print('\n\nwinter average - individual pairwise realizations================\n\n')
# # open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
# gridarea = fn.load_gridarea(gridDIR)
# data_dict_jja = fn.create_datadict(winteravDIR_ip, 'JJA', y1, duration, False)  
# data_dict_djf = fn.create_datadict(winteravDIR_ip, 'DJF', y1, duration, False)
# # convert to to tree area from treefrac and calculate changes in TAS and tree area
# change_treeArea_jja, change_treefrac_jja, change_tas_jja, change_tasmax_jja, sndnolu_jja, tashist_jja = fn.thirty_year_averages(data_dict_jja, gridarea, y1, duration, False)
# change_treeArea_djf, change_treefrac_djf, change_tas_djf, change_tasmax_djf, sndnolu_djf, tashist_djf = fn.thirty_year_averages(data_dict_djf, gridarea, y1, duration, False)
# # add change_treeArea and change_tas to a data frame 
# df_jja = fn.create_df(change_treeArea_jja, change_treefrac_jja, change_tas_jja, change_tasmax_jja, sndnolu_jja, tashist_jja)
# df_djf = fn.create_df(change_treeArea_djf, change_treefrac_djf, change_tas_djf, change_tasmax_djf, sndnolu_djf, tashist_djf)
# # remove wrong hemipsheres based on summer month periods
# df_djf = df_djf[df_djf.lat > 0]
# df_jja = df_jja[df_jja.lat < 0]
# df = pd.concat([df_djf,df_jja], axis=0)
# #apply the percent threshold for plotting to the dataframe and label the continents 
# regions_df = fn.label_df(fn.threshold_df(df,percent_threshold))
# #subset the df
# df_wa_ip = fn.subset_df (regions_df, lat_flag, lat_thres, snd_flag, snd_thres)
# #get sensitivity using linear regression
# sensitivity_wa_ip_tas = fn.getsensitivity(df_wa_ip,'change_tas')
# sensitivity_wa_ip_tasmax = fn.getsensitivity(df_wa_ip,'change_tasmax')

# if snd_flag == True:
#     snowpercent_wa_ip = fn.getsnowpercent(regions_df, snd_thres)


# # ensemble pairwise realizations============================================
# print('\n\nwinter average - ensemble pairwise realizations==================\n\n')
# # open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
# gridarea = fn.load_gridarea(gridDIR)
# data_dict_jja = fn.create_datadict(winteravDIR_ep, 'JJA', y1, duration, True)  
# data_dict_djf = fn.create_datadict(winteravDIR_ep, 'DJF', y1, duration, True)
# # convert to to tree area from treefrac and calculate changes in TAS and tree area
# change_treeArea_jja, change_treefrac_jja, change_tas_jja, change_tasmax_jja, sndnolu_jja, tashist_jja = fn.thirty_year_averages(data_dict_jja, gridarea, y1, duration, True)
# change_treeArea_djf, change_treefrac_djf, change_tas_djf, change_tasmax_djf, sndnolu_djf, tashist_djf = fn.thirty_year_averages(data_dict_djf, gridarea, y1, duration, True)
# # add change_treeArea and change_tas to a data frame 
# df_jja = fn.create_df(change_treeArea_jja, change_treefrac_jja, change_tas_jja, change_tasmax_jja, sndnolu_jja, tashist_jja)
# df_djf = fn.create_df(change_treeArea_djf, change_treefrac_djf, change_tas_djf, change_tasmax_djf, sndnolu_djf, tashist_djf)
# # remove wrong hemipsheres based on summer month periods
# df_djf = df_djf[df_djf.lat > 0]
# df_jja = df_jja[df_jja.lat < 0]
# df = pd.concat([df_djf,df_jja], axis=0)
# #apply the percent threshold for plotting to the dataframe and label the continents 
# regions_df = fn.label_df(fn.threshold_df(df,percent_threshold))
# #subset the df
# df_wa_ep = fn.subset_df (regions_df, lat_flag, lat_thres, snd_flag, snd_thres)
# #get sensitivity using linear regression
# sensitivity_wa_ep_tas = fn.getsensitivity(df_wa_ep,'change_tas')
# sensitivity_wa_ep_tasmax = fn.getsensitivity(df_wa_ep,'change_tasmax')

# if snd_flag == True:
#     snowpercent_wa_ep = fn.getsnowpercent(regions_df, snd_thres)


# # ensemble pairwise realizations============================================
# print('\n\nwinter average - ensemble all realizations=======================\n\n')
# # open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
# gridarea = fn.load_gridarea(gridDIR)
# data_dict_jja = fn.create_datadict(winteravDIR_ea, 'JJA', y1, duration, True)  
# data_dict_djf = fn.create_datadict(winteravDIR_ea, 'DJF', y1, duration, True)
# # convert to to tree area from treefrac and calculate changes in TAS and tree area
# change_treeArea_jja, change_treefrac_jja, change_tas_jja, change_tasmax_jja, sndnolu_jja, tashist_jja = fn.thirty_year_averages(data_dict_jja, gridarea, y1, duration, True)
# change_treeArea_djf, change_treefrac_djf, change_tas_djf, change_tasmax_djf, sndnolu_djf, tashist_djf = fn.thirty_year_averages(data_dict_djf, gridarea, y1, duration, True)
# # add change_treeArea and change_tas to a data frame 
# df_jja = fn.create_df(change_treeArea_jja, change_treefrac_jja, change_tas_jja, change_tasmax_jja, sndnolu_jja, tashist_jja)
# df_djf = fn.create_df(change_treeArea_djf, change_treefrac_djf, change_tas_djf, change_tasmax_djf, sndnolu_djf, tashist_djf)
# # remove wrong hemipsheres based on summer month periods
# df_djf = df_djf[df_djf.lat > 0]
# df_jja = df_jja[df_jja.lat < 0]
# df = pd.concat([df_djf,df_jja], axis=0)
# #apply the percent threshold for plotting to the dataframe and label the continents 
# regions_df = fn.label_df(fn.threshold_df(df,percent_threshold))
# #subset the df
# df_wa_ea = fn.subset_df (regions_df, lat_flag, lat_thres, snd_flag, snd_thres)
# #get sensitivity using linear regression
# sensitivity_wa_ea_tas = fn.getsensitivity(df_wa_ea,'change_tas')
# sensitivity_wa_ea_tasmax = fn.getsensitivity(df_wa_ea,'change_tasmax')

# if snd_flag == True:
#     snowpercent_wa_ea = fn.getsnowpercent(regions_df, snd_thres)

#%%==============================================================================
# plots and maps
#================================================================================

#scatterplot by continent and by model with tas and tasmax and sensitivity labels  
df_am_ep_melt = pd.melt(df_am_ep,
                        id_vars=['lat', 'lon', 'change_area','change_frac', 'snd', 'tas_hist','region', 'model', 'realization','continent',], 
                        value_vars=['change_tas', 'change_tasmax'],
                        var_name='tastype', 
                        value_name='change_tasvar')

fn.scatterplot_tasandtasmax(df_am_ep_melt, plotDIR, 'tas&tasmax_scatterplots_annualmin_ensemblepairs',sensitivity_am_ep_tas,sensitivity_am_ep_tasmax, False)

#scatterplot snow cover only cells by continent and by model with tas and tasmax and sensitivity labels
df_am_ep_snow = df_am_ep[df_am_ep['snd']> snd_thres]
sensitivity_am_ep_tas_snow = fn.getsensitivity(df_am_ep_snow,'change_tas', snd_thres, mean_tashist)
sensitivity_am_ep_tasmax_snow = fn.getsensitivity(df_am_ep_snow,'change_tasmax', snd_thres, mean_tashist)

df_am_ep_melt_snow = df_am_ep_melt[df_am_ep_melt['snd'] > snd_thres]

fn.scatterplot_tasandtasmax(df_am_ep_melt_snow, plotDIR, 'tas&tasmax_scatterplots_annualmin_ensemblepairs_snowcover_only',sensitivity_am_ep_tas_snow,sensitivity_am_ep_tasmax_snow, True)

#histograms 
fn.bypixel_hist_1row(indiv_sens_df,'sensitivity', plotDIR, 'histogram of sensitivities by pixel')
fn.bypixel_hist_snowcover(indiv_sens_df,'sensitivity', plotDIR, 'histogram of sensitivities by pixel hue=snowcover')

#maps of change in tas deforestation and sensitivity      
mfn.combined_plot(change_treeArea_masked, change_tas, tas_sensitivity_bypixel, models, letters, mapDIR, '/map_combined_trends_sensitivity.png')


#%%==============================================================================
# # tables
# #================================================================================
print('tas')
print('am_ep')
print(tabulate(sensitivity_am_ep_tas.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
print(tabulate(snowpercent_am_ep.pivot(index="Model", columns="Continent", values="Snow %"), headers = 'keys', tablefmt = 'plain'))
# print('am_ea')
# print(tabulate(sensitivity_am_ea_tas.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
# print('wa_ep')
# print(tabulate(sensitivity_wa_ep_tas.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
# print('wa_ea')
# print(tabulate(sensitivity_wa_ea_tas.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
   
print('\n\ntasmax')
print('am_ep')
print(tabulate(sensitivity_am_ep_tasmax.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
# print('am_ea')
# print(tabulate(sensitivity_am_ea_tasmax.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
# print('wa_ep')
# print(tabulate(sensitivity_wa_ep_tasmax.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
# print('wa_ea')
# print(tabulate(sensitivity_wa_ea_tasmax.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))

