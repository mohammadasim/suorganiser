from django.shortcuts import get_object_or_404


class GetObjectMixin:
    model = None

    def get_object(self, year, month, slug):
        return get_object_or_404(self.model,
                                 pub_date__year=year,
                                 pub_date__month=month,
                                 slug__iexact=slug)
