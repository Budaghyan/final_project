from django.core.management.base import BaseCommand, CommandError
from quotes.services import QuotesScraper
from quotes.models import Quotes
from tags.models import Tags
from user.models import User


class Command(BaseCommand):
    help = 'Management commands to scrap quotes'

    def handle(self, *args, **options):
        scraper = QuotesScraper(url='https://quotes.toscrape.com/page/', page_limit=10)
        for data in scraper.scrap_paginated():
            for item in data:
                author, quote, tags = item[0], item[1], item[2]
                user = self._create_user(author)

                db_tags = []
                for tag in tags.split('\n'):
                    tag = tag.strip()
                    if tag == "Tags:" or tag == "":
                        continue
                    db_tags.append(self._create_tag(tag))

                self._create_quote(quote, user, db_tags)

    def _create_user(self, full_name):
        names = full_name.split(" ")
        first_name = names[0]
        last_name = " ".join(names[1:])
        user, _ = User.objects.get_or_create(
            username=full_name, first_name=first_name, last_name=last_name)
        return user

    def _create_tag(self, tag):
        tag, _ = Tags.objects.get_or_create(name=tag)
        return tag

    def _create_quote(self, quote, user, tags):
        quote, _ = Quotes.objects.get_or_create(text=quote, user_id=user)
        for tag in tags:
            quote.tag.add(tag)
