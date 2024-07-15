# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import json
import logging
import shutil
import tarfile
from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.templates.device_template.device_template import DeviceTemplate, GeneralTemplate
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.templates import DeviceTemplateInformation, FeatureTemplateInformation
from catalystwan.session import ManagerSession
from catalystwan.typed_list import DataSequence

logger = logging.getLogger(__name__)


# ---------------------- HELPERS ---------------------- #


FEATURE_TEMPLATE_KEYS = [
    "templateName",
    "templateDescription",
    "templateType",
    "templateMinVersion",
    "deviceType",
    "factoryDefault",
    "templateDefinition",
]
DEVICE_TEMPLATE_KEYS = [
    "templateName",
    "templateDescription",
    "deviceType",
    "configType",
    "factoryDefault",
    "policyId",
    "featureTemplateUidRange",
    "generalTemplates",
]
POLICY_KEYS = ["policyName", "policyDescription", "policyDefinition", "policyType"]


class TemplatesJsonNames(Enum):
    DEVICE_TEMPLATES = "device_templates.json"
    FEAUTRE_TEMPLATES = "feature_templates.json"
    POLICIES = "policies.json"
    TEMPLATES_ARCHIVE = "templates_archive.tar.gz"


class DeviceTemplatesList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    templates: List[DeviceTemplate]


class FeatureTemplatesDict(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    feature_templates_definitions: Dict = Field(default={})


class PoiciesDict(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    policies_definitions: Dict = Field(default={})


# ---------------------- EXPORT TEMPLATES ---------------------- #


def write_json_to_file(data: BaseModel, file_path: Path):
    """Writes JSON representation of a Pydantic model to a file."""
    try:
        with file_path.open("w") as f:
            f.write(data.model_dump_json(indent=4, by_alias=True))
    except IOError as e:
        logger.error(f"Failed to write to {file_path}: {e}")
        raise e


def create_tar_archive(source_dir: Path, archive_path: Path):
    """Creates a tar.gz archive of the specified directory."""
    with tarfile.open(archive_path, "w:gz") as tar:
        for file_name in source_dir.glob("*"):
            tar.add(file_name, arcname=file_name.name)


def prepare_directory_for_templates(templates_directory: Path, force_existing_dir_removal: bool) -> bool:
    """Prepares a directory for storing templates, optionally removing existing content.

    Args:
        templates_directory: The path to the directory to prepare.
        force_existing_dir_removal: If True, any existing directory will be removed.

    Returns:
        bool: True if the directory was successfully prepared, False otherwise.

    Raises:
        PermissionError, OSError: If there is an error removing or creating the directory.
    """
    if templates_directory.exists():
        logger.info(f"The directory {templates_directory} already exists.")
        if force_existing_dir_removal:
            try:
                for child in templates_directory.iterdir():
                    if child.is_file():
                        child.unlink()
                    elif child.is_dir():
                        child.rmdir()
                templates_directory.rmdir()
                logger.info(f"Removed existing directory {templates_directory}.")
            except (PermissionError, OSError) as ex:
                logger.error(f"An error occurred while removing the directory: {ex}")
                raise ex
        else:
            logger.warning(f"Directory with name: {templates_directory} already exists and will not be overwritten.")
            return False
    try:
        templates_directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created at {templates_directory}")
        return True
    except (PermissionError, OSError) as ex:
        logger.error(f"Exception while creating directory: {ex}")
        raise ex


def extract_template_ids(template: GeneralTemplate) -> Set[str]:
    """Recursively extracts template IDs from a GeneralTemplate and its sub-templates."""
    template_ids = {template.template_id}
    for sub_template in getattr(template, "sub_templates", []):
        template_ids.update(extract_template_ids(sub_template))
    return template_ids


def export_device_templates(
    session: ManagerSession, device_template_list: DataSequence[DeviceTemplateInformation], templates_directory: Path
) -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    """Exports device templates to JSON files and returns related feature and policy IDs.

    Args:
        session: The session object to interact with the API.
        device_template_list: A sequence of DeviceTemplateInformation instances to be exported.
        templates_directory: The directory where the JSON files will be written.

    Returns:
        Tuple[Dict[str, Set[str]], Dict[str, str]]: A tuple containing two dictionaries,
        one mapping device template names to sets of feature IDs, and the other mapping
        device template names to policy IDs.
    """
    device_templates = DataSequence(DeviceTemplate)
    device_feature_id: Dict[str, Set[str]] = {}
    device_policy_id: Dict[str, str] = {}

    for device_template_info in device_template_list:
        device_template: DeviceTemplate = DeviceTemplate.get(name=device_template_info.name, session=session)

        if device_template.policy_id:
            device_policy_id[device_template_info.name] = device_template.policy_id

        device_feature_id[device_template_info.name] = set()

        for feature in device_template.general_templates:
            device_feature_id[device_template_info.name].update(extract_template_ids(feature))

        if device_template.feature_template_uid_range:
            for additional_template in device_template.feature_template_uid_range:
                device_feature_id[device_template_info.name].update(additional_template["templateId"])

        device_templates.append(device_template)

    device_templates_as_pydantic = DeviceTemplatesList(templates=[template for template in device_templates])

    file_path = Path(templates_directory / TemplatesJsonNames.DEVICE_TEMPLATES.value)
    write_json_to_file(device_templates_as_pydantic, file_path)

    logger.info(f"Successfully written {len(device_templates)} Device Template(s) definitions to files.")
    return device_feature_id, device_policy_id


def export_feature_templates(
    session: ManagerSession, device_feature_id: Dict[str, Set[str]], templates_directory: Path
) -> None:
    """Exports feature templates to a JSON file."""
    feature_template_dict = FeatureTemplatesDict()
    feature_template_json_file = Path(templates_directory / TemplatesJsonNames.FEAUTRE_TEMPLATES.value)

    for template_id_list in device_feature_id.values():
        for template_id in template_id_list:
            feature_data: DataSequence[
                FeatureTemplateInformation
            ] = session.endpoints.configuration_general_template.get_template_definition(
                template_id=template_id
            ).single_or_default()
            feature_template_dict.feature_templates_definitions[template_id] = feature_data

    write_json_to_file(feature_template_dict, feature_template_json_file)
    number_of_templates = len(feature_template_dict.feature_templates_definitions)
    logger.info(f"Successfully written {number_of_templates} Feature Templates definitions.")


def export_policy_templates(
    session: ManagerSession, device_policy_id_dict: Dict[str, str], templates_directory: Path
) -> None:
    """Exports policy templates to a JSON file."""
    policy_template_json_file = Path(templates_directory / TemplatesJsonNames.POLICIES.value)

    existing_policies = session.api.policy.localized._endpoints.generate_policy_template_list()
    policies_dict = PoiciesDict()

    for policy_id in device_policy_id_dict.values():
        for policy in existing_policies:
            if policy_id == str(policy.policy_id):
                policies_dict.policies_definitions[policy_id] = policy
    write_json_to_file(policies_dict, policy_template_json_file)


def export_templates(
    session: ManagerSession,
    templates_directory: Path = Path.home() / "default_templates",
    force_existing_dir_removal: bool = False,
    filters: dict = {},
):
    """Main function to export all templates and create an archive.

    Args:
        session: The session object to interact with the API.
        templates_directory: The directory where the templates and archive will be stored.
        force_existing_dir_removal: If True, the existing templates directory will be removed.
        filter: A dictionary of filters to apply when retrieving Device Templates
    """
    dir_ready = prepare_directory_for_templates(
        templates_directory=templates_directory, force_existing_dir_removal=force_existing_dir_removal
    )

    if dir_ready:
        device_templates_list: DataSequence[
            DeviceTemplateInformation
        ] = session.endpoints.configuration_template_master.get_device_template_list().filter(
            config_type="template", **filters
        )

        device_feature_id, device_policy_id = export_device_templates(
            session, device_templates_list, templates_directory
        )
        export_feature_templates(session, device_feature_id, templates_directory)
        export_policy_templates(session, device_policy_id, templates_directory)

        templates_archive_path = Path(templates_directory / TemplatesJsonNames.TEMPLATES_ARCHIVE.value)
        create_tar_archive(templates_directory, templates_archive_path)


# ---------------------- IMPORT TEMPLATES ---------------------- #


def extract_tar_with_templates_to_path(templates_directory: Path, dest_dir_path: Path) -> None:
    if dest_dir_path.exists():
        shutil.rmtree(dest_dir_path)
    dest_dir_path.mkdir(parents=True)
    templates_archive_path = Path(templates_directory / TemplatesJsonNames.TEMPLATES_ARCHIVE.value)
    try:
        with tarfile.open(templates_archive_path) as tar:
            tar.extractall(path=dest_dir_path)
    except tarfile.TarError as e:
        logger.error(f"An error occurred while extracting the tar file: {e}")
        raise


def load_json_from_file(file_path: Union[str, Path]):
    with open(file_path, "r") as file:
        return json.load(file)


def get_feature_template_name_to_id_map(session: ManagerSession) -> Dict[str, str]:
    """Retrieves a mapping of feature template names to their IDs."""
    feature_data = session.endpoints.configuration_general_template.get_feature_template_list()
    return {feature.name: feature.id for feature in feature_data} if feature_data else {}


def check_device_template_exists(session: ManagerSession, device_template_name: str) -> bool:
    device_data: DataSequence[
        DeviceTemplateInformation
    ] = session.endpoints.configuration_template_master.get_device_template_list()
    return any(device_template_name == device.name for device in device_data)


def check_policy_exists(session: ManagerSession, policy_name: str) -> Union[str, bool]:
    """Checks if a policy with the given name exists and returns its ID."""
    policy_data = session.endpoints.configuration.policy.vedge_template.generate_policy_template_list()
    policy = next((p for p in policy_data if p.policy_name == policy_name), None)
    return policy.policy_id if policy else False


def clean_dict(data: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
    """Prepare Dictionary so it can be used as JSON Payload."""
    return {k: v for k, v in data.items() if k in allowed_keys}


def update_template_ids(template: Dict[str, Any], template_id_mapping: Dict[str, str]) -> None:
    """Updates the template IDs in a template dictionary."""
    for key in ["generalTemplates", "featureTemplateUidRange"]:
        for item in template.get(key, []):
            item["templateId"] = template_id_mapping.get(item["templateId"], item["templateId"])
            for sub_key in ["subTemplates"]:
                for sub_item in item.get(sub_key, []):
                    sub_item["templateId"] = template_id_mapping.get(sub_item["templateId"], sub_item["templateId"])


def process_feature_templates(
    session: ManagerSession, feature_template_data, feature_template_name_to_id_map: Dict[str, str]
) -> Dict[str, str]:
    """Processes feature templates and creates new ones if they do not exist.

    Args:
        session: The session object to interact with the API.
        feature_template_data: The feature template data to process.
        feature_template_name_to_id_map: A mapping of feature template names to IDs.

    Returns:
        A dictionary mapping existing template IDs to new template IDs.

    Raises:
        ManagerHTTPError: If there is an error creating the feature templates.
    """

    template_id_mapping = {}

    for template_id, feature_data in feature_template_data["feature_templates_definitions"].items():
        template_definition = clean_dict(feature_data, FEATURE_TEMPLATE_KEYS)
        if template_definition["templateName"] in feature_template_name_to_id_map:
            new_template_id = feature_template_name_to_id_map[template_definition["templateName"]]
            logger.info(f"Skipping Feature Template: {template_definition['templateName']}")
        else:
            try:
                endpoint = "/dataservice/template/feature"
                response = session.post(endpoint, json=template_definition)
                new_template_id = response.json()["templateId"] if response else None
                logger.info(f"Created Feature Template: {template_definition['templateName']}")
            except ManagerHTTPError as ex:
                logger.error(
                    f"Could not create Feature Template {template_definition['templateName']}."
                    "\nManager error: {ex.info}"
                )
                raise ex
        template_id_mapping[template_id] = new_template_id

    return template_id_mapping


def process_device_template(
    session: ManagerSession, device_template: Dict[str, Any], template_id_mapping: Dict[str, str]
) -> None:
    """Processes a device template and creates it if it does not exist.

    Args:
        session: The session object to interact with the API.
        device_template: The device template data to process.
        template_id_mapping: A dictionary mapping old template IDs to new ones.

    Raises:
        ManagerHTTPError: If there is an error creating the device template.
    """
    new_device_template = deepcopy(device_template)
    update_template_ids(new_device_template, template_id_mapping)

    new_device_template = clean_dict(new_device_template, DEVICE_TEMPLATE_KEYS)

    if not check_device_template_exists(session, new_device_template["templateName"]):
        try:
            response = session.endpoints.configuration_template_master.create_device_template_from_feature_templates(
                payload=new_device_template
            )
            logger.info(f"Created Device Template: {new_device_template['templateName']}, id: {response.template_id}")
        except ManagerHTTPError as ex:
            logger.error(
                f"Could not create Device Template {new_device_template['templateName']}.\nManager error: {ex.info}"
            )
            raise ex
    else:
        print(f"Skipping Device Template: {new_device_template['templateName']}")


def process_policy(session: ManagerSession, policy_data, device_template: Dict[str, Any]) -> None:
    """Processes a policy and creates it if it does not exist."""
    if "policyId" in device_template and device_template["policyId"]:
        policy_id = device_template["policyId"]
        if policy_id in policy_data["policies_definitions"]:
            policy_definition = clean_dict(policy_data["policies_definitions"][policy_id], POLICY_KEYS)
            existing_policy_id = check_policy_exists(session, policy_definition["policyName"])
            if not existing_policy_id:
                # session.endpoints.configuration.policy.vedge_template.create_vedge_template
                try:
                    endpoint = "/dataservice/template/policy/vedge"
                    response = session.post(endpoint, json=policy_definition)
                    new_policy_id = response.json()["policyId"] if response else None
                    logger.info(f"Created Policy: {policy_definition['policyName']}")
                except ManagerHTTPError as ex:
                    logger.error(
                        f"Could not create Policy {policy_definition['policyName']}.\nManager error: {ex.info}"
                    )
                    raise ex
            else:
                new_policy_id = existing_policy_id
                logger.info(f"Skipping Policy: {policy_definition['policyName']}")
            device_template["policyId"] = str(new_policy_id)
        else:
            logger.warning("Policy data missing in backup")


def import_templates(session: ManagerSession, templates_directory: Path) -> None:
    """Imports templates from a specified directory into the session.

    Extracts the templates from a tar archive, loads the JSON data for device,
    feature, and policy templates, and then processes them to create or update the templates
    in the session.

    Args:
        session: The session object to interact with the API.
        templates_directory: The directory containing the tar archive of templates.

    Raises:
        FileNotFoundError: If the specified template JSON files are not found in the directory.
        ManagerHTTPError: If there is an error processing the templates through the API.
    """
    dest_dir_path = Path(Path.cwd() / "templates")
    extract_tar_with_templates_to_path(templates_directory, dest_dir_path)

    device_template_json_file = dest_dir_path / TemplatesJsonNames.DEVICE_TEMPLATES.value
    feature_template_file = dest_dir_path / TemplatesJsonNames.FEAUTRE_TEMPLATES.value
    policy_json_file = dest_dir_path / TemplatesJsonNames.POLICIES.value

    device_template_data = load_json_from_file(device_template_json_file)
    feature_template_data = load_json_from_file(feature_template_file)
    policy_data = load_json_from_file(policy_json_file) if policy_json_file.exists() else None

    feature_template_name_to_id_map = get_feature_template_name_to_id_map(session)

    template_id_mapping = process_feature_templates(session, feature_template_data, feature_template_name_to_id_map)

    for device_template in device_template_data["templates"]:
        if policy_data:
            process_policy(session, policy_data, device_template)
        process_device_template(session, device_template, template_id_mapping)


# --- Execution --- #

"""

session = create_manager_session(url="X.X.X.X", port=443, username="admin", password="blabla")

export_templates(
    session=session,
    templates_directory=Path("/Users/acichon/Work/cisco-open/cisco-catalyst-wan-sdk/templates_export"),
    filters={"factory_default": False},
    force_existing_dir_removal=True,
)

import_templates(
    session=session, templates_directory=Path("/Users/acichon/Work/cisco-open/cisco-catalyst-wan-sdk/templates_export")
)

"""
