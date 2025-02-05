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


class Dispatch(models.Model):
  drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  dispatched_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  dispatched_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Dispatched {self.quantity} {self.unit} of {self.drug.drug_name}"

  # def save(self, *args, **kwargs):
    if self.pk:  # If updating an existing dispatch
        original = Dispatch.objects.get(pk=self.pk)

        # First, restore the previous dispatch quantity back to the drug stock
        if original.quantity != self.quantity:
            self.drug.quantity += original.quantity  # Add the old quantity back to stock
            self.drug.save()

            # Now check if the new quantity is valid (not greater than the available stock)
            if self.drug.quantity >= self.quantity:
                self.drug.quantity -= self.quantity  # Subtract the new quantity
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
  def save(self, *args, **kwargs):
    if self.pk:  # If updating an existing dispatch
      original = Dispatch.objects.get(pk=self.pk)
      original_drug = original.drug  # Store the previous drug
      
      # Check if the drug has changed
      if original_drug != self.drug:
        # Restore the previous drug's quantity back to stock
        original_drug.quantity += original.quantity
        original_drug.save()

        # Ensure that the new drug has enough stock
        if self.drug.quantity >= self.quantity:
          self.drug.quantity -= self.quantity  # Subtract the new quantity from the new drug
          self.drug.save()
        else:
            raise ValueError("Not enough stock to dispatch the new drug")

      else:  # If the drug didn't change, just handle the quantity change
        if original.quantity != self.quantity:
          # Restore the previous quantity back to the drug stock
          self.drug.quantity += original.quantity  # Add the old quantity back
          self.drug.save()

          # Now check if the new quantity is valid (not greater than the available stock)
          if self.drug.quantity >= self.quantity:
            self.drug.quantity -= self.quantity  # Subtract the new quantity
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

  def delete(self, *args, **kwargs):
    """Restore quantity to the drug when dispatch is deleted"""
    drug = self.drug
    drug.quantity += self.quantity
    drug.save()
    super().delete(*args, **kwargs)