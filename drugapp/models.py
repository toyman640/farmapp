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
  drug_name = models.CharField(max_length=255, unique=True)
  batch_number = models.CharField(max_length=100, unique=True)
  manufacturing_date = models.DateField()
  expiry_date = models.DateField()
  quantity = models.PositiveIntegerField()
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  restock_quantity_notify = models.PositiveIntegerField()
  entered_at = models.DateTimeField(auto_now_add=True)
  has_been_edited = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.drug_name} ({self.batch_number})"

  def needs_restock(self):
    return self.quantity <= self.restock_quantity_notify

  def is_expiring_soon(self):
    return now().date() >= self.expiry_date - timedelta(days=7)

  # def update_stock(self, new_quantity, user):
    """
    Update stock correctly:
    - If increasing stock, add to previous quantity.
    - If correcting a mistake, allow user to adjust last entry.
    """
    if new_quantity < 0:
        raise ValueError("Stock quantity cannot be negative")

    # Log previous quantity before updating
    previous_quantity = self.quantity

    # Update drug stock
    self.quantity = new_quantity
    self.has_been_edited = False
    self.save()

    # Log the inventory change
    InventoryLog.objects.create(
        drug=self,
        previous_quantity=previous_quantity,
        new_quantity=new_quantity,
        updated_by=user
    )

  def request_stock_update(self, new_quantity, user):
    if new_quantity < 0:
      raise ValueError("Stock quantity cannot be negative")

    if user.is_staff or user.is_superuser:
      # Directly update stock for staff and superusers
      previous_quantity = self.quantity
      self.quantity = new_quantity
      self.has_been_edited = False
      self.save()

      InventoryLog.objects.create(
        drug=self,
        previous_quantity=previous_quantity,
        new_quantity=new_quantity,
        updated_by=user
      )
    else:
      # Store as pending update for non-staff users
      PendingStockUpdate.objects.create(
        drug=self,
        requested_quantity=new_quantity,
        requested_by=user
      )

  def correct_stock(self, correct_quantity, user):
    """
    Correct stock in case of data entry errors.
    - If there's a previous stock update, revert to the quantity before that update.
    - Then apply the new correction.
    - If no previous stock updates exist, adjust based on the original quantity.
    """
    last_log = self.inventory_logs.order_by('-updated_at').first()  # Get last stock update

    if last_log:
      # Get the correct reverted quantity
      reverted_quantity = last_log.previous_quantity + self.quantity
    else:
        # If no previous updates, use the existing quantity
      reverted_quantity = self.quantity

    # Compute new stock level correctly
    new_stock_level = reverted_quantity

    # Ensure stock is not negative
    if new_stock_level < 0:
        raise ValueError("Stock quantity cannot be negative.")

    # Log previous quantity
    previous_quantity = self.quantity

    # Update drug stock
    self.quantity = new_stock_level
    self.has_been_edited = True
    self.save()

    # Log the inventory correction
    InventoryLog.objects.create(
        drug=self,
        previous_quantity=previous_quantity,
        new_quantity=self.quantity,
        updated_by=user
    )



class InventoryLog(models.Model):
  drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name="inventory_logs")
  previous_quantity = models.PositiveIntegerField()
  new_quantity = models.PositiveIntegerField()
  updated_at = models.DateTimeField(auto_now=True)
  updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return f"{self.drug.drug_name}: {self.previous_quantity} → {self.new_quantity}"


class PendingStockUpdate(models.Model):
  drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name="pending_updates")
  requested_quantity = models.PositiveIntegerField()
  requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  requested_at = models.DateTimeField(auto_now_add=True)
  approved = models.BooleanField(default=False)

  def __str__(self):
    return f"Pending update for {self.drug.drug_name}: {self.requested_quantity}"



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