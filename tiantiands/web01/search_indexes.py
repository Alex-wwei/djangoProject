# coding=utf-8
from haystack import indexes
from .models import product


class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
        # return self.get_model().objects.filter(isDelete=False)