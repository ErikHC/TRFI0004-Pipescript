# This CASA pipescript is meant for use with CASA 6.4.1 and pipeline 2022.2.0.64
##### 2022-09-09 (D) #####
# Produces the following:
# (1) Uplink image (spw 2~9)                           (2) Downlink image (10~33) 
# (3) Starlink downlink channels 1-3 (spw 18~21,30~33) (4) Starlink downlink channels 6-8 (spw 10~17)

context = h_init()
context.set_state('ProjectSummary', 'observatory', 'Karl G. Jansky Very Large Array')
context.set_state('ProjectSummary', 'telescope', 'EVLA')
try:
    hifv_importdata(vis=['TRFI0004.sb41206290.eb42581852.59831.75615726852'],
                    createmms='automatic', asis='Receiver CalAtmosphere', ocorr_mode='co',
                    nocopy=False, overwrite=False)
    # Hanning smoothing is turned off in the following step.
    # In the case of extreme RFI or very bright masers, Hanning smoothing may still be required.
    # hifv_hanning(pipelinemode="automatic")
    hifv_flagdata(fracspw=0.01,
                  intents='*POINTING*,*FOCUS*,*ATMOSPHERE*,*SIDEBAND_RATIO*, *UNKNOWN*, '
                          '*SYSTEM_CONFIGURATION*, *UNSPECIFIED#UNSPECIFIED*', hm_tbuff='1.5int')
    hifv_vlasetjy(pipelinemode="automatic")
    hifv_priorcals(pipelinemode="automatic")
    hifv_syspower(pipelinemode="automatic")
    hifv_testBPdcals(pipelinemode="automatic")
    hifv_checkflag(checkflagmode='bpd-vla')
    hifv_semiFinalBPdcals(pipelinemode="automatic")
    hifv_checkflag(checkflagmode='allcals-vla')
    hifv_solint(pipelinemode="automatic")
    hifv_fluxboot(pipelinemode="automatic")
    hifv_finalcals(pipelinemode="automatic")
    hifv_applycals(pipelinemode="automatic")
    # Keep the following three steps in the script if cont.dat exists.
    # Otherwise we recommend to comment out the next task.
    hifv_checkflag(checkflagmode='target-vla')
    hifv_statwt(pipelinemode="automatic")
    hifv_plotsummary(pipelinemode="automatic")
    hif_makeimlist(intent='PHASE,BANDPASS', specmode='cont')
    hif_makeimages(hm_masking='centralregion')
    # Science target imaging pipeline commands
    hif_mstransform(pipelinemode="automatic")
    # hif_checkproductsize(maximsize=16384)
    hif_makeimlist(specmode='cont')
    hif_makeimages(hm_cyclefactor=3.0)
    # hifv_pbcor(pipelinemode="automatic")
    # Make sure VIS is correct
    # vis: TRFI0004.sb41206290.eb42581852.59831.75615726852_targets.ms
    # hifv_exportdata(pipelinemode="automatic")

    ### UL/DL (All Channels) ###
    # Make sure VIS is correct
    #
    tclean(vis=['TRFI0004.sb41206290.eb42581852.59831.75615726852_targets.ms'],
    field='J1239+3057_wea', spw='2~9', # Uplink only
    uvrange='>2.3klambda',
    antenna=['0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26&'],
    scan=['7,9,14,16'], intent='OBSERVE_TARGET#UNSPECIFIED',
    datacolumn='data',
    imagename='Dconfig_weak_source_uplink',
    imsize=[720, 720], cell=['0.93arcsec'], phasecenter='ICRS 12:39:36.8672 +030.57.48.772',
    stokes='I', specmode='mfs', nchan=-1, outframe='LSRK',
    perchanweightdensity=False, gridder='standard', mosweight=False,
    usepointing=False, pblimit=-0.1, deconvolver='mtmfs', nterms=2,
    restoration=True, restoringbeam='common', pbcor=True, weighting='briggs',
    robust=0.5, npixels=0, niter=30000, threshold='3.42e-05Jy', nsigma=4.0,
    cyclefactor=3.0, interactive=0, usemask='auto-multithresh',
    sidelobethreshold=2.0, minbeamfrac=0.3, dogrowprune=True, restart=True,
    savemodel='none', calcres=True, calcpsf=True, parallel=False)

    tclean(vis=['TRFI0004.sb41206290.eb42581852.59831.75615726852_targets.ms'],
    field='J1239+3057_wea',
    spw='10~33', # Downlink only
    uvrange='>1.9klambda',
    antenna=['0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26&'],
    scan=['7,9,14,16'], intent='OBSERVE_TARGET#UNSPECIFIED',
    datacolumn='data',
    imagename='Dconfig_weak_source_downlink',
    imsize=[750, 750], cell=['1arcsec'], phasecenter='ICRS 12:39:36.8672 +030.57.48.772',
    stokes='I', specmode='mfs', nchan=-1, outframe='LSRK',
    perchanweightdensity=False, gridder='standard', mosweight=False,
    usepointing=False, pblimit=-0.1, deconvolver='mtmfs', nterms=2,
    restoration=True, restoringbeam='common', pbcor=True, weighting='briggs',
    robust=0.5, npixels=0, niter=50000, threshold='2.2e-05Jy', nsigma=4.0,
    cyclefactor=3.0, interactive=0, usemask='auto-multithresh',
    sidelobethreshold=2.0, minbeamfrac=0.3, dogrowprune=True, restart=True,
    savemodel='none', calcres=True, calcpsf=True, parallel=False)

    ### STARLINK DL CHANNELS ###
    #
    #
    tclean(vis=['TRFI0004.sb41206290.eb42581852.59831.75615726852_targets.ms'],
    field='J1239+3057_wea', spw='10~17', # Channels 5ish,6,7,8
    uvrange='>2.3klambda',
    antenna=['0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26&'],
    scan=['7,9,14,16'], intent='OBSERVE_TARGET#UNSPECIFIED',
    datacolumn='data',
    imagename='Dconfig_Starlink_DLchs678',
    imsize=[720, 720], cell=['0.93arcsec'], phasecenter='ICRS 12:39:36.8672 +030.57.48.772',
    stokes='I', specmode='mfs', nchan=-1, outframe='LSRK',
    perchanweightdensity=False, gridder='standard', mosweight=False,
    usepointing=False, pblimit=-0.1, deconvolver='mtmfs', nterms=2,
    restoration=True, restoringbeam='common', pbcor=True, weighting='briggs',
    robust=0.5, npixels=0, niter=30000, threshold='3.42e-05Jy', nsigma=4.0,
    cyclefactor=3.0, interactive=0, usemask='auto-multithresh',
    sidelobethreshold=2.0, minbeamfrac=0.3, dogrowprune=True, restart=True,
    savemodel='none', calcres=True, calcpsf=True, parallel=False)

    tclean(vis=['TRFI0004.sb41206290.eb42581852.59831.75615726852_targets.ms'],
    field='J1239+3057_wea',
    spw='18~21, 30~33', # Channels 1,2,3,4
    uvrange='>1.9klambda',
    antenna=['0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26&'],
    scan=['7,9,14,16'], intent='OBSERVE_TARGET#UNSPECIFIED',
    datacolumn='data',
    imagename='Dconfig_Starlink_DLchs12345',
    imsize=[750, 750], cell=['1arcsec'], phasecenter='ICRS 12:39:36.8672 +030.57.48.772',
    stokes='I', specmode='mfs', nchan=-1, outframe='LSRK',
    perchanweightdensity=False, gridder='standard', mosweight=False,
    usepointing=False, pblimit=-0.1, deconvolver='mtmfs', nterms=2,
    restoration=True, restoringbeam='common', pbcor=True, weighting='briggs',
    robust=0.5, npixels=0, niter=50000, threshold='2.2e-05Jy', nsigma=4.0,
    cyclefactor=3.0, interactive=0, usemask='auto-multithresh',
    sidelobethreshold=2.0, minbeamfrac=0.3, dogrowprune=True, restart=True,
    savemodel='none', calcres=True, calcpsf=True, parallel=False)
    
    # hifv_exportdata(pipelinemode="automatic")
finally:
    h_save()

