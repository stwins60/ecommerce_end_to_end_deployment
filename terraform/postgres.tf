resource "kubernetes_namespace_v1" "postgres_ns" {
  metadata {
    name = "postgres-ns"
  }
}

resource "kubernetes_config_map_v1" "postgres_cm" {
  metadata {
    name      = "postgres-config"
    namespace = kubernetes_namespace_v1.postgres_ns.metadata[0].name
  }
  data = {
    POSTGRES_DB   = "ecommercedb"
    POSTGRES_HOST = "postgres-service"
    POSTGRES_PORT = "5432"
  }
}

resource "kubernetes_secret_v1" "postgres_secret" {
  metadata {
    name      = "postgres-config"
    namespace = kubernetes_namespace_v1.postgres_ns.metadata[0].name
  }
  data = {
    POSTGRES_USER     = base64encode("postgres")
    POSTGRES_PASSWORD = base64encode("postgres")
  }
}

resource "kubernetes_deployment_v1" "postgres_deploy" {
  metadata {
    namespace = kubernetes_namespace_v1.postgres_ns.metadata[0].name
    name      = "postgres-server"
  }
  spec {
    selector {
      match_labels = {
        app = "postgres"
      }
    }
    template {
      metadata {
        labels = {
          app = "postgres"
        }
      }
      spec {
        container {
          name  = "postgres"
          image = "postgres:15"
          port {
            container_port = 5432
          }
          env_from {
            config_map_ref {
              name = kubernetes_config_map_v1.postgres_cm.metadata[0].name
            }
          }
          env_from {
            secret_ref {
              name = kubernetes_secret_v1.postgres_secret.metadata[0].name
            }
          }
          volume_mount {
            name       = "postgres-storage"
            mount_path = "/var/lib/postgresql/data"
          }
        }
        volume {
          name = "postgres-storage"
          empty_dir {}
        }
      }
    }
  }
}

resource "kubernetes_service_v1" "postgres_svc" {
  metadata {
    namespace = kubernetes_namespace_v1.postgres_ns.metadata[0].name
    name      = "postgres-service"
  }
  spec {
    selector = {
      app = "postgres"
    }
    port {
      port        = 5432
      target_port = 5432
    }
    cluster_ip = "None"
  }
}