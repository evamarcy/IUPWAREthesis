# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:11:21 2022

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#function library for plotting historical scenario maps of 
#-change in tas
#-deforestation
#-sensitivity

#%%==============================================================================
# import
# ===============================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs

#%%==============================================================================
# function library
#================================================================================


#%%============================================================================
def data_lumper(dataset,
                models
                ):
    
    data = np.empty(1)
    for mod in models:
        mod_data = dataset[mod][1].values.flatten()
        data = np.append(data,mod_data)
        
    data = data[~np.isnan(data)]
    return data

#%%============================================================================
def colormap_details(sequence_string,
                     data,
                     null_bnds,
                     decimal, 
                     onetail_flag):

    # identify colors for land cover transition trends
    cmap_brbg = plt.cm.get_cmap(sequence_string)
    cmap55 = cmap_brbg(0.01)  
    cmap45 = cmap_brbg(0.1)  #blue
    cmap35 = cmap_brbg(0.2)
    cmap30 = cmap_brbg(0.25)
    cmap25 = cmap_brbg(0.3)
    cmap10 = cmap_brbg(0.4)
    cmap0 = 'white'
    cmap_10 = cmap_brbg(0.6)
    cmap_25 = cmap_brbg(0.7)
    cmap_30 = cmap_brbg(0.75)
    cmap_35 = cmap_brbg(0.8)
    cmap_45 = cmap_brbg(0.9)  #red 
    cmap_55 = cmap_brbg(0.99)

    colors = [cmap_45,
              cmap_35,
              cmap_30,
              cmap_25,
              cmap_10,
              cmap0,
              cmap10,
              cmap25,
              cmap30,
              cmap35,
              cmap45]
    
    if onetail_flag== True:
        colors = [
              'white',
              cmap_brbg(0.2),
              cmap_brbg(0.4),
              cmap_brbg(0.6),
              cmap_brbg(0.8),
              cmap_brbg(0.99)]
        

    cmap_list = mpl.colors.ListedColormap(colors,
                                          N=len(colors))
    

    cmap_list.set_over(cmap55)
    cmap_list.set_under(cmap_55)
        
    if onetail_flag== True:
        cmap_list.set_under('white')
        cmap_list.set_over(cmap_brbg(0.99))
        
    
    q_samples = []
    q_samples.append(np.abs(np.quantile(data,0.99)))
    q_samples.append(np.abs(np.quantile(data,0.01)))
        
    start = np.around(np.max(q_samples),decimals=decimal)
    inc = start/6
    
    values = [np.around(-1*start,decimals=decimal),
              np.around(-1*start+inc,decimals=decimal),
              np.around(-1*start+inc*2,decimals=decimal),
              np.around(-1*start+inc*3,decimals=decimal),
              np.around(-1*start+inc*4,decimals=decimal),
              null_bnds[0],
              null_bnds[1],
              np.around(start-inc*4,decimals=decimal),
              np.around(start-inc*3,decimals=decimal),
              np.around(start-inc*2,decimals=decimal),
              np.around(start-inc,decimals=decimal),
              np.around(start,decimals=decimal)]

    tick_locs = [np.around(-1*start,decimals=decimal),
                 np.around(-1*start+inc,decimals=decimal),
                 np.around(-1*start+inc*2,decimals=decimal),
                 np.around(-1*start+inc*3,decimals=decimal),
                 np.around(-1*start+inc*4,decimals=decimal),
                 0,
                 np.around(start-inc*4,decimals=decimal),
                 np.around(start-inc*3,decimals=decimal),
                 np.around(start-inc*2,decimals=decimal),
                 np.around(start-inc,decimals=decimal),
                 np.around(start,decimals=decimal)]

    tick_labels = [str(np.around(-1*start,decimals=decimal)),
                   str(np.around(-1*start+inc,decimals=decimal)),
                   str(np.around(-1*start+inc*2,decimals=decimal)),
                   str(np.around(-1*start+inc*3,decimals=decimal)),
                   str(np.around(-1*start+inc*4,decimals=decimal)),
                   str(0),
                   str(np.around(start-inc*4,decimals=decimal)),
                   str(np.around(start-inc*3,decimals=decimal)),
                   str(np.around(start-inc*2,decimals=decimal)),
                   str(np.around(start-inc,decimals=decimal)),
                   str(np.around(start,decimals=decimal))]
    
    if onetail_flag== True:
        values = [
              null_bnds[0],
              null_bnds[1],
              np.around(start-inc*4,decimals=decimal),
              np.around(start-inc*3,decimals=decimal),
              np.around(start-inc*2,decimals=decimal),
              np.around(start-inc,decimals=decimal),
              np.around(start,decimals=decimal)]

        tick_locs = [
                 0,
                 np.around(start-inc*4,decimals=decimal),
                 np.around(start-inc*3,decimals=decimal),
                 np.around(start-inc*2,decimals=decimal),
                 np.around(start-inc,decimals=decimal),
                 np.around(start,decimals=decimal)]

        tick_labels = [
                   str(0),
                   str(np.around(start-inc*4,decimals=decimal)),
                   str(np.around(start-inc*3,decimals=decimal)),
                   str(np.around(start-inc*2,decimals=decimal)),
                   str(np.around(start-inc,decimals=decimal)),
                   str(np.around(start,decimals=decimal))]

    norm = mpl.colors.BoundaryNorm(values,cmap_list.N)
    
    return cmap_list,tick_locs,tick_labels,norm,values

#%%============================================================================

#maps of treefrac and temp change
def combined_plot(
    change_treeArea_masked, change_tas, tas_sensitivity_bypixel,
    models,
    letters,
    mapDIR,
    mapname
    ):
    
    col_cbticlbl = '0'   # colorbar color of tick labels
    col_cbtic = '0.5'   # colorbar color of ticks
    col_cbedg = '0.9'   # colorbar color of edge
    cb_ticlen = 3.5   # colorbar length of ticks
    cb_ticwid = 0.4   # colorbar thickness of ticks
    cb_edgthic = 0   # colorbar thickness of edges between colors
    cstlin_lw = 0.75   # linewidth for coastlines
    
    #define fontsizes
    size_cbarnumbers    = 16
    size_titles         = 22 # titles, models, cbar labels

    x=21
    y=16

    # placment change_tas cbar
    cb_lu_x0 = 0.1275
    cb_lu_y0 = 0.05
    cb_lu_xlen = 0.225
    cb_lu_ylen = 0.015

    # placment change_treeArea cbar
    cb_lc_x0 = 0.40175
    cb_lc_y0 = 0.05
    cb_lc_xlen = 0.225
    cb_lc_ylen = 0.015
    
    # placment tas_sensitivity_bypixel cbar
    cb_corr_x0 = 0.675
    cb_corr_y0 = 0.05
    cb_corr_xlen = 0.225
    cb_corr_ylen = 0.015

    # extent
    east = 180
    west = -180
    north = 80
    south = -60
    extent = [west,east,south,north]
    
    # boundaries of 0 for tas
    null_bnds_tas = [-0.01, 0.01]
    
    # boundaries of 0 for tree area
    null_bnds_tf = [-10, 10]
    # null_bnds_tf = [0,0]
    
    # boundaries of 0 for sensitivity
    null_bnds_sens = [-1e-8, 1e-8]
    # null_bnds_sens = [0, 0]
      

    cmap_list_tas,tick_locs_tas,tick_labels_tas,norm_tas,levels_tas = colormap_details('RdBu',
                                                                                  data_lumper(change_tas, models),
                                                                                  null_bnds_tas,
                                                                                  2,False)

    cmap_list_tf,tick_locs_tf,tick_labels_tf,norm_tf,levels_tf = colormap_details('BrBG',
                                                                                  data_lumper(change_treeArea_masked, models),
                                                                                  null_bnds_tf,
                                                                                  -2,False)
    
    cmap_list_sens,tick_locs_sens,tick_labels_sens,norm_sens,levels_sens = colormap_details('RdBu',
                                                                                            data_lumper(tas_sensitivity_bypixel, models),
                                                                                            null_bnds_sens,
                                                                                            5,False)

        
    f, axes = plt.subplots(nrows=len(models),
                        ncols=3,
                        figsize=(x,y),
                        subplot_kw={'projection':ccrs.PlateCarree()})

    cbax_tas = f.add_axes([cb_lu_x0, 
                        cb_lu_y0, 
                        cb_lu_xlen, 
                        cb_lu_ylen])
    cbax_tf = f.add_axes([cb_lc_x0, 
                        cb_lc_y0, 
                        cb_lc_xlen, 
                        cb_lc_ylen])
    cbax_sens = f.add_axes([cb_corr_x0, 
                            cb_corr_y0, 
                            cb_corr_xlen, 
                            cb_corr_ylen])    

    i = 0


    for mod,row_axes in zip(models,axes):
        
        change_tas[mod][1].plot(ax=row_axes[0],
                                    cmap=cmap_list_tas,
                                    cbar_ax=cbax_tas,
                                    levels=levels_tas,
                                    extend='both',
                                    center=0,
                                    add_labels=False)
        
        change_treeArea_masked[mod][1].plot(ax=row_axes[1],
                                cmap=cmap_list_tf,
                                cbar_ax=cbax_tf,
                                levels=levels_tf,
                                extend='both',
                                center=0,
                                add_labels=False)
    
        
        tas_sensitivity_bypixel[mod][1].plot(ax=row_axes[2],
                                             transform=ccrs.PlateCarree(),
                                             cmap=cmap_list_sens,
                                             cbar_ax=cbax_sens,
                                             levels=levels_sens,
                                             center=0,
                                             add_labels=False)
            
        for ax,column in zip(row_axes,['Change in tas','Deforestation','Sensivitity']):
            
            ax.set_extent(extent,
                        crs=ccrs.PlateCarree())
            ax.set_title(letters[i],
                        loc='left',
                        fontsize = size_titles,
                        fontweight='bold')
            ax.coastlines(linewidth=cstlin_lw)
            
            if column == 'Change in tas':
                    
                    title = {'CanESM5':'CanESM5', 
                             'CNRM-ESM2-1':'CNRM\n-ESM2-1', 
                             'IPSL-CM6A-LR':'IPSL\n-CM6A-LR', 
                             'UKESM1-0-LL':'UKESM1\n-0-LL', 
                             'multimodel_average':'Multimodel\nAverage'}
                    
                    
                    ax.text(-0.2,
                            0.1,
                            title[mod],
                            fontsize=size_titles,
                            fontweight='bold',
                            rotation='vertical',
                            transform=ax.transAxes)
            
            if i < 3:
                
                ax.set_title(column,
                            loc='center',
                            fontsize = size_titles,
                            fontweight='bold')
                
            i += 1

        # taschange colorbar
        cb_lu = mpl.colorbar.ColorbarBase(ax=cbax_tas, 
                                        cmap=cmap_list_tas,
                                        norm=norm_tas,
                                        spacing='uniform',
                                        orientation='horizontal',
                                        extend='both',
                                        ticks=tick_locs_tas,
                                        drawedges=False)
        cb_lu.set_label( 'Change in tas [°C]',
                        size=size_titles)
        cb_lu.ax.xaxis.set_label_position('top')
        cb_lu.ax.tick_params(labelcolor=col_cbticlbl,
                            labelsize=size_cbarnumbers,
                            color=col_cbtic,
                            length=cb_ticlen,
                            width=cb_ticwid,
                            direction='out'); 
        cb_lu.ax.set_xticklabels(tick_labels_tas,
                                rotation=45)
        cb_lu.outline.set_edgecolor(col_cbedg)
        cb_lu.outline.set_linewidth(cb_edgthic)

        # change treefrac colorbar
        cb_lc = mpl.colorbar.ColorbarBase(ax=cbax_tf, 
                                        cmap=cmap_list_tf,
                                        norm=norm_tf,
                                        spacing='uniform',
                                        orientation='horizontal',
                                        extend='both',
                                        ticks=tick_locs_tf,
                                        drawedges=False)
        cb_lc.set_label('Decrease in treeArea [$km^2$]',
                        size=size_titles)
        cb_lc.ax.xaxis.set_label_position('top')
        cb_lc.ax.tick_params(labelcolor=col_cbticlbl,
                            labelsize=size_cbarnumbers,
                            color=col_cbtic,
                            length=cb_ticlen,
                            width=cb_ticwid,
                            direction='out'); 
        cb_lc.ax.set_xticklabels(tick_labels_tf,
                                rotation=45)
        cb_lc.outline.set_edgecolor(col_cbedg)
        cb_lc.outline.set_linewidth(cb_edgthic)
        
        # corr lu + lc
        cb = mpl.colorbar.ColorbarBase(ax=cbax_sens, 
                                    cmap=cmap_list_sens,
                                    norm=norm_sens,
                                    spacing='uniform',
                                    orientation='horizontal',
                                    extend='both',
                                    ticks=tick_locs_sens,
                                    drawedges=False)
        cb.set_label('Sensitivity [°C/$km^2$]',
                    size=size_titles)
        cb.ax.xaxis.set_label_position('top')
        cb.ax.tick_params(labelcolor=col_cbticlbl,
                        labelsize=size_cbarnumbers,
                        color=col_cbtic,
                        length=cb_ticlen,
                        width=cb_ticwid,
                        direction='out'); 
        cb.ax.set_xticklabels(tick_labels_sens,
                            rotation=45)
        cb.outline.set_edgecolor(col_cbedg)
        cb.outline.set_linewidth(cb_edgthic)        

        f.savefig(mapDIR+mapname,bbox_inches='tight')
        
