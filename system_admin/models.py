from django.db import models


# Create your models here.
class Voters(models.Model):
    VoterId = models.TextField(null=True)
    VoterFirstName = models.TextField(null=True)
    VoterMiddleName = models.TextField(null=True)
    VoterLastName = models.TextField(null=True)
    ResidenceStreetNumber = models.TextField(null=True)
    ResidenceStreetName = models.TextField(null=True)
    ResidenceApartment = models.TextField(null=True)
    ResidenceCity = models.TextField(null=True)
    ResidenceState = models.TextField(null=True)
    ResidenceFullZip = models.TextField(null=True)
    DobFormatted = models.TextField(null=True)
    VoterSex = models.TextField(null=True)
    VoterAreaCode = models.TextField(null=True)
    VoterPhone = models.TextField(null=True)
    VoterEMail = models.TextField(null=True)
    VoterPartyCode = models.TextField(null=True)
    MailingAddress1 = models.TextField(null=True)
    MailingCity = models.TextField(null=True)
    MailingState = models.TextField(null=True)
    MailingZip = models.TextField(null=True)
    ResidenceStreetAddress = models.TextField(null=True)
    RegistrationDateFormatted = models.TextField(null=True)
    VoterTownCode = models.TextField(null=True)
    VoterDistrictCode = models.TextField(null=True)
    VoterStateLegislativeDistrictCode = models.TextField(null=True)
