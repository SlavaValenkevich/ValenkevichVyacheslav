from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    tagname = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name


class Tasklist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name = 'owner', on_delete = models.CASCADE, null = True)#'auth.User'
    user = models.ManyToManyField(User, blank = True)
    def __str__(self):
        return "{}".format(self.name)

        
class Task(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    date_modified = models.DateField(auto_now=True)
    tasklist = models.ForeignKey(Tasklist, related_name='tasks', on_delete=models.CASCADE)
    tags_string = models.CharField( max_length=200, blank=True, null = True)
    tags = models.ManyToManyField(Tag, editable=False)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

    PRIORITY = (
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
        ('n', 'None')
    )

    priority = models.CharField(max_length=1, choices=PRIORITY, default='n')
 
    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        
        names = [name.strip() for name in self.tags_string.split(',')]
        
        for name in names:
            tag, created = Tag.objects.get_or_create(tagname=name)
            self.tags.add(tag)

    def __str__(self):
        return "{}".format(self.name)

class Share(models.Model):
    
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    tasklist = models.ForeignKey(Tasklist, related_name='lists',  on_delete=models.CASCADE)
    permission = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name = 'owner1',on_delete = models.CASCADE,  null = True)
    class Meta:
        unique_together = ('username','tasklist')

    #def save(self, *args, **kwargs):
    #    super(Share, self).save(*args, **kwargs)
    #    list_id = self.kwargs.get('list_id', None)
    #    self.tasklist.add(list_id)

    
    def __str__(self):
        return "{}".format(self.name)
