from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command creates amenities"

    """ 
    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that I love?"
        ) 
    """

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon Monoxide Detectors",
            "Chairs",
            "Coffee Maker",
            "Cooking Hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double Bed",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot Tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Oven",
            "Queen Size Bed",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Toilet",
            "Towels",
            "TV",
        ]
        for amenity in amenities:
            Amenity.objects.get_or_create(name=amenity)
        self.stdout.write(self.style.SUCCESS(f"{len(amenities)} amenities created!"))
