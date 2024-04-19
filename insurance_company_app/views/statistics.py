from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.db.models import Sum, Avg, Count
from django.utils import timezone
import statistics
import plotly.graph_objs as go
from ..models import InsuranceAgent, InsuranceContract, InsuranceClient


@login_required
@permission_required('insurance_company_app.view_statistics')
def statistics(request):
    total_sales = get_total_sales()
    sales_statistics = get_sales_statistics()
    clients_age_statistics = get_clients_age_statistics()
    most_popular_insurance_type = get_most_popular_insurance_type()
    agent_statistics = get_agent_statistics()

    return render(request, 'common/statistics.html',
                  {"total_sales": total_sales,
                   "sales_statistics": sales_statistics,
                   "clients_age_statistics": clients_age_statistics,
                   "most_popular_insurance_type": most_popular_insurance_type,
                   "agent_statistics": agent_statistics})


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
    age_stats = InsuranceClient.objects.aggregate(
        avg_age=Avg('age'),
        median_age=statistics.median('age')
    )
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


def visualize_sales_per_agent(request):
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

    return render(request, 'common/chart.html', {"chart_div": chart})
