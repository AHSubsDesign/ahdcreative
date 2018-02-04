import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from . import managers
# Create your models here.


@python_2_unicode_compatible
class License(models.Model):
    """
    A license in use for a project.
    This model is related through Version instead of directly on
    Project, in order to support re-licensing the project with a new
    version.
    """
    name = models.CharField(max_length=255,
                            unique=True)
    slug = AutoSlugField(populate_from='name')
    link = models.URLField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Project(models.Model):
    """ A software project """

    HIDDEN_STATUS = 0
    PUBLIC_STATUS = 1
    STATUS_CHOICES = (
                      (HIDDEN_STATUS, 'Hidden'),
                      (PUBLIC_STATUS, 'Public'),
                      )
    WEB_DESIGN = 2
    GRAPHIC = 3
    APP = 4
    CATEGORY_CHOICES = (
                        (GRAPHIC, 'Graphic'),
                        (WEB_DESIGN, 'Web Design'),
                        (APP, 'App'),
                        )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = AutoSlugField(populate_from='name')
    status = models.IntegerField(choices=STATUS_CHOICES, default=PUBLIC_STATUS, verbose_name=_("status"))
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=WEB_DESIGN, verbose_name=_("category"))
    description = models.TextField(verbose_name=_("description"))
    package_link = models.URLField(blank=True, null=True, verbose_name=_("package_link"), help_text=_("URL of the project"))

    objects = managers.ProjectQuerySet.as_manager()

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ('name',)

    def __str__(self):
        return self.name


class Version(models.Model):
    """ A version for a Project """

    PLANNING_STATUS = 1
    PRE_ALPHA_STATUS = 2
    ALPHA_STATUS = 3
    BETA_STATUS = 4
    STABLE_STATUS = 5

    STATUS_CHOICES = (
        (PLANNING_STATUS, 'Planning'),
        (PRE_ALPHA_STATUS, 'Pre-Alpha'),
        (ALPHA_STATUS, 'Alpha'),
        (BETA_STATUS, 'Beta'),
        (STABLE_STATUS, 'Stable'),
    )
    project = models.ForeignKey(Project, related_name='versions',
                                verbose_name=_("project"))
    version = models.CharField(max_length=255, verbose_name=_("version"))
    is_latest = models.BooleanField(default=False, help_text=_("latest"))
    status = models.IntegerField(choices=STATUS_CHOICES, default=STABLE_STATUS)
    license = models.ForeignKey(License, verbose_name=_("license"))
    release_date = models.DateField(default=datetime.date.today,
                                    verbose_name=_("release date"))

    objects = managers.VersionManager

    class Meta:
        verbose_name=_("version")
        verbose_name_plural = _("versions")
        ordering = ('project', 'version')
        unique_together = ('project', 'version')

    def __str__(self):
        return "%s %s" % (self.project, self.version)

        @models.permalink
        def get_absolute_url(self):
            return ('projects_version_detail', (), {
                    'project_slug': self.project.slug,
                    'slug': self.version
                    })
