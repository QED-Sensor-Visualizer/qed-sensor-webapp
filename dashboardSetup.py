from grafanalib.core import (
    Dashboard, Graph,
    OPS_FORMAT, Row,
    single_y_axis, Target, TimeRange, YAxes, YAxis
)


dashboard = Dashboard(
    title="Python generated dashboard",
    rows=[
        Row(panels=[
          Graph(
              title="Prometheus http requests",
              dataSource='default',
              targets=[
                  Target(
                    expr='rate(prometheus_http_requests_total[5m])',
                    legendFormat="{{ handler }}",
                    refId='A',
                  ),
              ],
              yAxes=single_y_axis(format=OPS_FORMAT),
          ),
        ]),
    ],
).auto_panel_ids()