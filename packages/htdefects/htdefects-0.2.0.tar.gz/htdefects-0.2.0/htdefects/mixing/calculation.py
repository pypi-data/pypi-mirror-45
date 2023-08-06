import os
import shutil
import six

from pypif.pif import Property, Scalar
import dftinpgen
from dftinpgen import atoms
from dftinpgen import calculation

from htdefects.mixing.defect import MixingDefectSet
from htdefects.mixing.parsers import parse_mixing_calculations_data


def _get_prop_val(prop):
    if not prop:
        return None
    return prop.scalars[0].value


class MixingCalculationError(Exception):
    """Base class for handling errors associated with a single dilute mixing defect."""
    pass


class MixingCalculationSet(MixingDefectSet):
    """Class to set up calculations for a set of dilute mixing defects."""

    def __init__(self, solvent_element=None, solvent_reference_structure_file=None,
                 solute_elements=None, solute_reference_structure_files=None,
                 min_image_dist=None, calc_dir=None, pseudo_dir=None, do_relaxation=None,
                 dft_code=None, dft_params=None, from_scratch=None, **kwargs):
        """Constructor.

        Args:

            solvent_element: String with the symbol of the solvent element.

            solvent_reference_structure_file: String specifying the location of the reference
                structure of the solvent in the VASP5 format.

            solute_elements: List of String objects each representing the symbol of a
                solute element.

            solute_reference_structure_files: Dictionary of solute elements (String) and the
                location of the respective reference structure files in the VASP5 format (String).

            min_image_dist: Floating point number representing the minimum distance between
                periodic images of the defect in a supercell, in Angstrom. Defaults to 15.

            calc_dir: String specifying the directory to perform all the defect calculations
                in. Defaults to a folder named "[solvent_element]_defects_set" at the location of
                the `solvent_reference_structure_file`.

            pseudo_dir: String specifying the location of the pseudopotentials. Defaults to the
                pseudopotentials folder in the `dftinpgen` module.

            do_relaxation: Boolean specifying if the structures should be relaxed before a
                final static calculation? If True, separate folders are created for the relaxation
                and static runs for each defect. Defaults to True.

            dft_code: String specifying the DFT package to use. Currently available options are
                VASP and PWscf. Defaults to VASP.

            dft_params: Dictionary of parameters for the DFT calculations and their
                corresponding values. If, a String "default" is input instead, defaults as defined
                in `dftinpgen` are used. Defaults to "default".

            from_scratch: Boolean specifying if the calculations have to started from scratch,
                i.e., the entire directory structure and input files will be deleted if present,
                and fresh calculations will be set up. Defaults to True.

            kwargs: Other keyword arguments.

        """

        self._solvent_reference_structure_file = None
        self.solvent_reference_structure_file = solvent_reference_structure_file
        _solvent_reference_structure = atoms.Structure(self.solvent_reference_structure_file)

        self._solute_reference_structure_files = None
        self.solute_reference_structure_files = solute_reference_structure_files
        _solute_reference_structures = dict([(e, atoms.Structure(f)) for e, f in
                                                 self.solute_reference_structure_files.items()])

        super().__init__(
            solvent_element=solvent_element,
            solvent_reference_structure=_solvent_reference_structure,
            solute_elements=solute_elements,
            solute_reference_structures=_solute_reference_structures,
            min_image_dist=min_image_dist,
            **kwargs)

        self._calc_dir = None
        self.calc_dir = calc_dir

        self._pseudo_dir = None
        self.pseudo_dir = pseudo_dir

        self._do_relaxation = None
        self.do_relaxation = do_relaxation

        self._dft_code = None
        self.dft_code = dft_code

        self._dft_params = None
        self.dft_params = dft_params

        self._from_scratch = None
        self.from_scratch = from_scratch

        self._mixing_calculations = {}
        self._mixing_calculations_data = {}
        self._mixing_properties = {}

    @property
    def solvent_reference_structure_file(self):
        """String with the location of the structure file of the solvent, in the VASP5 format."""
        return self._solvent_reference_structure_file

    @solvent_reference_structure_file.setter
    def solvent_reference_structure_file(self, solvent_reference_structure_file):
        if not os.path.isfile(solvent_reference_structure_file):
            error_msg = 'Input solvent structure file {} not found'.format(solvent_reference_structure_file)
            raise MixingCalculationError(error_msg)
        self._solvent_reference_structure_file = solvent_reference_structure_file

    @property
    def solute_reference_structure_files(self):
        """Dictionary of the solute elements (String) and the locations of the corresponding
        structure files in the VASP5 format (String)."""
        return self._solute_reference_structure_files

    @solute_reference_structure_files.setter
    def solute_reference_structure_files(self, solute_reference_structure_files):
        self._solute_reference_structure_files = {}
        if solute_reference_structure_files is None:
            return
        for element, structure_file in solute_reference_structure_files.items():
            if not os.path.isfile(structure_file):
                error_msg = 'Input solute structure file {} not found'.format(structure_file)
                raise MixingCalculationError(error_msg)
            self._solute_reference_structure_files.update({element: structure_file})

    @property
    def calc_dir(self):
        """String with the location where the calculations need to be set up/performed."""
        return self._calc_dir

    @calc_dir.setter
    def calc_dir(self, calc_dir):
        if calc_dir is None:
            solvent_structure_file_dir = os.path.dirname(self.solvent_reference_structure_file)
            default_calc_dir_name = '{}_mixing_defects'.format(self.solvent_element)
            self._calc_dir = os.path.join(solvent_structure_file_dir, default_calc_dir_name)
        else:
            self._calc_dir = calc_dir

    @property
    def pseudo_dir(self):
        """String with the location of the pseudopotential files."""
        return self._pseudo_dir

    @pseudo_dir.setter
    def pseudo_dir(self, pseudo_dir):
        if pseudo_dir is None:
            self._pseudo_dir = os.path.join((os.path.dirname(dftinpgen.__file__)), 'pseudo')
        else:
            self._pseudo_dir = pseudo_dir

    @property
    def do_relaxation(self):
        """Boolean specifying whether all structures need to be relaxed or not."""
        return self._do_relaxation

    @do_relaxation.setter
    def do_relaxation(self, do_relaxation):
        self._do_relaxation = True
        if isinstance(do_relaxation, six.string_types):
            self._do_relaxation = do_relaxation.strip().lower()[0] == 't'
        elif isinstance(do_relaxation, bool):
            self._do_relaxation = do_relaxation

    @property
    def dft_code(self):
        """String specifying the DFT package to use. Current options: VASP/PWscf."""
        return self._dft_code

    @dft_code.setter
    def dft_code(self, dft_code):
        if dft_code is None:
            self._dft_code = 'vasp'
            return
        if dft_code.strip().lower() not in calculation.supported_codes:
            error_msg = 'DFT code {} not supported.'.format(dft_code)
            error_msg += 'Use one of {}'.format('/'.join(calculation.supported_codes))
            raise MixingCalculationError(error_msg)
        self._dft_code = dft_code.strip().lower()

    @property
    def dft_params(self):
        """Dictionary with parameters (String) and corresponding values (String/Float/Integer) to
        be used in the DFT calculations. Alternatively, if it is a String "default",
        default parameters from the `dftinpgen` module are used."""
        return self._dft_params

    @dft_params.setter
    def dft_params(self, dft_params):
        self._dft_params = 'default'
        if dft_params is not None:
            self._dft_params = dft_params

    @property
    def from_scratch(self):
        """Boolean specifying if previous set of calculations, directories should be deleted
        before setting up new calculations."""
        return self._from_scratch

    @from_scratch.setter
    def from_scratch(self, from_scratch):
        self._from_scratch = True
        if isinstance(from_scratch, six.string_types):
            self._from_scratch = from_scratch.strip().lower()[0] == 't'
        elif isinstance(from_scratch, bool):
            self._from_scratch = from_scratch

    def setup_mixing_calculations(self):
        """Sets up all the relevant mixing calculations, and populates a Dictionary with the
        directory structure and the respective DftCalc objects.

        Uses the following directory structure for all the calculations (creating directories
        when necessary/as specified):
        [solvent]_mixing_defects -> solvent -> relax, static
                                     -> solutes -> [element 1] -> reference_structure -> relax, static
                                                                  solvent_structure   -> relax, static
                                                                  defect              -> relax, static
                                                -> [element 2] -> reference_structure -> relax, static
                                                                  solvent_structure   -> relax, static
                                                                  defect              -> relax, static
                                                -> [element 3] -> ...
                                     ...
        The corresponding `dftinpgen.calculation.DftCalc` objects are stored in a Dictionary
        that mimics the directory structure above, `mixing_calculations`.

        """
        # make defect set directory
        if self.from_scratch:
            if os.path.isdir(self.calc_dir):
                shutil.rmtree(self.calc_dir)

        if not os.path.isdir(self.calc_dir):
            os.mkdir(self.calc_dir)

        # solvent
        calc_dir = os.path.join(self.calc_dir, 'solvent')
        if not os.path.isdir(calc_dir):
            os.mkdir(calc_dir)
        dft_calcs = self._setup_dft_calcs(self.solvent_reference_structure, calc_dir,
                                          do_relaxation=self.do_relaxation)
        self._mixing_calculations['solvent'] = dft_calcs

        # all solutes
        self._mixing_calculations['solutes'] = {}
        ref_to_struct = {
            'defect': 'defect_structure',
            'solvent_structure': 'solute_in_solvent_structure',
            'reference_structure': 'solute_reference_structure'
        }
        for solute, defect in self.mixing_defects.items():
            self._mixing_calculations['solutes'][solute] = {}
            if not os.path.isdir(os.path.join(self.calc_dir, 'solutes', solute)):
                os.makedirs(os.path.join(self.calc_dir, 'solutes', solute))

            for ref, struct in ref_to_struct.items():
                calc_dir = os.path.join(self.calc_dir, 'solutes', solute, ref)
                self._mixing_calculations['solutes'][solute][ref] = self._setup_dft_calcs(
                    getattr(defect, struct), calc_dir, do_relaxation=self.do_relaxation
                )

    def _setup_dft_calcs(self, structure, calc_dir, do_relaxation=True):
        """Sets up the DFT calculation(s) for the specified structure in the specified location.

        Args:
            structure: `dftinpgen.atoms.Structure` object representing the structure.

            calc_dir: String specifying the calculation directory.

            do_relaxation: Boolean specifying if a relaxation calculation should be performed.
                Defaults to True.

        Returns:
            Dictionary of job type ("relax"/"static") and the corresponding DFT calculation as
            `dftinpgen.calculation.DftCalc` objects. Default value is None.

        """
        if structure is None:
            return None

        if not os.path.isdir(calc_dir):
            os.mkdir(calc_dir)

        job_types = ['relax', 'static']
        dft_calcs = dict([(jt, None) for jt in job_types])
        if not do_relaxation:
            job_types.remove('relax')

        for job_type in job_types:
            dft_calcs[job_type] = self._setup_dft_calc(structure, calc_dir, job_type=job_type)

        return dft_calcs

    def _setup_dft_calc(self, structure, calc_base_dir, job_type='static'):
        """Sets up a DFT calculation in the specified location, for the specified structure and
        job type.

        Args:
            structure: `dftinpgen.atoms.Structure` object of the structure.

            calc_base_dir: String specifying the location in a which a directory `job_type` will
                be used to set up the calculation.

            job_type: String specifying the type of the DFT run. One of "relax"/"static".
                Defaults to "static".

        Returns:
            `dftinpgen.calculation.DftCalc` object corresponding to the specified
            calculation directory, structure, pseudopotentials, parameters, DFT code, and job type.

        """
        job_dir = os.path.join(calc_base_dir, job_type)

        if not os.path.isdir(job_dir):
            os.mkdir(job_dir)

        structure_file = os.path.join(job_dir, 'POSCAR')
        structure.pposcar(structure_file)

        dft_calc = calculation.DftCalc(job_dir, structure_file, self.pseudo_dir,
                                       params=self.dft_params, code=self.dft_code, jobtype=job_type)
        dft_calc.gen_input_files()

        return dft_calc

    @property
    def mixing_calculations(self):
        """Dictionary with the solvent/solute and all the relevant DFT calculation objects.

        The structure of the dictionary mimics the directory structure:
        mixing_calculations["solvent"][solvent element]["relax"/"static"]
        mixing_calculations["solutes"][solute 1]["reference_structure"]["relax"/"static"]
                                                   ["solvent_structure"]["relax"/"static"]
                                                   ["defect"]["relax"/"static"]
        mixing_calculations["solutes"][solute 2]["reference_structure"]["relax"/"static"]
                                                   ...
        The values are either `dftinpgen.calculation.DftCalc` objects or None.
        """
        return self._mixing_calculations

    def _parse_mixing_calculations_data(self):
        self._mixing_calculations_data = parse_mixing_calculations_data(self.mixing_calculations)

    @property
    def mixing_calculations_data(self):
        """Dictionary of properties relevant to mixing parsed directly from
        output files of DFT calculations.

        The structure of the dictionary mimics the default directory structure
        (see `self.mixing_calculations`).
        """
        if not self._mixing_calculations_data:
            self._parse_mixing_calculations_data()
        return self._mixing_calculations_data

    @mixing_calculations_data.setter
    def mixing_calculations_data(self, mcd=None):
        self._mixing_calculations_data = mcd

    def calculate_mixing_energy(self, solute, reference='solvent_structure'):
        """Calculate mixing energy:
        E_mix(solute) = E_defect(N) - (N-1)*E_solvent - 1*E_solute
        Returns None if any of the quantities is not available.
        """
        n_atoms = _get_prop_val(self.mixing_calculations_data['solutes'][solute]['defect']['number_of_atoms'])
        e_solvent = _get_prop_val(self.mixing_calculations_data['solvent']['total_energy_per_atom'])
        e_defect = _get_prop_val(self.mixing_calculations_data['solutes'][solute]['defect']['total_energy_per_atom'])
        e_solute = _get_prop_val(self.mixing_calculations_data['solutes'][solute][reference]['total_energy_per_atom'])
        if any([p is None for p in [n_atoms, e_defect, e_solvent, e_solute]]):
            return None
        e_mix = n_atoms*e_defect - (n_atoms-1)*e_solvent - 1*e_solute
        return Property(name='Mixing energy ({})'.format(reference),
                        data_type='COMPUTATIONAL',
                        scalars=[Scalar(value=e_mix)],
                        units='eV/defect')

    def calculate_mixing_volume(self, solute):
        """Calculate mixing volume:
        V_mix(solute) = V_defect(N) - V_solvent(N)
        Returns None if any of the quantities is not available."""
        n_atoms = _get_prop_val(self.mixing_calculations_data['solutes'][solute]['defect']['number_of_atoms'])
        v_defect = _get_prop_val(self.mixing_calculations_data['solutes'][solute]['defect']['volume_per_atom'])
        v_solvent = _get_prop_val(self.mixing_calculations_data['solvent']['volume_per_atom'])
        if any([p is None for p in [n_atoms, v_defect, v_solvent]]):
            return None
        v_mix = n_atoms*v_defect - n_atoms*v_solvent
        return Property(name='Mixing volume',
                        data_type='COMPUTATIONAL',
                        scalars=[Scalar(value=v_mix)],
                        units='Angstrom^3/defect')

    def calculate_solute_mixing_properties(self, solute):
        """Calculate dilute mixing energy and mixing volume for a given solute."""
        props = {
            'mixing_energy_ss': self.calculate_mixing_energy(solute, reference='solvent_structure'),
            'mixing_energy_rs': self.calculate_mixing_energy(solute, reference='reference_structure'),
            'mixing_volume': self.calculate_mixing_volume(solute)
        }
        return props

    def calculate_mixing_properties(self):
        """Calculate dilute mixing energy and volume for all solutes."""
        self._parse_mixing_calculations_data()
        for solute in self.solute_elements:
            self._mixing_properties[solute] = self.calculate_solute_mixing_properties(solute)

    @property
    def mixing_properties(self):
        """Dictionary of dilute mixing energy and volume data as `pif.Property` objects."""
        if not self._mixing_properties:
            self.calculate_mixing_properties()
        return self._mixing_properties
