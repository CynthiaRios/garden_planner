from django.urls import path

from . import views


# CROP VIEWS: View all, add, delete, update  
# PLANT VIEWS: View all, add, delete, update  

# Share an index with 2 tabs (Bootstrap)
# Buttons to add, update, delete 

urlpatterns = [
    path("", views.index, name="crop_index"),
    #path("add_crop", views.add_crop, name="add_crop"),
    path("update_crop/<id>", views.update_crop, name="update_crop"),
    path("delete_crop/<id>", views.delete_crop, name="delete_crop"),

    #path("", views.plant_index, name="plant_index"),
    #path("add_plant/<id>", views.add_plant, name="add_plant"),
    path("update_plant/<id>", views.update_plant, name="update_plant"),
    path("delete_plant/<id>", views.delete_plant, name="delete_plant"),
]
