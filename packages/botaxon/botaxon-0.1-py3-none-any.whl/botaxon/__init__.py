# -*- coding: utf-8 -*-

from collections import deque, namedtuple

__VERSION__ = "0.1"
DEFAULT_HYBRID_MARKER = "×"


class InvalidSpeciesError(Exception):
    pass


class InvalidSubTaxonError(Exception):
    pass


class InvalidVerbatimRankError(Exception):
    pass


class SubTaxonMixin(object):

    @property
    def verbatim_rank(self):
        raise NotImplementedError()

    @property
    def name(self):
        return "{self.species.name} {self.verbatim_rank} " \
               "{self.epithet}".format(self=self)


_GenusResult = namedtuple("Genus", "epithet is_hybrid")
_SpeciesResult = namedtuple("Species", "genus epithet is_hybrid")
_SubSpeciesResult = namedtuple("SubSpecies", "species epithet")
_VarietyResult = namedtuple("Variety", "species epithet")
_SubVarietyResult = namedtuple("SubVariety", "species epithet")
_FormResult = namedtuple("Form", "species epithet")
_SubFormResult = namedtuple("SubForm", "species epithet")


class GenusResult(_GenusResult):

    @property
    def name(self):
        name_prefix = str()
        if self.is_hybrid:
            name_prefix = "{} ".format(DEFAULT_HYBRID_MARKER)
        return name_prefix + self.epithet


class SpeciesResult(_SpeciesResult):

    @property
    def name(self):
        name_prefix = str()
        if self.is_hybrid:
            name_prefix = "{} ".format(DEFAULT_HYBRID_MARKER)
        return "{self.genus.name} {prefix}{self.epithet}".format(
            self=self, prefix=name_prefix)


class SubSpeciesResult(_SubSpeciesResult, SubTaxonMixin):

    @property
    def verbatim_rank(self):
        return "subsp."


class VarietyResult(_VarietyResult, SubTaxonMixin):

    @property
    def verbatim_rank(self):
        return "var."


class SubVarietyResult(_SubVarietyResult, SubTaxonMixin):

    @property
    def verbatim_rank(self):
        return "subvar."


class FormResult(_FormResult, SubTaxonMixin):

    @property
    def verbatim_rank(self):
        return "f."


class SubFormResult(_SubFormResult, SubTaxonMixin):

    @property
    def verbatim_rank(self):
        return "subf."


VERBATIM_RANKS = {
    "subsp.": SubSpeciesResult,
    "var.": VarietyResult,
    "subvar.": SubVarietyResult,
    "f.": FormResult,
    "subf.": SubFormResult
}


def load(scientific_name, hybrid_marker=DEFAULT_HYBRID_MARKER):

    if isinstance(scientific_name, str):
        scientific_name = scientific_name.split()

    scientific_name = deque(map(str, scientific_name))

    genus_name_or_hybrid_marker = scientific_name.popleft()
    if genus_name_or_hybrid_marker == hybrid_marker:
        genus_is_hybrid = True
        genus_name = scientific_name.popleft()
    else:
        genus_is_hybrid = False
        genus_name = genus_name_or_hybrid_marker

    genus = GenusResult(genus_name, genus_is_hybrid)

    if not scientific_name:
        return genus

    species_name_or_hybrid_marker = scientific_name.popleft()
    if species_name_or_hybrid_marker == hybrid_marker:
        species_is_hybrid = True
        species_name = scientific_name.popleft()
    else:
        species_is_hybrid = False
        species_name = species_name_or_hybrid_marker

    species = SpeciesResult(genus, species_name, species_is_hybrid)

    if not scientific_name:
        return species

    verbatim_rank_or_species_name_leftover = scientific_name.popleft()
    if verbatim_rank_or_species_name_leftover in VERBATIM_RANKS.keys():
        infraspecific_rank = verbatim_rank_or_species_name_leftover

        if not scientific_name:
            raise InvalidSubTaxonError(
                "species must be followed by an epithet")

        infraspecific_epithet = " ".join(scientific_name)
        subtaxon_cls = VERBATIM_RANKS.get(infraspecific_rank)

        if not subtaxon_cls:
            raise InvalidVerbatimRankError()

        return subtaxon_cls(species, infraspecific_epithet)

    species_name = "{} {}".format(
        species_name, verbatim_rank_or_species_name_leftover)

    if scientific_name:
        raise InvalidSpeciesError("got leftovers: {}".format(scientific_name))

    if hybrid_marker in species_name:
        raise InvalidSpeciesError()

    return SpeciesResult(genus, species_name, species_is_hybrid)
