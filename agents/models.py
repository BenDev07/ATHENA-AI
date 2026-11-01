from django.db import models

# Create your models here.

class Reclamation(models.Model):

    id = models.AutoField(primary_key=True)

    client_name = models.CharField(max_length=150)

    description = models.TextField()
    agent_response = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=50,
        default="En attente"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "reclamations"

    def __str__(self):
        return self.client_name