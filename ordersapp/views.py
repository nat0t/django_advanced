from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, \
    UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import BaseFormSet

from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from basketapp.models import Basket


class OrderList(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemCreate(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm,
                                                     extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                basket_items.delete()
            else:
                formset = OrderFormSet()
        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemCreate, self).form_valid(form)


class OrderItemUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm, extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST,
                                              instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)

        # if self.request.POST:
        #     formset = OrderFormSet(self.request.POST)
        # else:
        #     basket_items = Basket.objects.filter(user=self.request.user)
        #     if len(basket_items):
        #         OrderFormSet = inlineformset_factory(Order, OrderItem,
        #                                              form=OrderItemForm,
        #                                              extra=len(basket_items))
        #         formset = OrderFormSet()
        #         for num, form in enumerate(formset.forms):
        #             form.initial['product'] = basket_items[num].product
        #             form.initial['quantity'] = basket_items[num].quantity
        #         basket_items.delete()
        #     else:
        #         formset = OrderFormSet()
        # data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemCreate, self).form_valid(form)


class OrderDelete(DeleteView):
   model = Order
   success_url = reverse_lazy('ordersapp:orders_list')


class OrderRead(DetailView):
   model = Order
   template_name = 'ordersapp/order_detail.html'

   def get_context_data(self, **kwargs):
       context = super(OrderRead, self).get_context_data(**kwargs)
       context['title'] = 'заказ/просмотр'
       return context


def order_forming_complete(request, pk):
   order = get_object_or_404(Order, pk=pk)
   order.status = Order.SENT_TO_PROCEED
   order.save()
   return HttpResponseRedirect(reverse('ordersapp:orders_list'))