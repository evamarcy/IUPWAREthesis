# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 14:02:32 2022

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#code for WP2: 

#caluculates sensitivity of TAS to change in treefrac for any chosen set of timesteps in the historical period
#creates CSV files to be read by combined_WP2_runfile

# - annual minimum values only
# - ensemble pairwise realizations only
# - filter for cells with a certain % of treefrac change
# - option to use pixels with snow cover only


#%%==============================================================================
# imports
# ===============================================================================
import os
import hist_functions as fn

#%%==============================================================================
# file paths
#================================================================================
dataDIR = 'C:/Users/eveem/Google Drive/School/Thesis/data/'
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
plotDIR = os.path.join(histDIR, 'scatterplots')

#%%==============================================================================
# settings
#================================================================================
y1=1850
duration = 165
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
#calculate sensitivities over time tas
sensitivity_am_ep_tas = fn.time_loop_am(data_dict,  GMT_data_dict,'change_tas', gridarea, y1, duration, startyear, tstep_size, True,
                                    percent_threshold, snd_thres)

sensitivity_am_ep_tas.to_csv(dataDIR + '/hist_tas_sensitivity.csv',index=False)
