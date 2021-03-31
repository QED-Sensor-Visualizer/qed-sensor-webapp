from kubipy.utils import minipy

from scripts import sCall, sOpen, sKill

grafanaInstance = sOpen('kubectl --namespace default port-forward $(kubectl get pods --namespace default -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana-release" -o jsonpath="{.items[0].metadata.name}") 3000')