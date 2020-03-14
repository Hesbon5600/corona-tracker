from django.db import models
from .push_id import PushID


class BaseModel(models.Model):
    """
    The common field in all the models are defined here
    """
    # Add id to every entry in the database
    id = models.CharField(db_index=True, max_length=255,
                          unique=True, primary_key=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # add deleted option for every entry
    deleted = models.BooleanField(default=False)

    def save(self,*args, **kwargs): # pylint: disable=W0221
        push_id = PushID()
        # This to check if it creates a new or updates an old instance
        if not self.id:
            self.id = push_id.next_id()
        super(BaseModel, self).save() # pylint: disable=W0221

    class Meta:
        abstract = True  # Set this model as Abstract
