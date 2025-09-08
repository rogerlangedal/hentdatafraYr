// High-level composition (example). Adjust parameters and API versions for your environment.
param location string = resourceGroup().location
param sqlServerName string
param dbName string = 'weather'
param aadAdminObjectId string
param containerAppEnvId string  // existing Container Apps Environment resourceId
param acrServer string          // e.g. myregistry.azurecr.io
param image string              // e.g. myregistry.azurecr.io/weather-etl:latest
param schedule string = '5,35 * * * *'

module sql '../modules/sql.bicep' = {
  name: 'sql'
  params: {
    location: location
    sqlServerName: sqlServerName
    dbName: dbName
    aadAdminObjectId: aadAdminObjectId
  }
}

module job '../modules/containerapp-job.bicep' = {
  name: 'job'
  params: {
    location: location
    jobName: 'weather-etl-job'
    containerAppEnvId: containerAppEnvId
    acrServer: acrServer
    image: image
    schedule: schedule
    sqlServerFqdn: sql.outputs.sqlFqdn
    dbName: dbName
  }
}
