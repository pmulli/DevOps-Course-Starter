terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
  
  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "tfstate19497"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }

}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "AmericanExpress21Group2_PaulMullineux_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name = "${var.prefix}-terraformed-asp"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind = "Linux"
  reserved = true
 
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name = "${var.prefix}-pdm-todo-exercise12"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|pmullineux/todo:latest"
  }
  
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "DB_CONNECTION_URL" = azurerm_cosmosdb_account.db.connection_strings[0]
    "CLIENT_ID"="${var.CLIENT_ID}"
    "CLIENT_SECRET"="${var.CLIENT_SECRET}"
    "OAUTHLIB_INSECURE_TRANSPORT"="1"
    "FLASK_APP"="todo_app/app"
    "FLASK_ENV"="development"
    "SECRET_KEY"="secret-key"
    "TODO_BOARD_ID"="609542268e084d62bd913af7"
    "TODO_DB_NAME"="todo"
  }
}

resource "azurerm_cosmosdb_account" "db" {
  name                = "${var.prefix}-pdm-todo-cosmos-db"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "EnableServerless"
  }
  
  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "todo-db" {
  name                = "${var.prefix}-pdm-todo-cosmos-mongo-db"
  resource_group_name = azurerm_cosmosdb_account.db.resource_group_name
  account_name        = azurerm_cosmosdb_account.db.name
  lifecycle {
    prevent_destroy = false
  }
}