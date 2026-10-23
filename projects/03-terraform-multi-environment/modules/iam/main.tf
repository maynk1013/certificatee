data "aws_iam_policy_document" "assume" {
  count = var.create ? 1 : 0
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "operate" {
  count = var.create ? 1 : 0
  statement {
    sid = "ReadOwnInstanceTags"
    actions = [
      "ec2:DescribeInstances",
      "ec2:DescribeTags",
    ]
    resources = ["*"]
  }
  statement {
    sid = "WriteInstanceLogs"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:log-group:/aws/ec2/${var.name}:*"]
  }
}

resource "aws_iam_role" "instance" {
  count              = var.create ? 1 : 0
  name               = "${var.name}-instance"
  assume_role_policy = data.aws_iam_policy_document.assume[0].json
  tags               = var.tags
}

resource "aws_iam_role_policy" "operate" {
  count  = var.create ? 1 : 0
  name   = "${var.name}-operate"
  role   = aws_iam_role.instance[0].id
  policy = data.aws_iam_policy_document.operate[0].json
}

resource "aws_iam_instance_profile" "instance" {
  count = var.create ? 1 : 0
  name  = "${var.name}-instance"
  role  = aws_iam_role.instance[0].name
  tags  = var.tags
}
