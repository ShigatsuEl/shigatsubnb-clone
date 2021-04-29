from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = "This command creates facilities"

    """ 
    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that I love?"
        ) 
    """

    def handle(self, *args, **options):
        facilities = [
            "Elevator",
            "Free parking",
            "Gym",
            "Samll Banquet",
            "Amuse Restaurant",
            "Cafe",
            "Conference Room",
            "Public Service Lounge",
            "Fitness",
            "Swimming Pool",
            "Free Breakfast",
            "Airport Transfer",
            "Luggage Storage",
            "Massage Shop",
            "Bar",
            "Souvenir Shop",
            "Rent Car",
            "Concierge",
            "Laundry",
            "Valet Parking",
            "Taxi Service",
            "Snack Bar",
            "Children Area",
        ]
        for facility in facilities:
            Facility.objects.get_or_create(name=facility)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!"))
