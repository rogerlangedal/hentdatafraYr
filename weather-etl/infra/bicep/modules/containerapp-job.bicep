// NOTE: Verify API versions before deploying; this is a starter template.
param location string
param jobName string
param containerAppEnvId string
param acrServer string
param image string
param schedule string  // e.g. "5,35 * * * *" for twice per hour
param sqlServerFqdn string
param dbName string

resource job 'Microsoft.App/jobs@2024-02-02-preview' = {
  name: jobName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    environmentId: containerAppEnvId
    configuration: {
      triggerType: 'Schedule'
      scheduleTriggerConfig: {
        cronExpression: schedule
        parallelism: 1
      }
      registries: [
        {
          server: acrServer
          identity: 'system'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'weather'
          image: image
          env: [
            { name: 'USE_MI', value: 'true' },
            { name: 'DB_SERVER', value: '${sqlServerFqdn},1433' },
            { name: 'DB_DATABASE', value: dbName },
            { name: 'MET_USER_AGENT', value: 'bir-weather-etl/0.1 roger@bir.no' }
          ]
        }
      ]
    }
  }
}
