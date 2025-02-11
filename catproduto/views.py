from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from catproduto.models import Categoria, Produto


class IndexView(TemplateView):
    template_name = 'index.html'


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'produtos/categorias.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        return context


class ProdutosListView(ListView):
    model = Produto
    template_name = 'produtos/categorias.html'
    context_object_name = 'produtos'
    queryset = Produto.disponiveis.all()

    def get_queryset(self): # removi o parâmetro daqui
        qs = super().get_queryset()
        slugcat = self.kwargs['slugcat'] # obtive o parâmetro dos argumentos passados na requisição
        if slugcat:
            cat = Categoria.objects.get(slug=slugcat) # acrescentei o objects.
            qs = qs.filter(categoria=cat)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slugcat = self.kwargs['slugcat']
        if slugcat:
            context['categoria'] = Categoria.objects.get(slug=slugcat)
            context['categorias'] = Categoria.objects.all()
        return context


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produtos/detalheProd.html'
    context_object_name = 'produto'

    def get_queryset(self):
        return Produto.objects.disponiveis.all()

    def get_object(self):
        slug_prod = self.kwargs['slugProd']
        return get_object_or_404(Produto, slug=slug_prod)

