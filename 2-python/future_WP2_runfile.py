# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 14:02:32 2022

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#code for WP2: 

#caluculates sensitivity of TAS to change in treefrac for any chosen set of timesteps in the future period
#creates CSV files to be read by combined_WP2_runfile

# - both future scenarios (SSP1-2.6 and SSP3-7.0)
# - annual minimum values only
# - ensemble pairwise realizations only
# - filter for cells with a certain % of treefrac change
# - option to use pixels with snow cover only

#%%==============================================================================
# imports
# ===============================================================================
import os
import future_functions as fn

#%%==============================================================================
# file paths
#================================================================================
dataDIR = 'C:/Users/eveem/Google Drive/School/Thesis/data/'
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
# settings
#================================================================================
y1=2015
duration = 85
startyear = 30
tstep_size = 5

# threshold of tree fraction change (as %) that will be shown in the scatterplots
percent_threshold = 5

#threshold for plotting where snow occurs
#uses max snow depth for the season when using min temp, average winter depth when using average winter temp
snd_thres = 0.01  # m of min snow depth
                
#%%==============================================================================
# calulations
#================================================================================

# ensemble pairwise realizations============================================
print('\n\nannual minimum - ensemble pairwise realizations==================')
# open files (gridarea, treefrac annual, TAS hist, TAS hist_no-Lu)
gridarea = fn.load_gridarea(gridDIR)
data_dict = fn.create_datadict(anminDIR_ep, 'min', y1, duration, True)  
GMT_data_dict = fn.create_datadict(anminDIR_ep, 'av_', y1, duration, True) 


#calculate sensitivities over time "ssp126-ssp370Lu"
sensitivity_am_ep_126 = fn.time_loop_am(data_dict, GMT_data_dict, gridarea, "ssp126", "ssp126-ssp370Lu", y1, duration, startyear, tstep_size, True,
                                    percent_threshold, snd_thres)
sensitivity_am_ep_126.to_csv(dataDIR + '/ssp126_tas_sensitivity.csv',index=False)

#calculate sensitivities over time "ssp370-ssp126Lu"
sensitivity_am_ep_370 = fn.time_loop_am(data_dict, GMT_data_dict, gridarea, "ssp370", "ssp370-ssp126Lu", y1, duration, startyear, tstep_size, True,
                                    percent_threshold, snd_thres)
sensitivity_am_ep_370.to_csv(dataDIR + '/ssp370_tas_sensitivity.csv',index=False)
