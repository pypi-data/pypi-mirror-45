import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_codebuild
import aws_cdk.aws_codepipeline
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_stepfunctions
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-events-targets", "0.28.0", __name__, "aws-events-targets@0.28.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_events.IEventRuleTarget)
class CodeBuildProject(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.CodeBuildProject"):
    def __init__(self, project: aws_cdk.aws_codebuild.IProject) -> None:
        jsii.create(CodeBuildProject, self, [project])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @property
    @jsii.member(jsii_name="project")
    def project(self) -> aws_cdk.aws_codebuild.IProject:
        return jsii.get(self, "project")


@jsii.implements(aws_cdk.aws_events.IEventRuleTarget)
class SnsTopic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SnsTopic"):
    def __init__(self, topic: aws_cdk.aws_sns.ITopic) -> None:
        jsii.create(SnsTopic, self, [topic])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @property
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        return jsii.get(self, "topic")


__all__ = ["CodeBuildProject", "SnsTopic", "__jsii_assembly__"]

publication.publish()
