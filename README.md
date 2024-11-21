# NEW REPOSITORY URL
- Development of SDK moved to: https://github.com/cisco-en-programmability/catalystwan-sdk
- New versions of `catalystwan` package will be built from new origin.

<p align="center">
  <a href="#"><img src="docs/images/catalystwan.svg" alt="Cisco Catalyst WAN SDK Logo" style="height:150px" />
</p>

[![Python-Supported](https://img.shields.io/static/v1?label=Python&logo=Python&color=3776AB&message=3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12)](https://www.python.org/)

Cisco Catalyst WAN SDK is a package for creating simple and parallel automatic requests via official SD-WAN Manager API. It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant). The library is not dependent on environment which is being run in, you just need a connection to any SD-WAN Manager.

## Important Notice: Early Beta Release

Welcome to the Cisco Catalyst WAN SDK!

We are thrilled to announce that Cisco Catalyst WAN SDK is now available in early beta. This is an exciting step forward in enabling developers to harness the full potential of Cisco's networking solutions.  Please be aware that, as an early beta release, this version of the SDK is still undergoing development and testing. As such, it is provided "as is" and support to address any issues are limited and best effort.

## Not recommend to use in production environments.
We encourage developers to explore and test the SDK's capabilities, but please exercise caution when using it in production environments.  We are dedicated to improving the Cisco Catalyst WAN SDK and we value your input. Your feedback is crucial to us-it will guide us in refining and enhancing the SDK to better meet your needs.
To report any issues, share your insights, or suggest improvements, please visit our Issues page on GitHub or reach out to us through the provided communication channels.

Thank you for being a part of our development journey!

## Installation
```console
pip install catalystwan
```

## Manager Session
In order to execute SDK APIs **ManagerSession** needs to be created. The fastest way to get started is to use `create_manager_session()` method which configures session, performs authentication for given credentials and returns **ManagerSession** instance in operational state. **ManagerSession** provides a collection of supported APIs in `api` instance variable.
Please check example below:

```python
from catalystwan.session import create_manager_session

url = "example.com"
username = "admin"
password = "password123"

with create_manager_session(url=url, username=username, password=password) as session:
    devices = session.api.devices.get()
    print(devices)
```

**ManagerSession** extends [requests.Session](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects) so all functionality from [requests](https://requests.readthedocs.io/en/latest/) library is avaiable to user, it also implements python [contextmanager](https://docs.python.org/3.8/library/contextlib.html#contextlib.contextmanager) and automatically frees server resources on exit.

<details>
    <summary> <b>Configure Manager Session before using</b> <i>(click to expand)</i></summary>

It is possible to configure **ManagerSession** prior sending any request.

```python
from catalystwan.session import ManagerSession
from catalystwan.vmanage_auth import vManageAuth

url = "example.com"
username = "admin"
password = "password123"

# configure session using constructor - nothing will be sent to target server yet
auth = vManageAuth(username, password)
session = ManagerSession(url=url, auth=auth)
# login and send requests
session.login()
session.get("/dataservice/device")
session.close()
```
When interacting with the SDWAN Manager API without using a context manager, it's important 
to manually execute the `close()` method to release the user session resource.
Ensure that the `close()` method is called after you have finished using the session to maintain optimal resource management and avoid potential errors.

</details>

<details>
    <summary> <b>Login as Tenant</b> <i>(click to expand)</i></summary>

Tenant domain needs to be provided in url together with Tenant credentials.

```python
from catalystwan.session import create_manager_session

url = "tenant.example.com"
username = "tenant_user"
password = "password123"

with create_manager_session(url=url, username=username, password=password) as session:
    print(session.session_type)
```

</details>

<details>
    <summary> <b>Login as Provider-as-Tenant</b> <i>(click to expand)</i></summary>

Tenant `subdomain` needs to be provided as additional argument together with Provider credentials.

```python
from catalystwan.session import create_manager_session

url = "example.com"
username = "provider"
password = "password123"
subdomain = "tenant.example.com"

with create_manager_session(url=url, username=username, password=password, subdomain=subdomain) as session:
    print(session.session_type)
```

</details>

<details>
    <summary> <b>Login using Api Gateway</b> <i>(click to expand)</i></summary>

```python
from catalystwan.session import create_apigw_session

with create_apigw_session(
    url="example.com",
    client_id="client_id",
    client_secret="client_secret",
    org_name="Org-Name",
    username="user",
    mode="user",
    token_duration=10,
) as session:
    devices = session.api.devices.get()
    print(devices)
```
</details>

<details>
    <summary> <b>Threading</b> <i>(click to expand)</i></summary>

```python
from threading import Thread
from catalystwan.session import ManagerSession
from catalystwan.vmanage_auth import vManageAuth
from copy import copy

def print_devices(manager: ManagerSession):
    # using context manager (recommended)
    with manager.login() as session:
        print(session.api.devices.get())

if __name__ =="__main__":

    # 1. Create shared authentication handler for user session
    auth = vManageAuth(username="username", password="password")
    # 2. Configure session with base url and attach authentication handler
    manager = ManagerSession(base_url="https://url:port", auth=auth)

    # 3. Make sure each thread gets own copy of ManagerSession object
    t1 = Thread(target=print_devices, args=(manager,))
    t2 = Thread(target=print_devices, args=(copy(manager),))
    t3 = Thread(target=print_devices, args=(copy(manager),))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("Done!")
```
Threading can be achieved by using a shared auth object with sessions in each thread. As `ManagerSession` is not guaranteed to be thread-safe, it is recommended to create one session per thread. `ManagerSession` also comes in with a default `RequestLimiter`, which limits the number of concurrent requests to 50. It keeps `ManagerSession` from overloading the server and avoids HTTP 503 and HTTP 429 errors.
If you wish to modify the limit, you can pass a modified `RequestLimiter` to `ManagerSession`:
```python
from catalystwan.session import ManagerSession
from catalystwan.vmanage_auth import vManageAuth
from catalystwan.request_limiter import RequestLimiter

auth = vManageAuth(username="username", password="password")
limiter = RequestLimiter(max_requests=30)
manager = ManagerSession(base_url="https://url:port", auth=auth, request_limiter=limiter)
```
</details>

## API usage examples
All examples below assumes `session` variable contains logged-in [Manager Session](#Manager-Session) instance.

<details>
    <summary> <b>Get devices</b> <i>(click to expand)</i></summary>

```python
devices = session.api.devices.get()
```

</details>

<details>
    <summary> <b>Admin Tech</b> <i>(click to expand)</i></summary>

```Python
admin_tech_file = session.api.admin_tech.generate("172.16.255.11")
session.api.admin_tech.download(admin_tech_file)
session.api.admin_tech.delete(admin_tech_file)
```
</details>

<details>
    <summary> <b>Speed test</b> <i>(click to expand)</i></summary>

```python
devices = session.api.devices.get()
speedtest = session.api.speedtest.speedtest(devices[0], devices[1])
```

</details>

<details>
    <summary> <b>Upgrade device</b> <i>(click to expand)</i></summary>

```python
# Prepare devices list
controllers = session.endpoints.configuration_device_inventory.get_device_details('controllers')
vsmarts = controllers.filter(personality=Personality.VSMART)
image = "viptela-20.7.2-x86_64.tar.gz"

# Upload image
session.api.repository.upload_image(image)

# Install software

install_task = session.api.software.install(devices=vsmarts, image=image)

# Check action status
install_task.wait_for_completed()
```

</details>

<details>
    <summary> <b>Get alarms</b> <i>(click to expand)</i></summary>
To get all alarms:

```python
alarms = session.api.alarms.get()
```

To get all not viewed alarms:

```python
not_viewed_alarms = session.api.alarms.get().filter(viewed=False)
```

To get all alarms from past `n` hours:

```python
n = 24
alarms_from_n_hours = session.api.alarms.get(from_time=n)
```

To get all critical alarms from past `n` hours:

```python
from catalystwan.utils.alarm_status import Severity
n = 48
critical_alarms = session.api.alarms.get(from_time=n).filter(severity=Severity.CRITICAL)
```

</details>

<details>
    <summary> <b>Users</b> <i>(click to expand)</i></summary>

```python
# Get all users
session.api.users.get()

# Create user
from catalystwan.endpoints.administration_user_and_group import User
new_user = User(username="new_user", password="new_user", group=["netadmin"], description="new user")
session.api.users.create(new_user)

# Update user data
new_user_update = UserUpdateRequest(username="new_user", group=["netadmin", "netops"], locale="en_US", description="updated-new_user-description")
session.api.users.update(new_user_update)

# Update user password
session.api.users.update_password("new_user", "n3W-P4s$w0rd")

# Reset user
session.api.users.reset("new_user")

# Delete user
session.api.users.delete("new_user")

# Get current user authentication type and role
session.api.users.get_auth_type()
session.api.users.get_role()
```

</details>

<details>
    <summary> <b>User Groups</b> <i>(click to expand)</i></summary>

```python
# Get all user groups
session.api.user_groups.get()

# Create user group
group = UserGroup("new_user_group", [])
group.enable_read({"Audit Log", "Alarms"})
group.enable_read_and_write({"Device Inventory"})
session.api.user_groups.create(group)

# Update user group
group.disable({"Alarms"})
session.api.user_groups.update(group)

# Delete user group
session.api.user_groups.delete(group.group_name)
```

</details>

</details>

<details>
    <summary> <b>Sessions</b> <i>(click to expand)</i></summary>

```python
# Get all active sessions
active_sessions = session.api.sessions.get()

# Invalidate sessions for given user
new_user_sessions = active_sessions.filter(raw_username="new_user")
session.api.sessions.invalidate(new_user_sessions)
```

</details>

<details>
    <summary> <b>Resource Groups</b> <i>(click to expand)</i></summary>

```python
# get resource groups
session.api.resource_groups.get()

# create resource group
new_resource_group = ResourceGroup(
    name="new_resource_group",
    desc="Custom Resource Group #1",
    siteIds=[]
)
session.api.resource_groups.create(new_resource_group)

# update resource group
resource_group = session.api.resource_groups.get().filter(name="new_resource_group").single_or_default()
updated_resource_group = ResourceGroupUpdateRequest(
    id=resource_group.id,
    name=resource_group.name,
    desc="Custom Resource Group #1 with updated description and site ids",
    siteIds=[200]
)

# switch to resource group view
session.api.resource_groups.switch("new_resource_group")

# delete resource group
session.api.resource_groups.delete(resource_group.id)
```

</details>

<details>
    <summary> <b>Tenant management</b> <i>(click to expand)</i></summary>

```python
api = session.api.tenant_management
# create tenants
tenants = [
    Tenant(
        name="tenant1",
        org_name="CiscoDevNet",
        subdomain="alpha.bravo.net",
        desc="This is tenant for unit tests",
        edge_connector_enable=True,
        edge_connector_system_ip="172.16.255.81",
        edge_connector_tunnel_interface_name="GigabitEthernet1",
        wan_edge_forecast=1,
    )
]
create_task = api.create(tenants)
create_task.wait_for_completed()
# list all tenants
tenants_data = api.get_all()
# pick tenant from list by name
tenant = tenants_data.filter(name="tenant1").single_or_default()
# get selected tenant id
tenant_id = tenant.tenant_id
# get vsession id of selected tenant
vsessionid = api.vsession_id(tenant_id)
# delete tenant by ids
delete_task = api.delete([tenant_id])
delete_task.wait_for_completed()
# others
api.get_hosting_capacity_on_vsmarts()
api.get_statuses()
api.get_vsmart_mapping()
```
</details>

<details>
    <summary> <b>Tenant migration</b> <i>(click to expand)</i></summary>

```python
from pathlib import Path
from catalystwan.session import create_manager_session
from catalystwan.models.tenant import TenantExport
from catalystwan.workflows.tenant_migration import migration_workflow

tenant = TenantExport(
    name="mango",
    desc="Mango tenant description",
    org_name="Provider Org-Mango Inc",
    subdomain="mango.fruits.com",
    wan_edge_forecast=100,
    migration_key="MangoTenantMigrationKey",   # only for SDWAN Manager >= 20.13
    is_destination_overlay_mt=True,            # only for SDWAN Manager >= 20.13
)

with create_manager_session(url="10.0.1.15", username="st-admin", password="") as origin_session, \
     create_manager_session(url="10.9.0.16", username="mt-provider-admin", password="") as target_session:
    migration_workflow(
        origin_session=origin_session,
        target_session=target_session,
        workdir=Path("workdir"),
        tenant=tenant,
        validator="10.9.12.26"
    )
```

`migration_workflow` performs multi-step migration procedure according to [Migrate Single-Tenant Cisco SD-WAN Overlay to Multitenant Cisco SD-WAN Deployment](https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b)


Since 20.13 also MT to ST is supported (just provide suitable origin/target sessions, and `is_destination_overlay_mt` parameter)


Each step of the `migration_workflow` procedure can be executed independently using api methods: `export_tenant`, `download`, `import_tenant`, `store_token`, `migrate_network`

```python
origin_api = origin_session.api.tenant_migration_api
target_api = target_session.api.tenant_migration_api
tenant_file = Path("~/tenant.tar.gz")
token_file = Path("~/tenant-token.txt")
# export
export_task = origin_api.export_tenant(tenant=tenant)
remote_filename = export_task.wait_for_file()
# download
origin_api.download(export_path, remote_filename)
# import
import_task = target_api.import_tenant(export_path, tenant.migration_key)
import_task.wait_for_completed()
# get token
migration_id = import_task.import_info.migration_token_query_params.migration_id
target_api.store_token(migration_id, token_path)
# migrate network
migrate_task = origin_api.migrate_network(token_path)
migrate_task.wait_for_completed()
```
</details>


### Note:
To remove `InsecureRequestWarning`, you can include in your scripts (warning is suppressed when `catalystwan_devel` environment variable is set):
```Python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Catching Exceptions
```python
try:
    session.api.users.delete("bogus-user-name")
except ManagerHTTPError as error:
    # Process an error.
    print(error.response.status_code)
    print(error.info.code)
    print(error.info.message)
    print(error.info.details)

```

## [Supported API endpoints](https://github.com/cisco-open/cisco-catalyst-wan-sdk/blob/main/ENDPOINTS.md)


## [Contributing, bug reporting and feature requests](https://github.com/cisco-open/cisco-catalyst-wan-sdk/blob/main/CONTRIBUTING.md)

## Seeking support

You can contact us by submitting [issues](https://github.com/cisco-open/cisco-catalyst-wan-sdk/issues), or directly via mail on catalystwan@cisco.com.
