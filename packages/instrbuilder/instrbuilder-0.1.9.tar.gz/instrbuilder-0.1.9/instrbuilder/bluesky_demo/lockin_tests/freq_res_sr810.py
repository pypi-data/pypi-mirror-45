# Lucas J. Koerner
# 05/2018
# koerner.lucas@stthomas.edu
# University of St. Thomas

# standard library imports
import sys
import os
import time

# imports that may need installation
import numpy as np
from bluesky import RunEngine
from bluesky.callbacks import LiveTable, LivePlot
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.plans import scan, grid_scan
from databroker import Broker

try:
    from ophyd.device import Kind
    from ophyd.ee_instruments import generate_ophyd_obj
except ModuleNotFoundError:
    print('Ophyd fork is not installed')
    print('First, (if needed) uninstall base ophyd:')
    print('  $ python -m pip uninstall ophyd')
    print('Next, install the fork:')
    print('  $ python -m pip install git+https://github.com/lucask07/ophyd@master#egg=ophyd')

from instrbuilder.instrument_opening import open_by_name

RE = RunEngine({})
bec = BestEffortCallback()
# Send all metadata/data captured to the BestEffortCallback.
# RE.subscribe(bec) # in this demo we will explicitly define LiveTables and Plots

db = Broker.named('local_file')  # a broker poses queries for saved data sets

# Insert all metadata/data captured into db.
RE.subscribe(db.insert)

# ------------------------------------------------
#           Lock-In Amplifier
# ------------------------------------------------
print('Warning ... The address to the serial adapter \n (E.g. /dev/tty.USA19H141113P1.1) can change ')
scpi_lia = open_by_name(name='srs_lockin')   # name within the configuration file (config.yaml)
LIA, component_dict = generate_ophyd_obj(name='LockIn', scpi_obj=scpi_lia)
lia = LIA(name='lockin')

# setup lock-in
# similar to a stage, but specific to this experiment
test_frequency = 5e6/512/8
lia.reset.set(None)
lia.fmode.set('Int')
lia.in_gnd.set('float')
lia.in_config.set('A')
lia.in_couple.set('DC')
lia.freq.set(test_frequency)
lia.sensitivity.set(1.0)  # 1 V RMS full-scale
tau = 0.03
lia.tau.set(tau)
# maximum settle to 99% accuracy is 9*tau for a filter-slope of 24-db/oct
max_settle = 9*tau*4
lia.filt_slope.set('6-db/oct')
lia.res_mode.set('normal')

# setup control of the lock-in filter-slope sweep (for LiveTable)
lia.filt_slope.delay = max_settle*2
lia.filt_slope.kind = Kind.hinted
lia.filt_slope.dtype = 'string'
lia.filt_slope.precision = 9  # so the string is not cutoff in the LiveTable
lia.ch1_disp.set('R')  # magnitude, i.e. sqrt(I^2 + Q^2)
# ------------------------------------------------
#           Function Generator
# ------------------------------------------------
fg_scpi = open_by_name(name='old_fg')   # name within the configuration file (config.yaml)
fg_scpi.name = 'fg'
FG, component_dict = generate_ophyd_obj(name='fg', scpi_obj=fg_scpi)
fg = FG(name='fg')

if fg.unconnected:
    sys.exit('Function Generator is not connected, exiting blueksy demo')
RE.md['fg'] = fg.id.get()

# setup control of the frequency sweep
fg.freq.delay = max_settle

# configure the function generator
fg.reset.set(None)  # start fresh
fg.function.set('SIN')
fg.load.set('INF')
fg.freq.set(test_frequency)
fg.v.set(2)  # full-scale range with 1 V RMS sensitivity is 2.8284
fg.offset.set(0)
fg.output.set('ON')

# ------------------------------------------------
#           Setup Supplemental Data
# ------------------------------------------------
from bluesky.preprocessors import SupplementalData
baseline_detectors = []
for dev in [fg, lia]:
    for name in dev.component_names:
        if getattr(dev, name).kind == Kind.config:
            baseline_detectors.append(getattr(dev, name))

sd = SupplementalData(baseline=baseline_detectors, monitors=[], flyers=[])
RE.preprocessors.append(sd)

# ------------------------------------------------
#                   Run a 2D sweep
# ------------------------------------------------
fc = 1/(2*np.pi*tau)
f1 = test_frequency - (fc * 2**3.5)  # 3.5 octaves below and above the cutoff
f2 = test_frequency + (fc * 2**3.5)
fg.freq.set(f1)
lia.filt_slope.set(0)
time.sleep(tau*12)
# grid_scan is a pre-configured Bluesky plan

lia.disp_val.name = 'amp'  # change name for Bluesky LiveTable

uid = RE(grid_scan([lia.disp_val],
         lia.filt_slope, 0, 3, 4,
         fg.freq, f1, f2, 60, False),
         LiveTable(['lockin_disp_val', 'fgen_freq', 'lockin_filt_slope']),
         # input parameters below are added to metadata
         attenuator='0dB',
         purpose='freq_resolution_SR810',
         operator='Lucas',
         dut='SR810',
         preamp='none',
         notes='test new ophyd object generation',
         fg_config=fg.read_configuration(),
         lia_config=lia.read_configuration())

# ------------------------------------------------
#   	(briefly) Investigate the captured data
# ------------------------------------------------

# get data into a pandas data-frame
header = db[uid[0]]  # db is a DataBroker instance
print(header.table())
df = header.table()
# view the baseline data (i.e. configuration values)
h = db[-1]
df_meta = h.table('baseline')

print('These configuration values are saved to baseline data:')
print(df_meta.columns.values)
