resource "aws_key_pair" "mykey" {
  key_name   = "mykey"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7udJwV+usXe1RFyrvbO9grvaVnv3zSGpFkGy8ysal7PwIMyWdHkk9vB9oSxRybKCy67qZDve1KoUOcyP2xE66p7UDlTRvrCpXH5f/QmnG88sHv1sIjQZc8AQrvzMemICc37S7WsNAP7ui1MgwseTQ1qHbth8svF34mA3PveNyjzIhKswsxPc63NI688zGhhe0P9zlXdjJLDb9UoRZiuoaRIT0pCf2Az8LRztB0jhbtdn9Q7h0lW49Knrw9QzdW2ggr+SPdgvLwMtpOm9Uq6yJhk9SrZHBUuxPFimQafZn3YXeU0qSS3NBk3CNtTqCZK4CDLM0kikzPlWTM9IAFD8H john-@LAPTOP-E3A20OJJ"

  tags = {
    Name        = "Key Pair for EC2 instances"
    Environment = "test"
  }
}

