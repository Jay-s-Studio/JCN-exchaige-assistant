"""
Schema for files
"""
from pydantic import BaseModel, Field, field_serializer, ConfigDict
from telegram import File


class TelegramFile(BaseModel):
    """TelegramFile"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    file_unique_id: str = Field(title="File Unique ID", description="File Unique ID")
    file: File = Field(title="File", description="File")
    file_name: str = Field(title="File Name", description="File Name")
    content_type: str = Field(title="Content Type", description="Content Type")

    @field_serializer("file")
    def serialize_file(self, value: File, _info):
        """
        serialize file
        :param value:
        :param _info:
        :return:
        """
        return value.to_dict()
