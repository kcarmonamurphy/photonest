from django.db import models
from django.db.models.signals import pre_save

class Record(models.Model):
    uri = models.CharField(max_length=255, primary_key=True, blank=True)
    name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.uri

    def save(self, *args, **kwargs):
        self.uri = self.parent.uri + '/' + self.name
        # if succeeds saving to file system, call save method
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print("DELETING")
        # if succeeds deleting from file system, call delete method
        super().delete(*args, **kwargs)

class Folder(Record):
    parent = models.ForeignKey('self',
        null=True,
        blank=True,
        related_name='folders',
        db_index=True,
        on_delete=models.CASCADE
    )

class Image(Record):
    parent = models.ForeignKey(Folder, 
        on_delete=models.CASCADE,
        related_name='images',
    )

    title = models.TextField(null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


def your_receiver_function(sender, instance, *args, **kwargs):
    print("HELLO THERE")
    if instance.name and not instance.uri:
               instance.slug = slugify(instance.title)

pre_save.connect(your_receiver_function, sender=Image)