from datetime import datetime

from catalystwan.models.templates import FeatureTemplateInformation

dhcp_server = FeatureTemplateInformation(
    last_updated_by="admin",
    id="88f9618c-1a47-450e-9c73-367952ca1d56",
    factory_default=False,
    name="DHCP_DEFAULT",
    devices_attached=0,
    description="1341324",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="cisco_dhcp_server",
    device_type=["vedge-C1101-4PLTEPW"],
    version="15.0.0",
    template_definiton='{"address-pool": {"vipObjectType": "object", "vipType": "constant", "vipValue":'
    '"10.0.0.0/32", "vipVariableName": "dhcp_address_pool"}, "exclude": {"vipObjectType":'
    '"list", "vipType": "ignore ", "vipVariableName": "dhcp-address_exclude"}, "lease-time":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipValue": 86400, "vipVariableName":'
    '"lease_time"}, "options": {"interface-mtu": {"vipObjectType": "object ", "vipType":'
    '"ignore", "vipVariableName": "dhcp_interface_mtu"}, "domain-name": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipVariableName": "dhcp_domain_name"}, "default-gateway":'
    '{"vipObjectType": "object",  "vipType": "ignore", "vipVariableName":'
    '"dhcp_default_gateway"}, "dns-servers": {"vipObjectType": "list", "vipType": "ignore",'
    '"vipVariableName": "dhcp_dns_server"}, "tftp-servers": {"vipObjectType": "list", "vipType'
    '": "ignore", "vipVariableName": "tftp-server"}, "option-code": {"vipType": "ignore",'
    '"vipValue": [], "vipObjectType": "tree", "vipPrimaryKey": ["code"]}}, "static-lease":'
    '{"vipType": "ignore", "vipValue": [], "vipObjectT ype": "tree", "vipPrimaryKey": ["mac-'
    'address"]}}',
)
