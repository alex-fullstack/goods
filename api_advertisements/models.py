from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def __str__(self):
        return str(self.name)


class Photo(models.Model):
    image = models.ImageField(upload_to='advertisements/', null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)


class Advertisement(models.Model):
    name = models.CharField(blank=False, null=False, max_length=200)
    view_counter = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tag = models.ManyToManyField(Tag, related_name='tag', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, related_name='photo', blank=True, null=True)

    def update_counter(self):
        self.view_counter += 1
        self.save(update_fields=['view_counter'])

    def __str__(self):
        return str(self.name)
