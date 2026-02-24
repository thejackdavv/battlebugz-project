class PaginatorMixin:

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get('per_page')
        if per_page:
            try:
                return int(per_page)
            except (TypeError, ValueError):
                pass
        return super().get_paginate_by(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['per_page_choices'] = [2, 4, 8, 16, 32]
        context['paginate_by'] = self.get_paginate_by(self.get_queryset())
        return context

class SearchBarMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(type__icontains=q)
        return qs

class CombinedMixin(PaginatorMixin, SearchBarMixin):
    pass