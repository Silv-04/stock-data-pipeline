resource "aws_instance" "ec2_ubuntu_vm" {
  ami           = "ami-0b0b91f00804b5b53"
  instance_type = "t2.micro"
  key_name      = "mykey"
  tags = {
    Name = "Instance EC2 Ubuntu"
    Owner = "JL"
    Environment = "test"
  }
  
  vpc_security_group_ids = ["${aws_security_group.default.id}"] 
}

# Default EC2 Ubuntu user is "ubuntu"
