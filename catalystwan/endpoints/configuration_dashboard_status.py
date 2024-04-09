# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.utils.operation_status import OperationStatus


class SubTaskData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    status: str
    status_id: str = Field(serialization_alias="statusId", validation_alias="statusId")
    action: Optional[str] = None
    activity: List[str] = []
    current_activity: Optional[str] = Field(
        default=None, serialization_alias="currentActivity", validation_alias="currentActivity"
    )
    action_config: Optional[Union[str, Dict]] = Field(
        default=None, serialization_alias="actionConfig", validation_alias="actionConfig"
    )
    order: Optional[int] = None
    uuid: Optional[str] = None
    hostname: Optional[str] = Field(default=None, serialization_alias="host-name", validation_alias="host-name")
    site_id: Optional[str] = Field(default=None, serialization_alias="site-id", validation_alias="site-id")


class TaskResult(BaseModel):
    result: bool
    sub_tasks_data: List[SubTaskData]


class RunningTaskData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    details_url: Optional[str] = Field(default=None, serialization_alias="detailsURL", validation_alias="detailsURL")
    user_session_username: Optional[str] = Field(
        default=None, serialization_alias="userSessionUserName", validation_alias="userSessionUserName"
    )
    rid: Optional[int] = Field(default=None, serialization_alias="@rid", validation_alias="@rid")
    tenant_name: Optional[str] = Field(default=None, serialization_alias="tenantName", validation_alias="tenantName")
    process_id: Optional[str] = Field(default=None, serialization_alias="processId", validation_alias="processId")
    name: Optional[str] = None
    tenant_id: Optional[str] = Field(default=None, serialization_alias="tenantId", validation_alias="tenantId")
    user_session_ip: Optional[str] = Field(
        default=None, serialization_alias="userSessionIP", validation_alias="userSessionIP"
    )
    action: Optional[str] = None
    start_time: Optional[int] = Field(default=None, serialization_alias="startTime", validation_alias="startTime")
    end_time: Optional[int] = Field(default=None, serialization_alias="endTime", validation_alias="endTime")
    status: Optional[str] = None


class Validation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    status_type: Optional[str] = Field(default=None, serialization_alias="statusType", validation_alias="statusType")
    activity: Optional[List[str]] = Field(default=None, serialization_alias="activity", validation_alias="activity")
    vmanage_ip: Optional[str] = Field(default=None, serialization_alias="vmanageIP", validation_alias="vmanageIP")
    system_ip: Optional[str] = Field(default=None, serialization_alias="system-ip", validation_alias="system-ip")
    device_id: Optional[str] = Field(default=None, serialization_alias="deviceID", validation_alias="deviceID")
    uuid: Optional[str] = Field(default=None, serialization_alias="uuid", validation_alias="uuid")
    rid: Optional[int] = Field(default=None, serialization_alias="@rid", validation_alias="@rid")
    status_id: str = Field(default=None, serialization_alias="statusId", validation_alias="statusId")
    process_id: Optional[str] = Field(default=None, serialization_alias="processId", validation_alias="processId")
    action_config: Optional[Union[str, Dict]] = Field(
        default=None, serialization_alias="actionConfig", validation_alias="actionConfig"
    )
    current_activity: Optional[str] = Field(
        default=None, serialization_alias="currentActivity", validation_alias="currentActivity"
    )
    action: Optional[str] = Field(default=None, serialization_alias="action", validation_alias="action")
    start_time: Optional[int] = Field(default=None, serialization_alias="startTime", validation_alias="startTime")
    request_status: Optional[str] = Field(
        default=None, serialization_alias="requestStatus", validation_alias="requestStatus"
    )
    status: OperationStatus = Field(default=None, serialization_alias="status", validation_alias="status")
    order: Optional[int] = Field(default=None, serialization_alias="order", validation_alias="order")


class Summary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    action: Optional[str] = Field(default=None, serialization_alias="action", validation_alias="action")
    name: Optional[str] = Field(default=None, serialization_alias="name", validation_alias="name")
    details_url: Optional[str] = Field(default=None, serialization_alias="detailsURL", validation_alias="detailsURL")
    start_time: Optional[str] = Field(default=None, serialization_alias="startTime", validation_alias="startTime")
    end_time: Optional[str] = Field(default=None, serialization_alias="endTime", validation_alias="endTime")
    user_session_user_name: Optional[str] = Field(
        default=None, serialization_alias="userSessionUserName", validation_alias="userSessionUserName"
    )
    user_session_ip: Optional[str] = Field(
        default=None, serialization_alias="userSessionIP", validation_alias="userSessionIP"
    )
    tenant_name: Optional[str] = Field(default=None, serialization_alias="tenantName", validation_alias="tenantName")
    total: Optional[int] = Field(default=None, serialization_alias="total", validation_alias="total")
    status: Optional[str] = Field(default=None, serialization_alias="status", validation_alias="status")
    count: Optional[dict] = Field(default=None, serialization_alias="count", validation_alias="count")


class TaskData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: List[SubTaskData] = []
    validation: Optional[Validation] = None
    summary: Optional[Summary] = None
    is_cancel_enabled: Optional[bool] = Field(
        default=None, serialization_alias="isCancelEnabled", validation_alias="isCancelEnabled"
    )
    is_parallel_execution_enabled: Optional[bool] = Field(
        default=None, serialization_alias="isParallelExecutionEnabled", validation_alias="isParallelExecutionEnabled"
    )


class TasksData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    running_tasks: List[RunningTaskData] = Field(
        default=[], serialization_alias="runningTasks", validation_alias="runningTasks"
    )


class ConfigurationDashboardStatus(APIEndpoints):
    @get("/device/action/status/{task_id}")
    def find_status(self, task_id: str) -> TaskData:
        ...

    @get("/device/action/status/tasks")
    def find_running_tasks(self) -> TasksData:
        ...
