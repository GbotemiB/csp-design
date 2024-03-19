#!/usr/bin/env python
# coding: utf-8
import pypsa
import numpy as np
import pandas as pd
import logging

# initialize network
n = pypsa.Network()

# use 24 hour period for consideration
index = pd.date_range("2024-01-01 00:00", "2024-01-01 23:00", freq="H")
n.set_snapshots(index)

np.random.seed(10)  # for reproducibility

# time-varying inputs for generator, link and load
p_nom_max = pd.Series(
    (np.random.uniform() for idx in range(len(n.snapshots))),
    index=n.snapshots, name="p_nom_max"
)

link_var = pd.Series(
    (np.random.uniform(len(n.snapshots))),
    index=n.snapshots, name="link"
)

load_var = pd.Series(
    100 * np.random.rand(len(n.snapshots)), index=n.snapshots, name="load"
)

# add carriers
n.add("Carrier", "heat")
n.add("Carrier", "AC")

# add buses
n.add("Bus", "csp_internal_bus", carrier="heat")
n.add("Bus", "electricity_bus", carrier="AC")

# add stores
n.add("Store", "salt_tank", bus="csp_internal_bus",
      standing_loss=0.01, capital_cost=600, e_nom_extendable=True)

# add generator and store
n.add("Generator", "receiver", bus="csp_internal_bus", p_set=100,
      capital_cost=700, p_nom_extendable=True, p_max_pu=p_nom_max)

# add links
n.add("Link", "csp_turbine", bus0="csp_internal_bus", bus1="electricity_bus",
      efficiency=0.6, p_nom_extendable=True, capital_cost=1000, p_max_pu=link_var)

# add load
n.add("Load", "external_load", bus="electricity_bus", p_set=load_var)

n.optimize()

logging.info(f"Network Objective: {n.objective}")
