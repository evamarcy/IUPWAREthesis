# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 12:50:22 2022

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#code for WP2 to create scatterplot of sensitivity versus GMT and versus snow cover % per continent
#with both hist and future scenarios

#%%==============================================================================
# imports
# ===============================================================================
import os
import pandas as pd
import combined_functions as fn
from tabulate import tabulate

#%%==============================================================================
# file paths
#================================================================================

#input directory
dataDIR = 'C:/Users/eveem/Google Drive/School/Thesis/data/'
os.chdir(dataDIR)

# ouput directory
plotDIR = os.path.join(dataDIR, 'GMT scatterplots')


#%%==============================================================================
# define variables 
#================================================================================
models = ['CanESM5', 'CNRM-ESM2-1', 'IPSL-CM6A-LR','UKESM1-0-LL', 'multimodel_average']
scenpairs = ["hist","ssp126", "ssp370"]
                
#%%==============================================================================
# read in files
#================================================================================

hist_sensitivities = pd.read_csv(dataDIR+'/hist_tas_sensitivity.csv')
ssp126_sensitivities = pd.read_csv(dataDIR+'/ssp126_tas_sensitivity.csv')
ssp370_sensitivities = pd.read_csv(dataDIR+'/ssp370_tas_sensitivity.csv')

hist_sensitivities['scenario'] = 'hist'
ssp126_sensitivities['scenario'] = 'ssp126'
ssp370_sensitivities['scenario'] = 'ssp370'

sens_df = pd.concat([hist_sensitivities,ssp126_sensitivities, ssp370_sensitivities]).reset_index(drop=True)

reference = 1850 #first year of 30 year reference period for historical GMT (can choose any year in sens_df['scenario'] = 'hist')
sens_df_rebuild = pd.DataFrame()
ref_val={}
for mod in models:
    mod_df = sens_df.loc[sens_df['Model'] == mod]
    ref_val[mod] = mod_df['GMT base'].loc[mod_df['Year'] == reference].mean()
    mod_df['GMT_anomaly'] = mod_df['GMT base']-ref_val[mod]
    sens_df_rebuild = pd.concat([sens_df_rebuild,mod_df])
    
    
GMTscalingslopes = fn.getsensitivity(sens_df_rebuild,'GMT_anomaly').reset_index(drop=True)
print('GMT Slopes')
for scen in scenpairs:
    scaling = GMTscalingslopes.loc[GMTscalingslopes['scenario'] == scen]
    print(scen)
    print(tabulate(scaling.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))
    
snowscalingslopes = fn.getsensitivity(sens_df_rebuild,'snow cover % hist').reset_index(drop=True)
print('Snow Slopes')
for scen in scenpairs:
    scaling = snowscalingslopes.loc[GMTscalingslopes['scenario'] == scen]
    print(scen)
    print(tabulate(scaling.pivot(index="Model", columns="Continent", values="Slope"), headers = 'keys', tablefmt = 'plain'))


#%%==============================================================================
# plot
#================================================================================

fn.sensitivityvsGMT(sens_df_rebuild, plotDIR, 'sensitivity_vs_GMT_annualmin_ensemblepairs_allscen.png', GMTscalingslopes)
fn.sensitivityvstime(sens_df_rebuild, plotDIR, 'sensitivity_vs_time_annualmin_ensemblepairs_allscen.png')
fn.sensitivityvssnowcoverpercent(sens_df_rebuild, plotDIR, 'sensitivity_vs_snow_annualmin_ensemblepairs_allscen.png', snowscalingslopes)

#remove outlier sensitivities
plot_df = sens_df_rebuild.loc[sens_df_rebuild['Slope'] < 0.0005]
plot_df = plot_df.loc[plot_df['Slope'] > -0.0005]
GMTscalingslopes_noout = fn.getsensitivity(plot_df,'GMT_anomaly').reset_index(drop=True)
snowscalingslopes_noout = fn.getsensitivity(plot_df,'snow cover % hist').reset_index(drop=True)

fn.sensitivityvsGMT(plot_df, plotDIR, 'sensitivity_vs_GMT_annualmin_ensemblepairs_allscen_nooutliers.png', GMTscalingslopes_noout)
fn.sensitivityvstime(plot_df, plotDIR, 'sensitivity_vs_time_annualmin_ensemblepairs_allscen_nooutliers.png')
fn.sensitivityvssnowcoverpercent(plot_df, plotDIR, 'sensitivity_vs_snow_annualmin_ensemblepairs_allscen_nooutliers.png', snowscalingslopes_noout)
