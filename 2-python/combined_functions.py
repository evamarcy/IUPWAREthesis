# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 14:11:02 2021

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#function library for WP2 combining histrical and future scenarios

#%%==============================================================================
# import
# ===============================================================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

#%%==============================================================================
# define variables 
#================================================================================
models = ['CanESM5', 'CNRM-ESM2-1', 'IPSL-CM6A-LR','UKESM1-0-LL', 'multimodel_average']
scenarios = ["ssp126", "ssp370", "ssp126-ssp370Lu", "ssp370-ssp126Lu"]
scenpairs = ["hist","ssp126", "ssp370"]
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

def getsensitivity(df,x_axisname):           
    sensitivity_df=pd.DataFrame()
    for scen in scenpairs:
        scen_df = df.loc[df['scenario'] == scen]
        for mod in models:
            mod_df = scen_df.loc[scen_df['Model'] == mod]
            for r in range(mod_df['Realization'].min(), mod_df['Realization'].max()+1):
                r_df = mod_df.loc[mod_df['Realization'] == r]
                for cont in continents:
                    cont_df = r_df.loc[r_df['Continent'] == cont]                  
                        
                    if not cont_df[x_axisname].empty and not cont_df['Slope'].empty:
                            X=np.array(cont_df[x_axisname])
                            Y=np.array(cont_df['Slope'])
                           
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

                                       
                    row = pd.DataFrame([scen, mod, r, cont, slope, CI_lower, CI_upper, intercept]).T
                    row.columns=['scenario','Model','Realization','Continent',
                                 'Slope','Confidence Interval Lower','Confidence Interval Upper','Intercept']
                    dtypedict = {'scenario':str,
                                'Model':str,
                                 'Realization':int,
                                 'Continent':str,
                                 'Slope':float,
                                 'Confidence Interval Lower':float,
                                 'Confidence Interval Upper':float,
                                 'Intercept':float}
                    row=row.astype(dtypedict)
                    sensitivity_df = pd.concat([sensitivity_df,row],axis=0)
    
    return sensitivity_df
            

#%%==============================================================================
# plots
#================================================================================

def sensitivityvstime(dataframe, plotDIR, plotname): 
    print('\nplotting '+plotname)
    g = sns.lmplot(x="Year", 
                   y="Slope", 
                   col='Model', 
                   row='Continent',
                   hue='scenario',
                   palette = ['#1f77b4','#2ca02c','#ff7f0e'],
                   data=dataframe, 
                   row_order=cont_order,
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
    
    #define axis range limits
    #g.set(ylim=(-0.0005,0.0002))
    g.set(xlim=(1850,2100)) 
    
    # clear seaborn labelling
    for i,ax in enumerate(axes):
        ax.set_title('')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_title(letters[i],
                     fontweight='bold',
                     loc='left',
                     fontsize = size_letters)
        ax.axhline(0,color='black',ls=':')
        ax.tick_params(labelsize = size_axisnumbers)
        
    # rename and resize legend
    sns.move_legend(g,'center',bbox_to_anchor=(0.48, -0.03),ncol=3, title=None)
    new_labels = ['Historical','SSP1-2.6', 'SSP3-7.0']
    for t, l in zip(g._legend.texts, new_labels):
        t.set_text(l)
    for text in g.legend.texts:
        text.set_fontsize(size_legend)
        
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
        
    # region labels
    c1_axes = g.axes[:,0]
    for i,ax in enumerate(c1_axes):
        ax.set_ylabel('Sensitivity [°C/$km^2$]', fontsize = size_axislabels)
        ax.text(-0.6,
                0.5,
                cont_order[i],
                verticalalignment='center',
                transform=ax.transAxes,
                fontweight='bold',
                rotation='vertical', 
                fontsize = size_modandcont)
   
        
    # xaxis label
    xlbl_ax = g.axes[-1,:]
    for ax in xlbl_ax:
        ax.set_xlabel('Year', fontsize = size_axislabels)
             
    plt.savefig(plotDIR + '/' + plotname, bbox_inches='tight')
    

    
def sensitivityvsGMT(dataframe, plotDIR, plotname, GMTscaling): 
    print('\nplotting '+plotname)
    g = sns.lmplot(x='GMT_anomaly', 
                   y="Slope", 
                   col='Model', 
                   row='Continent',
                   hue='scenario',
                   palette = ['#1f77b4','#2ca02c','#ff7f0e'],
                   data=dataframe, 
                   row_order=cont_order,
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
    
    #define axis range limits
    g.set(ylim=(-0.0005,0.0002))
    #g.set(xlim=(-60000,60000)) 
    
    # clear seaborn labelling
    for i,ax in enumerate(axes):
        ax.set_title('')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_title(letters[i],
                     fontweight='bold',
                     loc='left',
                     fontsize = size_letters)
        ax.axhline(0,color='black',ls=':')
        ax.tick_params(labelsize = size_axisnumbers)
    
    # rename and resize legend
    sns.move_legend(g,'center',bbox_to_anchor=(0.48, -0.03),ncol=3, title=None)
    new_labels = ['Historical','SSP1-2.6', 'SSP3-7.0']
    for t, l in zip(g._legend.texts, new_labels):
        t.set_text(l)
    for text in g.legend.texts:
        text.set_fontsize(size_legend)
        
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
    
    # xaxis label
    xlbl_ax = g.axes[-1,:]
    for ax in xlbl_ax:
        ax.set_xlabel('GMT Anomaly [°C]', fontsize = size_axislabels)  
        
    # region labels
    c1_axes = g.axes[:,0]
    for i,ax in enumerate(c1_axes):
        ax.set_ylabel('Sensitivity [°C/$km^2$]', fontsize = size_axislabels)
        ax.text(-0.6,
                0.5,
                cont_order[i],
                verticalalignment='center',
                transform=ax.transAxes,
                fontweight='bold',
                rotation='vertical', 
                fontsize = size_modandcont)
        
    # sensitivity labels
    labels_hist=[]
    labels_126=[]
    labels_370=[]
    for cont in cont_order:
        labels_hist.extend(list(GMTscaling[GMTscaling.Continent==cont][GMTscaling.scenario=='hist']['Slope']))
        labels_126.extend(list(GMTscaling[GMTscaling.Continent==cont][GMTscaling.scenario=='ssp126']['Slope']))
        labels_370.extend(list(GMTscaling[GMTscaling.Continent==cont][GMTscaling.scenario=='ssp370']['Slope']))
    for i,ax in enumerate(axes):
        ax.text(7, -0.00035, 'Slopes:'+
                '\nHistorical = '+ format(labels_hist[i],'.1e')+
                '\nSSP1-2.6 = '+ format(labels_126[i],'.1e')+
                '\nSSP3-7.0 = '+ format(labels_370[i],'.1e'),
                horizontalalignment='right', 
                verticalalignment='center',
                fontsize = size_onplottext, 
                color='black')
             
    plt.savefig(plotDIR + '/' + plotname, bbox_inches='tight')
    
def sensitivityvssnowcoverpercent(dataframe, plotDIR, plotname, snowscaling): 
    print('\nplotting '+plotname)
    g = sns.lmplot(x='snow cover % hist', 
                   y="Slope", 
                   col='Model', 
                   row='Continent',
                   hue='scenario',
                   palette = ['#1f77b4','#2ca02c','#ff7f0e'],
                   data=dataframe, 
                   row_order=cont_order[0:3],
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
    
    # clear seaborn labelling
    for i,ax in enumerate(axes):
        ax.set_title('')
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_title(letters[i],
                     fontweight='bold',
                     loc='left', 
                     fontsize = size_letters)
        ax.axhline(0,color='black',ls=':')
        ax.tick_params(labelsize = size_axisnumbers)
        
    # rename and resize legend
    sns.move_legend(g,'center',bbox_to_anchor=(0.48, -0.07),ncol=3, title=None)
    new_labels = ['Historical','SSP1-2.6', 'SSP3-7.0']
    for t, l in zip(g._legend.texts, new_labels):
        t.set_text(l)
    for text in g.legend.texts:
        text.set_fontsize(size_legend)
        
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
        
    # region labels
    c1_axes = g.axes[:,0]
    for i,ax in enumerate(c1_axes):
        ax.set_ylabel('Sensitivity [°C/$km^2$]', fontsize = size_axislabels )
        ax.text(-0.6,
                0.5,
                cont_order[i],
                verticalalignment='center',
                transform=ax.transAxes,
                fontweight='bold',
                rotation='vertical', 
                fontsize = size_modandcont)
        
    # xaxis label
    xlbl_ax = g.axes[-1,:]
    for ax in xlbl_ax:
        ax.set_xlabel('snow cover %\n(base scenario)', fontsize = size_axislabels )
        
    # sensitivity labels
    labels_hist=[]
    labels_126=[]
    labels_370=[]
    for cont in cont_order[0:3]:
        labels_hist.extend(list(snowscaling[snowscaling.Continent==cont][snowscaling.scenario=='hist']['Slope']))
        labels_126.extend(list(snowscaling[snowscaling.Continent==cont][snowscaling.scenario=='ssp126']['Slope']))
        labels_370.extend(list(snowscaling[snowscaling.Continent==cont][snowscaling.scenario=='ssp370']['Slope']))
    for i,ax in enumerate(axes):
        ax.text(0, -0.00035, 'Slopes'+
                '\nHist: '+ format(labels_hist[i],'.1e')+
                '\n1-2.6: '+ format(labels_126[i],'.1e')+
                '\n3-7.0: '+ format(labels_370[i],'.1e'),
                horizontalalignment='left', 
                verticalalignment='center',
                fontsize = size_onplottext, 
                color='black')
             
    plt.savefig(plotDIR + '/' + plotname, bbox_inches='tight')