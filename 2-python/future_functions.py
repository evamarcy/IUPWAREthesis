# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 14:11:02 2021

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#function library for future scenario calaculations and plots (map functions in separate file)

#%%==============================================================================
# import
# ===============================================================================
import os
import xarray as xr
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import regionmask as rm
from scipy import stats

#%%==============================================================================
# define variables 
#================================================================================
models = ['CanESM5', 'CNRM-ESM2-1', 'IPSL-CM6A-LR','UKESM1-0-LL', 'multimodel_average']
scenarios = ["ssp126", "ssp370", "ssp126-ssp370Lu", "ssp370-ssp126Lu"]
variables = ['treeFrac','tas','snd']


continents = {}
continents['North America'] = [1,2,3,4,5,6,7,8]
continents['South America'] = [9,10,11,12,13,14,15]
continents['Europe'] = [16, 17, 18, 19]
continents['Asia'] = [28,29,30,31,32,33,34,35,37,38]
continents['Africa'] = [21,22,23,24,25,26]

cont_order = ['North America', 'Europe', 'Asia','South America','Africa']

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
# function library
#================================================================================

# calculations
#================================================================================

def nc_read(file,
            var,
            y1,
            duration=False
            ):
    
    """ 
    From Luke:
    Read in netcdfs based on variable and set time.
    
    Parameters
    ----------
    file : files in data directory
    
    Returns
    ------- 
    Xarray data array
    """
    
    ds = xr.open_dataset(file,decode_times=False)
    da = ds[var].squeeze()
    
    units, reference_date = da.time.attrs['units'].split('since')
    reference_date = reference_date.replace(reference_date[1:5],str(y1))[1:]
    new_date = pd.date_range(start=reference_date, periods=da.sizes['time'], freq='YS')
    da['time'] = new_date
    
    if 'height' in da.coords:
        da = da.drop('height')
        
    if duration:
        da = da[0:duration,:,:]
        
    return da

def ar6_mask(da):
    """ 
    From Luke:
    """
    
    lat = da.lat.values
    lon = da.lon.values
    ar6_regs = rm.defined_regions.ar6.land.mask(lon,lat)
    landmask = rm.defined_regions.natural_earth_v5_0_0.land_110.mask(lon,lat)
    ar6_regs = ar6_regs.where(landmask == 0)
    
    return ar6_regs

def load_gridarea(gridDIR):
    gridarea={}
    os.chdir(gridDIR)
    for mod in models:
        for file in [file for file in sorted(os.listdir(gridDIR))
            if mod in file]:
                gridarea[mod] = xr.open_dataset(file, decode_times=False)['cell_area']
    
    gridarea['multimodel_average'] = gridarea['CanESM5'] # because regridded all files to match this model in CDO before taking the multimodel average files
    return gridarea

def create_datadict(DIR, prefix, y1, duration,  multimodav_flag):
    # where DIR is the directory for the desired type of data and 
    # prefix is the string 'min', 'JJA' or 'DJF' corresponding with the desired data
    
    if multimodav_flag == True:
        if 'multimodel_average' not in models:
            models.append('multimodel_average')
    if multimodav_flag == False:
        if 'multimodel_average' in models:
            models.remove('multimodel_average')
        
    os.chdir(DIR)  
    data_dict={}
    for scen in scenarios:
        data_dict[scen]={}
        for var in variables:
            data_dict[scen][var]={}
            for mod in models:
                data_dict[scen][var][mod]={}
                i = 1
                for file in [file for file in sorted(os.listdir(DIR))]:
                    if '_'+scen+'_' in file:
                        if '_'+var+'_' in file:
                            if file.startswith(prefix):
                                if mod in file:
                                    data_dict[scen][var][mod][i] = nc_read(file, var, y1, duration)
                                    i=i+1
                                
    if multimodav_flag == True:
        for scen in scenarios:
            for var in variables:
                data_dict[scen][var]['multimodel_average']={}
                for file in [file for file in sorted(os.listdir(DIR))]:
                    if '_'+scen+'_' in file:
                        if '_'+var+'_' in file:
                            if file.startswith(prefix):
                                if 'multimodelav' in file:
                                    data_dict[scen][var]['multimodel_average']={}
                                    data_dict[scen][var]['multimodel_average'][1] = nc_read(file, var, y1, duration)
                            

    return data_dict  
            


def thirty_year_averages(data_dictionary, GMT_data_dictionary, gridarea, base_scen, noLu_scen, y1, endyear, multimodav_flag):

    if multimodav_flag == True:
        if 'multimodel_average' not in models:
            models.append('multimodel_average')
    if multimodav_flag == False:
        if 'multimodel_average' in models:
            models.remove('multimodel_average')
        
    base_treefrac={}
    noLu_treefrac={} 
    base_treearea={}
    noLu_treearea={}        
    change_treefrac={} 
    change_treeArea={}

    tasnolu={}
    tasbase={}
    change_tas={}
    
    mean_tasbase={}
    
    sndbase={}
    
    gridarea1={}

    for mod in models:
        base_treefrac[mod]={}
        noLu_treefrac[mod]={} 
        base_treearea[mod]={}
        noLu_treearea[mod]={}
        change_treefrac[mod]={} 
        change_treeArea[mod]={}
    
        tasnolu[mod]={}
        tasbase[mod]={}
        change_tas[mod]={}
        
        mean_tasbase[mod]={}
        
        sndbase[mod]={}
        
        gridarea1[mod]={}
       
        for i in data_dictionary[base_scen]['treeFrac'][mod]:
            base_treefrac[mod][i] = data_dictionary[base_scen]['treeFrac'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean('time')
            noLu_treefrac[mod][i] = data_dictionary[noLu_scen]['treeFrac'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean('time')
            tasnolu[mod][i] = data_dictionary[noLu_scen]['tas'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean('time') 
            tasbase[mod][i] = data_dictionary[base_scen]['tas'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean('time')
            sndbase[mod][i] = data_dictionary[base_scen]['snd'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean('time')
            
            change_treefrac[mod][i] = noLu_treefrac[mod][i] - base_treefrac[mod][i]        
            gridarea[mod].load()
            change_treeArea[mod][i] = change_treefrac[mod][i]*gridarea[mod]/(100*1e6) #convert from percent and m2 to fraction and km2
            base_treearea[mod][i] = base_treefrac[mod][i]*gridarea[mod]/(100*1e6) #convert from percent and m2 to fraction and km2
            noLu_treearea[mod][i] = noLu_treefrac[mod][i]*gridarea[mod]/(100*1e6) #convert from percent and m2 to fraction and km2
            
            gridarea1[mod][i]=gridarea[mod]/1e6
            
            change_tas[mod][i] = tasbase[mod][i]-tasnolu[mod][i]
            
            mean_tasbase[mod][i] = GMT_data_dictionary[base_scen]['tas'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean() - 273.15#convert from kelvin to celcius

                  
    return change_treeArea, change_treefrac, change_tas, sndbase, mean_tasbase, tasbase, base_treearea, noLu_treearea, gridarea1



def final_tas(data_dictionary, gridarea, base_scen, noLu_scen, y1, endyear, multimodav_flag):

    if multimodav_flag == True:
        if 'multimodel_average' not in models:
            models.append('multimodel_average')
    if multimodav_flag == False:
        if 'multimodel_average' in models:
            models.remove('multimodel_average')

    tasnolu={}
    tasbase={}
    for mod in models:
        tasnolu[mod]={}
        tasbase[mod]={}
        for i in data_dictionary[base_scen]['treeFrac'][mod]:
            tasnolu[mod][i] = data_dictionary[noLu_scen]['tas'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean('time') -273.15
            tasbase[mod][i] = data_dictionary[base_scen]['tas'][mod][i].loc[str(y1+endyear-30)+'-01-01':str(y1+endyear-1)+'-01-01'].mean('time') -273.15
                  
    return tasbase, tasnolu

def pixel_sensitivity_calc(change_treeArea, change_treefrac, change_tas, percent_threshold):
    inv_mask={}
    mask={}
    tas_sensitivity_bypixel={}
    change_treeArea_masked={}
    for mod in models:
        inv_mask[mod]={}
        mask[mod] ={}
        tas_sensitivity_bypixel[mod]={}
        change_treeArea_masked[mod]={}
        for i in change_treefrac[mod]: 
            inv_mask[mod][i] = change_treefrac[mod][i]
            inv_mask[mod][i] = xr.where(change_treefrac[mod][i] > percent_threshold, 999, change_treefrac[mod][i]) 
            inv_mask[mod][i] = xr.where(inv_mask[mod][i] < -percent_threshold, 999, inv_mask[mod][i])
            mask[mod][i] = xr.where(inv_mask[mod][i]==999,change_treefrac[mod][i],0)
            
            tas_sensitivity_bypixel[mod][i] = change_tas[mod][i].where(mask[mod][i] != 0)/change_treeArea[mod][i].where(mask[mod][i] != 0)
            change_treeArea_masked[mod][i] = change_treeArea[mod][i].where(mask[mod][i] != 0)
    
    return tas_sensitivity_bypixel, change_treeArea_masked, mask

def pixel_sensitivity_df(sensitivity_bypixel, sndbase, mask):
    print ('\nmaking pixel sensitivity df...')
    
    sensitivity=pd.DataFrame()
    frac_arr=pd.DataFrame()
    snd_arr=pd.DataFrame()
    region_arr=pd.DataFrame()
    regions = {}
    
    for mod in models:
        print ('starting '+mod+'...')
        regions[mod]= {}
        for i in sensitivity_bypixel[mod]:
            print('r'+str(i)+"...")
            #sensitivity
            sensitivity1 = sensitivity_bypixel[mod][i].to_dataframe('sensitivity')
            sensitivity= pd.concat([sensitivity,sensitivity1])
            #tree frac
            frac_arr1 = mask[mod][i].to_dataframe('change_frac')
            frac_arr= pd.concat([frac_arr,frac_arr1])
            #snd
            snd_arr1 = sndbase[mod][i].to_dataframe('snd')
            snd_arr = pd.concat([snd_arr,snd_arr1])
            #AR6
            regions[mod][i] = ar6_mask(sensitivity_bypixel[mod][i])
            region_arr1 = regions[mod][i].to_dataframe('region')
            region_arr1['model'] = mod
            region_arr1['realization'] = str(i)
            region_arr = pd.concat([region_arr,region_arr1])
            
    df = pd.concat([sensitivity,frac_arr,snd_arr, region_arr], axis=1).reset_index(level=['lat', 'lon'])
    df.dropna(subset = ['sensitivity','region'], inplace=True)
        #( ^ if columns 'change_area', 'change_tas', or 'region' contain NaN, remove that row)
    print ('df complete')
    return df


def create_df(change_treeArea, change_treefrac, change_tas, sndbase, tasbase, base_treearea, noLu_treearea, gridarea1):
    print ('\nmaking df...')
    
    x_arr=pd.DataFrame()
    y1_arr=pd.DataFrame()
    frac_arr=pd.DataFrame()
    snd_arr=pd.DataFrame()
    tasbase_arr=pd.DataFrame()
    base_treearea_arr=pd.DataFrame()
    noLu_treearea_arr=pd.DataFrame()
    gridarea_arr=pd.DataFrame()
    
    region_arr=pd.DataFrame()
    regions = {}
    
    for mod in models:
        print ('starting '+mod+'...')
        regions[mod]= {}
        for i in change_treeArea[mod]:
            print('r'+str(i)+"...")
            #tree area
            x_arr1 = change_treeArea[mod][i].to_dataframe('change_area')
            x_arr= pd.concat([x_arr,x_arr1])
            #tree frac
            frac_arr1 = change_treefrac[mod][i].to_dataframe('change_frac')
            frac_arr= pd.concat([frac_arr,frac_arr1])
            #change tas
            y1_arr1 = change_tas[mod][i].to_dataframe('change_tas')
            y1_arr = pd.concat([y1_arr,y1_arr1])
            #tas base (min)
            tasbase_arr1 = tasbase[mod][i].to_dataframe('min_tas_base')
            tasbase_arr = pd.concat([tasbase_arr,tasbase_arr1])
            #snd
            snd_arr1 = sndbase[mod][i].to_dataframe('snd')
            snd_arr = pd.concat([snd_arr,snd_arr1]) 
            #tree area base
            base_treearea_arr1 = base_treearea[mod][i].to_dataframe('base_treearea')
            base_treearea_arr=pd.concat([base_treearea_arr,base_treearea_arr1])
            #tree area noLu
            noLu_treearea_arr1 = noLu_treearea[mod][i].to_dataframe('noLu_treearea')
            noLu_treearea_arr=pd.concat([noLu_treearea_arr,noLu_treearea_arr1])
            #gridarea
            gridarea_arr1 = gridarea1[mod][i].to_dataframe('gridarea')
            gridarea_arr=pd.concat([gridarea_arr,gridarea_arr1])
            #AR6
            regions[mod][i] = ar6_mask(change_treeArea[mod][i])
            region_arr1 = regions[mod][i].to_dataframe('region')
            region_arr1['model'] = mod
            region_arr1['realization'] = str(i)
            region_arr = pd.concat([region_arr,region_arr1])
            
    df = pd.concat([x_arr,y1_arr,frac_arr,snd_arr,tasbase_arr, base_treearea_arr, noLu_treearea_arr, gridarea_arr, region_arr], axis=1).reset_index(level=['lat', 'lon'])
    df.dropna(subset = ['change_area', 'change_tas', 'region' ], inplace=True)
        #( ^ if columns 'change_area', 'change_tas', or 'region' contain NaN, remove that row)
    print ('df complete')
    return df


def label_cont (row):
   if row['region'] in continents['North America']:
      return 'North America'
   if row['region'] in continents['South America']:
      return 'South America'
   if row['region'] in continents['Europe']:
      return 'Europe'
   if row['region'] in continents['Asia']:
      return 'Asia'
   if row['region'] in continents['Africa']:
      return 'Africa' 


def threshold_df(df, percent_threshold):
    print ('\nplot threshold = '+str(percent_threshold)+"%")
    pos_thres_df = df[df.change_frac > percent_threshold]
    neg_thres_df = df[df.change_frac < -percent_threshold]
    thres_df = pd.concat([pos_thres_df,neg_thres_df])
    return thres_df

def label_df(df):
  
    regions_df = df[df['region'].isin(regionlist)]

    regions_df['continent'] = regions_df.apply(lambda row : label_cont(row), axis = 1)
    
    dtypedict = {'lat':         float,
                 'lon':         float,
                 'change_area': float,
                 'change_tas':  float,
                 'change_frac': float,
                 'snd':         float,
                 'base_treearea':float,
                 'noLu_treearea':float,
                 'region':      int,
                 'model':       str,
                 'realization': int,
                 'continent':   str}
    

    regions_df=regions_df.astype(dtypedict)
    
    return regions_df


def label_sens_df(sens_df):
    regions_df = sens_df[sens_df['region'].isin(regionlist)]
    regions_df['continent'] = regions_df.apply(lambda row : label_cont(row), axis = 1)
    return regions_df


def getsnowpercent(df, snd_thres): 
    snowpercent_df=pd.DataFrame()
    for mod in models:
        mod_df = df.loc[df['model'] == mod]
        for cont in continents:
            cont_df = mod_df.loc[mod_df['continent'] == cont]
            for r in range(cont_df['realization'].min(), cont_df['realization'].max()+1):
                r_df = cont_df.loc[cont_df['realization'] == r]
                snow_df = r_df[r_df['snd'] > snd_thres]
                
                if r_df['snd'].shape[0] == 0:
                    snow_percent = float('NaN')
                else:
                    snow_percent = snow_df['gridarea'].sum()/r_df['gridarea'].sum()*100
                    snow_area = snow_df['gridarea'].sum()/1e6
    
                row = pd.DataFrame([mod, r, cont, snow_percent, snow_area]).T
                row.columns=['Model','Realization', 'Continent','Snow %', 'snow area(million km2)']
                # dtypedict = {'Model':str,'Realization':int,'Continent':str,'Snow %':float}
                # row=row.astype(dtypedict)
                snowpercent_df = pd.concat([snowpercent_df,row],axis=0)
    
    return snowpercent_df


def tree_area_calc(df, column_name): 
    
    '''only works for ensemble averages not individual realizations'''
    
    area_df=pd.DataFrame()
    for mod in models:
        mod_df = df.loc[df['model'] == mod]
        for cont in continents:
            cont_df = mod_df.loc[mod_df['continent'] == cont]
            area=cont_df[column_name].sum()
            row = pd.DataFrame([area,mod,cont]).T
            row.columns=[column_name,'model','continent']
            area_df= pd.concat([area_df,row],axis=0)
    
    return area_df


def descriptive_stats(df,column_name): 
    
    '''only gives stats across all realizations not for indiviual ones'''
    
    stats_df=pd.DataFrame()
    for mod in models:
        mod_df = df.loc[df['model'] == mod]
        for cont in continents:
            cont_df = mod_df.loc[mod_df['continent'] == cont]
            
            minimum=cont_df[column_name].min()
            maximum=cont_df[column_name].max()
            average=cont_df[column_name].mean()
            
            row = pd.DataFrame([minimum,maximum,average,mod,cont]).T
            row.columns=['minimum','maximum','average','model','continent']
            
            stats_df= pd.concat([stats_df,row],axis=0)
    
    return stats_df

def getsensitivity(df, mean_tasbase, tastype, snd_thres):           
    sensitivity_df=pd.DataFrame()
    for mod in models:
        mod_df = df.loc[df['model'] == mod]
        for r in range(mod_df['realization'].min(), mod_df['realization'].max()+1):
            r_df = mod_df.loc[mod_df['realization'] == r]
            GMT = mean_tasbase[mod][r]
            for cont in continents:
                cont_df = r_df.loc[r_df['continent'] == cont]                  
                    
                if not cont_df.loc[:,'change_area'].empty and not cont_df.loc[:,tastype].empty:
                        X=np.array(cont_df.loc[:,'change_area'])
                        Y=np.array(cont_df.loc[:,tastype])
                        
                        #mask the nans and do linear regresion:
                        mask = ~np.isnan(X) & ~np.isnan(Y)
                        result = stats.linregress(X[mask], Y[mask]) # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
                        
                        #store results and calculate confidence interval
                        slope, stderr, intercept = result.slope, result.stderr, result.intercept
                        degF=len(X[mask])-2
                        tcrit = stats.t.ppf(.975, degF) #https://www.statology.org/how-to-find-the-t-critical-value-in-python/  
                        CI_lower = slope-tcrit*stderr
                        CI_upper = slope+tcrit*stderr
                        
                else:
                    slope = float('NaN')
                    CI_lower = float('NaN')
                    CI_upper = float('NaN') 
                    intercept = float('NaN')
                    
                tasbase = cont_df['min_tas_base'].mean()-273.15 #convert from kelvin to celcius
                
                snow_df = cont_df[cont_df['snd'] > snd_thres]
                if cont_df['snd'].shape[0] == 0:
                    snow_percent = float('NaN')
                else:
                    snow_percent = snow_df['gridarea'].sum()/cont_df['gridarea'].sum()*100
                
                row = pd.DataFrame([mod, r, cont, slope, CI_lower, CI_upper, intercept, tasbase, GMT, snow_percent]).T
                row.columns=['Model','Realization','Continent',
                             'Slope','Confidence Interval Lower','Confidence Interval Upper','Intercept', 
                             'tas base by cont', 'GMT base', 'snow cover % hist']
                dtypedict = {'Model':str,
                             'Realization':int,
                             'Continent':str,
                             'Slope':float,
                             'Confidence Interval Lower':float,
                             'Confidence Interval Upper':float,
                             'Intercept':float,
                             'tas base by cont':float,
                             'GMT base':float,
                             'snow cover % hist':float}
                row=row.astype(dtypedict)
                sensitivity_df = pd.concat([sensitivity_df,row],axis=0)
    
    return sensitivity_df


def time_loop_am(data_dict, GMT_data_dict, gridarea, base_scen, noLu_scen, y1, duration, startyear, tstep_size, multimodav_flag,
                 percent_threshold, snd_thres):
    # loop to caculate sensitiviy over each timestep
    sensitivity=pd.DataFrame()
    timesteps = range(startyear, duration+1, tstep_size)                      
    for endyear in timesteps:
        print('\n\n\n'+str(y1+endyear-30)+'-'+str(y1+endyear-1)+'\n\n\n')
        print("calculating changes in tree area and TAS...")
        # convert to to tree area from treefrac and calculate changes in TAS and tree area
        change_treeArea, change_treefrac, change_tas, sndbase, mean_tasbase, tasbase, base_treearea, noLu_treearea, gridarea1 = thirty_year_averages(data_dict, GMT_data_dict, gridarea, base_scen, noLu_scen, y1, endyear, multimodav_flag)

        # add change_treeArea and change_tas to a data frame 
        df = create_df(change_treeArea, change_treefrac, change_tas, sndbase,  tasbase, base_treearea, noLu_treearea, gridarea1)
        
        #apply the percent threshold for plotting to the dataframe and label the continents 
        regions_df = label_df(threshold_df(df,percent_threshold))
        
        #get sensitivity using linear regression
        print("calculating sensitivities...")
        sensitivity1 = getsensitivity(regions_df, mean_tasbase,'change_tas', snd_thres)
        sensitivity1['Year'] = float(y1+endyear-30)       
        sensitivity = pd.concat([sensitivity,sensitivity1])
        print("loop done")
        
    return sensitivity




#%%==============================================================================
# plots
#================================================================================

def scatterplot_future_scen(dataframe, plotDIR, plotname, sensitivities_scen1, sensitivities_scen2,snowconts_only_flg): 
    print('\nplotting '+plotname+'.png')
    
    if snowconts_only_flg == True:
        conts = cont_order[0:3]
    else:
        conts = cont_order
    
    g = sns.lmplot(x="change_area", 
                   y="change_tas", 
                   col='model', 
                   row='continent',
                   hue='scenario',
                   data=dataframe, 
                   row_order=conts,
                   legend_out=True,
                   height=4.5, 
                   aspect=1,
                   ci=None)
    axes = g.axes.flatten()
    
    #define fontsizes
    size_axisnumbers    = 20
    size_axislabels     = 24
    size_modandcont     = 28
    size_legend         = 28
    size_letters        = 28
    size_onplottext     = 20
    
    #axis range limits
    g.set(ylim=(-4,6))
    g.set(xlim=(-60000,60000))
    
    # rename and resize legend
    sns.move_legend(g,'center',bbox_to_anchor=(0.48, -0.1),ncol=2, title=None)
    new_labels = ['SSP1-2.6', 'SSP3-7.0']
    for t, l in zip(g._legend.texts, new_labels):
        t.set_text(l)
    for text in g.legend.texts:
        text.set_fontsize(size_legend)

    
    # clear seaborn labelling
    for i,ax in enumerate(axes):
        ax.set_title('')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_title(letters[i],
                     fontweight='bold',
                     loc='left',
                     fontsize = size_letters)
        ax.tick_params(labelsize = size_axisnumbers)
        
    # sensitivity labels
    tas_labels=[]
    tasmax_labels=[]
    for cont in cont_order:
        tas_labels.extend(list(sensitivities_scen1[sensitivities_scen1.Continent==cont]['Slope']))
        tasmax_labels.extend(list(sensitivities_scen2[sensitivities_scen2.Continent==cont]['Slope']))
    for i,ax in enumerate(axes):
        ax.text(55000, 4.5, 
                'Sensitivities:' + 
                '\nSSP1-2.6 = '+ format(tas_labels[i],'.1e')+
                '\nSSP3-7.0 = '+ format(tasmax_labels[i],'.1e'),
                horizontalalignment='right', 
                verticalalignment='center', 
                fontsize = size_onplottext, 
                color='black')
        
    # xaxis label
    xlbl_ax = g.axes[-1,:]
    for ax in xlbl_ax:
        ax.set_xlabel('TreeArea\ndifference [$km^2$]', fontsize = size_axislabels)
        
    # model labels
    r1_axes = g.axes[0,:]
    for i,ax in enumerate(r1_axes):
        if models[i] == 'multimodel_average':
            ax.set_title('Multimodel\nAverage',
                     fontweight='bold',
                     loc='center', 
                     fontsize = size_modandcont)
        else:
            ax.set_title(models[i],
                     fontweight='bold',
                     loc='center', 
                     fontsize = size_modandcont)
        
    # y axis and continent labels
    c1_axes = g.axes[:,0]
    for i,ax in enumerate(c1_axes):
        ax.set_ylabel('TAS change [°C]', fontsize = size_axislabels)
        ax.text(-0.4,
                0.5,
                cont_order[i],
                verticalalignment='center',
                transform=ax.transAxes,
                fontweight='bold',
                rotation='vertical', 
                fontsize = size_modandcont)
 
    #save figure             
    plt.savefig(plotDIR + '/' + plotname+'.png', bbox_inches='tight')
    
    
def bypixel_hist_2row(sensitivity_dataframe, xname, plotDIR, plotname):
    
    #define fontsizes
    size_axisnumbers    = 20
    size_axislabels     = 24
    size_modandcont     = 28
    size_legend         = 28
    size_letters        = 28
    
    df=sensitivity_dataframe.reset_index(drop=True)
    #make test plot to get legend dictionary from facet grid
    leg = sns.FacetGrid(data=df, row='scenario',col='continent',col_order=cont_order,hue='model')
    leg.map_dataframe(sns.histplot, data=df,x=xname)
    leg.add_legend()
    legend_data=(leg._legend_data)
    #create actual plot using legend dictionary but apply hue in histplot to be able to use multiple='stack'
    g = sns.FacetGrid(data=df, row='scenario', col='continent',col_order=cont_order, height=4.5, aspect=1)
    g.map_dataframe(sns.histplot, data=df,x=xname, hue='model', multiple="stack",binwidth=.0001)
    g.add_legend(legend_data)#, title='model')
    sns.move_legend(g,'center',bbox_to_anchor=(0.48, -0.15),ncol=4)
    for text in g.legend.texts:
        text.set_fontsize(size_legend)
    
    #axis range limits
    #g.set(ylim=(0,800))
    g.set(xlim=(-0.0021,0.0021))
    
    # clear seaborn labelling
    axes = g.axes.flatten()
    for i,ax in enumerate(axes):
        ax.set_title('')
        ax.set_ylabel('Count',fontsize = size_axislabels)
        ax.set_xlabel('Sensitivity',fontsize = size_axislabels)
        ax.set_title(letters[i],
                      fontweight='bold',
                      loc='left',
                      fontsize = size_letters) 
        ax.tick_params(labelsize = size_axisnumbers)
        ax.tick_params(axis='x', rotation=45)
        
    # continent labels
    r1_axes = g.axes[0,:]
    for i,ax in enumerate(r1_axes):
        ax.set_title(cont_order[i],
                     fontweight='bold',
                     loc='center', 
                     fontsize = size_modandcont)
        
    # scenario labels
    scens=['SSP1-2.6','SSP3-7.0']
    c1_axes = g.axes[:,0]
    for i,ax in enumerate(c1_axes):
        ax.text(-0.35,
                0.5,
                scens[i],
                verticalalignment='center',
                transform=ax.transAxes,
                fontweight='bold',
                rotation='vertical', 
                fontsize = size_modandcont)
        
    plt.savefig(plotDIR + '/' + plotname+'.png', bbox_inches='tight')

def bypixel_hist_snowcover(sensitivity_dataframe, xname, plotDIR, plotname):
    
    #define fontsizes
    size_axisnumbers    = 20
    size_axislabels     = 24
    size_modandcont     = 28
    size_legend         = 28
    size_letters        = 28
    
    df=sensitivity_dataframe.reset_index(drop=True)
    #make test plot to get legend dictionary from facet grid
    leg = sns.FacetGrid(data=df, row='scenario',col='continent',col_order=cont_order,hue='snowcover')
    leg.map_dataframe(sns.histplot, data=df,x=xname)
    leg.add_legend()
    legend_data=(leg._legend_data)
    #create actual plot using legend dictionary but apply hue in histplot to be able to use multiple='stack'
    g = sns.FacetGrid(data=df, row='scenario', col='continent',col_order=cont_order, height=4.5, aspect=1)
    g.map_dataframe(sns.histplot, data=df,x=xname, hue='snowcover', multiple="stack",binwidth=.0001)
    g.add_legend(legend_data, title='')
    sns.move_legend(g,'center',bbox_to_anchor=(0.48, -0.15),ncol=2)
    new_labels = ['no snow cover', 'snow cover']
    for t, l in zip(g._legend.texts, new_labels):
        t.set_text(l)
    for text in g.legend.texts:
        text.set_fontsize(size_legend) 
                    
    #axis range limits
    #g.set(ylim=(0,800))
    g.set(xlim=(-0.0021,0.0021))
    
    # clear seaborn labelling
    axes = g.axes.flatten()
    for i,ax in enumerate(axes):
        ax.set_title('')
        ax.set_ylabel('Count',fontsize = size_axislabels)
        ax.set_xlabel('Sensitivity',fontsize = size_axislabels)
        ax.set_title(letters[i],
                      fontweight='bold',
                      loc='left',
                      fontsize = size_letters)  
        ax.tick_params(labelsize = size_axisnumbers)
        ax.tick_params(axis='x', rotation=45)
        
    # continent labels
    r1_axes = g.axes[0,:]
    for i,ax in enumerate(r1_axes):
        ax.set_title(cont_order[i],
                     fontweight='bold',
                     loc='center', 
                     fontsize = size_modandcont)
        
    # scenario labels
    scens=['SSP1-2.6','SSP3-7.0']
    c1_axes = g.axes[:,0]
    for i,ax in enumerate(c1_axes):
        ax.text(-0.35,
                0.5,
                scens[i],
                verticalalignment='center',
                transform=ax.transAxes,
                fontweight='bold',
                rotation='vertical', 
                fontsize = size_modandcont)
        
    plt.savefig(plotDIR + '/' + plotname+'.png', bbox_inches='tight')
    
