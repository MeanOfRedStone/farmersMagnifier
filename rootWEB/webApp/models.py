from django.db import models

# Create your models here.
class user_information(models.Model):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=15)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=10)  # Field name made lowercase.
    user_password = models.CharField(db_column='USER_PASSWORD', max_length=25)  # Field name made lowerca