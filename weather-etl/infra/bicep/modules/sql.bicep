// NOTE: Verify API versions with Azure docs before deploying.
param location string
param sqlServerName string
param dbName string
param aadAdminObjectId string  // Entra ID objectId for SQL AAD admin (group or user)

resource sqlServer 'Microsoft.Sql/servers@2023-08-01-preview' = {
  name: sqlServerName
  location: location
  properties: {
    publicNetworkAccess: 'Enabled'
    minimalTlsVersion: '1.2'
  }
  identity: { type: 'SystemAssigned' }
}

resource aadAdmin 'Microsoft.Sql/servers/administrators@2022-05-01-preview' = {
  name: 'activeDirectory'
  parent: sqlServer
  properties: {
    administratorType: 'ActiveDirectory'
    login: 'AadAdmin'
    sid: aadAdminObjectId
    tenantId: tenant().tenantId
  }
}

resource db 'Microsoft.Sql/servers/databases@2024-11-01-preview' = {
  name: '${sqlServerName}/${dbName}'
  location: location
  sku: {
    name: 'S0'
  }
}

output sqlFqdn string = sqlServer.properties.fullyQualifiedDomainName
