"""
Personnel models for staff management.

This file contains all models related to personnel management including:
- Employee: Main model for employee information
- Qualification: Employee qualifications and certifications
- Training: Employee training records
"""
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from company.models import Department

class Employee(models.Model):
    """Model representing an employee."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                               related_name='personnel_profile', null=True, blank=True)
    employee_id = models.CharField(max_length=50, unique=True, verbose_name=_("Employee ID"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    position = models.CharField(max_length=100, verbose_name=_("Position"))
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='employees', verbose_name=_("Department"))
    email = models.EmailField(verbose_name=_("Email"), blank=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    hire_date = models.DateField(null=True, blank=True, verbose_name=_("Hire Date"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.employee_id})"


class Qualification(models.Model):
    """Model representing an employee qualification."""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                               related_name='qualifications', verbose_name=_("Employee"))
    qualification_type = models.CharField(max_length=100, verbose_name=_("Qualification Type"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    issue_date = models.DateField(verbose_name=_("Issue Date"))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_("Expiry Date"))
    issuing_organization = models.CharField(max_length=255, blank=True, verbose_name=_("Issuing Organization"))
    certificate_number = models.CharField(max_length=100, blank=True, verbose_name=_("Certificate Number"))
    document = models.FileField(upload_to='qualification_documents/', null=True, blank=True, 
                              verbose_name=_("Document"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Qualification")
        verbose_name_plural = _("Qualifications")
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.employee} - {self.qualification_type}"


class Training(models.Model):
    """Model representing an employee training."""
    TRAINING_STATUS_CHOICES = [
        ('PLANNED', _('Planned')),
        ('IN_PROGRESS', _('In Progress')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                               related_name='training_records', verbose_name=_("Employee"))
    training_name = models.CharField(max_length=255, verbose_name=_("Training Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))
    status = models.CharField(max_length=20, choices=TRAINING_STATUS_CHOICES, default='PLANNED', 
                            verbose_name=_("Status"))
    provider = models.CharField(max_length=255, blank=True, verbose_name=_("Training Provider"))
    certificate_issued = models.BooleanField(default=False, verbose_name=_("Certificate Issued"))
    certificate_number = models.CharField(max_length=100, blank=True, verbose_name=_("Certificate Number"))
    certificate_date = models.DateField(null=True, blank=True, verbose_name=_("Certificate Date"))
    certificate_document = models.FileField(upload_to='training_certificates/', null=True, blank=True, 
                                          verbose_name=_("Certificate Document"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Training")
        verbose_name_plural = _("Training Records")
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee} - {self.training_name}"


class EmployeeRecord(models.Model):
    """Model representing an employee record or document."""
    RECORD_TYPES = [
        ('CONTRACT', _('Employment Contract')),
        ('AGREEMENT', _('Agreement')),
        ('ASSESSMENT', _('Performance Assessment')),
        ('DISCIPLINARY', _('Disciplinary Action')),
        ('AWARD', _('Award or Recognition')),
        ('OTHER', _('Other Document')),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                               related_name='employee_records', verbose_name=_("Employee"))
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES, verbose_name=_("Record Type"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    issue_date = models.DateField(verbose_name=_("Issue Date"))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_("Expiry Date"))
    document = models.FileField(upload_to='employee_records/', null=True, blank=True, 
                              verbose_name=_("Document"))
    is_confidential = models.BooleanField(default=False, verbose_name=_("Confidential"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _("Employee Record")
        verbose_name_plural = _("Employee Records")
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.employee} - {self.get_record_type_display()}: {self.title}"


class Education(models.Model):
    """Model representing an employee's educational background."""
    EDUCATION_LEVELS = [
        ('HIGH_SCHOOL', _('High School')),
        ('VOCATIONAL', _('Vocational School')),
        ('BACHELOR', _('Bachelor\'s Degree')),
        ('MASTER', _('Master\'s Degree')),
        ('DOCTORATE', _('Doctorate')),
        ('OTHER', _('Other')),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, 
                               related_name='education', verbose_name=_("Employee"))
    institution = models.CharField(max_length=255, verbose_name=_("Educational Institution"))
    level = models.CharField(max_length=20, choices=EDUCATION_LEVELS, verbose_name=_("Education Level"))
    field_of_study = models.CharField(max_length=255, blank=True, verbose_name=_("Field of Study"))
    degree = models.CharField(max_length=255, blank=True, verbose_name=_("Degree"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))
    is_completed = models.BooleanField(default=True, verbose_name=_("Completed"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    document = models.FileField(upload_to='education_documents/', null=True, blank=True, 
                              verbose_name=_("Diploma/Certificate"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Education")
        ordering = ['-end_date', '-start_date']
    
    def __str__(self):
        return f"{self.employee} - {self.degree} ({self.institution})"
