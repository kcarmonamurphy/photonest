from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Record(MPTTModel):
	uri = models.TextField()
	name = models.TextField()

	parent = TreeForeignKey('self',
		null=True,
		blank=True,
		related_name='records',
		db_index=True,
		on_delete=models.CASCADE
	)

	class MPTTMeta:
		order_insertion_by = ['name']

	def __str__(self):
		return self.uri

class Folder(Record):
	pass

class Image(models.Model):
	parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
	title = models.TextField(null=True, blank=True)
	width = models.IntegerField(null=True, blank=True)
	height = models.IntegerField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)