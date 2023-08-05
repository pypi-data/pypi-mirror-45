import string
from dataclasses import dataclass

from upsourceapi.model.dto import ProjectSettings


@dataclass()
class CreateProjectRequest(object):
    """CreateProjectRequestDTO
    :param newProjectId: An ID of the new Upsource project.
    :param settings: Settings of the new Upsource project.
    """
    newProjectId: str
    settings: ProjectSettings

    def __post_init__(self):
        if not self.newProjectId:
            raise ValueError('newProjectId of the new Upsource project is required parameter.')
        if self.settings is None:
            raise ValueError('Settings of the new Upsource project is required parameter.')
        replace_punctuation = str.maketrans(string.punctuation, " " * len(string.punctuation))
        new_project_id = self.newProjectId.translate(replace_punctuation)
        new_project_id = new_project_id.replace(" ", "-")
        self.newProjectId = new_project_id
