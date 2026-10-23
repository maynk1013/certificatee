{{/*
Expand the chart name.
*/}}
{{- define "demo-web.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Fully qualified name.
*/}}
{{- define "demo-web.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Common labels.
*/}}
{{- define "demo-web.labels" -}}
app.kubernetes.io/name: {{ include "demo-web.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: demo-web
{{- end -}}

{{/*
Selector labels. Keep these stable across upgrades.
*/}}
{{- define "demo-web.selectorLabels" -}}
app.kubernetes.io/name: {{ include "demo-web.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
