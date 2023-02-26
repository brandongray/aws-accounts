from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
)
from constructs import Construct


class AwsAccountsIamCicd(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domain = "https://token.actions.githubusercontent.com"
        aws_client_id = "sts.amazonaws.com"
        repo = "brandongray/aws-accounts"
        role_name = "github-oidc-role"

        github_oidc = iam.OpenIdConnectProvider(
            self,
            "GithubOidc",
            url=domain,
            client_ids=[aws_client_id],
            thumbprints=["6938fd4d98bab03faadb97b34396831e3780aea1"],
        )

        iam.Role(
            self,
            "GithubOidcIamRole",
            role_name=role_name,
            assumed_by=iam.WebIdentityPrincipal(
                identity_provider=github_oidc.open_id_connect_provider_arn,
                conditions={
                    "ForAllValues:StringLike": {
                        f"{domain}:sub": f"repo:{repo}:*",
                        f"{domain}:aud": aws_client_id,
                    }
                },
            ),
            inline_policies={
                "cdk-access": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["sts:AssumeRole"],
                            resources=["arn:aws:iam::*:role/cdk-*"],
                            effect=iam.Effect.ALLOW,
                        )
                    ]
                )
            },
        )
