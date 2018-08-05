from django.urls import path
from .views import ItemFilterView
from .views import ItemDetailView
from .views import ItemCreateView
from .views import ItemUpdateView
from .views import ItemDeleteView
from .views import ItemMetricsView
from .views import ItemMetricsHistoryView
from .views import ItemMetricsSummaryView
from .views import ItemObjectUsersView
from .views import ItemObjectTablesView
from .views import ItemObjectTableColumnsView
from .views import ItemObjectConstraintsView
from .views import ItemObjectIndexesView
from .views import ItemObjectIndexColumnsView
from .views import ItemObjectViewsView
from .views import ItemObjectProceduresView
from .views import ItemObjectQueuesView
from .views import ItemObjectSequencesView
from .views import ItemObjectSynonymsView
from .views import ItemObjectTabPartitionsView
from .views import ItemObjectTriggersView
from .views import ItemPrivilegesView
from .views import ItemPrivilegesRoleView
from .views import ItemPrivilegesSysView
from .views import ItemPrivilegesTabView
from .views import ItemDynamicPerformanceViewsListView
from .views import ItemDynamicPerformanceDatabaseView
from .views import ItemDynamicPerformanceInstanceView
from .views import ItemDynamicPerformanceLicenseView
from .views import ItemDynamicPerformanceNlsParametersView
from .views import ItemDynamicPerformanceOptionView
from .views import ItemDynamicPerformanceOsstatView
from .views import ItemDynamicPerformanceParameterView
from .views import ItemDynamicPerformancePgastatView
from .views import ItemDynamicPerformanceResourceLimitView
from .views import ItemDynamicPerformanceSgainfoView
from .views import ItemDynamicPerformanceSgastatView
from .views import ItemDynamicPerformanceSysstatView
from .views import ItemDynamicPerformanceVersionView


urlpatterns = [
    path('', ItemFilterView.as_view(), name='index'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/metrics/', ItemMetricsView.as_view(), name='metrics'),
    path('detail/<int:pk>/metrics/history/<path>', ItemMetricsHistoryView.as_view(), name='metrics_history'),
    path('detail/<int:pk>/metrics/summary/<path>', ItemMetricsSummaryView.as_view(), name='metrics_summary'),
    path('detail/<int:pk>/object_users/', ItemObjectUsersView.as_view(), name='object_users'),
    path('detail/<int:pk>/object_tables/<path_user>', ItemObjectTablesView.as_view(), name='object_tables'),
    path('detail/<int:pk>/object_table_columns/<path_user>/<path_table>', ItemObjectTableColumnsView.as_view(), name='object_table_columns'),
    path('detail/<int:pk>/object_constraints/<path_user>/<path_table>', ItemObjectConstraintsView.as_view(), name='object_constraints'),
    path('detail/<int:pk>/object_indexes/<path_user>/<path_table>', ItemObjectIndexesView.as_view(), name='object_indexes'),
    path('detail/<int:pk>/object_index_columns/<path_user>/<path_table>', ItemObjectIndexColumnsView.as_view(), name='object_index_columns'),
    path('detail/<int:pk>/object_views/<path_user>', ItemObjectViewsView.as_view(), name='object_views'),
    path('detail/<int:pk>/object_procedures/<path_user>', ItemObjectProceduresView.as_view(), name='object_procedures'),
    path('detail/<int:pk>/object_queues/<path_user>', ItemObjectQueuesView.as_view(), name='object_queues'),
    path('detail/<int:pk>/object_sequences/<path_user>', ItemObjectSequencesView.as_view(), name='object_sequences'),
    path('detail/<int:pk>/object_synonyms/<path_user>', ItemObjectSynonymsView.as_view(), name='object_synonyms'),
    path('detail/<int:pk>/object_tab_partitions/<path_user>', ItemObjectTabPartitionsView.as_view(), name='object_tab_partitions'),
    path('detail/<int:pk>/object_triggers/<path_user>', ItemObjectTriggersView.as_view(), name='object_triggers'),
    path('detail/<int:pk>/privileges/', ItemPrivilegesView.as_view(), name='privileges'),
    path('detail/<int:pk>/privileges/role/<path>', ItemPrivilegesRoleView.as_view(), name='privileges_role'),
    path('detail/<int:pk>/privileges/sys/<path>', ItemPrivilegesSysView.as_view(), name='privileges_sys'),
    path('detail/<int:pk>/privileges/tab/<path>', ItemPrivilegesTabView.as_view(), name='privileges_tab'),
    path('detail/<int:pk>/v$/', ItemDynamicPerformanceViewsListView.as_view(), name='v$'),
    path('detail/<int:pk>/v$database/', ItemDynamicPerformanceDatabaseView.as_view(), name='v$database'),
    path('detail/<int:pk>/v$instance/', ItemDynamicPerformanceInstanceView.as_view(), name='v$instance'),
    path('detail/<int:pk>/v$license/', ItemDynamicPerformanceLicenseView.as_view(), name='v$license'),
    path('detail/<int:pk>/v$nls_parameters/', ItemDynamicPerformanceNlsParametersView.as_view(), name='v$nls_parameters'),
    path('detail/<int:pk>/v$option/', ItemDynamicPerformanceOptionView.as_view(), name='v$option'),
    path('detail/<int:pk>/v$osstat/', ItemDynamicPerformanceOsstatView.as_view(), name='v$osstat'),
    path('detail/<int:pk>/v$parameter/', ItemDynamicPerformanceParameterView.as_view(), name='v$parameter'),
    path('detail/<int:pk>/v$pgastat/', ItemDynamicPerformancePgastatView.as_view(), name='v$pgastat'),
    path('detail/<int:pk>/v$resource_limit/', ItemDynamicPerformanceResourceLimitView.as_view(), name='v$resource_limit'),
    path('detail/<int:pk>/v$sgainfo/', ItemDynamicPerformanceSgainfoView.as_view(), name='v$sgainfo'),
    path('detail/<int:pk>/v$sgastat/', ItemDynamicPerformanceSgastatView.as_view(), name='v$sgastat'),
    path('detail/<int:pk>/v$sysstat/', ItemDynamicPerformanceSysstatView.as_view(), name='v$sysstat'),
    path('detail/<int:pk>/v$version/', ItemDynamicPerformanceVersionView.as_view(), name='v$version'),
]
