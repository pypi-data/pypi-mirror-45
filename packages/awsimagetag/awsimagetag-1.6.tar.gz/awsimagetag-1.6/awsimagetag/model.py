import json


class ImageMetadata:
  """
  Same as AWS Amazon Resource Name format
  Parameters
  __________
  arn: amazon arn
    arn:aws:ec2:us-west-2:565284218568:image/ami-072c61da4160ab947
  image_name: amazon image name
    AMI Name
  """

  def __init__(self, arn, image_name):
    self.arn = arn
    self.image_name = image_name

  @property
  def service(self):
    return self.arn_array()[2]
  
  @property
  def region(self):
    return self.arn_array()[3]

  @property
  def account_number(self):
    return self.arn_array()[4]
  
  @property
  def resource_type(self):
    return self.arn_array()[5].split('/')[0]
  
  @property
  def image_id(self):
    return self.arn_array()[5].split('/')[1]
  
  def arn_array(self):
    return self.arn.split(':')
  

  