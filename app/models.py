from django.db import models

class Record(models.Model):
	uri = models.URLField(max_length=255, primary_key=True)
	name = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.uri

class Folder(Record):
	parent = models.ForeignKey('self',
		null=True,
		blank=True,
		related_name='records',
		db_index=True,
		on_delete=models.CASCADE
	)

class Image(Record):
	parent = models.ForeignKey(Folder, 
		on_delete=models.CASCADE
	)

	title = models.TextField(null=True, blank=True)
	size = models.TextField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)

