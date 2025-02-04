from django.db import models

# Create your models here.

class PlantingOp(models.TextChoices):
    D = "1", "Direct Sow"
    I = "2", "Indoor Start"
    
class GardenGroup(models.Model): 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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

    # change 
    location = models.ForeignKey(GardenGroup, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.crop.name)


class Task(models.Model):
    # Format can be: Plant {CROP NAME} {Planting Option}
    title = models.CharField(max_length=200)
 
    done = models.BooleanField(default=False)
    done_on = models.DateField(null=True, blank=True)

    # default to appropriate dates 
    complete_on = models.DateField(null=True, blank=True)

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    #garden = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_date(self): 
        if self.done_on: 
            return self.done_on.strftime("%Y-%m-%d")
        if self.complete_on: 
            return self.complete_on.strftime("%Y-%m-%d")
        return None