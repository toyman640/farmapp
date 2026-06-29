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
  unit_quantity_or_amount = models.CharField(max_length=100, blank=True, null=True)
  quantity_per_pack = models.PositiveIntegerField(blank=True, null=True)
  quantity = models.PositiveIntegerField()
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  restock_quantity_notify = models.PositiveIntegerField()
  entered_at = models.DateTimeField(auto_now_add=True)
  has_been_edited = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.drug_name} ({self.batch_number})"

  def get_pack_and_pieces(self):
    if self.quantity_per_pack and self.quantity_per_pack > 0:
      packs = self.quantity // self.quantity_per_pack
      pieces = self.quantity % self.quantity_per_pack
      return f"{packs} pack(s) {pieces} piece(s)"
    return f"{self.quantity} piece(s)"

  def needs_restock(self):
    return self.quantity <= self.restock_quantity_notify

  def is_expiring_soon(self):
    return now().date() >= self.expiry_date - timedelta(days=7)

  def update_stock_absolute(self, new_value, user):
    """Used by Admin to set the quantity to a specific number (e.g., 500 -> 50)."""
    previous_quantity = self.quantity
    self.quantity = new_value
    self.save()
    
    InventoryLog.objects.create(
        drug=self, previous_quantity=previous_quantity, 
        new_quantity=new_value, updated_by=user
    )

  def update_stock_additive(self, addition, user):
    """Used to add quantity (e.g., 500 + 50 = 550)."""
    previous_quantity = self.quantity
    new_value = previous_quantity + addition
    self.quantity = new_value
    self.save()
    
    InventoryLog.objects.create(
        drug=self, previous_quantity=previous_quantity, 
        new_quantity=new_value, updated_by=user
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

    def save(self, *args, **kwargs):
        """Adjust drug stock safely after saving."""
        if self.pk:  # updating existing dispatch
            original = Dispatch.objects.get(pk=self.pk)
            original_drug = original.drug

            # If drug changed, restore old and deduct new
            if original_drug != self.drug:
                original_drug.quantity += original.quantity
                original_drug.save()
                self.drug.quantity -= self.quantity
                self.drug.save()
            else:
                # drug same → adjust for quantity change
                if original.quantity != self.quantity:
                    self.drug.quantity += original.quantity
                    self.drug.quantity -= self.quantity
                    self.drug.save()
        else:  # new dispatch
            self.drug.quantity -= self.quantity
            self.drug.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Restore quantity when a dispatch is deleted."""
        self.drug.quantity += self.quantity
        self.drug.save()
        super().delete(*args, **kwargs)



# # --- Choices ---
# SECTION_CHOICES = [
#   ("piggery", "Piggery"),
#   ("paddock", "Paddock"),
#   ("small_ruminant", "Small Ruminant"),
# ]

# TAG_CHOICES = [
#   ("pregnant", "Pregnant"),
#   ("nursing_mother", "Nursing Mother"),
# ]


# # --- Reference Models ---
# class Animal(models.Model):
#   name = models.CharField(max_length=50)  # e.g. Sow, Cow, Ram
#   section = models.CharField(max_length=50, choices=SECTION_CHOICES)

#   def __str__(self):
#     return f"{self.name} ({self.get_section_display()})"


# class Location(models.Model):
#   name = models.CharField(max_length=50)  # e.g. Line 1, Paddock 2, Ewe 3
#   section = models.CharField(max_length=50, choices=SECTION_CHOICES)

#   def __str__(self):
#     return f"{self.name} ({self.get_section_display()})"


# class Event(models.Model):
#   code = models.CharField(max_length=50)       # internal name e.g. "farrowing"
#   name = models.CharField(max_length=50)       # display name e.g. "Farrowing"
#   section = models.CharField(max_length=50, choices=SECTION_CHOICES)

#   def __str__(self):
#     return f"{self.name} ({self.get_section_display()})"


# class Treatment(models.Model):
#   TREATMENT_CHOICES = [
#     ("vaccination", "Vaccination"),
#     ("deworming", "Deworming"),
#     ("general", "General Treatment"),
#     ("emergency", "Emergencies"),
#   ]

#   treatment_type = models.CharField(max_length=50, choices=TREATMENT_CHOICES)
#   description = models.TextField(blank=True, null=True)

#   def __str__(self):
#     return self.get_treatment_type_display()


# # --- Main Record ---
# class Record(models.Model):
#   date = models.DateField(auto_now_add=True)
#   section = models.CharField(max_length=50, choices=SECTION_CHOICES)

#   event = models.ForeignKey(Event, on_delete=models.CASCADE)
#   animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True)
#   location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
#   treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)

#   tag = models.CharField(max_length=50, choices=TAG_CHOICES, blank=True, null=True)
#   comment = models.TextField(blank=True, null=True)

#   def __str__(self):
#     return f"{self.get_section_display()} - {self.event.name} ({self.date})"