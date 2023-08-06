import os
from dftinpgen import atoms
from dfttopif.drivers import directory_to_pif
from pypif.pif import Property, Scalar


class ParserError(Exception):
    pass


def get_number_of_atoms(calc_dir):
    """Returns the number of atoms in the structure in the input directory
    as a `pif.Property` object; returns None if number of atoms is not
    found.
    (Uses the parsers in `dfttopif.parsers`)
    """
    if calc_dir is None:
        return None
    chem = directory_to_pif(calc_dir, quality_report=False)
    natoms = list(filter(lambda x: 'number of atoms' in x.name.lower(),
                         chem.properties))
    if not natoms:
        return None
    return natoms[0]


def get_total_energy(calc_dir):
    """Returns the total energy per atom from the DFT calculation in the
    input directory as a `pif.Property` object; returns None if total energy
    is not found.
    (Uses the parsers in `dfttopif.parsers`)
    """
    if calc_dir is None:
        return None
    chem = directory_to_pif(calc_dir, quality_report=False)
    toten = list(filter(lambda x: 'total energy' in x.name.lower(),
                        chem.properties))
    if not toten:
        return None
    return toten[0]


def get_total_energy_pa(toten, natoms):
    """Returns total energy per atom as a `pif.Property` object or None."""
    if not toten or not natoms:
        return None
    toten_pa = toten.scalars[0].value/float(natoms.scalars[0].value)
    return Property(name='Total energy per atom',
                    methods=toten.methods,
                    conditions=toten.conditions,
                    data_type='COMPUTATIONAL',
                    scalars=[Scalar(value=toten_pa)],
                    units='eV/atom')


def get_volume(calc_dir):
    """Returns the volume from the DFT calculation in the input directory as
    a `pif.Property` object; returns None if volume is not found.
    """
    if calc_dir is None:
        return None
    chem = directory_to_pif(calc_dir, quality_report=False)
    volume = list(filter(lambda x: 'final volume' in x.name.lower(),
                         chem.properties))
    if not volume:
        return None
    return volume[0]


def get_volume_pa(vol, natoms):
    """Returns volume per atom as a `pif.Property` object or None."""
    if not vol or not natoms:
        return None
    vol_pa = vol.scalars[0].value/float(natoms.scalars[0].value)
    return Property(name='Volume per atom',
                    methods=vol.methods,
                    conditions=vol.conditions,
                    data_type='COMPUTATIONAL',
                    scalars=[Scalar(value=vol_pa)],
                    units='Angstrom^3/atom')


def get_ntv_data(calc_dir):
    """Parse and return as a dictionary the number of atoms, total energy
    and volume per atom from the specified DFT calculation directory."""
    natoms = get_number_of_atoms(calc_dir)
    props = {
        'number_of_atoms': natoms,
        'total_energy_per_atom': get_total_energy_pa(get_total_energy(calc_dir), natoms),
        'volume_per_atom': get_volume_pa(get_volume(calc_dir), natoms)
    }
    return props


def parse_mixing_calculations_data(mixing_calculations=None):
    """Parse all properties from mixing calculations (DFT)."""
    if not mixing_calculations:
        return {}

    calcs_data = dict()

    # solvent calculation data
    calcs_data['solvent'] = get_ntv_data(mixing_calculations['solvent']['static'].directory)

    # all solutes calculation data
    calcs_data['solutes'] = {}
    for solute in mixing_calculations['solutes']:
        calcs_data['solutes'][solute] = {}
        for ref in ['defect', 'solvent_structure', 'reference_structure']:
            calcs_data['solutes'][solute][ref] = get_ntv_data(
                mixing_calculations['solutes'][solute][ref]['static'].directory)

    return calcs_data


def parse_calculations_from_tree(base_dir=None):
    """Parse all DFT calculations from the specified directory tree `base_dir`."""
    if not base_dir:
        err_msg = 'Base directory for calculations not specified'
        raise ParserError(err_msg)

    if not os.path.isdir(base_dir):
        err_msg = 'Specified directory {} not found'.format(base_dir)
        raise ParserError(err_msg)

    calcs_data = dict()

    # solvent calculation data
    calc_dir = os.path.join(base_dir, 'solvent', 'static')
    if os.path.exists(calc_dir):
        calcs_data['solvent'] = get_ntv_data(calc_dir)

    # all solutes calculation data
    calcs_data['solutes'] = {}
    solutes_dir = os.path.join(base_dir, 'solutes')
    if os.path.exists(solutes_dir):
        for root, dirnames, filenames in os.walk(solutes_dir):
            try:
                solute, ref, calc = root.split('/')[-3:]
            except ValueError:
                continue
            if not calc == 'static':
                continue
            if ref not in ['defect', 'solvent_structure', 'reference_structure']:
                continue
            if solute not in atoms.ATOMIC_MASSES:
                continue
            if solute not in calcs_data['solutes']:
                calcs_data['solutes'][solute] = {ref: get_ntv_data(root)}
            calcs_data['solutes'][solute].update({ref: get_ntv_data(root)})

    return calcs_data
