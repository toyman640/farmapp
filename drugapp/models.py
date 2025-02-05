from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

class Unit(models.Model):
  name = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.name

class Drug(models.Model):
  manufacturer_name = models.CharField(max_length=255)
  drug_name = models.CharField(max_length=255)
  batch_number = models.CharField(max_length=100, unique=True)
  manufacturing_date = models.DateField()
  expiry_date = models.DateField()
  quantity = models.PositiveIntegerField()
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  restock_quantity_notify = models.PositiveIntegerField()

  def __str__(self):
    return f"{self.drug_name} ({self.batch_number})"

  def needs_restock(self):
    return self.quantity <= self.restock_quantity_notify

  def is_expiring_soon(self):
    return now().date() >= self.expiry_date - timedelta(days=7)

# class Dispatch(models.Model):
#   drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
#   quantity = models.PositiveIntegerField()
#   unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
#   dispatched_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#   dispatched_at = models.DateTimeField(auto_now_add=True)

#   def __str__(self):
#     return f"Dispatched {self.quantity} {self.unit} of {self.drug.drug_name}"

#   def save(self, *args, **kwargs):
#     if self.pk is None:
#         drug = self.drug
#         if drug.quantity >= self.quantity:
#             drug.quantity -= self.quantity
#             drug.save()
#         else:
#             raise ValueError("Not enough stock to dispatch")

#     super().save(*args, **kwargs)


class Dispatch(models.Model):
  drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  dispatched_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  dispatched_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Dispatched {self.quantity} {self.unit} of {self.drug.drug_name}"

  def save(self, *args, **kwargs):
    if self.pk:  # If updating an existing dispatch
      original = Dispatch.objects.get(pk=self.pk)
      quantity_diff = self.quantity - original.quantity  # Find the difference

      # Update the drug quantity accordingly
      if self.drug.quantity >= quantity_diff:
        self.drug.quantity -= quantity_diff
        self.drug.save()
      else:
        raise ValueError("Not enough stock to update dispatch quantity")

    else:  # If creating a new dispatch
      if self.drug.quantity >= self.quantity:
        self.drug.quantity -= self.quantity
        self.drug.save()
      else:
        raise ValueError("Not enough stock to dispatch")

    super().save(*args, **kwargs)