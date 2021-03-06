import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates rooms"

    # add_arguments = 커맨드에 인자를 추가하는 메서드
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create?",
        )

    # handle = 커스텀 커맨드를 실행하는 메서드
    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                # lambda는 자바스크립트에서 익명함수와 같은 역할을 한다
                # faker는 seeder에 내장되어 있는 라이브러리이다
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 20),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        # room을 만들고 만든 룸을 Room모델에서 찾는다
        # 찾은 room을 토대로 사진들을 생성함
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(0, random.randint(5, 10)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    # Foreign Key를 가능하게 하기 위함
                    room=room,
                    file=f"room_photos/{random.randint(1, 60)}.jpg",
                )
            for amenity in amenities:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    # Many to Many Field에 추가하기 위함
                    room.amenities.add(amenity)
            for facility in facilities:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    # Many to Many Field에 추가하기 위함
                    room.facilities.add(facility)
            for rule in rules:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    # Many to Many Field에 추가하기 위함
                    room.house_rules.add(rule)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
