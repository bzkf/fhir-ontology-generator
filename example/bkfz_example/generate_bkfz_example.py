from __future__ import annotations

import argparse
import copy
import json
from typing import List, ValuesView, Dict

from FHIRProfileConfiguration import *
from core.CQLMappingGenerator import CQLMappingGenerator
from core.FHIRSearchMappingGenerator import FHIRSearchMappingGenerator
from core.ResourceQueryingMetaDataResolver import ResourceQueryingMetaDataResolver
from core.StrucutureDefinitionParser import get_element_from_snapshot
from core.UIProfileGenerator import UIProfileGenerator
from core.UITreeGenerator import UITreeGenerator
from helper import download_simplifier_packages, generate_snapshots, write_object_as_json, load_querying_meta_data, \
    generate_result_folder
from model.MappingDataModel import CQLMapping, FhirMapping, MapEntryList
from model.ResourceQueryingMetaData import ResourceQueryingMetaData
from model.UIProfileModel import UIProfile
from model.UiDataModel import TermEntry, TermCode

WINDOWS_RESERVED_CHARACTERS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

core_data_sets = [DKTK]


class BKFZDataSetQueryingMetaDataResolver(ResourceQueryingMetaDataResolver):
    def __init__(self):
        super().__init__()

    def get_query_meta_data(self, fhir_profile_snapshot: dict, _context: TermCode) -> List[ResourceQueryingMetaData]:
        """
        Implementation as simple look up table.
        :param fhir_profile_snapshot:
        :param _context:
        :return: List of ResourceQueryingMetaData
        """
        result = []
        key = fhir_profile_snapshot.get("name")
        mapping = self._get_query_meta_data_mapping()
        for value in mapping[key]:
            with open(f"resources/QueryingMetaData/{value}QueryingMetaData.json", "r") as file:
                result.append(ResourceQueryingMetaData.from_json(file))
        return result

    @staticmethod
    def _get_query_meta_data_mapping():
        with open("resources/profile_to_query_meta_data_resolver_mapping.json", "r") as f:
            return json.load(f)


def generate_term_code_mapping(_entries: List[TermEntry]):
    """
    Generates the term code mapping for the given entries and saves it in the mapping folder
    :param _entries: TermEntries to generate the mapping for
    """
    pass


def generate_term_code_tree(_entries: List[TermEntry]):
    """
    Generates the term code tree for the given entries and saves it in the mapping folder
    :param _entries:
    :return:
    """
    pass


def validate_ui_profile(_profile_name: str):
    """
    Validates the ui profile with the given name against the ui profile schema
    :param _profile_name: name of the ui profile
    :raises: jsonschema.exceptions.ValidationError if the ui profile is not valid
             jsonschema.exceptions.SchemaError if the ui profile schema is not valid
    """
    pass
    # f = open("ui-profiles/" + profile_name + ".json", 'r')
    # validate(instance=json.load(f), schema=json.load(open("resources/schema/ui-profile-schema.json")))


def write_ui_trees_to_files(trees: List[TermEntry], directory: str = "ui-trees"):
    """
    Writes the ui trees to the ui-profiles folder
    :param trees: ui trees to write
    :param directory: directory to write the ui trees to
    """
    for tree in trees:
        print(tree.display)
        write_object_as_json(tree, f"{directory}/{tree.display}.json")


# Todo: this should be an abstract method that has to be implemented for each use-case
# Todo: move this concrete implementation elsewhere


def write_cds_ui_profile(module_category_entry):
    """
    Writes the ui profile for the given module category entry to the ui-profiles folder
    :param module_category_entry: name of the module category entry
    """
    f = open("ui-profiles/" + module_category_entry.display + ".json", 'w', encoding="utf-8")
    if len(module_category_entry.children) == 1:
        f.write(module_category_entry.children[0].to_json())
    else:
        f.write(module_category_entry.to_json())
    f.close()


def denormalize_ui_profile_to_old_format(ui_tree: List[TermEntry], term_code_to_profile_name: Dict[TermCode, str],
                                         ui_profile_name_to_profile: Dict[str, UIProfile]):
    """
    Denormalizes the ui tree and ui profiles to the old format

    :param ui_tree: entries to denormalize
    :param term_code_to_profile_name: mapping from term codes to profile names
    :param ui_profile_name_to_profile: ui profiles to use
    :return: denormalized entries
    """
    for entry in ui_tree:
        if entry.selectable:
            try:
                ui_profile = ui_profile_name_to_profile[term_code_to_profile_name[entry.termCode]]
                entry.to_v1_entry(ui_profile)
            except KeyError:
                print("No profile found for term code " + entry.termCode.code)
        for child in entry.children:
            denormalize_ui_profile_to_old_format([child], term_code_to_profile_name, ui_profile_name_to_profile)


def denormalize_mapping_to_old_format(term_code_to_mapping_name, mapping_name_to_mapping):
    """
    Denormalizes the mapping to the old format

    :param term_code_to_mapping_name: mapping from term codes to mapping names
    :param mapping_name_to_mapping: mappings to use
    :return: denormalized entries
    """
    result = MapEntryList()
    for context_and_term_code, mapping_name in term_code_to_mapping_name.items():
        try:
            mapping = copy.copy(mapping_name_to_mapping[mapping_name])
            mapping.key = context_and_term_code[1]
            result.entries.add(mapping)
        except KeyError:
            print("No mapping found for term code " + context_and_term_code[1].code)
    return result


def move_back_other(entries):
    """
    Entries are sorted alphabetically. This method moves the entries that express "Other" to the end of the list
    :param entries: list of entries
    """
    entries_copy = entries.copy()
    for entry in entries_copy:
        for other_naming in ["Sonstige", "sonstige", "andere", "Andere", "Weitere", "Other"]:
            if entry.termCode.display.startswith(other_naming):
                entries.remove(entry)
                entries.append(entry)
        if entry.children:
            move_back_other(entry.children)


def configure_args_parser():
    """
    Configures the argument parser
    :return: the configured argument parser
    """
    arg_parser = argparse.ArgumentParser(description='Generate the UI-Profile of the core data set for the MII-FDPG')
    arg_parser.add_argument('--download_packages', action='store_true')
    arg_parser.add_argument('--generate_snapshot', action='store_true')
    arg_parser.add_argument('--generate_csv', action='store_true')
    arg_parser.add_argument('--generate_ui_trees', action='store_true')
    arg_parser.add_argument('--generate_ui_profiles', action='store_true')
    arg_parser.add_argument('--generate_mapping', action='store_true')
    arg_parser.add_argument('--generate_old_format', action='store_true')
    return arg_parser


def remove_reserved_characters(file_name):
    return file_name.translate({ord(c): None for c in WINDOWS_RESERVED_CHARACTERS})


def write_ui_profiles_to_files(profiles: List[UIProfile] | ValuesView[UIProfile], folder: str = "ui-profiles"):
    for profile in profiles:
        with open(
                folder + "/" + remove_reserved_characters(profile.name).replace(" ", "_").replace(".", "_") + ".json",
                'w', encoding="utf-8") as f:
            f.write(profile.to_json())
    f.close()


def write_mappings_to_files(mappings, mapping_folder="mapping"):
    for mapping in mappings:
        if isinstance(mapping, CQLMapping):
            mapping_dir = f"{mapping_folder}/cql/"
        elif isinstance(mapping, FhirMapping):
            mapping_dir = f"{mapping_folder}/fhir/"
        else:
            raise ValueError("Mapping type not supported" + str(type(mapping)))
        with open(mapping_dir + mapping.name + ".json", 'w', encoding="utf-8") as f:
            f.write(mapping.to_json())
    f.close()


def write_v1_mapping_to_file(mapping, mapping_folder="mapping-old"):
    if isinstance(mapping.entries[0], CQLMapping):
        mapping_file = f"{mapping_folder}/cql/mapping_cql.json"
    elif isinstance(mapping.entries[0], FhirMapping):
        mapping_file = f"{mapping_folder}/fhir/mapping_fhir.json"
    else:
        raise ValueError("Mapping type not supported" + str(type(mapping)))
    with open(mapping_file, 'w', encoding="utf-8") as f:
        f.write(mapping.to_json())
    f.close()


if __name__ == '__main__':

    parser = configure_args_parser()
    args = parser.parse_args()

    generate_result_folder()

    # Download the packages
    if args.download_packages:
        download_simplifier_packages(core_data_sets)
    # ----Time consuming: Only execute initially or on changes----
    if args.generate_snapshot:
        # generate_snapshots("resources/core_data_sets")
        generate_snapshots("resources/bkfz_differential", core_data_sets)
    # -------------------------------------------------------------

    # You shouldn't need different implementations for the different generators
    resolver = BKFZDataSetQueryingMetaDataResolver()

    if args.generate_ui_trees:
        tree_generator = UITreeGenerator(resolver)
        ui_trees = tree_generator.generate_ui_trees("resources/bkfz_differential")
        # replace ui tree for loinc with the top 300 loinc tree
        write_ui_trees_to_files(ui_trees)

    if args.generate_ui_profiles:
        profile_generator = UIProfileGenerator(resolver)
        ui_profiles = profile_generator.generate_ui_profiles("resources/bkfz_differential")[1].values()
        write_ui_profiles_to_files(ui_profiles)

    if args.generate_mapping:
        cql_generator = CQLMappingGenerator(resolver)
        cql_mappings = cql_generator.generate_mapping("resources/bkfz_differential")
        cql_term_code_mappings = cql_mappings[0]
        cql_concept_mappings = cql_mappings[1]
        write_mappings_to_files(cql_concept_mappings.values())
        v1_cql_mappings = denormalize_mapping_to_old_format(cql_term_code_mappings, cql_concept_mappings)
        write_v1_mapping_to_file(v1_cql_mappings, "mapping-old")

        fhir_search_generator = FHIRSearchMappingGenerator(resolver)
        fhir_search_mappings = fhir_search_generator.generate_mapping("resources/bkfz_differential")
        fhir_search_term_code_mappings = fhir_search_mappings[0]
        fhir_search_concept_mappings = fhir_search_mappings[1]
        write_mappings_to_files(fhir_search_concept_mappings.values())
        v1_fhir_search_mapping = denormalize_mapping_to_old_format(fhir_search_term_code_mappings,
                                                                   fhir_search_concept_mappings)
        write_v1_mapping_to_file(v1_fhir_search_mapping, "mapping-old")

    if args.generate_old_format:
        tree_generator = UITreeGenerator(resolver)
        ui_trees = tree_generator.generate_ui_trees("resources/bkfz_differential")
        profile_generator = UIProfileGenerator(resolver)
        ui_profiles = profile_generator.generate_ui_profiles("resources/bkfz_differential")
        term_code_to_ui_profile_name = {context_tc[1]: profile_name for context_tc, profile_name in
                                        ui_profiles[0].items()}
        print("denormalizing ui trees to old format")
        denormalize_ui_profile_to_old_format(ui_trees, term_code_to_ui_profile_name, ui_profiles[1])
        print("writing ui trees to files")
        write_ui_trees_to_files(ui_trees, "ui-profiles-old")

    # core_data_category_entries = generate_core_data_set()
    #
    # for core_data_category_entry in core_data_category_entries:
    #     write_cds_ui_profile(core_data_category_entry)
    #     validate_ui_profile(core_data_category_entry.display)

    # move_back_other(category_entries)
    #
    # category_entries += core_data_category_entries
    # dbw = DataBaseWriter()
    # dbw.add_ui_profiles_to_db(category_entries)
    # generate_term_code_mapping(category_entries)
    # generate_term_code_tree(category_entries)
    # if args.generate_csv:
    #     to_csv(category_entries)

    # dump data from db with
    # docker exec -t 7ac5bfb77395 pg_dump --dbname="codex_ui" --username=codex-postgres
    # --table=UI_PROFILE_TABLE > ui_profile_dump_230822
