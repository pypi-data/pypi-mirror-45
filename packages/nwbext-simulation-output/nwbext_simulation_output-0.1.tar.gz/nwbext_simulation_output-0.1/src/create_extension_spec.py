from pynwb.spec import NWBDatasetSpec, NWBNamespaceBuilder, NWBGroupSpec, NWBLinkSpec
import os

name = 'simulation_output'

doc = 'NWB:N extension for storing large-scale simulation output ' \
      'with multi-cell multi-compartment recordings'
ns_builder = NWBNamespaceBuilder(doc=doc, name=name, version='0.2.1',
                                 author=['Ben Dichter', 'Kael Dai'],
                                 contact='ben.dichter@gmail.com')

ns_builder.include_type('VectorData', namespace='core')
ns_builder.include_type('VectorIndex', namespace='core')
ns_builder.include_type('TimeSeries', namespace='core')
ns_builder.include_type('DynamicTable', namespace='core')

# Continuous data for cell compartments

Compartments = NWBGroupSpec(
    default_name='compartments',
    neurodata_type_def='Compartments',
    neurodata_type_inc='DynamicTable',
    doc='table that holds information about what places are being recorded',
    datasets=[
        NWBDatasetSpec(name='number',
                       neurodata_type_inc='VectorData',
                       doc='cell compartment ids corresponding to a each column in the data',
                       dtype='int'),
        NWBDatasetSpec(name='number_index',
                       neurodata_type_inc='VectorIndex',
                       doc='maps cell to compartments',
                       quantity='?'),
        NWBDatasetSpec(name='position',
                       neurodata_type_inc='VectorData',
                       doc='position of recording within a compartment. 0 is close to soma, 1 is other end',
                       dtype='float',
                       quantity='?'),
        NWBDatasetSpec(name='position_index',
                       neurodata_type_inc='VectorIndex',
                       doc='indexes position',
                       quantity='?'),
        NWBDatasetSpec(name='label',
                       neurodata_type_inc='VectorData',
                       doc='labels for compartments',
                       dtype='text',
                       quantity='?'),
        NWBDatasetSpec(name='label_index',
                       neurodata_type_inc='VectorIndex',
                       doc='indexes label',
                       quantity='?')
    ]
)
CompartmentsSeries = NWBGroupSpec(
    neurodata_type_def='CompartmentSeries',
    neurodata_type_inc='TimeSeries',
    doc='Stores continuous data from cell compartments',
    links=[
        NWBLinkSpec(name='compartments',
                    target_type='Compartments',
                    doc='meta-data about compartments in this CompartmentSeries')
    ]
)

ns_path = name + '.namespace.yaml'
ext_source = name + '.extensions.yaml'

# Export
for neurodata_type in [Compartments, CompartmentsSeries]:
    ns_builder.add_spec(ext_source, neurodata_type)
ns_builder.export(ns_path, outdir=os.path.join('..', 'spec'))
