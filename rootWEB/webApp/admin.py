from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(user_information)
admin.site.register(pest_information)
admin.site.register(board_information)
admin.site.register(upload_table)

