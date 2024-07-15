from datetime import datetime
from uuid import uuid4

from catalystwan.models.templates import FeatureTemplateInformation

vpn_management = FeatureTemplateInformation(
    last_updated_by="",
    id=str(uuid4()),
    factory_default=True,
    name="Management_VPN",
    devices_attached=0,
    description="Default Cisco Management VPN template settings",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="cisco_vpn",
    device_type=[""],
    version="15.0.0",
    template_definiton='{"vpn-id":{"vipObjectType":"object","vipType":"constant","vipValue":512},'
    '"name":{"vipObjectType":"object","vipType":"constant","vipValue":"Management VPN"},'
    '"ecmp-hash-key":{"layer4":{"vipObjectType":"object","vipType":"ignore","vipValue":"false"}},'
    '"host":{"vipType":"ignore","vipValue":[],"vipObjectType":"tree","vipPrimaryKey":["hostname"]}}',
)

vpn_transport = FeatureTemplateInformation(
    last_updated_by="",
    id=str(uuid4()),
    factory_default=True,
    name="Transport_VPN",
    devices_attached=0,
    description="Default Cisco Transport VPN template settings",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="cisco_vpn",
    device_type=[""],
    version="15.0.0",
    template_definiton='{"vpn-id":{"vipObjectType":"object","vipType":"constant","vipValue":0},'
    '"name":{"vipObjectType":"object","vipType":"constant","vipValue":"Transport VPN"},'
    '"ecmp-hash-key":{"layer4":{"vipObjectType":"object","vipType":"ignore","vipValue":"false"}},'
    '"host":{"vipType":"ignore","vipValue":[],"vipObjectType":"tree","vipPrimaryKey":["hostname"]}}',
)

vpn_service = FeatureTemplateInformation(
    last_updated_by="",
    id=str(uuid4()),
    factory_default=True,
    name="Service_VPN",
    devices_attached=0,
    description="Factory Default template for VPN 1 Cisco",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="cisco_vpn",
    device_type=[""],
    version="15.0.0",
    template_definiton='{"vpn-id":{"vipValue":1,"vipObjectType":"object",'
    '"vipType":"constant","vipVariableName":""},"name":{"vipValue":"","vipObjectType":'
    '"object","vipType":"ignore"},"dns":{"vipValue":[],"vipObjectType":"tree",'
    '"vipType":"ignore","vipPrimaryKey":["dns-addr"]},"dns-ipv6":{"vipValue":[],'
    '"vipObjectType":"tree","vipType":"ignore","vipPrimaryKey":["dns-addr"]},'
    '"ecmp-hash-key":{"layer4":{"vipValue":"","vipObjectType":"object","vipType":"ignore"}},'
    '"host":{"vipValue":[],"vipObjectType":"tree","vipType":"ignore","vipPrimaryKey":'
    '["hostname"]},"ip":{"route": {"vipValue":[],"vipObjectType":"tree","vipType":"ignore",'
    '"vipPrimaryKey":["prefix"]}}, "ipv6":{"route":{"vipValue":[],"vipObjectType":"tree",'
    '"vipType":"ignore","vipPrimaryKey":["prefix"]}}, "omp":{"advertise":{"vipValue":[],'
    '"vipObjectType":"tree","vipType":"ignore","vipPrimaryKey":["protocol"]},'
    '"ipv6-advertise":{"vipValue":[],"vipObjectType":"tree","vipType":"ignore",'
    '"vipPrimaryKey":["protocol"]}}, "nat64":{"v4":{"pool":{"vipValue":[],"vipObjectType":'
    '"tree","vipType":"ignore","vipPrimaryKey":["name"]}}}}',
)
