## -*- coding: utf-8 -*-

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


# import oemof base classes to create energy system objects
import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
import oemof.solph as solph
import values

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
    ########################## Create oemof object ###########################
    ##########################################################################
    #Die Variablen z.B. values.lignite wurden in der Datei values.py ausgelagert
    logging.info('Create oemof objects')

    # create thermal and electricity bus
    bel = solph.Bus(label="electricity")
    #bth = solph.Bus(label="thermal")       

    # create gas bus
    bgas = solph.Bus(label="natural_gas")

    
    # create excess component for the electricity bus to allow overproduction
    solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})

    ##################################################################
    #####################     Sink Objects     #######################
    ##################################################################
    
    # create simple sink object for electrical demand
    solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=0.25)})

    ##################################################################
    ###################     Baseload Objects     #####################
    ##################################################################
    
    
    # create fixed source object for biomass
    solph.Source(label='biomass', outputs={bel: solph.Flow(
       actual_value=data['biomass'], nominal_value=values.biomass, fixed=True,
       fixed_costs=20)})

    # create fixed source object for brown coal/ lignite
    solph.Source(label='brown_lig', outputs={bel: solph.Flow(
       actual_value=data['brown_lig'], nominal_value=values.brown_lig, fixed=True,
       fixed_costs=20)})


    # create fixed source object for fossil-coal derived gas
    solph.Source(label='coal_derived_gas', outputs={bel: solph.Flow(
       actual_value=data['coal_derived_gas'], nominal_value=values.coal_derived_gas, fixed=True,
       fixed_costs=20)})

    # create fixed source object for fossil gas
    solph.Source(label='fossil_gas', outputs={bel: solph.Flow(
       actual_value=data['fossil_gas'], nominal_value=values.fossil_gas, fixed=True,
       fixed_costs=20)})

    # create fixed source object for fossil hardcoal
    solph.Source(label='fossil_hardcoal', outputs={bel: solph.Flow(
       actual_value=data['fossil_hardcoal'], nominal_value=values.fossil_hardcoal, fixed=True,
       fixed_costs=20)})
        
    # create fixed source object for fossil oil
    solph.Source(label='fossil_oil', outputs={bel: solph.Flow(
       actual_value=data['fossil_oil'], nominal_value=values.fossil_oil, fixed=True,
       fixed_costs=20)})

    # create fixed source object for fossil oil shale
    #solph.Source(label='fossil_oil_shale', outputs={bel: solph.Flow(
    #   actual_value=data['fossil_oil_shale'], nominal_value=values.fossil_oil_shale, fixed=True,
    #   fixed_costs=20)})

    # create fixed source object for fossil peat
    #solph.Source(label='fossil_peat', outputs={bel: solph.Flow(
    #   actual_value=data['fossil_peat'], nominal_value=values.fossil_peat, fixed=True,
    #   fixed_costs=20)})    

    # create fixed source object for geothermal
    solph.Source(label='geothermal', outputs={bel: solph.Flow(
       actual_value=data['geothermal'], nominal_value=values.geothermal, fixed=True,
       fixed_costs=20)})

    # create fixed source object for hydro pumped storage
    solph.Source(label='hydro_pumped_storage', outputs={bel: solph.Flow(
       actual_value=data['hydro_pumped_storage'], nominal_value=values.hydro_pumped_storage, fixed=True,
       fixed_costs=20)})

    # create fixed source object for run-of-river
    solph.Source(label='run_of_river', outputs={bel: solph.Flow(
       actual_value=data['run_of_river'], nominal_value=values.run_of_river, fixed=True,
       fixed_costs=20)})
    
    # create baseload object for hydro-water-reservoir
    solph.Source(label='hydro_water_reservoir', outputs={bel: solph.Flow(
        actual_value=data['hydro_water_reservoir'], nominal_value=values.hydro_water_reservoir, fixed=True,
        fixed_costs=20)})

    # create baseload object for marine
    #solph.Source(label='marine', outputs={bel: solph.Flow(
    #    actual_value=data['marine'], nominal_value=values.marine, fixed=True,
    #    fixed_costs=20)})

    # create baseload object for nuclear energy
    solph.Source(label='nuclear', outputs={bel: solph.Flow(
       actual_value=data['nuclear'], nominal_value=values.nuclear, fixed=True,
       fixed_costs=20)})

    # create commodity object for other
    #solph.Source(label='other', outputs={bel: solph.Flow(
    #    actual_value=data['other'], nominal_value=values.other, fixed=True,
    #    fixed_costs=20)})

    # create commodity object for other renewable
    #solph.Source(label='other_renewable', outputs={bel: solph.Flow(
    #    actual_value=data['other_renewable'], nominal_value=values.other_renewable, fixed=True,
    #    fixed_costs=20)})

    # create fixed source object for solar
    solph.Source(label='solar', outputs={bel: solph.Flow(
       actual_value=data['solar'], nominal_value=values.solar, fixed=True,
       fixed_costs=20)})  

    # create fixed source object for waste
    solph.Source(label='waste', outputs={bel: solph.Flow(
       actual_value=data['waste'], nominal_value=values.waste, fixed=True,
       fixed_costs=20)})

    
    # create fixed source object for wind offshore
    solph.Source(label='wind_offshore', outputs={bel: solph.Flow(
        actual_value=data['wind_offshore'], nominal_value=values.wind_offshore, fixed=True,
        fixed_costs=20)})


    ##################################################################
    ##########     Operating Reserve Objects (Regellast)    ##########
    ##################################################################

    # create commodity object for gas resource (summed_max für Begrenzung der Gasresource[kWh])
    solph.Source(label='rgas', outputs={bgas: solph.Flow(
        nominal_value=194397000 * number_timesteps / 8760, summed_max=5.8)})

    ##################################################################
    ###############     Transforming Objects     #####################
    ##################################################################

    # create simple transformer object for gas powerplant
    solph.LinearTransformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=30)},
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
        inputs={bel: solph.Flow(variable_costs=10e2)},
        outputs={bel: solph.Flow(variable_costs=10e2)},
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

    biomass = myresults.slice_by(obj_label='biomass', type='to_bus',
                                date_from=dafr,
                                date_to=dato)
    
    brown_lig = myresults.slice_by(obj_label='brown_lig', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    coal_derived_gas = myresults.slice_by(obj_label='coal_derived_gas', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    fossil_gas = myresults.slice_by(obj_label='fossil_gas', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    fossil_hardcoal = myresults.slice_by(obj_label='fossil_hardcoal', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    fossil_oil = myresults.slice_by(obj_label='fossil_oil', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    #fossil_oil_shale = myresults.slice_by(obj_label='fossil_oil_shale', type='to_bus',
    #                            date_from=dafr,
    #                            date_to=dato)

    #fossil_peat = myresults.slice_by(obj_label='fossil_peat', type='to_bus',
    #                            date_from=dafr,
    #                            date_to=dato)    

    geothermal = myresults.slice_by(obj_label='geothermal', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    hydro_pumped_storage = myresults.slice_by(obj_label='hydro_pumped_storage', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    run_of_river = myresults.slice_by(obj_label='run_of_river', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    hydro_water_reservoir = myresults.slice_by(obj_label='hydro_water_reservoir', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    #marine = myresults.slice_by(obj_label='marine', type='to_bus',
    #                            date_from=dafr,
    #                            date_to=dato)
    
    nuclear = myresults.slice_by(obj_label='nuclear', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    #other = myresults.slice_by(obj_label='other', type='to_bus',
    #                            date_from=dafr,
    #                            date_to=dato)

    #other_renewable = myresults.slice_by(obj_label='other_renewable', type='to_bus',
    #                            date_from=dafr,
    #                            date_to=dato)

    solar = myresults.slice_by(obj_label='solar', type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    waste = myresults.slice_by(obj_label='waste', type='to_bus',
                                date_from=dafr,
                                date_to=dato)
     
    wind_offshore = myresults.slice_by(obj_label='wind_offshore',type='to_bus',
                                date_from=dafr,
                                date_to=dato)

    demand = myresults.slice_by(obj_label='demand',type='to_bus',
                                date_from=dafr,
                                date_to=dato)


    return {'pp_gas_sum': pp_gas.sum(),
            'pp_gas_inst':pp_gas.max()/1,
            'biomass_sum': biomass.sum(),
            'biomass_inst': biomass.max()/1,
            'brown_lig_sum': brown_lig.sum(),
            'brown_lig_inst': brown_lig.max()/1,
            'coal_derived_gas_sum': coal_derived_gas.sum(),
            'coal_derived_gas_inst': coal_derived_gas.max()/1,
            'fossil_gas_sum': fossil_gas.sum(),
            'fossil_gas_inst': fossil_gas.max()/1,
            'fossil_hardcoal_sum':fossil_hardcoal.sum(),
            'fossil_hardcoal_inst':fossil_hardcoal.max()/1,
            'fossil_oil_sum':fossil_oil.sum(),
            'fossil_oil_inst':fossil_oil.max()/1,
            #'fossil_oil_shale_sum':fossil_oil_shale.sum(),
            #'fossil_oil_shale_inst':fossil_oil_shale.max()/1,
            #'fossil_peat_sum':fossil_peat.sum(),
            #'fossil_peat_inst':fossil_peat.max()/1,
            'geothermal_sum':geothermal.sum(),
            'geothermal_inst':geothermal.max()/1,
            'hydro_pumped_storage_sum':hydro_pumped_storage.sum(),
            'hydro_pumped_storage_inst':hydro_pumped_storage.max()/1,
            'run_of_river_sum':run_of_river.sum(),
            'run_of_river_inst':run_of_river.max()/1,
            'hydro_water_reservoir_sum':hydro_water_reservoir.sum(),
            'hydro_water_reservoir_inst':hydro_water_reservoir.max()/1,
            #'marine_sum':marine.sum(),
            #'marine_inst':marine.max()/1,
            'nuclear_sum': nuclear.sum(),
            'nuclear_inst': nuclear.max()/1,
            #'other_sum':other.sum(),
            #'other_inst':other.max()/1,
            #'other_renewable_sum':other_renewable.sum(),
            #'other_renewable_inst':other_reneweable.max()/1,
            'solar_sum': solar.sum(),
            'solar_inst': solar.max()/0.76474,
            'waste_sum': waste.sum(),
            'waste_inst': waste.max()/1,
            'wind_offshore_sum':wind_offshore.sum(),
            'wind_offshore_inst':wind_offshore.max()/1,
            'demand_sum': demand.sum(),
            'demand_max': demand.max(),
            'storage_cap': energysystem.results[storage][storage].invest,
            'objective': energysystem.results.objective
            }


def create_plots(energysystem):

    logging.info('Plot the results')

    cdict = {'storage': '#42c77a',
             'brown_lig':'#8B4513',
             'coal_derived_gas':'#D2B48C',
             'fossil_gas':'#CD661D',
             'fossil_hardcoal':'#030303',
             'fossil_oil':'#8B7355',
             #'fossil_oil_shale':'#636f6b',
             #'fossil_peat':'#636f6b',
             'geothermal': '#ff0000',
             #'marine': '#4169E1',
             'nuclear': '#ff4040',
             #'other':'#32CD32',
             #'other_renewable':'#32CD32',
             'solar':'#ffde32',
             'waste':'#458B74',
             'wind_offshore': '#5b5bae',
             'hydro_pumped_storage':'#00008B',
             'biomass': '#6B8E23',
             'run_of_river':'#00CED1',
             'hydro_water_reservoir': '#20B2AA',
             'pp_gas': '#636f6b',
             'demand': '#ce4aff',
             'excess_bel':'#555555',
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
        barorder=['nuclear','coal_derived_gas','fossil_gas','biomass','run_of_river','brown_lig',
                  'fossil_hardcoal','fossil_oil','fossil_oil_shale','fossil_peat','geothermal',
                  'hydro_pumped_storage','marine','solar','hydro_water_reservoir',
                  'waste','wind_offshore','other','other_renewable','pp_gas'],
        lineorder=['demand', 'storage', 'excess_bel'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(1, 1, 1),
<<<<<<< HEAD
        date_from="2012-06-01 00:00:00",
        date_to="2012-06-28 00:00:00",
=======
        date_from="2012-08-01 00:00:00",
        date_to="2012-09-08 00:00:00",
>>>>>>> abd36e0128a1525e2515063207fb26355b67d384
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
