from pydantic import BaseModel

from catalystwan.endpoints import APIEndpoints, post


class OnBoardClient(BaseModel):
    client_id: str
    client_secret: str
    client_name: str


class ApiGateway(APIEndpoints):
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
