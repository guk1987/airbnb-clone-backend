from django.db import models
from common.models import CommonModel

class Photo(CommonModel):
    
    """ Photo Model Definition """
    
    file = models.URLField()
    description = models.TextField(
        max_length=140, 
        blank=True,
        )
    room = models.ForeignKey(
        "rooms.Room", 
        on_delete=models.CASCADE,
        null = True,
        blank = True,
        related_name="photos",
        )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null = True,
        blank = True,
        related_name="photos",
        )
    
    def __str__(self) -> str:
        return "Photo file"
    
    
class Video(CommonModel):
    
    """ Video Model Definition """
    
    file = models.URLField()
    
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )
    def __str__(self) -> str:
        return "Video file"
    
    
    
