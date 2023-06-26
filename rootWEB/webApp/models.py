from django.db import models

# Create your models here.
class user_information(models.Model):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=15)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=10)  # Field name made lowercase.
    user_password = models.CharField(db_column='USER_PASSWORD', max_length=25)  # Field name made lowerca

class board_information(models.Model):
    board_no = models.IntegerField(db_column='BOARD_NO', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(user_information, on_delete=models.CASCADE, db_column='USER_ID')  # Field name made lowercase.
    board_title = models.CharField(db_column='BOARD_TITLE', max_length=50)  # Field name made lowercase.
    board_content = models.CharField(db_column='BOARD_CONTENT', max_length=1200)  # Field name made lowercase.
    view_cnt = models.IntegerField(db_column='VIEW_CNT')  # Field name made lowercase.
    create_dt = models.DateTimeField(db_column='CREATE_DT')  # Field name made lowercase.

class pest_information(models.Model):
    information_no = models.IntegerField(db_column='INFORMATION_NO', primary_key=True)  # Field name made lowercase.
    plant_category = models.CharField(db_column='PLANT_CATEGORY', max_length=25)  # Field name made lowercase.
    plant_nm = models.CharField(db_column='PLANT_NM', max_length=25)  # Field name made lowercase.
    content = models.CharField(db_column='CONTENT', max_length=800)  # Field name made lowercase.
    pest_img = models.CharField(db_column='PEST_IMG', max_length=200, blank=True,
                                null=True)  # Field name made lowercase.
    pest_name = models.CharField(db_column='PEST_NAME', max_length=25, default='')

class upload_table(models.Model):
    upload_no = models.AutoField(db_column='UPLOAD_NO', primary_key=True)
    image = models.ImageField(db_column='IMAGE', null=False)

