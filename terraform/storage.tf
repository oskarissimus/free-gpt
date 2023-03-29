data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../mercury"
  output_path = "${path.module}/function.zip"

  excludes = [
    ".env",
    "pyproject.toml",
    "README.md",
    "poetry.lock",
    "tests/**",
    "__pycache__/**",
    ".pytest_cache/**",
  ]
}

resource "google_storage_bucket" "chatgpt_function_bucket" {
  name     = "chatgpt-function-bucket-${random_string.bucket_suffix.result}"
  location = var.region
}

resource "google_storage_bucket" "chatgpt_response_bucket" {
  name     = "chatgpt-response-bucket-${random_string.bucket_suffix.result}"
  location = var.region
}

resource "google_storage_bucket_object" "chatgpt_function_archive" {
  name   = "function.zip"
  bucket = google_storage_bucket.chatgpt_function_bucket.name
  source = data.archive_file.function_zip.output_path
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}
