import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from statistics import *
import plotly.graph_objs as go
from ..models import InsuranceAgent, InsuranceContract, InsuranceClient


def get_total_sales():
    total_sales = InsuranceContract.objects.aggregate(total_sales=Sum('insurance_sum'))['total_sales']
    return total_sales


def get_sales_statistics():
    sales_stats = InsuranceContract.objects.aggregate(
        avg_sales=Avg('insurance_sum'),
        total_sales=Sum('insurance_sum')
    )
    return sales_stats


def get_clients_age_statistics():
    all_ages = InsuranceClient.objects.values_list('age', flat=True)
    median_age = median(all_ages)

    age_stats = InsuranceClient.objects.aggregate(
        avg_age=Avg('age'),
    )
    age_stats['median_age'] = median_age
    return age_stats


def get_most_popular_insurance_type():
    most_popular_type = InsuranceContract.objects.values('insurance_type__name').annotate(
        total_sum=Sum('insurance_sum')
    ).order_by('-total_sum').first()
    return most_popular_type


def get_agent_statistics():
    agent_stats = InsuranceAgent.objects.annotate(
        total_contracts=Count('insurancecontract'),
        total_sales=Sum('insurancecontract__insurance_sum'),
        average_sale=Avg('insurancecontract__insurance_sum')
    )
    return agent_stats


def visualize_sales_per_agent():
    agent_stats = InsuranceAgent.objects.annotate(
        total_sales=Sum('insurancecontract__insurance_sum')
    )

    agent_names = [agent.name for agent in agent_stats]
    total_sales = [agent.total_sales for agent in agent_stats]

    data = [
        go.Bar(
            x=agent_names,
            y=total_sales,
            marker=dict(color='green')
        )]

    layout = go.Layout(
        title='Total Sales by Insurance Agent',
        xaxis=dict(title='Insurance Agents'),
        yaxis=dict(title='Total Sales')
    )
    fig = go.Figure(data=data, layout=layout)
    chart = fig.to_html(full_html=False)
    return chart


def visualize_statistics_per_clients_group():
    age_groups = [
        (0, 18),  # Дети
        (19, 35),  # Молодежь
        (36, 60),  # Взрослые
        (61, 100)  # Пожилые
    ]

    clients_in_group = [
        InsuranceClient.objects.filter(age__range=(lower_bound, upper_bound)).count()
        for lower_bound, upper_bound in age_groups
    ]

    labels = ['Дети (0-18)', 'Молодежь(19-35)', 'Взрослые(36-60)', 'Пожилые(61-100)']
    values = clients_in_group

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Распределение клиентов по возрасту')

    chart = fig.to_html(full_html=False)
    return chart
