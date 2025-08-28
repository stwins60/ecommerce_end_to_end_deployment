resource "kubernetes_config_map_v1" "cm" {
  metadata {
    name      = "ecommerce-app-config"
    namespace = var.namespace
  }
  data = {
    FLASK_ENV    = "ENVIRONMENT"
    DATABASE_URL = "postgresql://postgres:postgres@postgres-service.postgres-ns.svc.cluster.local:5432/ecommercedb"
  }
}

resource "kubernetes_deployment_v1" "this" {
  metadata {
    name = "ecommerce-app"
    labels = {
      app = "ecommerce-app"
    }
    namespace = var.namespace
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
          name  = "ecommerce-app"
          image = "idrisniyi94/ecommerce_demo:${var.image_tag}"
          port {
            container_port = 5000
          }
          env_from {
            config_map_ref {
              name = kubernetes_config_map_v1.cm.metadata[0].name
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "svc" {
  metadata {
    name      = "ecommerce-svc"
    namespace = var.namespace
  }
  spec {
    selector = {
      app = "ecommerce-app"
    }
    port {
      port        = 5000
      target_port = 5000
    }
    type = "NodePort"
  }
}