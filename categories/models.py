from django.db import models
from common.models import CommonModel

class Category(CommonModel):
    
    """ Category Model Definition"""
    
    class CategoryKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCES = ("experience", "Experience")
    
    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15, 
        choices=CategoryKindChoices.choices
        )
        
    def __str__(self) -> str:
        return f"{self.kind}: {self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"
