import sys
import copy
import six
import numpy as np

from dftinpgen import atoms

from htdefects.data import ELEM_VOLUMES
from htdefects.mixing import supercell


class MixingDefectError(Exception):
    """Base class for handling errors associated with a single dilute mixing defect."""
    pass


def _validate_input_element(element):
    """Is the input a valid element?"""
    if element not in atoms.ATOMIC_MASSES:
        error_msg = 'Invalid input element: {}'.format(element)
        raise MixingDefectError(error_msg)


def _validate_input_structure(structure):
    """Is the input a valid `citrine_dft.atoms.Structure` object?"""
    if not isinstance(structure, atoms.Structure):
        error_msg = 'Structure: {} is not of type `atoms.Structure`'.format(structure)
        raise MixingDefectError(error_msg)


def _structure_has_element(structure, element):
    """Does the input structure have the input element?"""
    if element in structure.atomtypes:
        return True
    return False


class MixingDefect(object):
    """Class to represent a dilute substitutional (point-)defect."""

    def __init__(self, solvent_element=None,
                 solvent_reference_structure=None, solute_element=None,
                 solute_reference_structure=None, min_image_dist=None,
                 supercell_for_mixing=None, **kwargs):
        """Constructor.

        Args:

            solvent_element: String with the symbol of the solvent element.

            solvent_reference_structure: Reference crystal structure of the solvent as a
                `citrine_dft.atoms.Structure` object.

            solute_element: String with the symbol of the solute/impurity element.

            solute_reference_structure: Reference crystal structure of the solvent as a
                `citrine_dft.atoms.Structure` object.

            min_image_dist: Floating point number representing the minimum distance between
                periodic images of the defect in a supercell, in Angstrom. Defaults to 15.

            supercell_for_mixing (:obj:`atoms.Structure`):
                Supercell structure to use for creating a dilute mixing defect.

            kwargs: Other keyword arguments.

        Raises:

            MixingDefectError if

                - The solvent/solute element is not recognized.
                - The solvent reference structure is not provided/not in the correct format.
                - The provided solute reference structure is not in the correct format.
                - The solvent (solute) element specified is not in the input solvent (solute)
                reference structure.

        """

        self._solvent_element = None
        self.solvent_element = solvent_element

        self._solvent_reference_structure = None
        self.solvent_reference_structure = solvent_reference_structure

        self._solute_element = None
        self.solute_element = solute_element

        self._solute_reference_structure = None
        if solute_reference_structure is not None:
            self.solute_reference_structure = solute_reference_structure

        self._min_image_dist = None
        self.min_image_dist = min_image_dist

        self._supercell_for_mixing = None
        self.supercell_for_mixing = supercell_for_mixing


    @property
    def solvent_element(self):
        """String specifying the atomic symbol of the solvent element."""
        return self._solvent_element

    @solvent_element.setter
    def solvent_element(self, solvent_element):
        _validate_input_element(solvent_element)
        self._solvent_element = solvent_element

    @property
    def solvent_reference_structure(self):
        """`citrine_dft.atoms.Structure` object of the reference structure of the solvent."""
        return self._solvent_reference_structure

    @solvent_reference_structure.setter
    def solvent_reference_structure(self, solvent_reference_structure):
        if solvent_reference_structure is None:
            error_msg = 'Solvent reference structure (required) is not provided'
            raise MixingDefectError(error_msg)

        _validate_input_structure(solvent_reference_structure)
        if not _structure_has_element(solvent_reference_structure, self.solvent_element):
            error_msg = 'Input solvent reference structure {}'.format(solvent_reference_structure)
            error_msg += ' does not contain solvent element {}'.format(self.solvent_element)
            raise MixingDefectError(error_msg)
        self._solvent_reference_structure = solvent_reference_structure

    @property
    def solute_element(self):
        """String specifying the atomic symbol of the solute element."""
        return self._solute_element

    @solute_element.setter
    def solute_element(self, solute_element):
        _validate_input_element(solute_element)
        self._solute_element = solute_element

    @property
    def solute_reference_structure(self):
        """`citrine_dft.atoms.Structure` object of the reference structure of the solute."""
        return self._solute_reference_structure

    @solute_reference_structure.setter
    def solute_reference_structure(self, solute_reference_structure):
        _validate_input_structure(solute_reference_structure)
        if not _structure_has_element(solute_reference_structure, self.solute_element):
            error_msg = 'Input solute reference structure {}'.format(solute_reference_structure)
            error_msg += ' does not contain solute element {}'.format(self.solute_element)
            raise MixingDefectError(error_msg)
        self._solute_reference_structure = solute_reference_structure

    @property
    def min_image_dist(self):
        """Floating point number with the minimum distance between periodic defect images in a
        supercell, in Angstrom."""
        return self._min_image_dist

    @min_image_dist.setter
    def min_image_dist(self, min_image_dist):
        if min_image_dist is None:
            sys.stdout.write('Minimum image distance not provided. Using defaults.\n')
            self._min_image_dist = 15.0
            return
        try:
            self._min_image_dist = float(min_image_dist)
        except ValueError:
            sys.stdout.write('Invalid input for `min_image_dist`: {}.'.format(min_image_dist))
            sys.stdout.write(' Using defaults.\n')
            self._min_image_dist = 15.0

    @property
    def supercell_for_mixing(self):
        """Solvent supercell to use for creating a dilute mixing defect."""
        return self._supercell_for_mixing

    @supercell_for_mixing.setter
    def supercell_for_mixing(self, supercell_for_mixing):
        if supercell_for_mixing is None:
            self._supercell_for_mixing = supercell.get_supercell_for_mixing(
                    structure=self.solvent_reference_structure,
                    min_image_dist=self.min_image_dist,
            )
            return

        _validate_input_structure(supercell_for_mixing)
        if not _structure_has_element(supercell_for_mixing,
                                      self.solvent_element):
            error_msg = 'Defect supercell does not contain solvent element'
            raise MixingDefectError(error_msg)
        self._supercell_for_mixing = supercell_for_mixing

    @property
    def solute_in_solvent_structure(self):
        """Bulk solute in the structure of the solvent as a `citrine_dft.atoms.Structure` object.

        The structure is generated by replacing all solvent atoms in
        `self.solvent_reference_structure` with the solute, and scaling lattice vectors according
        to the elemental volumes of the solute and the solvent in their respective ground states.
        (Data in `citrine_defects.ELEM_VOLUMES` dictionary.) Currently implemented only for
        elemental solvents.
        """
        if len(self.solvent_reference_structure.atomtypes) > 1:
            return None

        structure = copy.deepcopy(self.solvent_reference_structure)
        structure.title = '{}{}'.format(structure.atomtypes[0], structure.natoms[0])

        # replace all solvent atoms with solute atoms
        structure.atomtypes = [self.solute_element]
        structure.gen_atominfo()

        # scale the cell isotropically
        volume_ratio = ELEM_VOLUMES[self.solute_element]/ELEM_VOLUMES[self.solvent_element]
        scaling_factor = volume_ratio**(1./3.)
        structure.cell = np.array([[a_n*scaling_factor for a_n in a] for a in structure.cell])

        # recalculate ionic positions in cartesian coordinates
        structure.ionsc = np.dot(structure.ions, structure.cell)
        structure.cellinfo()
        return structure

    def replace_solvent_atom_with_solute(self, structure):
        # Replace a solvent atom in the supercell with the solute
        structure.atomtypes.append(self.solute_element)
        structure.natoms = np.array([structure.natoms.tolist()[0]-1, 1])
        structure.gen_atominfo()

        # Set title as the composition
        title = ''.join(['{}{}'.format(e, n) for e, n in zip(
                structure.atomtypes, structure.natoms)])
        structure.title = title

    @property
    def defect_structure(self):
        """Solvent supercell with a single solute atom."""
        defect = copy.deepcopy(self.supercell_for_mixing)
        self.replace_solvent_atom_with_solute(defect)
        return defect


class MixingDefectSetError(Exception):
    """Base class for handling errors associated with a set of dilute mixing defects."""
    pass


class MixingDefectSet(object):
    """Class to represent a set of dilute substitutional (point-)defects."""

    def __init__(self, solvent_element=None, solvent_reference_structure=None,
                 solute_elements=None, solute_reference_structures=None,
                 min_image_dist=None, supercell_for_mixing=None, **kwargs):
        """

        Args:

            solvent_element: String with the symbol of the solvent element.

            solvent_reference_structure: Reference crystal structure of the solvent as a
                `citrine_dft.atoms.Structure` object.

            solute_elements: List of String objects each representing the symbol of a
                solute element. A comma-delimited String of atomic symbols is also acceptable.
                For example, ["Al", "Ca", "Sr", "O"] and "Al,Ca,Sr,O" are equivalent.

            solute_reference_structures: Dictionary of solute elements (String) and the
                corresponding structures (`citrine_dft.atoms.Structure`).

            min_image_dist: Floating point number representing the minimum distance between
                periodic images of the defect in a supercell, in Angstrom. Defaults to 15.

            supercell_for_mixing (:obj:`atoms.Structure`):
                Supercell structure to use for creating a dilute mixing defect.

            kwargs: Other keyword arguments.

        """
        self._solvent_element = None
        self.solvent_element = solvent_element

        self._solvent_reference_structure = None
        self.solvent_reference_structure = solvent_reference_structure

        self._solute_elements = None
        self.solute_elements = solute_elements

        self._solute_reference_structures = None
        self.solute_reference_structures = solute_reference_structures

        self._min_image_dist = None
        self.min_image_dist = min_image_dist

        self._supercell_for_mixing = None
        self.supercell_for_mixing = supercell_for_mixing

        self._mixing_defects = None
        self._set_mixing_defects()

    @property
    def solvent_element(self):
        """String specifying the atomic symbol of the solvent element."""
        return self._solvent_element

    @solvent_element.setter
    def solvent_element(self, solvent_element):
        _validate_input_element(solvent_element)
        self._solvent_element = solvent_element

    @property
    def solvent_reference_structure(self):
        """`citrine_dft.atoms.Structure` object of the reference structure of the solvent."""
        return self._solvent_reference_structure

    @solvent_reference_structure.setter
    def solvent_reference_structure(self, solvent_reference_structure):
        if solvent_reference_structure is None:
            error_msg = 'Solvent reference structure (required) is not provided'
            raise MixingDefectError(error_msg)

        _validate_input_structure(solvent_reference_structure)
        if not _structure_has_element(solvent_reference_structure, self.solvent_element):
            error_msg = 'Input solvent reference structure {}'.format(solvent_reference_structure)
            error_msg += ' does not contain solvent element {}'.format(self.solvent_element)
            raise MixingDefectSetError(error_msg)
        self._solvent_reference_structure = solvent_reference_structure

    @property
    def solute_elements(self):
        """List with Strings specifying the atomic symbol of each solvent element."""
        return self._solute_elements

    @solute_elements.setter
    def solute_elements(self, solute_elements):
        if self.solute_elements is not None:
            error_msg = 'Use `add_solute_to_defects_set()`, `remove_solute_from_defects_set()`'
            error_msg += ' to modify the list of solute elements'
            raise MixingDefectSetError(error_msg)

        if solute_elements is None:
            self._solute_elements = []
            return

        if isinstance(solute_elements, six.string_types):
            elements_set = set([e.strip() for e in solute_elements.split(',')])
        else:
            elements_set = set(solute_elements)

        if self.solvent_element in elements_set:
            elements_set.remove(self.solvent_element)

        for element in elements_set:
            _validate_input_element(element)

        self._solute_elements = sorted(list(elements_set))

    @property
    def solute_reference_structures(self):
        """Dictionary of solute elements (String) and the corresponding reference structure
        (`citrine_dft.atoms.Structure`)."""
        return self._solute_reference_structures

    @solute_reference_structures.setter
    def solute_reference_structures(self, solute_reference_structures):
        if self.solute_reference_structures is not None:
            error_msg = 'Use `add_solute_to_defects_set()`, `remove_solute_from_defects_set()`'
            error_msg += ' to modify the set of solute reference structures'
            raise MixingDefectSetError(error_msg)

        self._solute_reference_structures = dict([(e, None) for e in self.solute_elements])

        if solute_reference_structures is None:
            return

        try:
            for element, structure in solute_reference_structures.items():
                _validate_input_element(element)
                if structure is not None:
                    _validate_input_structure(structure)
                self._solute_reference_structures.update({element: structure})
        except AttributeError:
            error_msg = 'Input `solute_reference_structures` should be a dictionary'
            raise MixingDefectSetError(error_msg)

    @property
    def min_image_dist(self):
        """Floating point number with the minimum distance between periodic defect images in a
        supercell, in Angstrom."""
        return self._min_image_dist

    @min_image_dist.setter
    def min_image_dist(self, min_image_dist):
        if self.min_image_dist is not None:
            error_msg = 'Cannot set minimum image distance after initial setup'
            raise MixingDefectSetError(error_msg)

        if min_image_dist is None:
            sys.stdout.write('Minimum image distance not provided. Using defaults.\n')
            self._min_image_dist = 15.0
            return
        try:
            self._min_image_dist = float(min_image_dist)
        except ValueError:
            sys.stdout.write('Invalid input for `min_image_dist`: {}.'.format(min_image_dist))
            sys.stdout.write(' Using defaults.\n')
            self._min_image_dist = 15.0

    @property
    def supercell_for_mixing(self):
        """Solvent supercell to use for creating a dilute mixing defect."""
        return self._supercell_for_mixing

    @supercell_for_mixing.setter
    def supercell_for_mixing(self, supercell_for_mixing):
        if supercell_for_mixing is None:
            self._supercell_for_mixing = supercell.get_supercell_for_mixing(
                    structure=self.solvent_reference_structure,
                    min_image_dist=self.min_image_dist,
            )
            return

        _validate_input_structure(supercell_for_mixing)
        if not _structure_has_element(supercell_for_mixing,
                                      self.solvent_element):
            error_msg = 'Defect supercell does not contain solvent element'
            raise MixingDefectError(error_msg)
        self._supercell_for_mixing = supercell_for_mixing

    @property
    def mixing_defects(self):
        """Dictionary of solute elements (String) and the corresponding `MixingDefect` objects."""
        return self._mixing_defects

    def _set_mixing_defects(self):
        self._mixing_defects = {}
        for element in self.solute_elements:
            self._mixing_defects[element] = MixingDefect(
                    solvent_element=self.solvent_element,
                    solvent_reference_structure=self.solvent_reference_structure,
                    solute_element=element,
                    solute_reference_structure=self.solute_reference_structures.get(element, None),
                    min_image_dist=self.min_image_dist,
                    supercell_for_mixing=self.supercell_for_mixing,
            )

    def add_solute_to_defects_set(self, solute_element, solute_reference_structure=None):
        """Adds a solute to the set of defects `mixing_defects` if not in it already.

        Args:
            solute_element: String representing the atomic symbol of the solute element to be added.

            solute_reference_structure: Reference structure of the solute as a
                `citrine_dft.atoms.Structure` object.

        Raises:
            MixingSetError if solute already present in `mixing_defects`.

        """
        if solute_element in self.mixing_defects:
            error_msg = 'Solute {} already present in the defects set.'.format(solute_element)
            error_msg += ' Remove it using `remove_solute_from_defects_set()` first'
            raise MixingDefectSetError(error_msg)

        if solute_element == self.solvent_element:
            error_msg = 'Solute specified is same as solvent'
            raise MixingDefectSetError(error_msg)

        self._mixing_defects[solute_element] = MixingDefect(
            solvent_element=self.solvent_element,
            solvent_reference_structure=self.solvent_reference_structure,
            solute_element=solute_element,
            solute_reference_structure=solute_reference_structure,
            min_image_dist=self.min_image_dist)

        self._solute_reference_structures.update({solute_element: solute_reference_structure})
        self._solute_elements = sorted(self._mixing_defects.keys())

    def remove_solute_from_defects_set(self, solute_element):
        """Removes a solute from the set of mixing defects, if present.

        Args:
            solute_element: String representing the atomic symbol of the solute to be removed.

        """
        if solute_element not in self._mixing_defects:
            error_msg = 'Solute to be removed, {}, is not in the defects set'.format(solute_element)
            raise MixingDefectSetError(error_msg)

        self._mixing_defects.pop(solute_element)
        self._solute_reference_structures.pop(solute_element)
        self._solute_elements = sorted(self._mixing_defects.keys())
