#!/usr/bin/env python3.5

from graph import *

# Abbreviations used:
#  - ea: exhaust air
#  - ma: mixed air
#  - oa: outside air
#  - ra: return air
#  - sa: supply air


def construct_fan_assembly (nodelist=None):
    nodes = []
    flow_sensor = PrimitiveNode({'name': 'Flow Sensor'}, nodes)
    fan         = PrimitiveNode({'name': 'Fan'}, nodes)
    
    edges = []
    Edge('flow', flow_sensor, fan, edgelist=edges)
    
    incoming_portmap = {
        'input': [{'node': flow_sensor}],
        'control': [{'node': fan}],
    }
    
    outgoing_portmap = {
        'output': [{'node': fan}],
    }
    
    return ComplexNode(nodes, edges, incoming_portmap, outgoing_portmap, {'name': 'Fan Construct'}, nodelist=nodelist)


def construct_ahu1 ():
    nodes = []
    heating_coil = PrimitiveNode({'name': 'Heating Coil'}, nodelist=nodes)
    cooling_coil = PrimitiveNode({'name': 'Cooling Coil'}, nodelist=nodes)
    ma_temperature = PrimitiveNode({'name': 'MA Temperature'}, nodelist=nodes)
    oa_temperature = PrimitiveNode({'name': 'OA Temperature'}, nodelist=nodes)
    ra_temperature = PrimitiveNode({'name': 'RA Temperature'}, nodelist=nodes)
    sa_temperature = PrimitiveNode({'name': 'SA Temperature'}, nodelist=nodes)
    ma_filter = PrimitiveNode({'name': 'MA Filter'}, nodelist=nodes)
    ea_damper = PrimitiveNode({'name': 'EA Damper'}, nodelist=nodes)
    oa_damper = PrimitiveNode({'name': 'OA Damper'}, nodelist=nodes)
    ra_damper = PrimitiveNode({'name': 'RA Damper'}, nodelist=nodes)
    ra_flow_sensor = PrimitiveNode({'name': 'RA Flow Sensor'}, nodelist=nodes)
    ra_fan1 = PrimitiveNode({'name': 'RA Fan 1'}, nodelist=nodes)
    ra_fan2 = PrimitiveNode({'name': 'RA Fan 2'}, nodelist=nodes)
    sa_pressure = PrimitiveNode({'name': 'SA Pressure'}, nodelist=nodes)
    temperature_controller = PrimitiveNode({'name': 'Temperature Controller'}, nodelist=nodes)
    temperature_setpoint   = PrimitiveNode({'name': 'Temperature Setpoint'}, nodelist=nodes)
    pressure_controller = PrimitiveNode({'name': 'Pressure Controller'}, nodelist=nodes)
    pressure_setpoint   = PrimitiveNode({'name': 'Pressure Setpoint'}, nodelist=nodes)
    fan_construct = construct_fan_assembly(nodelist=nodes)
    
    edges = []
    Edge('flow', oa_temperature, oa_damper, edgelist=edges)
    Edge('flow', oa_damper, ma_temperature, edgelist=edges)
    Edge('flow', ma_temperature, ma_filter, edgelist=edges)
    Edge('flow', ma_filter, heating_coil, edgelist=edges)
    Edge('flow', heating_coil, cooling_coil, edgelist=edges)
    Edge('flow', cooling_coil, fan_construct, dst_port='input', edgelist=edges)
    Edge('flow', fan_construct, sa_temperature, src_port='output', edgelist=edges)
    Edge('flow', sa_temperature, sa_pressure, edgelist=edges)
    Edge('control', sa_temperature, temperature_controller, edgelist=edges)
    Edge('control', temperature_setpoint, temperature_controller, edgelist=edges)
    Edge('control', temperature_controller, heating_coil, edgelist=edges)
    Edge('control', temperature_controller, cooling_coil, edgelist=edges)
    Edge('control', sa_pressure, pressure_controller, edgelist=edges)
    Edge('control', pressure_setpoint, pressure_controller, edgelist=edges)
    Edge('control', pressure_controller, fan_construct, dst_port='control', edgelist=edges)
    Edge('flow', ra_temperature, ra_fan1, edgelist=edges)
    Edge('flow', ra_temperature, ra_fan2, edgelist=edges)
    Edge('flow', ra_fan1, ra_flow_sensor, edgelist=edges)
    Edge('flow', ra_fan2, ra_flow_sensor, edgelist=edges)
    Edge('flow', ra_flow_sensor, ea_damper, edgelist=edges)
    Edge('flow', ra_flow_sensor, ra_damper, edgelist=edges)
    Edge('flow', ra_damper, ma_temperature, edgelist=edges)
    
    incoming_portmap = {
        'outside air': [{'node': oa_temperature}],
        'return air': [{'node': ra_temperature}],
    }
    
    outgoing_portmap = {
        'exhaust air': [{'node': ea_damper}],
        'supply air': [{'node': sa_pressure}],
    }
    
    return ComplexNode(nodes, edges, incoming_portmap, outgoing_portmap, {'name': 'AHU-1'})

ahu1 = construct_ahu1()
ahu1.store_dotfile('ahu1.dot')

# dot -Tpdf ahu1.dot -Gnewank -o ahu1.pdf

