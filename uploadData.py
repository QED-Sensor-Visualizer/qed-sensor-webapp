import requests as req
import json
from scripts import sCall, sReturn
from tkinter.filedialog import askopenfilename, uploadDashboard

filename = askopenfilename()
if filename == ():
    exit()
token = sReturn(
    'kubectl get secret visualizer-release-influxdb -o jsonpath="{.data.admin-user-token}" | base64 --decode')
print("Enter a lower bound for the data's time range.")
start = input()
print("(Optional) Enter a lower bound for the data's time range.")
end = input()
rangeStr = "start: "+start
if end != "":
    rangeStr += " end: "+end

sCall('influx  write -t '+token+' -o vis-org -b vis-bucket -f '+filename +
      ' --header "#constant measurement, abc" --header "#datatype dateTime:RFC3339,double,tag"')

data = {"panels":[{"targets": [{
    "query": "from(bucket:\"vis-bucket\")\n|> range("+rangeStr+")\n|> yield()"
}]}]}
with open("grafanaData/dashboard.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
uploadDashboard()