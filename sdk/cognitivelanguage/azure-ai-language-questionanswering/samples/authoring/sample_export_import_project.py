# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
FILE: sample_export_import_project.py

DESCRIPTION:
    This sample demonstrates how to export and import a Qna project.

USAGE:
    python sample_export_import_project.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_QUESTIONANSWERING_ENDPOINT - the endpoint to your QuestionAnswering resource.
    2) AZURE_QUESTIONANSWERING_KEY - your QuestionAnswering API key.
"""


def sample_export_import_project():
    # [START export_import_project]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.questionanswering.authoring import QuestionAnsweringAuthoringClient

    # get service secrets
    endpoint = os.environ["AZURE_QUESTIONANSWERING_ENDPOINT"]
    key = os.environ["AZURE_QUESTIONANSWERING_KEY"]

    # create client
    client = QuestionAnsweringAuthoringClient(endpoint, AzureKeyCredential(key))
    with client:

        # create project
        project_name = "IssacNewton"
        client.create_project(
            project_name=project_name,
            options={
                "description": "biography of Sir Issac Newton",
                "language": "en",
                "multilingualResource": True,
                "settings": {
                    "defaultAnswer": "no answer"
                }
            })

        # export
        export_poller = client.begin_export(
            project_name=project_name,
            file_format="json"
        )
        export_result = export_poller.result()
        export_url = export_result["resultUrl"]

        # import project
        project = {
            "Metadata": {
                "ProjectName": "IssacNewton",
                "Description": "biography of Sir Issac Newton",
                "Language": "en",
                "DefaultAnswer": None,
                "MultilingualResource": False,
                "CreatedDateTime": "2022-01-25T13:10:08Z",
                "LastModifiedDateTime": "2022-01-25T13:10:08Z",
                "LastDeployedDateTime": None,
                "Settings": {
                    "DefaultAnswer": "no answer",
                    "EnableHierarchicalExtraction": None,
                    "DefaultAnswerUsedForExtraction": None
                }
            }
        }
        import_poller = client.begin_import_assets(
            project_name=project_name,
            options=project
        )
        import_poller.result()

        # list projects
        print("view all qna projects:")
        qna_projects = client.list_projects()
        for p in qna_projects:
            if p["projectName"] == project_name:
                print("project: {}".format(p["projectName"]))
                print("\tlanguage: {}".format(p["language"]))
                print("\tdescription: {}".format(p["description"]))

    # [END export_import_project]


if __name__ == '__main__':
    sample_export_import_project()
