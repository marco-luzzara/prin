{{ define "prin.commonMetadata" -}}
namespace: {{ .Global.Release.Namespace }}
labels:
  app.kubernetes.io/name: {{ .Global.Chart.Name }}
  app.kubernetes.io/managed-by: {{ .Global.Release.Service }}
  app.kubernetes.io/instance: {{ .Global.Release.Name }}
  app.kubernetes.io/part-of: {{ .PartOf | quote }}
  app.kubernetes.io/component: {{ .Component | quote }}
{{ end }}