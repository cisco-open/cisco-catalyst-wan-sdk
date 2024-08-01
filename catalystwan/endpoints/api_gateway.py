from pydantic import BaseModel

from catalystwan.endpoints import APIEndpoints, delete, post


class OnBoardClient(BaseModel):
    client_id: str
    client_secret: str
    client_name: str


class ApiGateway(APIEndpoints):
    @delete("/certificate/{uuid}")
    def delete_configuration(self, uuid: str) -> None:
        ...

    @post("/apigw/config/reload")
    def configuration_reload(self) -> None:
        """After launching the API Gateway, SSP can use the API
        and bearer authentication header with provision access token obtained
        in the step above. It reloads the configuration from S3 bucket, Secrets Manager
        and reset the RDS connection pool."""
        ...

    @post("/apigw/client/registration")
    def on_board_client(self, payload: OnBoardClient) -> None:
        ...

    @post("/certificate/vedge/list?action={action}")
    def send_to_controllers(self, action: str = "push") -> None:
        ...

    @post("/certificate/vsmart/list")
    def send_to_vbond(self) -> None:
        ...
