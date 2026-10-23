resource "aws_security_group" "instance" {
  count       = var.create ? 1 : 0
  name        = "${var.name}-instance"
  description = "Instance egress for patching and SSM. No inbound SSH."
  vpc_id      = var.vpc_id

  egress {
    description = "Outbound HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${var.name}-instance" })
}

resource "aws_launch_template" "this" {
  count       = var.create ? 1 : 0
  name_prefix = "${var.name}-"

  image_id      = data.aws_ami.al2023[0].id
  instance_type = var.instance_type

  iam_instance_profile {
    name = var.instance_profile_name
  }

  vpc_security_group_ids = [aws_security_group.instance[0].id]

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size = 8
      volume_type = "gp3"
      encrypted   = true
    }
  }

  tag_specifications {
    resource_type = "instance"
    tags          = var.tags
  }
}

data "aws_ami" "al2023" {
  count       = var.create ? 1 : 0
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_autoscaling_group" "this" {
  count               = var.create ? 1 : 0
  name                = var.name
  min_size            = 0
  max_size            = 2
  desired_capacity    = var.desired_capacity
  vpc_zone_identifier = var.subnet_ids

  launch_template {
    id      = aws_launch_template.this[0].id
    version = "$Latest"
  }

  dynamic "tag" {
    for_each = var.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}
