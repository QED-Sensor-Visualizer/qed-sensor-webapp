from scripts import runInPod

print("Installing World Map Panel...")
runInPod("grafana", "grafana-cli plugins install grafana-worldmap-panel")
print("Installing Video Panel...")
runInPod("grafana", "grafana-cli plugins install innius-video-panel")
while True:
    print("Any other plugins to install?")
    answer=input().lower().replace(" ","")
    if answer=="" or answer=="no" or answer=="N": break
    print("Installing '"+answer+"'...")
    runInPod("grafana", "grafana-cli plugins install "+answer)
print("\nTo apply the new plugins, restart the Kubernetes cluster.")