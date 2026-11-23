# [IaC] Misconfigurations volontaires (Checkov / tfsec / Trivy)
provider "aws" {
  region     = "eu-west-3"
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

resource "aws_s3_bucket" "data" {
  bucket = "devsecops-lab-data"
  acl    = "public-read" # bucket public, sans chiffrement ni versioning
}

resource "aws_security_group" "open" {
  name = "open-sg"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # tout ouvert
  }
}

resource "aws_db_instance" "db" {
  identifier          = "lab-db"
  engine              = "mysql"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  username            = "admin"
  password            = "admin123" # mot de passe en dur
  publicly_accessible = true
  storage_encrypted   = false
  skip_final_snapshot = true
}
