''' Visualization and post processing
'''
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import numpy as np
import pandas as pd
import os
import glob
from scipy.stats.mstats import mquantiles
import pickle

from . import utils
from . import load_gridded_data


def load_gmt_from_jobs(exp_dir, qs=[0.05, 0.5, 0.95], var='gmt_ensemble'):
    # load data
    if not os.path.exists(exp_dir):
        raise ValueError('ERROR: Specified path of the results directory does not exist!!!')

    paths = sorted(glob.glob(os.path.join(exp_dir, 'job_r*')))
    with open(paths[0], 'rb') as f:
        job_cfg, job_da = pickle.load(f)

    gmt_tmp = job_da.gmt_ens_save
    nt = np.shape(gmt_tmp)[0]
    nEN = np.shape(gmt_tmp)[-1]
    nMC = len(paths)

    gmt = np.ndarray((nt, nEN*nMC))
    for i, path in enumerate(paths):
        with open(path, 'rb') as f:
            job_cfg, job_da = pickle.load(f)

        job_gmt = {
            'gmt_ensemble': job_da.gmt_ens_save,
            'nhmt_ensemble': job_da.nhmt_ens_save,
            'shmt_ensemble': job_da.shmt_ens_save,
        }
        gmt[:, nEN*i:nEN+nEN*i] = job_gmt[var]

    gmt_qs = mquantiles(gmt, qs, axis=-1)
    return gmt_qs


def plot_gmt_vs_inst(gmt_qs, ana_pathdict,
                     verif_yrs=np.arange(1880, 2001), ref_period=[1951, 1980],
                     var='gmt_ensemble', lmr_label='LMR'):
    if np.shape(gmt_qs)[-1] == 1:
        nt = np.size(gmt_qs)
        gmt_qs_new = np.ndarray((nt, 3))
        for i in range(3):
            gmt_qs_new[:, i] = gmt_qs

        gmt_qs = gmt_qs_new

    syear, eyear = verif_yrs[0], verif_yrs[-1]
    lmr_gmt = gmt_qs[syear:eyear+1, :] - np.mean(gmt_qs[syear:eyear+1, :])

    load_func = {
        'GISTEMP': load_gridded_data.read_gridded_data_GISTEMP,
        'HadCRUT': load_gridded_data.read_gridded_data_HadCRUT,
        'BerkeleyEarth': load_gridded_data.read_gridded_data_BerkeleyEarth,
        'MLOST': load_gridded_data.read_gridded_data_MLOST,
        'ERA20-20C': load_gridded_data.read_gridded_data_CMIP5_model,
        '20CR-V2': load_gridded_data.read_gridded_data_CMIP5_model,
    }

    calib_vars = {
        'GISTEMP': ['Tsfc'],
        'HadCRUT': ['Tsfc'],
        'BerkeleyEarth': ['Tsfc'],
        'MLOST': ['air'],
        'ERA20-20C': {'tas_sfc_Amon': 'anom'},
        '20CR-V2': {'tas_sfc_Amon': 'anom'},
    }

    inst_gmt = {}
    inst_time = {}
    for name, path in ana_pathdict.items():
        print(f'Loading {name}: {path} ...')
        if name in ['ERA20-20C', '20CR-V2']:
            dd = load_func[name](
                os.path.dirname(path),
                os.path.basename(path),
                calib_vars[name],
                outtimeavg=list(range(1, 13)),
                anom_ref=ref_period,
            )
            time_grid = dd['tas_sfc_Amon']['years']
            lat_grid = dd['tas_sfc_Amon']['lat'][:, 0]
            anomaly_grid = dd['tas_sfc_Amon']['value']
        else:
            time_grid, lat_grid, lon_grid, anomaly_grid = load_func[name](
                os.path.dirname(path),
                os.path.basename(path),
                calib_vars[name],
                outfreq='annual',
                ref_period=ref_period,
            )

        gmt, _, _ = utils.global_hemispheric_means(anomaly_grid, lat_grid)
        year = np.array([d.year for d in time_grid])
        mask = (year >= syear) & (year <= eyear)
        inst_gmt[name] = gmt[mask] - np.nanmean(gmt[mask])
        inst_time[name] = year[mask]

    consensus_yrs = np.copy(verif_yrs)
    for name in ana_pathdict.keys():
        overlap_yrs = np.intersect1d(consensus_yrs, inst_time[name])
        ind_inst = np.searchsorted(inst_time[name], overlap_yrs)
        consensus_yrs = inst_time[name][ind_inst]

    consensus_gmt = np.zeros(np.size(consensus_yrs))
    for name in ana_pathdict.keys():
        overlap_yrs = np.intersect1d(consensus_yrs, inst_time[name])
        ind_inst = np.searchsorted(inst_time[name], overlap_yrs)
        consensus_gmt += inst_gmt[name][ind_inst]/len(ana_pathdict.keys())

    inst_gmt['consensus'] = consensus_gmt
    inst_time['consensus'] = consensus_yrs

    # stats
    corr_vs_lmr = {}
    ce_vs_lmr = {}
    for name in inst_gmt.keys():
        print(f'Calculating corr and CE against LMR for {name}')
        overlap_yrs = np.intersect1d(verif_yrs, inst_time[name])
        ind_lmr = np.searchsorted(verif_yrs, overlap_yrs)
        ind_inst = np.searchsorted(inst_time[name], overlap_yrs)
        ts_inst = inst_gmt[name][ind_inst]

        ts_lmr = lmr_gmt[ind_lmr, 1]
        corr_vs_lmr[name] = np.corrcoef(ts_inst, ts_lmr)[1, 0]
        ce_vs_lmr[name] = utils.coefficient_efficiency(ts_inst, ts_lmr)

    sns.set(style="darkgrid", font_scale=2)
    fig, ax = plt.subplots(figsize=[16, 10])

    ax.plot(verif_yrs, lmr_gmt[:, 1], '-', lw=3, color=sns.xkcd_rgb['black'], alpha=1, label=lmr_label)
    ax.fill_between(verif_yrs, lmr_gmt[:, 0], lmr_gmt[:, -1], color=sns.xkcd_rgb['black'], alpha=0.1)
    for name in inst_gmt.keys():
        ax.plot(inst_time[name], inst_gmt[name], '-', alpha=1,
                label=f'{name} (corr={corr_vs_lmr[name]:.2f}; CE={ce_vs_lmr[name]:.2f})')

    ax.set_xlim([syear, eyear])
    ax.set_ylim([-0.6, 0.8])
    ax.set_ylabel('Temperature anomaly (K)')
    ax.set_xlabel('Year (AD)')
    ax.set_title('Global mean temperature')
    ax.legend(frameon=False)

    return fig, corr_vs_lmr, ce_vs_lmr


def plot_corr_ce(corr_dict, ce_dict, lw=3, ms=10,
                 colors=[
                     sns.xkcd_rgb['denim blue'],
                     sns.xkcd_rgb['pale red'],
                     sns.xkcd_rgb['medium green'],
                     sns.xkcd_rgb['amber'],
                     sns.xkcd_rgb['purpleish'],
                 ], ncol=1):
    exp_names = list(corr_dict.keys())
    inst_names = list(corr_dict[exp_names[0]].keys())

    sns.set(style="darkgrid", font_scale=2)
    fig, ax = plt.subplots(figsize=[16, 10])

    inst_corr = {}
    inst_ce = {}
    for exp_name in exp_names:
        inst_corr[exp_name] = []
        inst_ce[exp_name] = []

    inst_cat = []
    for inst_name in inst_names:
        inst_cat.append(inst_name)
        for exp_name in exp_names:
            inst_corr[exp_name].append(corr_dict[exp_name][inst_name])
            inst_ce[exp_name].append(ce_dict[exp_name][inst_name])

    for i, exp_name in enumerate(exp_names):
        ax.plot(inst_cat, inst_corr[exp_name], '-o', lw=lw, ms=ms, color=colors[i % len(colors)],
                alpha=1, label=f'corr ({exp_name})')
        ax.plot(inst_cat, inst_ce[exp_name], '-*', lw=lw, ms=ms, color=colors[i % len(colors)],
                alpha=1, label=f'CE ({exp_name})')

    ax.set_title('corr and CE against LMR')
    ax.set_ylabel('coefficient')
    ax.legend(frameon=False, ncol=ncol)

    return fig


def plot_gmt_ts(exp_dir, savefig_path=None, plot_vars=['gmt_ensemble', 'nhmt_ensemble', 'shmt_ensemble'],
                qs=[0.025, 0.25, 0.5, 0.75, 0.975], pannel_size=[10, 4], font_scale=1.5, hspace=0.5, ylim=[-1, 1],
                plot_prior=False, prior_var_name='tas_sfc_Amon'):
    ''' Plot timeseries

    Args:
        exp_dir (str): the path of the results directory that contains subdirs r0, r1, ...

    Returns:
        fig (figure): the output figure
    '''
    # load data
    if not os.path.exists(exp_dir):
        raise ValueError('ERROR: Specified path of the results directory does not exist!!!')

    paths = sorted(glob.glob(os.path.join(exp_dir, 'r*')))
    filename = 'gmt_ensemble.npz'
    data = np.load(os.path.join(paths[0], filename))
    gmt_tmp = data['gmt_ensemble']
    nt = np.shape(gmt_tmp)[0]
    nEN = np.shape(gmt_tmp)[-1]
    nMC = len(paths)

    nvar = len(plot_vars)
    sns.set(style="darkgrid", font_scale=font_scale)
    fig = plt.figure(figsize=[pannel_size[0], pannel_size[1]*nvar])

    ax_title = {
            'gmt_ensemble': 'Global mean temperature',
            'shmt_ensemble': 'SH mean temperature',
            'nhmt_ensemble': 'NH mean temperature',
            }

    for plot_i, var in enumerate(plot_vars):
        gmt = np.ndarray((nt, nEN*nMC))
        for i, path in enumerate(paths):
            data = np.load(os.path.join(path, filename))
            gmt[:, nEN*i:nEN+nEN*i] = data[var]

        gmt_qs = mquantiles(gmt, qs, axis=-1)

        # plot
        gs = gridspec.GridSpec(nvar, 1)
        gs.update(wspace=0, hspace=hspace)

        to = np.arange(nt)
        ax = plt.subplot(gs[plot_i, 0])
        if qs[2] == 0.5:
            label='median'
        else:
            label='{}%'.format(qs[2]*100)

        ax.plot(to, gmt_qs[:,2], '-', color=sns.xkcd_rgb['pale red'], alpha=1, label='{}'.format(label))
        ax.fill_between(to, gmt_qs[:,-2], gmt_qs[:,1], color=sns.xkcd_rgb['pale red'], alpha=0.5,
                label='{}% to {}%'.format(qs[1]*100, qs[-2]*100))
        ax.fill_between(to, gmt_qs[:,-1], gmt_qs[:,0], color=sns.xkcd_rgb['pale red'], alpha=0.1,
                label='{}% to {}%'.format(qs[0]*100, qs[-1]*100))
        ax.set_title(ax_title[var])
        ax.set_ylabel('T anom. (K)')
        ax.set_xlabel('Year (AD)')
        ax.legend(loc='upper center', ncol=3, frameon=False)
        ax.set_ylim(ylim)

        if plot_prior:
            prior_gmt = np.zeros([nMC,nEN,nt])
            prior_nhmt = np.zeros([nMC,nEN,nt])
            prior_shmt = np.zeros([nMC,nEN,nt])
            for citer, path in enumerate(paths):
                data = np.load(os.path.join(path, 'Xb_one.npz'))
                Xb_one = data['Xb_one']
                Xb_one_coords = data['Xb_one_coords']
                state_info = data['state_info'].item()
                posbeg = state_info[prior_var_name]['pos'][0]
                posend = state_info[prior_var_name]['pos'][1]
                tas_prior = Xb_one[posbeg:posend+1, :]
                tas_coords = Xb_one_coords[posbeg:posend+1, :]
                nlat, nlon = state_info[prior_var_name]['spacedims']
                lat_lalo = tas_coords[:, 0].reshape(nlat, nlon)
                nstate, nens = tas_prior.shape
                tas_lalo = tas_prior.transpose().reshape(nens, nlat, nlon)
                [gmt,nhmt,shmt] = utils.global_hemispheric_means(tas_lalo, lat_lalo[:, 0])

                prior_gmt[citer,:,:]  = np.repeat(gmt[:,np.newaxis],nt,1)
                prior_nhmt[citer,:,:] = np.repeat(nhmt[:,np.newaxis],nt,1)
                prior_shmt[citer,:,:] = np.repeat(shmt[:,np.newaxis],nt,1)

            if var == 'gmt_ensemble':
                gmtp = prior_gmt.transpose(2,0,1).reshape(nt,-1)
            elif var == 'nhmt_ensemble':
                gmtp = prior_nhmt.transpose(2,0,1).reshape(nt,-1)
            elif var == 'shmt_ensemble':
                gmtp = prior_shmt.transpose(2,0,1).reshape(nt,-1)

            gmtp_qs = mquantiles(gmtp, qs, axis=-1)

            ax.plot(to, gmtp_qs[:,2], '-', color=sns.xkcd_rgb['grey'], alpha=1)
            ax.fill_between(to, gmtp_qs[:,3], gmtp_qs[:,1], color=sns.xkcd_rgb['grey'], alpha=0.5)
            ax.fill_between(to, gmtp_qs[:,-1], gmtp_qs[:,0], color=sns.xkcd_rgb['grey'], alpha=0.1)

    if savefig_path:
        plt.savefig(savefig_path, bbox_inches='tight')
        plt.close(fig)

    return fig


def plot_gmt_ts_from_jobs(exp_dir, savefig_path=None, plot_vars=['gmt_ensemble', 'nhmt_ensemble', 'shmt_ensemble'],
                          qs=[0.025, 0.25, 0.5, 0.75, 0.975], pannel_size=[10, 4],
                          font_scale=1.5, hspace=0.5, ylim=[-1, 1],
                          plot_prior=False, prior_var_name='tas_sfc_Amon'):
    ''' Plot timeseries

    Args:
        exp_dir (str): the path of the results directory that contains subdirs r0, r1, ...

    Returns:
        fig (figure): the output figure
    '''
    # load data
    if not os.path.exists(exp_dir):
        raise ValueError('ERROR: Specified path of the results directory does not exist!!!')

    paths = sorted(glob.glob(os.path.join(exp_dir, 'job_r*')))
    with open(paths[0], 'rb') as f:
        job_cfg, job_da = pickle.load(f)

    gmt_tmp = job_da.gmt_ens_save
    nt = np.shape(gmt_tmp)[0]
    nEN = np.shape(gmt_tmp)[-1]
    nMC = len(paths)

    nvar = len(plot_vars)
    sns.set(style="darkgrid", font_scale=font_scale)
    fig = plt.figure(figsize=[pannel_size[0], pannel_size[1]*nvar])

    ax_title = {
        'gmt_ensemble': 'Global mean temperature',
        'shmt_ensemble': 'SH mean temperature',
        'nhmt_ensemble': 'NH mean temperature',
    }

    for plot_i, var in enumerate(plot_vars):
        gmt = np.ndarray((nt, nEN*nMC))
        for i, path in enumerate(paths):
            with open(path, 'rb') as f:
                job_cfg, job_da = pickle.load(f)

            job_gmt = {
                'gmt_ensemble': job_da.gmt_ens_save,
                'nhmt_ensemble': job_da.nhmt_ens_save,
                'shmt_ensemble': job_da.shmt_ens_save,
            }

            gmt[:, nEN*i:nEN+nEN*i] = job_gmt[var]

        gmt_qs = mquantiles(gmt, qs, axis=-1)

        # plot
        gs = gridspec.GridSpec(nvar, 1)
        gs.update(wspace=0, hspace=hspace)

        to = np.arange(nt)
        ax = plt.subplot(gs[plot_i, 0])
        if qs[2] == 0.5:
            label='median'
        else:
            label='{}%'.format(qs[2]*100)

        ax.plot(to, gmt_qs[:,2], '-', color=sns.xkcd_rgb['pale red'], alpha=1, label='{}'.format(label))
        ax.fill_between(to, gmt_qs[:,-2], gmt_qs[:,1], color=sns.xkcd_rgb['pale red'], alpha=0.5,
                label='{}% to {}%'.format(qs[1]*100, qs[-2]*100))
        ax.fill_between(to, gmt_qs[:,-1], gmt_qs[:,0], color=sns.xkcd_rgb['pale red'], alpha=0.1,
                label='{}% to {}%'.format(qs[0]*100, qs[-1]*100))
        ax.set_title(ax_title[var])
        ax.set_ylabel('T anom. (K)')
        ax.set_xlabel('Year (AD)')
        ax.legend(loc='upper center', ncol=3, frameon=False)
        ax.set_ylim(ylim)

    if savefig_path:
        plt.savefig(savefig_path, bbox_inches='tight')
        plt.close(fig)

    return fig


def plot_vslite_params(lat_obs, lon_obs, T1, T2, M1, M2,
                       T1_ticks=None, T2_ticks=None, M1_ticks=None, M2_ticks=None, save_path=None):
    sns.set(style='ticks', font_scale=2)
    fig = plt.figure(figsize=[18, 12])
    gs = mpl.gridspec.GridSpec(2, 2)
    gs.update(wspace=0.1, hspace=0.1)

    map_proj = ccrs.Robinson()
    # map_proj = ccrs.PlateCarree()
    # map_proj = ccrs.Mercator()
    # map_proj = ccrs.Miller()
    # map_proj = ccrs.Mollweide()
    # map_proj = ccrs.EqualEarth()

    pad = 0.05
    fraction = 0.05

    # T1
    ax1 = plt.subplot(gs[0, 0], projection=map_proj)
    ax1.set_title('T1')
    ax1.set_global()
    ax1.add_feature(cfeature.LAND, facecolor='gray', alpha=0.3)
    ax1.gridlines(edgecolor='gray', linestyle=':')
    z = T1
    norm = mpl.colors.Normalize(vmin=np.min(z), vmax=np.max(z))
    im = ax1.scatter(
        lon_obs, lat_obs, marker='o', norm=norm,
        c=z, cmap='Reds', s=20, transform=ccrs.Geodetic()
    )
    cbar1 = fig.colorbar(im, ax=ax1, orientation='horizontal', pad=pad, fraction=fraction)
    if T1_ticks:
        cbar1.set_ticks(T1_ticks)

    # T2
    ax2 = plt.subplot(gs[0, 1], projection=map_proj)
    ax2.set_title('T2')
    ax2.set_global()
    ax2.add_feature(cfeature.LAND, facecolor='gray', alpha=0.3)
    ax2.gridlines(edgecolor='gray', linestyle=':')
    z = T2
    norm = mpl.colors.Normalize(vmin=np.min(z), vmax=np.max(z))
    im = ax2.scatter(
        lon_obs, lat_obs, marker='o', norm=norm,
        c=z, cmap='Reds', s=20, transform=ccrs.Geodetic()
    )
    cbar2 = fig.colorbar(im, ax=ax2, orientation='horizontal', pad=pad, fraction=fraction)
    if T2_ticks:
        cbar2.set_ticks(T2_ticks)

    # M1
    ax3 = plt.subplot(gs[1, 0], projection=map_proj)
    ax3.set_title('M1')
    ax3.set_global()
    ax3.add_feature(cfeature.LAND, facecolor='gray', alpha=0.3)
    ax3.gridlines(edgecolor='gray', linestyle=':')
    z = M1
    norm = mpl.colors.Normalize(vmin=np.min(z), vmax=np.max(z))
    im = ax3.scatter(
        lon_obs, lat_obs, marker='o', norm=norm,
        c=z, cmap='Blues', s=20, transform=ccrs.Geodetic()
    )
    cbar3 = fig.colorbar(im, ax=ax3, orientation='horizontal', pad=pad, fraction=fraction)
    if M1_ticks:
        cbar3.set_ticks(M1_ticks)

    # M2
    ax4 = plt.subplot(gs[1, 1], projection=map_proj)
    ax4.set_title('M2')
    ax4.set_global()
    ax4.add_feature(cfeature.LAND, facecolor='gray', alpha=0.3)
    ax4.gridlines(edgecolor='gray', linestyle=':')
    z = M2
    norm = mpl.colors.Normalize(vmin=np.min(z), vmax=np.max(z))
    im = ax4.scatter(
        lon_obs, lat_obs, marker='o', norm=norm,
        c=z, cmap='Blues', s=20, transform=ccrs.Geodetic()
    )
    cbar4 = fig.colorbar(im, ax=ax4, orientation='horizontal', pad=pad, fraction=fraction)
    if M2_ticks:
        cbar4.set_ticks(M2_ticks)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    return fig
