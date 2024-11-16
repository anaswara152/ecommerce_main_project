from django.db import models
# Create your models here.

class category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class covertypetable(models.Model):
    covertype=models.CharField(max_length=20)
    def __str__(self):
        return self.covertype

class product(models.Model):
    title=models.CharField(max_length=20)
    ISBN=models.CharField(max_length=20) 
    author=models.CharField(max_length=20)
    description=models.TextField()
    listprise=models.FloatField()   
    price=models.FloatField()
    price50=models.FloatField()
    price100=models.FloatField()
    categorys=models.ForeignKey(category,on_delete=models.CASCADE)
    covertype=models.ForeignKey(covertypetable,on_delete=models.CASCADE)
    image=models.FileField(upload_to='media')
    def __str__(self):
        return self.title
    



 
