# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:11:21 2022

@author: eveem
"""

#%%=============================================================================
# SUMMARY
# =============================================================================

#function library for plotting future scenario maps of 
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
def data_lumper(dataset1, 
                dataset2,
                models
                ):
    
    data = np.empty(1)
    for mod in models:
        mod_data1 = dataset1[mod][1].values.flatten()
        mod_data2 = dataset2[mod][1].values.flatten()
        data = np.append(data,mod_data1)
        data = np.append(data,mod_data2)
        
    data = data[~np.isnan(data)]
    return data


#%%============================================================================
def data_lumper_tas(dataset1, 
                    dataset2,
                    dataset3, 
                    dataset4,
                    models
                    ):
    
    data = np.empty(1)
    for mod in models:
        mod_data1 = dataset1[mod][1].values.flatten()
        mod_data2 = dataset2[mod][1].values.flatten()
        mod_data3 = dataset3[mod][1].values.flatten()
        mod_data4 = dataset4[mod][1].values.flatten()
        data = np.append(data,mod_data1)
        data = np.append(data,mod_data2)
        data = np.append(data,mod_data3)
        data = np.append(data,mod_data4)
        
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
    change_tas_126, change_tas_370, tas_sensitivity_bypixel_126, tas_sensitivity_bypixel_370,
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
    size_cbarnumbers    = 20
    size_titles         = 28 # titles, models, cbar labels

    x=28
    y=17

    # placment change_tas cbar
    cb_1_xlen = 0.225
    cb_1_ylen = 0.015
    cb_1_x0 = 0.315-(cb_1_xlen/2)
    cb_1_y0 = 0.05
    
    # placment tas_sensitivity_bypixel cbar
    cb_2_xlen = 0.225
    cb_2_ylen = 0.015
    cb_2_x0 = 0.715-(cb_2_xlen/2)
    cb_2_y0 = 0.05
    

    # extent
    east = 180
    west = -180
    north = 80
    south = -60
    extent = [west,east,south,north]
    
    # boundaries of 0 for tas
    null_bnds_tas = [-0.01, 0.01]
        
    # boundaries of 0 for sensitivity
    null_bnds_sens = [-1e-8, 1e-8]
    # null_bnds_sens = [0, 0]
      

    cmap_list_tas,tick_locs_tas,tick_labels_tas,norm_tas,levels_tas = colormap_details('RdBu',
                                                                                  data_lumper(change_tas_126, change_tas_370, models),
                                                                                  null_bnds_tas,
                                                                                  2,False)
    
    cmap_list_sens,tick_locs_sens,tick_labels_sens,norm_sens,levels_sens = colormap_details('RdBu',
                                                                                            data_lumper(tas_sensitivity_bypixel_126, tas_sensitivity_bypixel_370, models),
                                                                                            null_bnds_sens,
                                                                                            5,False)

        
    f, axes = plt.subplots(nrows=len(models),
                        ncols=4,
                        figsize=(x,y),
                        subplot_kw={'projection':ccrs.PlateCarree()})

    cbax_1 = f.add_axes([cb_1_x0, 
                        cb_1_y0, 
                        cb_1_xlen, 
                        cb_1_ylen])

    cbax_2 = f.add_axes([cb_2_x0, 
                            cb_2_y0, 
                            cb_2_xlen, 
                            cb_2_ylen])    

    i = 0


    for mod,row_axes in zip(models,axes):
        
        change_tas_126[mod][1].plot(ax=row_axes[0],
                                    cmap=cmap_list_tas,
                                    cbar_ax=cbax_1,
                                    levels=levels_tas,
                                    extend='both',
                                    center=0,
                                    add_labels=False)
        
        change_tas_370[mod][1].plot(ax=row_axes[1],
                                    cmap=cmap_list_tas,
                                    cbar_ax=cbax_1,
                                    levels=levels_tas,
                                    extend='both',
                                    center=0,
                                    add_labels=False)
    
        
        tas_sensitivity_bypixel_126[mod][1].plot(ax=row_axes[2],
                                             transform=ccrs.PlateCarree(),
                                             cmap=cmap_list_sens,
                                             cbar_ax=cbax_2,
                                             levels=levels_sens,
                                             center=0,
                                             add_labels=False)
        
        tas_sensitivity_bypixel_370[mod][1].plot(ax=row_axes[3],
                                             transform=ccrs.PlateCarree(),
                                             cmap=cmap_list_sens,
                                             cbar_ax=cbax_2,
                                             levels=levels_sens,
                                             center=0,
                                             add_labels=False)
            
        for ax,column in zip(row_axes,['Change in tas\nSSP1-2.6',
                                       'Change in tas\nSSP3-7.0',
                                       'Sensivitity\nSSP1-2.6',
                                       'Sensivitity\nSSP3-7.0' ]):
            
            ax.set_extent(extent,
                        crs=ccrs.PlateCarree())
            ax.set_title(letters[i],
                        loc='left',
                        fontsize = size_titles,
                        fontweight='bold')
            ax.coastlines(linewidth=cstlin_lw)
            
            if column == 'Change in tas\nSSP1-2.6':
                    
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
            
            if i < 4:
                
                ax.set_title(column,
                            loc='center',
                            fontsize = size_titles,
                            fontweight='bold')
                
            i += 1

        # taschange colorbar
        cb_1 = mpl.colorbar.ColorbarBase(ax=cbax_1, 
                                        cmap=cmap_list_tas,
                                        norm=norm_tas,
                                        spacing='uniform',
                                        orientation='horizontal',
                                        extend='both',
                                        ticks=tick_locs_tas,
                                        drawedges=False)
        cb_1.set_label( 'Change in tas [°C]',
                        size=size_titles)
        cb_1.ax.xaxis.set_label_position('top')
        cb_1.ax.tick_params(labelcolor=col_cbticlbl,
                            labelsize=size_cbarnumbers,
                            color=col_cbtic,
                            length=cb_ticlen,
                            width=cb_ticwid,
                            direction='out'); 
        cb_1.ax.set_xticklabels(tick_labels_tas,
                                rotation=45)
        cb_1.outline.set_edgecolor(col_cbedg)
        cb_1.outline.set_linewidth(cb_edgthic)


        
        # sensitivity colorbar
        cb_2 = mpl.colorbar.ColorbarBase(ax=cbax_2, 
                                    cmap=cmap_list_sens,
                                    norm=norm_sens,
                                    spacing='uniform',
                                    orientation='horizontal',
                                    extend='both',
                                    ticks=tick_locs_sens,
                                    drawedges=False)
        cb_2.set_label('Sensitivity [°C/$km^2$]',
                    size=size_titles)
        cb_2.ax.xaxis.set_label_position('top')
        cb_2.ax.tick_params(labelcolor=col_cbticlbl,
                        labelsize=size_cbarnumbers,
                        color=col_cbtic,
                        length=cb_ticlen,
                        width=cb_ticwid,
                        direction='out'); 
        cb_2.ax.set_xticklabels(tick_labels_sens,
                            rotation=45)
        cb_2.outline.set_edgecolor(col_cbedg)
        cb_2.outline.set_linewidth(cb_edgthic)        

        f.savefig(mapDIR+mapname,bbox_inches='tight')
        
        
#%%============================================================================

#maps of treefrac and temp change
def futurelanduse_plot(
    ssp126lu, ssp370lu, change_treeArea_masked, 
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
    y=15

    # placment col1 cbar
    cb_1_x0 = 0.1275
    cb_1_y0 = 0.05
    cb_1_xlen = 0.225
    cb_1_ylen = 0.015

    # placment col2 cbar
    cb_2_x0 = 0.40175
    cb_2_y0 = 0.05
    cb_2_xlen = 0.225
    cb_2_ylen = 0.015
    
    # placment col3 cbar
    cb_3_x0 = 0.675
    cb_3_y0 = 0.05
    cb_3_xlen = 0.225
    cb_3_ylen = 0.015

    # extent
    east = 180
    west = -180
    north = 80
    south = -60
    extent = [west,east,south,north]
    

    # boundaries of 0 for tree area
    null_bnds_tf = [-10, 10]


    cmap_list_tf,tick_locs_tf,tick_labels_tf,norm_tf,levels_tf = colormap_details('Greens',
                                                                                  data_lumper(ssp126lu,ssp370lu, models),
                                                                                  null_bnds_tf,
                                                                                  -2,True)
    
    cmap_list_change,tick_locs_change,tick_labels_change,norm_change,levels_change = colormap_details('BrBG_r',
                                                                                            data_lumper(change_treeArea_masked,change_treeArea_masked, models),
                                                                                            null_bnds_tf,
                                                                                            -2,False)

        
    f, axes = plt.subplots(nrows=len(models),
                        ncols=3,
                        figsize=(x,y),
                        subplot_kw={'projection':ccrs.PlateCarree()})

    cbax_1 = f.add_axes([cb_1_x0, 
                        cb_1_y0, 
                        cb_1_xlen, 
                        cb_1_ylen])
    cbax_2 = f.add_axes([cb_2_x0, 
                        cb_2_y0, 
                        cb_2_xlen, 
                        cb_2_ylen])
    cbax_3 = f.add_axes([cb_3_x0, 
                            cb_3_y0, 
                            cb_3_xlen, 
                            cb_3_ylen])    

    i = 0


    for mod,row_axes in zip(models,axes):
        
        ssp126lu[mod][1].plot(ax=row_axes[0],
                                    cmap=cmap_list_tf,
                                    cbar_ax=cbax_1,
                                    levels=levels_tf,
                                    extend='both',
                                    center=0,
                                    add_labels=False)
        
        ssp370lu[mod][1].plot(ax=row_axes[1],
                                cmap=cmap_list_tf,
                                cbar_ax=cbax_2,
                                levels=levels_tf,
                                extend='both',
                                center=0,
                                add_labels=False)
    
        
        change_treeArea_masked[mod][1].plot(ax=row_axes[2],
                                             transform=ccrs.PlateCarree(),
                                             cmap=cmap_list_change,
                                             cbar_ax=cbax_3,
                                             levels=levels_change,
                                             center=0,
                                             add_labels=False)
            
        for ax,column in zip(row_axes,['SSP1-2.6 TreeArea','SSP3-7.0 TreeArea','Difference in TreeArea']):
            
            ax.set_extent(extent,
                        crs=ccrs.PlateCarree())
            ax.set_title(letters[i],
                        loc='left',
                        fontsize = size_titles,
                        fontweight='bold')
            ax.coastlines(linewidth=cstlin_lw)
            
            if column == 'SSP1-2.6 TreeArea':
                
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

        # ssp126 colorbar
        cb_lu = mpl.colorbar.ColorbarBase(ax=cbax_1, 
                                        cmap=cmap_list_tf,
                                        norm=norm_tf,
                                        spacing='uniform',
                                        orientation='horizontal',
                                        extend='both',
                                        ticks=tick_locs_tf,
                                        drawedges=False)
        cb_lu.set_label( 'Tree Area [$km^2$]',
                        size=size_titles)
        cb_lu.ax.xaxis.set_label_position('top')
        cb_lu.ax.tick_params(labelcolor=col_cbticlbl,
                            labelsize=size_cbarnumbers,
                            color=col_cbtic,
                            length=cb_ticlen,
                            width=cb_ticwid,
                            direction='out'); 
        cb_lu.ax.set_xticklabels(tick_labels_tf,
                                rotation=45)
        cb_lu.outline.set_edgecolor(col_cbedg)
        cb_lu.outline.set_linewidth(cb_edgthic)

        # ssp370 colorbar
        cb_lc = mpl.colorbar.ColorbarBase(ax=cbax_2, 
                                        cmap=cmap_list_tf,
                                        norm=norm_tf,
                                        spacing='uniform',
                                        orientation='horizontal',
                                        extend='both',
                                        ticks=tick_locs_tf,
                                        drawedges=False)
        cb_lc.set_label('Tree Area [$km^2$]',
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
        
        # difference colorbar
        cb = mpl.colorbar.ColorbarBase(ax=cbax_3, 
                                    cmap=cmap_list_change,
                                    norm=norm_change,
                                    spacing='uniform',
                                    orientation='horizontal',
                                    extend='both',
                                    ticks=tick_locs_change,
                                    drawedges=False)
        cb.set_label('Tree Area Difference [$km^2$]\n(SSP370 minus SSP126)',
                    size=size_titles)
        cb.ax.xaxis.set_label_position('top')
        cb.ax.tick_params(labelcolor=col_cbticlbl,
                        labelsize=size_cbarnumbers,
                        color=col_cbtic,
                        length=cb_ticlen,
                        width=cb_ticwid,
                        direction='out'); 
        cb.ax.set_xticklabels(tick_labels_change,
                            rotation=45)
        cb.outline.set_edgecolor(col_cbedg)
        cb.outline.set_linewidth(cb_edgthic)        

        f.savefig(mapDIR+mapname,bbox_inches='tight')
        
        

#%%============================================================================

#maps of treefrac and temp change
def tasmaps_plot(
    ssp126_tas, ssp370_tas, ssp126_ssp370Lu_tas, ssp370_ssp126Lu_tas,
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
    size_cbarnumbers    = 18
    size_titles         = 28 # titles, models, cbar labels

    x=28
    y=12

    # placment tas cbar
    cb_1_xlen = 0.225
    cb_1_ylen = 0.015
    cb_1_x0 = 0.5-(cb_1_xlen/2)
    cb_1_y0 = 0.05

    # extent
    east = 180
    west = -180
    north = 80
    south = -60
    extent = [west,east,south,north]
    
    # boundaries of 0 for tas
    null_bnds_tas = [-0.01, 0.01]
        
    cmap_list_tas,tick_locs_tas,tick_labels_tas,norm_tas,levels_tas = colormap_details('RdBu',
                                                                                  data_lumper_tas(ssp126_tas, 
                                                                                                  ssp370_tas, 
                                                                                                  ssp126_ssp370Lu_tas, 
                                                                                                  ssp370_ssp126Lu_tas, 
                                                                                                  models),
                                                                                  null_bnds_tas,
                                                                                  2,False)
        
    f, axes = plt.subplots(nrows=len(models),
                        ncols=4,
                        figsize=(x,y),
                        subplot_kw={'projection':ccrs.PlateCarree()})

    cbax_1 = f.add_axes([cb_1_x0, 
                        cb_1_y0, 
                        cb_1_xlen, 
                        cb_1_ylen])
  

    i = 0


    for mod,row_axes in zip(models,axes):
        ssp126_tas, ssp370_tas, ssp126_ssp370Lu_tas, ssp370_ssp126Lu_tas,
        
        ssp126_tas[mod][1].plot(ax=row_axes[0],
                                    cmap=cmap_list_tas,
                                    cbar_ax=cbax_1,
                                    levels=levels_tas,
                                    extend='both',
                                    center=0,
                                    add_labels=False)
        
        ssp370_tas[mod][1].plot(ax=row_axes[1],
                                    cmap=cmap_list_tas,
                                    cbar_ax=cbax_1,
                                    levels=levels_tas,
                                    extend='both',
                                    center=0,
                                    add_labels=False)
    
        
        ssp126_ssp370Lu_tas[mod][1].plot(ax=row_axes[2],
                                             transform=ccrs.PlateCarree(),
                                             cmap=cmap_list_tas,
                                             cbar_ax=cbax_1,
                                             levels=levels_tas,
                                             center=0,
                                             add_labels=False)
        
        ssp370_ssp126Lu_tas[mod][1].plot(ax=row_axes[3],
                                             transform=ccrs.PlateCarree(),
                                             cmap=cmap_list_tas,
                                             cbar_ax=cbax_1,
                                             levels=levels_tas,
                                             center=0,
                                             add_labels=False)
            
        for ax,column in zip(row_axes,['ssp126_tas', 'ssp370_tas', 'ssp126_ssp370Lu_tas', 'ssp370_ssp126Lu_tas']):
            
            ax.set_extent(extent,
                        crs=ccrs.PlateCarree())
            ax.set_title(letters[i],
                        loc='left',
                        fontsize = size_titles,
                        fontweight='bold')
            ax.coastlines(linewidth=cstlin_lw)
            
            if column == 'ssp126_tas':
                
                    if mod == 'CanESM5':
                        height = 0.3
                    else:
                        height= 0.15
                    
                    if mod == 'multimodel_average':
                        title = 'Multimodel\nAverage'
                    else:
                        title = mod
                    
                    
                    ax.text(-0.1,
                            height,
                            title,
                            fontsize=size_titles,
                            fontweight='bold',
                            rotation='vertical',
                            transform=ax.transAxes)
            
            if i < 4:
                
                ax.set_title(column,
                            loc='center',
                            fontsize = size_titles,
                            fontweight='bold')
                
            i += 1

        # taschange colorbar
        cb_1 = mpl.colorbar.ColorbarBase(ax=cbax_1, 
                                        cmap=cmap_list_tas,
                                        norm=norm_tas,
                                        spacing='uniform',
                                        orientation='horizontal',
                                        extend='both',
                                        ticks=tick_locs_tas,
                                        drawedges=False)
        cb_1.set_label( 'TAS [°C]',
                        size=size_titles)
        cb_1.ax.xaxis.set_label_position('top')
        cb_1.ax.tick_params(labelcolor=col_cbticlbl,
                            labelsize=size_cbarnumbers,
                            color=col_cbtic,
                            length=cb_ticlen,
                            width=cb_ticwid,
                            direction='out'); 
        cb_1.ax.set_xticklabels(tick_labels_tas,
                                rotation=45)
        cb_1.outline.set_edgecolor(col_cbedg)
        cb_1.outline.set_linewidth(cb_edgthic)


       

        f.savefig(mapDIR+mapname,bbox_inches='tight')