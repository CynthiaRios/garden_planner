from django.db import models

# Create your models here.

class PlantingOp(models.TextChoices):
    D = "1", "Direct Sow"
    I = "2", "Indoor Start"
    
# Crop: Model to describe the different crops that can be planted
class Crop(models.Model):
    class Season(models.TextChoices):
        SP = "1", "Spring"
        SU = "2", "Summer"
        FA = "3", "Fall"
        WI = "4", "Winter"

    class Sunlight(models.TextChoices):
        FSU = "1", "Full Sun"
        PSU = "2", "Part Sun"
        PSH = "3", "Part Shade"
        FSH = "4", "Full Shade"
        DSH = "5", "Dense Shade"

    name = models.CharField(max_length=100)
    variety  = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    season = models.CharField(
        max_length=2,
        choices=Season.choices,
        null = True, 
        blank = True
    )
    # CHANGES 
    target_seed_start = models.DateTimeField(blank=True, null=True)
    target_transport_start = models.DateTimeField(blank=True, null=True) 
    target_seed_start_outdoors = models.DateTimeField(blank=True, null=True)

    #target_date_to_harvest = models.DateTimeField(blank=True, null=True)

    planting_op  = models.CharField(
        max_length=2,
        choices=PlantingOp.choices,
        null = True, 
        blank = True
    )
    sunlight = models.CharField(
        max_length=2,
        choices=Sunlight.choices,
        null = True, 
        blank = True
    )
    instructions  = models.CharField(max_length=256, null=True, blank=True)
    square_footage_needed = models.FloatField(null=True, blank=True)
    qty_per_square_foot = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


# Plant: Model to describe a specific Crop that was planted
class Plant(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    qty = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)

    date_planted = models.DateTimeField(blank=True, null=True)
    date_to_transplant = models.DateTimeField(blank=True, null=True) 
    date_to_harvest = models.DateTimeField(blank=True, null=True)

    planting_op  = models.CharField(
        max_length=2,
        choices=PlantingOp.choices,
        null = True, 
        blank = True
    )
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.crop.name)