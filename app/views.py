from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from chartjs.views.lines import BaseLineChartView
from .models import Item
from .filters import ItemFilter
from .forms import ItemForm
from .consts import *
import cx_Oracle


# Create your views here.
class ItemFilterView(LoginRequiredMixin, PaginationMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    queryset = Item.objects.all().order_by('id')

    # Settings for pure_pagination.
    paginate_by = 10
    object = Item

    # Save search condition in session.
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')


class ItemMetricsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select metric_name,value from v$sysmetric where group_id=2")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_metrics.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemMetricsHistoryView(LoginRequiredMixin, DetailView, BaseLineChartView):
    def get(self, request, pk, path):
        params = {'metric_name': path}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$sysmetric_history where group_id = 2 and metric_name = :metric_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_metrics_history.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params})


class ItemMetricsSummaryView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path):
        params = {'metric_name': path}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_hist_sysmetric_summary where group_id = 2 and metric_name = :metric_name and begin_time >= sysdate-14 order by begin_time desc", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_metrics_summary.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params})


class ItemObjectUsersView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select username from dba_users order by username")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_users.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemObjectTablesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select owner, table_name, tablespace_name from dba_tables where owner = :user_name order by tablespace_name, table_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_tables.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params})


class ItemObjectTableColumnsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user, path_table):
        params = {'user_name': path_user, 'table_name': path_table}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_tab_columns where owner = :user_name and table_name = :table_name order by column_id", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_table_columns.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectConstraintsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user, path_table):
        params = {'user_name': path_user, 'table_name': path_table}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_constraints where owner = :user_name and table_name = :table_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_constraints.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectIndexesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user, path_table):
        params = {'user_name': path_user, 'table_name': path_table}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_indexes where owner = :user_name and table_name = :table_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_indexes.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectIndexColumnsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user, path_table):
        params = {'user_name': path_user, 'table_name': path_table}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_ind_columns where table_owner = :user_name and table_name = :table_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_index_columns.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectViewsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_views where owner = :user_name order by view_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_views.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectProceduresView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_procedures where owner = :user_name order by object_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_procedures.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectQueuesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_queues where owner = :user_name order by name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_queues.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectSequencesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_sequences where sequence_owner = :user_name order by sequence_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_sequences.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectSynonymsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_synonyms where table_owner = :user_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_synonyms.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectTabPartitionsView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_tab_partitions where table_owner = :user_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_tab_partitions.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemObjectTriggersView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path_user):
        params = {'user_name': path_user}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_triggers where table_owner = :user_name", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_object_triggers.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params, 'desc':desc})


class ItemPrivilegesView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select distinct grantee from dba_tab_privs order by grantee")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_privileges.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemPrivilegesRoleView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path):
        params = {'grantee': path}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_role_privs where grantee = :grantee order by grantee, granted_role", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_privileges_role.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params})


class ItemPrivilegesSysView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path):
        params = {'grantee': path}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_sys_privs where grantee = :grantee order by grantee, privilege", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_privileges_sys.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params})


class ItemPrivilegesTabView(LoginRequiredMixin, DetailView):
    def get(self, request, pk, path):
        params = {'grantee': path}
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from dba_tab_privs where grantee = :grantee order by grantee, privilege", params)
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_privileges_tab.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result, 'params': params})


class ItemDynamicPerformanceViewsListView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        # print(vars())
        return render(request, 'app/item_dynamic_performance_views_list.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port})


class ItemDynamicPerformanceDatabaseView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$database")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_database.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceInstanceView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$instance")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_instance.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceLicenseView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$license")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_license.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceNlsParametersView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$nls_parameters")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_nls_parameters.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceOptionView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$option")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_option.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceOsstatView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$osstat")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_osstat.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceParameterView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select name, value, description from v$parameter")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_parameter.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformancePgastatView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$pgastat")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_pgastat.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceResourceLimitView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$resource_limit")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_resource_limit.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceSgainfoView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$sgainfo")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_sgainfo.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceSgastatView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$sgastat")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_sgastat.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceSysstatView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$sysstat")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_sysstat.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})


class ItemDynamicPerformanceVersionView(LoginRequiredMixin, DetailView):
    def get(self, request, pk):
        model = Item
        queryset = model.objects.values(
            'id', 'service_name', 'host_name', 'port').get(id=pk)
        id = queryset['id']
        service_name = queryset['service_name']
        host_name = queryset['host_name']
        port = queryset['port']
        conn = cx_Oracle.connect(
            CONNECT_USER, CONNECT_PASSWORD, host_name + ":" + str(port) + "/" + service_name)
        cursor = conn.cursor()
        cursor.execute("select * from v$version")
        desc = [d[0].replace('#', '') for d in cursor.description]
        result = [dict(zip(desc, line)) for line in cursor]
        cursor.close()
        # print(vars())
        return render(request, 'app/item_dynamic_performance_version.html', {'id': id, 'service_name': service_name, 'host_name': host_name, 'port': port, 'result': result})
