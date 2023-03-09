from django.db import models


class Schema(models.Model):

    """Schema template"""

    name = models.CharField(max_length=50)
    column_separator = models.CharField(max_length=5)
    string_character = models.CharField(max_length=5)
    creation_date = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_created = models.BooleanField(default=False)
    file_link = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('-updated',)
        verbose_name_plural = 'Schemas'

    def __str__(self):
        return f'{self.id}. Date - {self.creation_date}. {self.name}. {self.is_created}'

    def get_absolute_url(self):
        return f'/data_sets/{self.id}'

class ColumnItem(models.Model):

    """Columns added to schema"""

    col_name = models.CharField(max_length=50, blank=True, null=True)
    schema = models.ForeignKey(Schema, related_name='columns', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)
    range_min = models.PositiveIntegerField(blank=True, null=True)
    range_max = models.PositiveIntegerField(blank=True, null=True)
    col_type = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)

    class Meta:
        ordering = ('order',)

    def get_absolute_url(self):
        return f'/{self.schema.id}/update'

    def __str__(self):
        return f'{self.id}'

