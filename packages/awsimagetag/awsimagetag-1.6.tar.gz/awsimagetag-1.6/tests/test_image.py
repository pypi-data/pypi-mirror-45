#!/usr/bin/env python3

import unittest2 as unittest
from awsimagetag.model import ImageMetadata

class ImageMetaData_Tests(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.image_metadata = ImageMetadata(
          "arn:aws:ec2:us-west-2:565294218468:image/ami-072c61dc4163ab947",
          "admin-engine-201806160022"
    )

  def test_service(self):
    self.assertEqual(self.image_metadata.service, 'ec2')
  
  def test_region(self):
    self.assertEqual(self.image_metadata.region, 'us-west-2')

  def test_account_number(self):
    self.assertEqual(self.image_metadata.account_number, '565294218468')

  def test_resource_type(self):
    self.assertEqual(self.image_metadata.resource_type, 'image')

  def test_image_id(self):
    self.assertEqual(self.image_metadata.image_id, 'ami-072c61dc4163ab947')


if __name__ == '__main__':
    unittest.main()