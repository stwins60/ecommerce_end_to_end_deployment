resource "kubernetes_config_map_v1" "this" {
  metadata {
    name = "ecommerce-app-config"
    namespace = "NAMESPACE"
  }
  data = {
    FLASK_ENV = "ENVIRONMENT"
    DATABASE_URL = "postgresql://postgres:postgres@postgres-service.postgres-ns.svc.cluster.local:5432/ecommercedb"
  }
}

resource "kubernetes_deployment_v1" "this" {
  metadata {
    name = "ecommerce-app"
    labels = {
      app = "ecommerce-app"
    }
    namespace = "NAMESPACE"
  }
  spec {
    selector {
      match_labels = {
        app = "ecommerce-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "ecommerce-app"
        }
      }
      spec {
        container {
          name = "ecommerce-app"
          image = "IMAGE_NAME"
          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "this" {
  metadata {
    name = "ecommerce-svc"
    namespace = "NAMESPACE"
  }
  spec {
    selector = {
      app = "ecommerce-app"
    }
    port {
      port = 5000
      target_port = 5000
    }
    type = "NodePort"
  }
}