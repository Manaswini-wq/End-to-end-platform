variable "project_id" { type = string }
variable "region" { default = "us-central1" }

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "data_lake" {
  name          = "${var.project_id}-data-lake"
  location      = var.region
  force_destroy = true

  lifecycle_rule {
    action { type = "Delete" }
    condition { age = 90 }
  }
}

resource "google_bigquery_dataset" "raw" {
  dataset_id = "retail_raw"
  location   = var.region
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = "retail_analytics"
  location   = var.region
}
