# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |


"""

###############################################################################
# imports
###############################################################################

# Outputlib
from oemof import outputlib

# Default logger of oemof
from oemof.tools import logger
from oemof.tools import helpers
from examples.solph.HSNR_Energiesysteme import values
#from oemof.tools import values

# import oemof base classes to create energy system objects
import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
import oemof.solph as solph

def optimise_storage_size(filename="HSNR.csv", solvername='cbc',
                          debug=True, number_timesteps=8760, tee_switch=True):
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=number_timesteps,
                                    freq='H')

    energysystem = solph.EnergySystem(timeindex=date_time_index)

    # Read data file
    full_filename = os.path.join(os.path.dirname(__file__), filename)
    data = pd.read_csv(full_filename, sep=",")

    ##########################################################################
    # Create oemof object
    ##########################################################################
    #Die Variablen mit values.xyz wurden in values.py ausgelagert
    logging.info('Create oemof objects')

    # create thermal and electricity bus
    bel = solph.Bus(label="electricity")
    #bth = solph.Bus(label="thermal")       

    # create gas bus
    bgas = solph.Bus(label="natural_gas")

    
    # create excess component for the electricity bus to allow overproduction
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})

    ##################################################################
    ###################     Sink Objects     #####################
    ##################################################################
    
    # create simple sink object for demand
    solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1.0)})

    ##################################################################
    ###################     Baseload Objects     #####################
    ##################################################################
    
    # create baseload object for lignite resource
    solph.Source(label='lig', outputs={bel: solph.Flow(
        actual_value=data['lig'], nominal_value=values.lignite, fixed=True,
        fixed_costs=20)})

    # create baseload object for nuclear energy
    solph.Source(label='nuc', outputs={bel: solph.Flow(
       actual_value=data['nuc'], nominal_value=values.nuc, fixed=True,
       fixed_costs=15)})

    # create commodity object for coal resource
    solph.Source(label='coal', outputs={bel: solph.Flow(
        actual_value=data['coal'], nominal_value=values.coal, fixed=True,
        fixed_costs=20)})

    # create fixed source object for wind
    solph.Source(label='wind', outputs={bel: solph.Flow(
       actual_value=data['wind'], nominal_value=values.wind, fixed=True,
       fixed_costs=20)})  

    # create fixed source object for water
    solph.Source(label='water', outputs={bel: solph.Flow(
       actual_value=data['water'], nominal_value=values.water, fixed=True,
       fixed_costs=20)})

    # create fixed source object for biomass
    solph.Source(label='biomass', outputs={bel: solph.Flow(
       actual_value=data['biomass'], nominal_value=values.biomass, fixed=True,
       fixed_costs=20)})
    
    # create fixed source object for pv
    solph.Source(label='pv', outputs={bel: solph.Flow(
        actual_value=data['pv'], nominal_value=values.pv, fixed=True,
        fixed_costs=15)})


    ##################################################################
    ##########     Operating Reserve Objects (Regellast)    ##########
    ##################################################################

    # create commodity object for gas resource (summed_max für Begrenzung der Gasresource[kWh])
    solph.Source(label='rgas', outputs={bgas: solph.Flow(
        nominal_value=194397000 * number_timesteps / 8760, summed_max=1000)})

    ##################################################################
    ###############     Transforming Objects     #####################
    ##################################################################

    # create simple transformer object for gas powerplant
    solph.LinearTransformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58})

    # Calculate ep_costs from capex to compare with old solph
    capex = 1000
    lifetime = 20
    wacc = 0.05
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)

    # create storage transformer object for storage
    # zu hohe variable Kosten des Speichers bewirken eine Favorisierung hin zu fossilen Brennstoffen) 
    solph.Storage(
       label='storage',
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        fixed_costs=35,
        investment=solph.Investment(ep_costs=epc),
    )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = solph.OperationalModel(energysystem)

    if debug:
        filename = os.path.join(
            helpers.extend_basic_path('lp_files'), 'HSNR.lp')
        logging.info('Store lp-file in {0}.'.format(filename))
        om.write(filename, io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=solvername, solve_kwargs={'tee': tee_switch})

    return energysystem


def get_result_dict(energysystem):
    logging.info('Check the results')
    storage = energysystem.groups['storage']
    myresults = outputlib.DataFramePlot(energy_system=energysystem)

    dafr='2012-01-01 00:00:00'
    dato='2012-12-31 23:00:00'

    pp_gas = myresults.slice_by(obj_label='pp_gas', type='to_bus',
                                date_from=dafr,
                                date_to=dato)
    
    lig = myresults.slice_by(obj_label='lig', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    coal = myresults.slice_by(obj_label='coal', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    water = myresults.slice_by(obj_label='water', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    biomass = myresults.slice_by(obj_label='biomass', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    nuc = myresults.slice_by(obj_label='nuc', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    demand = myresults.slice_by(obj_label='demand',type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    wind = myresults.slice_by(obj_label='wind',
                                date_from=dafr,
                                date_to=dato)

    pv = myresults.slice_by(obj_label='pv',
                                date_from=dafr,
                                date_to=dato)



    return {'pp_gas_sum': pp_gas.sum(),
            'pp_gas_inst':pp_gas.max()/1,
            'lig_sum': lig.sum(),
            'lig_inst': lig.max()/1.0,
            'coal_sum': coal.sum(),
            'coal_inst': coal.max()/1.0,
            'water_sum': water.sum(),
            'water_inst': water.max()/1.0,
            'biomass_sum': biomass.sum(),
            'biomass_inst': biomass.max()/1.0,
            'nuc_sum': nuc.sum(),
            'nuc_inst': nuc.max()/1.0,
            'demand_sum': demand.sum(),
            'demand_max': demand.max(),
            'wind_sum': wind.sum(),
            'wind_inst': wind.max()/1.0,
            'pv_sum': pv.sum(),
            'pv_inst': pv.max()/0.76474,
            'storage_cap': energysystem.results[storage][storage].invest,
            'objective': energysystem.results.objective
            }


def create_plots(energysystem):

    logging.info('Plot the results')

    cdict = {'wind': '#5b5bae',
             'pv': '#ffde32',
             'storage': '#42c77a',
             'pp_gas': '#636f6b',
             'lig': '#8B4513',
             'coal': '#000000',
             'water': '#4169E1',
             'biomass': '#32CD32',
             'demand': '#ce4aff',
             'excess_bel': '#555555',
             'nuc': '#ff0000'
             }

    # Plotting the input flows of the electricity bus for January
    myplot = outputlib.DataFramePlot(energy_system=energysystem)
    myplot.slice_unstacked(bus_label="electricity", type="to_bus",
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-01-31 00:00:00")
    colorlist = myplot.color_from_dict(cdict)
    myplot.plot(color=colorlist, linewidth=2, title="January 2012")
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks(date_format='%d-%m-%Y', tick_distance=24*7)

    # Plotting the output flows of the electricity bus for year 2012
    myplot.slice_unstacked(bus_label="electricity", type="from_bus")
    myplot.plot(title="Year 2012", colormap='Spectral', linewidth=2)
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks()

    plt.show()

    # Plotting a combined stacked plot
    fig = plt.figure(figsize=(24, 14))
    plt.rc('legend', **{'fontsize': 19})
    plt.rcParams.update({'font.size': 19})
    plt.style.use('grayscale')

    handles, labels = myplot.io_plot(
        bus_label='electricity', cdict=cdict,
        barorder=['lig','nuc', 'coal', 'water', 'biomass', 'pv', 'wind', 'storage','pp_gas' ],
        lineorder=['demand', 'storage', 'excess_bel'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(1, 1, 1),
        date_from=values.datefrom,
        date_to=values.dateto,
        )
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_title("Electricity bus")
    myplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    myplot.outside_legend(handles=handles, labels=labels)

    plt.show()


def run_HSNR():
    logger.define_logging()
    esys = optimise_storage_size()
     #esys.dump()
     #esys.restore()
    import pprint as pp
    pp.pprint(get_result_dict(esys))
    create_plots(esys)


if __name__ == "__main__":
    run_HSNR()
