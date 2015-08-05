"""populate sensortype nodetype

Revision ID: 25a5ee59d391
Revises: 249f360e32e3
Create Date: 2013-01-15 22:03:46.253985

"""

# revision identifiers, used by Alembic.
revision = '25a5ee59d391'
down_revision = '249f360e32e3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Float


def upgrade():
    sensortype = table('SensorType',
                       column('id', Integer),
                       column('name', String(255)),
                       column('code', String(50)),
                       column('units', String(20)),
                       column('c0', Float),
                       column('c1', Float),
                       column('c2', Float),
                       column('c3', Float))

    op.bulk_insert(sensortype,
                   [{'id': 0, 'name': "Temperature",
                     'code': "T",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 1, 'name': "Delta Temperature",
                     'code': "dT",
                     'units': "deg.C/s",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 2, 'name': "Humidity",
                     'code': "RH",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 3, 'name': "Delta Humidity",
                     'code': "dRH",
                     'units': "%/s",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 4, 'name': "Light PAR",
                     'code': "PAR",
                     'units': "Lux",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 5, 'name': "Light TSR",
                     'code': "TSR",
                     'units': "Lux",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 6, 'name': "Battery Voltage",
                     'code': "BAT",
                     'units': "V",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 7, 'name': "Delta Battery Voltage",
                     'code': "dBT",
                     'units': "V/s",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 8, 'name': "CO2",
                     'code': "CO2",
                     'units': "ppm",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 9, 'name': "Air Quality",
                     'code': "AQ",
                     'units': "ppm",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 10, 'name': "VOC",
                     'code': "VOC",
                     'units': "ppm",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 11, 'name': "Power",
                     'code': "POW",
                     'units': "W",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 12, 'name': "Heat",
                     'code': "HET",
                     'units': "W",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 13, 'name': "Duty cycle",
                     'code': "DUT",
                     'units': "ms",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 14, 'name': "Error",
                     'code': "ERR",
                     'units': "",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 15, 'name': "Power Min",
                     'code': "PMI",
                     'units': "w",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 16, 'name': "Power Max",
                     'code': "PMA",
                     'units': "w",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 17, 'name': "Power Consumption",
                     'code': "CON",
                     'units': "kWh",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 18, 'name': "Heat Energy",
                     'code': "HEN",
                     'units': "kWh",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 19, 'name': "Heat Volume",
                     'code': "HVO",
                     'units': "L",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 20, 'name': "Delta CO2",
                     'code': "dCO2",
                     'units': "ppm/s",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.}, 
                    {'id': 21, 'name': "Delta VOC",
                     'code': "dVOC",
                     'units': "ppm/s",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.}, 
                    {'id': 22, 'name': "Delta AQ",
                     'code': "dAQ",
                     'units': "v/s",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.}, 
                    {'id': 23, 'name': "Temperature Health",
                     'code': "TH",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 24, 'name': "Temperature Cold",
                     'code': "TC",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 25, 'name': "Temperature Comfort",
                     'code': "TM",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 26, 'name': "Temperature Warm",
                     'code': "TW",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 27, 'name': "Temperature Over",
                     'code': "TO",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 28, 'name': "Humidity Dry",
                     'code': "HD",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 29, 'name': "Humidity Comfort",
                     'code': "HC",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 30, 'name': "Humidity Damp",
                     'code': "HDA",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 31, 'name': "Humidity Risk",
                     'code': "HR",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 32, 'name': "CO2 Acceptable",
                     'code': "CA",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 33, 'name': "CO2 Minor",
                     'code': "CMIN",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 34, 'name': "CO2 Medium",
                     'code': "CMED",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 35, 'name': "CO2 Major",
                     'code': "CMAJ",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 36, 'name': "VOC Acceptable",
                     'code': "VA",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 37, 'name': "VOC Poor",
                     'code': "VP",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 38, 'name': "AQ Acceptable",
                     'code': "AA",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 39, 'name': "AQ Poor",
                     'code': "AP",
                     'units': "%",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 40, 'name': "Opti Smart Count",
                     'code': "imp",
                     'units': "imp",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 99, 'name': "Gas Consumption",
                     'code': "Gas",
                     'units': "kWh",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 102, 'name': "Outside Temperature",
                     'code': "ws_temp_out",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 103, 'name': "Outside Humidity",
                     'code': "ws_hum_out",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 104, 'name': "WS Inside Temperature",
                     'code': "ws_temp_in",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 105, 'name': "WS Inside Humidity",
                     'code': "ws_hum_in",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 106, 'name': "Dew Point",
                     'code': "ws_dew",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 107, 'name': "Apparent Temperature",
                     'code': "ws_apparent_temp",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 108, 'name': "Wind Gust",
                     'code': "ws_wind_gust",
                     'units': "mph",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 109, 'name': "Average Wind Speed",
                     'code': "ws_wind_ave",
                     'units': "mph",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 110, 'name': "Wind Direction",
                     'code': "ws_wind_dir",
                     'units': "",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 111, 'name': "Wind Chill",
                     'code': "ws_wind_chill",
                     'units': "deg.C",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 112, 'name': "Rain Fall",
                     'code': "ws_rain",
                     'units': "mm",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.},
                    {'id': 113, 'name': "Absolute Pressure",
                     'code': "ws_abs_pressure",
                     'units': "hpa",
                     'c0': 0., 'c1': 1., 'c2': 0., 'c3': 0.}])

    pass

def downgrade():
    pass