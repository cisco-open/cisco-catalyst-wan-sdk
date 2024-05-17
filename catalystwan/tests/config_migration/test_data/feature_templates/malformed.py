from datetime import datetime
from uuid import uuid4

from catalystwan.models.templates import FeatureTemplateInformation

malformed = FeatureTemplateInformation(
    last_updated_by="",
    id=str(uuid4()),
    factory_default=True,
    name="Can be any name",
    devices_attached=0,
    description="",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="Can be any type to test the validation",
    device_type=[""],
    version="15.0.0",
    template_definiton="rasrewrwqerqwer",
)
