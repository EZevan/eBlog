import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.db.models.signals import pre_delete  # delete files
from django.dispatch.dispatcher import receiver  # delete files


# Create your models here.

# Website info table
class BaseModel(models.Model):
    """
    The base class for all models
    """
    # id = models.AutoField(primary_key=True)
    # Use uuid.uuid1().hex as primary key, which contain host id(MAC address) and current timestamp
    id = models.UUIDField(primary_key=True, null=False, auto_created=True, default=uuid.uuid1().hex)
    version = models.IntegerField(verbose_name="version number")
    create_time = models.DateTimeField(max_length=32, auto_now_add=True, verbose_name="creation time")
    create_by = models.CharField(max_length=15, verbose_name="creator name")
    update_time = models.DateTimeField(max_length=32, auto_now=True, verbose_name="update time")
    update_by = models.CharField(max_length=15, verbose_name="update by user")
    is_deleted = models.BooleanField(
        max_length=10,
        verbose_name="the flag of deleted or not; 0 means not deleted,1 means deleted")

    class Meta:
        # the abstract equals to True means that the base class won't be created database table by default
        abstract = True


class Website(BaseModel):
    """
    The website information, including website title,website record number,website version,etc.
    """
    title = models.CharField(max_length=50, verbose_name="website title")
    abstract = models.CharField(max_length=225, verbose_name="website brief introduction")
    key_words = models.CharField(max_length=50, verbose_name="website key word")
    record_number = models.CharField(max_length=32, verbose_name="website record number")
    version_number = models.CharField(max_length=15, verbose_name="website version number")
    icon = models.FileField(verbose_name="website icon", upload_to="website_icon/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "website info"


# My detailed info
class MyInfo(BaseModel):
    """
    Personal detailed information
    """
    name = models.CharField(max_length=15, verbose_name="Name")
    occupation = models.CharField(max_length=50, verbose_name="occupation")
    email = models.EmailField(max_length=50, verbose_name="email address")
    website_url = models.CharField(max_length=200, verbose_name="website link")
    address = models.CharField(max_length=50, verbose_name="address")
    bilibili_url = models.URLField(verbose_name="Bilibili link")
    github_url = models.URLField(verbose_name="Github link")
    webchat_img = models.FileField(verbose_name="Wechat images", upload_to="my_info/")
    qq_img = models.FileField(verbose_name="QQ images", upload_to="my_info/")

    class Meta:
        verbose_name_plural = "My detailed information"


# User info
class UserInfo(AbstractUser, BaseModel):
    """
    User information
    """
    signup_choice = (
        (0, "Account and password"),
        (1, "Mobile phone number"),
        (2, "Email"),
        (3, "QQ"),
        (4, "Wechat")
    )
    nick_name = models.CharField(max_length=15, verbose_name="nickname")
    user_signup_way = models.IntegerField(default=0, choices=signup_choice, verbose_name="the ways of signup")
    mobile = models.CharField(max_length=15, null=True, blank=True, verbose_name="mobile phone number")
    membership_points = models.IntegerField(default=0, verbose_name="membership points")
    token = models.UUIDField(default=uuid.uuid1().hex, null=True, blank=True, verbose_name="user token")
    avatar = models.ForeignKey(
        to="Avatar",
        to_field="id",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="User avatar id"
    )
    favorites = models.ManyToManyField(
        to="Article",
        verbose_name="The favorite articles of users"
    )

    class Meta:
        verbose_name_plural = "User information"


class Avatar(BaseModel):
    """
    User avatars
    """
    url = models.FileField(verbose_name="the path saved user avatar", upload_to="avatar/")

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = "User avatars"


@receiver(pre_delete, sender=Avatar)  # sender = the class which you want to delete or modify file field belongs to
def on_delete_avatar(instance, **kwargs):
    """
    This function will delete corresponding file while deleting avatar
    :param instance:
    :param kwargs:
    """
    instance.url.delete(False)


class Article(BaseModel):
    """
    Blog articles
    """
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name="article title")
    abstract = models.CharField(max_length=100, null=True, blank=True, verbose_name="article abstract")
    content = models.TextField(null=True, blank=True, verbose_name="article content")
    status_choice = (
        (0, "UNPUBLISHED"),
        (1, "PUBLISHED")
    )
    status = models.IntegerField(choices=status_choice)
    is_recommendation = models.BooleanField(default=True, verbose_name="recommended or not")
    cover = models.ForeignKey(
        to="Cover",
        to_field="id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="article cover"
    )
    read_times = models.IntegerField(default=0, verbose_name="read times of article")
    comment_counts = models.IntegerField(default=0, verbose_name="comment counts of article")
    likes_counts = models.IntegerField(default=0, verbose_name="the counts of likes for the article")
    favorites_counts = models.IntegerField(default=0, verbose_name="the counts of favorites for the article")
    category_choice = (
        (0, "DEVELOPMENT"),
        (1, "TEST"),
        (2, "DEVOPS")
    )
    category = models.IntegerField(null=True, blank=True, choices=category_choice, verbose_name="article category")
    tag = models.ManyToManyField(
        to="Tag",
        blank=True,
        verbose_name="article tags"
    )
    author = models.CharField(max_length=15, null=True, blank=True, verbose_name="article author")
    source = models.CharField(max_length=50, null=True, blank=True, verbose_name="article  source")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Articles"


class Comment(BaseModel):
    """
    Article comments
    """
    likes_counts = models.IntegerField(default=0, verbose_name="the counts of likes for the comment")
    article = models.ForeignKey(
        to="Article",
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name="comment on the corresponding article"
    )
    user = models.ForeignKey(
        to="UserInfo",
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name="comment user"
    )
    comment_content = models.TextField(null=True, blank=True, verbose_name="comment content")
    comment_counts = models.IntegerField(default=0, verbose_name="comment counts")
    illustration = models.TextField(null=True, blank=True, verbose_name="illustration in comment")
    parent_comment_content = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="parent level comment content"
    )

    def __str__(self):
        return self.comment_content

    class Meta:
        verbose_name_plural = "Article comments"


class News(BaseModel):
    """
    the news from third-party website, such as sina news
    """

    class Meta:
        verbose_name_plural = "crawled news from third party"


class Cover(BaseModel):
    """
    Article cover
    """
    cover_url = models.FileField(verbose_name="the url address of article cover images", upload_to="article_img/")

    def __str__(self):
        return str(self.cover_url)

    class Meta:
        verbose_name_plural = "Article cover images"


class Tag(BaseModel):
    """
    Article tags
    """
    name = models.CharField(max_length=20, verbose_name="tag name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Article tags"


class Memories(BaseModel):
    """
    Memories; History event
    """
    title = models.CharField(max_length=50, verbose_name="memories title")
    content = models.TextField(verbose_name="memories content")
    illustration = models.TextField(null=True, blank=True, verbose_name="illustration groups,delimit with semicolon")

    class Meta:
        verbose_name_plural = "Memories"


class Navigation(BaseModel):
    """
    Website navigation
    """
    nav_category = models.ForeignKey(
        to="NavigationCategory",
        to_field="id",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="website navigation category"
    )
    icon = models.FileField(
        null=True, blank=True, upload_to="website_icon/", verbose_name="website icon"
    )
    icon_href = models.URLField(help_text="Online link", null=True, blank=True, verbose_name="icon href")
    title = models.CharField(max_length=50, verbose_name="website title")
    abstract = models.CharField(max_length=200, null=True, verbose_name="website abstract")
    website_href = models.URLField(null=True, verbose_name="website href")
    status_choice = (
        (0, "PENDING"),
        (1, "APPROVAL"),
        (2, "REJECTED")
    )
    status = models.IntegerField(choices=status_choice, default=0, verbose_name="website navigation status")

    def color_state(self):
        if self.status == 0:
            assign_state_name = "Pending approval"
            color = "#ec921e"
        elif self.status == 1:
            assign_state_name = "Approval"
            color = "green"
        else:
            assign_state_name = "Rejected",
            color = "red"
        return format_html(
            '<span style="color:{};">{}</span>',
            color,
            assign_state_name
        )

    color_state.short_description = "Navigation status"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Navigation categories"


class NavigationCategory(BaseModel):
    """
    Navigation categories
    """
    name = models.CharField(max_length=50, verbose_name="category name")
    icon = models.CharField(max_length=50, verbose_name="category icon")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Navigation categories"


class Menu(BaseModel):
    """
    Website menu information
    """
    menu_name = models.CharField(max_length=50, null=True, verbose_name="chinese menu name")
    menu_name_en = models.CharField(max_length=50, null=True, verbose_name="english menu name")
    slogan = models.CharField(max_length=50, null=True, verbose_name="website slogan")
    slogan_abstract = models.CharField(max_length=100, null=True,
                                       help_text="delimit with semicolon for multiple slogan")
    is_rotate_slogan = models.BooleanField(default=False, verbose_name="rotating slogan abstract or not")
    background_img = models.ManyToManyField(
        to="MenuImg",
        help_text="can be set multiple background images",
        verbose_name="menu background images"
    )
    is_rotate_background = models.BooleanField(
        help_text="rotation by default if there are multiple images",
        default=False, verbose_name="rotating background images or not"
    )
    rotation_interval = models.IntegerField(
        help_text="rotation interval,default is 10 seconds",
        default=10, verbose_name="rotating background images interval"
    )

    class Meta:
        verbose_name_plural = "Website menu information"


class MenuImg(BaseModel):
    """
    Website background images
    """
    img_url = models.FileField(upload_to="website_bg/")

    def __str__(self):
        return str(self.img_url)

    class Meta:
        verbose_name_plural = "Website background images"


class Promotion(BaseModel):
    """
    Website promotion information, such as some Ads.
    """
    name = models.CharField(max_length=50, null=True, verbose_name="product name")
    href = models.URLField(verbose_name="promotion link")
    illustration = models.FileField(
        null=True, blank=True, help_text="single image",
        upload_to="promotion/", verbose_name="promotion illustration url"
    )
    illustration_list = models.TextField(
        null=True, blank=True, verbose_name="promotion illustration group",
        help_text="Please delimit with semicolon for multiple illustration url"
    )
    is_show = models.BooleanField(default=True, verbose_name="show the illustration or not")
    owner = models.CharField(max_length=50, null=True, blank=True, verbose_name="the owner of promotion")
    abstract = models.CharField(max_length=200, null=True, blank=True, verbose_name="promotion abstract")

    class Meta:
        verbose_name_plural = "Website promotion information"


class Feedback(BaseModel):
    """
    Website visitor feedback
    """
    email = models.EmailField(verbose_name="contact email")
    content = models.TextField(verbose_name="feedback content")
    status = models.BooleanField(default=False, verbose_name="feedback status; 0 - no reply, 1 - replied")
    reply_content = models.TextField(null=True, blank=True, verbose_name="reply content")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "Website visitor feedback"
