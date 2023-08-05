from janis.utils.janisconstants import GITHUB_URL
from janis.translations.exportpath import ExportPathKeywords
from . import cwl, wdl
from .wdl import dump_wdl as wdl_dump_workflow

SupportedTranslation = str


class SupportedTranslations:
    CWL: SupportedTranslation = "cwl"
    WDL: SupportedTranslation = "wdl"


def translate_workflow(workflow, translation: SupportedTranslation,
                       to_console=True, with_docker=True, with_resource_overrides=False, to_disk=False,
                       export_path=ExportPathKeywords.default, write_inputs_file=False, should_validate=False,
                       should_zip=True):
    if translation == SupportedTranslations.CWL:
        return cwl.dump_cwl(workflow, to_console=to_console, with_docker=with_docker,
                            with_resource_overrides=with_resource_overrides, to_disk=to_disk,
                            export_path=export_path, write_inputs_file=write_inputs_file,
                            should_validate=should_validate, should_zip=should_zip)

    elif translation == SupportedTranslations.WDL:
        return wdl.dump_wdl(workflow, to_console=to_console, with_docker=with_docker,
                            with_resource_overrides=with_resource_overrides, to_disk=to_disk,
                            export_path=export_path, write_inputs_file=write_inputs_file,
                            should_validate=should_validate, should_zip=should_zip)

    else:
        raise NotImplementedError(f"The requested translation ('{translation}') has not been implemented yet, "
                                  f"why not contribute one at '{GITHUB_URL}'.")


def translate_tool(tool, translation: SupportedTranslation, with_docker, with_resource_overrides=False):
    if translation == SupportedTranslations.CWL:
        return cwl.translate_tool_str(tool, with_docker=with_docker, with_resource_overrides=with_resource_overrides)

    elif translation == SupportedTranslations.WDL:
        return wdl.translate_tool_str(tool, with_docker=with_docker)

    else:
        raise NotImplementedError(f"The requested translation ('{translation}') has not been implemented yet, "
                                  f"why not contribute one at '{GITHUB_URL}'.")


def build_resources_input(workflow, translation: SupportedTranslation, hints):
    if translation == SupportedTranslations.CWL:
        return cwl.build_cwl_resource_inputs_dict(workflow, hints)

    elif translation == SupportedTranslations.WDL:
        return wdl.build_wdl_resource_inputs_dict(workflow, hints)

    else:
        raise NotImplementedError(f"The requested translation ('{translation}') has not been implemented yet, "
                                  f"why not contribute one at '{GITHUB_URL}'.")
