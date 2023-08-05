import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_dynamodb
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-dynamodb-global", "0.28.0", __name__, "aws-dynamodb-global@0.28.0.jsii.tgz")
class GlobalTable(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dynamodb-global.GlobalTable"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, regions: typing.List[str], table_name: str, auto_deploy: typing.Optional[bool]=None, env: typing.Optional[aws_cdk.cdk.Environment]=None, naming_scheme: typing.Optional[aws_cdk.cdk.IAddressingScheme]=None, stack_name: typing.Optional[str]=None, partition_key: aws_cdk.aws_dynamodb.Attribute, billing_mode: typing.Optional[aws_cdk.aws_dynamodb.BillingMode]=None, pitr_enabled: typing.Optional[bool]=None, read_capacity: typing.Optional[jsii.Number]=None, sort_key: typing.Optional[aws_cdk.aws_dynamodb.Attribute]=None, sse_enabled: typing.Optional[bool]=None, stream_specification: typing.Optional[aws_cdk.aws_dynamodb.StreamViewType]=None, ttl_attribute_name: typing.Optional[str]=None, write_capacity: typing.Optional[jsii.Number]=None) -> None:
        props: GlobalTableProps = {"regions": regions, "tableName": table_name, "partitionKey": partition_key}

        if auto_deploy is not None:
            props["autoDeploy"] = auto_deploy

        if env is not None:
            props["env"] = env

        if naming_scheme is not None:
            props["namingScheme"] = naming_scheme

        if stack_name is not None:
            props["stackName"] = stack_name

        if billing_mode is not None:
            props["billingMode"] = billing_mode

        if pitr_enabled is not None:
            props["pitrEnabled"] = pitr_enabled

        if read_capacity is not None:
            props["readCapacity"] = read_capacity

        if sort_key is not None:
            props["sortKey"] = sort_key

        if sse_enabled is not None:
            props["sseEnabled"] = sse_enabled

        if stream_specification is not None:
            props["streamSpecification"] = stream_specification

        if ttl_attribute_name is not None:
            props["ttlAttributeName"] = ttl_attribute_name

        if write_capacity is not None:
            props["writeCapacity"] = write_capacity

        jsii.create(GlobalTable, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="regionalTables")
    def regional_tables(self) -> typing.List[aws_cdk.aws_dynamodb.Table]:
        return jsii.get(self, "regionalTables")


@jsii.data_type(jsii_type="@aws-cdk/aws-dynamodb-global.GlobalTableProps")
class GlobalTableProps(aws_cdk.cdk.StackProps, aws_cdk.aws_dynamodb.TableOptions, jsii.compat.TypedDict):
    regions: typing.List[str]
    tableName: str

__all__ = ["GlobalTable", "GlobalTableProps", "__jsii_assembly__"]

publication.publish()
