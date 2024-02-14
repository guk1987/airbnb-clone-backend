from django.db import models
from common.models import CommonModel

class Experience(CommonModel):
    
    """ Experience Model Definition"""
    
    name = models.CharField(
        max_length=140, 
        default=""
        )
    country = models.CharField(
        max_length=50, 
        default="대한민국"
        )
    city = models.CharField(
        max_length=80, 
        default = "서울"
        )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    host = models.ForeignKey(
        "users.User", 
        on_delete=models.CASCADE,
        related_name="experiences",
        )
    start_at = models.TimeField()
    end_at = models.TimeField()
    description = models.TextField()
    perks  = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
        )
    category = models.ForeignKey(
        "categories.category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )
    
    def __str__(self) -> str:
        return self.name

class Perk(CommonModel):
    
    """Perk Model Definition"""
    
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(max_length=150, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Perks"
