import datetime

from contact.tasks import send_mail as celery_send_mail

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse


class MailToAdmin(models.Model):
    username = models.CharField(max_length=100)
    text = models.TextField()
    from_mail = models.EmailField()
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.text


class Post(models.Model):
    header = models.CharField(max_length=200)
    short_description = models.TextField()
    image = models.ImageField()
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.header

    def published_comments_count(self):
        cnt = Comment.objects.filter(post=self.id, is_published=True).count()
        return cnt


class Comment(models.Model):
    username = models.CharField(max_length=100)
    text = models.TextField()
    is_published = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


@receiver(post_save, sender=Post)
def post_handler(sender, **kwargs):
    new = kwargs["created"]
    if new:
        inst = kwargs["instance"]
        subject = 'New post added'
        from_email = 'sergemk@entecheco.com'
        recipient_list = [settings.ADMINS[1]]
        message = f'User {inst.user} has added a post "{inst.header}"'
        celery_send_mail.apply_async((subject, message, from_email, recipient_list))


@receiver(post_save, sender=Comment)
def comment_post_save_handler(sender, **kwargs):
    new = kwargs["created"]
    inst = kwargs["instance"]
    if new:
        subject = 'New comment added'
        from_email = 'sergemk@entecheco.com'
        recipient_list = [settings.ADMINS[1]]
        message = f'User {inst.username} has added a comment on post "{inst.post.header}"'
        celery_send_mail.apply_async((subject, message, from_email, recipient_list))


@receiver(pre_save, sender=Comment)
def comment_pre_save_handler(sender, **kwargs):
    inst = kwargs["instance"]
    if inst.is_published and not Comment.objects.get(id=inst.id).is_published:
        subject = 'New comment is approved by admin'
        from_email = 'sergemk@entecheco.com'
        recipient_list = [inst.post.user.email]
        message = f'User {inst.username} has added a comment on post "{inst.post.header}"\n' \
                  f'Link to post: {reverse("post_detail", kwargs={"pk": inst.post.id})}'
        celery_send_mail.apply_async((subject, message, from_email, recipient_list))


@receiver(post_save, sender=MailToAdmin)
def mailtoadmin_handler(sender, **kwargs):
    new = kwargs["created"]
    if new:
        inst = kwargs["instance"]
        subject = 'Message from user ' + inst.username
        from_email = inst.from_mail
        recipient_list = [settings.ADMINS[1]]
        message = inst.text
        celery_send_mail.apply_async((subject, message, from_email, recipient_list))
