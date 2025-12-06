# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    
    def __str__(self):
        return self.username



# CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# TAG
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

# POST
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('published', 'Published')
    ], default='draft')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.id)])

    def is_published(self):
        return self.status == 'published'

    def summary(self):
        return self.content[:150] + "..."

    def word_count(self):
        return len(self.content.split())

    def reading_time(self):
        words = len(self.content.split())
        return max(1, round(words / 200))

    def get_next(self):
        return Post.objects.filter(id__gt=self.id).order_by('id').first()

    def get_previous(self):
        return Post.objects.filter(id__lt=self.id).order_by('-id').first()

    def publish(self):
        self.status = 'published'
        self.save()

    # def display_tags(self):
    #     return ", ".join(tag.name for tag in self.tags.all()[:3])
    # display_tags.short_description = 'Tags'
    


# COMMENT
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    # def approve(self):
    #     self.approved = True
    #     self.save()
    def short_content(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content
    

# LIKES
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'Like by {self.user} on {self.post}'